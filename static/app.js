/* Toddler Piano — 前端 (HTML/JS + Web Audio API)
 * 1. 開始畫面：第一次點擊時啟動 AudioContext（iOS/Chrome 規定）
 * 2. 預先下載並解碼 8 個 WAV（Python 產生的） → 按下即發聲，延遲最低
 * 3. 跟唱模式：從 Python 後端 /api/songs 取得旋律，提示下一個要按的鍵
 * 4. 註冊 Service Worker → 可離線、可「加到主畫面」
 */
(() => {
  "use strict";

  const KEYS = [
    { note: "C4", label: "Do",  c: "#EF5350", shade: "#C62828", shape: "circle" },
    { note: "D4", label: "Re",  c: "#FFA726", shade: "#E65100", shape: "square" },
    { note: "E4", label: "Mi",  c: "#FFCA28", shade: "#F9A825", shape: "triangle" },
    { note: "F4", label: "Fa",  c: "#66BB6A", shade: "#2E7D32", shape: "star" },
    { note: "G4", label: "Sol", c: "#26C6DA", shade: "#00838F", shape: "hexagon" },
    { note: "A4", label: "La",  c: "#42A5F5", shade: "#1565C0", shape: "diamond" },
    { note: "B4", label: "Si",  c: "#AB47BC", shade: "#6A1B9A", shape: "moon" },
    { note: "C5", label: "Do",  c: "#EC407A", shade: "#AD1457", shape: "flower" },
  ];

  const MAX_VOLUME = 0.7;          // 保護幼兒聽力：音量上限
  const keysEl = document.getElementById("keys");
  const songsEl = document.getElementById("songs");
  const statusEl = document.getElementById("status");

  let ctx = null, master = null;
  const buffers = {};              // note -> AudioBuffer
  const keyEls = {};               // note -> <button>
  let song = null, songPos = 0;

  /* ---------------- 琴鍵 ---------------- */
  for (const k of KEYS) {
    const b = document.createElement("button");
    b.className = "key";
    b.dataset.note = k.note;
    b.dataset.shape = k.shape;
    b.style.setProperty("--c", k.c);
    b.style.setProperty("--shade", k.shade);
    b.setAttribute("aria-label", `${k.label} ${k.note}`);
    b.innerHTML = `<span class="shape" aria-hidden="true"></span><span>${k.label}</span>`;
    keysEl.appendChild(b);
    keyEls[k.note] = b;
  }

  // pointerdown 比 click 快 ~100ms，且支援多指同時按
  keysEl.addEventListener("pointerdown", (e) => {
    const key = e.target.closest(".key");
    if (!key) return;
    e.preventDefault();
    press(key, e.clientX, e.clientY);
  });
  const release = (e) => {
    const key = e.target.closest && e.target.closest(".key");
    if (key) key.classList.remove("down");
  };
  keysEl.addEventListener("pointerup", release);
  keysEl.addEventListener("pointercancel", release);
  keysEl.addEventListener("pointerleave", release, true);
  document.addEventListener("contextmenu", (e) => e.preventDefault());

  // 實體鍵盤也可以彈（方便錄教學影片）：A S D F G H J K
  const KB = "asdfghjk";
  document.addEventListener("keydown", (e) => {
    const i = KB.indexOf(e.key.toLowerCase());
    if (i >= 0 && !e.repeat) {
      const el = keyEls[KEYS[i].note];
      const r = el.getBoundingClientRect();
      press(el, r.left + r.width / 2, r.top + r.height / 2);
    }
  });
  document.addEventListener("keyup", (e) => {
    const i = KB.indexOf(e.key.toLowerCase());
    if (i >= 0) keyEls[KEYS[i].note].classList.remove("down");
  });

  function press(el, x, y) {
    const note = el.dataset.note;
    el.classList.add("down");
    setTimeout(() => el.classList.remove("down"), 180);
    play(note);
    bubble(el, x, y);
    if (song) advanceSong(note);
  }

  function bubble(el, x, y) {
    const d = document.createElement("div");
    d.className = "bubble";
    d.style.setProperty("--c", el.style.getPropertyValue("--c"));
    d.style.left = x + "px";
    d.style.top = y + "px";
    document.body.appendChild(d);
    setTimeout(() => d.remove(), 950);
  }

  /* ---------------- 聲音 ---------------- */
  async function initAudio() {
    if (ctx) return;
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    const comp = ctx.createDynamicsCompressor();   // 多鍵同按時避免爆音
    master = ctx.createGain();
    master.gain.value = MAX_VOLUME;
    master.connect(comp).connect(ctx.destination);

    await Promise.all(KEYS.map(async ({ note }) => {
      try {
        const res = await fetch(`sounds/${note}.wav`);
        const data = await res.arrayBuffer();
        buffers[note] = await new Promise((ok, fail) =>
          ctx.decodeAudioData(data, ok, fail));      // callback 版相容舊 Safari
      } catch (err) {
        console.warn("sound load failed", note, err);
      }
    }));
  }

  function play(note) {
    if (!ctx) return;
    if (ctx.state === "suspended") ctx.resume();
    const buf = buffers[note];
    if (buf) {
      const src = ctx.createBufferSource();
      src.buffer = buf;
      src.connect(master);
      src.start();
    } else {
      fallbackTone(note);                            // 音檔沒載到時的備援
    }
  }

  function fallbackTone(note) {
    const freq = { C4: 261.63, D4: 293.66, E4: 329.63, F4: 349.23,
                   G4: 392, A4: 440, B4: 493.88, C5: 523.25 }[note];
    const o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime;
    o.type = "triangle";
    o.frequency.value = freq;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.8, t + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 1.2);
    o.connect(g).connect(master);
    o.start(t);
    o.stop(t + 1.3);
  }

  /* ---------------- 跟唱模式（資料來自 Python 後端） ---------------- */
  async function loadSongs() {
    let data = null;
    for (const url of ["api/songs", "songs.json"]) {   // 有後端用 API；GitHub Pages 用靜態檔
      try {
        const r = await fetch(url);
        if (r.ok) { data = await r.json(); break; }
      } catch (_) { /* 試下一個 */ }
    }
    if (!data) return;
    for (const s of data.songs) {
      const b = document.createElement("button");
      b.className = "chip";
      b.dataset.song = s.id;
      b.textContent = s.title;
      b._song = s;
      songsEl.appendChild(b);
    }
  }

  songsEl.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip");
    if (!chip) return;
    songsEl.querySelectorAll(".chip").forEach((c) => c.classList.toggle("active", c === chip));
    song = chip._song || null;
    songPos = 0;
    highlightNext();
  });

  function advanceSong(note) {
    if (note !== song.notes[songPos]) return;        // 按錯不處罰，只是不前進
    songPos++;
    if (songPos >= song.notes.length) {
      keysEl.classList.add("celebrate");
      setTimeout(() => keysEl.classList.remove("celebrate"), 1200);
      songPos = 0;
    }
    highlightNext();
  }

  function highlightNext() {
    Object.values(keyEls).forEach((k) => k.classList.remove("next"));
    if (song) {
      keyEls[song.notes[songPos]].classList.add("next");
      statusEl.textContent = `${songPos + 1} / ${song.notes.length}`;
    } else {
      statusEl.textContent = "";
    }
  }

  /* ---------------- 開始畫面 ---------------- */
  document.getElementById("startBtn").addEventListener("click", async () => {
    document.getElementById("start").classList.add("hidden");
    await initAudio();
    play("C4");
  });

  /* ---------------- PWA ---------------- */
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("sw.js").catch((e) => console.warn("SW", e));
    });
  }

  loadSongs();
})();

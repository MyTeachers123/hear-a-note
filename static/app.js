/* Toddler Piano — 前端 (HTML/JS + Web Audio API)
 * 1. 開始畫面：第一次點擊時啟動 AudioContext（iOS/Chrome 規定）
 * 2. 預先下載並解碼 13 個 WAV（8 白鍵 + 5 黑鍵）（Python 產生的） → 按下即發聲，延遲最低
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
    { note: "B4", label: "Si",  c: "#AB47BC", shade: "#6A1B9A", shape: "heart" },
    { note: "C5", label: "Do",  c: "#EF5350", shade: "#C62828", shape: "arrow", high: true },  // 高八度：同色、向上箭頭、頭頂加點
  ];

  // 黑鍵：between = 夾在哪兩個白鍵中間（位置由 JS 動態計算）
  const BLACK_KEYS = [
    { note: "Cs4", label: "Do♯",  between: ["C4", "D4"] },
    { note: "Ds4", label: "Re♯",  between: ["D4", "E4"] },
    { note: "Fs4", label: "Fa♯",  between: ["F4", "G4"] },
    { note: "Gs4", label: "Sol♯", between: ["G4", "A4"] },
    { note: "As4", label: "La♯",  between: ["A4", "B4"] },
  ];
  const ALL_NOTES = [...KEYS.map((k) => k.note), ...BLACK_KEYS.map((k) => k.note)];

  const SHAPES_SVG = {
    heart: "M50 88 C22 68 6 52 6 33 C6 18 17 8 30 8 C39 8 46 13 50 21 C54 13 61 8 70 8 C83 8 94 18 94 33 C94 52 78 68 50 88 Z",
    arrow: "M50 4 L96 52 L70 52 L70 96 L30 96 L30 52 L4 52 Z",
  };

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
    // 心形、箭頭用 SVG 畫，其他形狀用 CSS
    const svg = SHAPES_SVG[k.shape]
      ? `<svg viewBox="0 0 100 100" aria-hidden="true"><path d="${SHAPES_SVG[k.shape]}"/></svg>` : "";
    const label = k.high ? `<span class="label high">${k.label}</span>` : `<span class="label">${k.label}</span>`;
    b.innerHTML = `<span class="shape" aria-hidden="true">${svg}</span>${label}`;
    b.setAttribute("aria-label", k.high ? `高音 ${k.label} ${k.note}` : `${k.label} ${k.note}`);
    keysEl.appendChild(b);
    keyEls[k.note] = b;
  }

  /* ---------------- 黑鍵圖層（疊在白鍵上方，位置動態計算） ---------------- */
  for (const k of BLACK_KEYS) {
    const b = document.createElement("button");
    b.className = "key black";
    b.dataset.note = k.note;
    b.style.setProperty("--c", "#333");
    b.setAttribute("aria-label", k.label);
    keysEl.appendChild(b);
    keyEls[k.note] = b;
  }

  // 用 offsetLeft/offsetWidth（版面座標），畫面被 CSS 轉 90 度時也不會算錯
  function layoutBlackKeys() {
    for (const k of BLACK_KEYS) {
      const el = keyEls[k.note];
      const L = keyEls[k.between[0]];
      const R = keyEls[k.between[1]];
      const w = L.offsetWidth * 0.6;
      el.style.width  = w + "px";
      el.style.height = L.offsetHeight * 0.55 + "px";
      el.style.left   = (L.offsetLeft + L.offsetWidth + R.offsetLeft) / 2 - w / 2 + "px";
      el.style.top    = L.offsetTop + "px";
    }
  }
  // 視窗大小、手機轉向改變時自動重新對齊
  new ResizeObserver(layoutBlackKeys).observe(keysEl);
  window.addEventListener("orientationchange", () => setTimeout(layoutBlackKeys, 200));
  layoutBlackKeys();

  // 家長開關：顯示／隱藏黑鍵（記住上次的選擇）
  const blackToggle = document.getElementById("blackToggle");
  let showBlack = true;
  try { showBlack = localStorage.getItem("showBlack") !== "0"; } catch (_) {}
  function applyBlack() {
    keysEl.classList.toggle("no-black", !showBlack);
    blackToggle.classList.toggle("active", showBlack);
    blackToggle.setAttribute("aria-pressed", String(showBlack));
  }
  blackToggle.addEventListener("click", () => {
    showBlack = !showBlack;
    try { localStorage.setItem("showBlack", showBlack ? "1" : "0"); } catch (_) {}
    applyBlack();
  });
  applyBlack();

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
  // 黑鍵：W E T Y U（和電腦音樂軟體的標準排法一樣）
  const KB = { a: "C4", s: "D4", d: "E4", f: "F4", g: "G4", h: "A4", j: "B4", k: "C5",
               w: "Cs4", e: "Ds4", t: "Fs4", y: "Gs4", u: "As4" };
  document.addEventListener("keydown", (e) => {
    const note = KB[e.key.toLowerCase()];
    if (note && !e.repeat) {
      if (keyEls[note].classList.contains("black") && keysEl.classList.contains("no-black")) return;
      const el = keyEls[note];
      const r = el.getBoundingClientRect();
      press(el, r.left + r.width / 2, r.top + r.height / 2);
    }
  });
  document.addEventListener("keyup", (e) => {
    const note = KB[e.key.toLowerCase()];
    if (note) keyEls[note].classList.remove("down");
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

    await Promise.all(ALL_NOTES.map(async (note) => {
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
                   G4: 392, A4: 440, B4: 493.88, C5: 523.25,
                   Cs4: 277.18, Ds4: 311.13, Fs4: 369.99, Gs4: 415.3, As4: 466.16 }[note];
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
  /* ---------------- 全螢幕 + 鎖定橫向（防止寶寶誤觸退出） ---------------- */
  const startEl = document.getElementById("start");
  const startHint = document.getElementById("startHint");
  const isInstalled = () =>
    matchMedia("(display-mode: fullscreen), (display-mode: standalone)").matches ||
    navigator.standalone === true;                       // iOS 加到主畫面
  const fsElement = () => document.fullscreenElement || document.webkitFullscreenElement;

  function enterFullscreen() {
    const el = document.documentElement;
    const req = el.requestFullscreen || el.webkitRequestFullscreen;
    if (!req || fsElement()) return Promise.resolve();
    // 必須在點擊當下同步呼叫，瀏覽器才允許
    return Promise.resolve(req.call(el, { navigationUI: "hide" })).catch(() => {});
  }

  async function lockLandscape() {
    try { await screen.orientation.lock("landscape"); } catch (_) { /* iOS 不支援 → 用 CSS 轉向 */ }
  }

  // 攔截「返回」手勢／按鈕：寶寶按到返回不會離開 App
  function trapBack() {
    history.pushState({ toddler: true }, "");
    window.addEventListener("popstate", () => history.pushState({ toddler: true }, ""));
  }

  let started = false;
  document.getElementById("startBtn").addEventListener("click", () => {
    const fs = enterFullscreen();                        // 同步呼叫（使用者手勢內）
    const audio = initAudio();                           // AudioContext 也要在手勢內建立
    startEl.classList.add("hidden");
    fs.then(lockLandscape);
    if (!started) { started = true; trapBack(); }
    audio.then(() => play("C4"));
  });

  // 如果被滑出全螢幕：蓋上「繼續」畫面，點一下就回到全螢幕
  const onFsChange = () => {
    if (!fsElement() && started && !isInstalled()) {
      startHint.textContent = "點一下繼續 · Tap to continue";
      startEl.classList.remove("hidden");
    }
    setTimeout(layoutBlackKeys, 100);
  };
  document.addEventListener("fullscreenchange", onFsChange);
  document.addEventListener("webkitfullscreenchange", onFsChange);

  /* ---------------- PWA ---------------- */
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("sw.js").catch((e) => console.warn("SW", e));
    });
  }

  loadSongs();
})();

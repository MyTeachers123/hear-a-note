/* piano.js — listens to the child's real piano
 *
  * Microphone pitch detection: works with any piano or keyboard, on every device (incl. iPhone, iPad)
 *
  * Privacy: microphone audio is analyzed for pitch on this device only — never recorded, stored or uploaded.
 *
  * API: startMic(onNote), micPermission(), stop() → onNote(noteNumber, "mic")  (60 = middle C)
 *       PianoInput.stop()
 */
(() => {
  "use strict";

  let micStream = null, micCtx = null, timer = null, noteCb = null;

  // ---------------- Microphone + pitch detection (McLeod Pitch Method) ----------------
  // Returns frequency in Hz, or 0 when there is no clear pitch
  function detectPitch(buf, sampleRate) {
    const n = buf.length, minLag = Math.floor(sampleRate / 1100), maxLag = Math.floor(sampleRate / 100);   // down to ~100 Hz (bass C3 = 131 Hz)
    const nsdf = new Float32Array(maxLag + 1);
    for (let tau = minLag; tau <= maxLag; tau++) {
      let acf = 0, m = 0;
      for (let i = 0; i < n - tau; i++) { acf += buf[i] * buf[i + tau]; m += buf[i] * buf[i] + buf[i + tau] * buf[i + tau]; }
      nsdf[tau] = m ? (2 * acf) / m : 0;
    }
    // Take the highest peak of each positive lobe; pick the first one ≥ 0.9 × the max (avoids octave errors)
    const peaks = [];
    let best = 0, bestTau = 0;
    for (let tau = minLag + 1; tau < maxLag; tau++) {
      if (nsdf[tau] > 0 && nsdf[tau] > nsdf[tau - 1] && nsdf[tau] >= nsdf[tau + 1]) {
        peaks.push(tau);
        if (nsdf[tau] > best) { best = nsdf[tau]; bestTau = tau; }
      }
    }
    if (best < 0.75) return 0;                           // not clear enough (noise, talking)
    const tau = peaks.find((t) => nsdf[t] >= 0.9 * best) || bestTau;
    // Parabolic interpolation for a more precise frequency
    const a = nsdf[tau - 1], b = nsdf[tau], c = nsdf[tau + 1];
    const shift = (a - c) / (2 * (a - 2 * b + c) || 1);
    return sampleRate / (tau + shift);
  }
  const freqToNum = (f) => Math.round(69 + 12 * Math.log2(f / 440));

  async function startMic() {
    micStream = await navigator.mediaDevices.getUserMedia({
      audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: false },
    });
    micCtx = new (window.AudioContext || window.webkitAudioContext)();
    const src = micCtx.createMediaStreamSource(micStream);
    const an = micCtx.createAnalyser();
    an.fftSize = 2048;
    src.connect(an);
    const buf = new Float32Array(an.fftSize);

    // Onset detection ("a new key press"): a sudden jump in volume → estimate pitch over the next frames
    // This distinguishes the same note played twice in a row (e.g. C C in Twinkle Twinkle)
    let prevRms = 0, floor = 0.01, waiting = 0, votes = [];
    timer = setInterval(() => {
      an.getFloatTimeDomainData(buf);
      let sum = 0;
      for (let i = 0; i < buf.length; i++) sum += buf[i] * buf[i];
      const rms = Math.sqrt(sum / buf.length);
      floor = Math.min(0.2, floor * 0.995 + (rms < floor ? rms * 0.005 : 0));   // slowly adapts to room noise
      const onset = rms > Math.max(0.012, floor * 3) && rms > prevRms * 1.5;
      prevRms = rms;
      if (onset) { waiting = 8; votes = []; return; }    // let the hammer attack noise pass
      if (waiting > 0) {
        waiting--;
        const f = detectPitch(buf, micCtx.sampleRate);
        if (f) votes.push(freqToNum(f));
        // Two consecutive identical estimates → confirmed
        const k = votes.length;
        if (k >= 2 && votes[k - 1] === votes[k - 2]) {
          waiting = 0;
          noteCb && noteCb(votes[k - 1], "mic");
        }
      }
    }, 25);
  }

  // ---------------- Public API ----------------
  window.PianoInput = {
    // Start listening through the microphone; throws if the user denies it or there is no mic
    async startMic(onNote) {
      noteCb = onNote;
      await startMic();
    },
    // Microphone permission: "granted" | "prompt" (not asked yet) | "denied" (blocked) | "unknown"
    async micPermission() {
      try {
        const p = await navigator.permissions.query({ name: "microphone" });
        return p.state;
      } catch (_) { return "unknown"; }          // some browsers do not support the query
    },
    stop() {
      noteCb = null;
      if (timer) clearInterval(timer), (timer = null);
      if (micStream) micStream.getTracks().forEach((t) => t.stop()), (micStream = null);
      if (micCtx) micCtx.close(), (micCtx = null);
    },
    detectPitch,     // exposed for testing
  };
})();

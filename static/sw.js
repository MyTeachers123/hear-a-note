/* Service Worker: caches every file on first visit so the app then works fully offline.
  * When you change content, bump VERSION; old caches are deleted automatically. */
const VERSION = "toddler-music-box-1.0.14";  // bump on every frontend change (e.g. 1.0.15)
const PCS = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"];
const NOTES = [...PCS.map((p) => p + 3), ...PCS.map((p) => p + 4), "C5"];                // 25 notes
const STAFF = [
  ...[...PCS.map((p) => p + 4), "C5", "clef"].map((n) => `staff/G/${n}.svg`),         // treble clef
  ...[...PCS.map((p) => p + 3), "C4", "clef"].map((n) => `staff/F/${n}.svg`),         // bass clef
  ...[...PCS.map((p) => p + 4), "C5"].map((n) => `staff/G/plain/${n}.svg`),           // reward: no clef
  ...[...PCS.map((p) => p + 3), "C4"].map((n) => `staff/F/plain/${n}.svg`),
];
const PRECACHE = [
  "./",
  "index.html",
  "style.css",
  "app.js",
  "piano.js",
  "songs.json",
  "i18n.json",
  "manifest.webmanifest",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/icon-maskable-512.png",
  "icons/apple-touch-icon.png",
  "icons/favicon-32.png",
  ...NOTES.map((n) => `sounds/${n}.wav`),
  "sounds/oops.wav",                                                   // wrong-note sound
  "media/silence.wav", "media/keep-awake.mp4", "media/keep-awake.webm", // iPhone sound unlock + keep screen on
  ...STAFF,
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(PRECACHE)));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;

  // API: network first (latest melodies), fall back to cache when offline
  if (url.pathname.endsWith("/api/songs")) {
    e.respondWith(
      fetch(e.request)
        .then((r) => { const copy = r.clone(); caches.open(VERSION).then((c) => c.put(e.request, copy)); return r; })
        .catch(() => caches.match(e.request).then((r) => r || caches.match("songs.json")))
    );
    return;
  }

  // Other static files: cache first → fastest and works offline
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then((hit) => hit || fetch(e.request))
  );
});

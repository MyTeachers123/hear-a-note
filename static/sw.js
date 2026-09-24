/* Service Worker：第一次開啟時把所有檔案存進快取，之後完全離線可用。
 * 更新內容時，把 VERSION 加 1，舊快取會被自動清掉。 */
const VERSION = "toddler-music-box-v4";
const NOTES = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "Cs4", "Ds4", "Fs4", "Gs4", "As4"];
const PRECACHE = [
  "./",
  "index.html",
  "style.css",
  "app.js",
  "songs.json",
  "manifest.webmanifest",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/icon-maskable-512.png",
  ...NOTES.map((n) => `sounds/${n}.wav`),
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

  // API：網路優先（拿最新旋律），離線時退回快取
  if (url.pathname.endsWith("/api/songs")) {
    e.respondWith(
      fetch(e.request)
        .then((r) => { const copy = r.clone(); caches.open(VERSION).then((c) => c.put(e.request, copy)); return r; })
        .catch(() => caches.match(e.request).then((r) => r || caches.match("songs.json")))
    );
    return;
  }

  // 其他靜態檔：快取優先 → 最快、可離線
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then((hit) => hit || fetch(e.request))
  );
});

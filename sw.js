/* 日本語ノート — 오프라인 캐시 (홈 화면 추가·비행기 모드 대비) */
const CACHE = 'nihongo-note-v6';
const ASSETS = [
  './', './index.html', './manifest.json',
  './icon.svg', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png',
  './assets/bakugo.jpg', './assets/bakugo-avatar.jpg', './assets/bakugo-portrait.jpg',
  './assets/bakugo-p1.jpg', './assets/bakugo-p2.jpg', './assets/bakugo-p3.jpg',
  './assets/bakugo-p4.jpg', './assets/bakugo-p5.jpg', './assets/bakugo-p6.jpg',
  './assets/bakugo-a1.jpg', './assets/bakugo-a2.jpg', './assets/bakugo-a3.jpg',
  './assets/bakugo-a4.jpg', './assets/bakugo-a5.jpg', './assets/bakugo-a6.jpg',
  './fridge-data.json', './diet-data.json'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE)
      .then(function (c) { return c.addAll(ASSETS).catch(function () {}); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys()
      .then(function (keys) {
        return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;

  /* 냉장고 재료·식단 기록은 네트워크 우선: 새 파일을 올리면 바로 반영되고, 오프라인이면 마지막 사본을 씁니다. */
  if (/\/(fridge|diet)-data\.json$/.test(url.pathname)) {
    const fallback = /\/diet-data\.json$/.test(url.pathname) ? './diet-data.json' : './fridge-data.json';
    e.respondWith(
      fetch(req, { cache: 'no-store' }).then(function (r) {
        if (r && r.ok) { const copy = r.clone(); caches.open(CACHE).then(function (c) { c.put(req, copy); }); }
        return r;
      }).catch(function () {
        return caches.match(req).then(function (hit) { return hit || caches.match(fallback); });
      })
    );
    return;
  }

  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then(function (r) {
        const copy = r.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return r;
      }).catch(function () {
        return caches.match(req).then(function (hit) { return hit || caches.match('./index.html'); });
      })
    );
    return;
  }

  e.respondWith(
    caches.match(req).then(function (hit) {
      const net = fetch(req).then(function (r) {
        if (r && r.ok) { const copy = r.clone(); caches.open(CACHE).then(function (c) { c.put(req, copy); }); }
        return r;
      }).catch(function () { return hit; });
      return hit || net;
    })
  );
});

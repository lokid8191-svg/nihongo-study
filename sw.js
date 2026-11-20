/* 日本語ノート — 오프라인 캐시 (홈 화면 추가·비행기 모드 대비) */
const CACHE = 'nihongo-note-v32';
const ASSETS = [
  './', './index.html', './manifest.json',
  './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png',
  /* 바쿠고 사진: index.html의 BAKUGO_IMAGES에 한 줄 넣을 때 여기에도 같은 경로를 넣어 주세요. */
  './assets/bakugo-1.jpg',
  './assets/bakugo-2.jpg',
  './assets/bakugo-3.jpg',
  './assets/bakugo-4.jpg',
  './assets/bakugo-5.jpg',
  './assets/bakugo-6.jpg',
  './assets/bakugo-7.jpg',
  './assets/bakugo-8.jpg',
  './assets/bakugo-9.jpg',
  './assets/bakugo-10.jpg',
  './assets/bakugo-11.jpg',
  './assets/bakugo-12.jpg',
  './assets/bakugo-13.jpg',
  './assets/bakugo-14.jpg',
  './assets/bakugo-15.jpg',
  './assets/bakugo-16.jpg',
  './assets/bakugo-17.jpg',
  './assets/bakugo-18.jpg',
  './assets/bakugo-19.jpg',
  './assets/bakugo-20.jpg',
  './assets/bakugo-21.jpg',
  './assets/bakugo-22.jpg',
  './assets/bakugo-23.jpg',
  './assets/bakugo-24.jpg',
  './assets/bakugo-25.jpg',
  './assets/bakugo-26.jpg',
  './assets/bakugo-27.jpg',
  './assets/bakugo-28.jpg',
  './assets/bakugo-29.jpg',
  './assets/bakugo-30.jpg',
  './assets/bakugo-31.jpg',
  './assets/bakugo-32.jpg',
  './assets/bakugo-33.jpg',
  './assets/bakugo-34.jpg',
  './assets/bakugo-35.jpg',
  './assets/bakugo-36.jpg',
  './assets/bakugo-37.jpg',
  './assets/bakugo-38.jpg',
  './assets/bakugo-39.jpg',
  './assets/bakugo-40.jpg',
  './assets/bakugo-41.jpg',
  './assets/bakugo-42.jpg',
  './assets/bakugo-43.jpg',
  './assets/bakugo-44.jpg',
  './assets/bakugo-45.jpg',
  './assets/bakugo-46.jpg',
  './assets/bakugo-47.jpg',
  './assets/bakugo-48.jpg',
  './assets/bakugo-49.jpg',
  './assets/bakugo-50.jpg',
  './assets/bakugo-51.jpg',
  './assets/bakugo-52.jpg',
  './assets/bakugo-53.jpg',
  './assets/bakugo-54.jpg',
  './assets/bakugo-55.jpg',
  './assets/bakugo-56.jpg',
  './assets/bakugo-57.jpg',
  './assets/bakugo-58.jpg',
  './fridge-data.json', './diet-data.json', './weight-data.json', './study-curriculum.json'
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

  /* 냉장고 재료·식단·체중 기록과 학습 커리큘럼은 네트워크 우선: 새 파일을 올리면 바로 반영되고, 오프라인이면 마지막 사본을 씁니다. */
  if (/\/(fridge|diet|weight)-data\.json$/.test(url.pathname) || /\/study-curriculum\.json$/.test(url.pathname)) {
    const fallback = /\/diet-data\.json$/.test(url.pathname) ? './diet-data.json'
      : /\/weight-data\.json$/.test(url.pathname) ? './weight-data.json'
      : /\/study-curriculum\.json$/.test(url.pathname) ? './study-curriculum.json'
      : './fridge-data.json';
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

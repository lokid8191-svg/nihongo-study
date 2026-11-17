/* 日本語ノート — 오프라인 캐시 (홈 화면 추가·비행기 모드 대비) */
const CACHE = 'nihongo-note-v9';
const ASSETS = [
  './', './index.html', './manifest.json',
  './icon.svg', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png',
  /* 바쿠고 사진: index.html의 BAKUGO_IMAGES에 한 줄 넣을 때 여기에도 같은 경로를 넣어 주세요. */
  './assets/bakugo-p1.jpg', './assets/bakugo-p2.jpg', './assets/bakugo-p3.jpg',
  './assets/bakugo-p4.jpg', './assets/bakugo-p5.jpg', './assets/bakugo-p6.jpg',
  './assets/bakugo-p7.jpg',
  './assets/bakugo-p8.jpg',
  './assets/bakugo-p9.jpg',
  './assets/bakugo-p10.jpg',
  './assets/bakugo-p11.jpg',
  './assets/bakugo-p12.jpg',
  './assets/bakugo-p13.jpg',
  './assets/bakugo-p14.jpg',
  './assets/bakugo-p15.jpg',
  './assets/bakugo-p16.jpg',
  './assets/bakugo-p17.jpg',
  './assets/bakugo-p18.jpg',
  './assets/bakugo-p19.jpg',
  './assets/bakugo-p20.jpg',
  './assets/bakugo-p21.jpg',
  './assets/bakugo-p22.jpg',
  './assets/bakugo-p23.jpg',
  './assets/bakugo-p24.jpg',
  './assets/bakugo-p25.jpg',
  './assets/bakugo-p26.jpg',
  './assets/bakugo-p27.jpg',
  './assets/bakugo-p28.jpg',
  './assets/bakugo-p29.jpg',
  './assets/bakugo-p30.jpg',
  './assets/bakugo-p31.jpg',
  './assets/bakugo-p32.jpg',
  './assets/bakugo-p33.jpg',
  './assets/bakugo-p34.jpg',
  './assets/bakugo-p35.jpg',
  './assets/bakugo-p36.jpg',
  './assets/bakugo-p37.jpg',
  './assets/bakugo-p38.jpg',
  './assets/bakugo-p39.jpg',
  './assets/bakugo-p40.jpg',
  './assets/bakugo-p41.jpg',
  './assets/bakugo-p42.jpg',
  './assets/bakugo-p43.jpg',
  './assets/bakugo-p44.jpg',
  './assets/bakugo-p45.jpg',
  './assets/bakugo-p46.jpg',
  './assets/bakugo-p47.jpg',
  './assets/bakugo-p48.jpg',
  './assets/bakugo-p49.jpg',
  './assets/bakugo-p50.jpg',
  './assets/bakugo-p51.jpg',
  './assets/bakugo-p52.jpg',
  './assets/bakugo-p53.jpg',
  './assets/bakugo-p54.jpg',
  './assets/bakugo-p55.jpg',
  './assets/bakugo-p56.jpg',
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

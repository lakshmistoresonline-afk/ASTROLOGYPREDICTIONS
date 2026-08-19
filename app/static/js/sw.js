const CACHE_NAME = 'jyotish-v2';
const ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/chart.js',
  '/static/img/icon.svg'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
});

self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});

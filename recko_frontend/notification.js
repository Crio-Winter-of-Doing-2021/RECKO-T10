if ('serviceWorker' in navigator && 'PushManager' in window) {
  var s = document.createElement('script');
  s.src = '/script/push.js';
  s.async = true;
  document.head.appendChild(s);
}
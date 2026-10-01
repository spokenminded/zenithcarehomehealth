(function () {
  'use strict';
  var side = document.getElementById('side');
  var open = document.getElementById('open');
  if (open) open.addEventListener('click', function () { side.classList.toggle('open'); });
  side.addEventListener('click', function (e) { if (e.target.closest('a')) side.classList.remove('open'); });

  // search the contents list
  var q = document.getElementById('q');
  var links = [].slice.call(side.querySelectorAll('a'));
  q.addEventListener('input', function () {
    var v = q.value.trim().toLowerCase();
    links.forEach(function (a) {
      var hit = !v || (a.textContent + ' ' + (a.getAttribute('data-t') || '')).toLowerCase().indexOf(v) !== -1;
      a.classList.toggle('hide', !hit);
    });
    [].forEach.call(side.querySelectorAll('details'), function (d) { if (v) d.open = true; });
  });

  // open every group while printing so nothing is hidden
  window.addEventListener('beforeprint', function () {
    [].forEach.call(document.querySelectorAll('details'), function (d) { d.open = true; });
  });
})();

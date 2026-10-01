'use strict';
/* =====================================================================================================
   AloraPlus Training Simulator: core
   Everything runs in this browser tab. There is no server, no network call, and nothing is ever sent.
   ===================================================================================================== */
const $ = (s, el) => (el || document).querySelector(s);
const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const ACT = {};          // click actions: <button data-act="name">
const ROUTES = {};       // hash routes
const S2SRC = {};        // select box sources
const CTX = {};          // binding contexts (page and modal state)
let DB = null;           // persisted practice data
let FILES = {};          // uploaded file data (data URLs), stored separately
let PAGE = { key: '', ctx: null, route: '', params: {} };
let ctxN = 0;

/* ---------------------------------------------------------------- icons (plain shapes, not Alora artwork) */
const ICONS = {
  home: 'M12 3 2 12h3v8h5v-6h4v6h5v-8h3z', dash: 'M3 13a9 9 0 1 1 18 0v4H3v-4zm9-6a1.300 1.300 0 1 0 0 2.600A1.300 1.300 0 0 0 12 7zm-5 3a1.300 1.300 0 1 0 0 2.600A1.300 1.300 0 0 0 7 10zm10 0a1.300 1.300 0 1 0 0 2.600 1.300 1.300 0 0 0 0-2.600zm-5 2.500 4-2.500-2.500 4.500a1.800 1.800 0 1 1-1.500-2z',
  user: 'M12 12a4.500 4.500 0 1 0 0-9 4.500 4.500 0 0 0 0 9zm0 2c-4.400 0-8 2.200-8 5v2h16v-2c0-2.800-3.600-5-8-5z', covid: 'M12 2 4 5v6c0 5 3.400 9.700 8 11 4.600-1.300 8-6 8-11V5l-8-3zm1 6v3h3v2h-3v3h-2v-3H8v-2h3V8h2z',
  cal: 'M7 2v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-2V2h-2v2H9V2H7zM5 10h14v10H5V10z', plusbox: 'M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm6 4v4H7v2h4v4h2v-4h4v-2h-4V7h-2z',
  mail: 'M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm1 2v.5l8 5 8-5V7l-8 5-8-5z', list: 'M3 5h18v14H3V5zm2 2v2h14V7H5zm0 4v2h14v-2H5zm0 4v2h9v-2H5z',
  dollar: 'M13 3v2.100c2 .3 3.500 1.500 3.500 3.400h-2c0-.9-.8-1.500-2.500-1.500s-2.500.6-2.500 1.400c0 .9.7 1.200 3 1.800 2.700.6 4 1.500 4 3.400 0 1.700-1.400 2.900-3.500 3.300V21h-2v-2.100c-2.100-.3-3.600-1.600-3.700-3.600h2c0 1 .9 1.700 2.700 1.700 1.700 0 2.500-.6 2.500-1.500 0-.9-.6-1.300-3-1.900-2.500-.6-4-1.600-4-3.300 0-1.600 1.300-2.800 3.500-3.200V3h2z',
  check: 'M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm2.500 9 3 3 6-6-1.400-1.400-4.600 4.600-1.600-1.600L7.500 12z', gear: 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm9 5.500v-3l-2.400-.5a7 7 0 0 0-.8-1.900l1.300-2.100-2.100-2.100-2.100 1.300a7 7 0 0 0-1.900-.8L12.500 2h-3l-.5 2.400a7 7 0 0 0-1.900.8L5 3.900 2.900 6l1.300 2.100a7 7 0 0 0-.8 1.900L1 11v3l2.400.5c.2.7.5 1.300.8 1.900L2.900 18.500 5 20.600l2.100-1.300c.6.4 1.200.7 1.900.8l.5 2.400h3l.5-2.400c.7-.2 1.300-.5 1.900-.8l2.100 1.300 2.100-2.100-1.300-2.100c.4-.6.700-1.200.8-1.900l2.500-.5z',
  report: 'M6 2h9l5 5v15H6V2zm8 1.500V8h4.500L14 3.500zM8 12h8v2H8v-2zm0 4h8v2H8v-2z', key: 'M7 14a4 4 0 1 1 3.900-5H21v3h-2v2h-3v-2h-5.100A4 4 0 0 1 7 14zm0-6a2 2 0 1 0 0 4 2 2 0 0 0 0-4z',
  cc: 'M12 3a4 4 0 1 1 0 8 4 4 0 0 1 0-8zm-8 17c0-3.300 3.600-5 8-5s8 1.700 8 5v1H4v-1z', wrench: 'M22 6.500a5 5 0 0 1-6.700 4.700L7 19.500a2.100 2.100 0 1 1-3-3l8.300-8.300A5 5 0 0 1 18 2l-3 3 .5 3.500L19 9l3-2.500z',
  help: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 16h-2v-2h2v2zm1.500-6.200-.9.900c-.6.600-.6 1-.6 1.800h-2v-.5c0-.9.3-1.700.9-2.300l1.200-1.300a1.600 1.600 0 0 0 .5-1.200 2 2 0 0 0-4 0H8a4 4 0 0 1 8 0c0 .8-.4 1.700-1.500 2.800z',
  doc: 'M6 2h8l6 6v14H6V2zm7 1.500V9h5.500L13 3.500z', folder: 'M3 5h7l2 2h9v13H3V5z', edit: 'M5 3h9l-2 2H5v14h14v-7l2-2v11H3V3h2zm14.500-.5 2 2L12 14H10v-2l9.500-9.500z',
  trash: 'M9 3h6l1 2h4v2H4V5h4l1-2zM6 9h12l-1 12H7L6 9z', print: 'M6 3h12v5H6V3zM4 9h16v8h-4v4H8v-4H4V9zm6 6v4h4v-4h-4z', eye: 'M12 5C7 5 2.700 8.100 1 12c1.700 3.900 6 7 11 7s9.300-3.100 11-7c-1.700-3.900-6-7-11-7zm0 11a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm0-6a2 2 0 1 0 0 4 2 2 0 0 0 0-4z',
  clip: 'M16.500 6v11.500a4 4 0 0 1-8 0V5a2.500 2.500 0 0 1 5 0v10.500a1 1 0 0 1-2 0V6H10v9.500a2.500 2.500 0 0 0 5 0V5a4 4 0 0 0-8 0v12.500a5.500 5.500 0 0 0 11 0V6h-1.500z',
  dots: 'M12 6a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z', search: 'M10 3a7 7 0 1 0 4.200 12.600l5.100 5.100 1.400-1.400-5.100-5.100A7 7 0 0 0 10 3zm0 2a5 5 0 1 1 0 10 5 5 0 0 1 0-10z',
  filter: 'M3 4h18l-7 8v7l-4 2v-9L3 4z', plus: 'M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7V4z', back: 'M20 11H7.800l5.600-5.600L12 4l-8 8 8 8 1.400-1.400L7.800 13H20v-2z', link: 'M14 3h7v7h-2V6.400l-8.300 8.300-1.400-1.400L17.600 5H14V3zM5 5h6v2H5v12h12v-6h2v8H3V5h2z',
  msg: 'M4 4h16a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H9l-5 4v-4H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z', pill: 'M5.500 12.500 12.500 5.500a4.200 4.200 0 0 1 6 6l-7 7a4.200 4.200 0 0 1-6-6zm2.800.400 3.300 3.300',
  bus: 'M5 4h14a2 2 0 0 1 2 2v10h-2v2h-3v-2H8v2H5v-2H3V6a2 2 0 0 1 2-2zm0 3v4h14V7H5z', shield: 'M12 2 4 5v6c0 5 3.400 9.700 8 11 4.600-1.300 8-6 8-11V5l-8-3z',
};
const ic = (n, cls) => `<svg class="${cls || 'ico'}" viewBox="0 0 24 24"><path d="${ICONS[n] || ICONS.doc}"/></svg>`;

/* ---------------------------------------------------------------- date and time helpers */
const pad = n => (n < 10 ? '0' : '') + n;
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
function isoD(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
function isoDT(d) { return isoD(d) + 'T' + pad(d.getHours()) + ':' + pad(d.getMinutes()); }
function toDate(s) { if (!s) return null; const m = /^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2}))?/.exec(s); return m ? new Date(+m[1], +m[2] - 1, +m[3], +(m[4] || 0), +(m[5] || 0)) : null; }
function fmtD(s) { const d = toDate(s); return d ? pad(d.getMonth() + 1) + '/' + pad(d.getDate()) + '/' + d.getFullYear() : ''; }
function fmtT(s) { const d = toDate(s); if (!d) return ''; let h = d.getHours(); const ap = h >= 12 ? 'PM' : 'AM'; h = h % 12 || 12; return pad(h) + ':' + pad(d.getMinutes()) + ' ' + ap; }
function fmtDT(s) { return s ? fmtD(s) + ' ' + fmtT(s) : ''; }
function fmtShortT(s) { const d = toDate(s); if (!d) return ''; let h = d.getHours(); const ap = h >= 12 ? 'p' : 'a'; h = h % 12 || 12; return h + ':' + pad(d.getMinutes()) + ap; }
function parseD(s) { s = String(s || '').trim(); const m = /^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2}|\d{4})$/.exec(s); if (!m) return null; let y = +m[3]; if (y < 100) y += 2000; const mo = +m[1], da = +m[2]; if (mo < 1 || mo > 12 || da < 1 || da > 31) return null; const d = new Date(y, mo - 1, da); if (d.getMonth() !== mo - 1) return null; return isoD(d); }
function parseDT(s) { s = String(s || '').trim(); const m = /^(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\s+(\d{1,2}):(\d{2})\s*([AaPp][Mm])?$/.exec(s); if (!m) return null; const d = parseD(m[1]); if (!d) return null; let h = +m[2]; const mi = +m[3]; if (m[4]) { const pm = /p/i.test(m[4]); if (h < 1 || h > 12) return null; h = (h % 12) + (pm ? 12 : 0); } if (h > 23 || mi > 59) return null; return d + 'T' + pad(h) + ':' + pad(mi); }
function addDays(s, n) { const d = toDate(s); d.setDate(d.getDate() + n); return s.length > 10 ? isoDT(d) : isoD(d); }
function addMin(s, n) { const d = toDate(s); d.setMinutes(d.getMinutes() + n); return isoDT(d); }
function diffMin(a, b) { return Math.round((toDate(a) - toDate(b)) / 60000); }
function diffDays(a, b) { return Math.round((toDate(a.slice(0, 10)) - toDate(b.slice(0, 10))) / 86400000); }
function dayName(s) { return DAYS[toDate(s).getDay()]; }

/* ---------------------------------------------------------------- the practice clock (simulated time) */
function nowDate() {
  const c = DB.clock; if (c.paused) return new Date(c.base);
  return new Date(c.base + (Date.now() - c.realAt));
}
function nowIso() { return isoDT(nowDate()); }
function todayIso() { return isoD(nowDate()); }
function setClock(ms, paused) { DB.clock.base = ms; DB.clock.realAt = Date.now(); if (paused != null) DB.clock.paused = paused; save(); }
function advanceClock(min) { const d = nowDate(); setClock(d.getTime() + min * 60000); }

/* ---------------------------------------------------------------- persistence */
const KEY = 'alorasim.v1', FKEY = 'alorasim.files.v1';
let memOnly = false;
function save() {
  if (!DB) return;
  DB.clock.lastSeen = Date.now();
  try { localStorage.setItem(KEY, JSON.stringify(DB)); if (typeof checkTasksSoon === 'function') checkTasksSoon(); }
  catch (e) { if (!memOnly) { memOnly = true; toast('Browser storage is full or blocked. Practice data will only last until you close this tab.', 'err'); } }
}
function saveFiles() { try { localStorage.setItem(FKEY, JSON.stringify(FILES)); } catch (e) { /* too big: viewing may be limited */ } }
function putFile(dataUrl) { const id = uid('F'); FILES[id] = dataUrl; saveFiles(); return id; }
function loadDB() {
  try { const s = localStorage.getItem(KEY); if (s) DB = JSON.parse(s); } catch (e) { DB = null; }
  try { const f = localStorage.getItem(FKEY); if (f) FILES = JSON.parse(f); } catch (e) { FILES = {}; }
  if (!DB || DB.v !== SEED_VERSION) { DB = seedData(); FILES = Object.assign({}, SEED_FILES); saveFiles(); }
  // do not count the time the tab was closed
  if (!DB.clock.paused && DB.clock.lastSeen) { const gap = Date.now() - DB.clock.lastSeen; if (gap > 10 * 60000) DB.clock.realAt += gap; }
  save();
}
function resetAll() { try { localStorage.removeItem(KEY); localStorage.removeItem(FKEY); } catch (e) { /* ignore */ } DB = seedData(); FILES = Object.assign({}, SEED_FILES); saveFiles(); save(); }
function uid(p) { DB.seq = (DB.seq || 1000) + 1; return p + DB.seq; }
function track(k) { DB.stats[k] = (DB.stats[k] || 0) + 1; }
function visited(k) { return (DB.stats['v:' + k] || 0) > 0; }
function simLog(kind, msg) {
  DB.log.unshift({ t: nowIso(), kind, msg, role: curRole(), user: curUser() ? curUser().name : '' });
  if (DB.log.length > 300) DB.log.length = 300;
  save(); if (typeof drawerRefresh === 'function') drawerRefresh();
}

/* ---------------------------------------------------------------- session helpers */
function curUser() { return DB.users.find(u => u.id === DB.session.userId) || null; }
function curRole() { const u = curUser(); return u ? u.role : ''; }
function roleIs() { const r = curRole(); return Array.from(arguments).indexOf(r) >= 0 || r === 'Administrator'; }
function byId(arr, id) { return arr.find(x => x.id === id) || null; }
function P(id) { return byId(DB.patients, id); }
function ST(id) { return byId(DB.staff, id); }
function ptName(p) { return p ? (p.last + ', ' + p.first + (p.mi ? ' ' + p.mi : '')).toUpperCase() : ''; }
function stName(s) { return s ? (s.last + ', ' + s.first).toUpperCase() : ''; }
function admOf(pid) { return DB.admissions.find(a => a.pid === pid) || null; }

/* ---------------------------------------------------------------- contexts, binding, and form controls */
function ctxNew(init) { const id = 'c' + (++ctxN); CTX[id] = Object.assign({ _id: id }, init || {}); return CTX[id]; }
function getp(o, path) { return path.split('.').reduce((a, k) => (a == null ? a : a[k]), o); }
function setp(o, path, v) { const ks = path.split('.'); let a = o; for (let i = 0; i < ks.length - 1; i++) { if (a[ks[i]] == null || typeof a[ks[i]] !== 'object') a[ks[i]] = {}; a = a[ks[i]]; } a[ks[ks.length - 1]] = v; }
const battr = (c, p) => `data-c="${c._id}" data-b="${p}"`;
function inp(c, p, o) { o = o || {}; const v = getp(c, p); return `<input type="${o.type || 'text'}" ${battr(c, p)} value="${esc(v == null ? '' : v)}"${o.ph ? ` placeholder="${esc(o.ph)}"` : ''}${o.ro ? ' readonly' : ''}${o.dis ? ' disabled' : ''}${o.max ? ` maxlength="${o.max}"` : ''}${o.cls ? ` class="${o.cls}"` : ''}${o.id ? ` id="${o.id}"` : ''}${o.auto ? ` autocomplete="${o.auto}"` : ' autocomplete="off"'}>`; }
function txt(c, p, o) { o = o || {}; return `<textarea ${battr(c, p)}${o.rows ? ` rows="${o.rows}"` : ''}${o.dis ? ' disabled' : ''}${o.ph ? ` placeholder="${esc(o.ph)}"` : ''}>${esc(getp(c, p) || '')}</textarea>`; }
function sel(c, p, opts, o) { o = o || {}; const v = getp(c, p); const list = opts.map(x => (Array.isArray(x) ? x : [x, x])); return `<select ${battr(c, p)}${o.rr ? ' data-rr="1"' : ''}${o.dis ? ' disabled' : ''}>${o.blank === false ? '' : `<option value="">${esc(o.blank || '')}</option>`}${list.map(([a, b]) => `<option value="${esc(a)}"${String(v) === String(a) ? ' selected' : ''}>${esc(b)}</option>`).join('')}</select>`; }
function chk(c, p, label, o) { o = o || {}; return `<label class="chk"><input type="checkbox" ${battr(c, p)}${getp(c, p) ? ' checked' : ''}${o.rr ? ' data-rr="1"' : ''}${o.dis ? ' disabled' : ''}> ${esc(label)}</label>`; }
function radio(c, p, val, label, o) { o = o || {}; return `<label class="chk"><input type="radio" name="${c._id}_${p}" ${battr(c, p)} value="${esc(val)}"${String(getp(c, p)) === String(val) ? ' checked' : ''}${o.rr ? ' data-rr="1"' : ''}${o.dis ? ' disabled' : ''}> ${esc(label)}</label>`; }
function dp(c, p, o) { o = o || {}; const v = getp(c, p); return `<input type="text" class="dpi${o.cls ? ' ' + o.cls : ''}" data-dp="${o.time ? 'dt' : 'd'}" ${battr(c, p)} value="${esc(v == null ? '' : v)}" placeholder="${o.time ? 'MM/DD/YYYY hh:mm AM' : 'MM/DD/YYYY'}" autocomplete="off"${o.dis ? ' disabled' : ''}${o.rr ? ' data-rr="1"' : ''}>`; }
function s2(c, p, src, o) {
  o = o || {}; const v = getp(c, p); const S = S2SRC[src]; const lab = v ? (S.label ? S.label(v, c) : v) : '';
  return `<div class="s2${o.dis ? ' dis' : ''}" tabindex="0" ${battr(c, p)} data-src="${src}"${o.ph ? ` data-ph="${esc(o.ph)}"` : ''}${o.rr ? ' data-rr="1"' : ''}${o.clear ? ' data-clear="1"' : ''}><span class="val">${lab ? esc(lab) : `<span class="ph">${esc(o.ph || '')}</span>`}</span>${o.clear && v ? '<span class="clr" data-s2clr="1">&times;</span>' : ''}</div>`;
}
function fg(label, ctrl, o) { o = o || {}; return `<div class="fg${o.cls ? ' ' + o.cls : ''}"><label${o.req ? ' class="req"' : ''}>${label}</label>${ctrl}${o.err ? `<div class="errtxt">${esc(o.err)}</div>` : ''}</div>`; }

function ctxOf(el) { const h = el.closest('[data-c]'); return h ? CTX[h.dataset.c] : null; }
function onBind(el) {
  const c = CTX[el.dataset.c]; if (!c) return null;
  let v;
  if (el.type === 'checkbox') v = el.checked; else if (el.type === 'radio') { if (!el.checked) return c; v = el.value; } else v = el.value;
  setp(c, el.dataset.b, v);
  el.classList.remove('bad');
  return c;
}
document.addEventListener('input', e => { const t = e.target; if (t.dataset && t.dataset.b && t.type !== 'checkbox' && t.type !== 'radio' && t.tagName !== 'SELECT') onBind(t); });
document.addEventListener('change', e => { const t = e.target; if (t.dataset && t.dataset.b) { const c = onBind(t); if (c && t.dataset.rr && c._rr) c._rr(); } });

/* keep the typing position when a view is re-drawn */
function withFocus(root, fn) {
  const a = document.activeElement; let key = null;
  if (a && a.dataset && a.dataset.b && root.contains(a)) key = { c: a.dataset.c, b: a.dataset.b, s: a.selectionStart, e: a.selectionEnd };
  else if (a && a.dataset && a.dataset.dtq && root.contains(a)) key = { q: a.dataset.dtq, s: a.selectionStart, e: a.selectionEnd };
  const sy = window.scrollY;
  fn();
  if (key) {
    const n = key.q ? root.querySelector(`[data-dtq="${key.q}"]`) : root.querySelector(`[data-c="${key.c}"][data-b="${key.b}"]`);
    if (n) { n.focus(); try { n.setSelectionRange(key.s, key.e); } catch (x) { /* not a text box */ } }
  }
  window.scrollTo(0, sy);
}

/* ---------------------------------------------------------------- clicks */
document.addEventListener('click', e => {
  const clr = e.target.closest('[data-s2clr]');
  if (clr) { e.stopPropagation(); const box = clr.closest('.s2'); const c = CTX[box.dataset.c]; setp(c, box.dataset.b, ''); const S = S2SRC[box.dataset.src]; if (S && S.onpick) S.onpick(c, '', box.dataset.b); if (c._rr) c._rr(); return; }
  const s = e.target.closest('.s2');
  if (s && !s.classList.contains('dis')) { openS2(s); return; }
  const a = e.target.closest('[data-act]');
  if (a) {
    if (a.classList.contains('dis') || a.disabled) { e.preventDefault(); return; }
    const f = ACT[a.dataset.act];
    if (f) { if (a.tagName !== 'INPUT') e.preventDefault(); f(a, e); } else console.warn('no action', a.dataset.act);
    return;
  }
  const t = e.target.closest('[data-go]');
  if (t) { e.preventDefault(); go(t.dataset.go); return; }
  closeMenus(e);
});
function closeMenus(e) {
  $$('.popmenu').forEach(m => { if (!m.contains(e.target)) m.remove(); });
  const um = $('#usermenu .dd'); if (um && !e.target.closest('#usermenu')) um.hidden = true;
  const gr = $('#gsearch .res'); if (gr && !e.target.closest('#gsearch')) gr.hidden = true;
}

/* ---------------------------------------------------------------- router */
function parseHash() {
  const h = location.hash.replace(/^#\/?/, ''); const [r, q] = h.split('?'); const params = {};
  (q || '').split('&').forEach(kv => { if (!kv) return; const [k, v] = kv.split('='); params[decodeURIComponent(k)] = decodeURIComponent(v || ''); });
  return { route: r || 'home', params };
}
function go(path, params) {
  const q = params ? '?' + Object.keys(params).map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k])).join('&') : '';
  const next = '#/' + path + q;
  if (location.hash === next) { PAGE.key = ''; render(); } else location.hash = next;
}
function render(keepCtx) {
  if (!DB || !DB.session.userId) { showLogin(); return; }
  const { route, params } = parseHash();
  const def = ROUTES[route] || ROUTES['notfound'];
  const key = route + '?' + JSON.stringify(params);
  const fresh = !(keepCtx && PAGE.key === key);
  if (fresh) { if (PAGE.ctx) delete CTX[PAGE.ctx._id]; PAGE = { key, ctx: ctxNew({ route, params }), route, params }; PAGE.ctx._rr = () => render(true); track('v:' + route); }
  const c = PAGE.ctx;
  const root = $('#content');
  withFocus(root, () => {
    root.innerHTML = `<div data-c="${c._id}">${def.render(c, params) || ''}</div>`;
    if (def.mount) def.mount(c, params, root);
  });
  if (fresh) window.scrollTo(0, 0);
  navActive(route, params);
  if (typeof simRefresh === 'function') simRefresh();
  if (typeof checkTasks === 'function') checkTasks();
}
function refresh() { render(true); }
window.addEventListener('hashchange', () => render(false));

/* ---------------------------------------------------------------- modals */
const MODALS = [];
function modal(o) {
  const m = { ctx: o.ctx || ctxNew(), o };
  m.ctx._modal = m; if (!m.ctx._rr) m.ctx._rr = () => m.rerender();
  const bd = document.createElement('div'); bd.className = 'bd'; if (o.z) bd.style.zIndex = o.z;
  m.el = bd;
  m.draw = () => {
    const body = typeof o.body === 'function' ? o.body(m.ctx, m) : o.body;
    const btns = (typeof o.buttons === 'function' ? o.buttons(m.ctx, m) : o.buttons) || [];
    bd.innerHTML = `<div class="modal ${o.size ? 'w-' + o.size : ''} ${o.kind ? o.kind + 'm' : ''}" role="dialog"><div class="mh"><span>${o.title || ''}</span>${o.noX ? '' : '<button class="x" data-mx="1" aria-label="Close">&times;</button>'}</div><div class="mb" data-c="${m.ctx._id}">${body || ''}</div>${btns.length ? `<div class="mf">${btns.map((b, i) => `<button class="btn ${b.cls || 'btn-cancel'}${b.dis ? ' dis' : ''}" data-mb="${i}">${b.label}</button>`).join('')}</div>` : ''}</div>`;
    bd._btns = btns;
  };
  m.rerender = () => withFocus(bd, () => { const sy = $('.mb', bd) ? $('.mb', bd).scrollTop : 0; m.draw(); if (o.mount) o.mount(m.ctx, m); const mb = $('.mb', bd); if (mb) mb.scrollTop = sy; });
  m.close = () => { const i = MODALS.indexOf(m); if (i >= 0) MODALS.splice(i, 1); bd.remove(); if (m.ctx && m.ctx._del !== false) delete CTX[m.ctx._id]; if (o.onClose) o.onClose(m); };
  bd.addEventListener('click', e => {
    if (e.target.closest('[data-mx]')) { e.stopPropagation(); if (o.onCancel) o.onCancel(m); m.close(); return; }
    const b = e.target.closest('[data-mb]');
    if (b) { e.stopPropagation(); const btn = bd._btns[+b.dataset.mb]; if (btn.dis) return; const r = btn.click ? btn.click(m, e) : undefined; if (r !== false) m.close(); }
  });
  m.draw(); $('#modal-root').appendChild(bd); MODALS.push(m);
  if (o.mount) o.mount(m.ctx, m);
  const first = $('input:not([type=hidden]):not([readonly]), textarea', bd); if (first && !o.noFocus) setTimeout(() => { try { first.focus(); } catch (x) { /* ignore */ } }, 30);
  return m;
}
document.addEventListener('keydown', e => { if (e.key === 'Escape' && MODALS.length && !$('.s2pop') && !$('.dpop')) { const m = MODALS[MODALS.length - 1]; if (m.o.noEsc) return; if (m.o.onCancel) m.o.onCancel(m); m.close(); } });
function alertBox(title, body, kind) { return modal({ title, body, kind, size: 'sm', buttons: [{ label: 'OK', cls: 'btn-ok' }] }); }
function confirmBox(title, body, yes, o) { o = o || {}; return modal({ title, body, kind: o.kind, size: o.size || 'sm', buttons: [{ label: o.yes || 'Yes', cls: o.yesCls || 'btn-ok', click: () => { yes(); } }, { label: o.no || 'No', cls: 'btn-del', click: () => { if (o.onNo) o.onNo(); } }] }); }
function toast(msg, kind) { const t = document.createElement('div'); t.className = 'toast ' + (kind || ''); t.textContent = msg; $('#toast-root').appendChild(t); setTimeout(() => t.remove(), kind === 'err' ? 6000 : 3500); }
function notice(msg, kind, x) { return `<div class="note ${kind || ''}"><span>${msg}</span>${x ? '<span class="x" data-act="closeNote">&times;</span>' : ''}</div>`; }
ACT.closeNote = el => el.closest('.note').remove();

/* ---------------------------------------------------------------- guard rails: Zenith rules and things the simulator never actually does */
// A rule that needs approval. Practice is allowed, but the coaching is recorded.
function needApproval(o) {
  if (o.roles && roleIs.apply(null, o.roles)) { o.go(); return; }
  modal({
    title: 'Zenith rule: approval needed', kind: 'warn', size: 'sm',
    body: `<p><b>${o.what}</b></p><p class="mt">${o.rule}</p><p class="mt small">Who approves: ${o.who || 'Administrator'} ${o.ref ? '(manual ' + o.ref + ')' : ''}</p><p class="mt">In real work you would STOP and ask. In this simulator you may continue so you can see what happens, and the choice is written in the Coach log.</p>`,
    buttons: [{ label: 'Stop (recommended)', cls: 'btn-ok', click: () => { simLog('good', 'Stopped and asked: ' + o.what); } }, { label: 'I have approval. Continue (practice)', cls: 'btn-or', click: () => { simLog('override', 'Continued without ' + (o.who || 'Administrator') + ' approval: ' + o.what); o.go(); } }],
  });
}
// An action the simulator will never perform (it would touch real money, a real fax, or real exports in the real Alora).
function neverDo(what, consequence, rule) {
  simLog('blocked', what + '. ' + consequence);
  modal({
    title: 'Simulator safety: nothing was done', kind: 'sim', size: 'sm',
    body: `<p><b>${what}</b></p><p class="mt">${consequence}</p>${rule ? `<p class="mt small">${rule}</p>` : ''}<p class="mt note sim">In the real Alora this is a real action. Here nothing was created, sent, billed or exported. The attempt is recorded in the Coach log.</p>`,
    buttons: [{ label: 'OK', cls: 'btn-ok' }],
  });
}

/* ---------------------------------------------------------------- date picker */
let DPOP = null;
function closeDP() { if (DPOP) { DPOP.remove(); DPOP = null; } }
document.addEventListener('focusin', e => { const t = e.target; if (t.dataset && t.dataset.dp && !t.readOnly && !t.disabled) openDP(t); else if (DPOP && !DPOP.contains(t)) closeDP(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && DPOP) { closeDP(); e.stopPropagation(); } }, true);
document.addEventListener('click', e => { const t = e.target; if (t.dataset && t.dataset.dp && !t.readOnly && !t.disabled && !DPOP) openDP(t); if (DPOP && !e.target.closest('.dpop') && !(t.dataset && t.dataset.dp)) closeDP(); });
function openDP(inp) {
  closeDP(); const withTime = inp.dataset.dp === 'dt';
  const cur = withTime ? parseDT(inp.value) : parseD(inp.value);
  let view = toDate(cur || todayIso()); view = new Date(view.getFullYear(), view.getMonth(), 1);
  let sel = cur ? toDate(cur) : null; let hh = sel ? sel.getHours() : 8, mm = sel ? sel.getMinutes() : 0;
  const pop = document.createElement('div'); pop.className = 'dpop'; DPOP = pop;
  const r = inp.getBoundingClientRect(); pop.style.left = (r.left + window.scrollX) + 'px'; pop.style.top = (r.bottom + window.scrollY + 2) + 'px';
  const commit = d => {
    let v = pad(d.getMonth() + 1) + '/' + pad(d.getDate()) + '/' + d.getFullYear();
    if (withTime) { const h12 = hh % 12 || 12; v += ' ' + pad(h12) + ':' + pad(mm) + ' ' + (hh >= 12 ? 'PM' : 'AM'); }
    inp.value = v; inp.dispatchEvent(new Event('input', { bubbles: true })); inp.dispatchEvent(new Event('change', { bubbles: true }));
  };
  const draw = () => {
    const y = view.getFullYear(), mo = view.getMonth(); const first = new Date(y, mo, 1).getDay(); const dim = new Date(y, mo + 1, 0).getDate(); const tdy = nowDate();
    let cells = DAYS.map(d => `<b>${d.slice(0, 2)}</b>`).join('');
    for (let i = 0; i < first; i++) { const d = new Date(y, mo, i - first + 1); cells += `<button class="o" data-d="${isoD(d)}">${d.getDate()}</button>`; }
    for (let d = 1; d <= dim; d++) { const dd = new Date(y, mo, d); const cls = (sel && isoD(sel) === isoD(dd)) ? 's' : (isoD(tdy) === isoD(dd) ? 't' : ''); cells += `<button class="${cls}" data-d="${isoD(dd)}">${d}</button>`; }
    const tail = (7 - ((first + dim) % 7)) % 7; for (let i = 1; i <= tail; i++) { const d = new Date(y, mo + 1, i); cells += `<button class="o" data-d="${isoD(d)}">${i}</button>`; }
    pop.innerHTML = `<div class="hd"><button data-n="-1">&lt;</button><span>${MONTHS[mo]} ${y}</span><button data-n="1">&gt;</button></div><div class="g">${cells}</div>` +
      (withTime ? `<div class="tm">Time <select data-h>${Array.from({ length: 12 }, (_, i) => `<option value="${i + 1}"${((hh % 12) || 12) === i + 1 ? ' selected' : ''}>${pad(i + 1)}</option>`).join('')}</select>:<select data-m>${Array.from({ length: 12 }, (_, i) => `<option value="${i * 5}"${mm === i * 5 ? ' selected' : ''}>${pad(i * 5)}</option>`).join('')}</select><select data-ap><option${hh < 12 ? ' selected' : ''}>AM</option><option${hh >= 12 ? ' selected' : ''}>PM</option></select></div>` : '') +
      `<div class="ft"><button data-today class="btn btn-sm btn-light">Today</button><button data-close class="btn btn-sm btn-light">Close</button></div>`;
  };
  draw(); document.body.appendChild(pop);
  const readTime = () => { const h = +$('[data-h]', pop).value, ap = $('[data-ap]', pop).value; hh = (h % 12) + (ap === 'PM' ? 12 : 0); mm = +$('[data-m]', pop).value; };
  pop.addEventListener('click', e => {
    const n = e.target.closest('[data-n]'); if (n) { view = new Date(view.getFullYear(), view.getMonth() + +n.dataset.n, 1); draw(); return; }
    const d = e.target.closest('[data-d]'); if (d) { if (withTime) readTime(); sel = toDate(d.dataset.d); commit(sel); if (!withTime) closeDP(); else draw(); return; }
    if (e.target.closest('[data-today]')) { if (withTime) readTime(); sel = toDate(todayIso()); commit(sel); closeDP(); return; }
    if (e.target.closest('[data-close]')) closeDP();
  });
  pop.addEventListener('change', () => { if (withTime) { readTime(); if (sel) commit(sel); } });
}

/* ---------------------------------------------------------------- select box with search (like the real Alora drop downs) */
let S2POP = null;
function closeS2() { if (S2POP) { S2POP.el.remove(); S2POP = null; } }
function openS2(box) {
  closeS2(); const S = S2SRC[box.dataset.src]; if (!S) return; const c = CTX[box.dataset.c]; if (!c) return;
  box.classList.add('open');
  const el = document.createElement('div'); el.className = 's2pop';
  const r = box.getBoundingClientRect(); el.style.left = (r.left + window.scrollX) + 'px'; el.style.top = (r.bottom + window.scrollY) + 'px'; el.style.minWidth = Math.max(r.width, S.cols ? 620 : 260) + 'px';
  if (S.cols && r.left + 640 > window.innerWidth) el.style.left = Math.max(4, window.innerWidth - 650) + 'px';
  el.innerHTML = `<div class="q"><input type="text" placeholder="" autocomplete="off"><svg class="ico" viewBox="0 0 24 24"><path d="${ICONS.search}"/></svg></div><div class="lst"></div>`;
  document.body.appendChild(el); S2POP = { el, box, hl: 0 };
  const inpEl = $('input', el), lst = $('.lst', el); let items = [];
  const cur = getp(c, box.dataset.b);
  const fill = () => {
    items = S.list(inpEl.value.trim(), c) || [];
    if (!items.length) { lst.innerHTML = '<div class="none">No results found</div>'; return; }
    if (S.cols) lst.innerHTML = `<table><thead><tr>${S.cols.map(h => `<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${items.map((o, i) => `<tr class="opt${i === S2POP.hl ? ' hl' : ''}" data-i="${i}">${(o.cells || [o.label]).map(x => `<td>${esc(x)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
    else lst.innerHTML = (S.head ? `<div class="grp">${esc(S.head)}</div>` : '') + items.map((o, i) => `<div class="opt${String(o.v) === String(cur) ? ' sel' : ''}${i === S2POP.hl ? ' hl' : ''}" data-i="${i}">${esc(o.label)}</div>`).join('');
  };
  const pick = i => {
    const o = items[i]; if (!o) return; setp(c, box.dataset.b, o.v);
    const ph = box.dataset.ph || ''; box.querySelector('.val').innerHTML = o.v ? esc(S.label ? S.label(o.v, c) : o.label) : `<span class="ph">${esc(ph)}</span>`;
    if (box.dataset.clear && o.v && !box.querySelector('.clr')) box.insertAdjacentHTML('beforeend', '<span class="clr" data-s2clr="1">&times;</span>');
    box.classList.remove('bad'); closeS2(); if (S.onpick) S.onpick(c, o.v, box.dataset.b, o); if (box.dataset.rr && c._rr) c._rr();
  };
  fill(); inpEl.focus();
  inpEl.addEventListener('input', () => { S2POP.hl = 0; fill(); });
  inpEl.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { S2POP.hl = Math.min(items.length - 1, S2POP.hl + 1); fill(); e.preventDefault(); } else if (e.key === 'ArrowUp') { S2POP.hl = Math.max(0, S2POP.hl - 1); fill(); e.preventDefault(); } else if (e.key === 'Enter') { pick(S2POP.hl); e.preventDefault(); } else if (e.key === 'Escape') { e.stopPropagation(); closeS2(); box.focus(); }
  });
  el.addEventListener('mousedown', e => { const o = e.target.closest('[data-i]'); if (o) { e.preventDefault(); pick(+o.dataset.i); } });
  const off = e => { if (S2POP && !S2POP.el.contains(e.target) && !box.contains(e.target)) { closeS2(); box.classList.remove('open'); document.removeEventListener('mousedown', off, true); } };
  document.addEventListener('mousedown', off, true);
}
document.addEventListener('keydown', e => { const b = e.target.closest && e.target.closest('.s2'); if (b && (e.key === 'Enter' || e.key === ' ') && !S2POP) { e.preventDefault(); openS2(b); } });

/* ---------------------------------------------------------------- data tables (search, sort, paging, like the real screens) */
function DT(c, id, defFn) {
  c.dtd = c.dtd || {}; c.dt = c.dt || {};
  c.dtd[id] = defFn; const d = defFn();
  if (!c.dt[id]) c.dt[id] = { q: '', applied: d.filterBtn ? '' : '', sort: d.sort || null, dir: d.dir || 1, page: 0, size: d.size || 10 };
  return `<div class="dt" id="dt-${c._id}-${id}" data-dtc="${c._id}" data-dtid="${id}">${dtInner(c, id)}</div>`;
}
function dtInner(c, id) {
  const d = c.dtd[id](), st = c.dt[id]; let rows = d.rows.slice();
  const cols = d.cols;
  const q = (d.filterBtn ? st.applied : st.q).toLowerCase();
  if (q) rows = rows.filter(r => (d.searchText ? d.searchText(r) : cols.map(cl => (cl.text ? cl.text(r) : r[cl.key])).join(' ')).toLowerCase().indexOf(q) >= 0);
  if (st.sort) { const cl = cols.find(x => x.key === st.sort); if (cl) { const f = cl.sort || (r => (cl.text ? cl.text(r) : r[cl.key])); rows.sort((a, b) => { const x = f(a), y = f(b); return (x < y ? -1 : x > y ? 1 : 0) * st.dir; }); } }
  const total = rows.length, size = st.size === 'all' ? Math.max(1, total) : +st.size; const pages = Math.max(1, Math.ceil(total / size)); if (st.page >= pages) st.page = pages - 1;
  const from = total ? st.page * size : 0; const slice = rows.slice(from, from + size);
  const sizes = d.sizes || [10, 25, 50, 100];
  const head = `<tr>${cols.map(cl => `<th class="${cl.sortable === false ? '' : 'srt'} ${st.sort === cl.key ? (st.dir > 0 ? 'asc' : 'desc') : ''} ${cl.blue ? 'blue' : ''}" ${cl.sortable === false ? '' : `data-dts="${cl.key}"`}${cl.w ? ` style="width:${cl.w}"` : ''}>${cl.label}</th>`).join('')}</tr>`;
  const body = slice.length ? slice.map(r => `<tr class="${d.rowCls ? d.rowCls(r) : ''}"${d.rowAttr ? ' ' + d.rowAttr(r) : ''}>${cols.map(cl => `<td>${cl.render ? cl.render(r) : esc(r[cl.key] == null ? '' : r[cl.key])}</td>`).join('')}</tr>`).join('') : `<tr><td class="none" colspan="${cols.length}">${esc(d.empty || 'No data available in table')}</td></tr>`;
  const pg = d.noPaging ? '' : `<div class="pg">${d.firstLast === false ? '' : `<button data-dtp="first"${st.page === 0 ? ' disabled' : ''}>First</button>`}<button data-dtp="prev"${st.page === 0 ? ' disabled' : ''}>Previous</button>${pageBtns(st.page, pages)}<button data-dtp="next"${st.page >= pages - 1 ? ' disabled' : ''}>Next</button>${d.firstLast === false ? '' : `<button data-dtp="last"${st.page >= pages - 1 ? ' disabled' : ''}>Last</button>`}</div>`;
  const top = d.noTop ? '' : `<div class="dt-top"><div>${d.noSize ? '' : `Show <select data-dtz>${sizes.map(s => `<option${String(s) === String(st.size) ? ' selected' : ''}>${s}</option>`).join('')}</select> entries`}</div><div class="sr">${d.noSearch ? '' : `Search: <input type="text" data-dtq="${id}" value="${esc(st.q)}" autocomplete="off">${d.filterBtn ? `<button class="btn filt" data-dtf="1" title="Filter">${ic('filter')}</button>` : ''}`}${d.extraTop || ''}</div></div>`;
  return `${top}<table class="t"><thead>${head}</thead><tbody>${body}</tbody></table>${d.noBottom ? '' : `<div class="dt-bot"><div>Showing ${total ? from + 1 : 0} to ${Math.min(from + size, total)} of ${total} entries</div>${pg}</div>`}`;
}
function pageBtns(p, n) { const out = []; const lo = Math.max(0, p - 2), hi = Math.min(n - 1, p + 2); for (let i = lo; i <= hi; i++) out.push(`<button class="${i === p ? 'on' : ''}" data-dtp="${i}">${i + 1}</button>`); return out.join(''); }
function dtRefresh(box) { const c = CTX[box.dataset.dtc]; if (!c) return; withFocus(box, () => { box.innerHTML = dtInner(c, box.dataset.dtid); }); }
document.addEventListener('click', e => {
  const box = e.target.closest('.dt'); if (!box) return; const c = CTX[box.dataset.dtc]; if (!c) return; const id = box.dataset.dtid, st = c.dt[id];
  const s = e.target.closest('[data-dts]'); if (s) { if (st.sort === s.dataset.dts) st.dir = -st.dir; else { st.sort = s.dataset.dts; st.dir = 1; } dtRefresh(box); return; }
  const p = e.target.closest('[data-dtp]'); if (p && !p.disabled) { const v = p.dataset.dtp; const d = c.dtd[id](); const total = d.rows.length; if (v === 'first') st.page = 0; else if (v === 'prev') st.page = Math.max(0, st.page - 1); else if (v === 'next') st.page++; else if (v === 'last') st.page = 9999; else st.page = +v; dtRefresh(box); return; }
  if (e.target.closest('[data-dtf]')) { st.applied = st.q; st.page = 0; track('dtfilter:' + c.route); if (st.applied) track('search:' + c.route); dtRefresh(box); }
});
document.addEventListener('input', e => { const t = e.target; if (!t.dataset || !t.dataset.dtq) return; const box = t.closest('.dt'); const c = CTX[box.dataset.dtc]; const st = c.dt[box.dataset.dtid]; const d = c.dtd[box.dataset.dtid](); st.q = t.value; if (!d.filterBtn) { st.page = 0; dtRefresh(box); } });
document.addEventListener('change', e => { const t = e.target; if (!t.dataset || t.dataset.dtz === undefined) return; const box = t.closest('.dt'); const c = CTX[box.dataset.dtc]; const st = c.dt[box.dataset.dtid]; st.size = t.value === 'all' ? 'all' : +t.value; st.page = 0; dtRefresh(box); });
document.addEventListener('keydown', e => { const t = e.target; if (t.dataset && t.dataset.dtq && e.key === 'Enter') { e.preventDefault(); /* like the real screen: Enter alone does not filter */ } });

/* ---------------------------------------------------------------- pop up menu (the three dot Action button) */
function popMenu(anchor, items) {
  $$('.popmenu').forEach(m => m.remove());
  const m = document.createElement('div'); m.className = 'popmenu';
  m.style.cssText = 'position:absolute;z-index:1250;background:#fff;border:1px solid #ccc;box-shadow:0 6px 18px rgba(0,0,0,.25);min-width:200px;padding:4px 0';
  const r = anchor.getBoundingClientRect(); m.style.left = (r.left + window.scrollX) + 'px'; m.style.top = (r.bottom + window.scrollY) + 'px';
  m.innerHTML = items.map((it, i) => `<a data-pm="${i}" style="display:flex;gap:10px;align-items:center;padding:8px 14px;color:#444;cursor:pointer;${it.danger ? 'color:#c0392b' : ''}">${it.ic ? ic(it.ic, 'ico ico-' + (it.cls || 'edit')) : ''}${esc(it.label)}</a>`).join('');
  document.body.appendChild(m);
  m.addEventListener('click', e => { const a = e.target.closest('[data-pm]'); if (a) { m.remove(); items[+a.dataset.pm].run(); } });
  m.addEventListener('mouseover', e => { const a = e.target.closest('[data-pm]'); $$('[data-pm]', m).forEach(x => (x.style.background = x === a ? '#eef5fc' : '')); });
}

/* ---------------------------------------------------------------- file viewer (shows what was uploaded, from this browser only) */
function dataUrlToBlob(url) { const m = /^data:([^;,]*)(;base64)?,(.*)$/s.exec(url); if (!m) return null; const bin = m[2] ? atob(m[3]) : decodeURIComponent(m[3]); const arr = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i); return new Blob([arr], { type: m[1] || 'application/octet-stream' }); }
function fixMime(url, name) {
  const m = /^data:([^;,]*)(;[^,]*)?,(.*)$/s.exec(url); if (!m) return url; const body = m[3]; let mime = m[1];
  if (/^(image\/|application\/pdf)/.test(mime)) return url;
  const ext = ((/\.([a-z0-9]+)$/i.exec(name || '') || [])[1] || '').toLowerCase(); const map = { png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif', webp: 'image/webp', svg: 'image/svg+xml', pdf: 'application/pdf' };
  if (map[ext]) mime = map[ext]; else if (body.indexOf('iVBORw0KGgo') === 0) mime = 'image/png'; else if (body.indexOf('/9j/') === 0) mime = 'image/jpeg'; else if (body.indexOf('JVBER') === 0) mime = 'application/pdf'; else if (body.indexOf('R0lGOD') === 0) mime = 'image/gif'; else if (body.indexOf('UklGR') === 0) mime = 'image/webp'; else return url;
  return 'data:' + mime + ';base64,' + body;
}
function viewFile(rec) {
  const url = rec.fileId ? FILES[rec.fileId] : null; let blobUrl = '';
  let body;
  if (!url) body = `<p class="note warn">This practice file was too large to keep in the browser, so only its name is stored.</p><div class="kv"><div>File name</div><div>${esc(rec.fileName || '')}</div><div>Size</div><div>${esc(rec.fileSize || '')}</div></div>`;
  else if (/^data:image\//.test(url)) body = `<img class="docview img" src="${url}" alt="${esc(rec.title)}">`;
  else if (/^data:application\/pdf/.test(url)) { const b = dataUrlToBlob(url); blobUrl = b ? URL.createObjectURL(b) : ''; body = blobUrl ? `<iframe class="docview" src="${blobUrl}" title="${esc(rec.title)}"></iframe>` : '<p class="note warn">This PDF could not be shown.</p>'; }
  else body = `<p class="note warn">This type of file cannot be shown here. In the real Alora it would open or download.</p><div class="kv"><div>File name</div><div>${esc(rec.fileName || '')}</div></div>`;
  modal({ title: esc(rec.title || 'Document'), size: 'lg', body, onClose: () => { if (blobUrl) URL.revokeObjectURL(blobUrl); }, buttons: (url ? [{ label: 'Download', cls: 'btn-add', click: () => { const b = dataUrlToBlob(url); if (b) { const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = rec.fileName || 'practice-file'; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 800); } return false; } }] : []).concat([{ label: 'Close', cls: 'btn-close' }]) });
}
function readFile(file, cb) {
  if (!file) { cb(null); return; }
  const rd = new FileReader();
  rd.onload = () => { const url = fixMime(String(rd.result), file.name); if (url.length > 900000) cb({ name: file.name, size: file.size, url: null }); else cb({ name: file.name, size: file.size, url }); };
  rd.onerror = () => cb({ name: file.name, size: file.size, url: null });
  rd.readAsDataURL(file);
}
function fmtSize(n) { return n > 1048576 ? (n / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(n / 1024)) + ' KB'; }
function downloadText(name, text, mime) { const b = new Blob([text], { type: mime || 'text/html' }); const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500); }

/* ---------------------------------------------------------------- tiny helpers used by many pages */
function pageHead(title, sub, manual) {
  return `<div class="ptitle">${esc(title)}${sub ? `<small>${esc(sub)}</small>` : ''}</div>`;
}
function tabsHtml(tabs, cur, attr) { return `<div class="tabs">${tabs.map(t => `<a class="${t.k === cur ? 'on' : ''}${t.off ? ' off' : ''}" data-act="${attr || 'tab'}" data-k="${t.k}">${esc(t.l)}</a>`).join('')}</div>`; }
function simplified() { return `<span class="chip simp" title="The real screen was not photographed. This is a simplified practice version.">SIMPLIFIED PRACTICE VERSION</span>`; }
function stub(msg) { return `<div class="stub"><b>Simplified practice screen.</b> ${msg}</div>`; }
function tagFor(status) { const s = String(status || ''); const m = { 'Completed': 'g', 'Approved': 'g', 'Signed': 'g', 'Active': 'g', 'In Use': 'y', 'Draft': 'y', 'Pending': 'o', 'Pending QA': 'o', 'Returned': 'r', 'Missed': 'r', 'Not Completed': 'gr', 'Cancelled': 'gr', 'Hospitalized': 'o', 'On Hold': 'o' }; return `<span class="tag ${m[s] || 'b'}">${esc(s)}</span>`; }
function rowIcons(list) { return list.map(i => `<button class="ico-btn ico-${i.cls || 'edit'}" title="${esc(i.t)}" data-act="${i.act}" ${Object.keys(i.data || {}).map(k => `data-${k}="${esc(i.data[k])}"`).join(' ')}>${ic(i.ic)}</button>`).join(''); }

'use strict';
/* =====================================================================================================
   Shell: simulator bar, login, header, left menu, global search, Home and Dashboards
   ===================================================================================================== */
const MANUAL_REF = {
  home: 'S1 and S2: Logging in and the main menu', patients: 'S3, O1, O2, O3: Finding a patient, demographics, referrals', patient: 'O1: Reviewing demographics', admissions: 'O4: Opening the admission', admission: 'O4, BI3: Admission, insurance, payer',
  chart: 'S4: Viewing the patient chart', ehr: 'O5, O6, O8: SOC document upload and naming', ehrlist: 'O5: SOC document upload', orders: 'O7, N5: Orders and the General Form', 'orders-pt': 'O7, N5: Orders and the General Form',
  f485: 'O8, N4: 485 and Face-to-Face', 'f485-pt': 'O8, N4: 485 and Face-to-Face', assess: 'N2: Starting the SOC assessment', 'assess-pt': 'N2: Starting the SOC assessment', sn: 'N3: Skilled nursing visit note', 'sn-pt': 'N3: Skilled nursing visit note', snnote: 'N3: Skilled nursing visit note',
  aide: 'AI2: Aide visit note and plan of care', 'aide-pt': 'AI2: Aide visit note and plan of care', alldocs: 'O9, AD2: All Documents', scheduler: 'SC1, SC2: Scheduling and changing visits', batch: 'SC1: Scheduling (batch entry)', monitor: 'SC3: Monitoring visits', conflicts: 'SC4, AD4: EVV conflicts',
  staff: 'H1 to H6: Staff records', 'staff-rec': 'H2 to H6: Staff record', 'ptfolders': 'AD3: Patient document folders', 'stfolders': 'H4: Staff folders', qa: 'AD1: QA Center', prebill: 'BI1: Pre-Billing QA', noa: 'BI2: Notice of Admission', claimsum: 'BI3: Billing screens (look only)', users: 'H7: User access',
  commlog: 'O2: Patient communication log', daily: 'Daily Office Alora Check', careconnect: 'N1, AI1: Clocking in and out',
};
const NAV = [
  { k: 'home', l: 'Home', ic: 'home', r: 'home' }, { k: 'dash', l: 'Dashboard', ic: 'dash', r: 'dashboard' }, { k: 'bdash', l: 'Billing Dashboard', ic: 'dash', r: 'billing-dashboard' },
  { k: 'patient', l: 'Patient', ic: 'user', items: [{ l: 'Patient Demographics and Referrals', r: 'patients' }, { l: 'Admission, Insurance & Prior Auth', r: 'admissions' }, { l: 'Patient Chart', r: 'chart' }, { l: 'Patient Communication Log', r: 'commlog' }] },
  { k: 'covid', l: 'COVID-19 Screening', ic: 'covid', items: [{ l: 'COVID-19 Patient Screening', r: 'covid' }, { l: 'COVID-19 Employee Screening', r: 'covid-emp' }] },
  { k: 'sched', l: 'Scheduling', ic: 'cal', items: [{ l: 'Scheduler', r: 'scheduler' }, { l: 'Batch Entry of Visits', r: 'batch' }, { l: 'Global Calendar', r: 'global' }, { l: 'Supply Log', r: 'form-supply' }] },
  { k: 'clin', l: 'Clinical', ic: 'plusbox', items: [{ l: 'Skilled Nursing Visit Notes', r: 'sn' }, { l: 'Assessments (OASIS/NON-OASIS)', r: 'assess' }, { l: '485 - Certification and Plan of Care', r: 'f485' }, { l: 'Plan of Care Plus', r: 'form-pocplus' },
    { l: 'Order Plus (Verbal Order Plus)', r: 'form-orderplus' }, { l: 'General Form (Orders & Docs)', r: 'orders' }, { l: 'Aide Documents', r: 'aide' }, { l: 'Electronic Health Records', r: 'ehr' }, { l: 'PT Documents', r: 'form-pt' }, { l: 'OT Documents', r: 'form-ot' }, { l: 'Speech Therapy', r: 'form-st' },
    { l: 'MSW', r: 'form-msw' }, { l: 'Supervisory Notes', r: 'form-sup' }, { l: 'Med Profile', r: 'form-med' }, { l: 'Allergy', r: 'form-allergy' }, { l: 'Missed Visit', r: 'form-missed' }, { l: 'Discharge/Transfer Summary', r: 'form-dc' }, { l: 'Tinetti Assessment', r: 'form-tinetti' }, { l: 'Braden Scale', r: 'form-braden' }] },
  { k: 'mail', l: 'AloraMail', ic: 'mail', r: 'mail', badge: () => (DB.messages.filter(m => m.to === DB.session.userId && !m.read).length || '') },
  { k: 'bill', l: 'Billing', ic: 'list', items: [{ l: 'Claim Summary', r: 'claimsum' }, { l: 'Generate Claims', r: 'genclaims' }, { l: 'Generate Claims PDGM', r: 'noa' }, { l: 'Electronic Claim File', r: 'eclaim' }, { l: 'Non-insurance Invoice', r: 'invoice' }, { l: 'Batch Printing of Claims', r: 'batchprint' }, { l: 'Pre-Billing QA', r: 'prebill' }] },
  { k: 'ar', l: 'A/R', ic: 'dollar', items: [{ l: 'Transaction Log', r: 'artrans' }, { l: 'Post Payment', r: 'postpay' }] },
  { k: 'qa', l: 'QA Center', ic: 'check', r: 'qa' },
  { k: 'setup', l: 'Setup', ic: 'gear', roles: ['Administrator', 'DON', 'HR', 'Biller'], items: [{ l: 'Aide Service Titles', r: 'setup-aide', roles: ['Administrator'] }, { l: 'Staff (Caregiver)', r: 'staff', roles: ['Administrator', 'HR', 'DON'] }, { l: 'Patient Electronic Document Folder', r: 'ptfolders', roles: ['Administrator'] },
    { l: 'Electronic Staff (Caregiver) Document Folder', r: 'stfolders', roles: ['Administrator', 'HR'] }, { l: 'EVV Change Reasons', r: 'setup-evv', roles: ['Administrator'] }, { l: 'Physicians', r: 'setup-phys', roles: ['Administrator'] }, { l: 'Referral Sources', r: 'setup-refsrc', roles: ['Administrator'] },
    { l: 'Billing Codes', r: 'setup-bc', roles: ['Administrator', 'Biller'] }, { l: 'Payers', r: 'setup-payers', roles: ['Administrator', 'Biller'] }, { l: 'Missed Visit Reasons', r: 'setup-missed', roles: ['Administrator'] }] },
  { k: 'rep', l: 'Reports', ic: 'report', r: 'reports' },
  { k: 'inov', l: 'Inovalon Claim Portal', ic: 'list', items: [{ l: 'Claim Portal', r: 'unbuilt', p: { n: 'Inovalon Claim Portal' } }] },
  { k: 'admin', l: 'Admin', ic: 'key', roles: ['Administrator'], items: [{ l: 'User / Security Manager', r: 'users' }] },
  { k: 'cc', l: 'CareConnect/EVV', ic: 'cc', items: [{ l: 'CareConnect', r: 'careconnect' }, { l: 'Monitor', r: 'monitor' }, { l: 'Conflicts', r: 'conflicts' }] },
  { k: 'tools', l: 'Tools', ic: 'wrench', roles: ['Administrator'], items: [{ l: 'Fax Confirmation', r: 'faxconf' }, { l: 'Undelete Documents', r: 'undelete' }, { l: 'Oasis Export', r: 'oasisexport' }, { l: 'OASIS Segue', r: 'oasissegue' }, { l: 'CAHPS Export', r: 'cahps' }] },
  { k: 'help', l: 'Help', ic: 'help', items: [{ l: 'Training Videos', r: 'videos' }, { l: 'Simulator Guide', r: 'simguide' }] },
];
const navVisible = n => !n.roles || n.roles.indexOf(curRole()) >= 0;

function wordmark(sub) { return `<div class="wordmark">ALORA<i>Plus</i><small>${sub || 'TRAINING SIMULATOR'}</small></div>`; }

/* ---------------------------------------------------------------- the simulator bar (not part of Alora) */
function buildSimBar() {
  const u = curUser();
  $('#simbar').innerHTML = `<b class="tag">TRAINING SIMULATOR</b><span class="msg">Nothing here is real. Nothing is sent, billed or saved outside this browser.</span><span class="grow"></span>
    ${u ? `<span>Practice as <select id="roleSel">${ROLES.map(r => `<option value="${r}"${r === u.role ? ' selected' : ''}>${esc(ROLE_LABEL[r])}</option>`).join('')}</select></span><span class="sep"></span>` : ''}
    <span class="clock" id="simclock" title="The practice clock. Visits, delays and deadlines use this time."></span>
    <button data-act="clk" data-m="15">+15 min</button><button data-act="clk" data-m="60">+1 hour</button><button data-act="clk" data-m="1440">+1 day</button><button data-act="clkset">Set time</button><button data-act="clkpause" id="clkpause">Pause</button>
    <span class="sep"></span><button data-act="phoneopen">CareConnect phone</button><button data-act="drawer" data-t="tasks">Practice guide</button><button data-act="drawer" data-t="log">Coach log</button>
    <span class="sep"></span><span class="ref" id="simref"></span>`;
  simClockTick();
}
function simClockTick() {
  const e = $('#simclock'); if (!e || !DB) return;
  const d = nowDate(); e.textContent = DAYS[d.getDay()] + ' ' + fmtD(isoD(d)) + ' ' + fmtT(isoDT(d)) + (DB.clock.paused ? ' (paused)' : '');
  const p = $('#clkpause'); if (p) p.textContent = DB.clock.paused ? 'Resume' : 'Pause';
}
function simRefresh() { const e = $('#simref'); if (e) { const r = MANUAL_REF[PAGE.route]; e.textContent = r ? 'Manual: ' + r : ''; } const rs = $('#roleSel'); const u = curUser(); if (rs && u) rs.value = u.role; simClockTick(); }
setInterval(() => { if (DB) simClockTick(); }, 5000);
ACT.clk = el => { advanceClock(+el.dataset.m); track('clock:advance'); toast('Practice clock moved ' + (el.dataset.m >= 1440 ? '1 day' : el.dataset.m + ' minutes') + ' ahead.', 'sim'); simClockTick(); refresh(); if (typeof phoneRefresh === 'function') phoneRefresh(); };
ACT.clkpause = () => { const c = DB.clock; if (c.paused) { c.base = nowDate().getTime(); c.realAt = Date.now(); c.paused = false; } else { c.base = nowDate().getTime(); c.paused = true; } save(); simClockTick(); };
ACT.clkset = () => {
  const c = ctxNew({ v: fmtDT(nowIso()) });
  modal({ title: 'Set the practice clock', ctx: c, size: 'sm', body: cc => `<p class="small">The practice clock is only for training. It decides which visits are late, which conflicts appear and when deadlines pass.</p>${fg('Date and time', dp(cc, 'v', { time: true }))}<p class="small">Manual date: 09/30/2026. Real time: <a data-act="clkreal">use this computer's clock</a>.</p>`, buttons: [{ label: 'Set', cls: 'btn-ok', click: (m, e) => { const v = parseDT(c.v); if (!v) { toast('Type a date and time like 09/30/2026 08:30 AM', 'err'); return false; } setClock(toDate(v).getTime()); simClockTick(); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] });
};
ACT.clkreal = () => { setClock(Date.now(), false); simClockTick(); $$('.bd').forEach(b => b.remove()); MODALS.length = 0; refresh(); };

document.addEventListener('change', e => { if (e.target.id === 'roleSel') switchRole(e.target.value); });
function switchRole(role) {
  const u = DB.users.find(x => x.role === role && x.active) || DB.users.find(x => x.role === role);
  if (!u) return; DB.session.userId = u.id; save(); track('role:' + role);
  closeAllModals(); buildShell(); toast('Now practicing as ' + ROLE_LABEL[role] + ' (' + u.name + ')', 'sim');
  if (PAGE.route && ROUTES[PAGE.route]) refresh(); else go('home');
}
function closeAllModals() { MODALS.slice().forEach(m => m.close()); closeS2(); closeDP(); $$('.popmenu').forEach(x => x.remove()); }

/* ---------------------------------------------------------------- login */
let loginFails = 0;
function showLogin() {
  $('#app').innerHTML = `<div id="login"><div class="login-card"><div class="logo">${wordmark()}</div><h3 style="font-weight:600;margin-bottom:4px">Sign in</h3><p class="small">Practice copy of the office login. Use your own login in real work. Never share it.</p>
    <label for="lu">Username</label><input id="lu" type="text" autocomplete="off" autofocus><label for="lp">Password</label><input id="lp" type="password" autocomplete="off">
    <button class="btn btn-add" data-act="dologin" id="lbtn">Login</button><div class="err" id="lerr"></div>
    <div class="demo"><b>Practice logins</b> (password for all: <code>practice</code>)<br>${DB.users.map(u => `<button data-act="fillLogin" data-u="${u.username}" title="${esc(ROLE_LABEL[u.role])}">${esc(u.username)}</button>`).join('')}</div>
    <div class="sim-note"><b>This is a training simulator.</b> It looks like the real screens so staff can practice, but it is not the real system. Nothing you do here reaches a patient, a payer or a physician.</div></div></div>`;
  buildSimBar();
  const lp = $('#lp'); if (lp) lp.addEventListener('keydown', e => { if (e.key === 'Enter') ACT.dologin(); }); const lu = $('#lu'); if (lu) lu.addEventListener('keydown', e => { if (e.key === 'Enter') ACT.dologin(); });
}
ACT.fillLogin = el => { $('#lu').value = el.dataset.u; $('#lp').value = 'practice'; $('#lp').focus(); };
ACT.dologin = () => {
  const u = DB.users.find(x => x.username === $('#lu').value.trim().toLowerCase() && x.active);
  if (u && u.pw === $('#lp').value) { loginFails = 0; DB.session.userId = u.id; track('login'); save(); simLog('info', 'Logged in as ' + u.name); buildShell(); if (!location.hash || location.hash === '#/login') go('home'); else render(); return; }
  loginFails++; $('#lerr').innerHTML = loginFails >= 2 ? '<b>Login failed twice. STOP.</b> Do not keep guessing. In real work you would tell the Administrator. (Here: use one of the practice logins above.)' : 'Login failed. Check your username and password and try once more.';
};
ACT.logout = () => { DB.session.userId = null; save(); closeAllModals(); showLogin(); history.replaceState(null, '', '#/login'); track('logout'); };

/* ---------------------------------------------------------------- header, menu, search */
function buildShell() {
  $('#app').innerHTML = `<div id="shell"${DB.ui.collapsed ? ' class="collapsed"' : ''}><header id="hdr">${wordmark()}<div id="gsearch"><div class="box">${ic('search')}<input id="gq" placeholder="What are you looking for?" autocomplete="off"><button class="new" data-act="newmenu">NEW</button></div><div class="res" hidden></div></div><span class="grow"></span>
    <div id="usermenu"><button data-act="usermenu">${esc(curUser().name)} &#9662;</button><div class="dd" hidden><a data-act="drawer" data-t="tasks">Practice guide</a><a data-act="logout">Log out</a></div></div></header>
    <nav id="nav" aria-label="Main menu"></nav><main id="main"><div id="content"></div><div id="foot"><span>AloraPlus Training Simulator. A practice copy built from the screens in Zenith's manual (captured 09/30/2026).</span><span>Not the real Alora. Not affiliated with or endorsed by Alora Healthcare Systems.</span></div></main></div>`;
  buildNav(); buildSimBar();
  const gq = $('#gq'); gq.addEventListener('input', globalSearch); gq.addEventListener('focus', globalSearch);
  gq.addEventListener('keydown', e => { if (e.key === 'Enter') { const a = $('#gsearch .res a'); if (a) a.click(); } });
}
ACT.usermenu = () => { const d = $('#usermenu .dd'); d.hidden = !d.hidden; };
function buildNav() {
  const open = DB.ui.open || {};
  $('#nav').innerHTML = `<div class="it" data-act="collapse">${ic('back')}<span class="lbl" style="color:#2b7bb9">Collapse</span></div>` + NAV.filter(navVisible).map(n => {
    const b = n.badge ? n.badge() : '';
    if (n.items) return `<div class="grp${open[n.k] ? ' open' : ''}" data-g="${n.k}"><div class="it" data-act="navgrp" data-k="${n.k}">${ic(n.ic)}<span class="lbl">${esc(n.l)}</span><svg class="car" viewBox="0 0 12 12"><path d="M2 4l4 4 4-4"/></svg></div><div class="sub">${n.items.filter(navVisible).map(i => `<a data-act="navgo" data-r="${i.r}"${i.p ? ` data-p='${JSON.stringify(i.p)}'` : ''} data-rr="${i.r}">${esc(i.l)}</a>`).join('')}</div></div>`;
    return `<div class="it" data-act="navgo" data-r="${n.r}" data-rr="${n.r}">${ic(n.ic)}<span class="lbl">${esc(n.l)}</span>${b ? `<span class="badge">${b}</span>` : ''}</div>`;
  }).join('');
}
ACT.collapse = () => { DB.ui.collapsed = !DB.ui.collapsed; save(); $('#shell').classList.toggle('collapsed', DB.ui.collapsed); };
ACT.navgrp = el => { const k = el.dataset.k; const was = DB.ui.open[k]; DB.ui.open = {}; if (!was) DB.ui.open[k] = true; save(); $$('#nav .grp').forEach(g => g.classList.toggle('open', !!DB.ui.open[g.dataset.g])); track('navopen:' + k); };
ACT.navgo = el => { go(el.dataset.r, el.dataset.p ? JSON.parse(el.dataset.p) : null); };
function navActive(route) {
  $$('#nav [data-rr]').forEach(a => { const base = a.dataset.rr; const on = base === route || (base === 'patients' && route === 'patient') || (base === 'admissions' && route === 'admission') || (base === 'ehr' && route === 'ehrlist') || (base === 'orders' && route === 'orders-pt') || (base === 'f485' && route === 'f485-pt') || (base === 'assess' && route === 'assess-pt') || (base === 'sn' && (route === 'sn-pt' || route === 'snnote')) || (base === 'aide' && route === 'aide-pt') || (base === 'staff' && route === 'staff-rec') || (base === 'scheduler' && route === 'scheduler'); a.classList.toggle('on', on); });
  const mail = $('#nav [data-rr="mail"] .badge'); if (mail) { const n = DB.messages.filter(m => m.to === DB.session.userId && !m.read).length; mail.textContent = n; mail.hidden = !n; }
}
function globalSearch() {
  const q = $('#gq').value.trim().toLowerCase(); const res = $('#gsearch .res');
  if (!q) { res.hidden = true; return; }
  const out = [];
  NAV.filter(navVisible).forEach(n => { if (n.r && n.l.toLowerCase().includes(q)) out.push({ t: n.l, s: 'Menu', go: [n.r] }); (n.items || []).filter(navVisible).forEach(i => { if (i.l.toLowerCase().includes(q)) out.push({ t: i.l, s: n.l, go: [i.r, i.p] }); }); });
  DB.patients.filter(p => (ptName(p) + ' ' + p.mrn).toLowerCase().includes(q)).forEach(p => out.push({ t: ptName(p), s: 'Patient, DOB ' + fmtD(p.dob), go: ['patient', { id: p.id }] }));
  DB.staff.filter(s => stName(s).toLowerCase().includes(q)).forEach(s => out.push({ t: stName(s), s: 'Staff (' + s.disc + ')', go: ['staff-rec', { id: s.id }] }));
  res.innerHTML = out.slice(0, 14).map((o, i) => `<a data-act="gsgo" data-i="${i}">${esc(o.t)}<small>${esc(o.s)}</small></a>`).join('') || '<a>No matches</a>';
  res._o = out; res.hidden = false;
}
ACT.gsgo = el => { const res = $('#gsearch .res'); const o = res._o[+el.dataset.i]; res.hidden = true; $('#gq').value = ''; go(o.go[0], o.go[1]); };
ACT.newmenu = el => popMenu(el, [{ label: 'New patient (Patient Demographics + Add)', ic: 'user', run: () => go('patients', { add: 1 }) }, { label: 'New visit (Scheduler)', ic: 'cal', run: () => go('scheduler') }, { label: 'New staff member (Staff + Add)', ic: 'user', run: () => go('staff', { add: 1 }) }, { label: 'New AloraMail message', ic: 'mail', run: () => go('mail', { compose: 1 }) }]);

/* ---------------------------------------------------------------- Home */
const FAQ = [
  ['I cannot log in', 'Try once more slowly. Then tell the Administrator.'], ['The search did not filter', 'Click the blue filter button next to the Search box. Pressing Enter alone does not filter.'],
  ['I cannot find the patient', 'Search last name only, then first name only, then spelling variations. Check Include Inactivated Admissions.'], ['Two records for one patient', 'STOP. Use neither. Tell the Administrator.'],
  ['The folder I need is not listed', 'Do not guess. Ask the Administrator.'], ['A note shows as yellow DRAFT', 'The visit is not finished. Tell the clinician and the DON.'],
  ['Validation errors on a note', 'Click the green pencil next to each message to jump to the field.'], ['I clicked + Add by mistake', 'Click Cancel, then Yes on "This unsaved document will be deleted."'],
  ['Wrong chart or wrong upload', 'STOP. Do not delete. Tell the Administrator now. Possible privacy incident.'], ['A screen differs from the manual', 'Write the real name on the page and tell the Administrator. Screens change over time.'],
];
ROUTES.home = {
  render() {
    return `<div class="flex" style="align-items:flex-start;gap:24px"><div class="grow" style="min-width:0"><div class="hero"><h1>Welcome home.</h1></div><div class="help-bar"><b>Need help with anything?</b> In the real Alora, use the help desk contact shown on your Alora Home screen. In this simulator, open the <a data-act="drawer" data-t="tasks">Practice guide</a>.</div>
      <div class="flex mt" style="align-items:flex-start"><div class="card grow" style="background:#e9e6d3"><h3 style="color:#e5532b;font:300 28px var(--font)">YOU'VE GOTTA SEE THIS (ENHANCEMENT)!</h3><ul><li>Practice release notes would show here.</li><li>The simulator has the screens named in Zenith's manual. Screens that were not photographed are marked <span class="chip simp">SIMPLIFIED</span>.</li></ul></div>
      <div style="width:260px"><h4 style="font:300 22px var(--font)">PAST ALERTS</h4><a data-act="alerts">See Alora announcements &gt;</a><h4 class="mt" style="font:300 22px var(--font)">PERFORM EVEN BETTER!</h4><a data-act="drawer" data-t="tasks">Review the practice tasks</a></div></div></div>
      <div style="width:220px;text-align:center;padding-top:30px"><h3 style="font:300 32px var(--font);color:#333">Top 10 FAQ</h3><a data-act="faq">Go to FAQ</a></div></div>`;
  },
};
ACT.faq = () => modal({ title: 'Top 10 FAQ', size: 'lg', body: FAQ.map(([q, a]) => `<div class="card" style="margin:8px 0"><b>${esc(q)}</b><br>${esc(a)}</div>`).join(''), buttons: [{ label: 'Close', cls: 'btn-close' }] });
ACT.alerts = () => modal({ title: 'Announcements (practice)', body: '<div class="card"><b>09/29/2026</b> Practice announcement: the QA Center now lists Pending documents first.</div><div class="card mt"><b>09/15/2026</b> Practice announcement: remember to lock your computer when you step away.</div>', buttons: [{ label: 'Close', cls: 'btn-close' }] });

/* ---------------------------------------------------------------- Dashboards (counts come from the practice data) */
function visitsOn(day) { return DB.visits.filter(v => v.start.slice(0, 10) === day); }
function visitStatus(v) {
  // returns {label, delayed (minutes), cls}
  const now = nowIso(); const e = v.evv || {};
  if (v.status === 'C') return { label: 'Completed', delayed: 0, cls: 'g' };
  if (v.status === 'A') return { label: 'Cancelled', delayed: 0, cls: 'gr' }; if (v.status === 'M') return { label: 'Missed', delayed: 0, cls: 'r' }; if (v.status === 'H') return { label: 'Hospitalized', delayed: 0, cls: 'o' }; if (v.status === 'O') return { label: 'On Hold', delayed: 0, cls: 'o' };
  if (e.inAt && !e.outAt) return { label: 'In Progress', delayed: Math.max(0, diffMin(e.inAt, v.start)), cls: 'b' };
  if (e.inAt && e.outAt) return { label: 'Clocked out', delayed: 0, cls: 'g' };
  if (now > v.start) { const d = diffMin(now, v.start); if (d > 15 && now < addMin(v.end, 60)) return { label: 'Delayed', delayed: d, cls: 'r' }; if (now >= addMin(v.end, 60)) return { label: 'Missed (no clock in)', delayed: d, cls: 'r' }; }
  return { label: 'Scheduled', delayed: 0, cls: 'gr' };
}
function evvConflicts() {
  const out = []; const now = nowIso();
  DB.visits.forEach(v => {
    const e = v.evv || {}; if (e.resolved) return; const reasons = [];
    if (e.inAt && !e.outAt && now > addMin(v.end, 60)) reasons.push('No clock out');
    if (e.inAt && e.inGps && e.inGps.where && !/patient's home/i.test(e.inGps.where)) reasons.push('Clock in location does not match the patient address (GPS)');
    if (e.outAt && e.outGps && e.outGps.where && !/patient's home/i.test(e.outGps.where)) reasons.push('Clock out location does not match the patient address (GPS)');
    if (e.inAt && Math.abs(diffMin(e.inAt, v.start)) > 60) reasons.push('Clock in more than 60 minutes from the scheduled start');
    if (!e.inAt && now > addMin(v.end, 120) && v.status === 'N') reasons.push('No clock in for a scheduled visit');
    if (reasons.length) out.push({ v, reason: reasons.join('; ') });
  });
  return out;
}
function dashCards() {
  const today = todayIso(); const vt = visitsOn(today); const delayed = vt.filter(v => visitStatus(v).label === 'Delayed').length;
  const qaPend = qaItems().filter(i => i.qa === 'Pending').length; const unsigned = DB.orders.filter(o => !o.signed || !o.received).length; const drafts = DB.snNotes.filter(n => n.status !== 'Completed').length;
  const exp = []; DB.staff.forEach(s => Object.keys(s.creds).forEach(k => { const c = s.creds[k]; if (c.exp && diffDays(c.exp, today) <= 30) exp.push(1); }));
  const refs = DB.referrals.filter(r => r.status === 'In Progress').length; const noa = noaList().filter(n => n.status !== 'Submitted').length; const conf = evvConflicts().length;
  return [['Visits today', vt.length, 'scheduler', ''], ['Delayed visits now', delayed, 'monitor', delayed ? 'bad' : 'ok'], ['EVV conflicts', conf, 'conflicts', conf ? 'warn' : 'ok'], ['QA items pending', qaPend, 'qa', qaPend ? 'warn' : 'ok'],
    ['Orders unsigned or not received', unsigned, 'orders', unsigned ? 'warn' : 'ok'], ['Notes still DRAFT', drafts, 'sn', drafts ? 'warn' : 'ok'], ['Credentials due in 30 days', exp.length, 'staff', exp.length ? 'warn' : 'ok'], ['Referrals in progress', refs, 'patients', ''], ['NOAs not submitted', noa, 'noa', noa ? 'warn' : 'ok']];
}
ROUTES.dashboard = {
  render() {
    const cards = dashCards().map(([t, n, r, c]) => `<div class="card ${c}" style="cursor:pointer" data-go="${r}"><h4>${esc(t)}</h4><div class="n">${n}</div></div>`).join('');
    const rows = visitsOn(todayIso()).sort((a, b) => a.start < b.start ? -1 : 1);
    return pageHead('Dashboard', '') + `<p class="small">Counts come from the practice data and the practice clock. ${simplified()}</p><div class="cardgrid">${cards}</div><div class="box"><h4>Today's visits</h4><table class="t"><thead><tr><th>Time</th><th>Patient</th><th>Caregiver</th><th>Visit</th><th>Status</th></tr></thead><tbody>${rows.map(v => { const s = visitStatus(v); return `<tr><td>${fmtShortT(v.start)} - ${fmtShortT(v.end)}</td><td>${esc(ptName(P(v.pid)))}</td><td>${esc(stName(ST(v.cgId)))}</td><td>${esc(bcDesc(v.billingCode))}</td><td><span class="tag ${s.cls}">${esc(s.label)}${s.delayed && s.label === 'Delayed' ? ' ' + s.delayed + ' min' : ''}</span></td></tr>`; }).join('') || '<tr><td colspan="5" class="none">No visits today</td></tr>'}</tbody></table></div>`;
  },
};
ROUTES['billing-dashboard'] = {
  render() {
    const noa = noaList(); const pb = preBillItems().length;
    return pageHead('Billing Dashboard', '') + `<p class="small">${simplified()} Billing screens are look-only in the simulator. Nothing is billed.</p><div class="cardgrid"><div class="card warn" data-go="noa" style="cursor:pointer"><h4>NOAs not submitted</h4><div class="n">${noa.filter(n => n.status !== 'Submitted').length}</div></div><div class="card warn" data-go="prebill" style="cursor:pointer"><h4>Pre-billing items due</h4><div class="n">${pb}</div></div><div class="card"><h4>Claims created</h4><div class="n">0</div><div class="small">The simulator never creates claims.</div></div><div class="card"><h4>Payments posted</h4><div class="n">0</div></div></div>`;
  },
};
ROUTES.notfound = { render() { return pageHead('Not found', '') + `<p>This address is not part of the simulator.</p><p><a data-go="home">Go to Home</a></p>`; } };
ROUTES.unbuilt = { render(c, p) { return pageHead(p.n || 'Not simulated', '') + `<div class="stub"><b>Not built in this simulator.</b> This menu item exists in the real Alora, but Zenith's manual does not cover it and it was not photographed, so it is not simulated. Ask the Administrator if you need it taught.</div>`; } };
ROUTES.videos = {
  render() {
    const R = [['Office and Intake', 'Alora Training 2 - Admin Setup & Intake; How to Add an Admission; Uploading an Electronic Health Record; Locating Documents; Using Communication Log; Entering and assigning a Referral Source'], ['Scheduler', 'Alora Training 4 - Scheduling; How to schedule a Single Visit; How to create Recurring Visits; How to Create a Missed Visit; Utilizing the CareConnect Monitor & Conflict Screen'],
      ['Human Resources', "Entering Caregivers into Alora; How to track a Caregiver's Absence; Tracking Caregiver Communication; How to Create Pay Rates; How to Utilize Disciplines; Setting up a CareConnect User"], ['Nurse and Clinician', "Alora Training 3 - Clinical Assessments; How to create an OASIS Assessment; How to Analyze an OASIS Assessment; Creating A Skilled Nursing Note; Creating a Plan of Care (485); Creating a Physician's Order or other signed document; CareConnect Overview Tutorial"],
      ['Home Health Aide', 'Creating Home Health Aide Documentation; Home Health Aide Documentation; CareConnect Overview Tutorial'], ['Biller', 'Alora Training 6 - Revenue Readiness; 7 - Revenue Cycling; 8 - Revenue Management; How to create Billing Codes; How to Create Payer'], ['Administrator', 'Alora Training 1 - Activation & Customization of Alora; How to Create Patient Electronic Document Folder; How to Create Physicians; How to Create Missed Visit Reasons']];
    return pageHead('Training Videos', '') + `<p class="note">The real Alora Home screen links to a library of how-to videos. The videos are not part of this simulator. These are the titles Zenith's manual lists for each role.</p><table class="t"><thead><tr><th>Role</th><th>Videos to watch in the real Alora</th></tr></thead><tbody>${R.map(r => `<tr><td><b>${r[0]}</b></td><td>${esc(r[1])}</td></tr>`).join('')}</tbody></table>`;
  },
};
ROUTES.simguide = {
  render() {
    return pageHead('Simulator Guide', '') + `<div class="note sim"><b>What this is.</b> A working practice copy of the Alora screens in Zenith's manual. You can click, type, upload, schedule, clock in on the CareConnect phone, sign notes, and watch the Monitor react. It runs only in this browser tab. Nothing is sent, faxed, billed or exported.</div>
    <div class="box"><h4>How it stays safe</h4><ul><li><b>Practice data only.</b> Every person and number is made up. The practice patient from the manual is <b>DOE, JOHN</b>.</li><li><b>No network.</b> The page cannot send anything anywhere. Uploaded files stay in this browser.</li><li><b>Blocked actions.</b> Things that are real in the real Alora (Generate Claims, Post Payment, faxes, OASIS export) are blocked here and explained.</li><li><b>Zenith rules.</b> When you try something the manual says needs approval, a coaching box appears. Your choices are written in the Coach log.</li><li><b>Reset any time.</b> <a data-act="resetAll">Reset all practice data</a>.</li></ul></div>
    <div class="box"><h4>Try these first</h4><ol><li>Open the <a data-act="drawer" data-t="tasks">Practice guide</a>. It lists a task for each procedure in the manual and checks itself.</li><li>Use <b>Practice as</b> at the top to switch jobs (Office, Scheduler, HR, Nurse, Aide, Biller, Administrator).</li><li>Use <b>+1 hour</b> to move the practice clock and watch visits become late.</li><li>Open the <b>CareConnect phone</b> to clock in and out.</li></ol></div>
    <div class="box"><h4>What is exact and what is simplified</h4><p>Screens that were photographed in the manual are copied closely (names, buttons, columns, order of clicks). Screens that were not photographed are marked <span class="chip simp">SIMPLIFIED PRACTICE VERSION</span>. They work, but their layout is a guess.</p></div>`;
  },
};
ACT.resetAll = () => confirmBox('Reset all practice data?', '<p>This puts every patient, visit, document and setting back the way it was when you first opened the simulator.</p>', () => { resetAll(); closeAllModals(); showLogin(); history.replaceState(null, '', '#/login'); toast('Practice data reset.', 'ok'); }, { yes: 'Reset', no: 'Cancel', kind: 'warn' });

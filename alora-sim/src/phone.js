'use strict';
/* =====================================================================================================
   The CareConnect practice phone: today's schedule, Clock In / Clock Out with a GPS location choice,
   the visit note (SN note, aide note or simple note) and signatures. Everything it does changes the
   same practice data the office screens read (Monitor, Conflicts, SN Notes, Aide Documents).
   ===================================================================================================== */
const PH = { screen: 'login', sess: '', vid: '', ctx: null, nctx: null, tabI: 0, msg: '', err: '' };
const PH_LOCS = [['home', "At the patient's home"], ['car', 'In my car, about 1.2 miles from the home'], ['office', 'At the office, about 4.8 miles away'], ['away', 'At my own house, about 9 miles away'], ['off', 'Location services OFF']];
function phState() { DB.ui.phone = DB.ui.phone || { open: false, who: 'S1', loc: 'home' }; return DB.ui.phone; }
function gpsFor(pt, loc) {
  const base = { lat: pt.lat, lng: pt.lng };
  if (loc === 'home') return Object.assign(base, { where: "At the patient's home" });
  if (loc === 'car') return { lat: pt.lat + 0.018, lng: pt.lng, where: 'About 1.2 miles from the home' };
  if (loc === 'office') return { lat: pt.lat + 0.07, lng: pt.lng + 0.02, where: 'At the office, about 4.8 miles from the home' };
  return { lat: pt.lat - 0.13, lng: pt.lng - 0.05, where: 'Away from the home, about 9 miles' };
}
function asPhone(fn) { const o = ACTOR_STAFF; ACTOR_STAFF = PH.sess || null; try { return fn(); } finally { ACTOR_STAFF = o; } }
function docComplete(v) {
  const d = discFor(v);
  if (v.billingCode && SN_CODES.indexOf(v.billingCode) >= 0) { const n = v.noteId ? byId(DB.snNotes, v.noteId) : null; return !!n && n.status === 'Completed'; }
  if (d === 'HHA') { const a = DB.aideDocs.find(x => x.kind === 'note' && x.visitId === v.id); return !!a && a.status === 'Completed'; }
  return !!(v.simpleDoc && v.simpleDoc.done);
}
function finishIfDone(v) { if (v.status === 'N' && v.evv && v.evv.outAt && docComplete(v)) { v.status = 'C'; save(); } }

ACT.phoneopen = () => { const s = phState(); s.open = true; save(); track('phone:open'); phoneRefresh(); };
ACT.phoneSide = () => { const s = phState(); s.left = !s.left; save(); phoneRefresh(); };
ACT.phoneclose = () => { phState().open = false; save(); phoneRefresh(); };
function phoneRefresh() {
  const root = $('#phone-root'); if (!root) return; const st = phState();
  if (!DB || !DB.session.userId || !st.open) { root.innerHTML = ''; return; }
  if (!PH.ctx) { PH.ctx = ctxNew({ who: st.who, loc: st.loc }); PH.ctx._rr = phoneRefresh; }
  const staff = DB.staff.filter(s => s.cc && s.cc.enabled);
  const sc = $('.scr', root); const sy = sc ? sc.scrollTop : 0;
  root.innerHTML = `<div id="phone" class="${st.left ? 'left' : ''}" data-c="${PH.ctx._id}"><button class="xbtn" data-act="phoneclose">Close phone</button><button class="xbtn" style="right:96px" data-act="phoneSide">Move phone</button><div class="ph-top"><span id="phtime">${fmtT(nowIso())}</span><span>CareConnect (practice)</span><span>LTE &#9646;&#9646;&#9646;</span></div><div class="scr">${phScreen()}</div>
    <div class="ph-ctl"><b>Practice controls</b> (not part of the app)<br>Who is holding this phone?<select id="phWho">${staff.map(s => `<option value="${s.id}"${s.id === st.who ? ' selected' : ''}>${esc(stName(s))} (${s.disc})</option>`).join('')}</select>My location right now:<select id="phLoc">${PH_LOCS.map(([k, l]) => `<option value="${k}"${k === st.loc ? ' selected' : ''}>${l}</option>`).join('')}</select></div></div>`;
  const sc2 = $('.scr', root); if (sc2) sc2.scrollTop = sy;
}
document.addEventListener('change', e => {
  const t = e.target; if (!t || !t.id) return;
  if (t.id === 'phWho') { const s = phState(); s.who = t.value; PH.sess = ''; PH.screen = 'login'; save(); phoneRefresh(); }
  if (t.id === 'phLoc') { phState().loc = t.value; save(); phoneRefresh(); }
});
setInterval(() => { const e = $('#phtime'); if (e && DB) e.textContent = fmtT(nowIso()); }, 5000);
// every change inside a note on the phone is saved straight away
document.addEventListener('change', e => { if (e.target.closest && e.target.closest('#phone') && PH.nctx) { if (PH.screen === 'sn' || PH.screen === 'aide' || PH.screen === 'simple') { if (PH.nctx.n && PH.nctx.n.id) save(); } } });

function appHead(sub, back) { const s = PH.sess ? ST(PH.sess) : null; return `<div class="app-h"><div>${back ? `<button class="ph-x" data-act="phBack">&#8249;</button> ` : ''}CareConnect<small>${esc(sub || (s ? stName(s) : 'Practice app'))}</small></div>${s ? '<button class="ph-x" data-act="phLogout" title="Log out">&#9211;</button>' : ''}</div>`; }
function phScreen() {
  const st = phState();
  if (!PH.sess) {
    const s = ST(st.who); const u = DB.users.find(x => x.staffId === st.who) || { username: s && s.cc.user ? s.cc.user : '' };
    return `${appHead('Sign in')}<div class="ph-b"><p class="tiny">Practice phone. Use your own login. Never share it or sign in for another person.</p><div class="pf"><label>Username</label><input id="phU" type="text" value="${esc(u.username || (s && s.cc.user) || '')}" autocomplete="off"></div><div class="pf"><label>Password</label><input id="phP" type="password" value="practice" autocomplete="off"></div><button class="bigbtn in" data-act="phLogin">Sign in</button>${PH.err ? `<div class="note err"><span>${esc(PH.err)}</span></div>` : ''}<p class="tiny">Practice password for every login: practice</p></div>`;
  }
  const v = PH.vid ? byId(DB.visits, PH.vid) : null;
  if (PH.screen === 'sched' || !v) return phSchedule();
  if (PH.screen === 'visit') return phVisit(v);
  const wrap = html => `<div data-c="${PH.nctx._id}" style="display:contents">${html}</div>`;
  if (PH.screen === 'sn') return wrap(phSN(v));
  if (PH.screen === 'aide') return wrap(phAide(v));
  if (PH.screen === 'simple') return wrap(phSimple(v));
  if (PH.screen === 'missed') return phMissed(v);
  return phSchedule();
}
ACT.phLogin = () => { const u = DB.users.find(x => x.username === $('#phU').value.trim().toLowerCase() && x.active) ; const s = phState(); const staff = ST(s.who);
  const okUser = (u && u.staffId === s.who) || (staff && staff.cc.user === $('#phU').value.trim().toLowerCase());
  if (!okUser || ($('#phP').value !== 'practice')) { PH.err = 'Login failed. Check your username and password. (Practice: the username must belong to the person holding the phone.)'; phoneRefresh(); return; }
  PH.sess = s.who; PH.err = ''; PH.screen = 'sched'; track('phone:login'); phoneRefresh(); };
ACT.phLogout = () => { PH.sess = ''; PH.screen = 'login'; PH.vid = ''; phoneRefresh(); };
ACT.phBack = () => { if (PH.screen === 'visit' || PH.screen === 'missed') { PH.screen = 'sched'; PH.vid = ''; } else PH.screen = 'visit'; PH.msg = ''; phoneRefresh(); };
function phSchedule() {
  const today = todayIso(); const mine = DB.visits.filter(v => v.cgId === PH.sess && v.status !== 'A').sort((a, b) => (a.start < b.start ? -1 : 1));
  const card = v => { const pt = P(v.pid), s = visitStatus(v); return `<div class="vcard" data-act="phVisit" data-id="${v.id}"><b>${fmtT(v.start)} - ${fmtT(v.end)}</b> <span class="tag ${s.cls}" style="float:right">${esc(s.label)}${s.label === 'Delayed' ? ' ' + s.delayed + ' min' : ''}</span><br>${esc(ptName(pt))}<br><span class="tiny">${esc(bcDesc(v.billingCode))}</span></div>`; };
  const t = mine.filter(v => v.start.slice(0, 10) === today), up = mine.filter(v => v.start.slice(0, 10) > today && v.start.slice(0, 10) <= addDays(today, 3));
  return `${appHead()}<div class="ph-b"><b>Today's schedule</b> <span class="tiny">${DAYS[toDate(today).getDay()]} ${fmtD(today)}</span>${t.map(card).join('') || '<p class="tiny" style="margin:14px 0">No visits today.</p>'}<b>Coming up</b>${up.map(v => `<div class="tiny" style="margin-top:6px">${fmtD(v.start)} ${fmtT(v.start)} ${esc(ptName(P(v.pid)))}</div>`).join('') || '<p class="tiny">Nothing in the next 3 days.</p>'}</div>`;
}
ACT.phVisit = el => { PH.vid = el.dataset.id; PH.screen = 'visit'; PH.msg = ''; track('phone:openvisit'); phoneRefresh(); };
function phVisit(v) {
  const pt = P(v.pid), e = v.evv || {}, s = visitStatus(v), adm = admOf(v.pid); const clockedIn = !!e.inAt, clockedOut = !!e.outAt;
  let btn = '';
  if (v.status === 'M') btn = `<div class="note"><span>This visit is marked Missed (${esc(v.missedReason || '')}).</span></div>`;
  else if (!clockedIn) btn = `<button class="bigbtn in" data-act="phClockIn">Clock In</button><p class="tiny">Tap Clock In only when you are inside the patient's home.</p><button class="bigbtn gray" data-act="phMissedGo">I cannot complete this visit</button>`;
  else if (!clockedOut) btn = `<div class="note ok"><span>Clocked in at ${fmtT(e.inAt)}</span></div><button class="bigbtn gray" data-act="phDoc">Document the visit</button><button class="bigbtn out" data-act="phClockOut">Clock Out</button>`;
  else btn = `<div class="note ok"><span>Clocked in ${fmtT(e.inAt)}. Clocked out ${fmtT(e.outAt)}.</span></div>${docComplete(v) ? '<div class="note ok"><span>Note complete and signed.</span></div>' : '<button class="bigbtn gray" data-act="phDoc">Finish the visit note</button>'}`;
  return `${appHead('Visit', true)}<div class="ph-b"><div class="tag ${s.cls}">${esc(s.label)}${s.label === 'Delayed' ? ' ' + s.delayed + ' min' : ''}</div><h3 style="margin:8px 0 2px">${esc(ptName(pt))}</h3><div class="tiny">${esc([pt.addr1, pt.city, pt.state, pt.zip].join(', '))}</div><div class="tiny">${esc(pt.phones.home)}</div><div style="margin:8px 0"><b>${fmtD(v.start)}</b> ${fmtT(v.start)} - ${fmtT(v.end)}<br><span class="tiny">${esc(bcDesc(v.billingCode))}</span></div>${adm && adm.other.precautions ? `<div class="note warn"><span><b>Precautions:</b> ${esc(adm.other.precautions)}</span></div>` : ''}${PH.msg ? `<div class="note ${PH.msgKind || 'warn'}"><span>${esc(PH.msg)}</span></div>` : ''}${btn}</div>`;
}
ACT.phClockIn = () => {
  const v = byId(DB.visits, PH.vid); const st = phState(); const pt = P(v.pid); PH.msg = ''; PH.msgKind = 'warn';
  if (st.loc === 'off') { PH.msg = 'Location services are off. EVV needs your GPS location, so the app will not clock you in. Turn on location (Practice controls below).'; track('phone:nogps'); simLog('good', 'The app refused to clock in with location services off'); phoneRefresh(); return; }
  const other = DB.visits.find(x => x.cgId === PH.sess && x.id !== v.id && x.evv && x.evv.inAt && !x.evv.outAt && x.start.slice(0, 10) === todayIso());
  if (other) { PH.msg = 'You are still clocked in at another visit (' + ptName(P(other.pid)) + '). Clock out there first.'; phoneRefresh(); return; }
  v.evv = v.evv || {}; v.evv.inAt = nowIso(); v.evv.inGps = gpsFor(pt, st.loc); v.evv.outAt = ''; v.evv.outGps = null; v.evv.resolved = false;
  save(); track('phone:clockin'); if (st.loc !== 'home') { track('phone:clockin-away'); PH.msg = 'You clocked in away from the patient\'s home. Never clock in from the car, the office, or home. The office will see a GPS conflict.'; simLog('override', 'Clocked in away from the patient\'s home (' + v.evv.inGps.where + ')'); } else simLog('info', 'Clocked in at the patient\'s home');
  if (Math.abs(diffMin(v.evv.inAt, v.start)) > 60) { PH.msg = (PH.msg ? PH.msg + ' ' : '') + 'You clocked in more than 60 minutes from the scheduled start. This will show on the Conflicts screen.'; }
  phoneRefresh(); refresh();
};
ACT.phClockOut = () => {
  const v = byId(DB.visits, PH.vid); const st = phState(); const pt = P(v.pid); PH.msg = ''; PH.msgKind = 'warn';
  if (st.loc === 'off') { PH.msg = 'Location services are off. Turn on location to clock out.'; phoneRefresh(); return; }
  const go2 = () => { v.evv.outAt = nowIso(); v.evv.outGps = gpsFor(pt, st.loc); finishIfDone(v); save(); track('phone:clockout'); if (st.loc !== 'home') { track('phone:clockout-away'); PH.msg = 'You clocked out away from the patient\'s home. The office will see a GPS conflict.'; simLog('override', 'Clocked out away from the patient\'s home'); } else simLog('info', 'Clocked out at the patient\'s home'); phoneRefresh(); refresh(); };
  if (!docComplete(v)) { PH.msg = ''; modal({ title: 'The note is not finished', kind: 'warn', size: 'sm', body: '<p>Zenith standard: document before you leave the home whenever possible. A note that is not signed stays DRAFT and the visit is not completed.</p>', buttons: [{ label: 'Go back and document (recommended)', cls: 'btn-ok' }, { label: 'Clock out anyway', cls: 'btn-or', click: go2 }] }); return; }
  go2();
};
ACT.phMissedGo = () => { PH.screen = 'missed'; phoneRefresh(); };
function phMissed(v) { return `${appHead('Cannot complete visit', true)}<div class="ph-b"><div class="note err"><span><b>Emergency?</b> Call 911 first, then the office.</span></div><p>Why can't you complete this visit? The office will be told.</p>${DB.lists.missedReasons.map(r => `<button class="bigbtn gray" data-act="phMissedPick" data-r="${esc(r)}" style="padding:10px;font-size:14px">${esc(r)}</button>`).join('')}</div>`; }
ACT.phMissedPick = el => { const v = byId(DB.visits, PH.vid); v.status = 'M'; v.missedReason = el.dataset.r; save(); track('phone:missed'); simLog('info', 'Visit marked Missed from the phone: ' + el.dataset.r); PH.screen = 'visit'; PH.msg = 'The office was told. Call the office now.'; PH.msgKind = 'ok'; phoneRefresh(); refresh(); };

/* ---------------------------------------------------------------- documenting the visit */
ACT.phDoc = () => {
  const v = byId(DB.visits, PH.vid); const d = discFor(v); PH.tabI = 0; PH.msg = '';
  if (SN_CODES.indexOf(v.billingCode) >= 0) { const n = ensureNote(v); n.start = v.evv.inAt; n.end = v.evv.outAt || ''; n.data = n.data || {}; n.sig = n.sig || {}; PH.nctx = ctxNew({ n }); PH.nctx._rr = phoneRefresh; PH.screen = 'sn'; }
  else if (d === 'HHA') { const poc = aidePoc(v.pid); let ex = DB.aideDocs.find(x => x.kind === 'note' && x.visitId === v.id); if (!ex) { ex = { id: uid('AD'), pid: v.pid, kind: 'note', title: 'Aide Note', visitId: v.id, cgId: v.cgId, from: v.start.slice(0, 10), to: v.start.slice(0, 10), status: 'In Use', tasks: [], done: {}, why: {}, narrative: '', sig: null, pat: null, by: DB.session.userId }; DB.aideDocs.push(ex); save(); } PH.nctx = ctxNew({ n: { visitId: v.id, done: JSON.parse(JSON.stringify(ex.done || {})), why: JSON.parse(JSON.stringify(ex.why || {})), narrative: ex.narrative || '', sig: ex.sig || null, pat: ex.pat || null }, ex, poc }); PH.nctx._rr = phoneRefresh; PH.screen = 'aide'; }
  else { v.simpleDoc = v.simpleDoc || { text: '', sig: null, done: false }; PH.nctx = ctxNew({ n: v.simpleDoc }); PH.nctx._rr = phoneRefresh; PH.screen = 'simple'; }
  phoneRefresh();
};
function phNoteHead(title, sub) { return `${appHead(title, true)}`; }
function phSN(v) {
  const c = PH.nctx; const n = c.n; const tabs = SN_TABS; const i = Math.min(PH.tabI, tabs.length - 1); const tab = tabs[i];
  let body = '';
  if (tab.k === 'vital') body += `<div class="pf"><label>Type of Visit</label>${VISIT_TYPES.map(t => radio(c, 'n.visitType', t, t)).join('<br>')}</div>`;
  if (tab.k === 'qa') {
    const { errs, warns } = snValidation(c);
    body += `<div class="note ${errs.length ? 'err' : 'ok'}"><span><b>Errors: ${errs.length}</b> &nbsp; Warnings: ${warns.length}</span></div>${errs.concat(warns).map(x => `<div class="tiny" style="margin:4px 0"><a data-act="phJump" data-tab="${x.tab}">&#9998;</a> <b>${esc(x.tabLabel)}</b>: ${esc(x.msg)}</div>`).join('')}
      <div class="box"><b>Nurse signature</b><br>${n.sig && n.sig.nurse ? sigImg(n.sig.nurse, 40) + '<div class="tiny">' + fmtDT(n.sig.nurse.at) + '</div>' : (n.nurseSigned ? 'Signed' : `<button class="bigbtn in" style="padding:9px;font-size:14px" data-act="phSignN">Sign as ${esc(stName(ST(n.cgId)))}</button>`)}</div>
      <div class="box"><b>Patient signature</b><br>${n.sig && n.sig.pat ? sigImg(n.sig.pat, 40) : (n.patSigned ? 'Signed' : `<button class="bigbtn gray" style="padding:9px;font-size:14px" data-act="phSignP">Patient signs</button><label class="chk tiny"><input type="checkbox" ${battr(c, 'n.patUnable')} data-rr="1"${n.patUnable ? ' checked' : ''}> Patient unable to sign</label>${n.patUnable ? inp(c, 'n.patUnableWhy', { ph: 'Reason' }) : ''}`)}</div>
      ${n.status === 'Completed' ? '<div class="note ok"><span>The note is complete. QA Pending.</span></div>' : ''}<p class="tiny"><a data-act="phFill">Practice shortcut: fill every tab</a></p>`;
  }
  body += tab.secs.map(s => snSectionHtml(c, s, false)).join('');
  if (tab.k === 'summ') body += `<div class="pf"><label>Narrative (summary of the visit)</label>${txt(c, 'n.data.narrative', { rows: 4 })}</div>`;
  return `${phNoteHead('SN note')}<div class="ph-b"><div class="tiny">${esc(ptName(P(n.pid)))}</div><div class="tiny">${i + 1} of ${tabs.length}</div><h3 style="margin:2px 0 6px">${esc(tab.l)}</h3>${body}<div class="flex mt"><button data-act="phTab" data-d="-1" style="flex:1;padding:8px">&#8249; Back</button><button data-act="phTab" data-d="1" style="flex:1;padding:8px">Next &#8250;</button></div></div>`;
}
ACT.phTab = el => { const n = SN_TABS.length; PH.tabI = Math.max(0, Math.min(n - 1, PH.tabI + +el.dataset.d)); phoneRefresh(); };
ACT.phJump = el => { PH.tabI = SN_TABS.findIndex(t => t.k === el.dataset.tab); phoneRefresh(); };
ACT.phFill = () => { const c = PH.nctx; c.n.data = Object.assign(c.n.data || {}, snFullData()); if (!c.n.visitType) c.n.visitType = 'Skilled Nursing'; save(); phoneRefresh(); toast('Sample answers entered on every tab.', 'sim'); };
ACT.phSignN = () => asPhone(() => { const c = PH.nctx; if (!snSignGuard(c, 'nurse')) return; sigPad('Nurse Signature', stName(ST(c.n.cgId)), s => { c.n.sig = c.n.sig || {}; c.n.sig.nurse = s; c.n.nurseSigned = true; c.n.signedAt = s.at; track('sn:nursesigned'); track('phone:signed'); snAfterSign(c); finishIfDone(byId(DB.visits, PH.vid)); phoneRefresh(); refresh(); }); });
ACT.phSignP = () => { const c = PH.nctx; sigPad('Patient Signature', ptName(P(c.n.pid)), s => { c.n.sig = c.n.sig || {}; c.n.sig.pat = s; c.n.patSigned = true; track('sn:patsigned'); asPhone(() => snAfterSign(c)); finishIfDone(byId(DB.visits, PH.vid)); phoneRefresh(); refresh(); }, { hint: 'Hand the phone to the patient. The patient signs in the box. Patient: ' }); };

function phAide(v) {
  const c = PH.nctx; const n = c.n, poc = c.poc; const tasks = poc ? poc.tasks : [];
  return `${phNoteHead('Aide note')}<div class="ph-b"><div class="tiny">${esc(ptName(P(v.pid)))}</div>${poc ? '' : '<div class="note warn"><span>There is no Aide Plan of Care. Stop and call the RN.</span></div>'}<h3 style="margin:2px 0 6px">Tasks</h3>${tasks.map((t, i) => `<div class="box" style="margin:6px 0;padding:6px 8px"><b>${esc(t)}</b><br>${radio(c, 'n.done.' + i, 'Done', 'Done', { rr: 1 })} ${radio(c, 'n.done.' + i, 'Not done', 'Not done', { rr: 1 })}${n.done[i] === 'Not done' ? inp(c, 'n.why.' + i, { ph: 'Why was it not done?' }) : ''}</div>`).join('')}<div class="pf"><label>Narrative</label>${txt(c, 'n.narrative', { rows: 3 })}</div>
    <div class="box"><b>Aide signature</b><br>${n.sig ? sigImg(n.sig, 40) : '<button class="bigbtn in" style="padding:9px;font-size:14px" data-act="phAideSign">Sign</button>'}</div><div class="box"><b>Patient signature (if able)</b><br>${n.pat ? sigImg(n.pat, 40) : '<button class="bigbtn gray" style="padding:9px;font-size:14px" data-act="phAideSignP">Patient signs</button>'}</div>
    ${c.ex.status === 'Completed' ? '<div class="note ok"><span>The note is complete.</span></div>' : ''}<button class="bigbtn in" data-act="phAideDone">Complete the note</button><button class="bigbtn gray" data-act="phAideDraft">Save draft</button></div>`;
}
function aideBind(c) { return { n: c.n }; }
ACT.phAideSign = () => asPhone(() => { const c = PH.nctx; const v = byId(DB.visits, PH.vid); if (!isMine(v.cgId)) { neverDo('Sign for another aide', 'Zenith rule: never sign for another person.', 'AI2'); return; } sigPad('Aide Signature', stName(ST(v.cgId)), s => { c.n.sig = s; phoneRefresh(); }); });
ACT.phAideSignP = () => { const c = PH.nctx; const v = byId(DB.visits, PH.vid); sigPad('Patient Signature', ptName(P(v.pid)), s => { c.n.pat = s; phoneRefresh(); }); };
ACT.phAideDone = () => asPhone(() => { const c = PH.nctx; const v = byId(DB.visits, PH.vid); c.n.visitId = v.id; const r = aideNoteSave(v.pid, c.ex, { n: c.n }, c.poc, true); if (r !== false) { finishIfDone(v); } phoneRefresh(); });
ACT.phAideDraft = () => asPhone(() => { const c = PH.nctx; const v = byId(DB.visits, PH.vid); c.n.visitId = v.id; aideNoteSave(v.pid, c.ex, { n: c.n }, c.poc, false); phoneRefresh(); });

function phSimple(v) {
  const c = PH.nctx; const n = c.n;
  return `${phNoteHead('Visit note')}<div class="ph-b"><div class="tiny">${esc(ptName(P(v.pid)))} &nbsp; ${esc(bcDesc(v.billingCode))}</div><div class="pf"><label>What you did and observed (use the patient's own words for complaints)</label>${txt(c, 'n.text', { rows: 7 })}</div><div class="box"><b>Your signature</b><br>${n.sig ? sigImg(n.sig, 40) : '<button class="bigbtn in" style="padding:9px;font-size:14px" data-act="phSimpleSign">Sign</button>'}</div>${n.done ? '<div class="note ok"><span>The note is complete.</span></div>' : '<button class="bigbtn in" data-act="phSimpleDone">Complete the note</button>'}</div>`;
}
ACT.phSimpleSign = () => asPhone(() => { const c = PH.nctx; const v = byId(DB.visits, PH.vid); if (!isMine(v.cgId)) { neverDo('Sign for someone else', 'Zenith rule: never sign for another person.', 'N3'); return; } sigPad('Signature', stName(ST(v.cgId)), s => { c.n.sig = s; save(); phoneRefresh(); }); });
ACT.phSimpleDone = () => { const c = PH.nctx; const v = byId(DB.visits, PH.vid); if (!String(c.n.text || '').trim()) { toast('Write the note first.', 'err'); return; } if (!c.n.sig) { toast('Sign the note first.', 'err'); return; } c.n.done = true; const map = { PT: 'pt', PTA: 'pt', OT: 'ot', OTA: 'ot', ST: 'st', MSW: 'msw' }; const type = map[discFor(v)] || 'sup'; DB.forms.push({ id: uid('FM'), pid: v.pid, type, date: v.start.slice(0, 10), d: { f1: 'Visit note', f2: c.n.text }, by: DB.session.userId }); finishIfDone(v); save(); track('phone:simple-done'); phoneRefresh(); refresh(); };

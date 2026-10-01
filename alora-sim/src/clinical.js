'use strict';
/* =====================================================================================================
   Clinical: signature pad, Assessments (OASIS), Skilled Nursing visit notes, Aide documents
   ===================================================================================================== */
let ACTOR_STAFF = null; // set while the practice phone acts for the person holding it
function myStaff() { if (ACTOR_STAFF) return ST(ACTOR_STAFF); const u = curUser(); return u && u.staffId ? ST(u.staffId) : null; }
function isMine(cgId) { const s = myStaff(); return !!s && s.id === cgId; }
function isClinicalRole() { return ['Nurse', 'DON', 'Administrator'].indexOf(curRole()) >= 0; }

/* ---------------------------------------------------------------- signature pad (draw with the mouse or finger, or type a name) */
function sigPad(title, who, cb, o) {
  o = o || {};
  const m = ctxNew({ name: '', drawn: false });
  modal({ title, ctx: m, size: 'sm', noFocus: true, z: o.z, noEsc: false,
    body: c => `<p class="small">${esc(o.hint || 'Sign inside the box with the mouse or your finger. You are signing as: ')}<b>${esc(who)}</b></p><canvas class="sig" width="420" height="130" id="sigcv"></canvas>
      <div class="flex mt"><button class="btn btn-light btn-sm" data-act="sigClear">Clear</button><span class="small">or type your full name instead:</span></div>${inp(c, 'name', { ph: 'Type your full name' })}
      <p class="small mt">Practice signature. It stays in this browser.</p>`,
    mount: (c, mm) => {
      const cv = $('#sigcv', mm.el); if (!cv) return; const g = cv.getContext('2d'); g.lineWidth = 2.2; g.lineCap = 'round'; g.strokeStyle = '#1a3a8a'; let down = false;
      const pos = e => { const r = cv.getBoundingClientRect(); return [(e.clientX - r.left) * cv.width / r.width, (e.clientY - r.top) * cv.height / r.height]; };
      cv.addEventListener('pointerdown', e => { down = true; cv.setPointerCapture(e.pointerId); const [x, y] = pos(e); g.beginPath(); g.moveTo(x, y); g.lineTo(x + .1, y + .1); g.stroke(); c.drawn = true; });
      cv.addEventListener('pointermove', e => { if (!down) return; const [x, y] = pos(e); g.lineTo(x, y); g.stroke(); });
      cv.addEventListener('pointerup', () => { down = false; });
    },
    buttons: [{ label: 'Save signature', cls: 'btn-ok', click: (mm) => {
      const cv = $('#sigcv', mm.el); let img;
      if (m.drawn) img = cv.toDataURL('image/png');
      else if (m.name.trim().length >= 3) { const g = cv.getContext('2d'); g.clearRect(0, 0, cv.width, cv.height); g.fillStyle = '#fff'; g.fillRect(0, 0, cv.width, cv.height); g.fillStyle = '#1a3a8a'; g.font = 'italic 44px "Brush Script MT", "Segoe Script", cursive'; g.fillText(m.name.trim(), 16, 80); img = cv.toDataURL('image/png'); }
      else { toast('Draw your signature in the box, or type your full name.', 'err'); return false; }
      cb({ img, name: m.name.trim() || who, at: nowIso(), by: DB.session.userId });
    } }, { label: 'Cancel', cls: 'btn-del' }] });
}
ACT.sigClear = el => { const m = ctxOf(el); const cv = $('#sigcv', m._modal.el); cv.getContext('2d').clearRect(0, 0, cv.width, cv.height); m.drawn = false; };
function sigImg(s, h) { return s && s.img ? `<img src="${s.img}" alt="signature" style="height:${h || 46}px;border-bottom:1px solid #666;background:#fff">` : ''; }

/* ---------------------------------------------------------------- Assessments (OASIS / non-OASIS) */
const ASMT_TYPES = ['OASIS', 'Non-OASIS', 'Pediatric Assessment', 'Non-Skilled Assessment'];
const M0100 = [['01', 'Start of care'], ['03', 'Resumption of care'], ['04', 'Recertification'], ['05', 'Other follow-up'], ['06', 'Transfer to an inpatient facility, patient not discharged'], ['07', 'Transfer to an inpatient facility, patient discharged'], ['08', 'Death at home'], ['09', 'Discharge from agency']];
const ADL_ITEMS = [['m1800', 'M1800 Grooming'], ['m1810', 'M1810 Dress upper body'], ['m1820', 'M1820 Dress lower body'], ['m1830', 'M1830 Bathing'], ['m1840', 'M1840 Toilet transferring'], ['m1845', 'M1845 Toileting hygiene'], ['m1850', 'M1850 Transferring'], ['m1860', 'M1860 Ambulation and locomotion']];
const ADL_OPTS = [['0', '0 Able to do it independently'], ['1', '1 Needs a device or some help'], ['2', '2 Needs hands on help'], ['3', '3 Cannot do it, dependent']];
function asmtReasonText(a) { const k = (a.data && a.data.m0100) || ''; const x = M0100.find(r => r[0] === k); return x ? k + ' ' + x[1] : (a.reason || ''); }
function asmtIsSoc(a) { return a.type === 'OASIS' && ((a.data && a.data.m0100) === '01' || /^01/.test(a.reason || '')); }
function asmtScore(a) { const d = a.data || {}; return ADL_ITEMS.reduce((n, [k]) => n + (d[k] === '' || d[k] == null ? 0 : +d[k]), 0); }
function asmtHipps(a) {
  const d = a.data || {}; const sc = asmtScore(a); const lvl = sc >= 17 ? 3 : sc >= 9 ? 2 : 1; const dx = (d.dx1 || 'A').toUpperCase().charAt(0); const letter = 'ABCDEFGHIJKL'.charAt('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.indexOf(dx) % 12);
  return { code: '1' + letter + lvl + 'A1', pay: (1800 + lvl * 450 + (d.dx1 ? 120 : 0)).toFixed(2) };
}
function asmtErrors(a) {
  const d = a.data || {}; const e = [];
  if (!parseD(d.m0090T || '')) e.push('M0090 Date Assessment Completed is required.'); if (!d.m0100) e.push('M0100 Reason for Assessment is required.'); if (!d.m0080) e.push('M0080 Discipline of the person completing the assessment is required.');
  if (a.type === 'OASIS') { if (!d.dx1) e.push('M1021 Primary Diagnosis is required.'); ADL_ITEMS.forEach(([k, l]) => { if (d[k] === '' || d[k] == null) e.push(l + ' must be answered.'); }); }
  return e;
}
ROUTES.assess = { render(c) { return admSearchPage(c, 'Assessments (OASIS/NON-OASIS)', 'assess-pt', { sub: 'Patient Admission Search' }); } };
ROUTES['assess-pt'] = {
  render(c, p) {
    const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return notice('Not found.', 'err');
    const tbl = DT(c, 'as', () => ({ sort: 'comp', dir: -1, firstLast: false,
      cols: [{ key: 'act', label: 'Select', sortable: false, blue: true, render: r => rowIcons([{ ic: 'edit', t: 'Open', act: 'asOpen', data: { id: r.id } }, { ic: 'trash', t: 'Delete', act: 'asDel', data: { id: r.id }, cls: 'del' }]) },
        { key: 'comp', label: 'Asmt Comp Dt', blue: true, text: r => r.compDate, render: r => fmtD(r.compDate) }, { key: 'type', label: 'Type', render: r => esc(r.type) }, { key: 'reason', label: 'Reason for Assessment', text: r => asmtReasonText(r), render: r => esc(asmtReasonText(r)) },
        { key: 'qa', label: 'QA Status', render: r => tagFor(r.qa) }, { key: 'exp', label: 'Export Status', render: r => esc(r.qa === 'In Use' ? 'In Use' : 'Not exported (simulator)') }, { key: 'hipps', label: 'HIPPS', text: r => (r.hipps || ''), render: r => esc(r.hipps || '') }, { key: 'pay', label: 'Payment', render: r => esc(r.payment || '0.00') }],
      rows: DB.assessments.filter(x => x.pid === pt.id) }));
    return pageHead('Assessments', 'Summary') + `<div class="bar"><h2>${ic('user')} ${esc(ptName(pt))}</h2><button class="btn btn-add" data-act="asAdd" data-aid="${a.id}">${ic('plus')} Add</button><button class="btn btn-back" data-act="asBack">${ic('back')} Back</button></div>${tbl}<p class="small">${simplified()} The OASIS form here has the key items (reason, diagnosis, daily living) and a practice payment estimate. The real OASIS has many more questions. Export is blocked in the simulator.</p>${gotoBtn()}${gotoPanel(c, a)}`;
  },
};
ACT.asBack = () => go('assess');
ACT.asOpen = el => { track('assess:open'); go('assess-edit', { id: el.dataset.id }); };
ACT.asDel = el => needApproval({ roles: ['Administrator'], what: 'Delete an assessment', rule: 'Never delete an assessment unless the DON or Administrator authorizes it. Ask the DON to remove a practice assessment.', who: 'DON or Administrator', ref: 'N2', go: () => confirmBox('Delete assessment?', '<p>Delete this assessment from the practice data?</p>', () => { DB.assessments = DB.assessments.filter(x => x.id !== el.dataset.id); save(); refresh(); }, { yes: 'Delete', no: 'Cancel' }) });
ACT.asAdd = el => {
  const a = byId(DB.admissions, el.dataset.aid);
  const open = () => {
    const m = ctxNew({ d: '', type: 'OASIS' });
    const existing = DB.assessments.find(x => x.pid === a.pid && asmtIsSoc(x));
    modal({ title: 'Enter Assessment Completed Date', ctx: m, size: 'sm', body: c => `${existing ? notice('An SOC assessment already exists for this admission (' + fmtD(existing.compDate) + '). Zenith rule: one SOC OASIS per admission. STOP and ask the DON.', 'warn') : ''}${fg('(M0090) Date Assessment Completed', dp(c, 'd'), { req: 1 })}<div class="fg chkbox" style="display:block">${ASMT_TYPES.map(t => radio(c, 'type', t, t)).join('<br>')}</div>`,
      buttons: [{ label: 'OK', cls: 'btn-ok', click: () => {
        const d = parseD(m.d); if (!d) { toast('Enter the date the assessment was completed (MM/DD/YYYY).', 'err'); return false; }
        const make = () => { const rec = { id: uid('AS'), pid: a.pid, type: m.type, compDate: d, reason: '', qa: 'In Use', exportStatus: 'In Use', hipps: '', payment: '0.00', lupa: '-', data: { m0090T: fmtD(d), m0100: '', m0080: '', dx1: '', dxd: '' }, by: DB.session.userId }; ADL_ITEMS.forEach(([k]) => (rec.data[k] = '')); DB.assessments.push(rec); save(); track('assess:created'); simLog('info', 'Started ' + m.type + ' for ' + ptName(P(a.pid))); go('assess-edit', { id: rec.id }); };
        if (existing && m.type === 'OASIS') { modal({ title: 'An SOC assessment already exists', kind: 'warn', size: 'sm', body: '<p>Zenith rule: <b>do not create a second SOC OASIS</b> for the same admission. STOP and ask the DON.</p>', buttons: [{ label: 'Stop (recommended)', cls: 'btn-ok', click: () => simLog('good', 'Stopped: SOC OASIS already exists') }, { label: 'Create anyway (practice)', cls: 'btn-or', click: () => { simLog('override', 'Created a second SOC OASIS (practice)'); make(); } }] }); return; }
        make(); } }, { label: 'Cancel', cls: 'btn-del' }] });
  };
  if (isClinicalRole()) open(); else needApproval({ roles: [], what: 'Start an assessment (OASIS)', rule: 'The RN starts and completes the SOC OASIS. Office staff do not complete OASIS.', who: 'DON or the RN', ref: 'N2', go: open });
};
ROUTES['assess-edit'] = {
  render(c, p) {
    const src = byId(DB.assessments, p.id); if (!src) return notice('Assessment not found.', 'err');
    if (!c.a) { c.a = JSON.parse(JSON.stringify(src)); c.orig = JSON.stringify(c.a); c.tab = 'rec'; }
    const a = c.a, d = a.data, pt = P(a.pid), adm = admOf(a.pid); const ro = a.qa === 'Completed';
    const tabs = tabsHtml([{ k: 'rec', l: 'Clinical Record Items' }, { k: 'dx', l: 'Diagnoses' }, { k: 'fn', l: 'Functional Status' }, { k: 'an', l: 'Analysis' }], c.tab, 'asTab');
    let pane = '';
    if (c.tab === 'rec') pane = `<div class="row c2">${fg('(M0080) Discipline of person completing the assessment', sel(c, 'a.data.m0080', ['RN', 'PT', 'SLP/ST', 'OT'], { dis: ro }), { req: 1 })}${fg('(M0090) Date Assessment Completed', dp(c, 'a.data.m0090T', { dis: ro }), { req: 1 })}${fg('(M0100) Reason for Assessment', sel(c, 'a.data.m0100', M0100.map(([k, l]) => [k, k + ' ' + l]), { dis: ro }), { req: 1 })}${fg('Type', inp(c, 'a.type', { ro: 1 }))}</div>`;
    else if (c.tab === 'dx') pane = `<div class="row c2">${fg('(M1021) Primary Diagnosis code (ICD-10)', inp(c, 'a.data.dx1', { dis: ro, ph: 'Example I50.9' }), { req: 1 })}${fg('Description', inp(c, 'a.data.dxd', { dis: ro }))}</div><p class="small">Practice field. The physician's diagnosis on the Admission is the source.${adm ? ' Admission diagnoses: ' + esc(adm.diag.map(x => x.code).join(', ') || 'none') : ''}</p>`;
    else if (c.tab === 'fn') pane = `<p class="small">Choose what the patient can do on the day of the assessment.</p>${ADL_ITEMS.map(([k, l]) => fg(l, sel(c, 'a.data.' + k, ADL_OPTS, { dis: ro, blank: 'Select' }))).join('')}`;
    else { const h = asmtHipps(a), errs = asmtErrors(a); pane = `<div class="cardgrid"><div class="card"><h4>Functional score</h4><div class="n">${asmtScore(a)}</div></div><div class="card"><h4>Practice HIPPS code</h4><div class="n" style="font-size:26px">${esc(h.code)}</div><div class="small">Practice calculation. Not a real code.</div></div><div class="card"><h4>Practice payment estimate</h4><div class="n" style="font-size:26px">$${h.pay}</div><div class="small">Nothing is billed.</div></div></div><div class="box"><h4>Items still needed (${errs.length})</h4>${errs.length ? '<ul>' + errs.map(x => `<li>${esc(x)}</li>`).join('') + '</ul>' : '<p>Nothing missing. You can click Complete.</p>'}</div>`; }
    return `<div class="flex"><div class="grow">${pageHead('OASIS Assessment', a.type)}</div></div>${ro ? '<span class="vo">View only mode (approved)</span>' : ''}<h2 style="font:400 34px var(--font);color:#2b7bb9;margin:6px 0">${esc(ptName(pt))}</h2><div class="bar" style="padding:6px 14px"><span>DOB &nbsp; ${fmtD(pt.dob)}</span><span>PAN &nbsp; ${adm ? adm.pan : ''}</span><span>QA Status &nbsp; ${tagFor(a.qa)}</span></div>${simplified()}${tabs}<div class="tabpane">${pane}</div>
      <div class="flex mt" style="justify-content:flex-end">${ro ? '' : `<button class="btn btn-save" data-act="asSave">Save</button><button class="btn btn-ok" data-act="asComplete">Complete</button>`}<button class="btn btn-close" data-act="asClose">Close</button></div>`;
  },
};
ACT.asTab = el => { const c = ctxOf(el); c.tab = el.dataset.k; refresh(); };
function asWrite(c) { const src = byId(DB.assessments, c.a.id); const a = c.a; const d = a.data; const dt = parseD(d.m0090T); if (dt) { a.compDate = dt; d.m0090 = dt; } a.reason = asmtReasonText(a); if (a.type === 'OASIS') { const h = asmtHipps(a); a.hipps = h.code; a.payment = h.pay; } Object.assign(src, JSON.parse(JSON.stringify(a))); save(); c.orig = JSON.stringify(c.a); }
ACT.asSave = el => { const c = ctxOf(el); asWrite(c); track('assess:saved'); toast('Saved.', 'ok'); refresh(); };
ACT.asComplete = el => {
  const c = ctxOf(el); const errs = asmtErrors(c.a);
  if (errs.length) { c.tab = 'an'; refresh(); alertBox('The assessment is not complete', '<p>Fix these first:</p><ul>' + errs.map(x => `<li>${esc(x)}</li>`).join('') + '</ul>', 'warn'); return; }
  c.a.qa = 'Pending'; c.a.exportStatus = 'Not exported (simulator)'; asWrite(c); track('assess:completed'); simLog('info', 'Completed ' + c.a.type + ' (now Pending in QA Center)'); toast('Assessment completed. It now waits in the QA Center for the DON.', 'ok'); go('assess-pt', { aid: admOf(c.a.pid).id });
};
ACT.asClose = el => { const c = ctxOf(el); const out = () => { const adm = admOf(c.a.pid); go('assess-pt', { aid: adm.id }); }; if (JSON.stringify(c.a) !== c.orig) confirmBox('Close without saving?', '<p>You typed changes that are not saved. Close anyway?</p>', out, { yes: 'Close anyway', no: 'Stay', kind: 'warn' }); else out(); };

/* ---------------------------------------------------------------- Skilled Nursing Visit Notes */
const VISIT_TYPES = ['Skilled Nursing', 'SN and Supervisory', 'Supervisory', 'Discharge', 'Other', 'Telehealth Visit'];
const SN_CODES = ['BC1', 'BC2', 'BC3', 'BC4'];
function noteVisit(n) { return n.visitId ? byId(DB.visits, n.visitId) : null; }
function noteGps(n) { const v = noteVisit(n); if (v && v.evv && v.evv.inGps) return /patient's home/i.test(v.evv.inGps.where || ''); return !!n.gps; }
function ensureNote(v) {
  if (v.noteId && byId(DB.snNotes, v.noteId)) return byId(DB.snNotes, v.noteId);
  const n = { id: uid('SN'), pid: v.pid, visitId: v.id, date: v.start.slice(0, 10), cgId: v.cgId, status: 'In Use', nurseSigned: false, patSigned: false, gps: false, visitType: '', data: {}, signedAt: '', qa: 'In Use', start: (v.evv && v.evv.inAt) || '', end: (v.evv && v.evv.outAt) || '', sig: {} };
  DB.snNotes.push(n); v.noteId = n.id; save(); return n;
}
function snWarnings(n) {
  const out = []; const v = noteVisit(n); const e = (v && v.evv) || {};
  if (v && e.inAt && e.inGps && !/patient's home/i.test(e.inGps.where || '')) out.push({ tab: 'vital', tabLabel: 'Vital Signs', msg: 'Visit Information - The clock in location (GPS) does not match the patient address. Tell the Administrator.' });
  if (v && e.inAt && Math.abs(diffMin(e.inAt, v.start)) > 30) out.push({ tab: 'vital', tabLabel: 'Vital Signs', msg: 'Visit Information - Start Time is more than 30 minutes from the scheduled time.' });
  if (v && !e.outAt) out.push({ tab: 'vital', tabLabel: 'Vital Signs', msg: 'Visit Information - End Time is empty. Clock out on the phone before you leave the home.' });
  if (!((n.data || {}).narrative || '').trim()) out.push({ tab: 'summ', tabLabel: 'Interv. Summary', sec: 'narrative', msg: 'Interv. Summary - No visit narrative (summary of the visit) was written.' });
  return out;
}
function syncVisitFromNote(n) { const v = noteVisit(n); if (v && n.status === 'Completed' && v.evv && v.evv.outAt && v.status === 'N') { v.status = 'C'; save(); } }
ROUTES.sn = { render(c) { return admSearchPage(c, 'Skilled Nursing Visit Notes', 'sn-pt', { sub: 'Patient Admission Search' }); } };
ROUTES['sn-pt'] = {
  render(c, p) {
    const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return notice('Not found.', 'err');
    const tbl = DT(c, 'sn', () => ({ sort: 'date', dir: -1, firstLast: false, rowCls: r => (r.status !== 'Completed' ? 'draft' : ''),
      cols: [{ key: 'act', label: 'Action', sortable: false, blue: true, render: r => `<button class="btn btn-add btn-sm" data-act="snMenu" data-id="${r.id}" title="Action">${ic('dots')}</button>` },
        { key: 'date', label: 'Visit Date', blue: true, text: r => r.date, render: r => fmtD(r.date) }, { key: 'cg', label: 'Caregiver', text: r => stName(ST(r.cgId)), render: r => esc(stName(ST(r.cgId))) }, { key: 'status', label: 'Status', text: r => (r.status === 'Completed' ? 'Completed' : 'DRAFT'), render: r => (r.status === 'Completed' ? 'Completed' : '<b>DRAFT</b>') },
        { key: 'ns', label: 'Nurse Signed', text: r => (r.nurseSigned ? 'Yes' : 'No'), render: r => (r.nurseSigned ? 'Yes' : 'No') }, { key: 'ps', label: 'Patient Signed', text: r => (r.patSigned ? 'Yes' : 'No'), render: r => (r.patSigned ? 'Yes' : 'No') },
        { key: 'gps', label: 'GPS', text: r => (noteGps(r) ? 'Yes' : 'No'), render: r => (noteGps(r) ? 'Yes' : 'No') }, { key: 'note', label: 'SN Note', sortable: false, render: () => 'SN Note according to POC' }],
      rows: DB.snNotes.filter(n => n.pid === pt.id) }));
    return pageHead('Skilled Nursing Visit Note', 'Summary') + `<div class="bar"><h2>${ic('user')} ${esc(ptName(pt))}</h2><button class="btn btn-add" data-act="snAdd" data-aid="${a.id}">${ic('plus')} Add</button><button class="btn btn-back" data-act="snBack">${ic('back')} Back</button></div><p class="small">Nurses normally write the note in the phone app during the visit. Use + Add only when the note was not started in the app. A yellow DRAFT row means the visit is not finished.</p>${tbl}${gotoBtn()}${gotoPanel(c, a)}`;
  },
};
ACT.snBack = () => go('sn');
S2SRC.snVisits = { label: v => { const x = byId(DB.visits, v); return x ? fmtDT(x.start) + ' ' + stName(ST(x.cgId)) : ''; }, list: (q, c) => DB.visits.filter(v => v.pid === c.pid && !v.noteId && v.status !== 'A' && (SN_CODES.indexOf(v.billingCode) >= 0)).filter(v => (fmtDT(v.start) + ' ' + stName(ST(v.cgId))).toLowerCase().includes(q.toLowerCase())).map(v => ({ v: v.id, label: fmtDT(v.start) + ' to ' + fmtT(v.end) + '  ' + stName(ST(v.cgId)) + ' (' + bcDesc(v.billingCode) + ')' })) };
ACT.snAdd = el => {
  const a = byId(DB.admissions, el.dataset.aid);
  const open = () => { const m = ctxNew({ pid: a.pid, v: '' }); modal({ title: 'Add SN Note: choose the scheduled visit', ctx: m, size: 'sm', body: c => fg('Scheduled Visit', s2(c, 'v', 'snVisits', { ph: 'Select the visit' }), { req: 1 }) + '<p class="small">Only skilled nursing visits without a note are listed. If the visit you need is missing, ask the Scheduler.</p>', buttons: [{ label: 'OK', cls: 'btn-ok', click: () => { if (!m.v) { toast('Choose the visit this note belongs to.', 'err'); return false; } const v = byId(DB.visits, m.v); const n = ensureNote(v); track('sn:created'); go('snnote', { nid: n.id, mode: 'edit' }); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
  if (isClinicalRole()) open(); else needApproval({ roles: [], what: 'Create a skilled nursing note', rule: 'Clinicians write notes. Office staff do not write clinical notes.', who: 'DON or the nurse', ref: 'N3', go: open });
};
ACT.snMenu = el => {
  const id = el.dataset.id; const n = byId(DB.snNotes, id);
  popMenu(el, [{ label: 'Edit', ic: 'edit', run: () => snEditStart(n) }, { label: 'View', ic: 'eye', cls: 'view', run: () => modal({ title: 'SN Note', size: 'sm', body: '<p>The SN Note will open in view only mode.</p>', buttons: [{ label: 'OK', cls: 'btn-ok', click: () => { track('sn:view'); go('snnote', { nid: id, mode: 'view' }); } }] }) },
    { label: 'Print', ic: 'print', cls: 'print', run: () => printPreview('SN Note', snHtml(n)) }, { label: 'Download Document', ic: 'doc', cls: 'word', run: () => snDownload(n, 'Document') }, { label: 'Download PDF', ic: 'doc', cls: 'pdf', run: () => snDownload(n, 'PDF') },
    { label: 'Delete', ic: 'trash', danger: true, run: () => snDelete(n) }, { label: 'Attach to AloraMail', ic: 'clip', cls: 'clip', run: () => composeMail({ subject: 'SN Note: ' + ptName(P(n.pid)) + ' ' + fmtD(n.date), body: '(attached SN note, practice)' }) }]);
};
function snDownload(n, kind) { track('sn:download'); downloadText('SN_Note_' + P(n.pid).last + '_' + n.date + (kind === 'PDF' ? '_pdf' : '') + '.html', '<!doctype html><meta charset="utf-8"><title>SN Note</title><body style="font-family:Arial">' + snHtml(n) + '<p style="color:#a60">Practice document from the AloraPlus Training Simulator. Not a real record.</p></body>'); toast('Practice file downloaded.', 'sim'); }
function snDelete(n) { needApproval({ roles: ['Administrator'], what: 'Delete a note', rule: 'Do not choose Edit or Delete on a completed note. Never delete a clinical document without the Administrator\'s written authorization.', who: 'Administrator, in writing', ref: 'N3, R2', go: () => confirmBox('Delete this SN note?', '<p>The note is removed from the practice data.</p>', () => { DB.snNotes = DB.snNotes.filter(x => x.id !== n.id); const v = noteVisit(n); if (v) v.noteId = ''; save(); refresh(); }, { yes: 'Delete', no: 'Cancel' }) }); }
function snEditStart(n) {
  const go2 = () => { track('sn:edit'); go('snnote', { nid: n.id, mode: 'edit' }); };
  if (curRole() === 'Nurse' && !isMine(n.cgId)) { neverDo('Edit another nurse\'s note', 'Zenith rule: edit only your own notes. Never sign or change another nurse\'s note. Tell the DON.', 'Use View to learn from a note.'); return; }
  if (n.status === 'Completed') { needApproval({ roles: ['Administrator'], what: 'Edit a completed note', rule: 'Do not choose Edit or Delete on a completed note. Use View to learn.', who: 'DON or Administrator', ref: 'N3', go: go2 }); return; }
  if (!isClinicalRole()) { needApproval({ roles: [], what: 'Edit a clinical note', rule: 'Office staff do not write or change clinical notes.', who: 'DON', ref: 'N3', go: go2 }); return; }
  go2();
}
function snHtml(n) {
  const pt = P(n.pid), d = n.data || {}, v = noteVisit(n); const adm = admOf(n.pid);
  const secs = snSections().map(s => s.kind === 'vitals' ? `<tr><td><b>${esc(s.t)}</b></td><td>${d.vitals ? `Temp ${esc(d.vitals.temp || '')}, Pulse ${esc(d.vitals.pulse || '')}, Resp ${esc(d.vitals.resp || '')}, BP ${esc(d.vitals.bps || '')}/${esc(d.vitals.bpd || '')}, O2 ${esc(d.vitals.o2 || '')}%` : ''}</td></tr>` : `<tr><td><b>${esc(s.t)}</b></td><td>${esc((d[s.id] || []).join('; '))}</td></tr>`).join('');
  return `<h2>Skilled Nursing Visit Note according to POC (practice)</h2><table class="t"><tbody><tr><td>Patient</td><td>${esc(ptName(pt))}</td><td>DOB</td><td>${fmtD(pt.dob)}</td></tr><tr><td>Nurse</td><td>${esc(stName(ST(n.cgId)))}</td><td>Visit</td><td>${v ? fmtDT(v.start) : fmtD(n.date)}</td></tr><tr><td>Start</td><td>${fmtDT(n.start)}</td><td>End</td><td>${fmtDT(n.end)}</td></tr><tr><td>Type of Visit</td><td>${esc(n.visitType)}</td><td>Critical precautions</td><td>${esc(adm ? adm.other.precautions : '')}</td></tr></tbody></table><table class="t mt"><tbody>${secs}<tr><td><b>Narrative</b></td><td>${esc(d.narrative || '')}</td></tr></tbody></table><p>Nurse signature: ${n.sig && n.sig.nurse ? sigImg(n.sig.nurse, 40) + ' ' + fmtDT(n.sig.nurse.at) : (n.nurseSigned ? esc(n.sigName || 'signed') + ' ' + fmtDT(n.signedAt) : 'not signed')}</p><p>Patient signature: ${n.sig && n.sig.pat ? sigImg(n.sig.pat, 40) + ' ' + fmtDT(n.sig.pat.at) : (n.patSigned ? 'signed' : (n.patUnable ? 'unable to sign: ' + esc(n.patUnableWhy || '') : 'not signed'))}</p>`;
}

ROUTES.snnote = {
  render(c, p) {
    const src = byId(DB.snNotes, p.nid); if (!src) return notice('Note not found.', 'err');
    if (!c.n) { c.n = JSON.parse(JSON.stringify(src)); c.n.data = c.n.data || {}; c.n.sig = c.n.sig || {}; c.orig = JSON.stringify(c.n); c.tab = p.tab || 'vital'; c.view = p.mode === 'view'; }
    const n = c.n, pt = P(n.pid), adm = admOf(n.pid), v = noteVisit(n); const view = c.view;
    const tabs = tabsHtml(SN_TABS.map(t => ({ k: t.k, l: t.l })), c.tab, 'snTab');
    const tab = SN_TABS.find(t => t.k === c.tab);
    let pane = '';
    if (c.tab === 'vital') pane = `<div class="box"><h4>Visit Information</h4><div class="row c3">${fg('Nurse', `<input type="text" value="${esc(stName(ST(n.cgId)))}" readonly>`)}${fg('Scheduled Visit', `<input type="text" value="${esc(v ? fmtDT(v.start) + ' to ' + fmtT(v.end) : '')}" readonly>`)}${fg('Start Time', `<input type="text" value="${esc(fmtDT(n.start))}" readonly>`)}${fg('End Time', `<input type="text" value="${esc(fmtDT(n.end))}" readonly>`)}</div><div class="fg" id="sec-type"><label>Type of Visit</label><div class="chkbox">${VISIT_TYPES.map(t => radio(c, 'n.visitType', t, t, { dis: view })).join('')}</div></div></div>`;
    pane += tab.secs.map(s => snSectionHtml(c, s, view)).join('');
    if (c.tab === 'summ') pane += `<div class="box" id="sec-narrative"><h4>Narrative (summary of the visit)</h4>${txt(c, 'n.data.narrative', { rows: 4, dis: view })}</div>`;
    if (c.tab === 'qa') pane = snQaPane(c, view);
    const crit = adm ? adm.other.precautions : '';
    return `<div class="flex"><div class="grow"><h3 style="font:400 22px var(--font);color:#555">SN Note according to POC</h3></div>${view ? '<span class="vo">View only mode</span>' : ''}</div>
      <h2 style="font:400 38px var(--font);color:#2b7bb9;margin:6px 0">${esc(ptName(pt))}</h2><div class="bar" style="flex-wrap:wrap;gap:20px;padding:6px 14px"><span>PAN &nbsp; <b>${adm ? adm.pan : ''}</b></span><span>Admit Date &nbsp; <b>${adm ? fmtD(adm.admit) : ''}</b></span><span>Date of Birth &nbsp; <b>${fmtD(pt.dob)}</b></span><span>DNR &nbsp; <b>${adm && adm.dnr ? 'Yes' : 'No'}</b></span><span style="flex-basis:100%">Critical Precautions &nbsp; <b style="color:#c0392b">${esc(crit || 'None listed')}</b></span></div>
      ${tabs}<div class="tabpane">${pane}</div><div class="flex mt" style="justify-content:flex-end">${view ? '' : `<button class="btn btn-save" data-act="snSave">Save</button>`}<button class="btn btn-close" data-act="snClose">Close</button></div>`;
  },
};
function snSectionHtml(c, s, view) {
  const d = c.n.data;
  if (s.kind === 'vitals') return `<div class="box" id="sec-vitals"><h4>${esc(s.t)}</h4><div class="row c3">${[['temp', 'Temperature (F)'], ['pulse', 'Pulse (per minute)'], ['resp', 'Respirations (per minute)'], ['bps', 'Blood pressure, top number'], ['bpd', 'Blood pressure, bottom number'], ['o2', 'Oxygen saturation (%)']].map(([k, l]) => fg(l, inp(c, 'n.data.vitals.' + k, { dis: view }))).join('')}</div></div>`;
  return `<div class="box" id="sec-${s.id}"><h4>${esc(s.t)}</h4><div class="chkbox">${s.opts.map(o => `<label class="chk"><input type="checkbox" data-act="snOpt" data-sec="${s.id}" data-opt="${esc(o)}"${(d[s.id] || []).indexOf(o) >= 0 ? ' checked' : ''}${view ? ' disabled' : ''}> ${esc(o)}</label>`).join('')}</div></div>`;
}
ACT.snTab = el => { const c = ctxOf(el); c.tab = el.dataset.k; track('sn:tab:' + c.tab); refresh(); };
ACT.snOpt = el => { const c = ctxOf(el); const sec = el.dataset.sec, o = el.dataset.opt; const a = (c.n.data[sec] = c.n.data[sec] || []); const i = a.indexOf(o); if (el.checked && i < 0) a.push(o); if (!el.checked && i >= 0) a.splice(i, 1); };
function snValidation(c) { const n = c.n; return { errs: snErrors(n), warns: snWarnings(n) }; }
function snQaPane(c, view) {
  const n = c.n; const { errs, warns } = snValidation(c);
  const row = (x, cls) => `<tr class="${cls}"><td>${esc(x.tabLabel)}</td><td>${esc(x.msg)}</td><td>${view ? '' : `<button class="ico-btn ico-green" title="Go to the field" data-act="snJump" data-tab="${x.tab}" data-sec="${x.sec || ''}">${ic('edit')}</button>`}</td></tr>`;
  const sg = (who, key, label) => { const s = n.sig && n.sig[key]; return `<div class="box"><h4>${label}</h4><div class="flex" style="justify-content:space-between;align-items:flex-end"><div>${s ? sigImg(s, 56) : (n[key === 'nurse' ? 'nurseSigned' : 'patSigned'] ? '<i>(signature hidden)</i>' : '<span class="small">No signature yet</span>')}${view || (key === 'nurse' ? n.nurseSigned : n.patSigned) ? '' : `<div class="mt"><button class="btn btn-add" data-act="${key === 'nurse' ? 'snSignN' : 'snSignP'}">${ic('plus')} Add Signature</button></div>`}</div><div>Signed Date &nbsp; <b>${s ? fmtDT(s.at) : (key === 'nurse' && n.nurseSigned ? fmtDT(n.signedAt) : '')}</b></div></div>${key === 'pat' && !view && !n.patSigned ? `<div class="mt">${chk(c, 'n.patUnable', 'Patient unable to sign', { rr: 1 })}${n.patUnable ? fg('Reason', inp(c, 'n.patUnableWhy')) : ''}</div>` : ''}</div>`; };
  return `<div class="box"><h4>Document Validation</h4><div class="flex"><b>Total Errors: <span style="color:${errs.length ? '#c0392b' : '#3c763d'}">${errs.length}</span></b><b>Total Warnings: <span style="color:#b07a00">${warns.length}</span></b><span class="grow"></span><button class="btn btn-blue btn-sm" data-act="snPrintVal">${ic('print')} Print Validations</button></div>
    <table class="t mt"><thead><tr><th>Tab</th><th>Message</th><th></th></tr></thead><tbody>${errs.map(x => row(x, 'er')).join('')}${warns.map(x => row(x, 'draft')).join('') || (errs.length ? '' : '<tr><td colspan="3" class="none">No messages. The note is ready to sign.</td></tr>')}</tbody></table><p class="small">Errors block signing. Warnings must be reviewed, not ignored. Click the green pencil to jump to the field.</p></div>
    ${sg('nurse', 'nurse', 'Nurse Signature')}${sg('pat', 'pat', 'Patient Signature')}
    ${view ? '' : `<div class="note sim"><b>Simulator shortcut:</b> <a data-act="snFill">fill every tab with sample answers</a> (so you can practice signing without typing 20 sections).</div>`}`;
}
ACT.snFill = el => { const c = ctxOf(el); const f = snFullData(); c.n.data = Object.assign(c.n.data, f); if (!c.n.visitType) c.n.visitType = 'Skilled Nursing'; track('sn:fill'); refresh(); toast('Sample answers entered on every tab.', 'sim'); };
ACT.snJump = el => { const c = ctxOf(el); c.tab = el.dataset.tab; track('sn:jump'); refresh(); const t = el.dataset.sec ? document.getElementById('sec-' + el.dataset.sec) : null; if (t) { t.scrollIntoView({ block: 'center' }); t.style.outline = '3px solid #3fae49'; setTimeout(() => (t.style.outline = ''), 1800); } };
ACT.snPrintVal = el => { const c = ctxOf(el); const { errs, warns } = snValidation(c); track('sn:printval'); printPreview('Document Validation', `<h2>Document Validation (practice)</h2><p>Total Errors: ${errs.length} &nbsp; Total Warnings: ${warns.length}</p><table class="t"><tbody>${errs.concat(warns).map(x => `<tr><td>${esc(x.tabLabel)}</td><td>${esc(x.msg)}</td></tr>`).join('') || '<tr><td>No messages</td></tr>'}</tbody></table>`); };
function snPersist(c) { const src = byId(DB.snNotes, c.n.id); Object.assign(src, JSON.parse(JSON.stringify(c.n))); src.gps = noteGps(src); save(); c.orig = JSON.stringify(c.n); }
ACT.snSave = el => { const c = ctxOf(el); snPersist(c); track('sn:saved'); toast('Saved.', 'ok'); refresh(); };
function snSignGuard(c, who) {
  if (who === 'nurse') {
    if (!isMine(c.n.cgId)) { neverDo('Sign a note that is not yours', 'Zenith rule: never sign another nurse\'s note. Only ' + stName(ST(c.n.cgId)) + ' signs this one. (Practice as Nurse and sign in as that nurse.)', 'N3: Never sign another nurse\'s note.'); return false; }
    const { errs } = snValidation(c); if (errs.length) { alertBox('Cannot sign yet', `<p>The note still has <b>${errs.length} error${errs.length === 1 ? '' : 's'}</b>. Errors block signing. Open the QA/Signature list and click each green pencil.</p>`, 'warn'); track('sn:signblocked'); simLog('good', 'Signing was blocked until errors were fixed'); return false; }
  }
  return true;
}
function snAfterSign(c) {
  const n = c.n; n.sigName = (n.sig.nurse || {}).name || n.sigName;
  if (n.nurseSigned && (n.patSigned || n.patUnable)) { n.status = 'Completed'; n.qa = n.qa === 'Completed' ? 'Completed' : 'Pending'; }
  snPersist(c); syncVisitFromNote(byId(DB.snNotes, n.id)); if (n.status === 'Completed') { track('sn:completed'); simLog('info', 'SN note completed and signed (QA Pending)'); }
}
ACT.snSignN = el => { const c = ctxOf(el); if (!snSignGuard(c, 'nurse')) return; sigPad('Nurse Signature', stName(ST(c.n.cgId)), s => { c.n.sig.nurse = s; c.n.nurseSigned = true; c.n.signedAt = s.at; track('sn:nursesigned'); snAfterSign(c); toast('Signed.', 'ok'); refresh(); }); };
ACT.snSignP = el => { const c = ctxOf(el); sigPad('Patient Signature', ptName(P(c.n.pid)), s => { c.n.sig.pat = s; c.n.patSigned = true; track('sn:patsigned'); snAfterSign(c); toast('Patient signature saved.', 'ok'); refresh(); }, { hint: 'Hand the device to the patient. The patient signs in the box. Patient: ' }); };
ACT.snClose = el => { const c = ctxOf(el); const out = () => go('sn-pt', { aid: admOf(c.n.pid).id }); if (!c.view && JSON.stringify(c.n) !== c.orig) confirmBox('Close without saving?', '<p>You typed changes that are not saved. Close anyway?</p>', out, { yes: 'Close anyway', no: 'Stay', kind: 'warn' }); else out(); };

/* ---------------------------------------------------------------- Aide Documents (plan of care and aide visit notes) */
ROUTES.aide = { render(c) { return admSearchPage(c, 'Aide Documents', 'aide-pt', { sub: 'Patient Admission Search' }); } };
function aidePoc(pid) { return DB.aideDocs.filter(x => x.pid === pid && x.kind === 'poc' && x.status !== 'Void').sort((a, b) => (a.from < b.from ? 1 : -1))[0] || null; }
ROUTES['aide-pt'] = {
  render(c, p) {
    const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return notice('Not found.', 'err');
    const tbl = DT(c, 'aide', () => ({ sort: 'from', dir: -1, firstLast: false,
      cols: [{ key: 'act', label: 'Action', sortable: false, blue: true, render: r => rowIcons([{ ic: 'edit', t: 'Open', act: 'aideOpen', data: { id: r.id } }, { ic: 'trash', t: 'Delete', act: 'aideDel', data: { id: r.id }, cls: 'del' }]) },
        { key: 'doc', label: 'Document', text: r => (r.kind === 'poc' ? 'Aide Plan of Care' : 'Aide Note'), render: r => (r.kind === 'poc' ? 'Aide Plan of Care' : 'Aide Note') }, { key: 'svc', label: 'Aide Service Title', text: r => (r.tasks || []).join(', '), render: r => esc((r.tasks || []).join(', ')) },
        { key: 'cg', label: 'Caregiver', text: r => stName(ST(r.cgId)), render: r => esc(stName(ST(r.cgId))) }, { key: 'from', label: 'From Date', blue: true, text: r => r.from, render: r => fmtD(r.from) }, { key: 'to', label: 'Through Date', text: r => r.to || '', render: r => fmtD(r.to) }, { key: 'status', label: 'Status', render: r => tagFor(r.status) }],
      rows: DB.aideDocs.filter(x => x.pid === pt.id) }));
    return pageHead('Aide Documents', 'Summary') + `<div class="bar"><h2>${ic('user')} ${esc(ptName(pt))}</h2><button class="btn btn-add" data-act="aideAdd" data-aid="${a.id}">${ic('plus')} Add</button><button class="btn btn-back" data-act="aideBack">${ic('back')} Back</button><button class="btn btn-or" data-act="aideDates" data-pid="${pt.id}">${ic('doc')} Edit From/To Date</button></div><p class="small">Most aides document in the phone app. Use this screen when the office or the RN asks.</p>${tbl}${gotoBtn()}${gotoPanel(c, a)}`;
  },
};
ACT.aideBack = () => go('aide');
ACT.aideAdd = el => { const aid = el.dataset.aid; popMenu(el, [{ label: 'Plan of Care', ic: 'doc', run: () => aidePocStart(byId(DB.admissions, aid).pid, null) }, { label: 'Note', ic: 'edit', run: () => aideNoteStart(byId(DB.admissions, aid).pid, null) }]); };
ACT.aideOpen = el => { const r = byId(DB.aideDocs, el.dataset.id); if (r.kind === 'poc') aidePocStart(r.pid, r.id); else aideNoteStart(r.pid, r.id); };
ACT.aideDel = el => needApproval({ roles: ['Administrator'], what: 'Delete an aide document', rule: 'Never delete a clinical document without written Administrator authorization.', who: 'Administrator', ref: 'R2', go: () => { DB.aideDocs = DB.aideDocs.filter(x => x.id !== el.dataset.id); save(); refresh(); } });
ACT.aideDates = el => needApproval({ roles: ['Nurse', 'DON'], what: 'Edit the aide plan of care From/To dates', rule: 'Only the RN or the Administrator changes the aide plan of care dates.', who: 'RN or Administrator', ref: 'AI2', go: () => { const list = DB.aideDocs.filter(x => x.pid === el.dataset.pid && x.kind === 'poc'); const m = ctxNew({ rows: list.map(x => ({ id: x.id, from: fmtD(x.from), to: fmtD(x.to) })) }); modal({ title: 'Edit From/To Date', ctx: m, size: 'sm', body: c => c.rows.map((r, i) => `<div class="row c2">${fg('From', dp(c, 'rows.' + i + '.from'))}${fg('Through', dp(c, 'rows.' + i + '.to'))}</div>`).join('') || '<p>No plan of care yet.</p>', buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { m.rows.forEach(r => { const x = byId(DB.aideDocs, r.id); x.from = parseD(r.from) || x.from; x.to = parseD(r.to) || x.to; }); save(); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); } });
function aidePocStart(pid, id) {
  const ex = id ? byId(DB.aideDocs, id) : null;
  const open = () => {
    const adm = admOf(pid); const m = ctxNew({ r: ex ? { cgId: ex.cgId, from: fmtD(ex.from), to: fmtD(ex.to), freq: ex.freq, tasks: (ex.tasks || []).slice(), notes: ex.notes || '' } : { cgId: '', from: fmtD(adm.admit), to: fmtD(addDays(adm.admit, 59)), freq: '', tasks: [], notes: '' } });
    modal({ title: 'Aide Plan of Care', ctx: m, size: 'lg', body: c => `<div class="row c2">${fg('Aide (caregiver)', s2(c, 'r.cgId', 'caregivers', { ph: 'Select aide' }), { req: 1 })}${fg('Visit frequency (example 3 times a week)', inp(c, 'r.freq'))}${fg('From', dp(c, 'r.from'), { req: 1 })}${fg('Through', dp(c, 'r.to'), { req: 1 })}</div><div class="box"><h4>Aide Service Titles (tasks)</h4><div class="chkbox">${DB.lists.aideTitles.map(t => `<label class="chk"><input type="checkbox" data-act="pocTask" data-t="${esc(t)}"${c.r.tasks.indexOf(t) >= 0 ? ' checked' : ''}> ${esc(t)}</label>`).join('')}</div></div>${fg('Instructions from the RN', txt(c, 'r.notes', { rows: 3 }))}`,
      buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { const f = parseD(m.r.from), t = parseD(m.r.to); if (!m.r.cgId || !f || !t || !m.r.tasks.length) { toast('Aide, dates and at least one task are required.', 'err'); return false; }
        const rec = { id: ex ? ex.id : uid('AD'), pid, kind: 'poc', title: 'Aide Plan of Care', cgId: m.r.cgId, from: f, to: t, status: 'Completed', tasks: m.r.tasks, freq: m.r.freq, notes: m.r.notes, by: DB.session.userId }; if (ex) Object.assign(ex, rec); else DB.aideDocs.push(rec); save(); track('aide:poc'); simLog('info', 'Saved aide plan of care for ' + ptName(P(pid))); refresh(); toast('Saved.', 'ok'); } }, { label: 'Cancel', cls: 'btn-del' }] });
  };
  if (roleIs('Nurse', 'DON')) open(); else needApproval({ roles: [], what: 'Create the Aide Plan of Care', rule: 'Aides do not create the Aide Plan of Care. The RN does.', who: 'The RN', ref: 'AI2', go: open });
}
ACT.pocTask = el => { const m = ctxOf(el); const t = el.dataset.t; const i = m.r.tasks.indexOf(t); if (el.checked && i < 0) m.r.tasks.push(t); if (!el.checked && i >= 0) m.r.tasks.splice(i, 1); };
function aideNoteStart(pid, id) {
  const poc = aidePoc(pid); const ex = id ? byId(DB.aideDocs, id) : null;
  const visits = DB.visits.filter(v => v.pid === pid && v.billingCode === 'BC5' && v.status !== 'A' && (!DB.aideDocs.some(d => d.kind === 'note' && d.visitId === v.id) || (ex && ex.visitId === v.id)));
  S2SRC.aideVisits = { label: v => { const x = byId(DB.visits, v); return x ? fmtDT(x.start) + ' ' + stName(ST(x.cgId)) : ''; }, list: (q, c) => visits.map(v => ({ v: v.id, label: fmtDT(v.start) + ' to ' + fmtT(v.end) + '  ' + stName(ST(v.cgId)) })) };
  const open = () => {
    const done = ex ? ex.done || {} : {}; const m = ctxNew({ n: ex ? { visitId: ex.visitId, done: JSON.parse(JSON.stringify(done)), why: ex.why || {}, narrative: ex.narrative || '', sig: ex.sig || null, pat: ex.pat || null } : { visitId: '', done: {}, why: {}, narrative: '', sig: null, pat: null } });
    modal({ title: 'Aide Note', ctx: m, size: 'lg', body: c => `${poc ? '' : notice('There is no Aide Plan of Care for this patient. Stop and call the RN. Do not guess the tasks.', 'warn')}${fg('Visit', s2(c, 'n.visitId', 'aideVisits', { ph: 'Select the visit', rr: 1 }), { req: 1 })}<div class="box"><h4>Tasks from the plan of care${poc ? ' (' + fmtD(poc.from) + ' to ' + fmtD(poc.to) + ')' : ''}</h4><table class="t"><thead><tr><th>Task</th><th>Done?</th><th>If not done, why</th></tr></thead><tbody>${(poc ? poc.tasks : []).map((t, i) => `<tr><td>${esc(t)}</td><td>${radio(c, 'n.done.' + i, 'Done', 'Done', { rr: 1 })} ${radio(c, 'n.done.' + i, 'Not done', 'Not done', { rr: 1 })}</td><td>${c.n.done[i] === 'Not done' ? inp(c, 'n.why.' + i, { ph: 'Required' }) : ''}</td></tr>`).join('') || '<tr><td colspan="3" class="none">No tasks</td></tr>'}</tbody></table></div>${fg('Narrative (use the patient\'s own words for complaints)', txt(c, 'n.narrative', { rows: 3 }))}
      <div class="row c2"><div class="box"><h4>Aide signature</h4>${c.n.sig ? sigImg(c.n.sig) : '<span class="small">No signature yet</span>'}<div class="mt"><button class="btn btn-add btn-sm" data-act="aideSign">${ic('plus')} Add Signature</button></div></div><div class="box"><h4>Patient signature (if able)</h4>${c.n.pat ? sigImg(c.n.pat) : '<span class="small">None</span>'}<div class="mt"><button class="btn btn-add btn-sm" data-act="aideSignP">${ic('plus')} Add Signature</button></div></div></div>`,
      buttons: [{ label: 'Save Draft', cls: 'btn-save', click: () => aideNoteSave(pid, ex, m, poc, false) }, { label: 'Complete', cls: 'btn-ok', click: () => aideNoteSave(pid, ex, m, poc, true) }, { label: 'Close', cls: 'btn-close' }] });
  };
  open();
}
function aideNoteSave(pid, ex, m, poc, complete) {
  const n = m.n; const v = n.visitId ? byId(DB.visits, n.visitId) : null; if (!v) { toast('Choose the visit.', 'err'); return false; }
  if (complete) {
    if (!isMine(v.cgId)) { neverDo('Complete a note for another aide', 'Zenith rule: never sign for another person. Only ' + stName(ST(v.cgId)) + ' completes this note.', 'AI2'); return false; }
    const tasks = poc ? poc.tasks : []; for (let i = 0; i < tasks.length; i++) { if (!n.done[i]) { toast('Mark every task Done or Not done: ' + tasks[i], 'err'); return false; } if (n.done[i] === 'Not done' && !String(n.why[i] || '').trim()) { toast('Say why "' + tasks[i] + '" was not done.', 'err'); return false; } }
    if (!n.sig) { toast('The aide signature is required to complete the note.', 'err'); return false; }
  }
  const rec = { id: ex ? ex.id : uid('AD'), pid, kind: 'note', title: 'Aide Note', visitId: n.visitId, cgId: v.cgId, from: v.start.slice(0, 10), to: v.start.slice(0, 10), status: complete ? 'Completed' : 'In Use', tasks: poc ? poc.tasks.filter((t, i) => n.done[i] === 'Done') : [], done: n.done, why: n.why, narrative: n.narrative, sig: n.sig, pat: n.pat, by: DB.session.userId };
  if (ex) Object.assign(ex, rec); else DB.aideDocs.push(rec);
  if (complete && v.evv && v.evv.outAt && v.status === 'N') v.status = 'C';
  save(); track(complete ? 'aide:note-completed' : 'aide:note-draft'); simLog('info', (complete ? 'Completed' : 'Saved a draft of') + ' an aide note'); refresh(); toast(complete ? 'Aide note completed.' : 'Draft saved.', 'ok');
}
ACT.aideSign = el => { const m = ctxOf(el); const v = m.n.visitId ? byId(DB.visits, m.n.visitId) : null; if (!v) { toast('Choose the visit first.', 'err'); return; } if (!isMine(v.cgId)) { neverDo('Sign for another aide', 'Zenith rule: never sign for another person.', 'AI2'); return; } sigPad('Aide Signature', stName(ST(v.cgId)), s => { m.n.sig = s; m._modal.rerender(); }, { z: 1250 }); };
ACT.aideSignP = el => { const m = ctxOf(el); const v = m.n.visitId ? byId(DB.visits, m.n.visitId) : null; if (!v) { toast('Choose the visit first.', 'err'); return; } sigPad('Patient Signature', ptName(P(v.pid)), s => { m.n.pat = s; m._modal.rerender(); }, { z: 1250 }); };

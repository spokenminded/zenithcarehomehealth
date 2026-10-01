'use strict';
/* =====================================================================================================
   Patient screens: Demographics and Referrals, Admission, Patient Chart, Communication Log, GoTo panel
   ===================================================================================================== */
const SEXES = ['Male', 'Female', 'Unknown'];
const ETHNICITIES = ['American Indian or Alaska Native', 'Asian', 'Black or African-American', 'Hispanic or Latino', 'Native Hawaiian or Pacific Islander', 'White', 'Other', 'Unknown'];
const LANGS = ['ENGLISH', 'SPANISH', 'HAITIAN CREOLE', 'PORTUGUESE', 'OTHER'];
const STATES = ['FL', 'GA', 'AL', 'NY', 'NJ', 'TX', 'CA'];

/* ---------------------------------------------------------------- select box sources */
S2SRC.patients = { cols: ['Patient', 'Admit. Date', 'Disch. Date', 'Payer', 'Ins. From', 'Ins. To', 'PAN', 'DOB'],
  label: (v) => ptName(P(v)),
  list: (q) => { q = q.toLowerCase(); return DB.admissions.filter(a => !a.draft).map(a => ({ a, p: P(a.pid) })).filter(x => x.p && (ptName(x.p) + ' ' + x.p.mrn).toLowerCase().includes(q)).map(({ a, p }) => { const i = a.ins[0] || {}; return { v: p.id, aid: a.id, label: ptName(p), cells: [ptName(p), fmtD(a.admit), fmtD(a.dischDate), payerName(i.payer), fmtD(i.from), fmtD(i.to), a.pan, fmtD(p.dob)] }; }); } };
S2SRC.patientsAll = { label: v => ptName(P(v)), list: q => DB.patients.filter(p => !p.draft && (ptName(p) + ' ' + fmtD(p.dob)).toLowerCase().includes(q.toLowerCase())).map(p => ({ v: p.id, label: ptName(p) + '  (DOB ' + fmtD(p.dob) + ')' })) };
S2SRC.physicians = { label: v => (byId(DB.lists.physicians, v) || {}).name || '', list: q => DB.lists.physicians.filter(x => x.name.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x.id, label: x.name })) };
S2SRC.refSources = { label: v => v, list: q => DB.lists.referralSources.filter(x => x.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x, label: x })) };
S2SRC.admSources = { label: v => v, list: q => DB.lists.admissionSources.filter(x => x.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x, label: x })) };
S2SRC.offices = { label: v => v, list: q => DB.lists.offices.filter(x => x.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x, label: x })) };
S2SRC.staff = { label: v => stName(ST(v)), list: q => DB.staff.filter(s => s.active && (stName(s) + ' ' + s.disc).toLowerCase().includes(q.toLowerCase())).map(s => ({ v: s.id, label: stName(s) + ' (' + s.disc + ')' })) };
S2SRC.caregivers = { label: v => stName(ST(v)), list: q => DB.staff.filter(s => s.active && s.disc !== 'OFFICE' && (stName(s) + ' ' + s.disc).toLowerCase().includes(q.toLowerCase())).map(s => ({ v: s.id, label: stName(s) + ' (' + s.disc + ')' })) };
S2SRC.payers = { label: v => payerName(v), list: q => DB.lists.payers.filter(x => x.name.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x.id, label: x.name })) };
S2SRC.ptFolders = { label: v => v, head: 'Folder', list: q => DB.lists.ptFolders.filter(x => x.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x, label: x })) };
S2SRC.stFolders = { label: v => v, head: 'Folder', list: q => DB.lists.staffFolders.filter(x => x.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x, label: x })) };
S2SRC.billingCodes = { label: v => { const b = byId(DB.lists.billingCodes, v); return b ? b.code + ' - ' + b.desc : ''; }, list: (q, c) => DB.lists.billingCodes.filter(x => (x.code + ' ' + x.desc).toLowerCase().includes(q.toLowerCase()) && (!c || !c.d || !c.d.discOnly || true)).map(x => ({ v: x.id, label: x.code + ' - ' + x.desc })) };
S2SRC.disciplines = { label: v => v, list: q => DISCIPLINES.filter(x => x.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x, label: x })) };
S2SRC.evvReasons = { label: v => v, list: q => DB.lists.evvReasons.filter(x => x.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x, label: x })) };
S2SRC.missedReasons = { label: v => v, list: q => DB.lists.missedReasons.filter(x => x.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x, label: x })) };
S2SRC.certPeriods = { label: v => v, list: (q, c) => (c.cps || []).map(x => ({ v: x.k, label: x.l })) };
S2SRC.users = { label: v => (byId(DB.users, v) || {}).name || '', list: q => DB.users.filter(u => u.active && u.name.toLowerCase().includes(q.toLowerCase())).map(u => ({ v: u.id, label: u.name + ' (' + ROLE_LABEL[u.role] + ')' })) };
function payerName(id) { const p = byId(DB.lists.payers, id); return p ? p.name : ''; }
function bcDesc(id) { const b = byId(DB.lists.billingCodes, id); return b ? b.desc : ''; }
function physName(id) { const p = byId(DB.lists.physicians, id); return p ? p.name : ''; }

/* ---------------------------------------------------------------- shared: patient admission search list (used by many modules) */
function admRows(c) {
  return DB.admissions.filter(a => !a.draft && (c.inactive || (!a.inactive && a.status === 'Admitted'))).map(a => ({ a, p: P(a.pid) })).filter(x => x.p);
}
function admSearchPage(c, title, nextRoute, opts) {
  opts = opts || {};
  const tbl = DT(c, 'adm', () => ({
    filterBtn: true, sort: 'name',
    cols: [{ key: 'sel', label: 'Select', sortable: false, blue: true, render: r => rowIcons([{ ic: 'edit', t: 'Select', act: 'admPick', data: { aid: r.a.id, to: nextRoute } }]) },
      { key: 'name', label: 'Patient Name', blue: true, text: r => ptName(r.p), render: r => esc(ptName(r.p)) }, { key: 'pan', label: 'PAN #', text: r => r.a.pan, render: r => esc(r.a.pan) },
      { key: 'admit', label: 'Admit Date', text: r => r.a.admit, render: r => fmtD(r.a.admit) }, { key: 'disch', label: 'Discharge Date', text: r => r.a.dischDate || '', render: r => fmtD(r.a.dischDate) },
      { key: 'dob', label: 'DOB', text: r => r.p.dob, render: r => fmtD(r.p.dob) }, { key: 'office', label: 'Office Name', text: r => r.a.office, render: r => esc(r.a.office) }],
    rows: admRows(c), searchText: r => ptName(r.p) + ' ' + r.a.pan + ' ' + r.p.mrn,
  }));
  return pageHead(title, opts.sub || 'Patient Admission Search') + (opts.pre || '') + tbl + `<label class="chk mt"><input type="checkbox" ${battr(c, 'inactive')} data-rr="1"${c.inactive ? ' checked' : ''}> Include Inactivated Admissions</label>`;
}
ACT.admPick = el => { track('admpick:' + el.dataset.to); go(el.dataset.to, { aid: el.dataset.aid }); };

/* ---------------------------------------------------------------- patient list and record */
ROUTES.patients = {
  render(c, p) {
    if (p.add && !c._added) { c._added = true; setTimeout(() => ACT.ptAdd(), 0); }
    const tbl = DT(c, 'pt', () => ({
      filterBtn: true, sort: 'last',
      cols: [{ key: 'sel', label: 'Select', sortable: false, blue: true, render: r => rowIcons([{ ic: 'edit', t: 'Select', act: 'ptOpen', data: { id: r.id } }]) }, { key: 'last', label: 'Last Name', blue: true, text: r => r.last, render: r => esc(r.last) },
        { key: 'first', label: 'First Name', render: r => esc(r.first) }, { key: 'mi', label: 'Middle Name', render: r => esc(r.mi) }, { key: 'dob', label: 'DOB', text: r => r.dob, render: r => fmtD(r.dob) }],
      rows: DB.patients.filter(x => !x.draft), searchText: r => r.last + ' ' + r.first + ' ' + r.mrn,
    }));
    return pageHead('Patient Demographics', 'Patient Search') + `<div class="bar"><h2>${ic('user')} Patient Demographics</h2><button class="btn btn-add" data-act="ptAdd">${ic('plus')} Add</button></div>
      <p class="small">Type in the Search box, then click the blue filter button. Pressing Enter alone does not filter the list.</p>${tbl}`;
  },
};
ACT.ptOpen = el => { track('demo:open'); go('patient', { id: el.dataset.id }); };
ACT.ptAdd = () => needApproval({ roles: ['Administrator'], what: 'Create a new patient (+ Add)', rule: 'Search twice first. Add a patient only when nothing matches AND the Administrator approved the admission.', who: 'Administrator', ref: 'S3, R2', go: () => { track('pt:addclick'); go('patient', { id: 'NEW', new: 1 }); } });

function blankPatient() { return { id: 'NEW', last: '', first: '', mi: '', suffix: '', dob: '', sex: '', ethnicity: '', addr1: '', addr2: '', city: '', state: 'FL', zip: '', instructions: '', mrn: '', ssn: '', medicare: '', medicaid: '', email: '', phones: { home: '', mobile: '', other: '' }, em: { name: '', phone1: '', phone2: '', email: '' }, lang: 'ENGLISH', comments: '', altLocs: [], contacts: [], lat: 26.2, lng: -80.25 }; }
function ptToForm(p) { const d = JSON.parse(JSON.stringify(p)); d.dobT = fmtD(p.dob); return d; }
ROUTES.patient = {
  render(c, p) {
    const isNew = p.id === 'NEW';
    if (!c.d) { const src = isNew ? blankPatient() : P(p.id); if (!src) return pageHead('Patient Demographics', '') + notice('That patient was not found.', 'err'); c.d = ptToForm(src); c.orig = JSON.stringify(c.d); c.tab = p.tab || 'demo'; }
    const d = c.d;
    const tabs = tabsHtml([{ k: 'demo', l: 'Patient Demographics' }, { k: 'ref', l: 'Referrals', off: isNew }], c.tab, 'ptTab');
    return pageHead('Patient Demographics', c.tab === 'ref' ? 'Referrals' : '') + tabs + `<div class="tabpane">${c.tab === 'ref' ? refTab(c, d) : demoTab(c, d, isNew)}</div>`;
  },
};
ACT.ptTab = el => { const c = ctxOf(el); if (el.classList.contains('off')) { toast('Alora opens the other tabs after the record is saved.', 'sim'); return; } c.tab = el.dataset.k; refresh(); };
function demoTab(c, d, isNew) {
  const dup = c.dupNote ? notice(c.dupNote, 'warn') : '';
  return `${dup}<div class="sec">Patient Demographics</div>
  <div class="flex" style="align-items:flex-start;gap:24px"><div class="grow"><div class="sec sm">Patient Name</div><div class="row c2">${fg('Last', inp(c, 'd.last', { cls: c.bad && c.bad.last ? 'bad' : '' }), { req: 1 })}${fg('First', inp(c, 'd.first', { cls: c.bad && c.bad.first ? 'bad' : '' }), { req: 1 })}${fg('Middle', inp(c, 'd.mi'))}${fg('Suffix', inp(c, 'd.suffix'))}</div></div>
    <div style="width:200px;border:1px dotted #aaa;height:180px;display:flex;align-items:center;justify-content:center;color:#666;text-align:center">${ic('user')}<br>Add Photo<br><span class="small">(not used in the simulator)</span></div></div>
  <div class="row c3 mt">${fg('Date of Birth', dp(c, 'd.dobT', { cls: c.bad && c.bad.dob ? 'bad' : '' }), { req: 1 })}${fg('Sex', sel(c, 'd.sex', SEXES))}${fg('Ethnicity', sel(c, 'd.ethnicity', ETHNICITIES))}</div>
  <div class="box"><h4>Home Address</h4><div class="row c1" style="grid-template-columns:1fr">${fg('Address Line 1', inp(c, 'd.addr1'))}${fg('Address Line 2', inp(c, 'd.addr2'))}</div><div class="row" style="grid-template-columns:2fr 80px 1fr">${fg('City', inp(c, 'd.city'))}${fg('State', sel(c, 'd.state', STATES, { blank: false }))}${fg('Zip', inp(c, 'd.zip'))}</div>${fg('Instructions', txt(c, 'd.instructions', { rows: 2 }))}<a data-act="mapOpen">Google Map to Patient's Home</a></div>
  <div class="box"><h4>Alternate Locations <button class="btn btn-add btn-sm" data-act="altAdd">${ic('plus')} Add</button></h4><table class="t"><thead><tr><th>Location Type</th><th>Address</th><th>City</th><th>State</th><th>Zip</th><th></th></tr></thead><tbody>${(c.d.altLocs || []).map((a, i) => `<tr><td>${esc(a.type)}</td><td>${esc(a.addr)}</td><td>${esc(a.city)}</td><td>${esc(a.state)}</td><td>${esc(a.zip)}</td><td><button class="ico-btn ico-del" data-act="altDel" data-i="${i}">${ic('trash')}</button></td></tr>`).join('') || '<tr><td colspan="6" class="none">No alternate locations</td></tr>'}</tbody></table></div>
  <div class="box"><h4>ID Numbers</h4><div class="row c2">${fg('Medical Record Number (MRN)', inp(c, 'd.mrn'))}${fg('SSN', inp(c, 'd.ssn', { type: 'password' }))}${fg('Medicare ID <a data-act="mbiInfo" title="About Medicare IDs">&#9432;</a>', inp(c, 'd.medicare'))}${fg('Medicaid ID', inp(c, 'd.medicaid'))}</div></div>
  ${fg('Email', inp(c, 'd.email', { type: 'email' }))}<div class="row c3">${fg('Home Phone', inp(c, 'd.phones.home'))}${fg('Mobile Phone', inp(c, 'd.phones.mobile'))}${fg('Other Phone', inp(c, 'd.phones.other'))}</div>
  <div class="box"><h4>Emergency Contact Information</h4><div class="row c2">${fg('Contact Name', inp(c, 'd.em.name'))}${fg('Email', inp(c, 'd.em.email'))}${fg('Phone 1', inp(c, 'd.em.phone1'))}${fg('Phone 2', inp(c, 'd.em.phone2'))}</div></div>
  <button class="btn btn-add" data-act="addContacts">Additional Contacts</button><div class="row c3 mt">${fg('Language', sel(c, 'd.lang', LANGS, { blank: false }))}</div>
  <div class="sec">Comments</div>${txt(c, 'd.comments', { rows: 4 })}
  <hr class="hr"><div class="flex" style="justify-content:flex-end"><button class="btn btn-del" data-act="ptDelete">Delete</button><button class="btn btn-save" data-act="ptSave">Save</button><button class="btn btn-cancel" data-act="ptCancel">Cancel</button><button class="btn btn-close" data-act="ptClose">Close</button></div>`;
}
ACT.mapOpen = () => alertBox("Map to the patient's home", `<p>In the real Alora this opens a map in a new window. In the simulator no map is loaded, so nothing leaves this page.</p>`);
ACT.mbiInfo = () => alertBox('Medicare ID', '<p>A Medicare number is 11 letters and numbers. Copy it exactly from the insurance card. Never type it from memory, and never put it in a file name, email or text.</p>');
ACT.altAdd = el => { const c = ctxOf(el); const m = ctxNew({ a: { type: 'Alternate address', addr: '', city: '', state: 'FL', zip: '' } }); modal({ title: 'Alternate Location', ctx: m, size: 'sm', body: mc => `${fg('Location Type', inp(mc, 'a.type'))}${fg('Address', inp(mc, 'a.addr'))}${fg('City', inp(mc, 'a.city'))}${fg('State', inp(mc, 'a.state'))}${fg('Zip', inp(mc, 'a.zip'))}`, buttons: [{ label: 'OK', cls: 'btn-ok', click: () => { c.d.altLocs.push(m.a); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
ACT.altDel = el => { const c = ctxOf(el); c.d.altLocs.splice(+el.dataset.i, 1); refresh(); };
ACT.addContacts = el => { const c = ctxOf(el); const m = ctxNew({ rows: JSON.parse(JSON.stringify(c.d.contacts || [])), n: '', r: '', ph: '' }); modal({ title: 'Additional Contacts', ctx: m, body: mc => `<table class="t"><thead><tr><th>Name</th><th>Relationship</th><th>Phone</th><th></th></tr></thead><tbody>${mc.rows.map((r, i) => `<tr><td>${esc(r.n)}</td><td>${esc(r.r)}</td><td>${esc(r.ph)}</td><td><button class="ico-btn ico-del" data-act="acDel" data-i="${i}">${ic('trash')}</button></td></tr>`).join('') || '<tr><td colspan="4" class="none">None</td></tr>'}</tbody></table><div class="row c3 mt">${fg('Name', inp(mc, 'n'))}${fg('Relationship', inp(mc, 'r'))}${fg('Phone', inp(mc, 'ph'))}</div><button class="btn btn-add btn-sm" data-act="acAdd">${ic('plus')} Add contact</button>`, buttons: [{ label: 'OK', cls: 'btn-ok', click: () => { c.d.contacts = m.rows; refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
ACT.acAdd = el => { const m = ctxOf(el); if (!m.n) return; m.rows.push({ n: m.n, r: m.r, ph: m.ph }); m.n = m.r = m.ph = ''; m._modal.rerender(); };
ACT.acDel = el => { const m = ctxOf(el); m.rows.splice(+el.dataset.i, 1); m._modal.rerender(); };

function ptDirty(c) { return JSON.stringify(c.d) !== c.orig; }
ACT.ptClose = el => { const c = ctxOf(el); const done = () => { track('demo:closed'); go('patients'); }; if (ptDirty(c)) confirmBox('Close without saving?', '<p>You typed changes that are not saved. Close anyway?</p>', done, { yes: 'Close anyway', no: 'Stay', kind: 'warn' }); else { if (!c.params.new) track('demo:closed-nochange'); done(); } };
ACT.ptCancel = el => {
  const c = ctxOf(el);
  if (c.params.new) confirmBox('Cancel', '<p>This unsaved document will be deleted. Are you sure?</p>', () => { track('pt:newcancel'); go('patients'); }, { yes: 'Yes', no: 'No' });
  else { c.d = ptToForm(P(c.params.id)); c.orig = JSON.stringify(c.d); c.bad = {}; refresh(); toast('What you typed was undone.', 'ok'); }
};
ACT.ptDelete = el => {
  const c = ctxOf(el);
  if (c.params.new) { ACT.ptCancel(el); return; }
  needApproval({ roles: ['Administrator'], what: 'Delete a patient', rule: 'Never click Delete on a patient, admission, or document unless the Administrator has authorized it in writing.', who: 'Administrator, in writing', ref: 'R2', go: () => confirmBox('Delete this patient?', `<p><b>${esc(ptName(P(c.params.id)))}</b> and everything filed under this patient will be removed from the practice data. (Reset restores it.)</p>`, () => {
    const pid = c.params.id; DB.patients = DB.patients.filter(x => x.id !== pid); const aids = DB.admissions.filter(a => a.pid === pid).map(a => a.id); DB.admissions = DB.admissions.filter(a => a.pid !== pid); ['referrals', 'docs', 'orders', 'assessments', 'snNotes', 'aideDocs', 'f485', 'commLog', 'forms', 'visits'].forEach(k => (DB[k] = DB[k].filter(x => x.pid !== pid)));
    simLog('override', 'Deleted patient (practice)'); save(); toast('Patient deleted (practice data).', 'ok'); go('patients');
  }, { yes: 'Delete', no: 'Cancel', kind: 'danger', yesCls: 'btn-del', noCls: 'btn-cancel' }) });
};
ACT.ptSave = el => {
  const c = ctxOf(el), d = c.d, isNew = !!c.params.new; c.bad = {}; c.dupNote = '';
  const dobIso = parseD(d.dobT);
  if (!d.last.trim()) c.bad.last = 1; if (!d.first.trim()) c.bad.first = 1; if (!dobIso) c.bad.dob = 1;
  if (Object.keys(c.bad).length) { refresh(); toast('Last name, first name and a valid date of birth (MM/DD/YYYY) are required.', 'err'); return; }
  const apply = () => {
    const rec = isNew ? Object.assign(blankPatient(), { id: uid('P'), created: todayIso(), createdBy: DB.session.userId }) : P(c.params.id);
    ['last', 'first', 'mi', 'suffix', 'sex', 'ethnicity', 'addr1', 'addr2', 'city', 'state', 'zip', 'instructions', 'mrn', 'ssn', 'medicare', 'medicaid', 'email', 'lang', 'comments'].forEach(k => (rec[k] = d[k]));
    rec.last = rec.last.trim().toUpperCase(); rec.first = rec.first.trim().toUpperCase(); rec.mi = (rec.mi || '').trim().toUpperCase(); rec.dob = dobIso; rec.phones = d.phones; rec.em = d.em; rec.altLocs = d.altLocs; rec.contacts = d.contacts;
    if (!rec.mrn) rec.mrn = String(DB.patients.length + 1);
    if (isNew) DB.patients.push(rec); rec.updatedBy = DB.session.userId; rec.updated = nowIso(); save(); track(isNew ? 'pt:created' : 'pt:saved'); simLog('info', (isNew ? 'Created patient ' : 'Saved changes to ') + ptName(rec));
    toast('Saved.', 'ok'); if (isNew) go('patient', { id: rec.id }); else { c.d = ptToForm(rec); c.orig = JSON.stringify(c.d); refresh(); }
  };
  const duplicate = DB.patients.find(x => x.id !== c.params.id && x.last === d.last.trim().toUpperCase() && x.first === d.first.trim().toUpperCase() && x.dob === dobIso);
  const proceed = () => {
    if (!isNew) { const o = P(c.params.id); const sens = o.last !== d.last.trim().toUpperCase() || o.first !== d.first.trim().toUpperCase() || o.dob !== dobIso || o.medicare !== d.medicare || o.medicaid !== d.medicaid || o.ssn !== d.ssn;
      if (sens) { needApproval({ roles: ['Administrator'], what: 'Change name, date of birth or ID numbers', rule: 'Office staff verify. The Administrator approves changes to identifiers and payer information.', who: 'Administrator', ref: 'O1, R2', go: apply }); return; } }
    apply();
  };
  if (isNew && duplicate) { modal({ title: 'Possible duplicate patient', kind: 'warn', size: 'sm', body: `<p><b>${esc(ptName(duplicate))}</b> with the same date of birth already exists.</p><p class="mt">Zenith rule: <b>STOP</b>. Use neither record. Tell the Administrator. Never create a second record for the same patient.</p>`, buttons: [{ label: 'Stop (recommended)', cls: 'btn-ok', click: () => simLog('good', 'Stopped at a possible duplicate patient') }, { label: 'Create anyway (practice)', cls: 'btn-or', click: () => { simLog('override', 'Created a duplicate patient record (practice): ' + ptName(duplicate)); proceed(); } }] }); return; }
  if (isNew) { const sim = DB.patients.find(x => x.last === d.last.trim().toUpperCase() && x.first === d.first.trim().toUpperCase()); if (sim) c.dupNote = 'A patient named ' + ptName(sim) + ' already exists (different date of birth). Check two identifiers before you go on.'; }
  proceed();
};

/* ---------------------------------------------------------------- referrals tab */
function refTab(c, d) {
  const pid = c.params.id; const tbl = DT(c, 'ref', () => ({ sort: 'date', dir: -1, noSearch: false, sizes: [10, 25, 50, 100], firstLast: false,
    cols: [{ key: 'act', label: 'Action', sortable: false, blue: true, render: r => rowIcons([{ ic: 'edit', t: 'Edit referral', act: 'refEdit', data: { id: r.id } }, { ic: 'trash', t: 'Delete', act: 'refDel', data: { id: r.id }, cls: 'del' }]) },
      { key: 'date', label: 'Referral date', text: r => r.date, render: r => fmtD(r.date) }, { key: 'status', label: 'Status', render: r => esc(r.status) }, { key: 'source', label: 'Referral Source', render: r => esc(r.source) }, { key: 'office', label: 'Office', render: r => esc(r.office) }, { key: 'comment', label: 'Comment', render: r => esc(r.comment) }],
    rows: DB.referrals.filter(r => r.pid === pid) }));
  return `${tbl}<div class="flex mt" style="justify-content:space-between"><a data-act="refAddAdm">Add Admission</a><div class="flex"><button class="btn btn-or" data-act="refAdd">Add Referral</button><button class="btn btn-close" data-act="refClose">Close</button></div></div>`;
}
ACT.refClose = () => go('patients'); ACT.refAddAdm = el => { const c = ctxOf(el); track('refs:addadm'); go('admission', { pid: c.params.id, add: 1 }); };
ACT.refAdd = el => refModal(ctxOf(el), null); ACT.refEdit = el => refModal(ctxOf(el), el.dataset.id);
ACT.refDel = el => needApproval({ roles: ['Administrator'], what: 'Delete a referral', rule: 'Never click Delete unless the Administrator has authorized it in writing.', who: 'Administrator', ref: 'R2', go: () => confirmBox('Delete referral?', '<p>Delete this referral entry?</p>', () => { DB.referrals = DB.referrals.filter(r => r.id !== el.dataset.id); save(); refresh(); }, { yes: 'Delete', no: 'Cancel' }) });
function refModal(pc, rid) {
  const ex = rid ? DB.referrals.find(r => r.id === rid) : null;
  const m = ctxNew({ r: ex ? { date: fmtD(ex.date), source: ex.source, physId: ex.physId, conf: ex.physConfirmed, status: ex.status, office: ex.office, comment: ex.comment } : { date: '', source: '', physId: '', conf: false, status: '', office: DB.lists.offices[0], comment: '' }, errs: {} });
  const mod = modal({ title: ex ? 'Edit Referral' : 'Add Referral', ctx: m, size: 'lg',
    body: c => `<div class="row c2">${fg('Referral Date', dp(c, 'r.date', { cls: c.errs.date ? 'bad' : '' }), { req: 1 })}<div></div>${fg('Referral Source', s2(c, 'r.source', 'refSources', { ph: 'Enter Referral Source' }) + `<a data-act="addRefSrc">Add Referral Source</a>`, { req: 1 })}<div></div>${fg('Physician', s2(c, 'r.physId', 'physicians', { ph: 'Enter Physician Name' }) + `<a data-act="addPhys">Add Physician</a>`)}<div></div></div>
      <div class="fg"><label class="chk"><input type="checkbox" ${battr(c, 'r.conf')}${c.r.conf ? ' checked' : ''}> Physician Confirmed</label> <a data-act="physConfInfo">&#9432;</a></div>
      <div class="fg"><label>Status</label><div class="chkbox">${['Admitted', 'In Progress', 'Not Admitted'].map(s => radio(c, 'r.status', s, s)).join('')}</div></div>${fg('Office', s2(c, 'r.office', 'offices', { ph: 'Enter Office' }))}${fg('Comments', txt(c, 'r.comment', { rows: 3 }))}`,
    buttons: [{ label: 'OK', cls: 'btn-ok', click: (mm) => {
      const r = m.r; m.errs = {}; const date = parseD(r.date); if (!date) m.errs.date = 1;
      if (!r.source) { toast('Referral Source is required.', 'err'); mm.rerender(); return false; }
      if (m.errs.date) { toast('Enter the referral date (MM/DD/YYYY).', 'err'); mm.rerender(); return false; }
      const save1 = () => { const rec = { id: ex ? ex.id : uid('RF'), pid: pc.params.id, date, source: r.source, physId: r.physId, physConfirmed: !!r.conf, status: r.status || 'In Progress', office: r.office, comment: r.comment, by: DB.session.userId };
        if (ex) Object.assign(ex, rec); else DB.referrals.push(rec); save(); track('referral:saved'); simLog('info', 'Logged referral for ' + ptName(P(pc.params.id))); mod.close(); refresh(); toast('Referral saved.', 'ok'); };
      if (!r.physId) { modal({ title: 'Referral is missing a physician', kind: 'warn', size: 'sm', body: '<p>Zenith rule: <b>STOP and ask the Administrator or DON</b> when a referral is missing a physician, diagnosis, payer or phone number. Do not guess.</p>', buttons: [{ label: 'Stop (recommended)', cls: 'btn-ok', click: () => simLog('good', 'Stopped: referral missing physician') }, { label: 'Save anyway (practice)', cls: 'btn-or', click: () => { simLog('override', 'Saved referral without a physician'); save1(); } }] }); return false; }
      save1(); return false; } }, { label: 'Cancel', cls: 'btn-del' }] });
}
ACT.addRefSrc = () => needApproval({ roles: ['Administrator'], what: 'Add a Referral Source', rule: 'Do not use Add Referral Source or Add Physician unless the Administrator told you to.', who: 'Administrator', ref: 'O2', go: () => { const m = ctxNew({ n: '' }); modal({ title: 'Add Referral Source', ctx: m, size: 'sm', body: c => fg('Name', inp(c, 'n')), buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { if (!m.n.trim()) return false; DB.lists.referralSources.push(m.n.trim()); save(); toast('Referral source added.', 'ok'); } }, { label: 'Cancel', cls: 'btn-del' }] }); } });
ACT.addPhys = () => needApproval({ roles: ['Administrator'], what: 'Add a Physician', rule: 'Do not use Add Referral Source or Add Physician unless the Administrator told you to.', who: 'Administrator', ref: 'O2', go: () => { const m = ctxNew({ n: '', npi: '' }); modal({ title: 'Add Physician', ctx: m, size: 'sm', body: c => fg('Name (LAST, FIRST MD)', inp(c, 'n')) + fg('NPI (10 digits)', inp(c, 'npi')), buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { if (!m.n.trim()) return false; DB.lists.physicians.push({ id: uid('PH'), name: m.n.trim().toUpperCase(), npi: m.npi }); save(); toast('Physician added.', 'ok'); } }, { label: 'Cancel', cls: 'btn-del' }] }); } });
ACT.physConfInfo = () => alertBox('Physician Confirmed', '<p>Check this box only when someone has confirmed with the physician\'s office that the physician really referred this patient.</p>');

/* ---------------------------------------------------------------- Admission, Insurance and Prior Auth */
ROUTES.admissions = {
  render(c) {
    const tbl = DT(c, 'adm', () => ({ filterBtn: true, sort: 'name',
      cols: [{ key: 'sel', label: 'Select', sortable: false, blue: true, render: r => `<div style="display:flex;flex-wrap:wrap;width:100px">${rowIcons([{ ic: 'edit', t: 'Select', act: 'admOpen', data: { aid: r.a.id } }, { ic: 'print', t: 'Print admission profile', act: 'admPrint', data: { aid: r.a.id }, cls: 'print' }, { ic: 'doc', t: 'Word', act: 'admPrint', data: { aid: r.a.id }, cls: 'word' }, { ic: 'doc', t: 'PDF', act: 'admPrint', data: { aid: r.a.id }, cls: 'pdf' }, { ic: 'clip', t: 'Attach to AloraMail', act: 'admMail', data: { aid: r.a.id }, cls: 'clip' }])}</div>` },
        { key: 'name', label: 'Patient Name', blue: true, text: r => ptName(r.p), render: r => esc(ptName(r.p)) }, { key: 'pan', label: 'PAN #', text: r => r.a.pan, render: r => esc(r.a.pan) }, { key: 'admit', label: 'Admit Date', text: r => r.a.admit, render: r => fmtD(r.a.admit) },
        { key: 'disch', label: 'Discharge Date', text: r => r.a.dischDate || '', render: r => fmtD(r.a.dischDate) }, { key: 'dob', label: 'DOB', text: r => r.p.dob, render: r => fmtD(r.p.dob) }, { key: 'office', label: 'Office Name', render: r => esc(r.a.office) }],
      rows: admRows(c), searchText: r => ptName(r.p) + ' ' + r.a.pan }));
    return pageHead('Admission, Insurance & Prior Auth', 'List') + `<div class="bar"><h2>${ic('user')} Admission</h2><button class="btn btn-add" data-act="admAdd">${ic('plus')} Add</button></div>${tbl}<label class="chk mt"><input type="checkbox" ${battr(c, 'inactive')} data-rr="1"${c.inactive ? ' checked' : ''}> Include Inactivated Admissions</label>
      <button class="gotobtn" style="background:#fff3d6;color:#c47a00;border:1px solid #f0c060;top:150px" data-act="covidEmp">COVID-19 Employee Screening</button><button class="helpvid" data-act="helpVideo" style="top:230px">&#9654; Help Video</button>`;
  },
};
ACT.helpVideo = () => alertBox('Help Video', '<p>The real Alora plays a how-to video here. Videos are not part of the simulator.</p>');
ACT.covidEmp = () => go('covid-emp');
ACT.admOpen = el => { track('adm:open'); go('admission', { aid: el.dataset.aid }); };
ACT.admPrint = el => { const a = byId(DB.admissions, el.dataset.aid); printPreview('Admission Profile', admProfileHtml(a)); };
ACT.admMail = el => { const a = byId(DB.admissions, el.dataset.aid); composeMail({ subject: 'Admission profile: ' + ptName(P(a.pid)), body: '(attached admission profile, practice)' }); };
ACT.admAdd = () => needApproval({ roles: ['Administrator', 'Office'], what: 'Add an admission', rule: 'Add an admission only after the Administrator approves the admission.', who: 'Administrator', ref: 'O4', go: () => { const m = ctxNew({ pid: '' }); modal({ title: 'Add Admission: choose the patient', ctx: m, size: 'sm', body: c => fg('Patient', s2(c, 'pid', 'patientsAll', { ph: 'Enter Patient name' })) + '<p class="small">Search the patient first. An admission belongs to one patient.</p>', buttons: [{ label: 'Continue', cls: 'btn-ok', click: () => { if (!m.pid) { toast('Choose a patient.', 'err'); return false; } go('admission', { pid: m.pid, add: 1 }); } }, { label: 'Cancel', cls: 'btn-del' }] }); } });

function certPeriods(a) { const out = []; let s = a.admit; const end = a.dischDate && a.dischDate > a.admit ? a.dischDate : addDays(todayIso(), 120); let n = 0; while (s <= end && n < 40) { const e = addDays(s, 59); out.push({ k: s, from: s, to: e, l: fmtD(s).slice(0, 6) + fmtD(s).slice(8) + ' - ' + fmtD(e).slice(0, 6) + fmtD(e).slice(8), no: n + 1 }); s = addDays(s, 60); n++; } return out; }
function curCert(a) { const t = todayIso(); return certPeriods(a).find(x => x.from <= t && t <= x.to) || null; }
function admProfileHtml(a) { const p = P(a.pid); return `<h2>Admission Profile (practice)</h2><table class="t"><tbody><tr><td>Patient</td><td>${esc(ptName(p))}</td></tr><tr><td>DOB</td><td>${fmtD(p.dob)}</td></tr><tr><td>Admit date</td><td>${fmtD(a.admit)}</td></tr><tr><td>PAN</td><td>${a.pan}</td></tr><tr><td>Physician</td><td>${esc(physName(a.physId))}</td></tr><tr><td>Payer</td><td>${esc(payerName((a.ins[0] || {}).payer))}</td></tr><tr><td>Status</td><td>${esc(a.status)}</td></tr></tbody></table>`; }
function printPreview(title, html) { modal({ title: esc(title) + ' (print preview)', size: 'lg', body: `<div class="note sim">Simulated print. Nothing is sent to a printer.</div><div style="border:1px solid #ccc;padding:20px;background:#fff">${html}</div>`, buttons: [{ label: 'Print (simulated)', cls: 'btn-blue', click: () => { simLog('info', 'Print preview shown (simulated): ' + title); toast('Simulated print. No printer was used.', 'sim'); return false; } }, { label: 'Download (practice file)', cls: 'btn-gray', click: () => { downloadText(title.replace(/\W+/g, '_') + '.html', '<!doctype html><meta charset="utf-8"><title>' + esc(title) + '</title><body style="font-family:Arial">' + html + '<p style="color:#a60">Practice document from the AloraPlus Training Simulator. Not a real record.</p></body>'); return false; } }, { label: 'Close', cls: 'btn-close' }] }); }

function blankAdm(pid) { return { id: 'NEW', pid, status: 'Admitted', admit: '', pan: '', office: DB.lists.offices[0], county: '', physId: '', refPhysId: '', caseMgr: '', sourceOfAdm: '', refSource: '', transferred: false, dnr: false, dischDate: '', dischCode: '', ins: [], diag: [], disciplines: [], freq: [], other: { precautions: '' } }; }
ROUTES.admission = {
  render(c, p) {
    const isNew = !!p.add; if (!c.a) { const src = isNew ? blankAdm(p.pid) : byId(DB.admissions, p.aid); if (!src) return pageHead('Admission', '') + notice('Admission not found.', 'err'); c.a = JSON.parse(JSON.stringify(src)); c.a.admitT = fmtD(c.a.admit); c.a.dischT = fmtD(c.a.dischDate); c.orig = JSON.stringify(c.a); c.tab = 'adm'; if (isNew) { c.a.pan = nextPan(); } }
    const a = c.a, pt = P(a.pid); const aid = a.id;
    const tabs = tabsHtml([{ k: 'adm', l: 'Admission' }, { k: 'dx', l: 'Diagnoses & Procedures' }, { k: 'disc', l: 'Disciplines' }, { k: 'freq', l: 'Frequency' }, { k: 'other', l: 'Other' }], c.tab, 'admTab');
    const pane = { adm: admPane, dx: dxPane, disc: discPane, freq: freqPane, other: otherPane }[c.tab](c, a, pt, isNew);
    return `<div class="flex"><div class="grow">${tabs}</div><button class="btn btn-or" data-act="gotoToggle">GoTo</button></div><div class="tabpane"><h2 style="font:400 34px var(--font);color:#2b7bb9;margin:6px 0">${esc(ptName(pt))}</h2><div class="bar" style="padding:6px 14px"><span>DOB &nbsp; ${fmtD(pt.dob)}</span></div>${pane}</div>${gotoPanel(c, a)}`;
  },
};
function nextPan() { return Math.max(0, ...DB.admissions.map(a => +a.pan || 0)) + 1; }
ACT.admTab = el => { const c = ctxOf(el); c.tab = el.dataset.k; refresh(); };
function covidToday(pid) { return DB.covid.find(x => x.pid === pid && x.date.slice(0, 10) === todayIso()); }
function covidLast(pid) { return DB.covid.filter(x => x.pid === pid).sort((a, b) => (a.date < b.date ? 1 : -1))[0]; }
function admPane(c, a, pt, isNew) {
  const lastC = covidLast(a.pid);
  const ban = covidToday(a.pid) ? '' : `<div class="note warn" style="align-items:center;font-size:16px"><span style="color:#d9534f;font-size:30px">&#9888;</span><div class="grow"><div>COVID-19 Patient Screening has not been completed today.</div><div class="mt">Most Recent Screening : ${lastC ? fmtD(lastC.date) : 'None'}<br>- Risk Level : ${lastC ? lastC.risk : 'N/A'}</div></div><button class="btn btn-or" data-act="admCovid">Go to Screening</button></div>`;
  const bad = c.bad || {};
  return `${ban}<div class="sec">Admission</div><div class="fg"><label>Admission Status</label><div class="chkbox" style="display:inline-flex">${['Admitted', 'Discharged', 'Not Admitted'].map(s => radio(c, 'a.status', s, s, { rr: 1 })).join('')}</div></div>
  <div class="row c2">${fg('Admit Date', dp(c, 'a.admitT', { cls: bad.admit ? 'bad' : '' }), { req: 1 })}${fg('Patient Account Number (PAN)', inp(c, 'a.pan'))}
  ${fg('Office', s2(c, 'a.office', 'offices'))}${fg('County/CBSA', inp(c, 'a.county'))}
  ${fg('Physician', s2(c, 'a.physId', 'physicians', { ph: 'Enter Physician Name', clear: 1 }) + `<a data-act="addPhys">Add Physician</a> &nbsp; <a data-act="physInfo">&#9432; Physician Info</a>`)}${fg('Case Manager/Primary RN', s2(c, 'a.caseMgr', 'staff', { ph: 'Enter Case Manager', clear: 1 }))}
  ${fg('Referring/Certifying Physician <a data-act="certPhysInfo">&#9432;</a>', s2(c, 'a.refPhysId', 'physicians', { ph: 'Enter Physician Name', clear: 1 }))}${fg('Referral Source', s2(c, 'a.refSource', 'refSources', { ph: 'Enter Referral Source', clear: 1 }))}
  ${fg('Source of Admission', s2(c, 'a.sourceOfAdm', 'admSources', { ph: 'Enter Source of Admission', clear: 1 }))}<div></div></div>
  <div class="fg">${chk(c, 'a.transferred', 'Transferred from another Home Health Agency')}</div>
  <div class="fg"><label>DNR:</label><div class="chkbox" style="display:inline-flex"><label class="chk"><input type="checkbox" data-act="dnr" data-v="yes"${a.dnr ? ' checked' : ''}> Yes</label><label class="chk"><input type="checkbox" data-act="dnr" data-v="no"${!a.dnr ? ' checked' : ''}> No</label></div></div>
  <div class="row c2">${fg('Discharge Date', dp(c, 'a.dischT') + `<a data-act="dcSummary">Discharge Summary</a>`)}${fg('Discharge Code', inp(c, 'a.dischCode'))}</div>
  <div class="sec sm" style="background:none;color:#2b7bb9;border-bottom:1px solid #ddd;padding-left:0">Insurance &amp; Prior Auth <button class="btn btn-add btn-sm" data-act="insAdd">${ic('plus')} Add Insurance</button></div>
  <table class="t"><thead><tr><th>Actions</th><th>Responsibility</th><th>Payer</th><th>Effective From</th><th>Effective To</th><th>Member ID</th></tr></thead><tbody>${a.ins.map((i, k) => `<tr><td><button class="btn btn-add btn-sm" data-act="insMenu" data-i="${k}" title="Actions">${ic('list')}</button></td><td>${esc(i.resp)}</td><td>${esc(payerName(i.payer))}</td><td>${fmtD(i.from)}</td><td>${fmtD(i.to)}</td><td>${esc(i.memberId || '')}</td></tr>`).join('') || '<tr><td colspan="6" class="none">No insurance entered. Add insurance before billing.</td></tr>'}</tbody></table>
  <div class="flex mt"><button class="btn btn-del" data-act="admDelete">Delete</button><span class="grow"></span><button class="btn btn-save" data-act="admSave">Save</button><button class="btn btn-back" data-act="admNext">Next Tab</button><button class="btn btn-close" data-act="admClose">Close</button></div>
  <div class="flex mt" style="gap:8px">${[['Show Cert Periods', 'admCerts'], ['Print Admission Profile', 'admProfile'], ['Vitals Dashboard', 'admSim'], ['Pre-Claim Review', 'admPre', 1], ['HHVBP Legacy', 'admSim'], ['Service Provided Location', 'admSim'], ['HHCCN', 'admSim'], ['NOMNC', 'admSim'], ['Emergency Preparedness Plan', 'admSim'], ['Attach to Alora Mail', 'admAttach'], ['Hospitalization Log', 'admSim']].map(([l, act, dis]) => `<button class="btn btn-add${dis ? ' dis' : ''}" data-act="${act}" data-l="${esc(l)}"${dis ? ' disabled' : ''}>${esc(l)}</button>`).join('')}</div>`;
}
ACT.dnr = el => { const c = ctxOf(el); c.a.dnr = el.dataset.v === 'yes'; refresh(); };
ACT.physInfo = el => { const c = ctxOf(el); const p = byId(DB.lists.physicians, c.a.physId); alertBox('Physician Info', p ? `<div class="kv"><div>Name</div><div>${esc(p.name)}</div><div>NPI</div><div>${esc(p.npi)}</div></div><p class="small mt">Practice data. In the real Alora physicians come from the NPI registry.</p>` : '<p>Choose a physician first.</p>'); };
ACT.certPhysInfo = () => alertBox('Referring/Certifying Physician', '<p>The physician who referred the patient or who certifies the plan of care. It can be the same person as the Physician above.</p>');
ACT.dcSummary = el => { const c = ctxOf(el); go('form-dc', { aid: c.a.id }); };
ACT.admCovid = el => { const c = ctxOf(el); go('covid', { pid: c.a.pid }); };
ACT.admSim = el => alertBox(el.dataset.l, `<p class="stub">${simplified()} This button opens a separate form in the real Alora. It is not part of Zenith's manual, so it is not simulated here.</p>`);
ACT.admProfile = el => printPreview('Admission Profile', admProfileHtml(ctxOf(el).a));
ACT.admAttach = el => { const c = ctxOf(el); composeMail({ subject: 'Admission: ' + ptName(P(c.a.pid)), body: '(attached admission profile, practice)' }); };
ACT.admNext = el => { const c = ctxOf(el); const order = ['adm', 'dx', 'disc', 'freq', 'other']; c.tab = order[(order.indexOf(c.tab) + 1) % order.length]; refresh(); };
ACT.admClose = el => { const c = ctxOf(el); const out = () => go('admissions'); if (JSON.stringify(c.a) !== c.orig) confirmBox('Close without saving?', '<p>You typed changes that are not saved. Close anyway?</p>', out, { yes: 'Close anyway', no: 'Stay', kind: 'warn' }); else out(); };
ACT.admCerts = el => { const c = ctxOf(el); const a = byId(DB.admissions, c.a.id) || c.a; const cp = certPeriods(a); modal({ title: 'Cert Periods', size: 'sm', body: `<table class="t"><thead><tr><th>#</th><th>From</th><th>Through</th><th></th></tr></thead><tbody>${cp.map(x => `<tr class="${curCert(a) && curCert(a).from === x.from ? 'sel' : ''}"><td>${x.no}</td><td>${fmtD(x.from)}</td><td>${fmtD(x.to)}</td><td>${curCert(a) && curCert(a).from === x.from ? '<span class="tag g">Current</span>' : ''}</td></tr>`).join('')}</tbody></table>`, buttons: [{ label: 'Close', cls: 'btn-close' }] }); track('certperiods'); };
ACT.admDelete = el => { const c = ctxOf(el); if (c.params.add) { go('admissions'); return; } needApproval({ roles: ['Administrator'], what: 'Delete an admission', rule: 'Never click Delete on a patient, admission, or document unless the Administrator has authorized it in writing.', who: 'Administrator', ref: 'R2', go: () => confirmBox('Delete this admission?', '<p>The admission and what is filed under it will be removed from the practice data.</p>', () => { DB.admissions = DB.admissions.filter(x => x.id !== c.a.id); save(); go('admissions'); }, { yes: 'Delete', no: 'Cancel' }) }); };
ACT.insAdd = el => insModal(ctxOf(el), -1); ACT.insMenu = el => { const c = ctxOf(el); const i = +el.dataset.i; popMenu(el, [{ label: 'Edit', ic: 'edit', run: () => insModal(c, i) }, { label: 'Delete', ic: 'trash', cls: 'del', danger: true, run: () => needApproval({ roles: ['Administrator'], what: 'Delete insurance', rule: 'Never delete without written Administrator authorization.', who: 'Administrator', ref: 'R2', go: () => { c.a.ins.splice(i, 1); refresh(); } }) }]); };
function insModal(c, i) {
  const ex = i >= 0 ? c.a.ins[i] : null;
  needApproval({ roles: ['Administrator', 'Biller'], what: 'Add or change insurance', rule: 'Admission Status, Admit Date and insurance are approved by the Administrator.', who: 'Administrator', ref: 'R2', go: () => {
    const m = ctxNew({ i: ex ? { resp: ex.resp, payer: ex.payer, from: fmtD(ex.from), to: fmtD(ex.to), memberId: ex.memberId } : { resp: 'Primary', payer: '', from: c.a.admitT || '', to: '', memberId: '' } });
    modal({ title: ex ? 'Insurance' : 'Add Insurance', ctx: m, size: 'sm', body: mc => fg('Responsibility', sel(mc, 'i.resp', ['Primary', 'Secondary', 'Tertiary', 'Non-Insurance'], { blank: false })) + fg('Payer', s2(mc, 'i.payer', 'payers', { ph: 'Enter Payer' }), { req: 1 }) + fg('Member ID', inp(mc, 'i.memberId')) + fg('Effective From', dp(mc, 'i.from'), { req: 1 }) + fg('Effective To', dp(mc, 'i.to')),
      buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { const f = parseD(m.i.from); if (!m.i.payer || !f) { toast('Payer and a valid Effective From date are required.', 'err'); return false; } const rec = { id: ex ? ex.id : uid('IN'), resp: m.i.resp, payer: m.i.payer, from: f, to: parseD(m.i.to) || '', memberId: m.i.memberId }; if (ex) c.a.ins[i] = rec; else c.a.ins.push(rec); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] });
  } });
}
function dxPane(c, a) { return `<div class="flex"><h4 style="font:400 22px var(--font)">Diagnoses &amp; Procedures</h4><button class="btn btn-add btn-sm" data-act="dxAdd">${ic('plus')} Add</button></div><table class="t"><thead><tr><th></th><th>Code</th><th>Description</th><th>Date</th><th>Type</th></tr></thead><tbody>${a.diag.map((d, i) => `<tr><td><button class="ico-btn ico-del" data-act="dxDel" data-i="${i}">${ic('trash')}</button></td><td>${esc(d.code)}</td><td>${esc(d.desc)}</td><td>${fmtD(d.date)}</td><td>${esc(d.type)}</td></tr>`).join('') || '<tr><td colspan="5" class="none">No diagnoses entered</td></tr>'}</tbody></table>${saveRow()}`; }
function saveRow() { return `<div class="flex mt" style="justify-content:flex-end"><button class="btn btn-save" data-act="admSave">Save</button><button class="btn btn-back" data-act="admNext">Next Tab</button><button class="btn btn-close" data-act="admClose">Close</button></div>`; }
ACT.dxAdd = el => { const c = ctxOf(el); const m = ctxNew({ d: { code: '', desc: '', date: fmtD(todayIso()), type: 'Primary' } }); modal({ title: 'Add Diagnosis (practice)', ctx: m, size: 'sm', body: mc => fg('Code', inp(mc, 'd.code')) + fg('Description', inp(mc, 'd.desc')) + fg('Date', dp(mc, 'd.date')) + fg('Type', sel(mc, 'd.type', ['Primary', 'Secondary'], { blank: false })), buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { if (!m.d.code.trim()) { toast('Enter a code.', 'err'); return false; } c.a.diag.push({ id: uid('DX'), code: m.d.code.trim(), desc: m.d.desc, date: parseD(m.d.date) || todayIso(), type: m.d.type }); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
ACT.dxDel = el => { const c = ctxOf(el); c.a.diag.splice(+el.dataset.i, 1); refresh(); };
function discPane(c, a) { return `<h4 style="font:400 22px var(--font)">Disciplines ordered</h4><div class="chkbox">${DISCIPLINES.filter(d => d !== 'OFFICE').map(d => `<label class="chk"><input type="checkbox" data-act="discTog" data-d="${d}"${a.disciplines.includes(d) ? ' checked' : ''}> ${d}</label>`).join('')}</div><p class="small mt">Schedule only disciplines the physician ordered.</p>${saveRow()}`; }
ACT.discTog = el => { const c = ctxOf(el); const d = el.dataset.d; const i = c.a.disciplines.indexOf(d); if (i >= 0) c.a.disciplines.splice(i, 1); else c.a.disciplines.push(d); };
function freqPane(c, a) { return `<div class="flex"><h4 style="font:400 22px var(--font)">Frequency</h4><button class="btn btn-add btn-sm" data-act="fqAdd">${ic('plus')} Add</button></div><table class="t"><thead><tr><th></th><th>Discipline</th><th>Frequency</th><th>From</th><th>To</th></tr></thead><tbody>${a.freq.map((f, i) => `<tr><td><button class="ico-btn ico-del" data-act="fqDel" data-i="${i}">${ic('trash')}</button></td><td>${esc(f.disc)}</td><td>${esc(f.freq)} <span class="small">${esc(freqText(f.freq))}</span></td><td>${fmtD(f.from)}</td><td>${fmtD(f.to)}</td></tr>`).join('') || '<tr><td colspan="5" class="none">No frequency entered</td></tr>'}</tbody></table><p class="small mt">Write frequency like 2w4 (2 times a week for 4 weeks). The Scheduler's "View Frequency" compares it with scheduled visits.</p>${saveRow()}`; }
function freqText(s) { const m = /^(\d+)w(\d+)$/i.exec(s || ''); return m ? `(${m[1]} time${m[1] == 1 ? '' : 's'} a week for ${m[2]} week${m[2] == 1 ? '' : 's'})` : ''; }
ACT.fqAdd = el => { const c = ctxOf(el); const m = ctxNew({ f: { disc: 'RN', freq: '', from: c.a.admitT || '', to: '' } }); modal({ title: 'Add Frequency', ctx: m, size: 'sm', body: mc => fg('Discipline', sel(mc, 'f.disc', DISCIPLINES.filter(d => d !== 'OFFICE'), { blank: false })) + fg('Frequency (example 2w4)', inp(mc, 'f.freq')) + fg('From', dp(mc, 'f.from')) + fg('To', dp(mc, 'f.to')), buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { if (!freqText(m.f.freq)) { toast('Write frequency like 2w4.', 'err'); return false; } c.a.freq.push({ id: uid('FQ'), disc: m.f.disc, freq: m.f.freq, from: parseD(m.f.from) || '', to: parseD(m.f.to) || '' }); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
ACT.fqDel = el => { const c = ctxOf(el); c.a.freq.splice(+el.dataset.i, 1); refresh(); };
function otherPane(c, a) { return `<h4 style="font:400 22px var(--font)">Other</h4>${fg('Critical Precautions (print at the top of every note)', txt(c, 'a.other.precautions', { rows: 3 }))}${saveRow()}`; }
ACT.admSave = el => {
  const c = ctxOf(el), a = c.a, isNew = !!c.params.add; c.bad = {};
  const admit = parseD(a.admitT); if (!admit) c.bad.admit = 1; if (Object.keys(c.bad).length) { c.tab = 'adm'; refresh(); toast('Enter a valid Admit Date (MM/DD/YYYY).', 'err'); return; }
  const orig = isNew ? null : byId(DB.admissions, a.id);
  const apply = () => {
    const rec = isNew ? Object.assign(blankAdm(a.pid), { id: uid('A') }) : orig;
    ['status', 'pan', 'office', 'county', 'physId', 'refPhysId', 'caseMgr', 'sourceOfAdm', 'refSource', 'transferred', 'dnr', 'dischCode'].forEach(k => (rec[k] = a[k]));
    rec.admit = admit; rec.dischDate = parseD(a.dischT) || ''; rec.ins = a.ins; rec.diag = a.diag; rec.disciplines = a.disciplines; rec.freq = a.freq; rec.other = a.other;
    rec.inactive = rec.status !== 'Admitted'; if (isNew) { DB.admissions.push(rec); track('adm:created'); } save(); track('adm:saved'); simLog('info', 'Saved admission for ' + ptName(P(rec.pid)));
    toast('Saved.', 'ok'); if (isNew) go('admission', { aid: rec.id }); else { c.a = JSON.parse(JSON.stringify(rec)); c.a.admitT = fmtD(rec.admit); c.a.dischT = fmtD(rec.dischDate); c.orig = JSON.stringify(c.a); refresh(); }
  };
  if (!isNew && (orig.status !== a.status || orig.admit !== admit)) needApproval({ roles: ['Administrator'], what: 'Change Admission Status or Admit Date', rule: 'Admission Status, Admit Date and insurance are approved by the Administrator.', who: 'Administrator', ref: 'R2', go: apply }); else apply();
};

/* ---------------------------------------------------------------- GoTo panel (shortcuts to the patient's other screens) */
const GOTO = [['COVID-19 Patient Screening', 'covid', 'link'], ['485', 'f485-pt', 'link'], ['Aide Docs', 'aide-pt', 'link'], ['All Documents', 'alldocs', 'doc'], ['Allergy', 'form-allergy', 'link'], ['Braden Scale', 'form-braden', 'link'], ['Alora Mail', 'mail', 'mail'], ['Care Team', 'form-careteam', 'link'], ['Claims', 'claimsum', 'link'],
  ['Communication Log', 'commlog', 'msg'], ['Electronic Health Records', 'ehrlist', 'link'], ['Invoice', 'invoice', 'link'], ['Med Profile', 'form-med', 'pill'], ['Missed Visit', 'form-missed', 'list'], ['MSW', 'form-msw', 'list'], ['Assessments (OASIS Mgmt)', 'assess-pt', 'link'], ['General Form (Orders & Docs)', 'orders-pt', 'link'], ['OT Documents', 'form-ot', 'link'],
  ['Patient Demographics', 'patient', 'list'], ['POC Plus', 'form-pocplus', 'link'], ['A/R Trans', 'artrans', 'link'], ['PT Documents', 'form-pt', 'link'], ['Scheduler', 'scheduler', 'link'], ['SN Note', 'sn-pt', 'link'], ['Speech Therapy', 'form-st', 'link'], ['Spl Pay Rate', 'form-splpay', 'msg'], ['Supervisory Notes', 'form-sup', 'link'],
  ['Supply/Modality Log', 'form-supply', 'pill'], ['Discharge/Transfer Summary', 'form-dc', 'bus'], ['Order Plus (Verbal Order Plus)', 'form-orderplus', 'link'], ['Tinetti Assessment', 'form-tinetti', 'link']];
function gotoPanel(c, a) { if (!DB.ui.goto) return ''; return `<div class="goto-panel">${GOTO.map(([l, r, i]) => `<a data-act="gotoGo" data-r="${r}" data-aid="${a.id}" data-pid="${a.pid}">${ic(i)}${esc(l)}</a>`).join('')}</div>`; }
ACT.gotoToggle = () => { DB.ui.goto = !DB.ui.goto; save(); refresh(); };
ACT.gotoGo = el => { DB.ui.goto = false; save(); track('goto:' + el.dataset.r); const r = el.dataset.r; if (r === 'patient') go('patient', { id: el.dataset.pid }); else if (r === 'covid') go('covid', { pid: el.dataset.pid }); else if (['mail', 'claimsum', 'invoice', 'artrans', 'scheduler'].includes(r)) go(r, r === 'scheduler' ? { pid: el.dataset.pid } : null); else go(r, { aid: el.dataset.aid }); };
function gotoBtn() { return `<button class="gotobtn" data-act="gotoToggle">GoTo</button><button class="helpvid" data-act="helpVideo">&#9654; Help Video</button>`; }

/* ---------------------------------------------------------------- Patient Chart (read only summary) */
ROUTES.chart = {
  render(c, p) {
    if (!p.aid) return admSearchPage(c, 'Patient Chart', 'chart', { sub: 'Patient Search', pre: `<div class="bar"><h2>${ic('user')} Patient Chart</h2></div>` });
    const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return notice('Not found.', 'err');
    const cp = curCert(a); const docs = DB.docs.filter(d => d.pid === pt.id && !d.deleted).length; const ords = DB.orders.filter(o => o.pid === pt.id);
    const notes = DB.snNotes.filter(n => n.pid === pt.id);
    return `<div class="small">Patient / <b>Patient Chart</b></div><div style="font:600 40px var(--font);color:#1a2b3c;margin:12px 0">Patient Chart</div><div class="card" style="padding:26px"><div class="flex" style="align-items:flex-start;gap:30px"><div style="width:110px;height:110px;border-radius:50%;background:#eee;display:flex;align-items:center;justify-content:center">${ic('user', 'ico')}</div><div class="grow"><div style="font:600 36px var(--font);color:#2b7bb9">${esc(pt.first + ' ' + pt.last)}</div>
      <div class="flex mt" style="gap:50px"><div><span class="small">PAN</span> &nbsp; ${a.pan}</div><div><span class="small">DOB</span> &nbsp; <b>${fmtD(pt.dob)}</b></div><div><span class="small">Admit Date</span> &nbsp; <b>${fmtD(a.admit)}</b></div></div>
      <div class="flex mt" style="gap:50px"><div><span class="small">Disch Date</span> &nbsp; ${a.dischDate ? fmtD(a.dischDate) : '-'}</div><div><span class="small">Current Cert Period</span> &nbsp; <b>${cp ? cp.l : 'null'}</b></div></div></div></div>
      <div class="mt" style="padding:20px"><h3 style="font:600 20px var(--font);margin-bottom:12px">Demographics</h3><div class="row c2"><div><div class="small">Home Phone</div>${esc(pt.phones.home)}</div><div><div class="small">Address</div>${esc([pt.addr1, pt.city, pt.state, pt.zip].filter(Boolean).join(', '))}</div><div><div class="small">Sex</div><b>${esc(pt.sex)}</b></div><div><div class="small">Emergency Contact</div><b>${esc(pt.em.name)} ${esc(pt.em.phone1)}</b></div></div></div></div>
      <div class="cardgrid"><div class="card"><h4>Documents on file</h4><div class="n">${docs}</div><a data-go="ehrlist?aid=${a.id}">Open Electronic Health Records</a></div><div class="card ${ords.some(o => !o.signed) ? 'warn' : ''}"><h4>Orders</h4><div class="n">${ords.length}</div><div class="small">${ords.filter(o => !o.signed).length} not signed</div></div><div class="card"><h4>SN notes</h4><div class="n">${notes.length}</div><div class="small">${notes.filter(n => n.status !== 'Completed').length} still DRAFT</div></div></div>
      <p class="small">Chart summary is look-only. It is not proof a document is uploaded. Check Electronic Health Records.</p><div class="flex"><button class="btn btn-back" data-act="chartBack">${ic('back')} Back</button></div>`;
  },
};
ACT.chartBack = () => go('chart');

/* ---------------------------------------------------------------- Patient Communication Log */
ROUTES.commlog = {
  render(c, p) {
    if (!p.aid) return admSearchPage(c, 'Patient Communication Log', 'commlog', { sub: 'Patient Admission Search' });
    const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return notice('Not found.', 'err');
    const tbl = DT(c, 'cl', () => ({ sort: 'date', dir: -1, cols: [{ key: 'act', label: 'Action', sortable: false, render: r => rowIcons([{ ic: 'trash', t: 'Delete', act: 'clDel', data: { id: r.id }, cls: 'del' }]) }, { key: 'date', label: 'Date', text: r => r.date, render: r => fmtDT(r.date) }, { key: 'type', label: 'Type', render: r => esc(r.type) }, { key: 'note', label: 'Note', render: r => esc(r.note) }, { key: 'by', label: 'Entered by', render: r => esc((byId(DB.users, r.by) || {}).name || '') }], rows: DB.commLog.filter(x => x.pid === pt.id) }));
    return pageHead('Patient Communication Log', 'Summary') + `<div class="bar"><h2>${ic('user')} ${esc(ptName(pt))}</h2><button class="btn btn-add" data-act="clAdd" data-pid="${pt.id}">${ic('plus')} Add</button><button class="btn btn-back" data-act="clBack">${ic('back')} Back</button></div>${tbl}`;
  },
};
ACT.clBack = () => go('commlog');
ACT.clAdd = el => { const m = ctxNew({ n: { type: 'Phone call', note: '' } }); modal({ title: 'Add to Communication Log', ctx: m, size: 'sm', body: c => fg('Type', sel(c, 'n.type', ['Phone call', 'Email', 'Visit', 'Fax', 'Other'], { blank: false })) + fg('Note (do not put SSN or Medicare numbers here)', txt(c, 'n.note', { rows: 4 })), buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { if (!m.n.note.trim()) { toast('Write a note.', 'err'); return false; } DB.commLog.push({ id: uid('CL'), pid: el.dataset.pid, date: nowIso(), type: m.n.type, note: m.n.note.trim(), by: DB.session.userId }); save(); track('commlog:add'); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
ACT.clDel = el => needApproval({ roles: ['Administrator'], what: 'Delete a communication log entry', rule: 'Never delete without the Administrator authorizing it in writing.', who: 'Administrator', ref: 'R2', go: () => { DB.commLog = DB.commLog.filter(x => x.id !== el.dataset.id); save(); refresh(); } });

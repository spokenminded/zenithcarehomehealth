'use strict';
/* =====================================================================================================
   Documents: Electronic Health Records, General Form (Orders & Docs), 485 and Face-to-Face, All Documents,
   and the simple forms (allergy, med profile, missed visit and so on)
   ===================================================================================================== */
function practiceDocsFor(pt) {
  const nm = ptName(pt), dob = fmtD(pt.dob), t = todayIso(); const d1 = addDays(t, -1), d12 = addDays(t, -12), dold = addDays(t, -152);
  const other = DB.patients.find(p => p.id !== pt.id && !p.draft);
  return [
    { label: 'Referral (signed)', kind: 'referral', o: { name: nm, dob, date: d1 }, file: 'referral_' + pt.last.toLowerCase() + '.svg' },
    { label: 'Physician order (signed and dated)', kind: 'order', o: { name: nm, dob, date: d1 }, file: 'order_' + pt.last.toLowerCase() + '.svg' },
    { label: 'Physician order (NOT signed)', kind: 'order_unsigned', o: { name: nm, dob, date: d1 }, file: 'order_unsigned_' + pt.last.toLowerCase() + '.svg' },
    { label: 'Face-to-face (encounter ' + fmtD(d12) + ', signed)', kind: 'f2f', o: { name: nm, dob, date: d1, enc: d12 }, file: 'f2f_' + pt.last.toLowerCase() + '.svg' },
    { label: 'Face-to-face (encounter ' + fmtD(dold) + ': too old)', kind: 'f2f_old', o: { name: nm, dob, date: d1, enc: dold }, file: 'f2f_old_' + pt.last.toLowerCase() + '.svg' },
    { label: 'Insurance card copy', kind: 'insurance', o: { name: nm, dob, date: d1, member: pt.medicare || 'PRACTICE-0001' }, file: 'insurance_' + pt.last.toLowerCase() + '.svg' },
    { label: 'Face sheet', kind: 'facesheet', o: { name: nm, dob, date: d1, addr: [pt.addr1, pt.city, pt.state, pt.zip].join(' ') }, file: 'facesheet_' + pt.last.toLowerCase() + '.svg' },
    other ? { label: 'TRAP: a referral for a DIFFERENT patient (' + ptName(other) + ')', kind: 'wrong', o: { name: ptName(other), dob: fmtD(other.dob), date: d1 }, file: 'referral_' + other.last.toLowerCase() + '.svg', meta: { name: ptName(other) } } : null,
  ].filter(Boolean).map(x => Object.assign(x, { meta: x.meta || { name: nm }, url: () => docUrl(x.kind, x.o) }));
}
function recNameCheck(title, pt) {
  const t = (title || '').trim(); if (!t) return null;
  const re = /^([A-Za-z'\-]+)_([A-Za-z'\-]+)_([A-Za-z0-9]+)_(\d{8})$/; const m = re.exec(t);
  if (!m) return { ok: false, msg: 'Zenith standard: LAST_FIRST_DocumentType_MMDDYYYY (example ' + pt.last + '_' + pt.first + '_Referral_09302026)' };
  if (m[1].toUpperCase() !== pt.last.toUpperCase() || m[2].toUpperCase() !== pt.first.toUpperCase()) return { ok: false, msg: 'The name in the Record Name is not this patient (' + pt.last + ', ' + pt.first + '). Check before you save.' };
  const d = m[4]; const mo = +d.slice(0, 2), da = +d.slice(2, 4); if (mo < 1 || mo > 12 || da < 1 || da > 31) return { ok: false, msg: 'The date part should be MMDDYYYY.' };
  if (/\d{9}/.test(t) || /ssn|medicare|medicaid/i.test(t)) return { ok: false, msg: 'Never put an SSN, Medicare or Medicaid number in a Record Name.' };
  return { ok: true, msg: 'Matches the Zenith naming pattern.' };
}

/* ---------------------------------------------------------------- Electronic Health Records */
ROUTES.ehr = { render(c) { return admSearchPage(c, 'Electronic Health Records', 'ehrlist', { sub: 'Patient Admission Search' }); } };
ROUTES.ehrlist = {
  render(c, p) {
    const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return notice('Not found.', 'err');
    if (c.all === undefined) { c.all = true; c.folder = ''; }
    const rows = () => DB.docs.filter(d => d.pid === pt.id && !d.deleted && (c.all || !c.folder || d.folder === c.folder));
    const tbl = DT(c, 'docs', () => ({ sort: 'created', dir: -1, noTop: false,
      cols: [{ key: 'act', label: 'Action', sortable: false, blue: true, render: r => rowIcons([{ ic: 'eye', t: 'Open', act: 'docView', data: { id: r.id }, cls: 'view' }, { ic: 'edit', t: 'Edit', act: 'docEdit', data: { id: r.id } }, { ic: 'trash', t: 'Delete', act: 'docDel', data: { id: r.id }, cls: 'del' }]) },
        { key: 'title', label: 'Title', render: r => `<a data-act="docView" data-id="${r.id}">${esc(r.title)}</a>` }, { key: 'created', label: 'Created Date', blue: true, text: r => r.created, render: r => fmtD(r.created) }, { key: 'folder', label: 'Folder Name', render: r => esc(r.folder) }],
      rows: rows() }));
    return pageHead('Electronic Health Records', 'Summary') + `<div class="bar"><h2>${ic('user')} ${esc(ptName(pt))}</h2><button class="btn btn-add" data-act="docAdd" data-pid="${pt.id}">${ic('plus')} Add</button><button class="btn btn-back" data-act="ehrBack">${ic('back')} Back</button></div>
      <div class="flex" style="align-items:flex-end"><div style="width:360px">${fg('Folder:', s2(c, 'folder', 'ptFolders', { ph: 'Enter Folder name', rr: 1 }))}</div><label class="chk" style="margin-bottom:12px"><input type="checkbox" ${battr(c, 'all')} data-rr="1"${c.all ? ' checked' : ''}> All</label></div>${tbl}${gotoBtn()}${gotoPanel(c, a)}`;
  },
  mount(c) { if (c._lastFolder !== c.folder) { c._lastFolder = c.folder; } },
};
// choosing a folder unchecks All; checking All clears the folder
const _origS2 = S2SRC.ptFolders; S2SRC.ptFolders.onpick = (c, v, path) => { if (path === 'folder') { c.all = !v; } };
document.addEventListener('change', e => { const t = e.target; if (t.dataset && t.dataset.b === 'all' && CTX[t.dataset.c] && CTX[t.dataset.c].route === 'ehrlist') { const c = CTX[t.dataset.c]; if (c.all) c.folder = ''; } }, true);
ACT.ehrBack = () => go('ehr');
ACT.docView = el => { const d = byId(DB.docs, el.dataset.id); track('doc:open'); viewFile(d); };
ACT.docAdd = el => docUploadModal({ kind: 'patient', pid: el.dataset.pid });
ACT.docEdit = el => { const d = byId(DB.docs, el.dataset.id); const m = ctxNew({ t: d.title, f: d.folder, cm: d.comment }); modal({ title: 'Electronic Health Record', ctx: m, size: 'lg', body: c => fg('Record Name', inp(c, 't')) + fg('Folder', s2(c, 'f', 'ptFolders', { ph: 'Enter Folder name' })) + fg('Comments', txt(c, 'cm', { rows: 3 })), buttons: [{ label: 'Save & Close', cls: 'btn-ok', click: () => { if (!m.t.trim() || !m.f) { toast('Record Name and Folder are required.', 'err'); return false; } d.title = m.t.trim(); d.folder = m.f; d.comment = m.cm; save(); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
ACT.docDel = el => needApproval({ roles: ['Administrator'], what: 'Delete a document', rule: 'Delete or Undelete Documents only with the Administrator\'s written authorization. A document in the wrong chart: STOP, do not delete, tell the Administrator now.', who: 'Administrator, in writing', ref: 'R2', go: () => confirmBox('Delete document?', '<p>The document moves to Undelete Documents (Administrator tool).</p>', () => { const d = byId(DB.docs, el.dataset.id); d.deleted = true; d.deletedBy = DB.session.userId; d.deletedAt = nowIso(); DB.deleted.push({ kind: 'patient', id: d.id }); save(); simLog('override', 'Deleted a document (practice): ' + d.title); refresh(); }, { yes: 'Delete', no: 'Cancel' }) });

// upload window for patient and staff documents (the staff version has its own folders)
function docUploadModal(o) {
  const staff = o.kind === 'staff'; const pt = staff ? null : P(o.pid); const who = staff ? ST(o.sid) : pt;
  const m = ctxNew({ rec: '', folder: '', cm: '', file: null, o });
  const mod = modal({ title: staff ? 'Electronic Staff Record' : 'Electronic Health Record', ctx: m, size: 'lg', noFocus: true,
    body: c => `<div class="fg"><input type="file" data-file="1" style="padding:4px"> <span class="small">${c.file ? esc(c.file.name) + ' (' + fmtSize(c.file.size) + ')' : 'No file chosen'}</span> <a data-act="docPractice">or use a simulator practice document</a></div>
      ${fg('Record Name', inp(c, 'rec', { id: 'recname' }) + (staff ? '' : recHint(c, pt)))}${fg('Folder', s2(c, 'folder', staff ? 'stFolders' : 'ptFolders', { ph: 'Enter Folder name' }))}${fg('Comments', txt(c, 'cm', { rows: 3 }))}
      <p class="small">The file stays in this browser. In the practice copy nothing is uploaded anywhere.</p>`,
    buttons: [{ label: 'Save & Close', cls: 'btn-ok', click: (mm) => {
      if (!m.file) { toast('Choose a file first.', 'err'); return false; } if (!m.rec.trim()) { toast('Record Name is required.', 'err'); $('#recname') && $('#recname').classList.add('bad'); return false; } if (!m.folder) { toast('Choose a Folder.', 'err'); return false; }
      const store = staff ? who.docs : DB.docs; const dup = store.find(d => (staff || d.pid === pt.id) && !d.deleted && d.title === m.rec.trim());
      const doIt = () => {
        const fileId = m.file.url ? putFile(m.file.url) : '';
        const rec = { id: uid('D'), pid: staff ? undefined : pt.id, title: m.rec.trim(), folder: m.folder, created: todayIso(), comment: m.cm, fileName: m.file.name, fileSize: fmtSize(m.file.size), fileId, by: DB.session.userId, deleted: false, meta: m.file.meta || null };
        store.push(rec); save(); track(staff ? 'staffdoc:upload' : 'ehr:upload'); simLog('info', 'Uploaded "' + rec.title + '" to ' + (staff ? stName(who) : ptName(pt)) + ' / ' + rec.folder);
        if (!staff && m.file.meta && m.file.meta.name && m.file.meta.name !== ptName(pt)) { simLog('override', 'WRONG CHART: the file shows ' + m.file.meta.name + ' but it was uploaded to ' + ptName(pt)); toast('Coach: this file names ' + m.file.meta.name + ', but you uploaded it to ' + ptName(pt) + '. In real work STOP and tell the Administrator now (do not delete).', 'sim'); }
        mod.close(); refresh(); toast('Uploaded.', 'ok');
      };
      if (dup) { confirmBox('Possible duplicate', '<p>A document named <b>' + esc(dup.title) + '</b> is already in this list. Zenith rule: no duplicate documents.</p>', doIt, { yes: 'Upload anyway (practice)', no: 'Cancel' }); return false; }
      doIt(); return false; } }, { label: 'Cancel', cls: 'btn-del' }] });
  return mod;
}
function recHint(c, pt) { const r = recNameCheck(c.rec, pt); if (!r) return '<div class="small">Zenith standard: LAST_FIRST_DocumentType_MMDDYYYY</div>'; return `<div class="small" style="color:${r.ok ? '#3c763d' : '#a94442'}">${r.ok ? '&#10003; ' : '&#9888; '}${esc(r.msg)}</div>`; }
document.addEventListener('change', e => {
  const t = e.target; if (!t.dataset || !t.dataset.file) return; const c = ctxOf(t); if (!c) return;
  readFile(t.files && t.files[0], f => { c.file = f; if (f && !c.rec) c.rec = ''; if (c._modal) c._modal.rerender(); });
});
document.addEventListener('input', e => { const t = e.target; if (t.id === 'recname') { const c = ctxOf(t); if (c && c.o && c.o.kind === 'patient') { const hint = t.parentNode.querySelector('.small'); const r = recNameCheck(c.rec, P(c.o.pid)); if (hint && r) { hint.style.color = r.ok ? '#3c763d' : '#a94442'; hint.innerHTML = (r.ok ? '&#10003; ' : '&#9888; ') + esc(r.msg); } } } });
ACT.docPractice = el => { const c = ctxOf(el); const pt = c.o.kind === 'patient' ? P(c.o.pid) : null; if (!pt) { const sd = [{ label: 'New hire paperwork (practice)', kind: 'facesheet' }, { label: 'License copy (practice)', kind: 'insurance' }]; popMenu(el, sd.map(x => ({ label: x.label, ic: 'doc', run: () => { c.file = { name: x.label.replace(/\W+/g, '_') + '.svg', size: 3000, url: docUrl(x.kind, { name: stName(ST(c.o.sid)), dob: fmtD(ST(c.o.sid).dob) }), meta: null }; c._modal.rerender(); } }))); return; }
  popMenu(el, practiceDocsFor(pt).map(x => ({ label: x.label, ic: 'doc', run: () => { c.file = { name: x.file, size: 3200, url: x.url(), meta: x.meta }; c._modal.rerender(); } }))); };

/* ---------------------------------------------------------------- General Form (Orders & Docs) */
ROUTES.orders = { render(c) { return admSearchPage(c, 'General Form (Orders & Docs)', 'orders-pt', { sub: 'Patient Admission Search' }); } };
ROUTES['orders-pt'] = {
  render(c, p) {
    const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return notice('Not found.', 'err');
    const tbl = DT(c, 'ord', () => ({ sort: 'date', dir: -1, firstLast: false,
      cols: [{ key: 'act', label: 'Action', sortable: false, blue: true, render: r => rowIcons([{ ic: 'eye', t: 'View', act: 'ordView', data: { id: r.id }, cls: 'view' }, { ic: 'edit', t: 'Edit', act: 'ordEdit', data: { id: r.id } }, { ic: 'trash', t: 'Delete', act: 'ordDel', data: { id: r.id }, cls: 'del' }]) },
        { key: 'date', label: 'Order Date', blue: true, text: r => r.date, render: r => fmtD(r.date) }, { key: 'title', label: 'Title', render: r => `<a data-act="ordView" data-id="${r.id}">${esc(r.title)}</a>` }, { key: 'sent', label: 'Sent Date', text: r => r.sent || '', render: r => fmtD(r.sent) },
        { key: 'received', label: 'Received Date', text: r => r.received || '', render: r => fmtD(r.received) }, { key: 'cg', label: 'Caregiver', text: r => stName(ST(r.cgId)), render: r => esc(stName(ST(r.cgId))) }, { key: 'status', label: 'Status', render: r => tagFor(ordStatus(r)) }, { key: 'signed', label: 'Signed', text: r => (r.signed ? 'Yes' : 'No'), render: r => (r.signed ? 'Yes' : '<span style="color:#c0392b">No</span>') }],
      rows: DB.orders.filter(o => o.pid === pt.id) }));
    return pageHead('General Form (Orders & Docs)', 'Summary') + `<div class="bar"><h2>${ic('user')} ${esc(ptName(pt))}</h2><button class="btn btn-add" data-act="ordAdd" data-pid="${pt.id}">${ic('plus')} Add</button><button class="btn btn-back" data-act="ordBack">${ic('back')} Back</button><button class="btn btn-or" data-act="ordDates" data-pid="${pt.id}">${ic('doc')} Edit Sent/Received Date</button></div>${tbl}${gotoBtn()}${gotoPanel(c, a)}`;
  },
};
function ordStatus(o) { return o.signed && o.received ? 'Completed' : 'Pending'; }
ACT.ordBack = () => go('orders');
ACT.ordView = el => { const o = byId(DB.orders, el.dataset.id); track('order:view'); modal({ title: esc(o.title), size: 'lg', body: `<div class="kv"><div>Patient</div><div>${esc(ptName(P(o.pid)))}</div><div>Order date</div><div>${fmtD(o.date)}</div><div>Physician</div><div>${esc(physName(o.physId))}</div><div>Sent</div><div>${fmtD(o.sent) || 'not sent'}</div><div>Received</div><div>${fmtD(o.received) || '<b style="color:#c0392b">not received</b>'}</div><div>Signed</div><div>${o.signed ? 'Yes' : '<b style="color:#c0392b">No</b>'}</div></div><hr class="hr"><div style="white-space:pre-wrap">${esc(o.text)}</div>`, buttons: [{ label: 'Close', cls: 'btn-close' }] }); };
ACT.ordAdd = el => orderModal(el.dataset.pid, null); ACT.ordEdit = el => orderModal(byId(DB.orders, el.dataset.id).pid, el.dataset.id);
ACT.ordDel = el => needApproval({ roles: ['Administrator'], what: 'Delete an order', rule: 'Never delete a clinical document unless the Administrator authorizes it in writing.', who: 'Administrator', ref: 'R2', go: () => confirmBox('Delete order?', '<p>Delete this order?</p>', () => { DB.orders = DB.orders.filter(o => o.id !== el.dataset.id); save(); refresh(); }, { yes: 'Delete', no: 'Cancel' }) });
function orderModal(pid, oid) {
  const ex = oid ? byId(DB.orders, oid) : null; const pt = P(pid);
  const open = () => { const adm = admOf(pid); const m = ctxNew({ o: ex ? { date: fmtD(ex.date), title: ex.title, text: ex.text, physId: ex.physId, cgId: ex.cgId, sent: fmtD(ex.sent), received: fmtD(ex.received), signed: ex.signed } : { date: fmtD(todayIso()), title: '', text: '', physId: adm ? adm.physId : '', cgId: '', sent: '', received: '', signed: false } });
    const mod = modal({ title: ex ? 'Order' : 'Add Order', ctx: m, size: 'lg', body: c => `<div class="row c2">${fg('Order Date', dp(c, 'o.date'), { req: 1 })}${fg('Title', inp(c, 'o.title'), { req: 1 })}${fg('Physician', s2(c, 'o.physId', 'physicians', { ph: 'Enter Physician Name' }))}${fg('Caregiver', s2(c, 'o.cgId', 'caregivers', { ph: 'Enter Caregiver' }))}${fg('Sent Date', dp(c, 'o.sent'))}${fg('Received Date', dp(c, 'o.received'))}</div>${fg('Order (what is ordered)', txt(c, 'o.text', { rows: 5 }), { req: 1 })}${chk(c, 'o.signed', 'Signed by the physician')}`,
      buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { const d = parseD(m.o.date); if (!d || !m.o.title.trim() || !m.o.text.trim()) { toast('Order date, Title and the order text are required.', 'err'); return false; }
        const rec = { id: ex ? ex.id : uid('OR'), pid, date: d, title: m.o.title.trim(), text: m.o.text, sent: parseD(m.o.sent) || '', received: parseD(m.o.received) || '', cgId: m.o.cgId, physId: m.o.physId, signed: !!m.o.signed, by: DB.session.userId, status: '' };
        if (ex) Object.assign(ex, rec); else DB.orders.push(rec); save(); track('order:saved'); simLog('info', 'Saved order for ' + ptName(pt)); refresh(); toast('Saved.', 'ok'); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
  if (roleIs('DON', 'Nurse')) open(); else needApproval({ roles: [], what: 'Create or change a clinical order', rule: 'Office staff do not create clinical orders. Clinical staff create orders. Office staff check that they are present, sent, received and signed.', who: 'DON or the clinician', ref: 'O7', go: open });
}
ACT.ordDates = el => needApproval({ roles: ['DON'], what: 'Edit Sent/Received Date', rule: 'Do not use Edit Sent/Received Date unless the DON or Administrator told you to.', who: 'DON or Administrator', ref: 'O7', go: () => {
  const list = DB.orders.filter(o => o.pid === el.dataset.pid); const m = ctxNew({ rows: list.map(o => ({ id: o.id, title: o.title, sent: fmtD(o.sent), received: fmtD(o.received) })) });
  modal({ title: 'Edit Sent/Received Date', ctx: m, size: 'lg', body: c => `<table class="t"><thead><tr><th>Order</th><th>Sent Date</th><th>Received Date</th></tr></thead><tbody>${c.rows.map((r, i) => `<tr><td>${esc(r.title)}</td><td>${dp(c, 'rows.' + i + '.sent')}</td><td>${dp(c, 'rows.' + i + '.received')}</td></tr>`).join('') || '<tr><td colspan="3" class="none">No orders</td></tr>'}</tbody></table>`, buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { m.rows.forEach(r => { const o = byId(DB.orders, r.id); o.sent = parseD(r.sent) || ''; o.received = parseD(r.received) || ''; }); save(); simLog('info', 'Edited order sent/received dates'); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] });
} });

/* ---------------------------------------------------------------- 485 Certification and Plan of Care, and the Face-to-Face window */
ROUTES.f485 = { render(c) { return admSearchPage(c, '485 - Certification and Plan of Care', 'f485-pt', { sub: 'Patient Admission Search' }); } };
ROUTES['f485-pt'] = {
  render(c, p) {
    const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return notice('Not found.', 'err');
    const tbl = DT(c, 'f485', () => ({ sort: 'from', dir: -1, firstLast: false,
      cols: [{ key: 'act', label: 'Action', sortable: false, blue: true, render: r => `<div style="min-width:170px">${rowIcons([{ ic: 'edit', t: 'Edit', act: 'f485Edit', data: { id: r.id }, cls: 'green' }, { ic: 'trash', t: 'Delete', act: 'f485Del', data: { id: r.id }, cls: 'del' }, { ic: 'print', t: 'Print', act: 'f485Print', data: { id: r.id }, cls: 'print' }, { ic: 'doc', t: 'Word', act: 'f485Print', data: { id: r.id }, cls: 'word' }, { ic: 'doc', t: 'PDF', act: 'f485Print', data: { id: r.id }, cls: 'pdf' }, { ic: 'eye', t: 'View', act: 'f485View', data: { id: r.id }, cls: 'view' }, { ic: 'clip', t: 'Attach to AloraMail', act: 'f485Mail', data: { id: r.id }, cls: 'clip' }])}</div>` },
        { key: 'from', label: 'Cert From', text: r => r.from, render: r => fmtD(r.from) }, { key: 'to', label: 'Cert Through', text: r => r.to, render: r => fmtD(r.to) }, { key: 'sent', label: 'Sent Date', text: r => r.sent || '', render: r => fmtD(r.sent) }, { key: 'recd', label: 'Recd. Date', text: r => r.recd || '', render: r => fmtD(r.recd) }, { key: 'status', label: 'Status', render: r => esc(r.status) }],
      rows: DB.f485.filter(x => x.pid === pt.id) }));
    return pageHead('485 Certification & POC', 'Summary') + `<div class="bar" style="flex-wrap:wrap"><h2>${ic('user')} ${esc(ptName(pt))}</h2><div class="flex"><button class="btn btn-add" data-act="f485Add" data-aid="${a.id}">${ic('plus')} Add</button><button class="btn btn-back" data-act="f485Back">${ic('back')} Back</button><button class="btn btn-pink" data-act="f2fOpen" data-aid="${a.id}">F2F</button><button class="btn btn-gray dis" disabled>${ic('back')} Move to Other Admission</button><button class="btn btn-or" data-act="f485Dates" data-pid="${pt.id}">${ic('doc')} Edit Sent/Received Date</button></div><div style="flex-basis:100%"><button class="btn btn-blue" data-act="medSheet" data-aid="${a.id}">${ic('print')} Print Med Sheet</button></div></div>${tbl}${gotoBtn()}${gotoPanel(c, a)}`;
  },
};
ACT.f485Back = () => go('f485');
ACT.f485Print = el => { const r = byId(DB.f485, el.dataset.id); printPreview('485 Plan of Care', f485Html(r)); };
ACT.f485View = el => { const r = byId(DB.f485, el.dataset.id); modal({ title: '485 Certification &amp; POC (view only)', size: 'lg', body: `<span class="vo">View only mode</span><div class="mt">${f485Html(r)}</div>`, buttons: [{ label: 'Close', cls: 'btn-close' }] }); };
ACT.f485Mail = el => composeMail({ subject: '485 plan of care (practice)', body: '(attached 485)' });
ACT.medSheet = el => { const a = byId(DB.admissions, el.dataset.aid); printPreview('Medication Sheet', `<h2>Medication Sheet (practice)</h2><p>${esc(ptName(P(a.pid)))}</p><table class="t"><thead><tr><th>Medication</th><th>Dose</th><th>Frequency</th></tr></thead><tbody>${DB.forms.filter(f => f.pid === a.pid && f.type === 'med').map(f => `<tr><td>${esc(f.d.f1)}</td><td>${esc(f.d.f2)}</td><td>${esc(f.d.f3)}</td></tr>`).join('') || '<tr><td colspan="3">No medications entered (Med Profile)</td></tr>'}</tbody></table>`); };
function f485Html(r) { const pt = P(r.pid), a = admOf(r.pid); return `<h2>Home Health Certification and Plan of Care (practice)</h2><table class="t"><tbody><tr><td>Patient</td><td>${esc(ptName(pt))}</td><td>DOB</td><td>${fmtD(pt.dob)}</td></tr><tr><td>Certification period</td><td>${fmtD(r.from)} to ${fmtD(r.to)}</td><td>Physician</td><td>${esc(physName(a && a.physId))}</td></tr><tr><td>Diagnoses</td><td colspan="3">${esc((a ? a.diag : []).map(d => d.code + ' ' + d.desc).join('; ')) || '(none)'}</td></tr><tr><td>Orders</td><td colspan="3">${esc((r.data || {}).orders || '')}</td></tr><tr><td>Goals</td><td colspan="3">${esc((r.data || {}).goals || '')}</td></tr></tbody></table><p class="small">Sent: ${fmtD(r.sent) || '-'} &nbsp; Received: ${fmtD(r.recd) || '-'}</p>`; }
ACT.f485Add = el => {
  const a = byId(DB.admissions, el.dataset.aid); const open = () => { const cps = certPeriods(a); const last = DB.f485.filter(x => x.pid === a.pid).map(x => x.from).sort().pop(); const next = cps.find(x => !last || x.from > last) || cps[cps.length - 1];
    const m = ctxNew({ f: { from: fmtD(next.from), to: fmtD(next.to), orders: '', goals: '' } });
    modal({ title: 'Add 485 Certification', ctx: m, size: 'lg', body: c => `<div class="row c2">${fg('Cert From', dp(c, 'f.from'), { req: 1 })}${fg('Cert Through', dp(c, 'f.to'), { req: 1 })}</div>${fg('Orders for discipline and treatment', txt(c, 'f.orders', { rows: 4 }))}${fg('Goals', txt(c, 'f.goals', { rows: 3 }))}<p class="small">Cert periods are 60 days. Diagnoses and frequency come from the Admission.</p>`, buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { const f = parseD(m.f.from), t = parseD(m.f.to); if (!f || !t) { toast('Enter valid dates.', 'err'); return false; } DB.f485.push({ id: uid('CP'), pid: a.pid, from: f, to: t, sent: '', recd: '', status: 'In Use', data: { orders: m.f.orders, goals: m.f.goals } }); save(); track('f485:created'); simLog('info', 'Created 485 for ' + ptName(P(a.pid))); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
  if (roleIs('DON', 'Nurse')) open(); else needApproval({ roles: [], what: 'Create or change a 485 plan of care', rule: 'Clinical staff and the Administrator own the 485. Office staff review.', who: 'DON or the clinician', ref: 'O8', go: open });
};
ACT.f485Edit = el => { const r = byId(DB.f485, el.dataset.id); const open = () => { const m = ctxNew({ f: { orders: (r.data || {}).orders || '', goals: (r.data || {}).goals || '' } }); modal({ title: '485 Certification &amp; POC', ctx: m, size: 'lg', body: c => `<div class="kv"><div>Cert period</div><div>${fmtD(r.from)} to ${fmtD(r.to)}</div><div>Status</div><div>${esc(r.status)}</div></div>${fg('Orders for discipline and treatment', txt(c, 'f.orders', { rows: 4 }))}${fg('Goals', txt(c, 'f.goals', { rows: 3 }))}`, buttons: [{ label: 'Save', cls: 'btn-save', click: () => { r.data = { orders: m.f.orders, goals: m.f.goals }; save(); refresh(); } }, { label: 'Complete', cls: 'btn-ok', click: () => { r.data = { orders: m.f.orders, goals: m.f.goals }; r.status = 'Completed'; save(); track('f485:completed'); simLog('info', '485 marked Completed'); refresh(); } }, { label: 'Close', cls: 'btn-close' }] }); };
  if (roleIs('DON', 'Nurse')) open(); else needApproval({ roles: [], what: 'Edit a 485', rule: 'Clinical staff and the Administrator own the 485. Office staff review only.', who: 'DON or the clinician', ref: 'O8', go: open }); };
ACT.f485Del = el => needApproval({ roles: ['Administrator'], what: 'Delete a 485', rule: 'Never delete a clinical document without written Administrator authorization.', who: 'Administrator', ref: 'R2', go: () => confirmBox('Delete 485?', '<p>Delete this certification?</p>', () => { DB.f485 = DB.f485.filter(x => x.id !== el.dataset.id); save(); refresh(); }, { yes: 'Delete', no: 'Cancel' }) });
ACT.f485Dates = el => needApproval({ roles: ['DON'], what: 'Edit Sent/Received Date on the 485', rule: 'Do not use Edit Sent/Received Date unless the DON or Administrator told you to.', who: 'DON or Administrator', ref: 'O7', go: () => { const list = DB.f485.filter(o => o.pid === el.dataset.pid); const m = ctxNew({ rows: list.map(o => ({ id: o.id, label: fmtD(o.from) + ' - ' + fmtD(o.to), sent: fmtD(o.sent), recd: fmtD(o.recd) })) }); modal({ title: 'Edit Sent/Received Date', ctx: m, size: 'lg', body: c => `<table class="t"><thead><tr><th>Cert period</th><th>Sent</th><th>Received</th></tr></thead><tbody>${c.rows.map((r, i) => `<tr><td>${esc(r.label)}</td><td>${dp(c, 'rows.' + i + '.sent')}</td><td>${dp(c, 'rows.' + i + '.recd')}</td></tr>`).join('')}</tbody></table>`, buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { m.rows.forEach(r => { const o = byId(DB.f485, r.id); o.sent = parseD(r.sent) || ''; o.recd = parseD(r.recd) || ''; if (o.recd) o.status = 'Signed'; else if (o.sent && o.status !== 'Completed') o.status = 'Sent'; }); save(); refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); } });

// Face-To-Face Encounter window
ACT.f2fOpen = el => {
  const a = byId(DB.admissions, el.dataset.aid); track('f2f:opened'); const m = ctxNew({ type: '' });
  modal({ title: 'Face-To-Face Encounter', ctx: m, size: 'lg', body: c => `<div class="box"><h4>Encounter Type</h4>${['Home Health Certifying Physician', 'Hospital/Institutional Physician'].map(t => radio(c, 'type', t, t, { rr: 1 })).join('<br>')}</div>`,
    buttons: c => [{ label: 'Send Report as Fax', cls: 'btn-ok' + (m.type ? '' : ' dis'), dis: !m.type, click: () => { neverDo('Send Report as Fax', 'In the real Alora this faxes the Face-To-Face request to a real physician\'s fax number.', 'Zenith rule: never click Send Report as Fax or Send Fax while practicing. Only the Administrator or DON sends F2F requests.'); return false; } },
      { label: 'Run Report', cls: 'btn-gray' + (m.type ? '' : ' dis'), dis: !m.type, click: () => { track('f2f:report'); printPreview('Face-To-Face Encounter', f2fReportHtml(a, m.type)); return false; } }, { label: 'Close', cls: 'btn-del', click: () => { track('f2f:closed'); } }] });
};
function f2fReportHtml(a, type) { const pt = P(a.pid); const soc = DB.f485.filter(x => x.pid === a.pid).map(x => x.from).sort()[0] || a.admit; return `<h2>Face-To-Face Encounter (practice form)</h2><p><b>Encounter type:</b> ${esc(type)}</p><table class="t"><tbody><tr><td>Patient</td><td>${esc(ptName(pt))}</td><td>DOB</td><td>${fmtD(pt.dob)}</td></tr><tr><td>Start of care</td><td>${fmtD(soc)}</td><td>Allowed encounter window</td><td>${fmtD(addDays(soc, -90))} to ${fmtD(addDays(soc, 30))}</td></tr></tbody></table><p>Date of the encounter: ____________ &nbsp; Practitioner: ____________________</p><p>Clinical findings: ____________________________________________</p><p>Signature: ____________________ &nbsp; Date: __________</p>`; }

/* ---------------------------------------------------------------- All Documents (visits, notes, assessments, orders in one list) */
function allDocRows(a, cpKey) {
  const rows = []; const pid = a.pid; const cp = certPeriods(a).find(x => x.k === cpKey);
  const inCp = d => !cp || (d >= cp.from && d <= cp.to);
  DB.snNotes.filter(n => n.pid === pid).forEach(n => { const v = byId(DB.visits, n.visitId); const d = (v ? v.start : n.date).slice(0, 10); if (inCp(d)) rows.push({ id: n.id, kind: 'SN Note', start: v ? v.start : n.date + 'T00:00', end: v ? v.end : '', svc: v ? bcDesc(v.billingCode) : '', vstat: v ? vcode(v.status) : '', qa: n.qa === 'Completed' && n.status === 'Completed' ? 'Completed' : n.status === 'Completed' ? n.qa : 'In Use', cg: n.cgId }); });
  DB.assessments.filter(x => x.pid === pid && inCp(x.compDate)).forEach(x => rows.push({ id: x.id, kind: x.type === 'OASIS' ? 'OASIS' : x.type, start: x.compDate + 'T00:00', end: '', svc: 'Assessment', vstat: '', qa: x.qa, cg: '' }));
  DB.f485.filter(x => x.pid === pid && x.to >= (cp ? cp.from : '0') && x.from <= (cp ? cp.to : '9')).forEach(x => rows.push({ id: x.id, kind: '485', start: x.from + 'T00:00', end: x.to + 'T00:00', svc: 'Plan of Care', vstat: '', qa: x.status === 'Completed' || x.status === 'Signed' ? 'Completed' : 'In Use', cg: '' }));
  DB.orders.filter(x => x.pid === pid && inCp(x.date)).forEach(x => rows.push({ id: x.id, kind: 'Order', start: x.date + 'T00:00', end: '', svc: x.title, vstat: '', qa: ordStatus(x), cg: x.cgId }));
  DB.aideDocs.filter(x => x.pid === pid && inCp(x.from)).forEach(x => rows.push({ id: x.id, kind: x.kind === 'poc' ? 'Aide Plan of Care' : 'Aide Note', start: x.from + 'T00:00', end: x.to ? x.to + 'T00:00' : '', svc: 'Home Health Aide', vstat: '', qa: x.status, cg: x.cgId }));
  DB.visits.filter(v => v.pid === pid && !v.noteId && inCp(v.start.slice(0, 10)) && v.status !== 'A').forEach(v => rows.push({ id: v.id, kind: 'Visit', start: v.start, end: v.end, svc: bcDesc(v.billingCode), vstat: vcode(v.status), qa: '', cg: v.cgId }));
  return rows;
}
function vcode(s) { return { C: 'Completed', N: 'Not Completed', H: 'Hospitalized', O: 'On Hold', A: 'Cancelled', M: 'Missed' }[s] || 'Not Completed'; }
ROUTES.alldocs = {
  render(c, p) {
    const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return admSearchPage(c, 'All Documents', 'alldocs', {});
    c.cps = certPeriods(a); if (c.cp === undefined) { const cur = curCert(a); c.cp = cur ? cur.k : (c.cps[0] || {}).k; c.allp = false; }
    const rows = () => allDocRows(a, c.allp ? '' : c.cp).map(r => Object.assign(r, { sel: !!(c.sel || {})[r.id] }));
    const tbl = DT(c, 'ad', () => ({ sort: 'start', dir: -1, size: 100, sizes: [10, 25, 50, 100],
      cols: [{ key: 'chk', label: '', sortable: false, render: r => `<span class="tag g" style="border-radius:50%">+</span> <input type="checkbox" data-act="adSel" data-id="${r.id}"${r.sel ? ' checked' : ''}>` }, { key: 'kind', label: 'Document Type', render: r => esc(r.kind) }, { key: 'start', label: 'Start Date', blue: true, text: r => r.start, render: r => fmtD(r.start) + '<br>' + (/T00:00$/.test(r.start) ? '' : fmtT(r.start)) },
        { key: 'end', label: 'End Date', text: r => r.end || '', render: r => fmtD(r.end) + '<br>' + (!r.end || /T00:00$/.test(r.end) ? '' : fmtT(r.end)) }, { key: 'svc', label: 'Service Description', render: r => esc(r.svc) }, { key: 'vstat', label: 'Visit Status', render: r => esc(r.vstat) }, { key: 'qa', label: 'QA Status', render: r => esc(r.qa) }, { key: 'cg', label: 'Caregiver', text: r => stName(ST(r.cg)), render: r => esc(stName(ST(r.cg))) }],
      rows: rows() }));
    return pageHead('All Documents', 'Summary') + `<div class="bar"><h2>${ic('user')} ${esc(ptName(pt))}</h2><button class="btn btn-back" data-act="adBack">${ic('back')}</button><button class="btn btn-pink" data-act="adPrint">Batch Print</button><button class="btn btn-save" data-act="adFax">Batch Fax</button></div>
      <div class="flex" style="align-items:flex-end"><div style="width:380px">${fg('Select Certification Period', s2(c, 'cp', 'certPeriods', { ph: 'Select period', rr: 1 }))}</div><label class="chk" style="margin-bottom:12px"><input type="checkbox" ${battr(c, 'allp')} data-rr="1"${c.allp ? ' checked' : ''}> All</label></div>${tbl}${gotoBtn()}${gotoPanel(c, a)}`;
  },
};
S2SRC.certPeriods.label = (v, c) => { const x = (c.cps || []).find(y => y.k === v); return x ? x.l : v; };
ACT.adBack = () => history.back(); ACT.adSel = el => { const c = ctxOf(el); c.sel = c.sel || {}; c.sel[el.dataset.id] = el.checked; };
ACT.adPrint = el => { const c = ctxOf(el); const n = Object.keys(c.sel || {}).filter(k => c.sel[k]).length; printPreview('Batch Print', `<p>${n || 'All'} document(s) selected for printing (practice).</p>`); };
ACT.adFax = () => neverDo('Batch Fax', 'In the real Alora this faxes the selected documents to a real fax number.', 'Zenith rule: never click any fax button while practicing. Only the Administrator or DON sends faxes.');

/* ---------------------------------------------------------------- simple forms (Allergy, Med Profile, Missed Visit and so on) */
const FORMS = {
  allergy: { t: 'Allergy', f: [['f1', 'Allergen', 'text', 1], ['f2', 'Reaction', 'text'], ['f3', 'Severity', 'sel:Mild,Moderate,Severe']] },
  braden: { t: 'Braden Scale', f: [['f1', 'Total score (6 to 23)', 'text', 1], ['f2', 'Risk level', 'sel:No risk,Mild,Moderate,High,Very high'], ['f3', 'Notes', 'area']] },
  careteam: { t: 'Care Team', f: [['f1', 'Team member', 'staff', 1], ['f2', 'Role on the team', 'text'], ['f3', 'Notes', 'text']] },
  med: { t: 'Med Profile', f: [['f1', 'Medication', 'text', 1], ['f2', 'Dose and route', 'text'], ['f3', 'Frequency', 'text'], ['f4', 'Start date', 'date']] },
  missed: { t: 'Missed Visit', f: [['f1', 'Reason', 'reason', 1], ['f2', 'Visit date', 'date', 1], ['f3', 'Notes', 'area']] },
  msw: { t: 'MSW', f: [['f1', 'Visit type', 'text'], ['f2', 'Summary', 'area', 1]] }, ot: { t: 'OT Documents', f: [['f1', 'Document', 'text', 1], ['f2', 'Summary', 'area']] }, pt: { t: 'PT Documents', f: [['f1', 'Document', 'text', 1], ['f2', 'Summary', 'area']] }, st: { t: 'Speech Therapy', f: [['f1', 'Document', 'text', 1], ['f2', 'Summary', 'area']] },
  sup: { t: 'Supervisory Notes', f: [['f1', 'Supervised caregiver', 'staff', 1], ['f2', 'Findings', 'area', 1]] }, pocplus: { t: 'Plan of Care Plus', f: [['f1', 'Title', 'text', 1], ['f2', 'Plan details', 'area']] }, orderplus: { t: 'Order Plus (Verbal Order Plus)', f: [['f1', 'Verbal order text', 'area', 1], ['f2', 'Ordering physician', 'phys']] },
  tinetti: { t: 'Tinetti Assessment', f: [['f1', 'Score (0 to 28)', 'text', 1], ['f2', 'Fall risk', 'sel:Low,Moderate,High']] }, dc: { t: 'Discharge/Transfer Summary', f: [['f1', 'Discharge or transfer date', 'date', 1], ['f2', 'Reason', 'text', 1], ['f3', 'Summary', 'area']] },
  supply: { t: 'Supply/Modality Log', f: [['f1', 'Item', 'text', 1], ['f2', 'Quantity', 'text'], ['f3', 'Notes', 'text']] }, splpay: { t: 'Spl Pay Rate', f: [['f1', 'Special pay rate', 'text', 1], ['f2', 'Reason (written approval on file)', 'text', 1]] },
};
Object.keys(FORMS).forEach(k => {
  ROUTES['form-' + k] = {
    render(c, p) {
      const F = FORMS[k];
      if (!p.aid) return admSearchPage(c, F.t, 'form-' + k, { sub: 'Patient Admission Search' });
      const a = byId(DB.admissions, p.aid), pt = a && P(a.pid); if (!pt) return notice('Not found.', 'err');
      const tbl = DT(c, 'f', () => ({ sort: 'date', dir: -1, firstLast: false,
        cols: [{ key: 'act', label: 'Action', sortable: false, blue: true, render: r => rowIcons([{ ic: 'trash', t: 'Delete', act: 'formDel', data: { id: r.id }, cls: 'del' }]) }, { key: 'date', label: 'Date', blue: true, text: r => r.date, render: r => fmtD(r.date) }].concat(F.f.slice(0, 4).map(([fk, l, t]) => ({ key: fk, label: l, text: r => r.d[fk] || '', render: r => esc(t === 'staff' ? stName(ST(r.d[fk])) : t === 'phys' ? physName(r.d[fk]) : t === 'date' ? fmtD(r.d[fk]) : r.d[fk] || '') }))).concat([{ key: 'by', label: 'Entered by', text: r => (byId(DB.users, r.by) || {}).name || '', render: r => esc((byId(DB.users, r.by) || {}).name || '') }]),
        rows: DB.forms.filter(f => f.pid === pt.id && f.type === k) }));
      return pageHead(F.t, 'Summary') + `<div class="bar"><h2>${ic('user')} ${esc(ptName(pt))}</h2><button class="btn btn-add" data-act="formAdd" data-k="${k}" data-pid="${pt.id}">${ic('plus')} Add</button><button class="btn btn-back" data-act="formBack" data-k="${k}">${ic('back')} Back</button></div>${stub('This form was not photographed in the manual. It is a plain practice list so you can click through the menu.')}${tbl}${gotoBtn()}${gotoPanel(c, a)}`;
    },
  };
});
ACT.formBack = el => go('form-' + el.dataset.k);
ACT.formDel = el => needApproval({ roles: ['Administrator'], what: 'Delete an entry', rule: 'Never delete without written Administrator authorization.', who: 'Administrator', ref: 'R2', go: () => { DB.forms = DB.forms.filter(f => f.id !== el.dataset.id); save(); refresh(); } });
ACT.formAdd = el => {
  const F = FORMS[el.dataset.k]; const m = ctxNew({ d: {}, date: fmtD(todayIso()) });
  modal({ title: 'Add ' + F.t, ctx: m, size: 'lg', body: c => fg('Date', dp(c, 'date'), { req: 1 }) + F.f.map(([fk, l, t, req]) => fg(l, t === 'area' ? txt(c, 'd.' + fk, { rows: 3 }) : t === 'date' ? dp(c, 'd.' + fk) : t === 'staff' ? s2(c, 'd.' + fk, 'staff', { ph: 'Select' }) : t === 'phys' ? s2(c, 'd.' + fk, 'physicians', { ph: 'Select' }) : t === 'reason' ? s2(c, 'd.' + fk, 'missedReasons', { ph: 'Select reason' }) : /^sel:/.test(t) ? sel(c, 'd.' + fk, t.slice(4).split(',')) : inp(c, 'd.' + fk), { req })).join(''),
    buttons: [{ label: 'Save', cls: 'btn-ok', click: () => { const d = parseD(m.date); if (!d) { toast('Enter a valid date.', 'err'); return false; } for (const [fk, l, t, req] of F.f) { if (req && !String(m.d[fk] || '').trim()) { toast(l + ' is required.', 'err'); return false; } }
      const doIt = () => { const dd = Object.assign({}, m.d); F.f.forEach(([fk, l, t]) => { if (t === 'date' && dd[fk]) dd[fk] = parseD(dd[fk]) || dd[fk]; }); DB.forms.push({ id: uid('FM'), pid: el.dataset.pid, type: el.dataset.k, date: d, d: dd, by: DB.session.userId }); save(); track('form:' + el.dataset.k); simLog('info', 'Saved ' + F.t); refresh(); toast('Saved.', 'ok'); };
      if (el.dataset.k === 'splpay') { needApproval({ roles: ['Administrator'], what: 'Add or change a special pay rate', rule: 'Pay rates change only with written approval from the Administrator.', who: 'Administrator, in writing', ref: 'H5, R2', go: doIt }); return; } doIt(); } }, { label: 'Cancel', cls: 'btn-del' }] });
};

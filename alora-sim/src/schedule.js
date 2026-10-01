'use strict';
/* =====================================================================================================
   Scheduling: Scheduler (month, week, day, cert period), Appointment Details, Batch Entry, Global Calendar,
   CareConnect Monitor, CareConnect Conflicts and the CareConnect page
   ===================================================================================================== */
const STATUS_LIST = [['N', 'Not Completed (N)'], ['H', 'Hospitalized (H)'], ['C', 'Completed (C)'], ['O', 'On Hold (O)'], ['A', 'Cancelled (A)'], ['M', 'Missed (M)']];
const WDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
function initials(name) { return String(name || '').split(/[ ,]+/).filter(Boolean).map(x => x[0]).join('').slice(0, 3); }
function ptInit(p) { return p ? (p.first[0] + p.last[0]) : ''; }
function stInit(s) { return s ? (s.first[0] + s.last[0]) : ''; }
function visitCls(v) { const s = visitStatus(v).label; if (s === 'Completed' || s === 'Clocked out') return 'g'; if (s === 'Delayed' || s.indexOf('Missed') === 0) return 'r'; if (s === 'In Progress') return 'y'; if (s === 'Cancelled') return 'gray'; if (s === 'Hospitalized' || s === 'On Hold') return 'p'; return 'b'; }
function overlapV(a1, a2, b1, b2) { return a1 < b2 && b1 < a2; }
function visitConflicts(v, exceptId) {
  const cg = [], pt = []; DB.visits.forEach(x => { if (x.id === exceptId || x.status === 'A' || x.status === 'M') return; if (!overlapV(v.start, v.end, x.start, x.end)) return; if (v.cgId && x.cgId === v.cgId) cg.push(x); else if (v.pid && x.pid === v.pid) pt.push(x); });
  return { cg, pt };
}
function freqParse(s) { const m = /^(\d+)w(\d+)$/i.exec(s || ''); return m ? { per: +m[1], weeks: +m[2] } : null; }
function discFor(v) { const s = ST(v.cgId); return s ? s.disc : ''; }
function credProblems(s) { const t = todayIso(); const out = []; CRED_ITEMS.forEach(([k, l]) => { const c = s.creds[k]; if (c && c.exp && c.exp < t) out.push(l + ' expired ' + fmtD(c.exp)); }); return out; }
function absenceOn(s, dayIso) { return (s.absences || []).find(a => a.from <= dayIso && dayIso <= (a.to || a.from)); }

/* ---------------------------------------------------------------- Scheduler page */
S2SRC.billingCodes.list = (q, c) => { const v = c && c.v; const st = v && v.cgId ? ST(v.cgId) : null; return DB.lists.billingCodes.filter(x => (x.code + ' ' + x.desc).toLowerCase().includes(q.toLowerCase()) && (!st || (v && v.showAll) || x.disc === st.disc || (st.disc === 'RN' && x.disc === 'LPN') || (st.disc === 'PTA' && x.disc === 'PT'))).map(x => ({ v: x.id, label: x.code + ' - ' + x.desc })); };
S2SRC.visitLoc = { label: v => v, list: (q, c) => { const pt = c.v && c.v.pid ? P(c.v.pid) : null; const o = ["Patient's home"].concat(pt ? (pt.altLocs || []).map(a => a.type + ': ' + a.addr) : []); return o.filter(x => x.toLowerCase().includes(q.toLowerCase())).map(x => ({ v: x, label: x })); } };
const LABEL_MODES = [['initials', 'Time and initials'], ['patient', 'Time and patient'], ['caregiver', 'Time and caregiver'], ['code', 'Time and billing code']];
function evLabel(c, v) { const a = fmtShortT(v.start) + ' - ' + fmtShortT(v.end); const pt = P(v.pid), cg = ST(v.cgId); const m = c.label; if (m === 'patient') return a + ' ' + ptName(pt); if (m === 'caregiver') return a + ' ' + stName(cg); if (m === 'code') return a + ' ' + ((byId(DB.lists.billingCodes, v.billingCode) || {}).code || ''); return a + ' ' + (c.pid && !c.glob ? stInit(cg) : ptInit(pt)); }
function schedVisits(c) {
  return DB.visits.filter(v => (!c.pid || v.pid === c.pid) && (!c.cgId || v.cgId === c.cgId) && (!c.disc || discFor(v) === c.disc) && (c.show.cancelled || v.status !== 'A') && (c.show.missed || v.status !== 'M') && (c.show.hold || (v.status !== 'H' && v.status !== 'O')));
}
function schedRender(c, p, glob) {
  if (!c.init) { c.init = 1; c.glob = glob; c.pid = p.pid || ''; c.cgId = p.cgId || ''; c.view = 'month'; c.mode = 'monthly'; c.cursor = todayIso(); c.label = 'initials'; c.show = { cancelled: true, missed: true, hold: true }; c.disc = ''; c.dispOpen = false; c.cpk = ''; }
  const adm = c.pid ? admOf(c.pid) : null, pt = c.pid ? P(c.pid) : null;
  const need = !glob && !c.pid && !c.cgId;
  c.cps = adm ? certPeriods(adm) : [];
  let body = '';
  if (need) body = `<p class="small" style="margin:30px 0">Select a Patient or Caregiver to view Appointments.</p>`;
  else body = schedView(c, adm);
  const top = `<div class="flex" style="align-items:flex-start;gap:26px;flex-wrap:wrap"><div style="width:300px"><div class="fg"><label>Patient</label>${s2(c, 'pid', 'patients', { ph: 'Enter Patient', rr: 1, clear: 1 })}${pt ? `<div class="small" style="margin-top:3px">Payer: <b>${esc(adm ? payerName((adm.ins[0] || {}).payer) : '')}</b></div><a data-act="viewFreq" data-pid="${pt.id}" class="small">View Frequency</a>` : ''}</div></div>
    <div style="width:260px"><div class="fg"><label>Caregiver</label>${s2(c, 'cgId', 'caregivers', { ph: 'Enter Caregiver', rr: 1, clear: 1 })}</div></div>${glob ? `<div style="width:160px">${fg('Discipline', sel(c, 'disc', DISCIPLINES.filter(d => d !== 'OFFICE'), { rr: 1, blank: 'All' }))}</div>` : ''}
    <div style="padding-top:20px"><button class="btn btn-blue" style="background:#3b8fd0" data-act="schedOptions">${ic('gear')} Options</button></div><div style="padding-top:10px;min-width:220px"><a data-act="dispTog" style="font:300 22px var(--font);color:#4a90c8">Display Options &#9662;</a>${c.dispOpen ? `<div class="box" style="margin-top:6px">${fg('Event label', sel(c, 'label', LABEL_MODES, { rr: 1, blank: false }))}</div>` : ''}</div></div>`;
  return `<div class="flex" style="align-items:baseline"><div class="grow">${pageHead(glob ? 'Global Calendar' : 'Scheduler', 'Calendar')}</div></div>${top}${body}${pt ? gotoBtn() + gotoPanel(c, adm) : gotoBtn()}`;
}
ROUTES.scheduler = { render(c, p) { return schedRender(c, p, false); } };
ROUTES.global = { render(c, p) { return schedRender(c, p, true); } };
ACT.dispTog = el => { const c = ctxOf(el); c.dispOpen = !c.dispOpen; refresh(); };
ACT.schedOptions = el => { const c = ctxOf(el); const m = ctxNew({ s: Object.assign({}, c.show) }); modal({ title: 'Calendar Options', ctx: m, size: 'sm', body: mc => `<p class="small">Choose which visits the calendar shows.</p>${chk(mc, 's.cancelled', 'Show Cancelled visits')}<br>${chk(mc, 's.missed', 'Show Missed visits')}<br>${chk(mc, 's.hold', 'Show Hospitalized and On Hold visits')}`, buttons: [{ label: 'OK', cls: 'btn-ok', click: () => { c.show = m.s; refresh(); } }, { label: 'Cancel', cls: 'btn-del' }] }); };
function schedView(c, adm) {
  const cur = c.cursor; const d = toDate(cur); const evs = schedVisits(c);
  let title = '', nav = '', grid = '';
  const mm = c.mode === 'cert' && adm;
  if (mm) {
    const cp = c.cps.find(x => x.k === c.cpk) || curCert(adm) || c.cps[0]; if (cp) { c.cpk = cp.k; title = fmtD(cp.from) + ' - ' + fmtD(cp.to); grid = monthGrid(c, evs, cp.from, cp.to); } else grid = '<p class="note warn">No cert period yet.</p>';
  } else if (c.view === 'month' || c.mode === 'cert') { title = MONTHS[d.getMonth()] + ' ' + d.getFullYear(); const first = isoD(new Date(d.getFullYear(), d.getMonth(), 1)); const last = isoD(new Date(d.getFullYear(), d.getMonth() + 1, 0)); grid = monthGrid(c, evs, first, last, true); }
  else if (c.view === 'week') { const s = addDays(cur, -d.getDay()); title = fmtD(s).slice(0, 5) + ' - ' + fmtD(addDays(s, 6)); grid = timeGrid(c, evs, s, 7); }
  else { title = DAYS[d.getDay()] + ', ' + MONTHS[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear(); grid = timeGrid(c, evs, cur, 1); }
  const mini = [0, 1].map(k => miniCal(c, new Date(d.getFullYear(), d.getMonth() + k, 1), evs)).join('');
  return `<div class="btngrp mt" style="margin-top:18px"><button class="${c.mode === 'monthly' ? 'on' : ''}" data-act="schedMode" data-m="monthly">Monthly View</button><button class="${c.mode === 'cert' ? 'on' : ''}" data-act="schedMode" data-m="cert">Cert Period View</button></div>
    <div class="cal-hd"><div class="flex"><div class="btngrp"><button data-act="schedNav" data-n="-1">&lt;</button><button data-act="schedNav" data-n="1">&gt;</button></div><button class="btn btn-gray" data-act="schedToday">today</button></div><h3>${esc(title)}</h3>${mm ? '<span></span>' : `<div class="btngrp">${['month', 'week', 'day'].map(v => `<button class="${c.view === v ? 'on' : ''}" data-act="schedView" data-v="${v}">${v}</button>`).join('')}</div>`}</div>
    <div class="flex" style="align-items:flex-start;gap:14px"><div class="grow" style="min-width:0;overflow:auto">${grid}</div><div style="width:190px" class="minical">${mini}</div></div>
    <div class="legend mt"><span><i style="background:#3a87ad"></i>Scheduled</span><span><i style="background:#3fae49"></i>Completed</span><span><i style="background:#e5a400"></i>In progress</span><span><i style="background:#d9534f"></i>Delayed or missed</span><span><i style="background:#999"></i>Cancelled</span><span><i style="background:#8e6cc0"></i>Hospitalized or on hold</span></div>`;
}
function monthGrid(c, evs, from, to, monthOnly) {
  const f = toDate(from), l = toDate(to); const start = addDays(from, -f.getDay()); const endD = addDays(to, 6 - l.getDay()); const weeks = [];
  for (let s = start; s <= endD; s = addDays(s, 7)) weeks.push(s);
  const t = todayIso();
  return `<table class="cal"><thead><tr>${DAYS.map(x => `<th>${x}</th>`).join('')}</tr></thead><tbody>${weeks.map(w => `<tr>${Array.from({ length: 7 }, (_, i) => { const day = addDays(w, i); const out = day < from || day > to; const list = out ? [] : evs.filter(v => v.start.slice(0, 10) === day).sort((a, b) => (a.start < b.start ? -1 : 1)); return `<td class="${out ? 'o' : ''}${day === t ? ' today' : ''}" data-act="calDay" data-d="${day}"><div class="dn">${out && monthOnly ? '<span style="color:#ccc">' + toDate(day).getDate() + '</span>' : toDate(day).getDate()}</div>${list.map(v => `<span class="ev ${visitCls(v)}" data-act="calEv" data-id="${v.id}" title="${esc(ptName(P(v.pid)) + ' with ' + stName(ST(v.cgId)) + ' (' + visitStatus(v).label + ')')}">${esc(evLabel(c, v))}</span>`).join('')}</td>`; }).join('')}</tr>`).join('')}</tbody></table>`;
}
function timeGrid(c, evs, startDay, n) {
  const H0 = 6, H1 = 21; const days = Array.from({ length: n }, (_, i) => addDays(startDay, i));
  let h = `<div class="wk" style="grid-template-columns:70px repeat(${n},1fr)"><div class="h"></div>${days.map(dd => `<div class="h">${DAYS[toDate(dd).getDay()]} ${fmtD(dd).slice(0, 5)}</div>`).join('')}`;
  for (let hr = H0; hr <= H1; hr++) {
    h += `<div class="tm">${hr % 12 || 12}${hr >= 12 ? 'p' : 'a'}</div>`;
    days.forEach(dd => {
      const cellEv = evs.filter(v => v.start.slice(0, 10) === dd && toDate(v.start).getHours() === hr);
      h += `<div class="cell" data-act="calSlot" data-d="${dd}" data-h="${hr}">${cellEv.map(v => { const mi = toDate(v.start).getMinutes(); const dur = Math.max(20, diffMin(v.end, v.start)); const cls = visitCls(v); const bg = { g: '#3fae49', r: '#d9534f', y: '#e5a400', gray: '#999', p: '#8e6cc0', b: '#3a87ad' }[cls]; return `<div class="evx" style="top:${mi / 60 * 30}px;height:${dur / 60 * 30 - 2}px;background:${bg}" data-act="calEv" data-id="${v.id}" title="${esc(ptName(P(v.pid)) + ' with ' + stName(ST(v.cgId)))}">${esc(evLabel(c, v))}</div>`; }).join('')}</div>`;
    });
  }
  return h + '</div>';
}
function miniCal(c, first, evs) {
  const y = first.getFullYear(), mo = first.getMonth(); const fd = first.getDay(), dim = new Date(y, mo + 1, 0).getDate(); let cells = DAYS.map(x => `<th>${x.slice(0, 2)}</th>`).join(''); let row = '<tr>' + cells + '</tr><tr>';
  for (let i = 0; i < fd; i++) row += '<td></td>';
  for (let dd = 1; dd <= dim; dd++) { const iso = y + '-' + pad(mo + 1) + '-' + pad(dd); const has = evs.some(v => v.start.slice(0, 10) === iso); row += `<td class="${iso === c.cursor ? 'cur' : ''}" data-act="miniGo" data-d="${iso}" style="cursor:pointer;${has ? 'font-weight:700;color:#2b7bb9' : ''}">${dd}</td>`; if ((fd + dd) % 7 === 0 && dd < dim) row += '</tr><tr>'; }
  return `<h5>${MONTHS[mo]} ${y}</h5><table>${row}</tr></table>`;
}
ACT.schedMode = el => { const c = ctxOf(el); c.mode = el.dataset.m; if (c.mode === 'cert') track('sched:cert'); refresh(); };
ACT.schedView = el => { const c = ctxOf(el); c.view = el.dataset.v; track('sched:' + c.view); refresh(); };
ACT.schedToday = el => { const c = ctxOf(el); c.cursor = todayIso(); c.cpk = ''; refresh(); };
ACT.schedNav = el => { const c = ctxOf(el); const n = +el.dataset.n; if (c.mode === 'cert' && c.cps.length) { const i = c.cps.findIndex(x => x.k === c.cpk); const j = Math.min(c.cps.length - 1, Math.max(0, i + n)); c.cpk = c.cps[j].k; } else if (c.view === 'month') { const d = toDate(c.cursor); c.cursor = isoD(new Date(d.getFullYear(), d.getMonth() + n, 1)); } else if (c.view === 'week') c.cursor = addDays(c.cursor, 7 * n); else c.cursor = addDays(c.cursor, n); refresh(); };
ACT.miniGo = el => { const c = ctxOf(el); c.cursor = el.dataset.d; refresh(); };
ACT.calDay = el => { const c = ctxOf(el); if (c.glob || !c.pid) { if (c.glob) { c.cursor = el.dataset.d; c.view = 'day'; refresh(); } else toast('Select a Patient first. A new visit belongs to one patient.', 'err'); return; } apptModal(c, null, { start: el.dataset.d + 'T08:00' }); };
ACT.calSlot = el => { const c = ctxOf(el); if (!c.pid) { toast(c.glob ? 'The global calendar is for looking. Open the Scheduler to add a visit.' : 'Select a Patient first. A new visit belongs to one patient.', 'err'); return; } apptModal(c, null, { start: el.dataset.d + 'T' + pad(+el.dataset.h) + ':00' }); };
ACT.calEv = el => { const c = ctxOf(el); track('sched:openvisit'); apptModal(c, el.dataset.id); };

/* View Frequency: ordered visits per week compared with scheduled visits */
ACT.viewFreq = el => {
  const adm = admOf(el.dataset.pid); const pt = P(adm.pid); track('sched:freq'); const rows = [];
  adm.freq.forEach(f => { const fp = freqParse(f.freq); if (!fp) return; for (let w = 0; w < fp.weeks; w++) { const ws = addDays(f.from, w * 7), we = addDays(ws, 6); const n = DB.visits.filter(v => v.pid === pt.id && v.status !== 'A' && discOf(v) === f.disc && v.start.slice(0, 10) >= ws && v.start.slice(0, 10) <= we).length; rows.push({ disc: f.disc, ws, we, ord: fp.per, n, past: we < todayIso() }); } });
  modal({ title: 'Frequency: ' + esc(ptName(pt)), size: 'lg', body: `<table class="t"><thead><tr><th>Discipline</th><th>Week</th><th>Ordered</th><th>Scheduled</th><th>Result</th></tr></thead><tbody>${rows.map(r => `<tr class="${r.n !== r.ord ? 'draft' : ''}"><td>${r.disc}</td><td>${fmtD(r.ws)} - ${fmtD(r.we)}</td><td>${r.ord}</td><td>${r.n}</td><td>${r.n === r.ord ? 'OK' : r.n < r.ord ? (r.past ? 'Missing ' + (r.ord - r.n) + ' (week is over)' : 'Needs ' + (r.ord - r.n) + ' more') : 'Over the order by ' + (r.n - r.ord)}</td></tr>`).join('') || '<tr><td colspan="5" class="none">No frequency on the admission</td></tr>'}</tbody></table><p class="small">Frequency comes from the Admission, Frequency tab (example 2w4). Schedule only what the physician ordered.</p>`, buttons: [{ label: 'Close', cls: 'btn-close' }] });
};
function discOf(v) { const s = ST(v.cgId); return s ? (s.disc === 'LPN' ? 'RN' : s.disc === 'PTA' ? 'PT' : s.disc) : ''; }

/* ---------------------------------------------------------------- Appointment Details */
function apptDefaults(c, d) { const adm = c.pid ? admOf(c.pid) : null; return { cgId: c.cgId || '', pid: c.pid || '', start: fmtDT(d.start), end: fmtDT(addMin(d.start, 60)), status: 'N', billing: '', billable: !(c.pid === 'P1'), showAll: false, tH: '', tM: '', oH: '', oM: '', miles: '', exp: '', cmtCg: '', dontValidate: false, qaMon: false, qaWhy: '', cmtAdmin: '', location: "Patient's home", missedReason: '', recur: { on: false, pattern: 'weekly', days: {}, until: '' } }; }
function apptNotices(m) {
  const v = m.v, out = []; const s = parseDT(v.start), e = parseDT(v.end); const cg = v.cgId ? ST(v.cgId) : null, pt = v.pid ? P(v.pid) : null, adm = v.pid ? admOf(v.pid) : null;
  if (s && s < nowIso()) out.push(['info', 'This appointment occurs in the past.']);
  if (s && e && e <= s) out.push(['err', 'Appt. End Time must be after Appt. Start Time.']);
  if (s && e && e > s) {
    const cf = visitConflicts({ start: s, end: e, cgId: v.cgId, pid: v.pid }, m.ex ? m.ex.id : '');
    if (cf.cg.length) out.push([v.dontValidate ? 'warn' : 'err', 'Time conflict: ' + stName(cg) + ' already has a visit with ' + ptName(P(cf.cg[0].pid)) + ' from ' + fmtT(cf.cg[0].start) + ' to ' + fmtT(cf.cg[0].end) + '.' + (v.dontValidate ? ' (Not checked because "Do not validate for Time Conflict" is on. Zenith rule: NEVER check it.)' : '')]);
    if (cf.pt.length) out.push(['warn', 'This patient already has a visit at this time with ' + stName(ST(cf.pt[0].cgId)) + ' (' + fmtT(cf.pt[0].start) + ' to ' + fmtT(cf.pt[0].end) + ').']);
    if (cg) { const ab = absenceOn(cg, s.slice(0, 10)); if (ab) out.push(['warn', stName(cg) + ' is marked absent on ' + fmtD(s) + ' (' + (ab.reason || 'absence') + ').']); const av = (cg.avail || {})[DAYS[toDate(s).getDay()]]; if (av && !av.on) out.push(['info', stName(cg) + ' is not available on ' + DAYS[toDate(s).getDay()] + '.']); else if (av && av.on && (fmtHM(s) < av.from || fmtHM(e) > av.to)) out.push(['info', stName(cg) + ' is usually available ' + av.from + ' to ' + av.to + '.']); }
  }
  if (cg) { const cp = credProblems(cg); if (cp.length) out.push(['warn', stName(cg) + ' has an expired credential: ' + cp.join('; ') + '. Tell HR before you schedule this person.']); if (pt && cg.covZips && cg.covZips.indexOf(pt.zip) < 0) out.push(['info', 'The patient zip code ' + pt.zip + ' is outside ' + stName(cg) + "'s coverage zip codes."]); }
  if (adm && cg && adm.disciplines.length && adm.disciplines.indexOf(discOf({ cgId: v.cgId })) < 0 && cg.disc !== 'OFFICE') out.push(['warn', 'The physician did not order ' + cg.disc + ' for this patient (Admission, Disciplines tab).']);
  if (adm && s && s.slice(0, 10) < adm.admit) out.push(['warn', 'The visit is before the Admit Date (' + fmtD(adm.admit) + ').']);
  if (adm && adm.status !== 'Admitted') out.push(['warn', 'This admission is ' + adm.status + '. Schedule only after the Administrator approves the admission.']);
  return out;
}
function fmtHM(iso) { return iso.slice(11, 16); }
function noticesHtml(list) { return list.map(([k, t]) => `<div class="note ${k === 'info' ? '' : k === 'err' ? 'err' : 'warn'}" style="${k === 'info' ? 'background:#d9edf7;border-color:#bce8f1;color:#31708f' : ''}"><span>${k === 'info' ? '&#9432; ' : '&#9888; '}${esc(t)}</span></div>`).join(''); }
function apptModal(pc, vid, d) {
  const ex = vid ? byId(DB.visits, vid) : null;
  const v0 = ex ? { cgId: ex.cgId, pid: ex.pid, start: fmtDT(ex.start), end: fmtDT(ex.end), status: ex.status, billing: ex.billingCode, billable: ex.billable, showAll: false, tH: (ex.travel || '').split(':')[0] || '', tM: (ex.travel || '').split(':')[1] || '', oH: (ex.overtime || '').split(':')[0] || '', oM: (ex.overtime || '').split(':')[1] || '', miles: ex.mileage || '', exp: ex.expenses || '', cmtCg: ex.comments || '', dontValidate: !!ex.dontValidate, qaMon: !!ex.qaMon, qaWhy: ex.qaWhy || '', cmtAdmin: ex.adminComments || '', location: ex.location || "Patient's home", missedReason: ex.missedReason || '', recur: { on: false, pattern: 'weekly', days: {}, until: '' } } : apptDefaults(pc, d);
  const m = ctxNew({ v: v0, ex, tab: 'appt', pc, orig: JSON.stringify(v0) });
  const mod = modal({ title: 'Appointment Details', ctx: m, size: 'lg', noFocus: true, noEsc: true,
    body: c => apptBody(c),
    mount: (c, mm) => { const upd = () => setTimeout(() => { const n = $('#appt-notices', mm.el); if (n) n.innerHTML = noticesHtml(apptNotices(c)); }, 0); mm.el.addEventListener('input', upd); mm.el.addEventListener('change', e => { upd(); const t = e.target; if (t && t.dataset && t.dataset.b === 'v.start') setTimeout(() => { const s = parseDT(c.v.start), e2 = parseDT(c.v.end); if (s && (!e2 || e2 <= s)) { c.v.end = fmtDT(addMin(s, 60)); const inp2 = $('[data-b="v.end"]', mm.el); if (inp2) inp2.value = c.v.end; upd(); } }, 0); }); },
    buttons: c => [{ label: 'Save and Close', cls: 'btn-ok', click: () => { apptSave(m, mod); return false; } }].concat(ex ? [{ label: 'Delete', cls: 'btn-del', click: () => { apptDelete(m, mod); return false; } }] : []).concat([{ label: 'Close', cls: 'btn-close', click: () => { if (JSON.stringify(m.v) !== m.orig) { confirmBox('Close without saving?', '<p>You changed this visit but did not save. Close anyway?</p>', () => mod.close(), { yes: 'Close anyway', no: 'Stay', kind: 'warn' }); return false; } } }]) });
  if (m.ex) track('visit:opened'); return mod;
}
function apptBody(c) {
  const v = c.v, pt = v.pid ? P(v.pid) : null, adm = v.pid ? admOf(v.pid) : null;
  const tabs = tabsHtml([{ k: 'appt', l: 'Appointment' }, { k: 'rec', l: 'Recurrence' }], c.tab, 'apTab');
  if (c.tab === 'rec') return tabs + `<div class="tabpane"><p class="note warn">Repeating visits need the DON's approval. Zenith rule: the DON or Administrator approves recurring visits.</p><div class="fg"><label class="chk"><input type="checkbox" data-act="recurTog"${v.recur.on ? ' checked' : ''}> Repeat this appointment</label></div>${v.recur.on ? `<div class="fg"><label>Repeat on</label><div class="chkbox">${WDAYS.map(d => `<label class="chk"><input type="checkbox" ${battr(c, 'v.recur.days.' + d)}${getp(c, 'v.recur.days.' + d) ? ' checked' : ''}> ${d}</label>`).join('')}</div></div>${fg('Repeat until', dp(c, 'v.recur.until'))}<p class="small">Each repeated visit uses the same caregiver, time of day, billing code and comments. Visits with a time conflict are skipped.</p>` : ''}</div>`;
  const fixed = (pt ? `<div class="small" style="margin:3px 0">Payer: <b>${esc(adm ? payerName((adm.ins[0] || {}).payer) : '')}</b></div><a data-act="apDayPt">Show all visits for Patient for this day</a><br><a data-act="apMap">Google Map to Patient's Home</a><br><a data-act="apFreq">View Frequency</a>` : '');
  return `${tabs}<div class="tabpane"><div id="appt-notices">${noticesHtml(apptNotices(c))}</div>
    <div class="row c2"><div>${fg('Caregiver', s2(c, 'v.cgId', 'caregivers', { ph: 'Enter Caregiver Name', rr: 1, clear: 1 }), { req: 1 })}<div class="small" style="line-height:1.9"><a data-act="apCare">Show Caregivers in Patient's Care Team</a><br><a data-act="apDayCg">Show all visits for Caregiver for this day</a><br><a data-act="apAvail">Show Available Caregivers</a><br><a data-act="apRegion">Show Caregivers in Patient's Region | Zip Code</a></div></div>
    <div>${fg('Patient', s2(c, 'v.pid', 'patients', { ph: 'Enter Patient', rr: 1, clear: 1 }), { req: 1 })}<div class="small" style="line-height:1.9">${fixed}</div></div>
    ${fg('Appt. Start Time:', dp(c, 'v.start', { time: true }), { req: 1 })}${fg('Appt. End Time:', dp(c, 'v.end', { time: true }), { req: 1 })}</div>
    <div class="sec" style="background:#428bca">Information needed to Save as Completed</div>
    <div class="row c2"><div class="box" style="margin-top:8px"><h4>Visit Status</h4><div class="chkbox" style="display:grid;grid-template-columns:1fr 1fr">${STATUS_LIST.map(([k, l]) => `<label class="chk"><input type="checkbox" data-act="apStatus" data-k="${k}"${v.status === k ? ' checked' : ''}> ${l}</label>`).join('')}</div>${v.status === 'M' || v.status === 'A' ? fg('Reason', s2(c, 'v.missedReason', 'missedReasons', { ph: 'Select reason' })) : ''}</div>
    <div><div class="fg">${chk(c, 'v.showAll', 'Show Billing Code for all Disciplines', { rr: 1 })}</div>${fg('Billing Code', s2(c, 'v.billing', 'billingCodes', { ph: 'Enter Billing Code' }), { req: 1 })}<div class="fg"><label class="chk"><input type="checkbox" data-act="apBillable" ${battr(c, 'v.billable')}${v.billable ? ' checked' : ''}> Billable</label></div></div></div>
    <div class="sec" style="background:#428bca">Optional</div>
    <div class="row c2"><div class="fg"><label>Travel Time</label><div class="flex">${inp(c, 'v.tH', { max: 2, ph: 'hh' })}:${inp(c, 'v.tM', { max: 2, ph: 'mm' })}</div></div><div class="fg"><label>Overtime</label><div class="flex">${inp(c, 'v.oH', { max: 2, ph: 'hh' })}:${inp(c, 'v.oM', { max: 2, ph: 'mm' })}</div></div>${fg('Mileage', inp(c, 'v.miles'))}${fg('Expenses', inp(c, 'v.exp'))}</div>
    ${fg('Comments (for caregiver view)', txt(c, 'v.cmtCg', { rows: 3 }))}
    <div class="fg"><label class="chk"><input type="checkbox" data-act="apDontVal" ${battr(c, 'v.dontValidate')}${v.dontValidate ? ' checked' : ''}> Do not validate for Time Conflict</label></div>
    <div class="fg">${chk(c, 'v.qaMon', 'Monitored for QA purposes', { rr: 1 })}${v.qaMon ? inp(c, 'v.qaWhy', { ph: 'Why is this visit monitored?' }) : ''}</div>
    ${fg('Comments (for administrative use only)', txt(c, 'v.cmtAdmin', { rows: 3 }))}
    <div class="box"><h4>Location</h4>${fg('Select Visit Location', s2(c, 'v.location', 'visitLoc', { ph: 'Enter Location' }))}</div></div>`;
}
ACT.apTab = el => { const m = ctxOf(el); m.tab = el.dataset.k; m._modal.rerender(); };
ACT.apStatus = el => {
  const m = ctxOf(el); const k = el.dataset.k; const set = () => { m.v.status = k; m._modal.rerender(); };
  if (!el.checked) { m.v.status = 'N'; m._modal.rerender(); return; }
  if (k === 'C') { el.checked = false; needApproval({ roles: ['Administrator', 'DON'], what: 'Mark a visit Completed in the Scheduler', rule: 'Clinicians complete visits (by clocking in and out and signing the note). Do not mark Visit Status Completed in the Scheduler.', who: 'DON or Administrator', ref: 'SC1', go: set }); return; }
  set();
};
ACT.apBillable = el => { const m = ctxOf(el); m.v.billable = el.checked; if (el.checked && m.v.pid === 'P1') { simLog('good', 'Billable checked on the practice patient (see warning)'); toast('Zenith rule: practice visits on JOHN DOE must have Billable UNCHECKED so nothing can be billed.', 'sim'); } };
ACT.apDontVal = el => {
  const m = ctxOf(el); if (!el.checked) { m.v.dontValidate = false; m._modal.rerender(); return; } el.checked = false;
  modal({ title: 'Zenith rule: NEVER check this box', kind: 'warn', size: 'sm', body: '<p><b>Do not validate for Time Conflict</b> hides a real double booking. A clinician cannot be in two homes at once.</p><p class="mt">If Alora shows a time conflict, STOP and ask the Administrator or DON.</p>', buttons: [{ label: 'Leave it unchecked (recommended)', cls: 'btn-ok', click: () => simLog('good', 'Left "Do not validate for Time Conflict" unchecked') }, { label: 'Check it anyway (practice)', cls: 'btn-or', click: () => { simLog('override', 'Checked "Do not validate for Time Conflict" (practice)'); m.v.dontValidate = true; m._modal.rerender(); } }] });
};
ACT.recurTog = el => { const m = ctxOf(el); if (!el.checked) { m.v.recur.on = false; m._modal.rerender(); return; } el.checked = false; needApproval({ roles: ['DON'], what: 'Create repeating (recurring) visits', rule: 'Repeating visits need the DON\'s approval.', who: 'DON or Administrator', ref: 'SC1', go: () => { m.v.recur.on = true; m._modal.rerender(); } }); };
ACT.apMap = () => alertBox("Map to the patient's home", '<p>The real Alora opens a map in a new window. The simulator loads no maps, so nothing leaves this page.</p>');
ACT.apFreq = el => { const m = ctxOf(el); if (m.v.pid) ACT.viewFreq({ dataset: { pid: m.v.pid } }); };
function dayList(title, list) { modal({ title, size: 'lg', z: 1100, body: `<table class="t"><thead><tr><th>Time</th><th>Patient</th><th>Caregiver</th><th>Status</th></tr></thead><tbody>${list.map(v => `<tr><td>${fmtT(v.start)} - ${fmtT(v.end)}</td><td>${esc(ptName(P(v.pid)))}</td><td>${esc(stName(ST(v.cgId)))}</td><td>${esc(visitStatus(v).label)}</td></tr>`).join('') || '<tr><td colspan="4" class="none">No visits that day</td></tr>'}</tbody></table>`, buttons: [{ label: 'Close', cls: 'btn-close' }] }); }
ACT.apDayPt = el => { const m = ctxOf(el); const s = parseDT(m.v.start); if (!m.v.pid || !s) return; dayList('Visits for ' + ptName(P(m.v.pid)) + ' on ' + fmtD(s), DB.visits.filter(v => v.pid === m.v.pid && v.start.slice(0, 10) === s.slice(0, 10))); };
ACT.apDayCg = el => { const m = ctxOf(el); const s = parseDT(m.v.start); if (!m.v.cgId || !s) { toast('Choose a caregiver and a start time first.', 'err'); return; } dayList('Visits for ' + stName(ST(m.v.cgId)) + ' on ' + fmtD(s), DB.visits.filter(v => v.cgId === m.v.cgId && v.start.slice(0, 10) === s.slice(0, 10))); };
function pickCg(m, title, list, note) { modal({ title, size: 'sm', z: 1100, body: `${note ? '<p class="small">' + note + '</p>' : ''}${list.map(s => `<div class="opt" style="padding:7px 10px;border-bottom:1px solid #eee;cursor:pointer" data-act="apPick" data-id="${s.id}">${esc(stName(s))} (${s.disc})</div>`).join('') || '<p class="none">No caregivers found</p>'}`, buttons: [{ label: 'Close', cls: 'btn-close' }], ctx: ctxNew({ target: m }) }); }
ACT.apPick = el => { const c = ctxOf(el); c.target.v.cgId = el.dataset.id; c.target._modal.rerender(); c._modal.close(); };
ACT.apCare = el => { const m = ctxOf(el); if (!m.v.pid) { toast('Choose a patient first.', 'err'); return; } const adm = admOf(m.v.pid); const ids = DB.forms.filter(f => f.pid === m.v.pid && f.type === 'careteam').map(f => f.d.f1); if (adm && adm.caseMgr) ids.push(adm.caseMgr); pickCg(m, "Caregivers in the patient's care team", DB.staff.filter(s => ids.indexOf(s.id) >= 0), 'People listed on the Care Team form and the Case Manager of the admission.'); };
ACT.apRegion = el => { const m = ctxOf(el); if (!m.v.pid) { toast('Choose a patient first.', 'err'); return; } const pt = P(m.v.pid); pickCg(m, 'Caregivers in the patient region: zip ' + pt.zip, DB.staff.filter(s => s.active && s.disc !== 'OFFICE' && (s.covZips || '').indexOf(pt.zip) >= 0), 'Caregivers whose coverage zip codes include ' + pt.zip + '.'); };
ACT.apAvail = el => { const m = ctxOf(el); const s = parseDT(m.v.start), e = parseDT(m.v.end); if (!s || !e) { toast('Enter the start and end time first.', 'err'); return; } pickCg(m, 'Available caregivers', DB.staff.filter(x => { if (!x.active || x.disc === 'OFFICE') return false; if (absenceOn(x, s.slice(0, 10))) return false; const av = (x.avail || {})[DAYS[toDate(s).getDay()]]; if (av && !av.on) return false; if (av && av.on && (fmtHM(s) < av.from || fmtHM(e) > av.to)) return false; return !DB.visits.some(v => v.cgId === x.id && v.status !== 'A' && overlapV(s, e, v.start, v.end)); }), 'Free at ' + fmtDT(s) + ', not absent, inside their availability.'); };
function apptCollect(m) { const v = m.v; return { s: parseDT(v.start), e: parseDT(v.end) }; }
function apptSave(m, mod) {
  const v = m.v, ex = m.ex; const { s, e } = apptCollect(m);
  const errs = [];
  if (!v.cgId) errs.push('Choose the Caregiver.'); if (!v.pid) errs.push('Choose the Patient.'); if (!s || !e) errs.push('Enter valid Appt. Start Time and Appt. End Time (MM/DD/YYYY hh:mm AM).'); else if (e <= s) errs.push('Appt. End Time must be after Appt. Start Time.');
  if (!v.billing) errs.push('Choose a Billing Code.'); if ((v.status === 'M' || v.status === 'A') && !v.missedReason) errs.push('Choose a reason for a Missed or Cancelled visit.');
  if (!errs.length && !v.dontValidate) { const cf = visitConflicts({ start: s, end: e, cgId: v.cgId, pid: v.pid }, ex ? ex.id : ''); if (cf.cg.length) errs.push('Time conflict: ' + stName(ST(v.cgId)) + ' already has a visit from ' + fmtT(cf.cg[0].start) + ' to ' + fmtT(cf.cg[0].end) + ' with ' + ptName(P(cf.cg[0].pid)) + '. STOP and ask the Administrator or DON. Do not hide the conflict.'); }
  if (errs.length) { track('visit:savefail'); alertBox('The visit was not saved', '<ul>' + errs.map(x => `<li>${esc(x)}</li>`).join('') + '</ul>', 'warn'); return; }
  const coach = [];
  const bc = byId(DB.lists.billingCodes, v.billing); const adm = admOf(v.pid);
  if (v.pid === 'P1' && v.billable) coach.push('Practice visits on JOHN DOE must have Billable UNCHECKED so nothing can be billed.');
  if (adm && adm.status !== 'Admitted') coach.push('This admission is ' + adm.status + '. Do not schedule before the Administrator approves the admission.');
  if (adm && adm.disciplines.length && adm.disciplines.indexOf(discOf({ cgId: v.cgId })) < 0 && ST(v.cgId).disc !== 'OFFICE') coach.push('Do not assign a discipline the physician did not order (' + ST(v.cgId).disc + ' is not on the admission).');
  if (bc && bc.soc && !String(v.cmtAdmin).trim() && !(ex && ex.adminComments)) coach.push('Write who approved the SOC and when in Comments (for administrative use only).');
  if (ex && !roleIs('DON') && (ex.cgId !== v.cgId || ex.start !== s || ex.end !== e || ex.pid !== v.pid)) { coach.push('Do not change a visit without authorization from the Administrator or DON. Write the reason and who authorized it in Comments (for administrative use only).'); if (String(v.cmtAdmin).trim() === String(ex.adminComments || '').trim()) coach.push('Comments (for administrative use only) were not updated with the reason and who authorized the change.'); }
  const credP = credProblems(ST(v.cgId)); if (credP.length) coach.push(stName(ST(v.cgId)) + ' has an expired credential (' + credP.join('; ') + ').');
  const doIt = () => {
    const rec = { id: ex ? ex.id : uid('V'), pid: v.pid, cgId: v.cgId, start: s, end: e, status: v.status, billingCode: v.billing, billable: !!v.billable, comments: v.cmtCg, adminComments: v.cmtAdmin, location: v.location, travel: v.tH || v.tM ? (v.tH || '0') + ':' + (v.tM || '00') : '', overtime: v.oH || v.oM ? (v.oH || '0') + ':' + (v.oM || '00') : '', mileage: v.miles, expenses: v.exp, dontValidate: !!v.dontValidate, qaMon: !!v.qaMon, qaWhy: v.qaWhy, missedReason: v.missedReason };
    const made = [];
    if (ex) { Object.assign(ex, rec); track('visit:changed'); simLog('info', 'Changed a visit for ' + ptName(P(v.pid))); made.push(ex); }
    else { Object.assign(rec, { createdBy: DB.session.userId, evv: {}, noteId: '', qaMon: !!v.qaMon }); DB.visits.push(rec); made.push(rec); track('visit:created'); if (bc && bc.soc) track('visit:soc'); if (v.billable && v.pid === 'P1') track('visit:billable-practice'); simLog('info', 'Scheduled a visit for ' + ptName(P(v.pid)) + ' with ' + stName(ST(v.cgId)) + ' on ' + fmtD(s)); }
    let skipped = 0;
    if (v.recur.on && !ex) { const until = parseD(v.recur.until); if (until) { const days = Object.keys(v.recur.days).filter(k => v.recur.days[k]); let n = 0; for (let d = addDays(s.slice(0, 10), 1); d <= until && n < 120; d = addDays(d, 1), n++) { if (days.length && days.indexOf(DAYS[toDate(d).getDay()]) < 0) continue; const ss = d + s.slice(10), ee = d + e.slice(10); if (visitConflicts({ start: ss, end: ee, cgId: v.cgId, pid: v.pid }, '').cg.length) { skipped++; continue; } const r2 = Object.assign({}, rec, { id: uid('V'), start: ss, end: ee, status: 'N', evv: {}, noteId: '', createdBy: DB.session.userId }); DB.visits.push(r2); made.push(r2); } track('visit:recurring'); } }
    save(); mod.close(); refresh(); toast((ex ? 'Visit saved.' : made.length + ' visit' + (made.length === 1 ? '' : 's') + ' added.') + (skipped ? ' ' + skipped + ' skipped for time conflicts.' : '') + (ex ? '' : ' Call the patient to confirm the date and time.'), 'ok');
  };
  if (coach.length) { modal({ title: 'Zenith rules to check before saving', kind: 'warn', size: 'lg', z: 1100, body: `<ul>${coach.map(x => `<li>${esc(x)}</li>`).join('')}</ul><p class="mt">In real work you would STOP and ask the Administrator or DON. In this simulator you may save anyway so you can see the result. The choice is written in the Coach log.</p>`, buttons: [{ label: 'Go back (recommended)', cls: 'btn-ok', click: () => simLog('good', 'Went back before saving a visit: ' + coach[0]) }, { label: 'Save anyway (practice)', cls: 'btn-or', click: () => { simLog('override', 'Saved a visit despite: ' + coach.join(' | ')); doIt(); } }] }); return; }
  doIt();
}
function apptDelete(m, mod) { needApproval({ roles: ['Administrator', 'DON'], what: 'Delete a visit', rule: 'Do not change or delete a visit without authorization. A visit that was started (clocked in) is never deleted.', who: 'DON or Administrator', ref: 'SC2', go: () => confirmBox('Delete this visit?', '<p>The visit is removed from the practice schedule.</p>', () => { DB.visits = DB.visits.filter(x => x.id !== m.ex.id); save(); track('visit:deleted'); mod.close(); refresh(); }, { yes: 'Delete', no: 'Cancel' }) }); }

/* ---------------------------------------------------------------- Batch Entry of Visits (simplified) */
ROUTES.batch = {
  render(c) {
    if (!c.b) c.b = { pid: '', cgId: '', code: '', from: fmtD(todayIso()), to: '', time: '09:00', dur: '60', days: {}, billable: true };
    const b = c.b; const dates = batchDates(b); const bad = dates.filter(d => batchConflict(b, d));
    return pageHead('Batch Entry of Visits', 'Summary') + `${simplified()}<p class="small">Create several visits at once. Zenith rule: repeating visits need the DON's approval, and every visit still follows the ordered frequency.</p>
      <div class="row c2">${fg('Patient', s2(c, 'b.pid', 'patients', { ph: 'Enter Patient', rr: 1 }), { req: 1 })}${fg('Caregiver', s2(c, 'b.cgId', 'caregivers', { ph: 'Enter Caregiver', rr: 1 }), { req: 1 })}${fg('Billing Code', s2(c, 'b.code', 'billingCodes', { ph: 'Enter Billing Code' }), { req: 1 })}<div class="fg"><label class="chk" style="margin-top:22px"><input type="checkbox" ${battr(c, 'b.billable')}${b.billable ? ' checked' : ''}> Billable</label></div>${fg('From date', dp(c, 'b.from'), { req: 1 })}${fg('To date', dp(c, 'b.to'), { req: 1 })}${fg('Start time (24 hour, example 09:00)', inp(c, 'b.time'))}${fg('Length in minutes', inp(c, 'b.dur'))}</div>
      <div class="fg"><label>Days of the week</label><div class="chkbox">${WDAYS.map(d => `<label class="chk"><input type="checkbox" ${battr(c, 'b.days.' + d)} data-rr="1"${getp(c, 'b.days.' + d) ? ' checked' : ''}> ${d}</label>`).join('')}</div></div>
      <div class="box"><h4>Preview (${dates.length} visits${bad.length ? ', ' + bad.length + ' with a time conflict' : ''})</h4><div style="max-height:200px;overflow:auto">${dates.map(d => `<span class="tag ${batchConflict(b, d) ? 'r' : 'b'}" style="margin:2px">${fmtD(d).slice(0, 5)} ${DAYS[toDate(d).getDay()]}</span>`).join('') || '<span class="small">Choose dates and days of the week.</span>'}</div></div>
      <div class="flex mt"><button class="btn btn-save" data-act="batchGo">Create visits</button><button class="btn btn-close" data-act="batchClose">Close</button></div>`;
  },
};
function batchDates(b) { const f = parseD(b.from), t = parseD(b.to); if (!f || !t) return []; const days = Object.keys(b.days).filter(k => b.days[k]); const out = []; for (let d = f, n = 0; d <= t && n < 120; d = addDays(d, 1), n++) if (days.indexOf(DAYS[toDate(d).getDay()]) >= 0) out.push(d); return out; }
function batchTimes(b, d) { const hm = /^(\d{1,2}):(\d{2})$/.exec(b.time || ''); if (!hm) return null; const s = d + 'T' + pad(+hm[1]) + ':' + hm[2]; return { s, e: addMin(s, +b.dur || 60) }; }
function batchConflict(b, d) { const t = batchTimes(b, d); if (!t || !b.cgId) return false; return visitConflicts({ start: t.s, end: t.e, cgId: b.cgId, pid: b.pid }, '').cg.length > 0; }
ACT.batchClose = () => go('home');
ACT.batchGo = el => {
  const c = ctxOf(el), b = c.b; const dates = batchDates(b);
  if (!b.pid || !b.cgId || !b.code || !dates.length || !batchTimes(b, dates[0] || todayIso())) { toast('Patient, Caregiver, Billing Code, dates, days of the week and a valid start time (like 09:00) are required.', 'err'); return; }
  const go2 = () => { let n = 0, skip = 0; dates.forEach(d => { const t = batchTimes(b, d); if (batchConflict(b, d)) { skip++; return; } DB.visits.push({ id: uid('V'), pid: b.pid, cgId: b.cgId, start: t.s, end: t.e, status: 'N', billingCode: b.code, billable: !!b.billable, comments: '', adminComments: 'Batch entry (practice)', location: "Patient's home", travel: '', overtime: '', mileage: '', dontValidate: false, qaMon: false, createdBy: DB.session.userId, evv: {}, noteId: '' }); n++; }); save(); track('batch:created'); simLog('info', 'Batch entry created ' + n + ' visits'); toast(n + ' visits created' + (skip ? ', ' + skip + ' skipped for time conflicts' : '') + '.', 'ok'); refresh(); };
  needApproval({ roles: ['DON'], what: 'Create many visits at once (batch entry)', rule: 'Repeating visits need the DON\'s approval.', who: 'DON or Administrator', ref: 'SC1', go: go2 });
};

/* ---------------------------------------------------------------- CareConnect Monitor */
ROUTES.monitor = {
  render(c) {
    if (!c.init) { c.init = 1; c.date = fmtD(todayIso()); c.pause = false; c.incl = false; c.by = 'Caregiver'; c.info = true; }
    const day = parseD(c.date) || todayIso(); c.dayIso = day;
    const dur = m => (m < 0 ? '' : Math.floor(m / 60) + ':' + pad(m % 60));
    const tbl = DT(c, 'mon', () => ({ filterBtn: true, sort: 'vt', dir: -1, noTop: false, empty: 'No data available in table', extraTop: ` Search By: <select style="width:120px" ${battr(c, 'by')} data-rr="1">${['Caregiver', 'Patient'].map(x => `<option${c.by === x ? ' selected' : ''}>${x}</option>`).join('')}</select>`,
      cols: [{ key: 'act', label: 'Action', sortable: false, blue: true, render: r => rowIcons([{ ic: 'eye', t: 'View visit details', act: 'monView', data: { id: r.v.id }, cls: 'view' }]) }, { key: 'pt', label: 'Patient', text: r => ptName(P(r.v.pid)), render: r => esc(ptName(P(r.v.pid))) }, { key: 'cg', label: 'Caregiver', text: r => stName(ST(r.v.cgId)), render: r => esc(stName(ST(r.v.cgId))) },
        { key: 'del', label: 'Delayed', text: r => String(r.s.delayed), sort: r => r.s.delayed, render: r => (r.s.delayed ? `<b style="color:#c0392b">${r.s.delayed} min</b>` : '') }, { key: 'status', label: 'Status', text: r => r.s.label, render: r => `<span class="tag ${r.s.cls}">${esc(r.s.label)}</span>` },
        { key: 'st', label: 'Start Time', text: r => r.v.evv.inAt || r.v.start, render: r => (r.v.evv.inAt ? fmtT(r.v.evv.inAt) : '<span style="color:#999">' + fmtT(r.v.start) + '</span>') }, { key: 'en', label: 'End Time', text: r => r.v.evv.outAt || '', render: r => (r.v.evv.outAt ? fmtT(r.v.evv.outAt) : '') },
        { key: 'vt', label: 'Visit Time', blue: true, text: r => String(r.vt), sort: r => r.vt, render: r => dur(r.vt) }, { key: 'sd', label: 'Sched. Dur.', text: r => String(diffMin(r.v.end, r.v.start)), sort: r => diffMin(r.v.end, r.v.start), render: r => dur(diffMin(r.v.end, r.v.start)) }],
      rows: monRows(c, day), searchText: r => (c.by === 'Patient' ? ptName(P(r.v.pid)) : stName(ST(r.v.cgId))) }));
    return pageHead('CareConnect Monitor', 'Summary') + (c.info ? `<div class="note" style="background:#e3f1fb;border:1px solid #9cc6e6;border-radius:8px;display:block"><div class="flex"><b class="grow">${ic('help')} Want to be notified about delays?</b><a data-act="monInfo">See Less &#9650;</a></div><p class="small mt">The Delayed Visit Alerts feature can notify your administration and caregivers of visit delays. Alerts are sent to smartphones.</p><a data-act="monFeat">Go to Features Activation</a></div>` : `<div class="mt"><a data-act="monInfo">Want to be notified about delays? See More &#9660;</a></div>`) +
      `<div class="flex mt" style="align-items:flex-end"><div style="width:200px">${fg('Date', dp(c, 'date', { rr: 1 }))}</div><button class="btn btn-add" data-act="monGo">Go</button></div><div class="fg"><label class="chk"><input type="checkbox" ${battr(c, 'pause')} data-rr="1"${c.pause ? ' checked' : ''}> Pause Auto Refreshing</label>${c.pause ? '' : ' <span class="small">(refreshes every 30 seconds)</span>'}</div>
      <div class="fg"><label class="chk"><input type="checkbox" ${battr(c, 'incl')} data-rr="1"${c.incl ? ' checked' : ''}> Include Cancelled, Missed, Hospitalized and On Hold Visits</label></div>${tbl}<p class="small">Look only. Do not edit visits or mark them complete from here. Check at the start of the day and after lunch, then report delayed or missed visits to the DON.</p>`;
  },
};
function monRows(c, day) {
  const out = []; DB.visits.filter(v => v.start.slice(0, 10) === day).forEach(v => { const hidden = ['A', 'M', 'H', 'O'].indexOf(v.status) >= 0; if (hidden && !c.incl) return; const s = visitStatus(v); const e = v.evv || {}; const vt = e.inAt ? (e.outAt ? diffMin(e.outAt, e.inAt) : Math.max(0, diffMin(nowIso(), e.inAt))) : -1; out.push({ v, s, vt }); });
  return out;
}
ACT.monInfo = el => { const c = ctxOf(el); c.info = !c.info; refresh(); };
ACT.monFeat = () => alertBox('Features Activation', '<p>The real Alora has a Features Activation setup screen where Delayed Visit Alerts are turned on. Alerts send text messages to real phones, so it is not part of the simulator.</p>');
ACT.monGo = el => { const c = ctxOf(el); track('monitor:setdate'); refresh(); };
ACT.monView = el => { const v = byId(DB.visits, el.dataset.id); const e = v.evv || {}; const s = visitStatus(v); modal({ title: 'Visit details (look only)', size: 'sm', body: `<div class="kv"><div>Patient</div><div>${esc(ptName(P(v.pid)))}</div><div>Caregiver</div><div>${esc(stName(ST(v.cgId)))}</div><div>Scheduled</div><div>${fmtDT(v.start)} to ${fmtT(v.end)}</div><div>Clock in</div><div>${e.inAt ? fmtDT(e.inAt) + ' (' + esc((e.inGps || {}).where || '') + ')' : 'none'}</div><div>Clock out</div><div>${e.outAt ? fmtDT(e.outAt) + ' (' + esc((e.outGps || {}).where || '') + ')' : 'none'}</div><div>Status</div><div>${esc(s.label)}</div></div><p class="small mt">Do not edit visits from the Monitor. Report delays to the DON.</p>`, buttons: [{ label: 'Close', cls: 'btn-close' }] }); };
setInterval(() => { if (PAGE && PAGE.route === 'monitor' && PAGE.ctx && !PAGE.ctx.pause && !MODALS.length && !$('.s2pop') && !$('.dpop') && document.activeElement && !(document.activeElement.dataset && document.activeElement.dataset.dtq)) refresh(); }, 30000);

/* ---------------------------------------------------------------- CareConnect Conflicts */
function gpsMiles(g, pt) { if (!g || g.lat == null) return null; const R = 3958.8, rad = x => x * Math.PI / 180; const dl = rad(g.lat - pt.lat), dn = rad(g.lng - pt.lng); const a = Math.sin(dl / 2) ** 2 + Math.cos(rad(pt.lat)) * Math.cos(rad(g.lat)) * Math.sin(dn / 2) ** 2; return 2 * R * Math.asin(Math.sqrt(a)); }
ROUTES.conflicts = {
  render(c) {
    if (!c.init) { c.init = 1; c.from = fmtD(addDays(todayIso(), -7)); c.to = fmtD(todayIso()); c.sel = ''; }
    const f = parseD(c.from) || addDays(todayIso(), -7), t = parseD(c.to) || todayIso();
    const rows = evvConflicts().filter(x => x.v.start.slice(0, 10) >= f && x.v.start.slice(0, 10) <= t);
    const tbl = DT(c, 'cf', () => ({ filterBtn: true, sort: 'v', empty: 'No pending items for the selected office',
      cols: [{ key: 'v', label: 'Visit', blue: true, text: r => r.v.start, render: r => `<label class="chk"><input type="radio" name="cfsel" data-act="cfSel" data-id="${r.v.id}"${c.sel === r.v.id ? ' checked' : ''}> ${fmtD(r.v.start)}</label>` }, { key: 'reason', label: 'Conflict Reason', text: r => r.reason, render: r => esc(r.reason) }, { key: 'pt', label: 'Patient', text: r => ptName(P(r.v.pid)), render: r => esc(ptName(P(r.v.pid))) }, { key: 'cg', label: 'Caregiver', text: r => stName(ST(r.v.cgId)), render: r => esc(stName(ST(r.v.cgId))) },
        { key: 'ss', label: 'Sch. Start Time', text: r => r.v.start, render: r => fmtDT(r.v.start) }, { key: 'se', label: 'Sch. End Time', text: r => r.v.end, render: r => fmtDT(r.v.end) }, { key: 'cs', label: 'Captured Start Time', text: r => r.v.evv.inAt || '', render: r => fmtDT(r.v.evv.inAt) }, { key: 'ce', label: 'Captured End Time', text: r => r.v.evv.outAt || '', render: r => fmtDT(r.v.evv.outAt) }],
      rows, searchText: r => ptName(P(r.v.pid)) + ' ' + stName(ST(r.v.cgId)) + ' ' + r.reason }));
    return pageHead('CareConnect Conflicts', 'Summary') + `<div class="box"><div class="row c2" style="max-width:520px">${fg('Date From:', dp(c, 'from', { rr: 1 }))}${fg('Date To:', dp(c, 'to', { rr: 1 }))}</div><button class="btn btn-add btn-sm" data-act="cfGo">Show</button>${tbl}
      <div class="flex mt" style="gap:0"><button class="btn" style="background:#5b9bd5;color:#fff" data-act="cfAct" data-a="end">End Visit</button><button class="btn" style="background:#a7d3ee;color:#fff" data-act="cfAct" data-a="ack">Acknowledge</button><button class="btn" style="background:#a58fd0;color:#fff" data-act="cfAct" data-a="gps">Review GPS Information</button><button class="btn" style="background:#8cc59a;color:#fff" data-act="cfAct" data-a="rm">Remove without Action</button></div></div>
      <p class="small mt">Report conflicts. Only the Administrator uses these four buttons. Do not change times to make a conflict disappear.</p>`;
  },
};
ACT.cfGo = () => { track('conflicts:setdate'); refresh(); };
ACT.cfSel = el => { const c = ctxOf(el); c.sel = el.dataset.id; };
ACT.cfAct = el => {
  const c = ctxOf(el); const a = el.dataset.a; track('conflicts:button'); const v = c.sel ? byId(DB.visits, c.sel) : null;
  const label = { end: 'End Visit', ack: 'Acknowledge', gps: 'Review GPS Information', rm: 'Remove without Action' }[a];
  needApproval({ roles: ['Administrator'], what: 'Click ' + label + ' on the Conflicts screen', rule: 'Office staff do not click End Visit, Acknowledge, Review GPS Information or Remove without Action. Only the Administrator resolves EVV conflicts, with an EVV Change Reason.', who: 'Administrator', ref: 'SC4, AD4', go: () => {
    if (!v) { toast('Select a conflict row first.', 'err'); return; }
    if (a === 'gps') { gpsModal(v); return; }
    const m = ctxNew({ reason: '', cm: '', end: fmtDT(v.end) });
    modal({ title: 'EVV Change Reason: ' + label, ctx: m, size: 'sm', body: mc => `<div class="kv"><div>Patient</div><div>${esc(ptName(P(v.pid)))}</div><div>Caregiver</div><div>${esc(stName(ST(v.cgId)))}</div></div>${a === 'end' ? fg('End time to record', dp(mc, 'end', { time: true })) : ''}${fg('EVV Change Reason', s2(mc, 'reason', 'evvReasons', { ph: 'Select a reason' }), { req: 1 })}${fg('Comments', txt(mc, 'cm', { rows: 3 }))}<p class="small">Every change to EVV data needs a reason. Never enter a time that did not really happen.</p>`,
      buttons: [{ label: label, cls: 'btn-ok', click: () => { if (!m.reason) { toast('Choose an EVV Change Reason.', 'err'); return false; } const e = v.evv; if (a === 'end') { const t = parseDT(m.end); if (!t || t <= (e.inAt || v.start)) { toast('Enter a valid end time after the clock in.', 'err'); return false; } e.outAt = t; e.outGps = e.outGps || e.inGps; if (v.status === 'N' && v.noteId && (byId(DB.snNotes, v.noteId) || {}).status === 'Completed') v.status = 'C'; } e.resolved = true; e.changeReason = m.reason; e.changeNote = m.cm; e.resolvedBy = DB.session.userId; e.resolvedAs = label; save(); track('conflicts:resolved'); simLog('info', label + ' on a conflict: ' + m.reason); c.sel = ''; refresh(); toast('Conflict resolved: ' + label + '.', 'ok'); } }, { label: 'Cancel', cls: 'btn-del' }] });
  } });
};
function gpsModal(v) {
  const pt = P(v.pid), e = v.evv || {}; const mi = gpsMiles(e.inGps, pt); const mo = e.outGps ? gpsMiles(e.outGps, pt) : null;
  const sc = 4000; const px = (g) => ({ x: 150 + (g.lng - pt.lng) * sc * 1.0, y: 110 - (g.lat - pt.lat) * sc * 1.0 });
  const pin = (g, col, lab) => { if (!g || g.lat == null) return ''; const p = px(g); return `<g transform="translate(${Math.max(14, Math.min(286, p.x))},${Math.max(14, Math.min(206, p.y))})"><circle r="9" fill="${col}" stroke="#fff" stroke-width="2"/><text x="14" y="4" font-size="11" font-family="Arial" fill="#222">${lab}</text></g>`; };
  modal({ title: 'Review GPS Information', size: 'lg', body: `<div class="map"><svg viewBox="0 0 300 220" width="100%" height="260" preserveAspectRatio="xMidYMid slice"><rect width="300" height="220" fill="#e8f0e0"/><path d="M0 120 L300 90" stroke="#fff" stroke-width="8"/><path d="M110 0 L150 220" stroke="#fff" stroke-width="6"/>${pin({ lat: pt.lat, lng: pt.lng }, '#3a7a3a', 'Patient home')}${pin(e.inGps, '#d9534f', 'Clock in')}${e.outGps ? pin(e.outGps, '#8e6cc0', 'Clock out') : ''}</svg></div><div class="kv mt"><div>Patient home</div><div>${esc([pt.addr1, pt.city, pt.state, pt.zip].join(', '))}</div><div>Clock in location</div><div>${esc((e.inGps || {}).where || 'none')}${mi != null ? ' (' + mi.toFixed(1) + ' miles from the home)' : ''}</div><div>Clock out location</div><div>${esc((e.outGps || {}).where || 'none')}${mo != null ? ' (' + mo.toFixed(1) + ' miles from the home)' : ''}</div></div><p class="small mt">Practice map. A real map would load tiles from the internet, so the simulator draws a simple picture instead.</p>`, buttons: [{ label: 'Close', cls: 'btn-close' }] });
}

/* ---------------------------------------------------------------- CareConnect page */
ROUTES.careconnect = {
  render(c) {
    const rows = DB.staff.filter(s => s.cc && s.cc.enabled);
    return pageHead('CareConnect', 'Summary') + `<div class="note sim">CareConnect is the phone app caregivers use to see their schedule, clock in and out (EVV), write notes and collect signatures. The simulator includes a practice phone.</div>
      <div class="flex mt"><button class="btn btn-add" data-act="phoneopen">${ic('cc')} Open the CareConnect phone</button><a data-go="monitor">Monitor</a><a data-go="conflicts">Conflicts</a></div>
      <div class="box mt"><h4>Caregivers with CareConnect</h4><table class="t"><thead><tr><th>Caregiver</th><th>Discipline</th><th>CareConnect user</th><th>Invited</th><th>Today's visits</th></tr></thead><tbody>${rows.map(s => `<tr><td>${esc(stName(s))}</td><td>${s.disc}</td><td>${esc(s.cc.user)}</td><td>${fmtD(s.cc.invited)}</td><td>${DB.visits.filter(v => v.cgId === s.id && v.start.slice(0, 10) === todayIso()).length}</td></tr>`).join('') || '<tr><td colspan="5" class="none">No caregivers have CareConnect yet. HR: Staff record, Enable CareConnect.</td></tr>'}</tbody></table></div>`;
  },
};

'use strict';
/* =====================================================================================================
   Practice data. Every person, number and document here is made up. Nothing is a real patient or employee.
   The practice clock starts on 09/30/2026 (the day the Zenith manual was written) so the screens match the manual.
   ===================================================================================================== */
const SEED_VERSION = 4;
const ROLES = ['Administrator', 'DON', 'Office', 'Scheduler', 'HR', 'Nurse', 'Aide', 'Biller'];
const ROLE_LABEL = { Administrator: 'Administrator', DON: 'Director of Nursing (DON)', Office: 'Office and Intake', Scheduler: 'Scheduler', HR: 'Human Resources', Nurse: 'Nurse / Clinician (RN)', Aide: 'Home Health Aide', Biller: 'Biller' };
const DISCIPLINES = ['RN', 'LPN', 'HHA', 'PT', 'PTA', 'OT', 'OTA', 'ST', 'MSW', 'OFFICE'];
const CRED_ITEMS = [
  ['LIC', 'Professional license'], ['CPR', 'CPR certification'], ['TB', 'TB screening'], ['PHY', 'Physical examination'], ['BGC', 'Background screening'],
  ['I9', 'I-9 employment eligibility'], ['HEPB', 'Hepatitis B vaccine or declination'], ['COMP', 'Annual competency'], ['INS', 'Auto insurance (if driving)'],
];
const PT_FOLDERS = ['PHYSICIAN ORDERS', 'PLANS OF CARE', 'PRIOR AUTHORIZATIONS', 'DISCHARGE RECORDS', 'MEDICAL RECORDS'];
const STAFF_FOLDERS = ['NEW HIRE PAPERWORK', 'CREDENTIAL ITEMS', 'HEALTH SCREENINGS', 'PERFORMANCE EVALUATIONS'];

/* ---------------------------------------------------------------- SN note form layout (checks and messages) */
const SN_TABS = [
  { k: 'vital', l: 'Vital Signs', secs: [
    { id: 'vitals', t: 'Vital signs', kind: 'vitals', msg: 'Vital Signs - Temperature, pulse, respirations, blood pressure and oxygen saturation need to be entered' },
    { id: 'pain', t: 'Pain', opts: ['No pain', 'Mild (1 to 3)', 'Moderate (4 to 6)', 'Severe (7 to 10)'] }] },
  { k: 'cardio', l: 'Cardio & Pulm.', secs: [
    { id: 'cardio', t: 'Cardiovascular', opts: ['Heart rhythm regular', 'Heart rhythm irregular', 'Edema none', 'Edema present', 'Chest pain reported', 'No cardiovascular problems'] },
    { id: 'resp', t: 'Respiratory', opts: ['Lungs clear', 'Wheezes', 'Crackles', 'Short of breath', 'Oxygen in use', 'No respiratory problems'] }] },
  { k: 'neuro', l: 'Neuro & Gastro', secs: [
    { id: 'neuro', t: 'Neurological', opts: ['Alert and oriented', 'Confused', 'Weakness', 'Dizziness', 'No neurological problems'] },
    { id: 'gi', t: 'Gastrointestinal', opts: ['Appetite good', 'Appetite poor', 'Diet as ordered', 'Tube feeding in use', 'Nausea', 'No gastrointestinal problems'], msg: 'Gastrointestinal - For Appetite, Diet/Nutritional Requirements and Tube Feeding at least one of the option needs to be selected or completed' }] },
  { k: 'genito', l: 'Genito & Endo.', secs: [
    { id: 'gu', t: 'Genitourinary', opts: ['Voiding without problems', 'Catheter in place', 'Incontinence', 'No genitourinary problems'] },
    { id: 'endo', t: 'Endocrine', opts: ['Blood sugar checked', 'Insulin given', 'Diabetic teaching done', 'No endocrine problems'] }] },
  { k: 'skin', l: 'Skin & Wound', secs: [
    { id: 'skin', t: 'Integumentary', opts: ['Skin intact', 'Dry skin', 'Bruising', 'Pressure area', 'No skin problems'] },
    { id: 'wound', t: 'Wound', opts: ['No wound', 'Wound care done', 'Wound improving', 'Wound worse'] }] },
  { k: 'med', l: 'Medication', secs: [
    { id: 'medchg', t: 'Medication changes', opts: ['Unchanged', 'New/Changed'], msg: 'Medication - Unchanged or New/Changed at least one of the two checkboxes needs to be checked' },
    { id: 'medopt', t: 'Medication review', opts: ['Reviewed with patient', 'Reviewed with caregiver', 'Pill box filled', 'Side effects discussed'], msg: 'Medication - At least one of the option needs to be selected or completed' },
    { id: 'iv', t: 'IV therapy', opts: ['No IV therapy', 'IV site checked', 'IV medication given'], msg: 'IV Therapy - At least one of the option needs to be selected or completed' }] },
  { k: 'other', l: 'Other Interv.', secs: [
    { id: 'teach', t: 'Teaching', opts: ['Disease process', 'Medications', 'Safety', 'Diet', 'No teaching needed'] },
    { id: 'safety', t: 'Safety', opts: ['Home safety reviewed', 'Fall precautions reviewed', 'Emergency plan reviewed', 'No safety concerns'] }] },
  { k: 'summ', l: 'Interv. Summary', secs: [
    { id: 'interv', t: 'Interventions', opts: ['Assessment', 'Teaching', 'Wound care', 'Medication management', 'Other'], msg: 'Interv. Summary - There has to be at least one intervention' },
    { id: 'resp2', t: 'Patient response', opts: ['Verbalized understanding', 'Needs more teaching', 'Refused'] }] },
  { k: 'plan', l: 'Plan', secs: [
    { id: 'plan', t: 'Plan', opts: ['Continue plan of care', 'Notify physician', 'Revise plan of care'] },
    { id: 'edu', t: 'Education plan', opts: ['Continue teaching', 'Teaching complete'] },
    { id: 'next', t: 'Next visit', opts: ['As scheduled', 'Needs earlier visit'] }] },
  { k: 'qa', l: 'QA/Signature', secs: [] },
];
function snSections() { const o = []; SN_TABS.forEach(t => t.secs.forEach(s => o.push(Object.assign({ tab: t.k, tabLabel: t.l }, s)))); return o; }
function snErrors(note) {
  const d = note.data || {}; const out = [];
  snSections().forEach(s => {
    let ok;
    if (s.kind === 'vitals') { const v = d.vitals || {}; ok = v.temp && v.pulse && v.resp && v.bps && v.bpd && v.o2; }
    else ok = (d[s.id] || []).length > 0;
    if (!ok) out.push({ tab: s.tab, tabLabel: s.tabLabel, sec: s.id, msg: s.msg || `${s.t} - At least one of the option needs to be selected or completed` });
  });
  if (!note.visitType) out.push({ tab: 'vital', tabLabel: 'Vital Signs', sec: 'type', msg: 'Visit Information - Type of Visit must be selected' });
  return out;
}
function snFullData() {
  const d = { vitals: { temp: '98.4', pulse: '72', resp: '16', bps: '124', bpd: '78', o2: '97' } };
  snSections().forEach(s => { if (s.kind !== 'vitals') d[s.id] = [s.opts[0]]; });
  d.narrative = 'Practice note. Patient seen as scheduled. Plan of care followed.';
  return d;
}

/* ---------------------------------------------------------------- seed */
function seedData() {
  SEED_FILES = {};
  let seq = 1000; const id = p => p + (++seq);
  const T = s => s; // dates are written as ISO strings
  const D = {
    v: SEED_VERSION, seq: 0, session: { userId: null }, ui: { open: { patient: true }, collapsed: false, goto: false },
    clock: { base: new Date(2026, 8, 30, 8, 30).getTime(), realAt: Date.now(), paused: false, lastSeen: Date.now() },
    stats: {}, tasksDone: {}, log: [], visitedAt: {},
    users: [], staff: [], patients: [], admissions: [], referrals: [], docs: [], orders: [], assessments: [], snNotes: [], aideDocs: [], f485: [], commLog: [], forms: [], visits: [],
    messages: [], covid: [], noa: [], deleted: [], faxes: [], accessRequests: [], payments: [],
    lists: {
      offices: ['Zenith Care Home Health LLC'],
      physicians: [{ id: 'PH1', name: 'TEST PHYSICIAN, MD', npi: '1000000001' }, { id: 'PH2', name: 'SAMPLE, ALEX MD', npi: '1000000002' }, { id: 'PH3', name: 'DEMO, CASEY DO', npi: '1000000003' }],
      referralSources: ['Sample General Hospital', 'Demo Family Clinic', 'Practice Rehab Center', 'Family or self'],
      admissionSources: ['Hospital', 'Physician office', 'Skilled nursing facility', 'Family or self'],
      payers: [{ id: 'PY1', name: 'PRIVATE PAY', type: 'Non-Insurance' }, { id: 'PY2', name: 'MEDICARE (PRACTICE)', type: 'Primary' }, { id: 'PY3', name: 'MEDICAID (PRACTICE)', type: 'Primary' }, { id: 'PY4', name: 'SAMPLE HMO', type: 'Primary' }],
      billingCodes: [
        { id: 'BC1', code: 'SN-SOC', desc: 'RN Start of Care Visit (practice code)', disc: 'RN', soc: true }, { id: 'BC2', code: 'SN-DC', desc: 'RN Direct Care', disc: 'RN' }, { id: 'BC3', code: 'LPN-DC', desc: 'LPN Direct Care', disc: 'LPN' },
        { id: 'BC4', code: 'SN-SUP', desc: 'RN Supervisory Visit', disc: 'RN' }, { id: 'BC5', code: 'HHA', desc: 'Home Health Aide Visit', disc: 'HHA' }, { id: 'BC6', code: 'PT-EVAL', desc: 'PT Evaluation', disc: 'PT' },
        { id: 'BC7', code: 'PT', desc: 'PT Visit', disc: 'PT' }, { id: 'BC8', code: 'OT', desc: 'OT Visit', disc: 'OT' }, { id: 'BC9', code: 'MSW', desc: 'MSW Visit', disc: 'MSW' }],
      ptFolders: PT_FOLDERS.slice(), staffFolders: STAFF_FOLDERS.slice(),
      evvReasons: ['Caregiver forgot to clock in', 'Caregiver forgot to clock out', 'Phone or GPS problem', 'Caregiver clocked in away from the home', 'Visit time changed by patient', 'Other (explain in notes)'],
      missedReasons: ['Patient not home', 'Patient refused', 'Patient hospitalized', 'Caregiver ill', 'Bad weather'],
      aideTitles: ['Bathing', 'Dressing', 'Toileting', 'Meal preparation', 'Skin care', 'Mouth care', 'Walking assistance', 'Light housekeeping'],
    },
  };
  D.seq = 5000;

  /* users: one practice login for each job in the manual (password for all: practice) */
  [['admin', 'Practice Administrator', 'Administrator', null], ['don', 'Practice DON', 'DON', null], ['intake', 'Practice Office/Intake', 'Office', null], ['scheduler', 'Practice Scheduler', 'Scheduler', null],
   ['hr', 'Practice HR', 'HR', null], ['rn', 'Rita Testnurse, RN', 'Nurse', 'S1'], ['hha', 'Sam Testaide, HHA', 'Aide', 'S2'], ['biller', 'Practice Biller', 'Biller', null]].forEach(([u, n, r, s], i) => D.users.push({ id: 'U' + (i + 1), username: u, name: n, role: r, staffId: s, active: true, pw: 'practice' }));

  /* staff (caregivers) */
  const mkStaff = (sid, last, first, disc, emp, extra) => Object.assign({
    id: sid, last, first, mi: '', empId: emp, disc, active: true, empType: 'Employee', dob: '1985-03-15', sex: 'Female', ssn: '000-00-' + emp.slice(-4), title: '', hire: '2024-02-01', term: '',
    addr1: '200 Practice Way', addr2: '', city: 'Tamarac', state: 'FL', zip: '33321', covZips: '33319, 33321, 33351', lic: disc === 'RN' ? 'RN9000' + emp.slice(-2) : '', exclPayroll: false,
    phones: { home: '', cell: '(954) 555-02' + emp.slice(-2), work: '', pager: '' }, noText: false, fax: '', email: first.toLowerCase() + '.' + last.toLowerCase() + '@practice.example', emName: 'Practice Contact', emPhone: '(954) 555-0300', comments: '',
    creds: {}, docs: [], absences: [], commLog: [], pay: [], avail: {}, cc: { enabled: false, user: '', invited: '' },
  }, extra || {});
  const cr = (days, rem) => ({ exp: T(addDaysS('2026-09-30', days)), remark: rem || '' });
  const s1 = mkStaff('S1', 'TESTNURSE', 'RITA', 'RN', 'E1001', { cc: { enabled: true, user: 'rn', invited: '2024-02-02' } });
  s1.creds = { LIC: cr(220), CPR: cr(20, 'renewal class booked'), TB: cr(150), PHY: cr(300), BGC: cr(500), I9: cr(900), HEPB: cr(400), COMP: cr(95), INS: cr(60) };
  const s2 = mkStaff('S2', 'TESTAIDE', 'SAM', 'HHA', 'E1002', { sex: 'Male', cc: { enabled: true, user: 'hha', invited: '2024-03-02' } });
  s2.creds = { LIC: cr(240), CPR: cr(120), TB: cr(-10, 'expired: screening scheduled'), PHY: cr(200), BGC: cr(500), I9: cr(900), HEPB: cr(400), COMP: cr(40), INS: cr(70) };
  const s3 = mkStaff('S3', 'TESTPT', 'PAT', 'PT', 'E1003', { lic: 'PT7000' + '03', cc: { enabled: true, user: 'pat', invited: '2024-05-02' } });
  s3.creds = { LIC: cr(310), CPR: cr(200), TB: cr(180), PHY: cr(45), BGC: cr(500), I9: cr(900), HEPB: cr(400), COMP: cr(130), INS: cr(70) };
  const s4 = mkStaff('S4', 'TESTLPN', 'LEE', 'LPN', 'E1004', { lic: 'LPN6000' + '04' }); s4.creds = { LIC: cr(15, 'renewal submitted'), CPR: cr(140), TB: cr(180), PHY: cr(250), BGC: cr(500), I9: cr(900), HEPB: cr(400), COMP: cr(130), INS: cr(70) };
  const s5 = mkStaff('S5', 'TESTRN', 'ALEX', 'RN', 'E1005', { sex: 'Male', cc: { enabled: true, user: 'alex', invited: '2024-06-02' } }); s5.creds = { LIC: cr(280), CPR: cr(160), TB: cr(180), PHY: cr(250), BGC: cr(500), I9: cr(900), HEPB: cr(400), COMP: cr(130), INS: cr(70) };
  const s6 = mkStaff('S6', 'OFFICE', 'PAM', 'OFFICE', 'E1006', { title: 'Office staff' });
  [s1, s2, s3, s4, s5, s6].forEach(s => { ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].forEach(d => (s.avail[d] = { on: true, from: '08:00', to: '17:00' })); ['Sat', 'Sun'].forEach(d => (s.avail[d] = { on: false, from: '', to: '' })); s.pay = [{ id: id('PR'), from: '2024-02-01', type: 'Hourly', rate: s.disc === 'RN' ? '38.00' : s.disc === 'HHA' ? '14.00' : '30.00' }]; });
  D.staff.push(s1, s2, s3, s4, s5, s6);
  D.staff[0].docs.push({ id: id('SD'), title: 'TESTNURSE_RITA_Credential_01152026', folder: 'CREDENTIAL ITEMS', created: '2026-01-15', fileName: 'license.png', fileId: '', by: 'U5' });

  /* patients */
  const mkP = (pid, last, first, dob, sex, extra) => Object.assign({
    id: pid, last, first, mi: '', suffix: '', dob, sex, ethnicity: '', addr1: '100 Practice Lane', addr2: '', city: 'Tamarac', state: 'FL', zip: '33319', instructions: '', mrn: pid.slice(1),
    ssn: '', medicare: '', medicaid: '', email: '', phones: { home: '(954) 555-01' + pid.slice(1).padStart(2, '0'), mobile: '', other: '' }, em: { name: '', phone1: '', phone2: '', email: '' },
    lang: 'ENGLISH', comments: '', altLocs: [], contacts: [], created: '2024-12-20', createdBy: 'U1', lat: 26.2, lng: -80.25,
  }, extra || {});
  const p1 = mkP('P1', 'DOE', 'JOHN', '2020-12-28', 'Male', { mrn: '1', ethnicity: 'Black or African-American', medicaid: '123456789', phones: { home: '(954) 555-0100', mobile: '(954) 555-1212', other: '' }, em: { name: 'MARIE DOE', phone1: '(954) 555-1386', phone2: '', email: '' }, ssn: '000-00-0001' });
  const p2 = mkP('P2', 'SAMPLE', 'MARIA', '1944-04-12', 'Female', { mrn: '2', ethnicity: 'Hispanic or Latino', medicare: '1AA2-BB3-CC44', addr1: '210 Sample Street', city: 'Tamarac', zip: '33321', phones: { home: '(954) 555-0201', mobile: '(954) 555-0202', other: '' }, em: { name: 'LUIS SAMPLE', phone1: '(954) 555-0203', phone2: '', email: '' }, instructions: 'Gate code 0000 (practice). Call from the driveway.', created: '2026-09-26', lat: 26.21, lng: -80.24 });
  const p3 = mkP('P3', 'ROE', 'JANE', '1939-11-02', 'Female', { mrn: '3', medicaid: '987654321', addr1: '33 Demo Court', zip: '33351', phones: { home: '(954) 555-0301', mobile: '', other: '' }, em: { name: 'PAT ROE', phone1: '(954) 555-0302', phone2: '', email: '' }, created: '2026-05-20' });
  const p4 = mkP('P4', 'SAMPLE', 'MARIA', '1957-07-21', 'Female', { mrn: '4', medicare: '9ZZ8-YY7-XX66', addr1: '55 Another Road', zip: '33313', phones: { home: '(954) 555-0401', mobile: '', other: '' }, em: { name: 'NO CONTACT LISTED', phone1: '', phone2: '', email: '' }, created: '2026-09-29' });
  D.patients.push(p1, p2, p3, p4);

  /* admissions */
  const adm = (aid, pid, status, admit, pan, physId, payer, extra) => Object.assign({
    id: aid, pid, status, admit, pan, office: 'Zenith Care Home Health LLC', county: '', physId, refPhysId: '', caseMgr: '', sourceOfAdm: '', refSource: '', transferred: false, dnr: false, dischDate: '', dischCode: '',
    ins: [{ id: id('IN'), resp: payer === 'PY1' ? 'Non-Insurance' : 'Primary', payer, from: admit, to: '', memberId: '' }], diag: [], disciplines: [], freq: [], other: { precautions: '' }, created: admit, inactive: false,
  }, extra || {});
  D.admissions.push(
    adm('A1', 'P1', 'Admitted', '2024-12-28', 1, 'PH1', 'PY1', { other: { precautions: 'Oxygen usage precautions, Seizure precautions, Aspiration precautions,' }, diag: [{ id: id('DX'), code: 'R56.9', desc: 'Unspecified convulsions (practice)', date: '2024-12-28', type: 'Primary' }], disciplines: ['RN', 'HHA'], freq: [{ id: id('FQ'), disc: 'RN', freq: '2w4', from: '2026-08-20', to: '2026-10-18' }] }),
    adm('A2', 'P2', 'Admitted', '2026-09-28', 2, 'PH2', 'PY2', { refSource: 'Sample General Hospital', sourceOfAdm: 'Hospital', diag: [{ id: id('DX'), code: 'I50.9', desc: 'Heart failure, unspecified (practice)', date: '2026-09-26', type: 'Primary' }], disciplines: ['RN', 'PT', 'HHA'], freq: [{ id: id('FQ'), disc: 'RN', freq: '2w4', from: '2026-09-28', to: '2026-11-26' }, { id: id('FQ'), disc: 'HHA', freq: '3w4', from: '2026-09-28', to: '2026-11-26' }, { id: id('FQ'), disc: 'PT', freq: '2w4', from: '2026-09-28', to: '2026-11-26' }], caseMgr: 'S1' }),
    adm('A3', 'P3', 'Discharged', '2026-05-22', 3, 'PH3', 'PY3', { dischDate: '2026-09-15', dischCode: 'Goals met', inactive: true }),
  );
  D.admissions[1].ins[0].memberId = p2.medicare;

  /* referrals */
  D.referrals.push({ id: id('RF'), pid: 'P2', date: '2026-09-26', source: 'Sample General Hospital', physId: 'PH2', physConfirmed: true, status: 'Admitted', office: 'Zenith Care Home Health LLC', comment: 'Heart failure, new start of care.', by: 'U3' },
    { id: id('RF'), pid: 'P4', date: '2026-09-29', source: 'Demo Family Clinic', physId: 'PH3', physConfirmed: false, status: 'In Progress', office: 'Zenith Care Home Health LLC', comment: 'Waiting for order and face-to-face.', by: 'U3' });

  /* documents (Electronic Health Records) for P2 */
  const doc = (pid, title, folder, created, kind, fname, by) => ({ id: id('D'), pid, title, folder, created, comment: '', fileName: fname, fileSize: '2 KB', fileId: putSeedFile(docUrl(kind, { name: ptName(P0(pid)), dob: fmtD(P0(pid).dob), date: created })), by: by || 'U3', deleted: false });
  function P0(pid) { return D.patients.find(p => p.id === pid); }
  D.docs.push(doc('P2', 'SAMPLE_MARIA_Referral_09262026', 'MEDICAL RECORDS', '2026-09-26', 'referral', 'referral.svg'), doc('P2', 'SAMPLE_MARIA_Order_09262026', 'PHYSICIAN ORDERS', '2026-09-26', 'order', 'order.svg'),
    doc('P2', 'SAMPLE_MARIA_F2F_09182026', 'MEDICAL RECORDS', '2026-09-26', 'f2f', 'f2f.svg'));

  /* orders (General Form) */
  D.orders.push({ id: id('OR'), pid: 'P2', date: '2026-09-26', title: 'Home health evaluate and treat', text: 'Skilled nursing, PT and aide for heart failure. Practice order.', sent: '2026-09-26', received: '2026-09-27', cgId: 'S1', status: 'Completed', signed: true, physId: 'PH2', by: 'U6' },
    { id: id('OR'), pid: 'P2', date: '2026-09-29', title: 'Increase aide visits to 4 per week', text: 'Practice order. Not yet returned.', sent: '2026-09-29', received: '', cgId: 'S1', status: 'Pending', signed: false, physId: 'PH2', by: 'U6' });

  /* assessments (OASIS) */
  D.assessments.push({ id: id('AS'), pid: 'P1', type: 'OASIS', compDate: '2025-01-11', reason: '', qa: 'In Use', exportStatus: 'In Use', hipps: '', payment: '0.00', lupa: '-', data: {}, by: 'U6' },
    { id: id('AS'), pid: 'P2', type: 'OASIS', compDate: '2026-09-28', reason: '01 Start of care', qa: 'In Use', exportStatus: 'In Use', hipps: '', payment: '0.00', lupa: '-', data: { m0100: '01', m0090: '2026-09-28' }, by: 'U6' });

  /* visits */
  const vis = (pid, cg, start, end, status, bc, billable, extra) => Object.assign({ id: id('V'), pid, cgId: cg, start, end, status, billingCode: bc, billable, comments: '', adminComments: '', location: '', travel: '', overtime: '', mileage: '', dontValidate: false, qaMon: false, createdBy: 'U4', evv: {}, noteId: '', docType: '' }, extra || {});
  const home2 = { lat: 26.21, lng: -80.24, where: "At the patient's home" }, car2 = { lat: 26.228, lng: -80.24, where: 'About 1.2 miles from the home' };
  const v1 = vis('P1', 'S1', '2026-09-16T08:00', '2026-09-16T09:00', 'C', 'BC2', false, { evv: { inAt: '2026-09-16T07:58', outAt: '2026-09-16T09:02', inGps: { lat: 26.2, lng: -80.25, where: "At the patient's home" }, outGps: { lat: 26.2, lng: -80.25, where: "At the patient's home" } } });
  const v1b = vis('P1', 'S1', '2026-05-03T08:00', '2026-05-03T09:00', 'N', 'BC2', false);
  const v2 = vis('P2', 'S1', '2026-09-28T10:00', '2026-09-28T11:00', 'C', 'BC1', true, { evv: { inAt: '2026-09-28T10:03', outAt: '2026-09-28T10:58', inGps: car2, outGps: home2 } });
  const v3 = vis('P2', 'S2', '2026-09-29T14:00', '2026-09-29T16:00', 'N', 'BC5', true, { evv: { inAt: '2026-09-29T14:02', outAt: '', inGps: home2, outGps: null } });
  const v4 = vis('P2', 'S5', '2026-09-30T07:30', '2026-09-30T08:30', 'N', 'BC2', true, { evv: { inAt: '2026-09-30T07:28', outAt: '', inGps: home2, outGps: null } });
  const v5 = vis('P2', 'S3', '2026-09-30T08:00', '2026-09-30T09:00', 'N', 'BC6', true);
  const v6 = vis('P2', 'S2', '2026-09-30T10:00', '2026-09-30T12:00', 'N', 'BC5', true);
  const v7 = vis('P2', 'S5', '2026-09-30T13:00', '2026-09-30T14:00', 'N', 'BC2', true);
  const v8 = vis('P2', 'S2', '2026-10-01T10:00', '2026-10-01T12:00', 'N', 'BC5', true);
  const v9 = vis('P2', 'S1', '2026-10-02T10:00', '2026-10-02T11:00', 'N', 'BC2', true);
  const v10 = vis('P2', 'S1', '2026-09-30T11:00', '2026-09-30T12:00', 'N', 'BC2', true);
  D.visits.push(v1, v1b, v2, v3, v4, v5, v6, v7, v8, v9, v10);

  /* SN notes */
  D.snNotes.push({ id: id('SN'), pid: 'P1', visitId: v1.id, date: '2026-09-16', cgId: 'S1', status: 'Completed', nurseSigned: true, patSigned: true, gps: true, visitType: 'Skilled Nursing', data: snFullData(), signedAt: '2026-09-16T11:35', qa: 'Completed', qaBy: 'U2', sigName: 'Rita Testnurse, RN', start: '2026-09-16T08:00', end: '2026-09-16T09:00' },
    { id: id('SN'), pid: 'P1', visitId: v1b.id, date: '2026-05-03', cgId: 'S1', status: 'In Use', nurseSigned: false, patSigned: false, gps: false, visitType: '', data: {}, signedAt: '', qa: 'In Use', start: '', end: '' },
    { id: id('SN'), pid: 'P2', visitId: v2.id, date: '2026-09-28', cgId: 'S1', status: 'Completed', nurseSigned: true, patSigned: true, gps: false, visitType: 'Skilled Nursing', data: snFullData(), signedAt: '2026-09-28T12:20', qa: 'Pending', sigName: 'Rita Testnurse, RN', start: '2026-09-28T10:03', end: '2026-09-28T10:58' });
  v1.noteId = D.snNotes[0].id; v1b.noteId = D.snNotes[1].id; v2.noteId = D.snNotes[2].id;
  v1.status = 'C'; v2.status = 'C';

  /* 485 and aide documents */
  D.f485.push({ id: id('CP'), pid: 'P1', from: '2024-12-28', to: '2025-02-25', sent: '', recd: '', status: 'Completed', encounterType: '', data: {} },
    { id: id('CP'), pid: 'P2', from: '2026-09-28', to: '2026-11-26', sent: '', recd: '', status: 'In Use', encounterType: '', data: {} });
  D.aideDocs.push({ id: id('AD'), pid: 'P2', kind: 'poc', title: 'Aide Plan of Care', cgId: 'S1', from: '2026-09-28', to: '2026-11-26', status: 'Completed', tasks: ['Bathing', 'Dressing', 'Skin care'], freq: '3 times a week' });
  D.commLog.push({ id: id('CL'), pid: 'P2', date: '2026-09-26T15:10', type: 'Phone call', note: 'Called daughter to confirm referral details (practice entry).', by: 'U3' });
  D.messages.push({ id: id('M'), to: 'U3', from: 'U2', subject: 'Welcome to practice', body: 'Practice message. Use the left menu to try the screens in your manual. Nothing here is real.', date: '2026-09-29T08:00', read: false },
    { id: id('M'), to: 'U3', from: 'U1', subject: 'Reminder: search twice before + Add', body: 'Practice message: search twice before you add a new patient.', date: '2026-09-29T09:15', read: false },
    { id: id('M'), to: 'U3', from: 'U6', subject: 'Order not yet returned (SAMPLE, MARIA)', body: 'Practice message: the 09/29 order has no received date yet.', date: '2026-09-30T07:45', read: false });
  return D;
}
function addDaysS(iso, n) { const d = new Date(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10)); d.setDate(d.getDate() + n); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
let SEED_FILES = {};
function putSeedFile(url) { const id = 'FS' + (Object.keys(SEED_FILES).length + 1); SEED_FILES[id] = url; return id; }

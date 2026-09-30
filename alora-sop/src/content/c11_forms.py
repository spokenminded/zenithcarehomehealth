"""Tab 11: SOC Desk Checklist, printable forms, Quick Cards, Live Alora Verification Worksheet, training sign-off, glossary.

Every paper form in this tab is printed from the same definition that draws the picture of it in the procedures,
so the picture and the real form can never disagree.
"""
import importlib
import math

import scenes2
import ui
from model import Proc, Text, Divider, md
from blocks import *

# ----------------------------------------------------------------------------- scan every procedure once
_MODS = ['c2_signin', 'c3_patients', 'c4_documents', 'c5_soc', 'c6_schedule', 'c7_monitor', 'c8_billing', 'c9_routines']
PROCS = []
USED = {}          # ui key -> [step ids]
for _n in _MODS:
    _mod = importlib.import_module('content.' + _n)
    for _p in _mod.PAGES:
        if isinstance(_p, Proc):
            PROCS.append(_p)
            scenes2.CUR[0] = _p.num
            for _s in _p.steps:
                _m = _s.mock()
                for _c in _m.calls:
                    if _c['key'] and _c['key'] != 'zenith':
                        USED.setdefault(_c['key'], [])
                        if _s.id not in USED[_c['key']]:
                            USED[_c['key']].append(_s.id)
scenes2.CUR[0] = None

# forms drawn only here (no picture in a procedure)
scenes2.CUR[0] = 'P26'
scenes2.zform('PROBLEM REPORT', [
    ('h', 'WHO AND WHEN'), ('two', 'emp', 'Employee:', 'dt', 'Date and time:'),
    ('h', 'WHAT YOU SAW'), ('line', 'scr', 'Screen or step (manual page):'), ('line', 'exp', 'What the manual said you should see:'),
    ('line', 'saw', 'What you saw instead (exact words of any message):'),
    ('h', 'WHAT YOU DID'), ('line', 'did', 'What you did:'), ('line', 'told', 'Who you told (name, time):'),
    ('h', 'ADMINISTRATOR'), ('line', 'act', 'Action taken:')])
scenes2.CUR[0] = 'P5B'
scenes2.zform('NEW PATIENT CHECK', [
    ('h', 'PATIENT FROM THE REFERRAL'), ('two', 'pt', 'Name:', 'dob', 'DOB:'),
    ('h', 'THREE SEARCHES IN ALORA (NOTHING FOUND)'), ('line', 's1', 'Search 1 (what you typed):'), ('line', 's2', 'Search 2 (shorter spelling):'),
    ('line', 's3', 'Search 3 (birth date, maiden name or nickname):'),
    ('h', 'OK TO ADD THE PATIENT'), ('line', 'ok', 'DON or Administrator initials and date:'), ('check', 'ref', 'Referral accepted by the DON')])
scenes2.CUR[0] = None

FORM_ORDER = [
    'SOC PACKET INTAKE LOG', 'PACKET CHECKLIST', 'REFERRAL REVIEW', 'REFERRAL DECISION', 'NEW PATIENT CHECK', 'RECORD CORRECTION REQUEST',
    'DOCUMENT VERIFICATION', 'DOCUMENT PROBLEM REPORT', 'ORDER REVIEW SHEET', 'FACE-TO-FACE REVIEW SHEET',
    'SOC READINESS CHECK', 'SOC ASSIGNMENT', 'SOC CALL NOTES',
    'VISIT SCHEDULING REQUEST', 'VISIT NOTICE LOG', 'VISIT FREQUENCY CHECK', 'SCHEDULE CHANGE APPROVAL', 'CHANGE NOTICE LOG',
    'LATE OR MISSED VISIT LOG', 'EXCEPTION FOLLOW-UP', 'CLINICAL DOCUMENT TRACKER', 'QA COMPLETENESS CHECK', 'QA LOG',
    'BILLING READINESS CHECK', 'NOA CHECK', 'NOA TRACKING LOG',
    'DAILY OFFICE ALORA CHECK', 'WEEKLY OFFICE ALORA CHECK', 'CERTIFICATION PERIOD WATCH', 'MONTHLY OFFICE ALORA CHECK', 'DISCHARGE CHECK',
    'PROBLEM REPORT', 'SCAN SETTINGS']
_EXCLUDE = {'SOC DESK CHECKLIST (EXTRACT)'}
_extra = [t for t in scenes2.ZFORMS if t not in FORM_ORDER and t not in _EXCLUDE]
if _extra:
    print('NOTE: forms not in FORM_ORDER, appended:', _extra)
FORM_ORDER += _extra
FORM_ORDER = [t for t in FORM_ORDER if t in scenes2.ZFORMS]
FORM_NO = {t: i + 1 for i, t in enumerate(FORM_ORDER)}


def form_id(title):
    return 'form-' + ''.join(ch.lower() if ch.isalnum() else '-' for ch in title).strip('-')


def _used(title):
    u = scenes2.ZUSE.get(title, [])
    return ', '.join(u) if u else 'any time'


# ============================================================================= SOC desk checklist (one page)
def _sec(title, refs, items):
    lis = ''.join(f'<li>{md(i)}</li>' for i in items)
    return (f'<section class="dsec"><h4><span>{md(title)}</span><small>{md(refs)}</small><em>Init. <i class="blank"></i></em></h4>'
            f'<ul class="checks big">{lis}</ul></section>')


def _checklist_html():
    left = (_sec('Patient', 'P3 to P5, {{pg:find}}', ['Correct patient found', 'Demographics reviewed', 'No duplicate identified'])
            + _sec('Referral', 'P6, {{pg:referral}}', ['Referral received', 'Referral reviewed', 'Referral uploaded', 'Correct patient record confirmed'])
            + _sec('Orders', 'P11, {{pg:orders}}', ['Physician order received', 'Physician order uploaded', 'Physician order reviewed'])
            + _sec('Face-to-Face', 'P12, {{pg:f2f}}', ['Face-to-Face reviewed', 'Face-to-Face uploaded when required', 'Dates verified'])
            + '<section class="dsec"><h4><span>Notes</span></h4><p class="blank wide"></p><p class="blank wide"></p><p class="blank wide"></p></section>')
    right = (_sec('Documents', 'P7U, {{pg:socupload}}', ['All required documents uploaded', 'Documents open correctly', 'Documents legible', 'No duplicate documents'])
             + _sec('Scheduling', 'P13, {{pg:socprep}}', ['SOC visit scheduled', 'Appropriate discipline assigned', 'Schedule verified'])
             + _sec('Final check', 'P7, {{pg:socstages}}', ['Patient ready for clinical workflow', 'QA items complete', 'Administrator/DON notified of unresolved issues'])
             + '<section class="dsec"><h4><span>Unresolved issues</span></h4><p class="blank wide"></p><p class="blank wide"></p><p class="blank wide"></p></section>'
             + '<section class="dsec"><h4><span>Administrator / DON told</span></h4><p class="blank wide"></p></section>')
    return ('<div class="dcl"><div class="dcl-head"><div class="dcl-org">ZENITH CARE HOME HEALTH</div><h1>SOC PROCESSING DESK CHECKLIST</h1></div>'
            '<div class="dcl-fields"><div><b>PATIENT</b><i class="blank"></i></div><div><b>DOB</b><i class="blank"></i></div>'
            '<div><b>REFERRAL DATE</b><i class="blank"></i></div><div><b>SOC DATE</b><i class="blank"></i></div></div>'
            '<div class="dcl-fields clocks"><div><b>REFERRAL RECEIVED (DATE, TIME)</b><i class="blank"></i></div><div><b>48-HOUR DEADLINE</b><i class="blank"></i></div>'
            '<div><b>NOA DUE (SOC + 5 DAYS)</b><i class="blank"></i></div></div>'
            f'<div class="dcl-cols"><div>{left}</div><div>{right}</div></div>'
            '<div class="dcl-foot"><span><b>Employee initials</b> <i class="blank"></i></span><span><b>Date</b> <i class="blank"></i></span></div></div>')


CHECKLIST = Text('soc-checklist', 11, 'SOC Desk Checklist (one page)', _checklist_html, kind='form')


# ============================================================================= printable forms
def _form_html(title):
    sections = scenes2.ZFORMS[title]
    n = FORM_NO[title]
    out = [f'<div class="fhead"><div class="fb">ZENITH CARE HOME HEALTH, LLC</div><h1>{md(title)}</h1>'
           f'<div class="fno">Form F{n:02d} · Used in {md(_used(title))} · Print a new copy each time</div></div><div class="fbody">']
    checks = []

    def flush():
        if checks:
            out.append('<ul class="checks">' + ''.join(f'<li>{md(c)}</li>' for c in checks) + '</ul>')
            checks.clear()
    for sct in sections:
        k = sct[0]
        if k != 'check':
            flush()
        if k == 'h':
            out.append(f'<h4>{md(sct[1].title() if False else sct[1])}</h4>')
        elif k == 'line':
            out.append(f'<div class="frow"><span class="f"><span class="lb">{md(sct[2])}</span><i class="blank"></i></span></div>')
        elif k == 'two':
            out.append(f'<div class="frow"><span class="f"><span class="lb">{md(sct[2])}</span><i class="blank"></i></span>'
                       f'<span class="f"><span class="lb">{md(sct[4])}</span><i class="blank"></i></span></div>')
        elif k == 'check':
            checks.append(sct[2])
        elif k == 'kv':
            out.append(f'<div class="fkv"><span>{md(sct[2])}</span><b>{md(sct[3])}</b></div>')
        elif k == 'text':
            out.append(f'<p class="fnote">{md(sct[1])}</p>')
        elif k == 'gap':
            out.append('<div style="height:6px"></div>')
    flush()
    if title != 'SCAN SETTINGS':
        out.append('<h4>Notes</h4>' + '<p class="blank wide"></p>' * 4)
    out.append('</div>')
    return ''.join(out)


FORM_PAGES = [Text(form_id(t), 11, f'Form F{FORM_NO[t]:02d}: {t.title() if t != "SCAN SETTINGS" else "Scan settings card"}', (lambda t=t: _form_html(t)), kind='form')
              for t in FORM_ORDER]


def _index_rows(titles):
    return [[f'F{FORM_NO[t]:02d}', f'**{t.title().replace("Soc ", "SOC ").replace("Noa ", "NOA ").replace("Qa ", "QA ").replace("Face-To-Face", "Face-to-Face")}**',
             _used(t), '{{pg:' + form_id(t) + '}}'] for t in titles]


def _index_html(part):
    half = math.ceil(len(FORM_ORDER) / 2)
    titles = FORM_ORDER[:half] if part == 0 else FORM_ORDER[half:]
    return (f'<h1 class="ttl">Forms index ({part + 1} of 2)</h1>'
            '<p class="sub">Every paper form used in this manual. Make copies from these pages. Each procedure names the forms it needs on its start page.</p>'
            + TABLE(['No.', 'Form', 'Used in', 'Page'], _index_rows(titles), widths=['9%', '51%', '28%', '12%']))


INDEX_PAGES = [Text('forms-index-1', 11, 'Forms index (1 of 2)', lambda: _index_html(0), kind='text'),
               Text('forms-index-2', 11, 'Forms index (2 of 2)', lambda: _index_html(1), kind='text')]


# ============================================================================= quick cards
def _qcard(n, title, pid, steps, stop, donot, extra=''):
    def html():
        lis = ''.join(f'<li>{md(s)}</li>' for s in steps)
        return (f'<div class="qtop"><div class="qn">Quick Card {n} of 6 · Keep beside the computer</div><h1>{md(title)}</h1></div>'
                f'<ol class="qsteps">{lis}</ol>{extra}'
                + GRID2(KBOX('Stop and ask the Administrator or DON if', UL(stop), 'red'), KBOX('Do not', UL(donot), 'gold'))
                + f'<p class="qfoot">Full procedure with pictures: {md("{{pg:" + pid + "}}")}. Button names in your Alora may differ from these words. '
                  'Write the real names in the margin once the Administrator has verified them.</p>')
    return html


QCARDS = [
    Text('qc-1', 11, 'Quick Card 1: How to Find a Patient', _qcard(
        1, 'How to Find a Patient', 'find',
        ['Sign in to Alora (your own login). Click **Patients** in the main menu.', 'Click the **search box**. Type the **last name**.',
         'If there is a **date of birth** box, type the birth date.', 'Click **Search**.',
         'Read **every row**: name, date of birth, record number.', 'Match **two things**: the name AND the date of birth.',
         'One match: click that **row** to open the record.', 'Read the **banner name** before you do anything else.'],
        ['Two patients match.', 'No patient matches after three searches.', 'The status is not what you expected.'],
        ['Do not create a patient after one search.', 'Do not open a row because it looks close.', 'Do not keep two patients open.']), kind='qcard'),
    Text('qc-2', 11, 'Quick Card 2: How to Upload a Document', _qcard(
        2, 'How to Upload a Document', 'upload',
        ['**Scan**: PDF, 300 dpi, one patient, one document type.', '**Name** it: LASTNAME_FIRSTNAME_TYPE_YYYYMMDD.pdf. Save it in **Ready to upload**.',
         '**Open** the file. Check the name and the pages.', '**Find the patient** (Card 1). Banner name = file name.', 'Click the **Documents** section. Is it already listed? If yes, stop.',
         'Click **Add**, then **Choose file**. Pick your file. Click **Open**.', 'Choose the **document type**. Type the **document date**.',
         'Check patient, file, type, date. Click **Save once**.', '**Verify** (Card 4).'],
        ['The banner name is not the file name.', 'No document type matches.', 'An error appears.', 'The document is in the wrong chart: tell the Administrator **now**.'],
        ['Do not upload into the wrong chart.', 'Do not click Save twice.', 'Do not delete a document.']), kind='qcard'),
    Text('qc-3', 11, 'Quick Card 3: SOC Processing', _qcard(
        3, 'SOC Processing (14 stages)', 'soc-flow',
        ['**Receive**: write the arrival time.', '**Review**: same name on every page. DON decides.', '**Find or create** the patient (search three ways first).', '**Open** the record. Name and birth date match.',
         '**Upload** referral, order, face-to-face.', '**Verify** each document opens.', '**Enter and verify** patient information.', '**Verify orders**: signed and dated.', '**Verify face-to-face**: date in the window.',
         '**Prepare and schedule** the SOC visit. 48-hour limit.', '**Verify** the clinical workflow is in place.', '**Monitor** the visit.', '**QA**: complete and sent on.', '**Billing**: NOA within 5 calendar days.'],
        ['The 48-hour limit cannot be met.', 'The order or face-to-face is missing or not valid.', 'A document is in the wrong chart.'],
        ['Do not skip a stage.', 'Do not tick a box you did not do.', 'Do not schedule before the DON names the nurse.']), kind='qcard'),
    Text('qc-4', 11, 'Quick Card 4: Document Verification', _qcard(
        4, 'Document Verification', 'verify',
        ['Open the patient\'s **document list**.', 'Find each document you uploaded. **Once each.**', 'Click the document to **open** it.', 'Read the **patient name** and **date of birth** on the page.',
         'Look at **every page**. All readable?', 'Check the **type** and the **document date**.', 'Fill in the **Document Verification** form. Initial it.', 'Orders and face-to-face: a **second person** checks too.'],
        ['A document is in the wrong chart.', 'A document will not open or cannot be read.', 'You find a duplicate.', 'The type does not match the paper.'],
        ['Do not delete or rename a document.', 'Do not assume it is fine because the upload finished.', 'Do not remove the scan file before you verify.']), kind='qcard'),
    Text('qc-5', 11, 'Quick Card 5: Scheduling', _qcard(
        5, 'Scheduling a Visit', 'schedule',
        ['Get the **signed Visit Scheduling Request** from the DON.', 'Click **Schedule** in the main menu.', 'Click **Add visit**.', 'Choose **patient**, **visit type**, **team member**.',
         'Enter **date**, **time**, **repeat** (same number of visits as the order).', 'Read **every alert**.', 'Click **Save once**.', 'Check the **calendar**: once, right day, right person.', '**Tell** the team member and the patient.'],
        ['There is no signed request.', 'An alert names a conflict, a missing authorization or a frequency problem.', 'A start of care visit cannot be inside 48 hours.', 'An error appears.'],
        ['Do not change the ordered frequency.', 'Do not use a team member the DON did not name.', 'Do not click Save twice.']), kind='qcard'),
    Text('qc-6', 11, 'Quick Card 6: Daily Office Alora Check', _qcard(
        6, 'Daily Office Alora Check', 'daily',
        ['**Sign in** with your own login.', 'Read **pending items** and the **NOA box**. NOA due today goes to billing.', 'Check the **Live Monitor**. Call about every late visit.',
         'Open the **exception list**. Start a follow-up for each new one.', 'Look at **today\'s schedule**. Every visit has a team member.', '**Midday**: Live Monitor again.',
         '**One hour before the end of the day**: Live Monitor again.', 'Check the **scan folder**: only files still waiting.', '**Log out**. Lock the computer (Windows key + L). Initial the sheet.'],
        ['An NOA is due today and not sent.', 'A start of care visit is late or missed.', 'An exception is older than 2 business days.', 'A patient file is where it should not be.'],
        ['Do not skip a step on a busy day.', 'Do not tick a box you did not do.', 'Do not sign in as someone else.']), kind='qcard'),
]


# ============================================================================= live Alora verification worksheet
def _ws_rows():
    rows = []
    for key in ui.all_keys():
        if key not in USED:
            continue
        st = ui.status(key)
        if st not in ('VERIFY', 'FEATURE'):
            continue
        desc, feat = ui.REG[key]
        pages = USED[key]
        pg = ', '.join('{{pg:' + p + '}}' for p in pages[:3]) + (f' +{len(pages) - 3} more' if len(pages) > 3 else '')
        rows.append((key, desc, feat, pg, st))
    return rows


WS_ROWS = _ws_rows()
WS_PER = 12
WS_PAGES_N = math.ceil(len(WS_ROWS) / WS_PER)


def _ws_intro():
    return ('<h1 class="ttl">Live Alora Verification Worksheet</h1>'
            '<p class="sub">The pictures in this manual are training mockups. Nobody has checked them against Zenith\'s live Alora account yet. '
            'This worksheet is how that check is done, once, by the Administrator.</p>'
            + KBOX('How to do the check (about 2 hours, at an office computer, signed in to live Alora)', OL([
                'Sit with the Administrator. Open live Alora. Do **not** type or save anything in a real patient record.',
                'Go down the worksheet one row at a time. For each row, open the screen named on the pages shown in the third column.',
                'Write the **exact words** Alora shows for that button, menu or box in the \'Alora says\' column. Write **where it is** (for example \'left menu, third item\').',
                'If the row says \'Alora feature documented\', the feature exists. You are confirming only the words and the place.',
                'If a row does not exist in your Alora, write **NONE** and the real way to do the task. Tell the Administrator. That step of the manual must be rewritten.',
                'When a row is correct, initial the last column.',
                'Give the finished worksheet to the person who maintains this manual. They enter the real names and the manual is reissued. Pictures then show \'verified\'.']), 'gold')
            + KBOX('What the two tags mean', UL([
                '**Verify** (dashed gold): nothing public confirms this name or place. Verify it.',
                '**Alora feature** (blue): Alora publicly describes this feature by name (from its website and review sites). The exact menu or button text and its place are still to verify.']), 'blue')
            + P(f'There are **{len(WS_ROWS)} rows** on the next {WS_PAGES_N} pages. Rows for paper forms and Windows screens are not on this list because they are not Alora screens.')
            + '<div class="sign"><div><div class="ln"></div><small>Checked by (Administrator)</small></div><div><div class="ln"></div><small>Date</small></div>'
              '<div><div class="ln"></div><small>Alora version or release date shown on screen (if any)</small></div><div><div class="ln"></div><small>Browser used</small></div></div>')


def _ws_page(i):
    chunk = WS_ROWS[i * WS_PER:(i + 1) * WS_PER]
    body = ''
    for key, desc, feat, pg, st in chunk:
        tag = '<span class="chip feature">FEATURE</span>' if st == 'FEATURE' else '<span class="chip verify">VERIFY</span>'
        body += ('<tr><td>' + tag + f'<br><b>{md(desc)}</b><br><small>{key}</small></td><td><small>{md(pg)}</small></td>'
                 f'<td><small>{md(feat) if feat else ""}</small></td><td class="wr"></td><td class="wr"></td><td class="ck"></td></tr>')
    return (f'<h1 class="ttl">Live Alora Verification Worksheet ({i + 1} of {WS_PAGES_N})</h1>'
            '<table class="t ws"><thead><tr><th style="width:24%">What the manual calls it</th><th style="width:12%">Pages</th><th style="width:17%">Documented feature</th>'
            '<th style="width:21%">Alora says (exact words)</th><th style="width:18%">Where it is</th><th style="width:8%">Init.</th></tr></thead>'
            f'<tbody>{body}</tbody></table>')


WS_PAGES = [Text('ws-intro', 11, 'Live Alora Verification Worksheet: instructions', _ws_intro, kind='text')] + [
    Text(f'ws-{i + 1}', 11, f'Live Alora Verification Worksheet ({i + 1} of {WS_PAGES_N})', (lambda i=i: _ws_page(i)), kind='text') for i in range(WS_PAGES_N)]


# ============================================================================= training sign-off
def _signoff_rows():
    rows = []
    for p in PROCS:
        rows.append([f'**{md(p.num)}**', md(p.title), '', '', ''])
    return rows


SIGN_PER = 19
_SIGN_ROWS = _signoff_rows()
SIGN_N = math.ceil(len(_SIGN_ROWS) / SIGN_PER)


def _sign_page(i):
    chunk = _SIGN_ROWS[i * SIGN_PER:(i + 1) * SIGN_PER]
    head = ('<h1 class="ttl">Training sign-off</h1>'
            '<p class="sub">A procedure is signed off when the trainee has done it alone, at a real Alora screen, from this manual, and the trainer checked the result. '
            'The test is: could a new employee who has never used Alora follow the pictures and finish the task?</p>')
    if i == 0:
        head += ('<div class="frow"><span class="f"><span class="lb">Trainee:</span><i class="blank"></i></span><span class="f"><span class="lb">Trainer:</span><i class="blank"></i></span></div>'
                 '<div class="frow"><span class="f"><span class="lb">Start date:</span><i class="blank"></i></span><span class="f"><span class="lb">Alora login created on:</span><i class="blank"></i></span></div>')
    return head + TABLE(['Proc.', 'Procedure', 'Trainer showed (initials)', 'Did it alone, correct (initials)', 'Date'], chunk, cls='tight signtbl', widths=['8%', '42%', '17%', '20%', '13%'])


SIGN_PAGES = [Text(f'signoff-{i + 1}', 11, f'Training sign-off ({i + 1} of {SIGN_N})', (lambda i=i: _sign_page(i)), kind='text') for i in range(SIGN_N)]


# ============================================================================= glossary
GLOSS = [
    ('Administrator', 'The person who runs Zenith and approves changes. You stop and ask the Administrator when this manual says so.'),
    ('Alert', 'A warning Alora shows, for example a scheduling conflict. Read it. Do not click through it.'),
    ('Alora', 'The web system Zenith uses for patient records, scheduling, visit tracking, quality review and billing. Office staff use it in a browser on a Windows computer.'),
    ('Certification period', 'Up to 60 days of care covered by one plan of care.'),
    ('Chart (patient record)', 'Everything stored about one patient.'),
    ('Claim', 'A bill sent to an insurance company or program for care given.'),
    ('Demographics', 'Basic facts about a patient: name, birth date, address, phone, language, emergency contact.'),
    ('Discharge', 'The end of care for a patient.'),
    ('Discipline', 'A kind of care worker: nurse (RN), physical therapist (PT), occupational therapist (OT), speech therapist (ST), aide, social worker (MSW).'),
    ('DON', 'Director of Nursing. The nurse leader who decides clinical questions and names the nurse for each start of care.'),
    ('Document type', 'The label you choose when you upload a document, for example referral. It helps everyone find the document later.'),
    ('Duplicate', 'A second copy of the same patient or the same document. Duplicates cause errors. Report them. Do not delete them.'),
    ('EVV', 'Electronic visit verification. Proof from a phone or device that a visit happened: who, where and when.'),
    ('Exception', 'A visit record that does not match the plan, for example a missing clock-out.'),
    ('Face-to-face (F2F)', 'A visit in which a physician or allowed practitioner saw the patient in person. Medicare requires it for home health.'),
    ('HIPAA', 'The federal law that protects the privacy of health information.'),
    ('Live Monitor', 'An Alora screen that shows visits as they happen, with warnings for late visits and no-shows.'),
    ('MBI', 'Medicare Beneficiary Identifier. The patient\'s Medicare number.'),
    ('NOA', 'Notice of Admission. It tells Medicare that a patient has started care. It is due within 5 calendar days of the start of care.'),
    ('NPI', 'National Provider Identifier. A 10-digit number that identifies a physician or other provider.'),
    ('OASIS', 'A standard assessment a nurse or therapist completes at start of care and at other times. Its answers are sent to Medicare.'),
    ('Payer', 'The one who pays for care: Medicare, Medicaid or an insurance company.'),
    ('Physician order', 'A written instruction from a doctor for the care a patient will receive.'),
    ('Plan of care (485)', 'The document that lists a patient\'s care, goals and how often visits happen. The physician signs it.'),
    ('Protected health information (PHI)', 'Any detail that can identify a patient and relates to health or care. Treat everything in Alora as PHI.'),
    ('QA', 'Quality assurance. A check that work is complete and correct before it moves on.'),
    ('Recertification', 'A new assessment near the end of a 60-day period when care continues.'),
    ('Referral', 'A request for Zenith to care for a patient, from a doctor, hospital or family.'),
    ('Scan', 'To make a digital copy of a paper.'),
    ('Start of care (SOC)', 'The date of the first visit that starts care for a new patient.'),
    ('Team member', 'A person who goes to visits: a nurse, therapist or aide.'),
    ('Upload', 'To copy a file from the office computer into Alora.'),
    ('Verify', 'To prove something is true by checking it yourself.'),
]


def _gloss_html(part):
    half = math.ceil(len(GLOSS) / 2)
    items = GLOSS[:half] if part == 0 else GLOSS[half:]
    return (f'<h1 class="ttl">Glossary ({part + 1} of 2)</h1><p class="sub">Words used in this manual, in plain language.</p>'
            '<dl class="gl">' + ''.join(f'<dt>{md(t)}</dt><dd>{md(d)}</dd>' for t, d in items) + '</dl>')


GLOSS_PAGES = [Text('gloss-1', 11, 'Glossary (1 of 2)', lambda: _gloss_html(0), kind='text'), Text('gloss-2', 11, 'Glossary (2 of 2)', lambda: _gloss_html(1), kind='text')]

for _t in [CHECKLIST, INDEX_PAGES[0], WS_PAGES[0], SIGN_PAGES[0], GLOSS_PAGES[0]] + QCARDS:
    _t.toc = True


PAGES = ([Divider(11, 'The SOC Desk Checklist, every paper form, six printable Quick Cards, the Live Alora Verification Worksheet, training sign-off and the glossary.',
                  [('soc-checklist', 'SOC Desk Checklist (one page)'), ('forms-index-1', 'Forms index'), ('qc-1', 'Quick Card 1: How to Find a Patient'), ('qc-2', 'Quick Card 2: How to Upload a Document'),
                   ('qc-3', 'Quick Card 3: SOC Processing'), ('qc-4', 'Quick Card 4: Document Verification'), ('qc-5', 'Quick Card 5: Scheduling'), ('qc-6', 'Quick Card 6: Daily Office Alora Check'),
                   ('ws-intro', 'Live Alora Verification Worksheet'), ('signoff-1', 'Training sign-off'), ('gloss-1', 'Glossary')]),
          CHECKLIST] + QCARDS + INDEX_PAGES + FORM_PAGES + WS_PAGES + SIGN_PAGES + GLOSS_PAGES)

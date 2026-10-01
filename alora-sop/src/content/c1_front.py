"""Tab 1: cover, document control, how to use this binder, what is verified, roles, stop rules, Zenith standards, Alora access sheet."""
import ui
import scenes as S
from model import Text, Divider, md
from blocks import *

EDITION = 'Version 2.0 DRAFT'
DOC_NO = 'ZCHH-SOP-ALORA-OFFICE-001'

# ============================================================================= cover
COVER = Text('cover', 1, 'Cover', (
    '<div class="band"><div class="logo"><img src="{logo}" alt="Zenith Care Home Health"></div>'
    '<div class="eyebrow">Standard Operating Procedure · Office staff</div>'
    '<h1>Alora Office<br>Operating Manual</h1>'
    '<p>Step-by-step procedures for the Alora website, on the office Windows computer. Start of Care, documents, scheduling, monitoring, billing readiness and daily checks.</p></div>'
    '<div class="gold"></div>'
    '<div class="lower">'
    ''
    + TABLE(['Document', 'Edition', 'Issued to', 'Binder copy'], [[f'{DOC_NO}', f'{EDITION}, September 2026', '<span class="blank" style="min-width:1.6in"></span>', '<span class="blank" style="min-width:0.6in"></span>']], cls='tight')
    + '<h3 style="margin-top:14px">Inside this binder</h3><ol class="tablist">' + ''.join(f'<li><b>{n}</b> {md(t)}</li>' for n, t in [
        (1, 'Start Here: how it works, what is verified, who does what'), (2, 'Sign In and Navigate: login, dashboard, HIPAA'), (3, 'Patient Records: find, open, check, create'),
        (4, 'Documents and Orders: referral, scan, upload, verify, orders, face-to-face'), (5, 'Start of Care (SOC) Workflow: all 14 stages, SOC document upload, scheduling the SOC visit'),
        (6, 'Scheduling: add, view and change visits'), (7, 'Monitoring and Review: Live Monitor, EVV exceptions, clinical documents, QA'), (8, 'Billing and NOA'),
        (9, 'Daily, Weekly and Monthly Checks'), (10, 'Problems and Approvals: troubleshooting, what needs approval, who to call'),
        (11, 'Forms and Quick Cards: SOC Desk Checklist, forms, six quick cards, worksheet')]) + '</ol>'
    + '<div class="draft">DRAFT FOR ADMINISTRATOR REVIEW.<br>The pictures in this manual are <b>training mockups, not screenshots</b>. '
      'No screen, button or menu name has been checked against Zenith\'s live Alora account yet. Zenith standards in the text are proposed and not yet approved. '
      'Read {{pg:verify-status}}, then complete the Live Alora Verification Worksheet (Tab 11) before you train anyone from this manual.</div>'
    '<p style="margin-top:12px;font-size:9pt;color:#5B6472">Desktop website only. This manual does not cover the mobile app or field clinician work. '
    'Zenith Care Home Health, LLC. Uncontrolled when printed: check that your edition matches the latest edition held by the Administrator.</p>'
    '</div>'
), kind='cover')


# ============================================================================= document control
DOC_CONTROL = Text('doccontrol', 1, 'Document control', (
    '<h1 class="ttl">Document control</h1>'
    '<p class="sub">Keep this page at the front of the binder. It says which edition you are holding, who owns it, and whether it is approved for training.</p>'
    + TABLE(['Item', 'Detail'], [
        ['Title', 'Alora Office Operating Manual: Step-by-Step Office Procedures'],
        ['Document number', DOC_NO],
        ['Edition', f'{EDITION}. September 2026.'],
        ['Owner', 'The Administrator, Zenith Care Home Health, LLC'],
        ['Applies to', 'Office employees who use the **Alora website on a Windows desktop computer**.'],
        ['Does not cover', 'The mobile app, field clinician workflows, and clinical documentation. Office staff never complete clinical forms.'],
        ['Review', 'Every year, and every time Alora changes a screen that this manual shows.'],
        ['Copy status', '**Uncontrolled when printed.** A printed page may be out of date. Ask the Administrator for the latest edition.'],
        ['Training use', 'Not approved until the Administrator signs below **and** the Live Alora Verification Worksheet (Tab 11) is complete.'],
    ], widths=['24%', '76%'], cls='tight')
    + H('Revision history')
    + TABLE(['Edition', 'Date', 'What changed', 'By'], [
        ['1.0', 'Earlier', 'General guide to Alora for all staff. Replaced.', ''],
        ['2.0 DRAFT', 'September 2026', 'Rebuilt as a step-by-step office manual. Desktop website only. One workflow for Start of Care. Training mockups with verification tags. Forms, checklist and quick cards added.', ''],
        ['', '', '', ''], ['', '', '', '']], widths=['14%', '18%', '54%', '14%'], cls='tight')
    + H('Approval')
    + P('I confirm that this edition may be used to train Zenith office employees. I confirm that the Zenith standards on the Standards pages are correct, and that the Live Alora Verification Worksheet was completed on the date shown.')
    + SIGN(['Administrator name and signature', 'Date approved', 'Director of Nursing name and signature', 'Live Alora verification completed on (date)'])
    + KBOX('What this manual is based on', UL([
        '**Alora:** public product information, used only to name features. Zenith\'s live Alora account was **not** available when this edition was written.',
        '**Medicare and HIPAA:** the Medicare Conditions of Participation for home health agencies (42 CFR 484), the face-to-face requirement (42 CFR 424.22), Medicare payment rules for the Notice of Admission, and the HIPAA Security Rule (45 CFR 164.312).',
        '**Florida:** section 415.1034, Florida Statutes (reporting of abuse, neglect and exploitation of vulnerable adults).',
        '**Zenith:** the earlier Zenith Alora guide and its standards. Zenith standards here are drafts until approved.']), 'blue')
), kind='text')


# ============================================================================= how to use
HOWTO_1 = Text('howto-1', 1, 'How to use this binder', (
    '<h1 class="ttl">How to use this binder</h1>'
    '<p class="sub">Sit at the office computer with the binder open beside the keyboard. Do one procedure at a time. Never do a step from memory.</p>'
    + H('The method')
    + '<div class="method"><div>SEE IT<small>match the picture to your screen</small><span class="arr">›</span></div><div>CLICK IT<small>follow the red numbers in order</small><span class="arr">›</span></div>'
      '<div>ENTER IT<small>type only what the page asks</small><span class="arr">›</span></div><div>SAVE IT<small>click once, then wait</small><span class="arr">›</span></div>'
      '<div>VERIFY IT<small>check the result on screen</small></div></div>'
    + H('Every procedure has the same pattern')
    + OL(['**Start page.** What the procedure is for, what you need before you begin, and the list of steps with page numbers.',
          '**Step pages.** One picture with red numbers, and the words for what to do after each click. Follow the numbers in order.',
          '**Finish page.** The final verification checklist, the stop rules, and the things you must not do.'])
    + H('Your first four weeks')
    + TABLE(['Week', 'Do these procedures with a trainer', 'Then do them alone'], [
        ['1', 'P1 Log Into Alora · P2 Dashboard · P28 Security and HIPAA · P3 Find a Patient · P4 Open a Patient Record', 'P1, P3, P4'],
        ['2', 'P5 Demographics · P9 Scan and Name · P8 Upload · P10 Verify Documents', 'P9, P8, P10'],
        ['3', 'P6 Process a Referral · P11 Orders · P12 Face-to-Face · P7U SOC Document Upload', 'P6, P7U'],
        ['4', 'P7 SOC Stage Guide · P13 Prepare the SOC Visit · P14 to P16 Scheduling · P23 Daily Check', 'P13, P14, P23'],
        ['After', 'P15 to P22 Monitoring, QA, Billing and NOA (as the Administrator assigns) · P24, P25 Weekly and Monthly', ''],
    ], widths=['10%', '68%', '22%'], cls='tight')
    + KBOX('Rules for the binder', UL([
        'Write in the margins. If your Alora shows a different button name, write the real name next to the tag and tell the Administrator.',
        'Do not remove pages. Copy forms from Tab 11.',
        'If this manual and the Administrator disagree, follow the Administrator and report the difference.']), 'gold')
), kind='text')


def _chip(cls, text):
    return f'<span class="chip {cls}">{text}</span>'


def _mini():
    m = S.login(filled=True)
    m.call(1, 'login_user', 'Username', ('right', 0, 0), key='login_user')
    m.call(2, 'login_pass', 'Password', ('right', 0, 0), key='login_pass')
    m.call(3, 'login_btn', 'Login', ('right', 0, 0), key='login_btn')
    return m.svg()


HOWTO_2 = Text('howto-2', 1, 'How to read a step page', (
    '<h1 class="ttl">How to read a step page</h1>'
    '<p class="sub">Every step page has the same parts in the same places. Learn them once.</p>'
    '<div class="anat">'
    '<div class="a-title"><b>A</b> Step number and title</div>'
    '<div class="a-pic"><div class="a-mini">' + _mini() + '</div><div><b>B</b> The picture. A training mockup of the screen. <span class="rc">1</span> <span class="rc">2</span> <span class="rc">3</span> The red numbers show where to click, in order. Each number has a short label. Follow them in order.</div></div>'
    '<div class="a-l"><div class="a-do"><b>C</b> Do these in order. One line for each red number.</div><div class="a-rows"><b>D</b> ENTER: what to type. CHECK: what to check before you save. EXPECTED RESULT: what should happen.</div></div>'
    '<div class="a-r"><div class="a-see"><b>E</b> What you should see</div><div class="a-dont"><b>F</b> Do not do this</div><div class="a-stop"><b>G</b> If it does not look right: stop</div></div>'
    '<div class="a-std"><div><b>H</b> Alora action <i>what to do in Alora</i></div><div><b>I</b> Zenith standard <i>Zenith\'s own rule</i></div></div>'
    '<div class="a-live"><b>J</b> Live Alora check. The Administrator initials this when the picture was compared with live Alora.</div>'
    '</div>'
    + H('The tags')
    + TABLE(['Tag', 'What it means for you'], [
        [_chip('verify', 'VERIFY IN LIVE ALORA'), 'Nothing public confirms this name or place. Compare the picture with your screen. If they differ, write the real name in the margin and tell the Administrator.'],
        [_chip('feature', 'ALORA FEATURE'), 'Alora publicly describes this feature by name. The exact words of the menu or button and their place still have to be checked.'],
        [_chip('verified', 'VERIFIED'), 'The Administrator confirmed the name and place in live Alora. (None yet in this edition.)'],
        [_chip('verified', 'FROM LIVE ALORA'), 'The picture is a real screenshot from Zenith\'s Alora with numbers added.'],
        [_chip('windows', 'WINDOWS'), 'A standard Windows window, such as the file chooser. Not Alora.'],
        [_chip('zenith', 'ZENITH FORM'), 'A paper form from Tab 11. Not a screen.'],
        ['**Alora action**', 'What you do in Alora: click, type, choose, save.'],
        ['**Zenith standard**', 'A rule Zenith sets for its own office. It is stricter than, or additional to, what Alora does.'],
        [_chip('law', 'FEDERAL RULE'), 'A rule from Medicare, HIPAA or Florida law. The Administrator explains it if you ask.'],
    ], widths=['28%', '72%'], cls='tight')
), kind='text')


# ============================================================================= verification status
def _features():
    seen = []
    for k, (desc, feat) in ui.REG.items():
        if feat and feat not in seen:
            seen.append(feat)
    return seen


VERIFY_STATUS = Text('verify-status', 1, 'What is verified and what is not', (
    '<h1 class="ttl">What is verified and what is not</h1>'
    '<p class="sub">Read this page before you trust any picture in this manual.</p>'
    + KBOX('Plain statement', P('**In this edition, no screen, button, menu or box name has been verified against Zenith\'s live Alora account.** '
                                  'Alora\'s own training screens are not public and were not available. The pictures are a neutral, clearly labeled wireframe of a web application. '
                                  'They show where on a typical screen an item would be, and they show the **order** of the clicks. They do not show what Alora really looks like.'), 'red')
    + TABLE(['Kind of item', 'Status in this edition', 'What the manual does'], [
        ['Names of Alora features (for example Live Monitor, QA, NOA widget)', _chip('feature', 'FEATURE'), 'Uses the public feature name. Tags the exact menu or button text as \'to verify\'.'],
        ['Menu, button, box and column names', _chip('verify', 'VERIFY'), 'Describes the item in plain words. Tags it. Never presents a guessed name as real.'],
        ['Order of the clicks', _chip('verify', 'VERIFY'), 'Follows how web scheduling and records systems normally work. The Administrator confirms it in live Alora.'],
        ['Windows windows (file chooser, folders, lock screen)', _chip('windows', 'WINDOWS'), 'Standard Windows behavior.'],
        ['Paper forms and Zenith rules', _chip('zenith', 'ZENITH'), 'Written by Zenith. Drafts until the Administrator approves them.'],
    ], widths=['36%', '18%', '46%'], cls='tight')
    + H('How to close the gap')
    + OL(['**Live Alora check (about 2 hours).** The Administrator works through the **Live Alora Verification Worksheet** (Tab 11) at a computer signed in to live Alora, and writes the real names and places.',
          '**Reissue.** The real names go into the manual. Tags change to VERIFIED. Wording that needs changing is changed.',
          '**Real screenshots (optional but best).** Capture each screen from live Alora, add the red numbers with the annotation tool, and drop the file into the manual. The picture then says FROM LIVE ALORA.',
          '**Approve.** The Administrator signs the Document control page.'])
    + H('Features Alora documents publicly')
    + '<p style="font-size:8.4pt;color:#39424F;margin-bottom:2px">Alora\'s public product information names these features. That tells us a feature exists, not where it is on Zenith\'s screens.</p>'
    + '<ul class="two-col" style="font-size:8.2pt;margin-top:2px;margin-bottom:0">' + ''.join(f'<li>{md(f)}</li>' for f in _features()) + '</ul>'
), kind='text')


# ============================================================================= roles
ROLES = Text('roles', 1, 'Who does what', (
    '<h1 class="ttl">Who does what</h1>'
    '<p class="sub">Office staff prepare, check and report. Clinicians and the DON decide clinical questions. The Administrator decides everything else that this manual says needs approval.</p>'
    + TABLE(['Role', 'What they do in this manual', 'What they never do'], [
        ['**Intake staff**', 'Log and check referral packets. Find patients. Scan, name and upload documents. Check demographics. Check orders and face-to-face papers.', 'Accept or decline a referral. Change clinical information. Choose the nurse.'],
        ['**Second person**', 'Verifies orders and face-to-face documents that someone else uploaded.', 'Verify their own upload.'],
        ['**Scheduler**', 'Adds visits from a signed request. Checks the calendar. Changes a visit only with written approval. Tells team members and patients.', 'Change the ordered frequency. Choose the nurse for a start of care.'],
        ['**Office staff on duty**', 'Watch the Live Monitor. Call about late visits. Gather facts for exceptions. Do the daily checks.', 'Change a visit status or time. Approve an exception.'],
        ['**QA reviewer** (named by the DON)', 'Judges clinical content. Returns items for correction.', 'Approve their own work.'],
        ['**Billing staff**', 'Check billing readiness. Create and send the NOA when named by the Administrator. Send claims.', 'Change clinical documents.'],
        ['**Director of Nursing (DON)**', 'Decides referrals and clinical questions. Names the nurse for every start of care. Approves clinical changes.', ''],
        ['**Administrator**', 'Owns this manual. Approves record changes, document removals, EVV exceptions, user logins and anything marked \'Administrator\'.', ''],
    ], widths=['20%', '50%', '30%'], cls='tight')
    + KBOX('Your name in this binder', '<p>Write who fills each role at Zenith, so a new employee knows whom to ask.</p>' + BLANKS(4, ''), 'gold')
), kind='text')


# ============================================================================= stop rules
STOPRULES = Text('stoprules', 1, 'When to stop and ask', (
    '<h1 class="ttl">When to stop and ask</h1>'
    '<p class="sub">These rules apply to every procedure. Each procedure also has its own stop rules on its finish page. To stop is always correct. A guess that goes wrong is not.</p>'
    + KBOX('Always stop and ask the Administrator or DON if', CHECKS([
        'A screen or a button does **not look like the picture** and you are not sure what to click.',
        'The patient\'s **name or date of birth does not match** a document.',
        '**Two patients** could be the right one, or **no patient** can be found after three searches.',
        'A document is in the **wrong patient\'s chart**. Tell the Administrator **now**.',
        'An **error message** appears, or Alora does nothing after you click.',
        'An **alert** appears while you schedule or save.',
        'The **48-hour deadline** cannot be met, or an NOA is close to its 5-day limit.',
        'An **order or face-to-face document** is missing, unsigned or outside its date window.',
        'Someone asks you to **change a time, a status or a record** to make it look right.',
        'Someone asks for **patient information** and you are not sure they may have it.',
        'You think someone used **your login**, or you used someone else\'s.',
        'You are asked to do something this manual says needs **approval**.'], big=True), 'red')
    + H('What to say')
    + P('Say it in short, plain sentences. You do not have to use perfect English. Use this pattern:')
    + '<div class="kbox gold"><p style="font-size:11pt;line-height:1.7"><b>1.</b> \"I am **stopping** at procedure <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>, step <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>.\"<br>'
      '<b>2.</b> \"I saw <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>.\"<br>'
      '<b>3.</b> \"I have **not changed** anything.\"<br><b>4.</b> \"What should I do?\"</p></div>'
    + GRID2(KBOX('Do', UL(['Stop at once.', 'Leave the screen as it is.', 'Write the time and the words you saw.', 'Ask.']), 'green'),
            KBOX('Do not', UL(['Do not try a different button to see what happens.', 'Do not start again and hope it fixes itself.', 'Do not hide a mistake.']), 'red'))
), kind='text')


# ============================================================================= Zenith standards
STANDARDS = [
    ('Log every referral packet within 15 minutes of arrival.', 'P6', 'The 48-hour initial visit clock starts at referral.'),
    ('The DON or Administrator decides every referral. Office staff never accept, hold or decline.', 'P6, P27', ''),
    ('Identify a patient with two identifiers: name and date of birth.', 'P3, P4, P8', ''),
    ('Search three ways before creating a patient. Create only after the DON accepts.', 'P5B', ''),
    ('Name files LASTNAME_FIRSTNAME_DOCUMENTTYPE_YYYYMMDD.pdf. Scan as PDF at 300 dpi, one patient and one document type per file.', 'P9', ''),
    ('Verify a document in the same session you upload it. Orders and face-to-face: a second person verifies.', 'P8, P10', ''),
    ('Every new order goes to the DON the same day, signed or not.', 'P11', ''),
    ('Tell the DON the same day about a face-to-face problem.', 'P12', 'Face-to-face visit 90 days before to 30 days after start of care (42 CFR 424.22).'),
    ('The first nurse visit is scheduled inside 48 hours of the referral, unless the physician ordered a later date.', 'P13', 'Initial assessment within 48 hours (42 CFR 484.55).'),
    ('Visits follow a signed Visit Scheduling Request. Office staff never change the frequency.', 'P14', 'Visits follow the plan of care.'),
    ('Change a visit only with written approval from the DON or Administrator. Never delete a visit.', 'P16', ''),
    ('Check the Live Monitor at the start of the day, at midday and one hour before the end of the day.', 'P17, P23', ''),
    ('Call the team member when a visit is more than 15 minutes late. Tell the DON when it is more than 30 minutes late. Tell the DON at once about a no-show or a late start of care visit.', 'P17', ''),
    ('Report an EVV exception older than 2 business days to the Administrator. Office staff never approve an exception.', 'P18, P23', 'Visit records must be accurate.'),
    ('Remind about a late clinical document the same day it is found. Report items older than 7 days to the DON.', 'P19, P24', 'Comprehensive assessment within 5 calendar days of start of care (42 CFR 484.55). OASIS sent within 30 days (42 CFR 484.45).'),
    ('Office staff check QA items for completeness only. The QA reviewer named by the DON returns or approves.', 'P20', ''),
    ('Check billing readiness at least 3 business days before a claim is due.', 'P21', ''),
    ('Send the NOA within 5 calendar days of the start of care. Check its status every business day until accepted. Only billing staff the Administrator names create it.', 'P22', 'NOA within 5 calendar days (Medicare payment rules).'),
    ('Complete the daily sheet every day, the weekly sheet every Friday, the monthly sheet by the last business day of the month.', 'P23 to P25', ''),
    ('Lock the computer every time you leave your seat. Log out at the end of your shift. Remove a scanned file from the scan folder only after it is verified.', 'P28', 'Unique user login and safeguards (45 CFR 164.312).'),
    ('A document in the wrong chart is reported to the Administrator at once.', 'P10, P26', 'HIPAA.'),
]

STD_ROWS = [[str(i + 1), md(s), p, l, ''] for i, (s, p, l) in enumerate(STANDARDS)]


def _std_page(part):
    half = 10
    rows = STD_ROWS[:half] if part == 0 else STD_ROWS[half:]
    head = (f'<h1 class="ttl">Zenith standards in this manual ({part + 1} of 2)</h1>'
            '<p class="sub">These are the times, numbers and rules that Zenith sets for its own office. <b>They are drafts.</b> The Administrator initials each one to approve it, or writes a change. '
            'Where a federal rule also applies, it is shown. A Zenith standard must never allow more time than the law allows.</p>' if part == 0 else
            '<h1 class="ttl">Zenith standards in this manual (2 of 2)</h1>')
    t = TABLE(['No.', 'Standard', 'Where', 'Federal rule it must not exceed', 'Approved (initials)'], rows, widths=['6%', '44%', '9%', '28%', '13%'], cls='tight')
    tail = ''
    if part == 1:
        tail = P('Approved by the Administrator:') + SIGN(['Administrator name and signature', 'Date'])
    return head + t + tail


STANDARDS_1 = Text('standards-1', 1, 'Zenith standards (1 of 2)', lambda: _std_page(0), kind='text')
STANDARDS_2 = Text('standards-2', 1, 'Zenith standards (2 of 2)', lambda: _std_page(1), kind='text')


# ============================================================================= access sheet
ACCESS = Text('access', 1, 'Alora access sheet', (
    '<h1 class="ttl">Alora access sheet</h1>'
    '<p class="sub">The Administrator fills this in when the binder is issued. It holds the facts this manual cannot know. Never write a password here.</p>'
    + H('Getting in')
    + BLANKS(1, 'Zenith\'s Alora web address (bookmark name):')
    + BLANKS(1, 'Browser the office uses:')
    + BLANKS(1, 'How usernames are made (for example first initial and last name):')
    + BLANKS(1, 'Who creates and resets logins:')
    + H('People')
    + BLANKS(1, 'Administrator (name, phone):')
    + BLANKS(1, 'Director of Nursing (name, phone):')
    + BLANKS(1, 'Billing staff who may create NOAs:')
    + BLANKS(1, 'QA reviewers named by the DON:')
    + BLANKS(1, 'Alora support contact:')
    + H('The office computer')
    + BLANKS(1, 'Scan folder path (Ready to upload):')
    + BLANKS(1, 'Scanner model and where it is:')
    + BLANKS(1, 'Where original papers are filed after upload:')
    + H('Names in Zenith\'s Alora (copy from live Alora)')
    + BLANKS(1, 'Document types in the upload list:')
    + BLANKS(1, '')
    + BLANKS(1, 'Status words on the Live Monitor (green, yellow, red):')
    + BLANKS(1, 'Where the Live Monitor is in the menu:')
    + KBOX('Rule', 'This sheet holds no passwords. Passwords are never written down, shared or kept in this binder.', 'red')
), kind='text')

# ============================================================================= task index
TASKS = [
    ('Log into Alora', 'P1', 'login'), ('Find my way around the dashboard', 'P2', 'dashboard'), ('Find a patient', 'P3', 'find'), ('Open a patient record', 'P4', 'open'),
    ('Check patient name, birth date, address, insurance', 'P5', 'demographics'), ('Add a new patient (only when allowed)', 'P5B', 'newpatient'), ('A referral just arrived', 'P6', 'referral'),
    ('Process a whole Start of Care packet', 'P7', 'socstages'), ('Upload the referral, order and face-to-face', 'P7U', 'socupload'), ('Upload a scanned document', 'P8', 'upload'),
    ('Scan and name a document', 'P9', 'naming'), ('Check that an upload is correct', 'P10', 'verify'), ('Review a physician order', 'P11', 'orders'),
    ('Review face-to-face documentation', 'P12', 'f2f'), ('Get a new patient ready for the first visit', 'P13', 'socprep'), ('Put a visit on the schedule', 'P14', 'schedule'),
    ('Look at the schedule', 'P15', 'viewschedule'), ('Change a visit (only with written approval)', 'P16', 'changeschedule'), ('Watch visits today', 'P17', 'monitor'),
    ('A visit record does not match', 'P18', 'evv'), ('Check that clinical papers are moving', 'P19', 'clinrev'), ('Do the QA check', 'P20', 'qa'),
    ('Check that a patient is ready to bill', 'P21', 'billing'), ('Send and track the NOA', 'P22', 'noa'), ('Do the daily check', 'P23', 'daily'),
    ('Do the weekly check', 'P24', 'weekly'), ('Do the monthly check', 'P25', 'monthly'), ('Something does not look right', 'P26', 'trouble-1'),
    ('Can I do this, or do I need approval?', 'P27', 'approvals-1'), ('Protect patient information', 'P28', 'security'),
]

TASK_INDEX = Text('taskindex', 1, 'I need to... (task index)', (
    '<h1 class="ttl">I need to...</h1><p class="sub">Find your task, then turn to the page. The procedure numbers (P1, P2...) are the same on every page header.</p>'
    + TABLE(['I need to...', 'Procedure', 'Page'], [[t, f'**{p}**', '{{pg:' + pid + '}}'] for t, p, pid in TASKS], widths=['64%', '16%', '20%'], cls='tight')
), kind='text')
TASK_INDEX.toc = True


for _t in (DOC_CONTROL, HOWTO_1, HOWTO_2, TASK_INDEX, VERIFY_STATUS, ROLES, STOPRULES, STANDARDS_1, ACCESS):
    _t.toc = True

PAGES = [COVER, DOC_CONTROL,
         Divider(1, 'Read these pages first. They tell you how the binder works, what has and has not been verified, who does what, and when to stop.',
                 [('howto-1', 'How to use this binder'), ('howto-2', 'How to read a step page and the tags'), ('taskindex', 'I need to... (task index)'), ('verify-status', 'What is verified and what is not'), ('roles', 'Who does what'),
                  ('stoprules', 'When to stop and ask'), ('standards-1', 'Zenith standards in this manual'), ('access', 'Alora access sheet')]),
         HOWTO_1, HOWTO_2, TASK_INDEX, VERIFY_STATUS, ROLES, STOPRULES, STANDARDS_1, STANDARDS_2, ACCESS]

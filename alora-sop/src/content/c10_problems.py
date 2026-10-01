"""Tab 10: troubleshooting, the wrong-chart emergency page, the approval matrix, and who to call."""
from model import Text, Divider
from blocks import *


def _trouble_rows(rows):
    return [[f'**{a}**', b, c, d] for a, b, c, d in rows]


T_HEAD = ['What you see', 'What it may mean', 'What you do', 'Stop and ask?']
T_W = ['20%', '22%', '42%', '16%']

TROUBLE_1 = Text('trouble-1', 10, 'Troubleshooting (1 of 2): signing in and screens', (
    '<h1 class="ttl">Troubleshooting (1 of 2)</h1>'
    '<p class="sub">Signing in, screens and saving. Find what you see in the left column. If the last column says <b>STOP</b>, stop and ask the Administrator. '
    'Write the time and what you saw on the Problem Report (Tab 11).</p>'
    + TABLE(T_HEAD, _trouble_rows([
        ('The sign-in page does not open', 'The address was typed wrong, or the internet is down.', 'Use the bookmark the Administrator saved. Do not search for Alora on a search engine. Check that other websites open.', '**STOP** if a security warning appears.'),
        ('Sign-in does not work once', 'Typing mistake. Caps Lock may be on.', 'Check that Caps Lock is off. Type the password slowly. Try once more.', 'After two tries, **STOP**.'),
        ('You forgot your password', 'Normal. It happens.', 'Ask the Administrator to reset it. Never use another person\'s login, even for a minute.', '**STOP**. Ask.'),
        ('The screen is different from this manual', 'Alora changed, your role is different, or the picture in this manual was not checked yet.', 'Do not guess. Write what you see in the margin. Ask the Administrator. The pictures are training mockups, not screenshots.', '**STOP**.'),
        ('A button named in this manual is missing', 'The button has another name, or your role cannot see it.', 'Do not click a different button that looks close. Ask the Administrator to show you.', '**STOP**.'),
        ('The page is blank or keeps loading', 'The internet is slow.', 'Wait 30 seconds. Do not click many times. Do not refresh while a form is saving. Try the Alora menu.', '**STOP** after 2 minutes.'),
        ('You are signed out suddenly', 'The session ended after you were idle.', 'Sign in again. Open the record. Check whether your last save is there. Do not assume it is.', '**STOP** if data is missing.'),
        ('An error message appears after Save', 'The save did not finish.', 'Do not click Save again. Look in the list to see if the item saved. Write the exact words of the message.', '**STOP**.'),
        ('A yellow or red alert appears while scheduling', 'Alora found a conflict or a rule problem.', 'Read it. Do not click through. Show it to the DON.', '**STOP**.'),
        ('The page looks frozen after you clicked', 'The computer is still working.', 'Wait. Do not click again. A second click can save twice.', 'After 1 minute, **STOP**.'),
    ]), widths=T_W)
), kind='text')

TROUBLE_2 = Text('trouble-2', 10, 'Troubleshooting (2 of 2): patients, documents and visits', (
    '<h1 class="ttl">Troubleshooting (2 of 2)</h1>'
    '<p class="sub">Patients, documents and visits. The rule is the same: do not fix it yourself. Report it.</p>'
    + TABLE(T_HEAD, _trouble_rows([
        ('The patient is not found', 'Spelling, birth date or a nickname.', 'Search three ways (P3). Do not create a patient.', 'If three searches fail, **STOP**.'),
        ('Two patients have the same name', 'Normal for common names.', 'Use date of birth and record number. Do not guess.', '**STOP** if you cannot tell them apart.'),
        ('The upload did not finish', 'File problem or internet problem.', 'Do not click Save again. Check the document list for a new row. Write the message.', '**STOP**.'),
        ('A document shows twice', 'Saved twice.', 'Do not delete one. Fill in a Document Problem Report.', '**STOP**.'),
        ('A document is in the wrong chart', 'Wrong patient was open. This is a **privacy problem**.', 'Stop. Do not delete or move it. Write the two names, the document and the time. Tell the Administrator **now**.', '**STOP NOW**.'),
        ('A document will not open or is blank', 'Bad scan.', 'Scan it again. Check it in the viewer before uploading. Do not delete the bad one.', '**STOP** if it still fails.'),
        ('The visit is not on the schedule after Save', 'The view hides it (wrong patient, day or week).', 'Check view by and show. Look at the week. Do not add it again.', '**STOP** if it is still missing.'),
        ('A visit is on the schedule twice', 'Saved twice.', 'Do not delete one. Tell the DON.', '**STOP**.'),
        ('The Live Monitor is empty but visits are scheduled', 'Wrong day or filter.', 'Check the date and filters. Look at the schedule.', '**STOP** if it stays empty.'),
        ('An NOA shows rejected', 'A number or a date was wrong.', 'Write the words of the message. Tell the Administrator the same day.', '**STOP**.'),
        ('A name in Alora is different from the insurance card', 'Typing mistake in the record.', 'Do not change it. Fill in a Record Correction Request (P5).', '**STOP**.'),
        ('You opened the wrong patient by mistake', 'A click on the wrong row.', 'Close it. Do not read it. Tell the Administrator if you read anything.', 'Tell the Administrator.'),
        ('You think someone used your login', 'Shared or guessed password.', 'Lock the computer. Tell the Administrator **at once**.', '**STOP NOW**.'),
    ]), widths=T_W)
), kind='text')

WRONG_CHART = Text('wrong-chart', 10, 'A document is in the wrong chart: the first ten minutes', (
    '<h1 class="ttl">A document is in the wrong chart</h1>'
    '<p class="sub">This is the one mistake that must be reported at once. It is a privacy problem and it can also cause a wrong care decision. Do these five things, in this order.</p>'
    + KBOX('The first ten minutes', OL([
        '**Stop.** Do not click anything else in that chart.',
        '**Do not delete, move or rename** the document. The Administrator decides how to correct it.',
        '**Write down:** the name of the patient whose chart has the document, the name of the patient it belongs to, the document name, the date and the time.',
        '**Tell the Administrator now.** Go to the Administrator\'s desk or call. Do not send an email or a text with patient names.',
        '**Close the chart** and wait for instructions.']), 'red')
    + GRID2(
        KBOX('Do', UL(['Tell the truth about what happened.', 'Tell the Administrator even if you are not sure.', 'Write what you did and when.']), 'green'),
        KBOX('Do not', UL(['Do not try to fix it quietly.', 'Do not tell anyone outside Zenith.', 'Do not wait until the end of the day.']), 'red'))
    + H('Write it here')
    + BLANKS(1, 'Patient whose chart has the document:')
    + BLANKS(1, 'Patient it belongs to:')
    + BLANKS(1, 'Document, date and time:')
    + BLANKS(1, 'Time the Administrator was told:')
    + KBOX('Federal rule', 'HIPAA requires Zenith to look into any use or disclosure of patient information that is not allowed, and to decide whether it must be reported. That decision belongs to the Administrator and the privacy contact, not to office staff.', 'blue')
), kind='text')

MATRIX_HEAD = ['Action', 'Office staff may', 'Needs approval from', 'Form (Tab 11)']
MATRIX_W = ['30%', '24%', '22%', '24%']

MATRIX_1 = Text('approvals-1', 10, 'What needs Administrator or DON approval (1 of 2)', (
    '<h1 class="ttl">What needs Administrator or DON approval (1 of 2)</h1>'
    '<p class="sub">Office staff prepare, check and report. The people in the third column decide. If an action is not on this list, ask before you do it.</p>'
    + TABLE(MATRIX_HEAD, [
        ['Accept, hold or decline a referral', 'No. Log and check the packet.', 'DON or Administrator', 'Referral Decision'],
        ['Create a new patient', 'Only after the DON accepts and three searches find nothing (P5B).', 'DON', 'Referral Decision'],
        ['Change a demographic detail', 'Prepare a request when a document shows a difference.', 'Administrator', 'Record Correction Request'],
        ['Change a clinical detail (diagnosis, medicines, allergies)', '**No.**', 'DON', 'None. Clinicians only.'],
        ['Choose the nurse for a start of care', 'No.', 'DON', 'SOC Assignment'],
        ['Schedule a start of care visit', 'Yes, after the readiness check.', 'DON names the nurse', 'SOC Readiness Check'],
        ['Agree to a start date later than 48 hours', '**No.**', 'DON and the physician\'s order', 'SOC Call Notes'],
        ['Add a visit from a plan of care', 'Yes, from a signed request.', 'DON signs the request', 'Visit Scheduling Request'],
        ['Change a visit', 'Only with written approval.', 'DON or Administrator', 'Schedule Change Approval'],
        ['Delete or cancel a visit', '**No.**', 'DON', 'None. Ask.'],
        ['Upload a document into a chart', 'Yes, when trained.', 'A second person verifies orders and face-to-face', 'Document Verification'],
        ['Choose the type \'Other\'', 'No, unless told.', 'Administrator', 'None. Ask.'],
        ['Delete or replace a document', '**No.**', 'Administrator or DON', 'Document Problem Report'],
    ], widths=MATRIX_W)
), kind='text')

MATRIX_2 = Text('approvals-2', 10, 'What needs Administrator or DON approval (2 of 2)', (
    '<h1 class="ttl">What needs Administrator or DON approval (2 of 2)</h1>'
    '<p class="sub">Clinical documents, visit records, billing and access.</p>'
    + TABLE(MATRIX_HEAD, [
        ['Change a visit time or status', '**Never.** Not even when asked.', 'Nobody in the office', 'None. Report the request.'],
        ['Approve an EVV exception', 'No. Gather the facts.', 'Administrator or DON', 'Exception Follow-up'],
        ['Complete or change an OASIS, plan of care or visit note', '**No.**', 'The clinician', 'None. Clinicians only.'],
        ['Sign or date anything for a physician or clinician', '**Never.**', 'Nobody', 'None.'],
        ['Return a QA item for correction', 'Only a QA reviewer the DON named.', 'DON', 'QA Completeness Check'],
        ['Approve a clinical item in QA', '**No.**', 'QA reviewer or DON', 'None.'],
        ['Create and send an NOA', 'Only billing staff the Administrator named.', 'Administrator', 'NOA Check, NOA Tracking Log'],
        ['Send a claim or change a billing status', 'No.', 'Billing staff, Administrator', 'Billing Readiness Check'],
        ['Discharge a patient or change a patient status', '**No.**', 'DON', 'Discharge Check'],
        ['Give patient information by phone', 'Only to a person you verified, and only what they need.', 'Administrator decides who is allowed', 'None. Ask.'],
        ['Add, change or remove a user login', '**No.**', 'Administrator', 'None.'],
        ['Share a password or use another login', '**Never.**', 'Nobody', 'None.'],
        ['Photograph or screenshot patient information', '**Never.**', 'Nobody', 'None.'],
    ], widths=MATRIX_W)
), kind='text')

CONTACTS = Text('contacts', 10, 'Who to call', (
    '<h1 class="ttl">Who to call</h1>'
    '<p class="sub">The Administrator fills in the blanks when the binder is issued. The two hotline numbers are public. The Administrator confirms them.</p>'
    + TABLE(['Who', 'Call when', 'Name and number'], [
        ['**Emergency**', 'Anyone is in danger.', '**911**'],
        ['**Administrator**', 'Any stop rule in this manual. Privacy problems.', '<span class="blank" style="min-width:2.2in"></span>'],
        ['**Director of Nursing (DON)**', 'Clinical questions. Late or missed visits. Referral decisions.', '<span class="blank" style="min-width:2.2in"></span>'],
        ['**On-call nurse** (after hours and weekends)', 'An urgent clinical problem.', '<span class="blank" style="min-width:2.2in"></span>'],
        ['**Privacy contact**', 'A document in the wrong chart. A lost paper. Login misuse.', '<span class="blank" style="min-width:2.2in"></span>'],
        ['**Compliance officer**', 'A record that may be false. A billing worry.', '<span class="blank" style="min-width:2.2in"></span>'],
        ['**Billing**', 'Claims and NOA questions.', '<span class="blank" style="min-width:2.2in"></span>'],
        ['**Alora support**', 'A problem the Administrator cannot solve.', '<span class="blank" style="min-width:2.2in"></span>'],
        ['**Office IT help**', 'Scanner, printer, computer, internet.', '<span class="blank" style="min-width:2.2in"></span>'],
        ['**Florida Abuse Hotline**', 'You suspect abuse, neglect or exploitation of a vulnerable adult. Report it at once. Also tell the Administrator.', '**1-800-96-ABUSE** (1-800-962-2873)'],
        ['**HHS Office of Inspector General**', 'You suspect Medicare or Medicaid fraud.', '**1-800-HHS-TIPS**'],
    ], widths=['27%', '43%', '30%'])
    + KBOX('Federal and Florida rule', 'Florida law (section 415.1034, Florida Statutes) says any person who knows or has reasonable cause to suspect that a vulnerable adult is being abused, neglected or exploited must report it immediately to the Florida Abuse Hotline. You do not need proof.', 'blue')
), kind='text')

for _t in (TROUBLE_1, TROUBLE_2, WRONG_CHART, MATRIX_1, MATRIX_2, CONTACTS):
    _t.toc = True

PAGES = [Divider(10, 'What to do when something does not look right, what office staff may not do without approval, and who to call.',
                 [('trouble-1', 'P26  Troubleshooting (1 of 2): signing in and screens'), ('trouble-2', 'P26  Troubleshooting (2 of 2): patients, documents, visits'),
                  ('wrong-chart', 'A document is in the wrong chart'), ('approvals-1', 'P27  What needs approval (1 of 2)'), ('approvals-2', 'P27  What needs approval (2 of 2)'),
                  ('contacts', 'Who to call')]),
         TROUBLE_1, TROUBLE_2, WRONG_CHART, MATRIX_1, MATRIX_2, CONTACTS]

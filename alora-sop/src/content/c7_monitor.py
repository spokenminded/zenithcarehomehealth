"""Tab 7: monitor visits (Live Monitor), EVV exceptions, clinical documentation review, QA review."""
import scenes as S
import scenes2 as S2
import scenes3 as S3
import scenes4 as S4
from model import Proc, Step, Divider
from blocks import *


# ============================================================================= P17 Monitor visits
def m_mo_1():
    m = S4.blank_shell('dash', 'Dashboard')
    m.call(1, 'nav', 'Main menu', ('right', 0, 60), key='lm_open')
    return m


def m_mo_2():
    m = S4.live_monitor()
    m.call(1, 'lm_status', 'Status column', (600, 92), key='lm_status')
    m.call(2, 'lm_table.r0', 'On time', (465, 420), key='lm_table')
    return m


def m_mo_3():
    m = S4.live_monitor()
    m.call(1, 'lm_table.r1', 'Late, not clocked in', (420, 420), key='lm_row_late')
    m.call(2, 'lm_status', 'Status column', (600, 92), key='lm_status')
    return m


def m_mo_4():
    m = S2.zform('LATE OR MISSED VISIT LOG', [
        ('h', 'THE VISIT'), ('two', 'pt', 'Patient:', 'vis', 'Planned date and time:'), ('line', 'tm', 'Team member:'),
        ('h', 'WHAT YOU DID'), ('line', 'call', 'Called team member (time, what they said):'), ('line', 'told', 'Told DON (time):'),
        ('line', 'res', 'Result (visit done at, rescheduled to, other):'),
        ('h', 'LOGGED BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')])
    m.call(1, 'call', 'Call and write the answer', ('right', 0, 0), key='zenith')
    m.call(2, 'told', 'Tell the DON', ('right', 0, 0), key='zenith')
    m.call(3, 'res', 'Write the result', ('right', 0, 0), key='zenith')
    return m


def m_mo_5():
    m = S4.live_monitor()
    m.call(1, 'lm_table.r2', 'No-show', (463, 420), key='lm_row_noshow')
    m.call(2, 'lm_status', 'Status column', (600, 92), key='lm_status')
    return m


MONITOR = Proc(
    id='monitor', tab=7, num='P17', title='Monitor Visits (Live Monitor)',
    purpose='To watch visits as they happen, so a late or missed visit is found in minutes and not the next day. '
            'Alora documents a Live Monitor with color-coded warnings for delays and no-shows. '
            'Office staff watch, call and report. They never change a visit status.',
    before=['You are signed in (P1).', 'The **Late or Missed Visit Log** (Tab 11).', 'The phone numbers of team members on duty.'],
    who='Office staff on duty.', time='5 minutes each time. Check at the start of the day, at midday and near the end.',
    steps=[
        Step('mo-1', 'Open the Live Monitor', m_mo_1,
             do=['Use the **main menu** to find the Live Monitor. Write its real name in the margin once you find it.'],
             check=['You are not inside a form.'],
             expect='A list of today\'s visits opens.',
             see='A list of visits with a time, a team member, a patient and a status.',
             alora='Alora documents a Live Monitor. Where it is in the menu must be verified.', astatus='FEATURE',
             zenith='Check at the start of the day, at midday and one hour before the end of the day.',
             stop=['You cannot find the Live Monitor.']),
        Step('mo-2', 'Read the statuses', m_mo_2,
             do=['Read the **status** of each visit. Colors and words show on time, late, no-show or complete.', 'Find a visit that is **on time** and in progress. Nothing to do.'],
             check=['You can name the color and the word for each status.'],
             expect='You know which visits need nothing and which need you.',
             see='A list where each visit has a colored status.',
             donot=['Do not change a status yourself.'],
             alora='Alora documents color-coded delay and no-show warnings. The colors and words in Zenith\'s Alora must be verified and written in the margin.', astatus='FEATURE',
             zenith='Green or \'on time\' needs nothing. Anything else needs a call.'),
        Step('mo-3', 'A visit is late', m_mo_3,
             do=['Find the **late** visit.', 'Read the **status** words. They say the team member has not clocked in.'],
             check=['The planned time has passed by more than 15 minutes.', 'The visit is for today.'],
             expect='You know which visit is late.',
             see='A row that says late or not clocked in, in a warning color.',
             donot=['Do not mark the visit complete or change its time.'],
             alora='Alora documents color-coded delay warnings. The wording must be verified.', astatus='FEATURE',
             zenith='Call the team member right away. Report to the DON if the visit is more than 30 minutes late.',
             rule='A late first visit can break the 48-hour rule for a new patient.',
             stop=['The late visit is a start of care visit.', 'The team member does not answer.']),
        Step('mo-4', 'Call, record and report', m_mo_4,
             do=['Call the team member. Write the **time and what they said**.', 'Tell the **DON**. Write the time you told them.', 'Write the **result** when it is known.'],
             enter='On the paper log only: times and what was said. Do not type anything in Alora.',
             check=['You wrote the time of each call.', 'You wrote what was said in the person\'s own words.'],
             expect='The log shows the late visit, the call, the DON told and the result.',
             see='A log with the visit, the call and the result written.',
             donot=['Do not ask the team member to clock in later to look on time.', 'Do not promise the patient a time.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Never ask anyone to change a time to look right. The record must say what really happened.',
             stop=['The team member says the visit already happened but it does not show.']),
        Step('mo-5', 'A visit is a no-show', m_mo_5,
             do=['Find the **no-show** visit.', 'Read the **status**. It says the visit did not start.'],
             check=['The planned time passed long ago.', 'You called the team member first.'],
             expect='You know the visit did not happen.',
             see='A row that says no-show in a warning color.',
             donot=['Do not reschedule it yourself.', 'Do not call the patient before the DON decides what to say.'],
             alora='Alora documents no-show warnings. The wording must be verified.', astatus='FEATURE',
             zenith='Tell the **DON at once**. The DON decides how to reach the patient and when to reschedule.',
             stop=['Any no-show: tell the DON at once.']),
    ],
    final=['I opened the Live Monitor and read the statuses.', 'I called the team member for every late visit.', 'I told the DON about every late start of care visit and every no-show.',
           'Everything I did is on the Late or Missed Visit Log.', 'I changed no status and no time.'],
    stop=['A start of care visit is late or missed.', 'A visit is more than 30 minutes late.', 'A visit is a no-show.', 'A team member cannot be reached.', 'Someone asks you to change a time or a status.'],
    donot=['Do not change a visit status.', 'Do not ask anyone to clock in or out later.', 'Do not promise the patient a visit time.'],
)


# ============================================================================= P18 EVV exceptions
def m_ev_1():
    m = S4.exceptions_list()
    m.call(1, 'ex_list', 'Visits waiting for review', (200, 420), key='ex_list')
    m.call(2, 'ex_issue', 'What does not match', (600, 92), key='ex_issue')
    return m


def m_ev_2():
    m = S4.exceptions_list()
    m.call(1, 'ex_list.r0', 'Open one visit', (345, 420), key='ex_row')
    return m


def m_ev_3():
    m = S4.exception_detail()
    m.call(1, 'ex_issue', 'What does not match', ('above', 320, 0), key='ex_issue')
    return m


def m_ev_4():
    m = S2.zform('EXCEPTION FOLLOW-UP', [
        ('h', 'THE VISIT'), ('two', 'pt', 'Patient:', 'vis', 'Visit date and time:'), ('line', 'tm', 'Team member:'),
        ('h', 'WHAT DOES NOT MATCH'), ('line', 'what', 'What Alora shows:'),
        ('h', 'WHAT REALLY HAPPENED'), ('line', 'said', 'What the team member said (time of call):'), ('line', 'proof', 'How we can tell (note time, phone log, other):'),
        ('h', 'PASS TO'), ('check', 'to', 'Administrator or DON to decide (always)')])
    m.call(1, 'said', 'What they said', ('right', 0, 0), key='zenith')
    m.call(2, 'proof', 'How we can tell', ('right', 0, 0), key='zenith')
    m.call(3, 'to', 'Administrator decides', ('right', 0, 0), key='zenith')
    return m


def m_ev_5():
    m = S4.exception_detail()
    m.call(1, 'ex_reason', 'Write the reason', (300, 380), key='ex_reason')
    m.call(2, 'ex_approve', 'DO NOT CLICK: DON only', (560, 360), key='ex_approve')
    return m


EVV = Proc(
    id='evv', tab=7, num='P18', title='Review EVV Exceptions',
    purpose='An EVV exception is a visit record that does not match what was planned: a clock-in far from the address, a missing clock-out, a visit too short. '
            'Alora documents that visits can be held for manual review before they are sent. Office staff gather the facts. The Administrator or DON decides.',
    before=['You are signed in (P1).', 'The **Exception Follow-up** form (Tab 11).', 'The Administrator will tell you which payers require EVV for Zenith.'],
    who='Trained office staff. The Administrator or DON approves.', time='10 minutes for each exception.',
    steps=[
        Step('ev-1', 'Open the exception list', m_ev_1,
             do=['Find the **list** of visits waiting for review.', 'Read **what does not match** for each visit.'],
             check=['You know how many visits are waiting.', 'You know what is wrong with each.'],
             expect='A list of visits held for review, each with a reason.',
             see='A list with a visit, a team member and the reason it does not match.',
             alora='Alora documents that visits can be held for manual review. Where the list is and what it is called must be verified.', astatus='FEATURE',
             zenith='Review the exception list every morning (P23).',
             stop=['You cannot find the exception list.']),
        Step('ev-2', 'Open one exception', m_ev_2,
             do=['Click the **visit** you want to review.'],
             check=['You opened one visit only.'],
             expect='The visit opens with the reason it does not match.',
             see='A detail screen for one visit.',
             alora='Open a visit that is held for review. How to open it must be verified.', astatus='FEATURE',
             zenith='One exception at a time. Finish it before you open the next.'),
        Step('ev-3', 'Read what does not match', m_ev_3,
             do=['Read **what does not match**. Write it on the follow-up form.'],
             check=['You understood the reason. If not, ask the Administrator.'],
             expect='You know exactly what does not match.',
             see='A box that names the problem: for example, no clock-out.',
             donot=['Do not guess the reason.'],
             alora='Read the reason a visit is held. The wording must be verified.',
             zenith='Write the wording from the screen. Do not paraphrase.'),
        Step('ev-4', 'Find out what really happened', m_ev_4,
             do=['Call the team member. Write what they **said** and the **time of the call**.', 'Write **how we can tell**: a signed visit note, a phone log, or another record.',
                 'Give the form to the **Administrator or DON**.'],
             enter='On the paper form only. Do not enter anything in Alora yet.',
             check=['You wrote the time of the call.', 'You wrote the team member\'s words, not yours.'],
             expect='The Administrator or DON has the facts.',
             see='A form with the exception, what was said and how we can tell.',
             donot=['Do not ask the team member to change a time.', 'Do not decide the exception is fine because it looks small.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='The record must say what really happened, even when that is uncomfortable.',
             rule='Visit records must be accurate. Changing a record to hide a problem can be fraud.',
             stop=['The team member says the visit did not happen.', 'The team member asks you to change a time.']),
        Step('ev-5', 'Write the reason. Do not approve.', m_ev_5,
             do=['Type the **reason** in words, from the form the Administrator or DON decided.', '**Do not click Approve.** It is for the Administrator or DON.'],
             enter='The reason the Administrator or DON approved, in their words.',
             check=['The reason matches what the Administrator or DON decided.'],
             expect='The reason is in the box. The Administrator or DON approves or sends the visit back.',
             see='A detail screen with a reason and two buttons. You click neither on your own.',
             donot=['Do not click **Approve** or **Send back** without the Administrator or DON.', 'Do not write a reason you were not told.'],
             alora='Enter a reason, then approve or send back. The box and the buttons must be verified.',
             zenith='Office staff prepare. The Administrator or DON approves.',
             stop=['You are asked to approve and you are not authorized.']),
    ],
    final=['I read what did not match.', 'I called the team member and wrote what they said.', 'The Administrator or DON decided.', 'I wrote the reason they gave.',
           'I did not click Approve or Send back myself.', 'I did not change any time.'],
    stop=['The team member says the visit did not happen.', 'Anyone asks you to change or delete a time.', 'You cannot find the facts.', 'The same exception appears again and again.'],
    donot=['Do not change a visit time.', 'Do not approve an exception.', 'Do not delete an exception.', 'Do not write a reason that is not true.'],
)


# ============================================================================= P19 Clinical documentation review
def m_cr_1():
    m = S.dashboard(noa=False)
    m.call(1, 'pend.485', 'Plans of care (485)', ('right', 0, -14), key='dash_pending')
    m.call(2, 'pend.orders', 'Orders', ('right', 0, 0), key='dash_pending')
    m.call(3, 'pend.oasis', 'OASIS', ('right', 0, 14), key='dash_pending')
    return m


def m_cr_2():
    m = S3.pending_list('oasis')
    m.call(1, 'pend', 'Pending OASIS list', (220, 400), key='cl_oasis')
    m.call(2, 'pend.c3', 'Status', (620, 92), key='cl_oasis')
    return m


def m_cr_3():
    m = S3.pending_list('485')
    m.call(1, 'pend', 'Pending plans of care', (200, 400), key='cl_485')
    m.call(2, 'pend.c3', 'Status', (620, 92), key='cl_485')
    return m


def m_cr_4():
    m = S3.pending_list('orders')
    m.call(1, 'pend', 'Pending orders', (220, 400), key='cl_order')
    m.call(2, 'pend.c3', 'Status', (620, 92), key='cl_order')
    return m


def m_cr_5():
    m = S2.zform('CLINICAL DOCUMENT TRACKER', [
        ('h', 'THE ITEM'), ('two', 'pt', 'Patient:', 'item', 'Item (OASIS, 485, order, note):'), ('line', 'due', 'Due date:'),
        ('h', 'WHAT YOU FOUND'), ('check', 'late', 'Waiting longer than the Administrator\'s limit'), ('check', 'miss', 'Missing or not started'),
        ('h', 'WHAT YOU DID'), ('line', 'rem', 'Reminded (name, date and time):'), ('line', 'don', 'Told DON (date):'),
        ('h', 'LOGGED BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')])
    m.call(1, 'late', 'Waiting too long', ('right', 0, 0), key='zenith')
    m.call(2, 'rem', 'Who you reminded', ('right', 0, 0), key='zenith')
    m.call(3, 'don', 'Tell the DON', ('right', 0, 0), key='zenith')
    return m


CLINREV = Proc(
    id='clinrev', tab=7, num='P19', title='Review Clinical Documentation (Office Check)',
    purpose='Office staff do not write or judge clinical documents. They check that the items that must exist do exist, are not stuck, and are moving to the people who complete them. '
            'Alora documents that pending plans of care (485), orders and OASIS are shown in one place.',
    before=['You are signed in (P1).', 'The **Clinical Document Tracker** (Tab 11).', 'The Administrator\'s limit for how long an item may wait.'],
    who='Trained office staff.', time='10 minutes each day.',
    steps=[
        Step('cr-1', 'Find the pending items on the dashboard', m_cr_1,
             do=['Read the count for **plans of care (485)**.', 'Read the count for **orders**.', 'Read the count for **OASIS**.'],
             check=['You wrote the three numbers on the tracker.'],
             expect='You know how many items of each kind are waiting.',
             see='A box with three rows, each with a number.',
             alora='Alora documents pending 485 forms, orders and OASIS shown in one place. Where they are in Zenith\'s Alora must be verified.', astatus='FEATURE',
             zenith='Compare today\'s numbers with yesterday\'s. A number that keeps rising is a problem.'),
        Step('cr-2', 'Look at the pending OASIS list', m_cr_2,
             do=['Open the **list** of pending OASIS.', 'Read the **status** of each item and the date.'],
             check=['You know which items are in progress, waiting for QA, or not started.'],
             expect='You know the status of each OASIS.',
             see='A list of patients with an OASIS item and a status.',
             donot=['Do not open or edit an OASIS. It is a clinical form.'],
             alora='Open a pending OASIS list. The list and its words must be verified.', astatus='FEATURE',
             zenith='An OASIS must be finished within 5 calendar days of the start of care.',
             rule='The comprehensive assessment must be completed within 5 calendar days after the start of care. OASIS must be sent within 30 days.',
             stop=['An OASIS is near its limit and not started.']),
        Step('cr-3', 'Look at the pending plans of care (485)', m_cr_3,
             do=['Open the **list** of pending plans of care.', 'Read the **status**: sent to the doctor, waiting for signature, or signed.'],
             check=['You know which plans are waiting for a physician signature.'],
             expect='You know the status of each plan of care.',
             see='A list of plans of care with a status.',
             donot=['Do not open or edit a plan of care.'],
             alora='Alora documents the plan of care (CMS-485). The list and its words must be verified.', astatus='FEATURE',
             zenith='Follow up with the physician\'s office for an unsigned plan of care on the day the limit is reached.',
             rule='The plan of care must be reviewed and signed by the physician. An unsigned plan of care can stop billing.',
             stop=['A plan of care has waited longer than the Administrator\'s limit.']),
        Step('cr-4', 'Look at the pending orders', m_cr_4,
             do=['Open the **list** of pending orders.', 'Read the **status** of each: needs signature or signed.'],
             check=['Every order has a date and a status.'],
             expect='You know which orders are waiting for a signature.',
             see='A list of orders with a status.',
             donot=['Do not change an order status.'],
             alora='Alora documents pending orders. The list and its words must be verified.', astatus='FEATURE',
             zenith='Follow up on an unsigned order the same day it is found.',
             stop=['A verbal order has no written record.']),
        Step('cr-5', 'Record what you found and remind', m_cr_5,
             do=['Check **waiting too long** for any item past the limit.', 'Write **who you reminded**, with the date and time.', 'Tell the **DON** about anything that is late.'],
             check=['Every late item is on the tracker.', 'The DON knows.'],
             expect='The tracker shows every late item and who was reminded.',
             see='A tracker with the late items and the reminders.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Remind by phone or by the approved message tool. Never send patient details by personal email or text.',
             stop=['An item is late and the clinician does not answer.']),
    ],
    final=['I read the three counts on the dashboard.', 'I looked at the pending OASIS, plans of care and orders.', 'I opened and changed no clinical document.',
           'Every late item is on the tracker.', 'The DON knows about every late item.'],
    stop=['An OASIS is near its 5-day limit and not started.', 'A plan of care or order is unsigned past the limit.', 'A verbal order has no written record.', 'You are asked to complete a clinical form.'],
    donot=['Do not open, edit or complete a clinical form.', 'Do not change a status.', 'Do not sign for a clinician or a physician.'],
)


# ============================================================================= P20 QA review
def m_qa_1():
    m = S4.blank_shell('dash', 'Dashboard')
    m.call(1, 'nav.qa', 'QA menu', ('right', 0, 0), key='nav_qa')
    return m


def m_qa_2():
    m = S4.qa_screen()
    m.call(1, 'qa_items', 'QA list', (200, 400), key='qa_items')
    m.call(2, 'qa_items.c3', 'Status', (620, 92), key='qa_items')
    return m


def m_qa_3():
    m = S2.zform('QA COMPLETENESS CHECK', [
        ('h', 'THE ITEM'), ('two', 'pt', 'Patient:', 'item', 'Item:'),
        ('h', 'IS IT COMPLETE? (OFFICE CHECK ONLY)'), ('check', 'q_id', 'Name and date of birth are right on every page'),
        ('check', 'q_date', 'Dates and times are filled in'), ('check', 'q_sig', 'Signed and dated by the clinician'),
        ('check', 'q_all', 'Every required part is there (Administrator\'s list)'), ('check', 'q_blank', 'Nothing is blank that should not be'),
        ('h', 'RESULT'), ('check', 'q_ok', 'Complete: send to the QA reviewer'), ('check', 'q_no', 'Not complete: list what is missing')])
    m.call(1, 'q_sig', 'Signed and dated', ('right', 0, 0), key='zenith')
    m.call(2, 'q_all', 'Every part is there', ('right', 0, 0), key='zenith')
    m.call(3, 'q_no', 'Missing: list it', ('right', 0, 0), key='zenith')
    return m


def m_qa_4():
    m = S4.qa_screen()
    m.call(1, 'qa_items.r1', 'Needs correction', (200, 400), key='qa_row')
    m.call(2, 'qa_return', 'QA reviewer only', ('above', 0, 0), key='qa_return')
    return m


def m_qa_5():
    m = S2.zform('QA LOG', [
        ('h', 'THE DAY'), ('two', 'dt', 'Date:', 'emp', 'Checked by:'),
        ('h', 'WHAT YOU FOUND'), ('line', 'cnt', 'Items checked / complete / not complete:'), ('line', 'miss', 'Items missing (patient and item):'),
        ('line', 'told', 'Clinician or DON told (name, time):'),
        ('h', 'FOLLOW-UP'), ('line', 'nxt', 'Check again on (date):')])
    m.call(1, 'cnt', 'Count of items', ('right', 0, 0), key='zenith')
    m.call(2, 'told', 'Who was told', ('right', 0, 0), key='zenith')
    m.call(3, 'nxt', 'Check again', ('right', 0, 0), key='zenith')
    return m


QAREV = Proc(
    id='qa', tab=7, num='P20', title='QA Review (Office Completeness Check)',
    purpose='Quality assurance (QA) catches errors before they reach the physician or the payer. Alora documents a QA area. '
            'Office staff check that each item is complete and in the right place. A trained QA reviewer, named by the DON, judges clinical content and sends items back.',
    before=['You are signed in (P1).', 'The **QA Completeness Check** and **QA Log** (Tab 11).', 'The Administrator\'s list of required parts for each item.'],
    who='Trained office staff. A QA reviewer named by the DON approves or sends back.', time='10 to 20 minutes each day.',
    steps=[
        Step('qa-1', 'Open QA', m_qa_1,
             do=['Click **QA** in the main menu on the left.'],
             check=['You are not inside a form.'],
             expect='The QA screen opens.',
             see='A list of items waiting for quality review.',
             alora='Alora documents a QA area. The menu name must be verified.', astatus='FEATURE',
             zenith='Do QA at the same time each day.',
             stop=['You cannot find QA, or you are not allowed in.']),
        Step('qa-2', 'Read the QA list', m_qa_2,
             do=['Read the **list**: each line is a patient and an item.', 'Read the **status** of each: ready for QA, needs correction, or approved.'],
             check=['You know how many items are in each status.'],
             expect='You know what is waiting for QA.',
             see='A list of items with a status.',
             donot=['Do not open an item that is not assigned to you.'],
             alora='Alora documents QA. The list and its status words must be verified.', astatus='FEATURE',
             zenith='Oldest items first.'),
        Step('qa-3', 'Check that the item is complete', m_qa_3,
             do=['Check **signed and dated** only if it is.', 'Check **every part is there** against the Administrator\'s list.', 'If something is missing, check **not complete** and write what is missing.'],
             check=['Every box you checked is true.'],
             expect='The item is marked complete, or you know what is missing.',
             see='A form with the completeness checks and a result.',
             donot=['Do not judge if the clinical content is correct.', 'Do not fill in a blank for the clinician.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Office staff check that parts exist. The QA reviewer judges what is written.'),
        Step('qa-4', 'Items that need correction', m_qa_4,
             do=['Find an item that **needs correction**.', 'The **return for correction** button is for the QA reviewer only. Do not click it.'],
             check=['You gave the missing items to the QA reviewer.'],
             expect='The QA reviewer returns the item to the clinician.',
             see='A list with one item marked needs correction, and a button that only the QA reviewer uses.',
             donot=['Do not click **Return for correction** unless the DON named you as a QA reviewer.', 'Do not edit the item.'],
             alora='Return an item for correction. The button and who may use it must be verified.', astatus='FEATURE',
             zenith='Give the QA reviewer a written list of what is missing.',
             stop=['You are not sure who the QA reviewer is.']),
        Step('qa-5', 'Write the QA log', m_qa_5,
             do=['Write how many items you **checked**, how many were complete and how many were not.', 'Write **who you told** and when.', 'Write when you will **check again**.'],
             check=['The counts match what you saw.'],
             expect='The QA log is complete for the day.',
             see='A log with counts, names and a date to check again.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Give the QA Log to the DON every Friday.'),
    ],
    final=['I read the QA list.', 'I checked each item for completeness.', 'I gave the QA reviewer a written list of what is missing.', 'I clicked nothing that is for the QA reviewer.',
           'The QA Log is complete.'],
    stop=['An item is missing.', 'An item needs correction and you do not know who should fix it.', 'You are asked to approve a clinical item.', 'The same error appears again and again.'],
    donot=['Do not approve a clinical item yourself.', 'Do not change clinical content.', 'Do not return an item unless the DON named you a QA reviewer.'],
)


PAGES = [Divider(7, 'Watch visits as they happen, review visit exceptions, check that clinical documents are moving, and run the daily quality review.',
                 [('monitor', 'P17  Monitor Visits (Live Monitor)'), ('evv', 'P18  Review EVV Exceptions'), ('clinrev', 'P19  Review Clinical Documentation'), ('qa', 'P20  QA Review')]),
         MONITOR, EVV, CLINREV, QAREV]

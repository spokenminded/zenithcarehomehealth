"""Tab 8: billing readiness and the NOA (Notice of Admission) workflow."""
import scenes as S
import scenes2 as S2
import scenes4 as S4
from model import Proc, Step, Divider
from blocks import *


# ============================================================================= P21 Billing readiness
def m_bi_1():
    m = S4.blank_shell('dash', 'Dashboard')
    m.call(1, 'nav.billing', 'Billing menu', ('right', 0, 0), key='nav_billing')
    return m


def m_bi_2():
    m = S4.billing_list()
    m.call(1, 'bill_ready', 'Billing list', (200, 400), key='bill_ready')
    m.call(2, 'bill_ready.c3', 'Claim status', (620, 92), key='bill_ready')
    return m


def m_bi_3():
    m = S4.tab_billing()
    m.call(1, 'tab.bill', 'Billing section', (470, 98), key='tab_bill')
    m.call(2, 'bill_items', 'What is missing?', (200, 458), key='bill_items')
    return m


def m_bi_4():
    m = S2.zform('BILLING READINESS CHECK', [
        ('h', 'PATIENT AND PERIOD'), ('two', 'pt', 'Patient:', 'per', 'Billing period:'),
        ('h', 'CHECK EACH ONE (ALL MUST BE CHECKED)'), ('check', 'b_noa', 'NOA sent and accepted'), ('check', 'b_poc', 'Plan of care signed and dated by the physician'),
        ('check', 'b_oasis', 'OASIS finished and sent'), ('check', 'b_qa', 'Visits documented and approved in QA'), ('check', 'b_evv', 'No open EVV exceptions'),
        ('check', 'b_ord', 'Orders signed'), ('check', 'b_f2f', 'Face-to-face on file'),
        ('h', 'RESULT'), ('check', 'b_ready', 'Ready: tell billing'), ('check', 'b_not', 'Not ready: list what is missing and who owns it')])
    m.call(1, 'b_noa', 'NOA accepted', ('right', 0, 0), key='zenith')
    m.call(2, 'b_poc', 'Plan of care signed', ('right', 0, 0), key='zenith')
    m.call(3, 'b_not', 'Not ready: list it', ('right', 0, 0), key='zenith')
    return m


BILLING = Proc(
    id='billing', tab=8, num='P21', title='Billing Readiness',
    purpose='A claim goes out only when every required item exists. Checking this before the claim is built prevents rejected claims and delayed payment. '
            'Office staff check readiness and route what is missing. Billing staff send claims.',
    before=['You are signed in (P1).', 'The **Billing Readiness Check** (Tab 11).', 'The Administrator\'s billing calendar.'],
    who='Trained office staff. Billing staff send claims.', time='10 minutes for each patient and period.',
    steps=[
        Step('bi-1', 'Open Billing', m_bi_1,
             do=['Click **Billing** in the main menu on the left.'],
             check=['You are not inside a form.'],
             expect='The billing area opens.',
             see='A list of patients and billing periods with a status.',
             alora='Alora documents billing for all payers. The menu name must be verified.', astatus='FEATURE',
             zenith='Check readiness at least 3 business days before the claim is due.',
             stop=['You cannot find Billing, or you are not allowed in.']),
        Step('bi-2', 'Read the billing list', m_bi_2,
             do=['Read the **list**: each line is a patient and a billing period.', 'Read the **claim status** of each: ready, not ready, or a missing item.'],
             check=['You know which patients are not ready.'],
             expect='You know which claims are ready and which are not.',
             see='A list of periods with a claim status.',
             donot=['Do not send a claim. Billing staff send claims.'],
             alora='Alora documents billing. The list and its status words must be verified.', astatus='FEATURE',
             zenith='Work the \'not ready\' lines first.'),
        Step('bi-3', 'Find out what is missing', m_bi_3,
             do=['Open the patient\'s **Billing** section.', 'Read the **items list**. Find the item that is missing or not complete.'],
             check=['You can name each missing item.'],
             expect='You know what is missing for this patient.',
             see='A list of items with complete or missing next to each.',
             donot=['Do not change a status to make an item look complete.'],
             alora='Open the patient\'s billing items. Whether the section shows a list like this must be verified.',
             zenith='The layout may differ. Use the Billing Readiness Check (next step) as the master list.',
             stop=['You cannot tell why the claim is not ready.']),
        Step('bi-4', 'Complete the readiness check and route it', m_bi_4,
             do=['Check **NOA accepted** only if it shows accepted.', 'Check **plan of care signed** only if it is signed and dated.',
                 'If anything is missing, check **not ready** and write what is missing and who owns it.'],
             check=['You checked a box only for something you saw.', 'Every missing item has an owner.'],
             expect='The Billing Readiness Check is complete. Billing staff know if the claim is ready.',
             see='A form with seven checks and a result.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Give the form to billing staff the same day.',
             rule='A home health claim needs a signed plan of care, an accepted OASIS and an accepted NOA before payment.',
             stop=['An item is missing and cannot be fixed before the claim is due.']),
    ],
    final=['I checked each item against what Alora shows.', 'Every missing item is written with an owner.', 'Billing staff have the form.', 'I sent no claim.', 'I changed no status.'],
    stop=['The NOA is late or rejected.', 'An item is missing and the claim is nearly due.', 'You cannot tell why the claim is not ready.', 'Someone asks you to change a status.'],
    donot=['Do not send a claim.', 'Do not change a status.', 'Do not check a box for something you did not see.'],
)


# ============================================================================= P22 NOA workflow
def m_no_1():
    m = S.dashboard()
    m.call(1, 'w_noa', 'NOA timely-filing box', (560, 84), key='dash_noa')
    m.call(2, 'noa_due', 'Five-day deadline', (560, 330), key='dash_noa')
    return m


def m_no_2():
    m = S4.noa_list()
    m.call(1, 'noa_list', 'NOA list', (200, 400), key='noa_row')
    m.call(2, 'noa_status', 'NOA status', (620, 92), key='noa_status')
    return m


def m_no_3():
    m = S2.zform('NOA CHECK', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'soc', 'Start of care date:'),
        ('h', 'BEFORE YOU CREATE THE NOA'), ('check', 'n_soc', 'The SOC visit is done (the nurse completed the visit)'),
        ('check', 'n_id', 'Name, birth date and Medicare number match the card'), ('check', 'n_phy', 'Physician name and NPI match the order'),
        ('line', 'n_due', 'NOA due date (SOC date + 5 calendar days):'),
        ('h', 'CHECKED BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')])
    m.call(1, 'n_soc', 'SOC visit done', ('right', 0, 0), key='zenith')
    m.call(2, 'n_id', 'Numbers match', ('right', 0, 0), key='zenith')
    m.call(3, 'n_due', 'Write the due date', ('right', 0, 0), key='zenith')
    return m


def m_no_4():
    m = S4.noa_list()
    m.call(1, 'noa_list.r0b', 'Create NOA', ('below', 0, 0), key='noa_gen')
    return m


def m_no_5():
    m = S4.noa_list()
    m.call(1, 'noa_status', 'Status: accepted?', (620, 92), key='noa_status')
    m.call(2, 'noa_list', 'NOA list', (200, 400), key='noa_row')
    return m


def m_no_6():
    m = S2.zform('NOA TRACKING LOG', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'soc', 'Start of care date:'),
        ('h', 'NOA'), ('line', 'due', 'Due date:'), ('line', 'sent', 'Sent (date and time, by):'), ('line', 'acc', 'Accepted (date):'),
        ('check', 'rej', 'Rejected: tell the Administrator the same day'),
        ('h', 'LOGGED BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')])
    m.call(1, 'due', 'Due date', ('right', 0, 0), key='zenith')
    m.call(2, 'acc', 'Accepted date', ('right', 0, 0), key='zenith')
    m.call(3, 'rej', 'Rejected: tell the Administrator', ('right', 0, 0), key='zenith')
    return m


NOA = Proc(
    id='noa', tab=8, num='P22', title='NOA Workflow (Notice of Admission)',
    purpose='The NOA tells Medicare that a patient has started care. It must be sent within 5 calendar days of the start of care. '
            'If it is late, payment is reduced for each late day. Alora documents an NOA dashboard widget and one-click NOA generation. '
            'Only staff the Administrator has named click the create button.',
    before=['The start of care date for the patient.', 'The **NOA Check** and the **NOA Tracking Log** (Tab 11).', 'You are signed in (P1).',
            'Ask the Administrator if you are allowed to create and send NOAs.'],
    who='Billing staff. Other office staff prepare and watch.', time='10 minutes for each NOA, plus a daily look until accepted.',
    steps=[
        Step('no-1', 'Find NOAs that are due', m_no_1,
             do=['Read the number in the **NOA box** on the dashboard.', 'Read the **deadline** words under it.'],
             check=['You wrote the number on the daily sheet.'],
             expect='You know how many NOAs still need to be sent.',
             see='A box with a number and the words about the 5-day deadline.',
             alora='Alora documents an NOA widget for timely filing. Where it is and how it looks must be verified.', astatus='FEATURE',
             zenith='Read this box first thing every business day.',
             rule='The NOA is due within 5 calendar days of the start of care. A late NOA reduces payment for each late day.',
             stop=['A number is greater than zero and the due date is today or past.']),
        Step('no-2', 'Open the NOA list', m_no_2,
             do=['Open the **NOA list** (click the box, or find it under Billing).', 'Read each **status**: not sent, sent, accepted or rejected.'],
             check=['You know which patients need an NOA.'],
             expect='A list of patients with their NOA dates and statuses.',
             see='A list with start of care dates, NOA due dates and statuses.',
             alora='Alora documents an NOA list or widget. The name and place of the list must be verified.', astatus='FEATURE',
             zenith='Work the earliest due date first.'),
        Step('no-3', 'Check the patient before creating the NOA', m_no_3,
             do=['Check **SOC visit done**. Do not create an NOA before the nurse completed the visit.', 'Check that name, birth date and **Medicare number** match the card.',
                 'Write the **NOA due date**: SOC date plus 5 calendar days.'],
             check=['The Medicare number matches the insurance card copy exactly.', 'The physician name and NPI match the order.'],
             expect='The NOA Check is complete.',
             see='A form with three checks and a due date.',
             donot=['Do not create an NOA for a patient who has not started care.', 'Do not type a Medicare number from memory.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='A wrong number gets the NOA rejected, and the days keep counting.',
             stop=['The SOC visit has not happened.', 'A number does not match the card.']),
        Step('no-4', 'Create and send the NOA', m_no_4,
             do=['Click **Create NOA** on the patient\'s row. Do this **once**.'],
             enter='Nothing to type if Alora fills the NOA from the record. If it asks for anything, stop and ask the Administrator.',
             check=['You are on the right patient\'s row.', 'You are allowed to create NOAs.'],
             expect='The NOA is created. The status changes to sent or pending.',
             see='The row\'s status changes.',
             donot=['Do not click Create NOA twice.', 'Do not click it if you are not named by the Administrator.'],
             alora='Alora documents one-click NOA generation. The button and what happens next must be verified.', astatus='FEATURE',
             zenith='Only billing staff named by the Administrator create NOAs.',
             ifwrong='An error message appears: do not click again. **Stop** and ask the Administrator.',
             stop=['An error message appears.', 'Alora asks for information you do not have.']),
        Step('no-5', 'Check that it was accepted', m_no_5,
             do=['Find the **status** next business day.', 'Find the patient\'s **row**. It should say accepted.'],
             check=['Status says accepted.', 'You did this the next business day, not a week later.'],
             expect='The NOA is accepted.',
             see='A status that reads accepted.',
             alora='Read the NOA status. The words must be verified.', astatus='FEATURE',
             zenith='Check again each business day until it is accepted.',
             stop=['The status says rejected.', 'The status is still not accepted after 2 business days.']),
        Step('no-6', 'Write it on the tracking log', m_no_6,
             do=['Write the **due date**.', 'Write the date the NOA was **accepted**.', 'If it was rejected, check the box and **tell the Administrator the same day**.'],
             check=['Every date on the log matches what Alora shows.'],
             expect='The NOA Tracking Log is complete for this patient.',
             see='A log with the NOA dates.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Keep the log in the patient\'s billing folder.',
             stop=['The NOA was rejected.']),
    ],
    final=['The SOC visit was done before I created the NOA.', 'Name, birth date and Medicare number matched the card.', 'The NOA was created once, within 5 calendar days of the start of care.',
           'I checked the status until it showed accepted.', 'The NOA Tracking Log is complete.'],
    stop=['The NOA is close to the 5-day limit and not sent.', 'The NOA was rejected.', 'A number does not match the card.', 'Alora gives an error.', 'You are not sure you may create the NOA.'],
    donot=['Do not create an NOA before the SOC visit is done.', 'Do not create an NOA twice.', 'Do not wait for the last day.', 'Do not type a Medicare number from memory.'],
)


PAGES = [Divider(8, 'Check that a patient is ready to bill, and get the Notice of Admission (NOA) sent and accepted on time.',
                 [('billing', 'P21  Billing Readiness'), ('noa', 'P22  NOA Workflow')]),
         BILLING, NOA]

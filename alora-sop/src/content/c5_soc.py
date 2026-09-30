"""Tab 5: the complete Start of Care (SOC) workflow.

Order in the binder:
  1. SOC master flow page (all 14 stages on one page)
  2. SOC clocks page (the dates that matter)
  3. P7  SOC Stage Guide (one picture page for each of the 14 stages)
  4. P7U SOC Document Upload (its own visual procedure: referral, orders, face-to-face)
  5. P13 Prepare and Schedule the SOC Visit (stage 10 in detail)
"""
import scenes as S
import scenes2 as S2
import scenes3 as S3
import scenes4 as S4
from content import c4_documents as C4
from model import Proc, Step, Divider, Text, md
from blocks import *

# ============================================================================= master flow page
STAGES = [
    (1, 'Receive', 'Write down the date and time the packet arrived. Count the pages.', 'Intake staff', 'paper', 'soc-1', 'referral'),
    (2, 'Review', 'Sort the papers. Check that names and dates match. The DON decides.', 'Intake staff, DON', 'paper', 'soc-2', 'referral'),
    (3, 'Find or create patient', 'Search first. Create only after the DON accepts and three searches find nothing.', 'Intake staff', 'alora', 'soc-3', 'find'),
    (4, 'Open patient record', 'Open the one correct record. Name and birth date must match.', 'Intake staff', 'alora', 'soc-4', 'open'),
    (5, 'Upload documents', 'Referral, physician order and face-to-face into the right chart, under the right type.', 'Intake staff', 'alora', 'soc-5', 'socupload'),
    (6, 'Verify documents', 'Open each one. Right patient, readable, in the list only once.', 'Second person', 'alora', 'soc-6', 'verify'),
    (7, 'Enter and verify patient information', 'Name, birth date, address, phone, insurance, physician.', 'Intake staff', 'alora', 'soc-7', 'demographics'),
    (8, 'Verify orders', 'Signed, dated, matches the referral. Give to the DON.', 'Intake staff, DON', 'alora', 'soc-8', 'orders'),
    (9, 'Verify face-to-face', 'Visit date inside the window. Findings written. Signed.', 'Intake staff, DON', 'paper', 'soc-9', 'f2f'),
    (10, 'Prepare and schedule SOC', 'Readiness check, nurse named by the DON, time agreed with the patient, visit on the calendar.', 'Scheduler, DON', 'alora', 'soc-10', 'socprep'),
    (11, 'Verify clinical workflow', 'Confirm the SOC visit, the OASIS and the plan of care show where they should.', 'Office, DON', 'alora', 'soc-11', 'soc-11'),
    (12, 'Monitor', 'Watch the visit and any exceptions until the SOC visit is done.', 'Office', 'alora', 'soc-12', 'soc-12'),
    (13, 'QA', 'Run the QA list. Send back anything that needs correction.', 'Office, DON', 'alora', 'soc-13', 'soc-13'),
    (14, 'Billing readiness', 'NOA sent within 5 calendar days. Nothing missing before the claim.', 'Billing', 'alora', 'soc-14', 'soc-14'),
]


def _flow_html():
    rows = []
    for n, name, desc, who, kind, stage_pg, detail in STAGES:
        rows.append(f'<li class="{kind}"><span class="n">{n}</span><span class="t">{md(name)}</span><span class="d">{md(desc)}</span>'
                    f'<span class="w">{md(who)}</span><span class="p">{md("{{pg:" + stage_pg + "}}")}</span></li>')
    return '<ol class="flow">' + ''.join(rows) + '</ol>'


FLOW_PAGE = Text('soc-flow', 5, 'The SOC workflow on one page', (
    '<h1 class="ttl">Start of Care: the whole workflow on one page</h1>'
    '<p class="sub">Do the stages in this order. Do not skip a stage. Each stage has its own picture page. The last column is the page to turn to.</p>'
    '<div class="flowkey"><span><i></i>Done in Alora (desktop website)</span><span><i class="paper"></i>Done on paper or at the scanner</span></div>'
    + _flow_html()
    + P('**Print the SOC Desk Checklist** ({{pg:soc-checklist}}). Use one for each patient. Initial each section as you finish it.')
    + KBOX('If a stage cannot be finished', 'Stop at that stage. Write the problem on the SOC Desk Checklist (Tab 11). Tell the Administrator or DON the same day. Do not start the next stage.', 'red')
), kind='text')

CLOCKS_PAGE = Text('soc-clocks', 5, 'The SOC clocks', (
    '<h1 class="ttl">The SOC clocks</h1>'
    '<p class="sub">Five time limits start when a referral arrives or care starts. Missing one can delay care or reduce payment. Write the dates on the SOC Desk Checklist the day the packet arrives.</p>'
    + TABLE(['Clock', 'Starts', 'Due', 'Who watches'], [
        ['**First nurse visit** (initial assessment)', 'The referral arrives, or the patient returns home', 'Within **48 hours**, or on the start of care date the physician ordered', 'Intake, then the DON'],
        ['**Face-to-face visit** (paper)', 'Start of care date', 'The visit happened **90 days before** to **30 days after** the start of care', 'Intake staff, then the DON'],
        ['**Comprehensive assessment** (OASIS)', 'Start of care date', 'Finished within **5 calendar days** after the start of care', 'The assessing nurse, then the DON'],
        ['**OASIS sent**', 'The day the assessment is finished', 'Sent within **30 days**', 'QA'],
        ['**NOA** (Notice of Admission)', 'Start of care date', 'Sent within **5 calendar days** of the start of care. Late NOAs reduce payment for each late day.', 'Billing'],
    ], widths=['24%', '24%', '32%', '20%'])
    + KBOX('How to use this page', UL([
        'On the day a referral arrives, write the **48-hour deadline** at the top of the SOC Desk Checklist (Tab 11).',
        'When the SOC visit is scheduled, write the **NOA due date** (SOC date plus 5 calendar days).',
        'Count calendar days, not business days. Weekends and holidays count.',
        'The Administrator confirms these rules each year. If this page and the Administrator disagree, follow the Administrator.']), 'gold')
    + KBOX('Federal rule', 'These clocks come from the Medicare Conditions of Participation for home health agencies and the Medicare home health payment rules. '
           'The initial assessment visit is due within 48 hours of the referral (or of the patient\'s return home), or on the start of care date ordered by the physician. '
           'The comprehensive assessment is due within 5 calendar days after the start of care.', 'blue')
    + KBOX('Stop and ask the Administrator or DON if', UL(['A clock will be missed or is already missed.', 'The physician wants a start date that is later than 48 hours.', 'The patient asks to start later.', 'You are not sure which date to count from.']), 'red')
), kind='text')


# ============================================================================= P7 SOC stage guide (14 pictures)
def m_s3():
    m = S.patients_list(results=True, selected=0, query=('Smith', '03/14/1941'))
    m.call(1, 'pt_search_field', 'Search box', (330, 82), key='pt_search_field')
    m.call(2, 'pt_results.r0', 'One match: open it', (470, 410), key='pt_result_row')
    m.call(3, 'btn_new_pt', 'New: only after P5B', ('left', 0, -12), key='btn_new_pt')
    return m


def _banner_calls(m):
    m.call(1, 'pt_name', 'Name matches', ('right', 0, -6), key='pt_banner')
    m.call(2, 'pt_ids', 'Birth date matches', (560, 118), key='pt_banner')


def m_s4():
    m = S.patient_record('sum')
    _banner_calls(m)
    m.call(3, 'tab.docs', 'Documents section', (400, 300), key='tab_docs')
    return m


def m_s5():
    m = S.tab_docs(rows=[])
    m.call(1, 'btn_upload', 'Add / upload button', ('left', 0, 0), key='btn_upload')
    m.call(2, 'docs_list', 'Is it already here?', (300, 380), key='docs_list')
    return m


def m_s7():
    m = S.tab_demographics('a')
    m.call(1, 'f_lname', 'Last name', ('right', 0, 0), key='f_lname')
    m.call(2, 'f_dob', 'Date of birth', ('right', 0, 0), key='f_dob')
    m.call(3, 'f_addr', 'Address', ('right', 40, 0), key='f_addr')
    m.call(4, 'f_phone', 'Phone', ('right', 0, 0), key='f_phone')
    return m


def m_s8():
    m = S.tab_orders(rows=[['Home health evaluate and treat', '09/27/2026', 'Sample, Jane MD', ('chip', 'Signed', 'ok')]], sel=0)
    m.call(1, 'ord_list.r0', 'The order row', (300, 340), key='cl_order')
    m.call(2, 'ord_list.c2', 'Physician name', (470, 410), key='cl_order')
    m.call(3, 'ord_list.c3', 'Status', (640, 340), key='cl_order')
    return m


def m_s9():
    m = S3.f2f_timeline()
    m.call(1, 'enc', 'Visit date: inside', (330, 330), key='zenith')
    m.call(2, 'soc', 'Start of care date', (640, 112), key='zenith')
    return m


def m_s10():
    m = S4.new_visit_form()
    m.call(1, 'f_visit_pt', 'Patient', ('right', 0, 0), key='f_visit_pt')
    m.call(2, 'f_visit_type', 'Visit type', ('right', 0, 0), key='f_visit_type')
    m.call(3, 'f_visit_date', 'Date', ('right', 0, 0), key='f_visit_date')
    m.call(4, 'f_visit_member', 'Team member', ('right', 0, 0), key='f_visit_member')
    m.call(5, 'btn_save', 'Save', ('above', 60, 16), key='btn_save')
    return m


def m_s11():
    m = S.dashboard(noa=False)
    m.call(1, 'pend.485', 'Plans of care (485)', ('right', 0, -14), key='dash_pending')
    m.call(2, 'pend.orders', 'Orders', ('right', 0, 0), key='dash_pending')
    m.call(3, 'pend.oasis', 'OASIS', ('right', 0, 14), key='dash_pending')
    return m


def m_s12():
    m = S4.live_monitor()
    m.call(1, 'lm_table', 'Find the SOC visit', (200, 420), key='lm_table')
    m.call(2, 'lm_status', 'Read the status', (600, 92), key='lm_status')
    return m


def m_s13():
    m = S4.qa_screen()
    m.call(1, 'qa_items', 'Find the patient\'s item', (200, 400), key='qa_items')
    m.call(2, 'qa_items.c3', 'Status', (620, 92), key='qa_items')
    return m


def m_s14():
    m = S4.noa_list()
    m.call(1, 'noa_list', 'Find the patient\'s row', (200, 400), key='noa_row')
    m.call(2, 'noa_status', 'NOA status', (620, 92), key='noa_status')
    return m


def _nt(text):
    return text


SOC = Proc(
    id='socstages', tab=5, num='P7', title='SOC Stage Guide (14 stages)',
    purpose='One picture page for each of the 14 stages of a Start of Care, in the order you do them. Each stage tells you where to look, what to click, and what to check. '
            'Where a stage has its own full procedure, the page tells you which one and where to find it.',
    before=['A referral packet for a new patient.', 'A **SOC Desk Checklist** (Tab 11). Fill in one for each patient. Initial each stage as you finish it.',
            'You are signed in to Alora (P1) and know your way around the dashboard (P2).'],
    who='Intake staff (stages 1 to 9), scheduler and DON (10), office team and billing (11 to 14).',
    time='Stages 1 to 9: about 1 hour of office time. Stage 10: 15 minutes. Stages 11 to 14: a few minutes on each day.',
    steps=[
        Step('soc-1', 'Receive the packet', C4.m_ref_1,
             do=['Write the **date and time** the packet arrived.', 'Write **how** it arrived and who **sent** it.', 'Count the pages and write the **number of pages**.'],
             enter='On the paper log only. Nothing in Alora yet.',
             check=['The time is the real arrival time. Use the fax time stamp if there is one.', 'The page count matches the pages you hold.'],
             expect='One new line on the intake log, and the 48-hour deadline written on the SOC Desk Checklist.',
             see='The intake log with the date, the time, the sender and the page count.',
             donot=['Do not leave the time blank.', 'Do not round the time.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Log every packet within 15 minutes of arrival.',
             rule='The first nurse visit is due within 48 hours of the referral, so the arrival time must be exact.',
             key_note='Full procedure: **P6**, {{pg:referral}}.'),
        Step('soc-2', 'Review the packet', C4.m_ref_3,
             do=['Check the **same name and birth date** are on every page.', 'Check that a **physician order** for home health is in the packet.',
                 'Complete: check **Send to the DON**. Missing items: list them and call the referral source.'],
             check=['You compared every page.', 'You did not guess anything that is missing.'],
             expect='The packet is with the DON, or marked with what is missing.',
             see='A review form with clear marks and, if needed, a list of missing items.',
             donot=['Do not decide if Zenith can take the patient. The DON decides.', 'Do not call the patient to promise a start date.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Office staff check that the papers are there and match. The DON decides.',
             stop=['Names or birth dates differ between pages.', 'There is no order.'],
             key_note='Full procedure: **P6**, {{pg:referral}}.'),
        Step('soc-3', 'Find the patient, or create one only if allowed', m_s3,
             do=['Search by last name and date of birth.', 'Exactly one match: **open that row**.',
                 'No match: **stop** here. Go to P5B only after the DON has accepted and you searched three ways. Do not click New before that.'],
             check=['Two identifiers match: name and date of birth.'],
             expect='You have one matching record, or a confirmed \'no match\'.',
             see='One matching row, or a message that no patient was found.',
             donot=['Do not click **New** because the first search found nothing.', 'Do not open a row if two patients look alike.'],
             alora='Use the patient search. Box and button names must be verified.',
             zenith='A duplicate patient is one of the most costly office mistakes. Search three ways before you create anyone.',
             stop=['Two patients match.', 'The patient is shown as active or discharged and you did not expect it.'],
             key_note='Full procedures: **P3**, {{pg:find}}, and **P5B**, {{pg:newpatient}}.'),
        Step('soc-4', 'Open the patient record', m_s4,
             do=['Read the **name** at the top. It must be the name in the packet.', 'Read the **date of birth** and record number.',
                 'Note where the **Documents** section is. You use it next.'],
             check=['Name and date of birth match the referral.'],
             expect='The correct patient record is open.',
             see='The patient banner with the same name and birth date as the packet.',
             donot=['Do not go on if the name is even slightly different.'],
             alora='Open the patient record. Section names must be verified.', astatus='FEATURE',
             zenith='Write the record number on the SOC Desk Checklist.',
             stop=['The name or birth date does not match.'],
             key_note='Full procedure: **P4**, {{pg:open}}.'),
        Step('soc-5', 'Upload the documents', m_s5,
             do=['Click the **add or upload button** in the Documents section.', 'First look at the list: is the document **already there**?'],
             check=['You are in the correct patient\'s record.', 'The document is not already listed.'],
             expect='An upload window opens.',
             see='A window to choose a file and a document type.',
             donot=['Do not upload before you confirm the patient name in stage 4.', 'Do not upload a document that is already listed.'],
             alora='Start an upload from the patient\'s documents. The button name must be verified.', astatus='FEATURE',
             zenith='Upload the referral, the physician order and the face-to-face documentation. Each has its own type.',
             stop=['You cannot find an add or upload button.'],
             key_note='Full procedure with pictures for each document: **SOC Document Upload**, {{pg:socupload}}.'),
        Step('soc-6', 'Verify the documents', C4.m_ver_1,
             do=['Look at the **list** of documents. Your uploads are there.', 'Check the **type** column: each document has the right type.'],
             check=['Every document is listed once.', 'You opened each document and read the patient name.'],
             expect='Every document is in the chart once, with the right type, and opens.',
             see='A list with a row for each document you uploaded.',
             donot=['Do not assume it is fine because the upload finished.'],
             alora='The document list shows what is stored in the chart.', astatus='FEATURE',
             zenith='A second person verifies orders and face-to-face documents.',
             stop=['A document is in the wrong chart: tell the Administrator **now**.'],
             key_note='Full procedure: **P10**, {{pg:verify}}.'),
        Step('soc-7', 'Enter and verify patient information', m_s7,
             do=['Check the **last name** against the referral.', 'Check the **date of birth**.', 'Check the **address**.', 'Check the **phone** number.'],
             check=['Each item matches the referral and the face sheet.', 'Insurance and physician (next page of the record) also match.'],
             expect='The demographics match the documents, or you reported a difference.',
             see='A demographics section with the patient\'s details.',
             donot=['Do not change a detail because it looks wrong. Report it.', 'Do not guess a missing detail.'],
             alora='Open the demographics section. The field names must be verified.', astatus='FEATURE',
             zenith='Office staff enter and check administrative information. A change to a clinical detail needs the DON.',
             stop=['A detail in Alora is different from the document.'],
             key_note='Full procedure: **P5**, {{pg:demographics}}.'),
        Step('soc-8', 'Verify the physician order', m_s8,
             do=['Find the **order row** in the patient\'s Orders section.', 'Check the **physician** name.', 'Check the **status**: it matches the paper.'],
             check=['The order is for this patient and asks for home health.', 'It is signed and dated.'],
             expect='You know the order is present and signed, and the DON has it.',
             see='An order with a status and the physician\'s name.',
             donot=['Do not change, add to or sign an order.', 'Do not decide what an order means.'],
             alora='Open the orders for the patient. The section name must be verified.',
             zenith='Every new order goes to the DON the same day.',
             stop=['The order is not signed or not dated.', 'The patient name differs.'],
             key_note='Full procedure: **P11**, {{pg:orders}}.'),
        Step('soc-9', 'Verify the face-to-face documentation', m_s9,
             do=['Find the **date of the face-to-face visit** on the document.', 'Check it is between 90 days before and 30 days after the **start of care date**.'],
             check=['You counted the days with a calendar.', 'The document has findings and a signature.'],
             expect='The visit date is inside the window, or the DON knows it is not.',
             see='A timeline with the visit date inside the colored window.',
             donot=['Do not guess a date that is not written.', 'Do not decide that an outside date is acceptable.'],
             alora='Not an Alora step. This is a check on a document.', astatus='ZENITH',
             zenith='Tell the DON the same day about any problem. Do not wait for the start of care.',
             rule='The face-to-face visit must be no more than 90 days before, or up to 30 days after, the start of care and must relate to the main reason for home health.',
             stop=['The date is outside the window.', 'There is no signature.'],
             key_note='Full procedure: **P12**, {{pg:f2f}}.'),
        Step('soc-10', 'Prepare and schedule the SOC visit', m_s10,
             do=['Choose the **patient**.', 'Choose the **visit type**: start of care.', 'Enter the **date** agreed with the patient.',
                 'Choose the **team member** the DON named.', 'Check everything, then click **Save** once.'],
             enter='Only what the DON and the patient agreed. See P13 for the full check.',
             check=['The nurse is the one the DON named.', 'The date is inside the 48-hour limit, or the physician ordered a later date.', 'Any alert is read, not ignored.'],
             expect='The SOC visit appears on the schedule.',
             see='The visit form with patient, type, date and team member filled in.',
             donot=['Do not schedule before the DON has accepted the referral and named the nurse.', 'Do not click Save twice.'],
             alora='Add a visit on the schedule. The form and its names must be verified.', astatus='FEATURE',
             zenith='Call the patient to agree the time before you save the visit.',
             rule='The first nurse visit is due within 48 hours of the referral, or on the date the physician ordered.',
             stop=['No nurse is free inside the 48 hours.', 'An alert says the visit breaks a rule.'],
             key_note='Full procedures: **P13**, {{pg:socprep}}, and **P14**, {{pg:schedule}}.'),
        Step('soc-11', 'Verify that the clinical workflow is in place', m_s11,
             do=['Find **plans of care (485)**. The patient\'s plan will appear after the SOC visit.', 'Find **orders** waiting for a signature.',
                 'Find **OASIS**. The start of care OASIS will be listed once the nurse starts it.'],
             check=['The SOC visit is on the schedule.', 'Nothing for this patient is unexpectedly waiting.'],
             expect='You know what is waiting for the nurse or the physician for this patient.',
             see='The dashboard pending items box with counts.',
             donot=['Do not open, edit or complete a clinical form. That is for clinicians.', 'Do not change a status.'],
             alora='Alora documents that pending 485 forms, orders and OASIS are shown together. Where they appear in Zenith\'s Alora must be verified.', astatus='FEATURE',
             zenith='Office staff only confirm that the items exist and are moving. Clinicians complete them.',
             stop=['An item is waiting longer than the Administrator\'s limit.', 'The SOC visit is not on the schedule.'],
             key_note='See also **P19**, {{pg:clinrev}}.'),
        Step('soc-12', 'Monitor the SOC visit', m_s12,
             do=['Find the **SOC visit** in the list on the day.', 'Read the **status**: on time, late, no-show or complete.'],
             check=['The status matches what the nurse tells you.'],
             expect='You know if the visit happened, is late, or did not happen.',
             see='A list of visits for today with a color and a word for each status.',
             donot=['Do not change a visit status yourself.'],
             alora='Live Monitor shows visits as they happen, with color-coded warnings. Where to open it must be verified.', astatus='FEATURE',
             zenith='Check at the start of the visit window and again one hour later. Report a late or missed SOC visit to the DON at once.',
             rule='A late first visit can put the 48-hour deadline at risk.',
             stop=['The SOC visit is late or did not happen.'],
             key_note='Full procedures: **P17**, {{pg:monitor}}, and **P18**, {{pg:evv}}.'),
        Step('soc-13', 'Run the QA check', m_s13,
             do=['Find the patient\'s **item** in the QA list.', 'Read its **status**. \'Needs correction\' means it goes back.'],
             check=['Every SOC item for this patient is listed.', 'You checked completeness only, not clinical content.'],
             expect='Each SOC item is approved, or sent back with a reason.',
             see='A QA list with a status for each item.',
             donot=['Do not approve a clinical item yourself.', 'Do not change clinical content.'],
             alora='Alora documents a QA area. The menu name and the list must be verified.', astatus='FEATURE',
             zenith='Office staff check that every item is present and complete. The DON approves clinical content.',
             stop=['An item is missing.', 'An item needs correction and you are not sure who should fix it.'],
             key_note='Full procedure: **P20**, {{pg:qa}}.'),
        Step('soc-14', 'Check billing readiness and the NOA', m_s14,
             do=['Find the patient\'s **row** in the NOA list.', 'Read the **NOA status**. Send the NOA if it is due and you are allowed to.'],
             check=['The NOA is sent within 5 calendar days of the start of care.', 'The NOA due date is on the SOC Desk Checklist.'],
             expect='The NOA is sent and accepted, or the billing person knows it is due.',
             see='A list with the start of care date, the due date and the NOA status.',
             donot=['Do not send an NOA for a patient who has not started care.', 'Do not wait for the last day.'],
             alora='Alora documents an NOA widget and one-click NOA creation. Where they are in Zenith\'s Alora must be verified.', astatus='FEATURE',
             zenith='The NOA is checked every business day until it is accepted.',
             rule='The NOA is due within 5 calendar days of the start of care. A late NOA reduces payment for each late day.',
             stop=['The NOA is close to the 5-day limit and not sent.', 'The NOA was rejected.'],
             key_note='Full procedures: **P21**, {{pg:billing}}, and **P22**, {{pg:noa}}.'),
    ],
    final=['Stages 1 to 9 are initialed on the SOC Desk Checklist.', 'The SOC visit is on the schedule, with a nurse the DON named, inside the 48-hour limit.',
           'Nothing is waiting for the nurse or physician that I did not report.', 'The NOA due date is written on the checklist and tracked.',
           'Any unresolved item is written on the checklist and the Administrator or DON has been told.'],
    stop=['The 48-hour deadline cannot be met.', 'Any stage reports a problem you cannot resolve with this manual.', 'A document is in the wrong chart.',
          'The order or face-to-face documentation is missing or not valid.'],
    donot=['Do not skip a stage.', 'Do not start a later stage because an earlier one is slow.', 'Do not mark a box on the checklist for something you did not do.'],
)


# ============================================================================= P7U SOC document upload (its own visual procedure)
def _soc_rows(n):
    allrows = [['SMITH_MARY_REFERRAL_20260928.pdf', 'Referral', '09/28/2026', '09/28/2026'],
               ['SMITH_MARY_ORDER_20260927.pdf', 'Physician order', '09/27/2026', '09/28/2026'],
               ['SMITH_MARY_F2F_20260915.pdf', 'Face-to-face', '09/15/2026', '09/28/2026']]
    return allrows[:n]


def m_su_1a():
    m = S.patients_list(results=True, selected=0, query=('Smith', '03/14/1941'))
    m.call(1, 'pt_search_field', 'Patient search', (330, 82), key='pt_search_field')
    m.call(2, 'pt_results.r0c0', 'Patient name', (200, 186), key='pt_result_row', pad=3)
    m.call(3, 'pt_results.r0', 'Open patient record', (520, 186), key='pt_open', pad=8)
    return m


def m_su_1b():
    m = S.patient_record('sum')
    _banner_calls(m)
    return m


def m_su_2():
    m = S.tab_docs(rows=[])
    m.call(1, 'tab.docs', 'Documents', (330, 206), key='tab_docs')
    m.call(2, 'docs_list', 'Patient\'s document list', (430, 330), key='docs_list')
    return m


def m_su_3a():
    m = S.upload_dialog()
    m.call(1, 'btn_upload', 'Add button', ('below', 0, 0), key='btn_upload')
    m.call(2, 'dlg_file', 'Choose file', ('left', 0, 0), key='dlg_file')
    return m


def m_su_3b():
    return C4.m_up_5()


def m_su_3c():
    m = S.upload_dialog(doctype='Referral', filename='SMITH_MARY_REFERRAL_20260928.pdf', date='09/28/2026')
    m.call(1, 'dlg_file', 'File is the referral', ('left', 0, 0), key='dlg_file')
    m.call(2, 'dlg_type', 'Type: Referral', ('left', 0, 0), key='dlg_type')
    m.call(3, 'dlg_date', 'Document date', ('left', 0, 0), key='dlg_date')
    m.call(4, 'dlg_save', 'Save', ('right', 0, 0), key='dlg_save')
    return m


def _dlg(doctype, filename, date, rows):
    m = S.upload_dialog(doctype=doctype, filename=filename, rows=rows, date=date)
    m.call(1, 'btn_upload', 'Add button', ('below', 0, 0), key='btn_upload')
    m.call(2, 'dlg_file', 'Choose file', ('left', 0, 0), key='dlg_file')
    m.call(3, 'dlg_type', 'Document type', ('left', 0, 0), key='dlg_type')
    m.call(4, 'dlg_date', 'Document date', ('left', 0, 0), key='dlg_date')
    m.call(5, 'dlg_save', 'Save', ('right', 0, 0), key='dlg_save')
    return m


def m_su_4():
    return _dlg('Physician order', 'SMITH_MARY_ORDER_20260927.pdf', '09/27/2026', _soc_rows(1))


def m_su_5():
    return _dlg('Face-to-face', 'SMITH_MARY_F2F_20260915.pdf', '09/15/2026', _soc_rows(2))


def m_su_6a():
    m = S.tab_docs(rows=_soc_rows(3))
    m.call(1, 'docs_list', 'The list', (180, 440), key='docs_list')
    m.call(2, 'docs_list.c1', 'Type column', (380, 440), key='docs_list')
    m.call(3, 'docs_list.c2', 'Date column', (600, 440), key='docs_list')
    return m


def m_su_6b():
    m = S3.alora_doc_open()
    m.call(1, 'v_name', 'Name on the page', ('right', 0, 0), key='doc_view')
    m.call(2, 'v_pages', 'Page count', ('right', 0, 0), key='doc_view')
    return m


SOCUPLOAD = Proc(
    id='socupload', tab=5, num='P7U', title='SOC Document Upload',
    purpose='To put the three documents of a Start of Care packet into the **correct patient\'s** chart in Alora, each under its own document type, and to prove they are there. '
            'The three documents are the **referral**, the **physician order** and the **face-to-face documentation**. '
            'Alora documents scanned-document storage for patients; every button name here must be verified in live Alora.',
    before=['The three files are scanned, named and checked, and waiting in **Ready to upload** (P9): referral, order, face-to-face.',
            'The packet paper. The patient\'s name and date of birth.', 'You are signed in (P1).'],
    who='Trained intake staff. A second person verifies orders and face-to-face.', time='About 20 minutes for all three documents.',
    steps=[
        Step('su-1a', 'Find the correct patient', m_su_1a, label='1A',
             do=['Type the patient\'s **last name** and **date of birth** in the search box.', 'Read the **name** in the results. Check it against the packet.',
                 'Click the **row** to open the patient record.'],
             enter='Last name and date of birth, as written on the referral.',
             check=['Only one row matches the name and date of birth.', 'If there are two, **stop**.'],
             expect='The patient record opens.',
             see='A results list with one row that matches your packet.',
             donot=['Do not open a row just because the name looks close.'],
             alora='Use the patient search and open the record. Box and row names must be verified.', astatus='FEATURE',
             zenith='Two identifiers must match: name and date of birth.',
             stop=['Two patients match.', 'No patient matches.'],
             key_note='Full procedure: **P3**, {{pg:find}}.'),
        Step('su-1b', 'Open the record and confirm who it is', m_su_1b, label='1B',
             do=['Read the **name** in the banner. It must be the name in the file names.', 'Read the **date of birth**. It must be the date on the documents.'],
             check=['Name and date of birth match every document you will upload.'],
             expect='You are in the right chart before you upload anything.',
             see='The patient banner with the same name and birth date as the packet.',
             donot=['Do not upload anything if the name is even slightly different.'],
             alora='Open the patient record.', astatus='FEATURE',
             zenith='Verify the document belongs to this patient **before** you upload it.',
             stop=['Name or birth date does not match: close the record and ask the Administrator.'],
             key_note='Full procedure: **P4**, {{pg:open}}.'),
        Step('su-2', 'Open the patient\'s document area', m_su_2, label='2',
             do=['Click the **Documents** section below the patient name.', 'Look at the patient\'s **document list**. A new patient often has an empty list.'],
             check=['The section you opened shows documents, not orders or visits.', 'Note any document already listed. You will not add it twice.'],
             expect='The document list for this patient.',
             see='The patient name at the top. A list of documents underneath, or an empty list.',
             alora='Alora documents paperless records (scanned document storage). The section name and its place must be verified.', astatus='FEATURE',
             zenith='If you cannot find the documents section, do not use another section. Ask the Administrator.',
             stop=['You cannot find a documents section.']),
        Step('su-3a', 'Referral: click Add, then Choose file', m_su_3a, label='3A',
             do=['Click the **add or upload button** in the document list. A window opens.', 'In the window, click **Choose file**. A Windows window opens (next page).'],
             check=['You are still in the correct patient\'s Documents section.', 'The window you opened says it adds a document.'],
             expect='The upload window is open. No file is chosen yet.',
             see='An upload window with \'No file chosen\', and the document list behind it.',
             donot=['Do not click Save yet.'],
             alora='Start an upload, then choose a file. The names of both buttons must be verified.', astatus='FEATURE',
             zenith='Open the window only after you confirmed the patient name (step 1B).',
             stop=['You cannot find an add or upload button.', 'No window opens.']),
        Step('su-3b', 'Referral: pick the file in the Windows window', m_su_3b, label='3B',
             do=['Click your **referral file**.', 'Check that the **file name** box shows the same name.', 'Click **Open**.'],
             check=['The file name starts with the patient\'s last name and ends with REFERRAL and a date.', 'You are in the Ready to upload folder.'],
             expect='The window closes and the file name appears in the upload window.',
             see='Back in Alora, the upload window now shows the referral file name.',
             donot=['Do not pick a file from Downloads or the desktop.'],
             alora='Not an Alora screen. This is the standard Windows \'Open\' window. It appears when you click Choose file.', astatus='ZENITH',
             zenith='Choose only from the Ready to upload folder. You use this same window for the order and the face-to-face document.'),
        Step('su-3c', 'Referral: choose the type, check, and Save', m_su_3c, label='3C',
             do=['Check that the **file** is the referral.', 'Choose the document type **Referral**.', 'Type the **document date** from the referral.', 'Check everything. Click **Save** once.'],
             enter='Type: Referral. Document date: the date on the referral, as month/day/year.',
             check=['File name is the referral file.', 'Type is Referral.', 'Document date matches the paper.', 'The patient name at the top of the chart is correct.'],
             expect='The window closes. The referral is in the list.',
             see='An upload window with the file name, the type Referral and a date.',
             donot=['Do not click Save more than once.', 'Do not choose \'Other\' unless the Administrator told you to.'],
             alora='Choose a document type, set a date and save. Every button name and the list of types must be verified.',
             zenith='One last check before Save: right patient, right file, right type, right date.',
             ifwrong='No type matches, or an error message appears: do not click Save. **Stop** and ask the Administrator.',
             stop=['No document type matches.', 'An error message appears.']),
        Step('su-4', 'Physician order: add, choose, type, date, Save', m_su_4, label='4',
             do=['Click the **add or upload button**.', 'Click **Choose file** and pick the **order file** (as in 3B).', 'Choose the document type **Physician order**.',
                 'Type the **document date**: the date the physician wrote the order.', 'Check everything. Click **Save** once.'],
             enter='Type: Physician order. Document date: the date on the order, as month/day/year.',
             check=['File name ends with ORDER and the order date.', 'Type is Physician order.', 'Document date matches the order.'],
             expect='The order is in the list, under the referral.',
             see='The upload window with the order file and the type Physician order. Behind it, one document already listed.',
             donot=['Do not use the type for referral or face-to-face.', 'Do not sign or change the order.'],
             alora='Same upload steps as the referral. The type name must be verified.',
             zenith='A physician order is always uploaded under its own type so the DON can find it.',
             stop=['No type matches a physician order.']),
        Step('su-5', 'Face-to-face: add, choose, type, date, Save', m_su_5, label='5',
             do=['Click the **add or upload button**.', 'Click **Choose file** and pick the **face-to-face file** (as in 3B).', 'Choose the document type **Face-to-face**.',
                 'Type the **document date**: the date of the face-to-face visit.', 'Check everything. Click **Save** once.'],
             enter='Type: Face-to-face. Document date: the date of the face-to-face visit.',
             check=['File name ends with F2F and the visit date.', 'Type is Face-to-face.', 'Document date is the visit date.'],
             expect='The face-to-face document is in the list, under the order.',
             see='The upload window with the face-to-face file and its type. Behind it, two documents already listed.',
             donot=['Do not upload a face-to-face document from a different patient.', 'Do not skip it because the order is signed.'],
             alora='Same upload steps. The type name must be verified.',
             zenith='Upload the face-to-face documentation when the payer requires it. Medicare home health requires it.',
             rule='Medicare home health requires a face-to-face encounter documented in the record.',
             stop=['No type matches face-to-face documentation.', 'There is no face-to-face document: tell the DON the same day.']),
        Step('su-6a', 'Verify: the completed document list', m_su_6a, label='6A',
             do=['Look at the **list**. It should show three documents for this patient.', 'Read the **type** of each: Referral, Physician order, Face-to-face.', 'Read the **dates**. They match the paper.'],
             check=['Three rows. No fourth row. No row twice.', 'Each type matches its file name.', 'Each date matches the paper.'],
             expect='The list shows the referral, the order and the face-to-face documentation, once each.',
             see='A list with three rows. Each row has a file name, a type and a date. This is what a finished upload looks like.',
             donot=['Do not delete a duplicate yourself. Report it.'],
             alora='The document list shows what is stored in the chart.', astatus='FEATURE',
             zenith='Verify in the same session. Do not leave it for later.',
             stop=['A row is missing, shows twice, or has the wrong type.']),
        Step('su-6b', 'Verify: open each document', m_su_6b, label='6B',
             do=['Click a **document** to open it. Find the **patient name** on the page.', 'Find the **page count**. Look at every page.'],
             check=['The document opens and is not blank or cut off.', 'The name on the page is the patient in the banner.', 'Repeat for all three documents.'],
             expect='All three documents open and show the right patient.',
             see='A document viewer with the patient name and the page count.',
             donot=['Do not remove the scan file from the folder until all three are verified.'],
             alora='Open a document from the list. The viewer and its buttons must be verified.',
             zenith='A document you did not open is not verified. Initial the SOC Desk Checklist only after all three open.',
             stop=['A document will not open.', 'A page shows a different patient.'],
             key_note='Full verification procedure: **P10**, {{pg:verify}}.'),
    ],
    final=['Referral uploaded.', 'Physician order uploaded.', 'Face-to-Face documentation uploaded when required.', 'Correct patient.', 'Correct document.',
           'Correct date.', 'Document opens successfully.', 'No duplicate document.'],
    stop=['You are not sure the patient is correct.', 'No document type matches.', 'An error message appears.', 'A document shows twice.', 'A document will not open.',
          'A document went into another patient\'s chart: tell the Administrator **at once**. Do not try to fix it.', 'The face-to-face documentation is missing.'],
    donot=['Do not upload into the wrong patient\'s chart.', 'Do not delete a clinical document unless the Administrator or DON tells you.',
           'Do not guess the type. Ask.', 'Do not click Save twice.', 'Do not mark a box on the SOC Desk Checklist until you have opened the document.'],
)


# ============================================================================= P13 Prepare and schedule the SOC visit
def m_pr_1():
    m = S2.zform('SOC READINESS CHECK', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'dob', 'DOB:'),
        ('h', 'READY TO SCHEDULE? (ALL MUST BE CHECKED)'),
        ('check', 'r_acc', 'DON or Administrator accepted the referral'), ('check', 'r_ord', 'Physician order uploaded, signed, dated'),
        ('check', 'r_f2f', 'Face-to-face uploaded, date in the window'), ('check', 'r_demo', 'Name, address, phone and insurance match'),
        ('check', 'r_docs', 'All documents verified (P10)'),
        ('h', 'DEADLINE'), ('line', 'r_48', '48 hours from the referral ends:')])
    m.call(1, 'r_acc', 'DON accepted', ('right', 0, 0), key='zenith')
    m.call(2, 'r_docs', 'Documents verified', ('right', 0, 0), key='zenith')
    m.call(3, 'r_48', 'Write the deadline', ('right', 0, 0), key='zenith')
    return m


def m_pr_2():
    m = S2.zform('SOC ASSIGNMENT', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'dob', 'DOB:'),
        ('h', 'NAMED BY THE DON'), ('line', 'a_rn', 'Nurse (RN) for the start of care:'), ('line', 'a_dis', 'Other disciplines ordered:'),
        ('line', 'a_init', 'DON initials:'),
        ('h', 'SCHEDULER'), ('line', 'a_when', 'Earliest time the nurse can go:')])
    m.call(1, 'a_rn', 'Nurse named by DON', ('right', 0, 0), key='zenith')
    m.call(2, 'a_init', 'DON initials', ('right', 0, 0), key='zenith')
    m.call(3, 'a_when', 'When the nurse can go', ('right', 0, 0), key='zenith')
    return m


def m_pr_3():
    m = S2.zform('SOC CALL NOTES', [
        ('h', 'THE CALL'), ('line', 'c_who', 'Spoke with (name and relationship):'), ('line', 'c_when', 'Date and time of the call:'),
        ('h', 'CONFIRM'), ('check', 'c_addr', 'Address and phone number confirmed'), ('check', 'c_name', 'Told the patient the nurse\'s name'),
        ('line', 'c_agree', 'Agreed visit date and time:'),
        ('h', 'IF THE PATIENT ASKS FOR A LATER DATE'), ('check', 'c_later', 'Tell the DON the same day. Do not agree to a later date yourself.')])
    m.call(1, 'c_who', 'Who you spoke with', ('right', 0, 0), key='zenith')
    m.call(2, 'c_agree', 'Agreed date and time', ('right', 0, 0), key='zenith')
    m.call(3, 'c_later', 'Later date: ask the DON', ('right', 0, 0), key='zenith')
    return m


def m_pr_4():
    m = S4.new_visit_form()
    m.call(1, 'f_visit_pt', 'Patient', ('right', 0, 0), key='f_visit_pt')
    m.call(2, 'f_visit_type', 'Start of care', ('right', 0, 0), key='f_visit_type')
    m.call(3, 'f_visit_date', 'Agreed date', ('right', 0, 0), key='f_visit_date')
    m.call(4, 'f_visit_time', 'Agreed time', ('right', 0, 0), key='f_visit_time')
    m.call(5, 'f_visit_member', 'Nurse the DON named', ('right', 0, 0), key='f_visit_member')
    return m


def m_pr_5():
    m = S4.new_visit_form(alerts=True)
    m.call(1, 'sch_alerts', 'Read every alert', ('below', 0, 0), key='sch_alerts')
    m.call(2, 'btn_save', 'Save once', ('above', 60, 16), key='btn_save')
    return m


def m_pr_6():
    m = S4.schedule_calendar(extra_visit=True)
    m.call(1, 'sch_visit', 'SOC visit is here', ('below', -40, 10), key='sch_visit')
    m.call(2, 'sch_range', 'Week view', ('above', 60, 0), key='sch_range')
    return m


def m_pr_7():
    m = S2.zform('SOC DESK CHECKLIST (EXTRACT)', [
        ('h', 'SCHEDULING'), ('check', 's_vis', 'SOC visit scheduled (date and time written below)'),
        ('check', 's_dis', 'Appropriate discipline assigned'), ('check', 's_ver', 'Schedule verified on the calendar'),
        ('line', 's_dt', 'SOC date and time:'), ('line', 's_noa', 'NOA due date (SOC date + 5 days):'),
        ('h', 'DONE BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')])
    m.call(1, 's_ver', 'Verified on the calendar', ('right', 0, 0), key='zenith')
    m.call(2, 's_noa', 'Write the NOA due date', ('right', 0, 0), key='zenith')
    m.call(3, 'emp_row', 'Initials and date', ('right', 0, 0), key='zenith')
    return m


SOCPREP = Proc(
    id='socprep', tab=5, num='P13', title='Prepare and Schedule the SOC Visit',
    purpose='Stage 10 of the SOC workflow. Before anyone is scheduled, the office proves the packet is ready, the DON names the nurse, the patient agrees on a time, '
            'and then the start of care visit is put on the Alora schedule and checked. The first nurse visit is due within 48 hours of the referral, unless the physician ordered a later date.',
    before=['Stages 1 to 9 are initialed on the SOC Desk Checklist.', 'The **SOC Readiness Check**, **SOC Assignment** and **SOC Call Notes** forms (Tab 11).',
            'The referral arrival time, and the DON or Administrator\'s accepted decision.'],
    who='Scheduler. The DON names the nurse.', time='15 to 25 minutes.',
    steps=[
        Step('pr-1', 'Check that the patient is ready', m_pr_1,
             do=['Check **DON accepted** only if the DON\'s initials are on the decision.', 'Check **documents verified** only after P10.', 'Write the **48-hour deadline**.'],
             check=['Every box above is checked. If not, stop and finish that step first.'],
             expect='A readiness check with every box checked and the deadline written.',
             see='A form with every box checked and a date and time for the deadline.',
             donot=['Do not schedule a patient who is not ready.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='A patient is scheduled only when the readiness check is complete.',
             rule='The first nurse visit is due within 48 hours of the referral, or on the start of care date ordered by the physician.',
             stop=['A box cannot be checked.']),
        Step('pr-2', 'Get the nurse from the DON', m_pr_2,
             do=['Write the **nurse** the DON names.', 'The DON writes **initials**.', 'Write when the nurse **can go**.'],
             check=['You did not choose the nurse yourself.'],
             expect='The DON named the nurse and initialed.',
             see='A form with the nurse\'s name and the DON\'s initials.',
             donot=['Do not assign a clinician without the DON.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='The DON assigns clinicians for the start of care.',
             stop=['No nurse can go before the 48-hour deadline.']),
        Step('pr-3', 'Call the patient and agree a time', m_pr_3,
             do=['Write **who** you spoke with.', 'Write the **date and time** you agreed.', 'If the patient wants a **later** date, stop and tell the DON the same day.'],
             enter='On the paper form only: the name, the call time and the agreed visit time.',
             check=['The agreed time is before the 48-hour deadline, or the DON agreed to a later date.'],
             expect='A visit date and time the patient agreed to.',
             see='A call form with a name, a call time and an agreed time.',
             donot=['Do not promise a later date.', 'Do not discuss the patient\'s care or diagnosis on the call. Schedule only.'],
             alora='Not an Alora step. This is a Zenith office step.', astatus='ZENITH',
             zenith='Use the phone number from the chart. Identify yourself as calling from Zenith Care Home Health. Give out no health information until you are sure who you are speaking with.',
             stop=['You cannot reach the patient within 4 hours of the deadline.', 'The patient refuses the visit.']),
        Step('pr-4', 'Add the SOC visit in Alora', m_pr_4,
             do=['Choose the **patient**.', 'Choose the visit type **start of care**.', 'Enter the **date** you agreed.', 'Enter the **time** you agreed.', 'Choose the **nurse** the DON named.'],
             enter='Only what is written on your forms. Do not change anything to make an alert go away.',
             check=['Patient name and date of birth are right.', 'The nurse is the one on the SOC Assignment.', 'Date and time match the SOC Call Notes.'],
             expect='The form is filled in and not saved yet.',
             see='A visit form with the five boxes filled in.',
             donot=['Do not guess the visit type.', 'Do not use another nurse because this one seems busy.'],
             alora='Add a visit from the schedule. The button, the form and the visit type names must be verified.', astatus='FEATURE',
             zenith='Fill the form only from the paper forms. Never from memory.',
             stop=['The visit type \'start of care\' is not in the list.', 'The nurse is not in the list.']),
        Step('pr-5', 'Read the alerts, then Save', m_pr_5,
             do=['Read **every alert**. Alora can warn about a conflict, a missing authorization or a visit-frequency problem.', 'If the alerts are fine, click **Save** once.'],
             check=['You read every alert.', 'An alert about a conflict is reported to the DON, not clicked away.'],
             expect='The form closes and the visit is saved.',
             see='A visit form with an alert box at the right, then the schedule after Save.',
             donot=['Do not click through an alert without reading it.', 'Do not click Save more than once.'],
             alora='Alora documents conflict and compliance alerts while scheduling. How the alerts look must be verified.', astatus='FEATURE',
             zenith='An alert is a question for the DON. You do not answer it alone.',
             ifwrong='An error message appears: do not click Save again. **Stop** and ask the Administrator.',
             stop=['An alert names a conflict, a missing authorization or a frequency problem.', 'An error message appears.']),
        Step('pr-6', 'Check the visit is on the calendar', m_pr_6,
             do=['Find the **SOC visit** on the calendar.', 'Use the **week** view for the nurse. Check the day, the time and the nurse.'],
             check=['The visit shows once, on the right day, at the right time, for the right nurse.'],
             expect='The SOC visit is on the calendar exactly once.',
             see='A calendar with a highlighted SOC visit on the day you chose.',
             donot=['Do not drag or edit a visit to make it fit. Ask the DON.'],
             alora='Alora documents schedule views by patient, team member and day, week or month. The view names must be verified.', astatus='FEATURE',
             zenith='Verify in the same session you scheduled.',
             stop=['The visit is missing, or shows twice, or shows for a different nurse.']),
        Step('pr-7', 'Close out: checklist, NOA date, tell the nurse', m_pr_7,
             do=['Check **verified on the calendar** only if you saw it.', 'Write the **NOA due date**: SOC date plus 5 calendar days.', 'Write your **initials and the date**.'],
             check=['The SOC date and time on the checklist match the calendar.', 'The NOA date is five calendar days after the SOC date.'],
             expect='The Scheduling section of the SOC Desk Checklist is complete.',
             see='A checklist with the scheduling boxes checked and the dates written.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Tell the DON the visit is scheduled. Do not wait to be asked.',
             rule='The NOA is due within 5 calendar days of the start of care date.'),
    ],
    final=['The readiness check is complete and the 48-hour deadline is written.', 'The DON named the nurse.', 'The patient agreed to the time (or the DON agreed to a later date).',
           'The SOC visit is on the Alora calendar exactly once, for the right nurse.', 'The NOA due date is written on the SOC Desk Checklist.', 'The DON knows the visit is scheduled.'],
    stop=['The 48-hour deadline cannot be met.', 'The patient asks for a later date.', 'An alert appears while you schedule.', 'No nurse is available.', 'The patient cannot be reached.'],
    donot=['Do not schedule before the DON names the nurse.', 'Do not promise the patient a later date.', 'Do not ignore an alert.', 'Do not save the visit twice.'],
)


FLOW_PAGE.toc = True
CLOCKS_PAGE.toc = True

PAGES = [Divider(5, 'The full Start of Care workflow, from the moment a referral packet arrives to billing readiness. Do the stages in order.',
                 [('soc-flow', 'The SOC workflow on one page'), ('soc-clocks', 'The SOC clocks'), ('socstages', 'P7  SOC Stage Guide (14 stages)'),
                  ('socupload', 'P7U  SOC Document Upload'), ('socprep', 'P13  Prepare and Schedule the SOC Visit')]),
         FLOW_PAGE, CLOCKS_PAGE, SOC, SOCUPLOAD, SOCPREP]

"""Tab 3: Patient records. Find, open, review, create."""
import scenes as S
import scenes2 as S2
from model import Proc, Step, Divider, Text
from blocks import *


# ============================================================================= P3 Find a patient
def m_find_1():
    m = S.dashboard()
    m.call(1, 'nav.patients', 'Patients menu item', (170, 440), key='nav_patients')
    m.call(2, 'search', 'Or: the top search box', (330, 84), key='search')
    return m


def m_find_2():
    m = S.patients_list(results=False, query=('Smith', '03/14/1941'))
    m.call(1, 'pt_search_field', 'Last name', ('below', 0, 0), key='pt_search_field')
    m.call(2, 'pt_dob', 'Date of birth', ('below', 0, 0), key='f_dob')
    m.call(3, 'pt_search_btn', 'Search button', ('below', 0, 0), key='pt_search_btn')
    return m


def m_find_3():
    m = S.patients_list(results=True, selected=0, query=('Smith', '03/14/1941'))
    m.call(1, 'pt_results.r0c0', 'Name matches', (186, 418), key='pt_results')
    m.call(2, 'pt_results.r0c1', 'Birth date matches', (390, 418), key='pt_results')
    m.call(3, 'pt_results.r0c2', 'Record number', (620, 418), key='pt_result_row')
    return m


FIND = Proc(
    id='find', tab=3, num='P3', title='Find a Patient',
    purpose='To find the right patient every time. Opening or saving into the wrong patient is the most serious and most common office mistake. '
            'You will use two identifiers (name and date of birth) before you open anything.',
    before=['The patient\'s **full name** and **date of birth** from the referral, order or face sheet.',
            'The source document in your hand.', 'You are signed in with your own login (P1).'],
    who='Every office employee.', time='2 minutes.',
    steps=[
        Step('find-1', 'Go to the patient search', m_find_1,
             do=['Click the **patients menu item** on the left.',
                 'Or click the **top search box** if Zenith uses it. Use only one of the two.'],
             check=['You are not inside another patient\'s record.'],
             expect='A patient search screen opens.',
             see='A screen with a box to search for a patient and, underneath, a list.',
             alora='Alora documents intake, referral tracking and patient record features. The menu word and the search place must be verified.',
             astatus='FEATURE',
             zenith='Search from the main menu, never from inside another patient\'s chart.',
             ifwrong='Nothing opens or the screen is different: **stop** and ask. Do not try other menu items.'),
        Step('find-2', 'Type the last name and birth date', m_find_2,
             do=['Click the **last name** box. Type the patient\'s last name.',
                 'If the screen has a **date of birth** box, click it and type the date.',
                 'Click the **Search** button.'],
             enter='Last name exactly as on the source document. Date of birth as month/day/year. Do not type the first name alone.',
             check=['The spelling matches the document.', 'You typed the date of birth, not today\'s date.'],
             expect='A list of patients with a matching name appears.',
             see='A list of rows. Each row shows a name, a date of birth and other details.',
             donot=['Do not search with only a first name.', 'Do not guess a spelling. If unsure, try the part you are sure of.'],
             alora='Enter the patient\'s name in the search and start the search. Box and button names must be verified.',
             zenith='Search by last name plus date of birth. If there is no result, search once more with a shorter spelling before you decide the patient is new.',
             stop=['Nothing is found. Go to P5B only after the duplicate check in P5B step 1.']),
        Step('find-3', 'Choose the correct patient', m_find_3,
             do=['Compare the **name** in this row with the source document.',
                 'Compare the **date of birth** in this row with the source document.',
                 'Write the **record number** on your SOC Desk Checklist. This row is now your patient. Do not open it yet.'],
             check=['Two identifiers match: name AND date of birth.', 'No other row has the same name and birth date.', 'The status looks reasonable (for example Active or Pending).'],
             expect='You know exactly which row is the right patient.',
             see='One row that matches the document in name and date of birth.',
             donot=['Do not open a patient because the name looks close.', 'Do not choose a row with a different birth date.'],
             alora='Alora shows matching patients in a list. Column names must be verified.',
             zenith='Two identifiers must match the source document before you open a chart.',
             stop=['Two rows match in name and birth date.', 'Nothing matches but you believe the patient is already in Alora.', 'The patient\'s status is discharged or unexpected and you do not know why.']),
    ],
    final=['I searched by last name (and date of birth when available).', 'Name AND date of birth match the source document.',
           'I found only one matching patient.', 'I did not open a patient I was unsure about.'],
    stop=['Two patients have the same name and date of birth.', 'You cannot tell which record is correct.',
          'The patient cannot be found but you think the patient has been here before.', 'The source document has no date of birth.'],
    donot=['Do not open a patient just because the name looks close.', 'Do not create a new patient before you finish the duplicate check (P5B).',
           'Do not use a nickname instead of the legal name.'],
)


# ============================================================================= P4 Open a patient record
def m_open_1():
    m = S.patients_list(results=True, selected=0, query=('Smith', '03/14/1941'))
    m.call(1, 'pt_results.r0c0', 'Click the patient name', (300, 410), key='pt_open')
    return m


def m_open_2():
    m = S.patient_record('sum')
    m.call(1, 'pt_name', 'Patient name', (200, 250), key='pt_banner')
    m.call(2, 'pt_ids', 'Birth date, record number', (470, 250), key='pt_banner')
    return m


def m_open_3():
    m = S.patient_record('sum')
    m.call(1, 'tab.demo', 'Demographics', (170, 230), key='tab_demo')
    m.call(2, 'tab.docs', 'Documents', (360, 310), key='tab_docs')
    m.call(3, 'tab.orders', 'Orders', (520, 230), key='tab_orders')
    m.call(4, 'tab.sched', 'Schedule', (690, 310), key='tab_sched')
    return m


OPEN = Proc(
    id='open', tab=3, num='P4', title='Open a Patient Record',
    purpose='To open the chart of the patient you found in P3, and to prove to yourself that the name at the top of the screen is the patient you meant.',
    before=['You finished P3 and chose exactly one row.', 'The source document is next to you.'],
    who='Every office employee.', time='1 minute.',
    steps=[
        Step('open-1', 'Open the record', m_open_1,
             do=['Click the **patient\'s name** in the row you chose.'],
             check=['You clicked the row you compared in P3.'],
             expect='The patient record opens.',
             see='A screen with the patient\'s name in a banner at the top and a row of sections under it.',
             alora='Select the patient in the search results to open the record. How Alora opens a record must be verified.',
             zenith='Open only the row you compared. Never open several patients at once.',
             ifwrong='A different patient opened: close it with the main menu and **stop**. Tell the Administrator if you saved anything.'),
        Step('open-2', 'Confirm the name, birth date and record number', m_open_2,
             do=['Read the **patient name** in the banner. Compare it with the source document.',
                 'Read the **date of birth** and record number. Compare them with the source document.'],
             check=['Name matches.', 'Date of birth matches.', 'You are on the correct patient before you type or upload anything.'],
             expect='You have confirmed the patient.',
             see='The banner at the top: the name, the date of birth, the record number and a status.',
             donot=['Do not skip this step. Every save and every upload depends on it.'],
             alora='The patient banner shows who is open. Its exact layout must be verified.',
             zenith='Say the name and date of birth out loud and compare them with the source document before you save, upload or change anything.',
             stop=['The name or date of birth does not match: **stop**. Close the record and ask the Administrator.']),
        Step('open-3', 'Learn the sections of the record', m_open_3,
             do=['**Demographics**: name, address, phone, language.',
                 '**Documents**: scanned papers and uploads.',
                 '**Orders**: physician orders.',
                 '**Schedule**: the patient\'s visits.'],
             check=['You know which section holds what.'],
             expect='You can name the sections you will use most.',
             see='A row of section names under the banner. The open one is marked.',
             alora='Alora documents paperless (scanned) records and a patient communication log. The section names and their order must be verified.',
             astatus='FEATURE',
             zenith='Learn the sections before you touch them. Each procedure in this manual tells you which section to use.',
             key_note='Your record may show more sections, such as Clinical, Billing and Communication log. Write the real section names in the margin once verified.'),
    ],
    final=['The record that opened is the patient I searched for.', 'Name and date of birth on the screen match the source document.',
           'I know which section holds demographics, documents, orders and schedule.', 'I changed nothing.'],
    stop=['The banner shows a different name or birth date.', 'The status is unexpected (for example discharged) and you do not know why.',
          'The record looks empty or damaged.'],
    donot=['Do not type, upload or save until you finish step 2.', 'Do not keep two patient records open at once.'],
)


# ============================================================================= P5 Review demographics
def m_demo_1():
    m = S.patient_record('sum')
    m.call(1, 'tab.demo', 'Demographics section', (170, 230), key='tab_demo')
    return m


def m_demo_2():
    m = S.tab_demographics('a')
    m.call(1, 'f_lname', 'Last name', ('right', 0, 0), key='f_lname')
    m.call(2, 'f_dob', 'Date of birth', ('right', 0, 0), key='f_dob')
    m.call(3, 'f_addr', 'Address', ('right', 0, 0), key='f_addr')
    m.call(4, 'f_phone', 'Phone', ('right', 0, 0), key='f_phone')
    return m


def m_demo_3():
    m = S.tab_demographics('b')
    m.call(1, 'f_payer', 'Insurance', ('right', 0, 0), key='f_payer')
    m.call(2, 'f_phys', 'Physician', ('right', 0, 0), key='f_phys')
    return m


def m_demo_4():
    m = S2.zform('RECORD CORRECTION REQUEST', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'dob', 'DOB:'),
        ('h', 'WHAT DOES NOT MATCH'), ('line', 'field', 'Field in Alora:'), ('line', 'alora', 'What Alora shows:'), ('line', 'src', 'What the document shows:'),
        ('line', 'doc', 'Document name and date:'),
        ('h', 'REQUESTED BY'), ('two', 'emp', 'Employee:', 'date', 'Date:'),
        ('h', 'ADMINISTRATOR / DON'), ('check', 'ok', 'Approved: make this change'), ('check', 'no', 'Not approved: no change')])
    m.call(1, 'alora', 'What Alora shows', ('right', 0, 0), key='zenith')
    m.call(2, 'src', 'What the document shows', ('right', 0, 0), key='zenith')
    m.call(3, 'ok', 'Administrator approves', ('right', 0, 0), key='zenith')
    return m


DEMO = Proc(
    id='demographics', tab=3, num='P5', title='Review Patient Demographics',
    purpose='To check that the patient\'s name, birth date, address, phone, language, insurance and physician in Alora match the source documents. '
            'Wrong details cause wrong claims, missed calls and visits to the wrong address.',
    before=['The patient\'s record is open and confirmed (P4).', 'The referral or face sheet and the insurance card copy.'],
    who='Intake and admission staff.', time='5 minutes.',
    steps=[
        Step('demo-1', 'Open the demographics section', m_demo_1,
             do=['Click the **demographics section** under the patient banner.'],
             expect='The patient\'s personal details open.',
             see='A screen with boxes for name, birth date, address, phone and other details. They already have information in them.',
             alora='Open the patient\'s demographic details. Section name and place must be verified.',
             zenith='Only look. Do not click Edit on this step.',
             donot=['Do not click an edit button yet.']),
        Step('demo-2', 'Compare name, birth date and address', m_demo_2,
             do=['Compare the **last name** (and the first name below it) with the document.',
                 'Compare the **date of birth** with the document.',
                 'Compare the **address** with the document.',
                 'Compare the **phone** number with the document.'],
             check=['Every letter of the name matches.', 'The birth date matches exactly.', 'Street number, street name and ZIP code match.'],
             expect='Each detail matches the document, or you have a list of differences.',
             see='The details in Alora next to your document. Point at each one with your finger as you compare.',
             donot=['Do not change anything because it \'looks wrong\'.', 'Do not guess a missing detail.'],
             alora='Read the demographic fields. Field names must be verified.',
             zenith='A difference is not yours to fix. Write it down and go to step 4.'),
        Step('demo-3', 'Compare insurance and physician', m_demo_3,
             do=['Compare the **insurance** name and ID number with the insurance card copy.',
                 'Compare the **physician** name with the order or referral.'],
             check=['Insurance ID matches the card, character by character.', 'The physician is the one on the order.', 'The physician\'s NPI matches (when shown).'],
             expect='Insurance and physician match the documents.',
             see='An insurance entry and a physician entry that match the papers.',
             alora='Alora documents unlimited insurance records per patient and a physician lookup from the national NPI registry. The fields and their place must be verified.',
             astatus='FEATURE',
             zenith='More than one insurance entry is normal. Check that the **current** one is correct and first.',
             stop=['You cannot find the physician or the insurance and do not know why.']),
        Step('demo-4', 'Report a difference (do not fix it yourself)', m_demo_4,
             do=['Write what **Alora shows** and what the **document shows**.',
                 'Write the document name and date. Sign and give the form to the Administrator.',
                 'Wait for the Administrator\'s **approval** before any change.'],
             enter='Only on the paper form: the patient, the field, both values and the document. Nothing in Alora.',
             check=['Both values are written exactly.'],
             expect='The Administrator has your form. No change is made in Alora until approved.',
             see='A filled-in Record Correction Request form.',
             donot=['Do not change a name, birth date or insurance number on your own.', 'Do not delete a patient.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Changes to name, date of birth, insurance or physician need the Administrator\'s OK. A plain spelling mistake that the source document proves can be fixed by intake after the Administrator initials the form.'),
    ],
    final=['Name, birth date, address and phone match the source document.', 'Insurance and physician match.',
           'I listed every difference on a Record Correction Request.', 'I changed nothing without approval.'],
    stop=['Name or birth date differs from the document.', 'The insurance number differs.', 'You are asked to change something you cannot prove with a document.',
          'The patient may already exist under a different spelling.'],
    donot=['Do not change clinical information.', 'Do not guess a missing detail.', 'Do not merge or delete patient records.'],
)


# ============================================================================= P6 Create a new patient
def m_new_1():
    m = S2.patients_none('Smith')
    m.call(1, 'pt_search_field', 'Search again first', (330, 82), key='pt_search_field')
    m.call(2, 'pt_none', 'Nothing found', (560, 392), key='pt_none')
    return m


def m_new_2():
    m = S.patients_list(results=False, query=('Smith', ''))
    m.call(1, 'btn_new_pt', 'New patient button', (470, 84), key='btn_new_pt')
    return m


def m_new_3():
    m = S2.new_patient_form('a')
    m.call(1, 'f_refdate', 'Referral date', ('right', 0, 0), key='f_refdate')
    m.call(2, 'f_lname', 'Legal last name', ('right', 0, 0), key='f_lname')
    m.call(3, 'f_dob', 'Date of birth', ('right', 0, 0), key='f_dob')
    return m


def m_new_4():
    m = S2.new_patient_form('b')
    m.call(1, 'f_payer', 'Insurance', ('right', 0, 0), key='f_payer')
    m.call(2, 'f_memberid', 'Insurance ID', ('right', 0, 0), key='f_memberid')
    m.call(3, 'f_phys', 'Physician', ('right', 0, 0), key='f_phys')
    return m


def m_new_5():
    m = S2.new_patient_form('b')
    m.call(1, 'btn_save', 'Save button', ('above', 0, 0), key='btn_save')
    return m


NEWPT = Proc(
    id='newpatient', tab=3, num='P5B', title='Create a New Patient',
    purpose='To add a patient who is truly new to Alora, after you prove that the patient is not already there. '
            'A duplicate record splits a patient\'s history in two and can cause wrong care and wrong billing.',
    before=['You finished the search in P3 twice and found nothing.', 'The referral, face sheet and insurance card copy.',
            'The **Administrator\'s or DON\'s OK to admit** (Zenith standard).', 'The **New Patient Check** form (Tab 11). Write your three searches on it.'],
    who='Trained intake staff only.', time='10 minutes.',
    steps=[
        Step('new-1', 'Prove the patient is not already in Alora', m_new_1,
             do=['Search again with a **shorter or different spelling** of the last name.',
                 'Check that the search really found **nothing**.'],
             enter='Try the last name only, then the first three letters of the last name, then the date of birth alone if the screen allows it.',
             check=['Three different searches found nothing.', 'You also tried the maiden name or a nickname if the referral lists one.'],
             expect='You are sure the patient is new.',
             see='A message that says nothing was found (the wording may vary).',
             donot=['Do not create a patient after a single search.'],
             alora='Use the patient search to look for an existing record before you add one.',
             zenith='Search three ways before you create a patient.',
             stop=['Anything close to the name or birth date appears: **stop** and go back to P3.']),
        Step('new-2', 'Open the new patient form', m_new_2,
             do=['Click the **new patient button**.'],
             check=['You have the Administrator\'s or DON\'s OK.'],
             expect='A blank new patient form opens.',
             see='A form with empty boxes for the patient\'s details.',
             alora='Alora documents intake, referral tracking and patient admission processing. The button word and place must be verified.',
             astatus='FEATURE',
             zenith='Do not start a new patient form without the Administrator\'s or DON\'s OK to admit.',
             stop=['You do not see a new patient button. Your role may not allow it: **stop** and ask.']),
        Step('new-3', 'Enter the referral date and the patient\'s legal details', m_new_3,
             do=['Type the **referral date** (the day Zenith received the referral).',
                 'Type the patient\'s **legal last and first name** exactly as on the insurance card.',
                 'Type the **date of birth** as month/day/year.'],
             enter='Referral date, legal name, date of birth, address, phone and language from the source documents. Nothing from memory.',
             check=['Spelling matches the insurance card.', 'Date of birth is correct.', 'The referral date is the day the referral arrived.'],
             expect='The boxes show the information from the document.',
             see='A form with the details filled in. Nothing is saved yet.',
             donot=['Do not guess a missing detail. Leave it blank and ask.', 'Do not use nicknames.'],
             alora='Enter the patient\'s details in the new patient form. Box names must be verified.',
             zenith='Two people check the legal name and date of birth against the card before you save.',
             rule='The first nurse visit is due within 48 hours of the referral, so the referral date and time must be correct.'),
        Step('new-4', 'Enter insurance and physician', m_new_4,
             do=['Choose or type the **insurance** name.',
                 'Type the **insurance ID** from the card. Check each character.',
                 'Choose the **physician**. Use the lookup if the screen offers one.'],
             enter='Insurance name and ID from the card copy. Physician name and NPI from the order.',
             check=['The ID matches the card.', 'The physician matches the order.'],
             expect='Insurance and physician are filled in.',
             see='A form with insurance and physician filled in. Nothing is saved yet.',
             alora='Alora documents unlimited insurance entries and a physician lookup from the national NPI registry. Field names and their place must be verified.',
             astatus='FEATURE',
             zenith='If the physician is not found, ask the Administrator. Do not type a physician from memory.'),
        Step('new-5', 'Save, then verify the new record', m_new_5,
             do=['Check the whole form once more against the documents. Then click **Save** one time and wait.'],
             check=['Every box matches the source documents.'],
             expect='The new patient\'s record opens with the name in the banner.',
             see='The patient banner with the correct name, date of birth and a new record number.',
             alora='Save the new patient. The button word and what happens next must be verified.',
             zenith='After saving, search for the patient (P3) and confirm that exactly one record exists.',
             ifwrong='An error message appears or the page does not change: do not click Save again. **Stop** and ask the Administrator.'),
    ],
    final=['I proved the patient was not already in Alora.', 'I had the Administrator\'s or DON\'s OK.', 'Legal name, birth date, insurance and physician match the documents.',
           'Searching for the patient now finds exactly one record.', 'I wrote the new record number on the SOC Desk Checklist.'],
    stop=['You found anything close to the name or birth date.', 'You do not have the Administrator\'s or DON\'s OK to admit.', 'A detail is missing or does not match.',
          'An error message appears when you save.', 'You saved twice by mistake.'],
    donot=['Do not create a patient to \'test\' the system.', 'Do not create a patient after only one search.', 'Do not click Save more than once.',
           'Do not merge or delete records.'],
)

PAGES = [Divider(3, 'Find the right patient, open the record, check the demographics, and (only when needed) add a new patient.',
                 [('find', 'P3  Find a Patient'), ('open', 'P4  Open a Patient Record'), ('demographics', 'P5  Review Patient Demographics'), ('newpatient', 'P5B  Create a New Patient')]),
         FIND, OPEN, DEMO, NEWPT]

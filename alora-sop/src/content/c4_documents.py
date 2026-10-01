"""Tab 4: Referral, scanning and naming, uploading, verifying, orders, face-to-face."""
import scenes as S
import scenes2 as S2
import scenes3 as S3
from model import Proc, Step, Divider, Text
from blocks import *


# ============================================================================= P6 Process a referral
def m_ref_1():
    m = S2.zform('SOC PACKET INTAKE LOG', [
        ('h', 'WHEN AND HOW IT ARRIVED'), ('line', 'when', 'Date and time received:'),
        ('line', 'how', 'How received (fax, e-fax, email, hand):'), ('line', 'from', 'Sent by (name and phone):'),
        ('line', 'pages', 'Number of pages:'),
        ('h', 'LOGGED BY'), ('two', 'emp', 'Employee:', 'init', 'Initials:')])
    m.call(1, 'when', 'Date and time', ('right', 0, -6), key='zenith')
    m.call(2, 'how', 'How it arrived', ('right', 0, 6), key='zenith')
    m.call(3, 'pages', 'Page count', ('right', 0, 0), key='zenith')
    return m


def m_ref_2():
    m = S2.zform('PACKET CHECKLIST', [
        ('h', 'WHAT IS IN THE PACKET'),
        ('check', 'c_ref', 'Referral form'), ('check', 'c_ord', 'Physician order (signed and dated)'),
        ('check', 'c_face', 'Face sheet (patient details)'), ('check', 'c_ins', 'Insurance card copy (front and back)'),
        ('check', 'c_dis', 'Hospital discharge summary or recent notes'), ('check', 'c_f2f', 'Face-to-face documentation'),
        ('check', 'c_med', 'Medication list'), ('gap',),
        ('text', 'Mark each paper you can hold in your hand. Do not mark a paper you cannot find.')])
    m.call(1, 'c_ord', 'Order: must have', ('right', 0, 0), key='zenith')
    m.call(2, 'c_f2f', 'Face-to-face: must have', ('right', 0, 0), key='zenith')
    m.call(3, 'c_ins', 'Insurance card', ('right', 0, 0), key='zenith')
    return m


def m_ref_3():
    m = S2.zform('REFERRAL REVIEW', [
        ('h', 'IDENTITY AND CONTACT'), ('check', 'r_id', 'Same name and date of birth on every page'),
        ('check', 'r_addr', 'Address and phone are written and readable'),
        ('h', 'CARE REQUEST'), ('check', 'r_ord', 'Order asks for home health (services stated)'),
        ('check', 'r_pay', 'Insurance or payer is stated'), ('check', 'r_lang', 'Preferred language is written (or asked)'),
        ('h', 'DECISION FOR THE DON'), ('check', 'r_ok', 'Complete: send to the DON'),
        ('check', 'r_hold', 'Missing items: ask the referral source')])
    m.call(1, 'r_id', 'Same name on every page', ('right', 0, 0), key='zenith')
    m.call(2, 'r_ord', 'Order in the packet', ('right', 0, 0), key='zenith')
    m.call(3, 'r_ok', 'Send to the DON', ('right', 0, 0), key='zenith')
    return m


def m_ref_4():
    m = S.patients_list(results=True, selected=0, query=('Smith', '03/14/1941'))
    m.call(1, 'pt_search_field', 'Search (P3)', (330, 82), key='pt_search_field')
    m.call(2, 'pt_results.r0', 'One match: open it', (470, 410), key='pt_result_row')
    return m


def m_ref_5():
    m = S3.referral_form()
    m.call(1, 'ref_date', 'Date and time', ('right', 0, 0), key='ref_date')
    m.call(2, 'ref_src', 'Referral source', ('right', 0, 0), key='ref_src')
    m.call(3, 'ref_status', 'Status', ('right', 0, 0), key='ref_status')
    return m


def m_ref_6():
    m = S2.zform('REFERRAL DECISION', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'dob', 'DOB:'),
        ('h', 'DECISION (DON OR ADMINISTRATOR ONLY)'), ('check', 'd_acc', 'Accept for admission'), ('check', 'd_hold', 'Hold: more information needed'),
        ('check', 'd_dec', 'Cannot accept'),
        ('h', 'DECIDED BY'), ('line', 'init', 'DON / Administrator initials:'), ('line', 'dt', 'Date and time of decision:')])
    m.call(1, 'd_acc', 'Accept', ('right', 0, 0), key='zenith')
    m.call(2, 'init', 'DON initials', ('right', 0, 0), key='zenith')
    m.call(3, 'dt', 'Date and time', ('right', 0, 6), key='zenith')
    return m


REFERRAL = Proc(
    id='referral', tab=4, num='P6', title='Process a Referral',
    purpose='A referral is the request that starts care. This procedure shows how to log it the moment it arrives, check that the packet is complete, '
            'record it in Alora, and hand it to the DON for the decision. It protects the 48-hour clock.',
    before=['The referral packet (fax, e-fax, email or hand delivered).', 'The **SOC Packet Intake Log** and **Referral Review** forms (Tab 11).',
            'A pen. The clock or the fax time stamp.'],
    who='Intake staff.', time='15 minutes.',
    steps=[
        Step('ref-1', 'Write down when the packet arrived', m_ref_1,
             do=['Write the **date and the time** the packet arrived.', 'Write **how** it arrived and who **sent** it.', 'Count the pages and write the **number of pages**.'],
             enter='On the paper log only. Nothing in Alora yet.',
             check=['The time is the real arrival time (use the fax or e-fax time stamp if there is one).', 'The page count matches the pages you hold.'],
             expect='One new line on the intake log.',
             see='The log with the date, the time, the sender and the number of pages filled in.',
             donot=['Do not leave the time blank.', 'Do not round the time.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Log every referral within 15 minutes of arrival, including after-hours faxes (first person in the morning).',
             rule='The first nurse visit is due within 48 hours of the referral, so the arrival time must be correct.'),
        Step('ref-2', 'Sort the packet and check what is there', m_ref_2,
             do=['Find the **physician order**. Check the box only if you hold it.', 'Find the **face-to-face** documentation.', 'Find the **insurance card** copy.'],
             check=['You checked only papers you can hold.', 'Every page shows the patient\'s name.'],
             expect='You know what is in the packet and what is missing.',
             see='A checklist with boxes checked for each paper you found.',
             donot=['Do not mark a paper as received because you expect it to come later.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='The order, the face-to-face and the insurance card are the three papers that can stop an admission. Flag them first.',
             stop=['Pages are missing, unreadable, or belong to a different patient.']),
        Step('ref-3', 'Review the referral for the basics', m_ref_3,
             do=['Check that the **same name and date of birth** are on every page.', 'Check that an **order** for home health is in the packet.',
                 'If everything is complete, check **Send to the DON**. If not, check the **missing items** box and list them.'],
             check=['You compared names and birth dates on each page.', 'You did not guess any missing detail.'],
             expect='The packet is either ready for the DON or marked with what is missing.',
             see='A review form with clear marks and, if needed, a list of missing items.',
             donot=['Do not decide whether Zenith can take the patient. The DON decides.', 'Do not call the patient to confirm a start date before the DON accepts.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Office staff check that the papers are there and match. Office staff do not judge the clinical content.',
             stop=['Names or birth dates differ between pages.', 'There is no order.']),
        Step('ref-4', 'Find the patient in Alora', m_ref_4,
             do=['Search for the patient exactly as in **P3**.', 'Exactly one match: open that row (P4). No match: go to **P5B** only after the DON accepts.'],
             check=['Two identifiers match: name and date of birth.'],
             expect='You have either one matching patient or a confirmed \'no match\'.',
             see='One matching row, or a message that no patient was found.',
             alora='Use the patient search to look for an existing record. Box and button names must be verified.',
             zenith='Never create a new patient before the DON has accepted the referral and you have searched three ways (P5B).',
             stop=['Two patients match.', 'The patient is shown as discharged or active and you did not expect it.']),
        Step('ref-5', 'Record the referral in Alora', m_ref_5,
             do=['Enter the **referral date and time** from your log.', 'Enter the **referral source** (the hospital or doctor\'s office).', 'Set the **status** to show the referral is pending.'],
             enter='Date and time from the intake log. The source as written on the packet.',
             check=['The date and time match the log exactly.'],
             expect='The referral is saved and shows as pending in Alora.',
             see='The referral with today\'s date, the source and a pending status.',
             alora='Alora documents intake and referral tracking. The screen, the boxes and the status words in Zenith\'s Alora must be verified.',
             astatus='FEATURE',
             zenith='The referral date and time in Alora must match the paper log.',
             ifwrong='You cannot find where to enter a referral: **stop** and ask. Do not put referral details in another box.'),
        Step('ref-6', 'Give the packet to the DON for the decision', m_ref_6,
             do=['Put the packet, the log and the review form on the DON\'s desk, or hand them over.', 'Wait for the DON or Administrator to **decide** and **initial**.',
                 'Write down the **date and time** of the decision on the log.'],
             check=['The decision is written and initialed. You did not fill it in yourself.'],
             expect='A decision to accept, hold, or decline is written on the form.',
             see='A Referral Decision form with one box checked and the DON\'s initials.',
             donot=['Do not schedule a visit before the decision.', 'Do not tell the referral source \'yes\' before the decision.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Only the DON or the Administrator may accept, hold or decline a referral.'),
    ],
    final=['The arrival date and time are on the intake log.', 'The packet checklist is filled in and any missing papers are listed.',
           'The referral is recorded in Alora with the same date and time.', 'The DON or Administrator made and initialed the decision.',
           'The packet is stored where the Administrator said.'],
    stop=['The packet has no order, or the order is not signed.', 'Names or birth dates differ between pages.', 'It is after hours and the packet says urgent.',
          'Two patients match the name and birth date.', 'The referral source is one you do not know.'],
    donot=['Do not accept or decline a referral yourself.', 'Do not create a patient before the DON accepts.', 'Do not leave the packet on an open desk.'],
)


# ============================================================================= P9 Scan and name documents
def m_nm_1():
    m = S2.zform('SCAN SETTINGS', [
        ('h', 'SET THESE ON THE SCANNER OR SCAN PROGRAM'), ('kv', 'k_type', 'File type', 'PDF'), ('kv', 'k_res', 'Resolution', '300 dpi'),
        ('kv', 'k_col', 'Color', 'Black and white or grayscale'), ('kv', 'k_one', 'One file contains', 'One patient, one document type'),
        ('kv', 'k_side', 'Sides', 'Both sides when there is writing on both'),
        ('gap',), ('text', 'Names of these settings differ by scanner. The values do not.')])
    m.call(1, 'k_type', 'File type', ('right', 0, 0), key='zenith')
    m.call(2, 'k_res', 'Resolution', ('right', 0, 0), key='zenith')
    m.call(3, 'k_one', 'One patient per file', ('right', 0, 0), key='zenith')
    return m


def m_nm_2():
    m = S3.filename_anatomy()
    m.call(1, 'last', 'Last name', (100, 110), key='zenith')
    m.call(2, 'first', 'First name', (270, 110), key='zenith')
    m.call(3, 'type', 'Document type', (400, 160), key='zenith')
    m.call(4, 'date', 'Date on the document', (610, 110), key='zenith')
    return m


def m_nm_3():
    files = [('SMITH_MARY_REFERRAL_20260928.pdf', '09/28/2026 9:12 AM', '212 KB'),
             ('SMITH_MARY_ORDER_20260927.pdf', '09/28/2026 9:14 AM', '188 KB'),
             ('SMITH_MARY_F2F_20260915.pdf', '09/28/2026 9:16 AM', '240 KB')]
    m = S.explorer(files, path='This PC  >  Documents  >  Zenith Scans  >  Ready to upload')
    m.call(1, 'win_folder', 'Correct folder', (560, 36), key='win_folder')
    m.call(2, 'file0', 'Clear, correct name', (430, 320), key='win_file')
    return m


def m_nm_4():
    m = S3.pdf_viewer()
    m.call(1, 'pdf_name', 'Patient name', (600, 196), key='pdf_name')
    m.call(2, 'pdf_pages', 'Page count', (560, 30), key='pdf_pages')
    m.call(3, 'pdf_text', 'Text is readable', (600, 330), key='pdf_text')
    return m


NAMING = Proc(
    id='naming', tab=4, num='P9', title='Scan, Name and Identify Documents',
    purpose='A clear file name and a clean scan let anyone see what a document is before they open it, and stop a document from going into the wrong chart. '
            'This procedure is done before you upload anything.',
    before=['The paper document and the patient\'s name and date of birth.', 'The office scanner.', 'The **Ready to upload** folder on the computer (the Administrator will show you).'],
    who='Intake and records staff.', time='5 minutes for each document.',
    steps=[
        Step('nm-1', 'Scan with the Zenith settings', m_nm_1,
             do=['Set the file type to **PDF**.', 'Set the resolution to **300 dpi**.', 'Scan **one patient and one document type** in each file.'],
             check=['Every page of the document is in the file.', 'Nothing is cut off at the edges.', 'You removed staples and paper clips before scanning.'],
             expect='A scanned file is ready.',
             see='A scan that shows every page, straight and readable.',
             donot=['Do not scan two patients into one file.', 'Do not mix document types in one file.'],
             alora='Not an Alora step. This is a Zenith office step at the scanner.', astatus='ZENITH',
             zenith='Scanner menu words differ by model. The values in the picture do not. Ask the Administrator if your scanner does not offer one of them.'),
        Step('nm-2', 'Name the file the Zenith way', m_nm_2,
             do=['Type the patient\'s **last name** in capital letters.', 'Type the **first name** in capital letters.',
                 'Type the **document type** word (see the list on this page).', 'Type the **date that is on the document** as year, month, day.'],
             enter='LASTNAME_FIRSTNAME_DOCUMENTTYPE_YYYYMMDD.pdf. No spaces. Use the underscore between parts.',
             check=['The name and the date come from the document, not from memory.'],
             expect='A file called, for example, SMITH_MARY_REFERRAL_20260928.pdf.',
             see='A file name with four parts joined by underscores, ending in .pdf.',
             donot=['Do not use spaces, nicknames or words like \'scan1\'.'],
             alora='Not an Alora step. This is a Zenith naming standard.', astatus='ZENITH',
             zenith='Document type words: **REFERRAL, ORDER, F2F, FACESHEET, INSCARD, DISCHARGE, MEDLIST**. Ask the Administrator before you use any other word.',
             key_note='Use the date printed or written on the document (for example the order date), not today\'s date.'),
        Step('nm-3', 'Save it in the Ready to upload folder', m_nm_3,
             do=['Check that the folder path ends in **Ready to upload**.', 'Check that your file is listed there with its clear name.'],
             check=['The file is in the right folder.', 'There is no older copy with a similar name.'],
             expect='The file is waiting in the Ready to upload folder.',
             see='A folder list that shows your file with a name like SMITH_MARY_REFERRAL_20260928.pdf.',
             alora='Not an Alora step. This is a Windows folder.', astatus='ZENITH',
             zenith='Every scanned patient file lives in this one folder until it is uploaded and verified, then it is removed (P28).'),
        Step('nm-4', 'Open the file and check it', m_nm_4,
             do=['Find the **patient name** on the page and compare it with the file name.', 'Check the **page count**: it matches the paper.', 'Check that the text is **readable** when the page is full size.'],
             check=['Name on the page = name in the file name.', 'All pages are present.', 'You can read every word.'],
             expect='You know the file is correct and readable before you upload it.',
             see='A viewer with the page in front of you and the page count at the top.',
             alora='Not an Alora step. Any PDF viewer on the office computer will do.', astatus='ZENITH',
             zenith='A file you cannot read is not uploaded. Scan it again.',
             stop=['The name on the page is not the name in the file name.', 'A page is missing.']),
    ],
    final=['The scan has every page and is readable.', 'The file name has four parts: last name, first name, document type, date.',
           'The file is in the Ready to upload folder.', 'I opened the file and checked the name and the pages.'],
    stop=['You are not sure which patient a page belongs to.', 'A page has a different patient\'s name.', 'You are not sure which document type word to use.', 'The scanner or folder is missing.'],
    donot=['Do not name a file from memory.', 'Do not put two patients in one file.', 'Do not save patient files on the desktop or in Downloads.'],
)


# ============================================================================= P8 Upload scanned documents
def m_up_1():
    m = S.patients_list(results=True, selected=0, query=('Smith', '03/14/1941'))
    m.call(1, 'pt_search_field', 'Search (P3)', (330, 82), key='pt_search_field')
    m.call(2, 'pt_results.r0', 'Correct patient', (470, 410), key='pt_result_row')
    return m


def m_up_2():
    m = S.patient_record('sum')
    m.call(1, 'pt_name', 'Name matches the file', (200, 250), key='pt_banner')
    m.call(2, 'pt_ids', 'Birth date matches', (470, 250), key='pt_banner')
    return m


def m_up_3():
    m = S.patient_record('sum')
    m.call(1, 'tab.docs', 'Documents section', (300, 250), key='tab_docs')
    return m


def m_up_4():
    m = S.tab_docs()
    m.call(1, 'btn_upload', 'Add / upload button', ('left', 0, 0), key='btn_upload')
    m.call(2, 'docs_list.r0', 'Is it already here?', (300, 360), key='docs_list')
    return m


def m_up_5():
    m = S.win_open(filename='SMITH_MARY_REFERRAL_20260928.pdf', selected='SMITH_MARY_REFERRAL_20260928.pdf')
    m.call(1, 'win_sel', 'Click your file', (560, 250), key='win_file')
    m.call(2, 'win_filename', 'Name matches', (450, 482 - 30), key='win_filename')
    m.call(3, 'win_open', 'Open button', (590, 378), key='win_open')
    return m


def m_up_6():
    m = S.type_list_open(selected='Referral')
    m.call(1, 'dlg_type', 'Document type list', (20, 250), key='dlg_type')
    m.call(2, 'opt_sel', 'Type that matches', (20, 330), key='dlg_type')
    return m


def m_up_7():
    m = S.upload_dialog(doctype='Referral', filename='SMITH_MARY_REFERRAL_20260928.pdf')
    m.call(1, 'dlg_file', 'File is the right one', ('left', 0, 0), key='dlg_file')
    m.call(2, 'dlg_type', 'Type is right', ('left', 0, 0), key='dlg_type')
    m.call(3, 'dlg_date', 'Document date', ('left', 0, 0), key='dlg_date')
    m.call(4, 'dlg_save', 'Save', ('right', 0, 0), key='dlg_save')
    return m


def m_up_8():
    rows = [['SMITH_MARY_REFERRAL_20260928.pdf', 'Referral', '09/28/2026', '09/28/2026']]
    m = S.tab_docs(rows=rows, sel=0)
    m.call(1, 'docs_list.r0', 'New document is here', (300, 360), key='docs_list')
    m.call(2, 'docs_list.r0c1', 'Type is correct', (560, 420), key='doc_row')
    return m


UPLOAD = Proc(
    id='upload', tab=4, num='P8', title='Upload Scanned Documents',
    purpose='To put a scanned document into the **correct patient\'s** chart in Alora, under the **correct document type**, and to prove it arrived. '
            'Alora documents scanned-document storage (paperless records) for patients. Every button and name in this procedure must be verified in live Alora.',
    before=['A scanned, named and checked file in the Ready to upload folder (P9).', 'The patient\'s name and date of birth.',
            'You are signed in with your own login (P1).'],
    who='Trained office staff.', time='5 minutes for each document.',
    steps=[
        Step('up-1', 'Find the patient', m_up_1,
             do=['Search by last name and date of birth, as in **P3**.', 'Choose the row where **name and date of birth** match the file.'],
             check=['Two identifiers match the file name and the document.'],
             expect='You know the right patient.',
             see='One matching row in the list.',
             alora='Use the patient search.', astatus='FEATURE',
             zenith='Follow P3 exactly. Do not skip the two-identifier check.',
             stop=['Two rows match.', 'No row matches.']),
        Step('up-2', 'Open the record and confirm the name', m_up_2,
             do=['Read the **name** in the banner. It must be the name in your file name.', 'Read the **date of birth**. It must match the document.'],
             check=['The banner name equals the file name.', 'You are in the right chart before you upload.'],
             expect='The correct patient record is open.',
             see='The patient banner with the same name and birth date as the document.',
             donot=['Do not go on if the name is even slightly different.'],
             alora='Open the patient record.', astatus='FEATURE',
             zenith='Verify the document belongs to this patient **before** you upload it.',
             stop=['Name or birth date does not match: **stop**, close the record and ask the Administrator.']),
        Step('up-3', 'Open the documents section', m_up_3,
             do=['Click the **documents section** under the patient banner.'],
             check=['The section you opened shows documents, not orders or visits.'],
             expect='The patient\'s document list opens.',
             see='The patient name at the top. A list of documents underneath, or an empty list.',
             alora='Alora documents paperless records (scanned document storage) for patients. The section name and its place must be verified.',
             astatus='FEATURE',
             zenith='If you cannot find the documents section, do not use another section. Ask the Administrator.'),
        Step('up-4', 'Start the upload', m_up_4,
             do=['Click the **add or upload button** in the document list.', 'First look at the list: is this document **already there**? Do not add a second copy.'],
             check=['The list does not already hold the same document.'],
             expect='A window or a form opens to add a document.',
             see='A window titled like \'Add document\', with a place to choose a file and a place to choose a type.',
             donot=['Do not upload a document that is already in the list.'],
             alora='Start an upload from the patient\'s documents. The button name must be verified.',
             zenith='Duplicates are not allowed. If it is already there, skip to step 8 to check it and stop.',
             stop=['You cannot find an add or upload button.']),
        Step('up-5', 'Choose the file on the computer', m_up_5,
             do=['Click your **file** in the list. Look for the name you gave it in P9.', 'Check that the **file name** box shows the right name.', 'Click **Open**.'],
             check=['The file name is the one for this patient.', 'You are in the Ready to upload folder.'],
             expect='The window closes and the file name appears in the upload window.',
             see='Back in Alora, the upload window now shows the file name.',
             donot=['Do not pick a file from Downloads or the desktop.'],
             alora='Not an Alora screen. This is the standard Windows \'Open\' window that Alora opens when you choose a file.', astatus='ZENITH',
             zenith='Choose only from the Ready to upload folder.'),
        Step('up-6', 'Choose the document type', m_up_6,
             do=['Click the **document type list**.', 'Click the type that **matches the document**: Referral, Physician order or Face-to-face.'],
             enter='The type from your file name. If the exact type is not in the list, do not guess.',
             check=['The type matches the document you are holding.'],
             expect='The type you chose shows in the box.',
             see='The type box shows one type, for example \'Referral\'.',
             donot=['Do not choose \'Other\' unless the Administrator told you to.'],
             alora='Choose the document type or category. The real list of types in Zenith\'s Alora must be verified and copied on the Live Alora Verification Worksheet.',
             zenith='Use the document type that matches your file name word. If Alora has no matching type, **stop** and ask the Administrator to tell you which to use.',
             stop=['No type in the list matches the document.']),
        Step('up-7', 'Check everything, then Save', m_up_7,
             do=['Check the **file name** is the right one.', 'Check the **document type** is right.', 'Type the **document date** from the paper if the window asks for it.', 'Click **Save** one time and wait.'],
             enter='The date that is on the document, as month/day/year.',
             check=['The patient is correct.', 'The file, the type and the date are correct.'],
             expect='The window closes and you are back in the document list.',
             see='The document list, now with one more row.',
             donot=['Do not click Save more than once.', 'Do not save if you are unsure about the patient.'],
             alora='Save the upload. The button name and what happens next must be verified.',
             zenith='One last check before you save: right patient, right file, right type, right date.',
             ifwrong='An error message appears: do not click Save again. **Stop** and ask the Administrator.'),
        Step('up-8', 'Verify that the document is in the list', m_up_8,
             do=['Find your document in the list. It should be the **newest row**.', 'Check that its **type** is the one you chose.'],
             check=['Exactly one new row.', 'The name, the type and the date look right.'],
             expect='The document is in the patient\'s list, once, with the right type.',
             see='A row with your file name, the document type and the date.',
             alora='The document list shows what was uploaded.',
             astatus='FEATURE',
             zenith='Now do **P10** to open the document and prove it is correct. Only then may the scan file be removed from the folder.',
             stop=['There is no new row, or there are two new rows.', 'The row shows a different type or patient.']),
    ],
    final=['The correct patient was open (name and date of birth matched).', 'The right file was chosen from the Ready to upload folder.',
           'The right document type was chosen.', 'The document appears once in the patient\'s document list.', 'I will now verify the document (P10).'],
    stop=['You are not sure the patient is correct.', 'No document type matches.', 'An error message appears.', 'The document shows twice.',
          'The document went into another patient\'s chart: tell the Administrator **at once**. Do not try to fix it.'],
    donot=['Do not upload into the wrong patient\'s chart.', 'Do not delete a document.', 'Do not choose \'Other\' unless told to.', 'Do not click Save twice.'],
)


# ============================================================================= P10 Verify uploaded documents
def m_ver_1():
    rows = [['SMITH_MARY_REFERRAL_20260928.pdf', 'Referral', '09/28/2026', '09/28/2026'],
            ['SMITH_MARY_ORDER_20260927.pdf', 'Physician order', '09/27/2026', '09/28/2026'],
            ['SMITH_MARY_F2F_20260915.pdf', 'Face-to-face', '09/15/2026', '09/28/2026']]
    m = S.tab_docs(rows=rows)
    m.call(1, 'docs_list', 'The document list', (200, 440), key='docs_list')
    m.call(2, 'docs_list.c1', 'Type column', (560, 440), key='docs_list')
    return m


def m_ver_2():
    m = S3.alora_doc_open()
    m.call(1, 'v_name', 'Name on the page', ('right', 0, 0), key='doc_view')
    m.call(2, 'v_pages', 'Page count', ('right', 0, 0), key='doc_view')
    return m


def m_ver_3():
    m = S2.zform('DOCUMENT VERIFICATION', [
        ('h', 'PATIENT AND DOCUMENT'), ('two', 'pt', 'Patient:', 'doc', 'Document:'),
        ('h', 'CHECK EACH ONE'), ('check', 'v_name', 'Name on the page = name in the chart'), ('check', 'v_dob', 'Date of birth matches'),
        ('check', 'v_type', 'Document type and date are correct'),
        ('check', 'v_read', 'All pages open and are readable'), ('check', 'v_dup', 'No duplicate in the list'),
        ('h', 'VERIFIED BY'), ('two', 'emp', 'Employee:', 'dt', 'Date:')])
    m.call(1, 'v_name', 'Right patient', ('right', 0, 0), key='zenith')
    m.call(2, 'v_read', 'Readable', ('right', 0, -8), key='zenith')
    m.call(3, 'v_dup', 'Only once', ('right', 0, 10), key='zenith')
    return m


def m_ver_4():
    rows = [['SMITH_MARY_REFERRAL_20260928.pdf', 'Referral', '09/28/2026', '09/28/2026'],
            ['SMITH_MARY_REFERRAL_20260928.pdf', 'Referral', '09/28/2026', '09/28/2026'],
            ['SMITH_MARY_ORDER_20260927.pdf', 'Physician order', '09/27/2026', '09/28/2026']]
    m = S.tab_docs(rows=rows)
    m.call(1, 'docs_list.r0', 'Same document', (400, 440), key='docs_list')
    m.call(2, 'docs_list.r1', 'listed twice', (640, 440), key='docs_list')
    return m


def m_ver_5():
    m = S2.zform('DOCUMENT PROBLEM REPORT', [
        ('h', 'PATIENT AND DOCUMENT'), ('two', 'pt', 'Patient:', 'doc', 'Document:'),
        ('h', 'WHAT IS WRONG'), ('check', 'p_wrong', 'Wrong patient'), ('check', 'p_dup', 'Duplicate'), ('check', 'p_read', 'Cannot read it'),
        ('check', 'p_type', 'Wrong document type'), ('line', 'p_note', 'Notes:'),
        ('h', 'ADMINISTRATOR / DON DECISION'), ('line', 'p_dec', 'Action to take:'), ('two', 'p_init', 'Initials:', 'p_dt', 'Date:')])
    m.call(1, 'p_wrong', 'Check what is wrong', ('right', 0, 0), key='zenith')
    m.call(2, 'p_dec', 'Administrator decides', ('right', 0, 0), key='zenith')
    return m


VERIFY = Proc(
    id='verify', tab=4, num='P10', title='Verify Uploaded Documents',
    purpose='An upload is not finished until you have opened the document in Alora and proved that it is the right patient, the right document, readable, and only there once.',
    before=['You uploaded one or more documents (P8).', 'The paper originals or the scan files.', 'The **Document Verification** form (Tab 11).'],
    who='The employee who uploaded, then a second person for orders and F2F.', time='3 minutes for each document.',
    steps=[
        Step('ver-1', 'Open the document list', m_ver_1,
             do=['Look at the **list** of documents for this patient.', 'Find the **type** column. Each document you uploaded is there once.'],
             check=['You can see every document you uploaded today.'],
             expect='You see your documents in the list.',
             see='A list with your new rows, each with a name, a type and a date.',
             alora='The document list shows what is stored in the patient\'s chart.', astatus='FEATURE',
             zenith='Verify in the same session that you uploaded. Do not leave it for later.'),
        Step('ver-2', 'Open each document', m_ver_2,
             do=['Click the **document** to open it. Find the **patient name** on the page.', 'Find the **page count**. Look at every page.'],
             check=['The document opens. It is not blank or cut off.', 'The name on the page is the patient in the banner.'],
             expect='Each document opens and shows the right patient.',
             see='The document in a viewer, with the patient name and the pages visible.',
             alora='Open a document from the list. The viewer and its buttons must be verified.',
             zenith='Open every document you uploaded. A document you did not open is not verified.',
             stop=['A document will not open.', 'The page shows a different patient.']),
        Step('ver-3', 'Check the six things', m_ver_3,
             do=['Check **name** and date of birth against the chart.', 'Check that **all pages** open and are readable.', 'Check that the document is in the list **only once**.'],
             check=['Name and date of birth.', 'Type and document date.', 'All pages readable.', 'No duplicate.'],
             expect='You checked every box on the Document Verification form.',
             see='A form with six check marks and your initials.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Write your initials and the date. A second person verifies orders and face-to-face documents.'),
        Step('ver-4', 'Look for duplicates', m_ver_4,
             do=['Look for **two rows** with the same name, type and date.', 'If you find a duplicate, do not delete it. Use the next page.'],
             check=['Each document is in the list only once.'],
             expect='No duplicates, or you know which rows are duplicates.',
             see='A list where each document appears once.',
             donot=['Do not delete a duplicate yourself.'],
             alora='Deleting or voiding is not an office employee action without approval.', astatus='ZENITH',
             zenith='Report a duplicate on the Document Problem Report. Only the Administrator or DON removes a document.',
             stop=['Two rows look the same.']),
        Step('ver-5', 'If anything is wrong: report it, do not fix it', m_ver_5,
             do=['Check what is **wrong** on the form.', 'Give the form to the Administrator or DON, who **decides** what to do.'],
             enter='Only on the paper form: the patient, the document and what is wrong.',
             check=['You wrote the patient and the document exactly.'],
             expect='The Administrator or DON has the form and decides.',
             see='A Document Problem Report with one or more boxes checked.',
             donot=['Do not delete, rename or re-upload before the Administrator decides.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='A document in the wrong chart is a privacy problem. Tell the Administrator **at once**.',
             stop=['A document is in the wrong patient\'s chart: tell the Administrator **now**.']),
    ],
    final=['I opened every document I uploaded.', 'The name and date of birth on the pages match the chart.', 'The document type and date are right.',
           'All pages open and are readable.', 'Nothing is in the chart twice.', 'I initialed the Document Verification form.'],
    stop=['A document is in the wrong patient\'s chart.', 'A document will not open or cannot be read.', 'You find a duplicate.', 'The type in the list does not match the paper.'],
    donot=['Do not delete a clinical document unless the Administrator or DON tells you.', 'Do not assume it is fine because the upload finished.', 'Do not remove the scan file until the document is verified.'],
)


# ============================================================================= P11 Review physician orders
def m_ord_1():
    rows = [['SMITH_MARY_REFERRAL_20260928.pdf', 'Referral', '09/28/2026', '09/28/2026'],
            ['SMITH_MARY_ORDER_20260927.pdf', 'Physician order', '09/27/2026', '09/28/2026']]
    m = S.tab_docs(rows=rows, sel=1)
    m.call(1, 'docs_list.r1', 'The order row', (300, 370), key='docs_list')
    return m


def m_ord_2():
    m = S3.order_sample()
    m.call(1, 'o_id', 'Right patient', ('right', 0, -6), key='zenith')
    m.call(2, 'o_text', 'What is ordered', ('right', 0, 6), key='zenith')
    m.call(3, 'o_date', 'Date of order', ('right', 40, -14), key='zenith')
    return m


def m_ord_3():
    m = S3.order_sample()
    m.call(1, 'o_sig', 'Physician signature', ('right', 0, 0), key='zenith')
    m.call(2, 'o_signdate', 'Date signed', ('right', 0, 0), key='zenith')
    m.call(3, 'o_npi', 'NPI number', ('right', 0, 0), key='zenith')
    return m


def m_ord_4():
    m = S3.pending_list('orders')
    m.call(1, 'pend', 'Pending orders list', (460, 380), key='cl_pending')
    m.call(2, 'pend.r0', 'Is the order listed?', (560, 330), key='cl_order')
    return m


def m_ord_5():
    m = S2.zform('ORDER REVIEW SHEET', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'dob', 'DOB:'),
        ('h', 'OFFICE REVIEW (PRESENT AND MATCHING)'), ('check', 'o_id', 'Name and date of birth match the chart'),
        ('check', 'o_txt', 'Order states home health and services'), ('check', 'o_sig', 'Physician signed and dated'),
        ('check', 'o_npi', 'Physician name and NPI are readable'), ('check', 'o_up', 'Uploaded and verified (P10)'),
        ('h', 'ROUTE TO'), ('check', 'o_don', 'DON (every new order)')])
    m.call(1, 'o_sig', 'Signed and dated', ('right', 0, 0), key='zenith')
    m.call(2, 'o_up', 'Uploaded and verified', ('right', 0, 6), key='zenith')
    m.call(3, 'o_don', 'Give to the DON', ('right', 0, 0), key='zenith')
    return m


ORDERS = Proc(
    id='orders', tab=4, num='P11', title='Review Physician Orders',
    purpose='Care must follow a physician\'s order. Office staff check that the order is in the chart, is for the right patient, is signed and dated, and has been given to the DON. '
            'Office staff never decide what the order means for care.',
    before=['The order is uploaded and verified (P8, P10).', 'The **Order Review Sheet** (Tab 11).', 'The paper order, if you have it.'],
    who='Intake staff and a second person for verification.', time='10 minutes.',
    steps=[
        Step('ord-1', 'Find the order in the patient\'s documents', m_ord_1,
             do=['In the document list, click the **order** row to open it.'],
             check=['The row says Physician order (or the type Zenith uses).', 'The patient is the one you opened.'],
             expect='The order is open in front of you.',
             see='The order document on your screen.',
             alora='Open a document from the patient\'s document list.', astatus='FEATURE',
             zenith='Open the order **from the chart**, not from the scan folder.'),
        Step('ord-2', 'Check who it is for and what it says', m_ord_2,
             do=['Check the **patient name and date of birth** against the chart.', 'Read **what is ordered**. It must ask for home health care.',
                 'Check the **date of the order**.'],
             check=['Name and date of birth match.', 'The order says what care is requested.', 'The date is readable.'],
             expect='You know the order is for the right patient and what it asks for.',
             see='An order with the patient name, the ordered care and a date.',
             donot=['Do not change the order or add anything.', 'Do not decide if the ordered care is right. That is for the DON.'],
             alora='Not an Alora step. You are reading a document.', astatus='ZENITH',
             zenith='Office staff check that the order exists and matches. The DON decides what it means.',
             stop=['The name or date of birth is different.', 'You cannot tell what is ordered.']),
        Step('ord-3', 'Check the signature, the date and the NPI', m_ord_3,
             do=['Find the **physician\'s signature**. It must be there.', 'Find the **date signed**.', 'Find the **NPI** number or the printed physician name.'],
             check=['Signed.', 'Signature date is written.', 'Physician name is readable, and the NPI when it is shown.'],
             expect='The order is signed and dated, or you know what is missing.',
             see='A signature on the signature line, with a date.',
             donot=['Do not sign, date or initial for the physician.', 'Do not accept a stamp or a typed name unless the Administrator says it is allowed.'],
             alora='Not an Alora step. You are reading a document.', astatus='ZENITH',
             zenith='An unsigned order goes on the tracking list for follow-up. Tell the DON the same day.',
             stop=['There is no signature, no date, or no physician name.']),
        Step('ord-4', 'Check the pending orders list in Alora', m_ord_4,
             do=['Open the **pending orders** list (from the dashboard or the clinical area).', 'Find the **patient\'s order**. See if it is listed, and its status.'],
             check=['You see the same patient and the same order date.', 'The status fits what you saw on the paper.'],
             expect='You know whether Alora lists this order as waiting for a signature or as signed.',
             see='A list of pending orders with a status for each.',
             alora='Alora documents that it can show pending 485 forms, orders and OASIS in one place. The list name and where to find it must be verified.',
             astatus='FEATURE',
             zenith='Do not change a status. Only the DON or a clinician changes order status.',
             stop=['The status in Alora does not match the paper.']),
        Step('ord-5', 'Write your review and give it to the DON', m_ord_5,
             do=['Check **signed and dated** only if it is.', 'Check **uploaded and verified** only after P10.', 'Give the sheet and the order to the **DON**.'],
             enter='On the Order Review Sheet: what is present and what is missing.',
             check=['You did not check a box for something that is missing.'],
             expect='The DON has the order and your sheet.',
             see='A filled-in Order Review Sheet with your initials.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Every new order goes to the DON the same day, signed or not.'),
    ],
    final=['The order is in the chart and opens.', 'Name and date of birth on the order match the chart.', 'The order is signed and dated, or the gap is written on the sheet.',
           'I checked the pending orders list in Alora.', 'The DON has the order and my sheet.'],
    stop=['The order is not signed or not dated.', 'The patient name or date of birth differs.', 'You are not sure what the order asks for.',
          'The order asks for something that seems different from the referral.', 'A verbal order was given and there is no written record.'],
    donot=['Do not change, add to or sign an order.', 'Do not guess what an order means.', 'Do not schedule visits from an order the DON has not seen.'],
)


# ============================================================================= P12 Review Face-to-Face documentation
def m_f2f_1():
    rows = [['SMITH_MARY_ORDER_20260927.pdf', 'Physician order', '09/27/2026', '09/28/2026'],
            ['SMITH_MARY_F2F_20260915.pdf', 'Face-to-face', '09/15/2026', '09/28/2026']]
    m = S.tab_docs(rows=rows, sel=1)
    m.call(1, 'docs_list.r1', 'The face-to-face row', (300, 370), key='docs_list')
    return m


def m_f2f_2():
    m = S3.f2f_sample()
    m.call(1, 'f_date', 'Date of the visit', ('right', 30, -14), key='zenith')
    m.call(2, 'f_who', 'Who saw the patient', ('right', 0, 12), key='zenith')
    return m


def m_f2f_3():
    m = S3.f2f_timeline()
    m.call(1, 'enc', 'Visit date: 09/15/2026', (330, 330), key='zenith')
    m.call(2, 'soc', 'Start of care date', (640, 112), key='zenith')
    return m


def m_f2f_4():
    m = S3.f2f_sample()
    m.call(1, 'f_find', 'Clinical findings written', ('right', 0, 0), key='zenith')
    m.call(2, 'f_rel', 'Related to home health need', ('right', 0, 0), key='zenith')
    m.call(3, 'f_sig', 'Signed and dated', ('right', 0, 0), key='zenith')
    return m


def m_f2f_5():
    m = S2.zform('FACE-TO-FACE REVIEW SHEET', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'soc', 'Planned SOC date:'),
        ('h', 'OFFICE REVIEW'), ('line', 'f_enc', 'Date of the face-to-face visit:'), ('check', 'f_win', 'Date is 90 days before to 30 days after SOC'),
        ('check', 'f_who', 'Seen by a physician or allowed practitioner'), ('check', 'f_txt', 'Findings and reason are written'),
        ('check', 'f_sig', 'Signed and dated'), ('check', 'f_up', 'Uploaded and verified (P10)'),
        ('check', 'f_don', 'Given to the DON')])
    m.call(1, 'f_win', 'Date in the window', ('right', 0, 0), key='zenith')
    m.call(2, 'f_up', 'Uploaded and verified', ('right', 0, 0), key='zenith')
    m.call(3, 'f_don', 'Give to the DON', ('right', 0, 0), key='zenith')
    return m


F2F = Proc(
    id='f2f', tab=4, num='P12', title='Review Face-to-Face Documentation',
    purpose='For Medicare home health, a physician or allowed practitioner must have seen the patient face to face, close to the start of care. '
            'Office staff check that the paper exists, is in the right window, and is uploaded. The DON decides if it is enough.',
    before=['The face-to-face document is uploaded and verified (P8, P10).', 'The **planned start of care (SOC) date**.', 'The **Face-to-Face Review Sheet** (Tab 11).'],
    who='Intake staff, then the DON.', time='10 minutes.',
    steps=[
        Step('f2f-1', 'Find the face-to-face document', m_f2f_1,
             do=['In the document list, click the **face-to-face** row to open it.'],
             check=['The type is face-to-face (or the type Zenith uses).', 'The patient is the one you opened.'],
             expect='The face-to-face document is open.',
             see='The document on your screen.',
             alora='Open a document from the patient\'s document list.', astatus='FEATURE',
             zenith='Open it from the chart, not from the scan folder.',
             stop=['There is no face-to-face document: **stop**. Tell the DON the same day.']),
        Step('f2f-2', 'Find the visit date and who saw the patient', m_f2f_2,
             do=['Find the **date of the visit** (the encounter).', 'Find **who saw** the patient and what kind of practitioner they are.'],
             check=['The date is written and readable.', 'The person is a physician or another practitioner allowed to do this. Ask the DON if unsure.'],
             expect='You have the visit date and the name of who saw the patient.',
             see='A document with an encounter date and a practitioner name and type.',
             donot=['Do not guess a date that is not written.'],
             alora='Not an Alora step. You are reading a document.', astatus='ZENITH',
             zenith='Write the date on the Face-to-Face Review Sheet exactly as it appears on the document.',
             stop=['No date, or the date is unreadable.']),
        Step('f2f-3', 'Check the date window', m_f2f_3,
             do=['Find the **start of care date**.', 'Check that the visit date is between **90 days before** and **30 days after** the start of care.'],
             enter='On the review sheet: the visit date and the planned start of care date.',
             check=['Count the days carefully. Use a calendar.', 'The visit date is not earlier than 90 days before the start of care.', 'It is not later than 30 days after.'],
             expect='You know if the visit date is inside the window.',
             see='A timeline with the start of care and the visit date marked.',
             alora='Not an Alora step. This is a check on a document.', astatus='ZENITH',
             rule='The face-to-face encounter must be no more than 90 days before, or up to 30 days after, the start of care, and must be related to the main reason the patient needs home health.',
             zenith='If the date is outside the window, do not decide what to do. Tell the DON the same day.',
             stop=['The date is outside the window.']),
        Step('f2f-4', 'Check that the reason and the signature are there', m_f2f_4,
             do=['Check that **clinical findings** are written.', 'Check that the visit is **related to the reason** for home health.', 'Check **signed and dated**.'],
             check=['Findings are written in words, not blank.', 'There is a signature and a date.'],
             expect='The face-to-face paper has findings, a reason and a signature, or you know what is missing.',
             see='A document with written findings, a statement about the reason, and a signature.',
             donot=['Do not judge if the findings are good enough. The DON does that.', 'Do not add or change anything on the document.'],
             alora='Not an Alora step. You are reading a document.', astatus='ZENITH',
             zenith='Office staff check that the parts are present. The DON decides if the content is enough.',
             stop=['Findings are blank.', 'There is no signature.']),
        Step('f2f-5', 'Write your review and give it to the DON', m_f2f_5,
             do=['Check **date in the window** only if it is.', 'Check **uploaded and verified** only after P10.', 'Give the sheet and the document to the **DON**.'],
             check=['Every box you checked is true.'],
             expect='The DON has the face-to-face document and your sheet.',
             see='A filled-in Face-to-Face Review Sheet with your initials.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Tell the DON the same day about any problem. Do not wait for the start of care.'),
    ],
    final=['The face-to-face document is in the chart and opens.', 'I wrote the visit date and who saw the patient on the sheet.',
           'The visit date is inside the 90-days-before to 30-days-after window, or I told the DON it is not.',
           'Findings, reason and signature are present, or the gap is written.', 'The DON has my sheet.'],
    stop=['There is no face-to-face document.', 'The date is outside the window.', 'The document has no signature or no findings.', 'You cannot tell who saw the patient.',
          'The document is for a different patient.'],
    donot=['Do not add, change or sign a face-to-face document.', 'Do not decide that a missing or late face-to-face is acceptable.', 'Do not skip this step because the order is signed.'],
)

PAGES = [Divider(4, 'Take in a referral, scan and name the documents, upload them into the right chart, and review the physician order and the face-to-face documentation.',
                 [('referral', 'P6  Process a Referral'), ('naming', 'P9  Scan, Name and Identify Documents'), ('upload', 'P8  Upload Scanned Documents'),
                  ('verify', 'P10  Verify Uploaded Documents'), ('orders', 'P11  Review Physician Orders'), ('f2f', 'P12  Review Face-to-Face Documentation')]),
         REFERRAL, NAMING, UPLOAD, VERIFY, ORDERS, F2F]

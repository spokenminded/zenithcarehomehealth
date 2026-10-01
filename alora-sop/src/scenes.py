"""Reusable training screens. Each function draws a screen and registers named targets.
Steps add callouts on top (see content/*.py). Nothing here claims to be a real Alora screenshot."""
from mock import Mock, tw, W, H, RIBBON_Y, TXT, MUTED, LINE, LINE2, WHITE, NAVY, HDR, NAVBG, SEL, BTN, BTNP, RED, GOLD

ITAL = dict(italic=True)


# =========================================================================== browser and sign in
def desktop_browser():
    """Windows desktop with the taskbar and a browser window that has no page open yet."""
    m = Mock('Training mockup: Windows desktop with a web browser window and taskbar')
    m.rect(0, 0, W, RIBBON_Y, fill='#D9E2F0', stroke='#8A96A8', sw=2)
    # browser window
    m.rect(120, 40, 680, 380, fill=WHITE, stroke='#8A96A8', sw=2, rx=6)
    m.rect(121, 41, 678, 34, fill='#DDE3EB', stroke='none')
    m.rect(190, 46, 520, 24, fill=WHITE, stroke=LINE2, rx=12, name='addr')
    m.text(206, 63, 'Type the address here', 14, False, MUTED, italic=True)
    m.text(460, 240, 'Blank page', 22, False, '#9AA5B5', 'middle', italic=True)
    # taskbar
    m.rect(0, 452, W, 60, fill='#1F2A3D', stroke='none')
    m.rect(14, 464, 36, 36, fill='#33507F', stroke='none', rx=6)
    m.text(32, 488, 'W', 18, True, WHITE, 'middle')
    m.rect(70, 462, 40, 40, fill='#2C3A52', stroke='#5C6B85', rx=6, name='browser_icon')
    m.ops.append('<circle cx="90" cy="482" r="12" fill="none" stroke="#9DB8E6" stroke-width="3"/><circle cx="90" cy="482" r="4" fill="#9DB8E6"/>')
    m.reg('taskbar', 0, 452, W, 60)
    m.text(W - 20, 488, '9:00 AM', 14, False, '#C9D3E6', 'end')
    m.rib_extra = 'Windows screens look a little different on each computer.'
    return m


def login(filled=False, url="[ Zenith's Alora web address ]"):
    m = Mock('Training mockup: a generic sign in page with username, password and login button')
    m.chrome(url)
    m.rect(1, 35, W - 2, RIBBON_Y - 36, fill='#F4F6FA', stroke='none')
    m.rect(270, 92, 360, 360, fill=WHITE, stroke=LINE2, rx=10, sw=1.5, name='card')
    m.text(450, 142, '[ logo ]', 18, False, '#9AA5B5', 'middle', italic=True)
    m.text(450, 184, '[ sign in page ]', 15, False, MUTED, 'middle', italic=True)
    m.field('login_user', 300, 226, 300, 'Username', 'your.username' if not filled else 'jsmith', placeholder=not filled)
    m.field('login_pass', 300, 308, 300, 'Password', '' if not filled else '••••••••••')
    m.btn('login_btn', 300, 372, 300, 42, 'Login', primary=True, size=17)
    return m


# =========================================================================== application shell
def dashboard(active='dash', widgets=True, noa=True):
    m = Mock('Training mockup: a generic office dashboard with menu, search box and widgets')
    m.chrome()
    cx, cy = m.shell(active)
    m.text(176, 112, 'Dashboard', 24, True, NAVY)
    m.skeleton(176, 126, 0, 0)
    # pending items widget (feature documented by Alora)
    m.rect(176, 132, 360, 170, fill=WHITE, stroke=LINE2, rx=8, sw=1.5, name='w_pending')
    m.text(190, 158, 'Pending items', 16, True, TXT)
    rows = [('485 plans of care', ('chip', '3', 'warn')), ('Orders', ('chip', '5', 'warn')), ('OASIS', ('chip', '2', 'warn'))]
    for i, (lab, chip) in enumerate(rows):
        y = 178 + i * 40
        m.line(190, y, 522, y, LINE, 1)
        m.text(190, y + 26, lab, 15, False, TXT)
        m.chip(480, y + 8, chip[1], chip[2], 14)
    m.reg('pend.485', 184, 174, 346, 38)
    m.reg('pend.orders', 184, 214, 346, 38)
    m.reg('pend.oasis', 184, 254, 346, 38)
    # NOA widget (feature documented by Alora)
    if noa:
        m.rect(556, 132, 320, 170, fill=WHITE, stroke=LINE2, rx=8, sw=1.5, name='w_noa')
        m.text(570, 158, 'NOA (timely filing)', 16, True, TXT)
        m.text(570, 214, '2', 44, True, '#7A4A00')
        m.text(620, 214, 'to send', 16, False, MUTED)
        m.text(570, 252, 'Due within 5 calendar days', 14, False, MUTED, italic=True, name='noa_due')
        m.text(570, 276, 'of the start of care.', 14, False, MUTED, italic=True)
    # today's visits area (not documented: descriptive)
    m.rect(176, 322, 700, 170, fill=WHITE, stroke=LINE2, rx=8, sw=1.5, name='w_visits')
    m.text(190, 348, "Today's visits", 16, True, TXT)
    m.skeleton(190, 366, 660, lines=4, gap=26, lh=8)
    if not noa:
        m.rib_extra = 'Only the pending items box is drawn on this picture.'
    return m


def patients_list(results=True, selected=None, query=('Smith', '')):
    m = Mock('Training mockup: a generic patient search screen with a results list')
    m.chrome()
    m.shell('patients')
    m.text(176, 112, 'Patients', 24, True, NAVY)
    m.field('pt_search_field', 176, 152, 300, 'Search by last name', query[0], placeholder=False)
    m.field('pt_dob', 492, 152, 170, 'Date of birth (if available)', query[1], placeholder=False)
    m.btn('pt_search_btn', 678, 152, 100, 32, 'Search', primary=True)
    m.btn('btn_new_pt', 770, 88, 106, 32, '+ New', False)
    if results:
        cols = [('Patient name', 230), ('Date of birth', 140), ('Record number', 150), ('Status', 130)]
        rows = [['Smith, Mary A.', '03/14/1941', 'R-10482', ('chip', 'Active', 'ok')],
                ['Smith, Mary', '03/14/1914', 'R-09110', ('chip', 'Discharged', 'done')],
                ['Smith, Marie', '07/02/1944', 'R-11236', ('chip', 'Pending', 'warn')]]
        m.table('pt_results', 176, 222, cols, rows, row_h=40, head_h=34, sel=selected)
        m.text(176, 222 + 34 + 40 * 3 + 30, 'Sample data. Not real patients.', 13, False, MUTED, italic=True)
    else:
        m.skeleton(176, 240, 600, lines=5, gap=30, lh=9)
    return m


def patient_banner(m, name='Smith, Mary A.', dob='03/14/1941', rec='R-10482', status='Active', payer='[ payer ]'):
    m.rect(166, 88, 718, 62, fill='#F1F4F8', stroke=LINE2, rx=8, sw=1.5, name='pt_banner')
    m.text(182, 116, name, 22, True, NAVY, name='pt_name')
    m.text(182, 138, f'DOB {dob}    Record {rec}', 14, False, MUTED, name='pt_ids')
    m.chip(770, 98, status, 'ok', 14)
    m.text(770, 138, payer, 13, False, MUTED, italic=True)


TAB_SET = [('sum', 'Summary'), ('demo', 'Demographics'), ('docs', 'Documents'), ('orders', 'Orders'),
           ('sched', 'Schedule'), ('clin', 'Clinical'), ('bill', 'Billing')]


def patient_record(tab='sum', name='Smith, Mary A.', dob='03/14/1941', rec='R-10482'):
    m = Mock('Training mockup: a generic patient record with the patient name banner and record sections')
    m.chrome()
    m.shell('patients')
    patient_banner(m, name, dob, rec)
    m.tabs('tab', 166, 162, TAB_SET, tab)
    return m


def tab_docs(rows=None, sel=None, newrows=None, with_btn=True):
    m = patient_record('docs')
    if with_btn:
        m.btn('btn_upload', 744, 206, 130, 34, '+ Add', False, 15)
    cols = [('Document name', 290), ('Document type', 190), ('Document date', 120), ('Added', 110)]
    rows = rows if rows is not None else [
        ['SMITH_MARY_REFERRAL_20260928.pdf', 'Referral', '09/28/2026', '09/28/2026'],
    ]
    m.text(176, 232, 'Documents', 18, True, TXT)
    m.table('docs_list', 176, 250, cols, rows, row_h=40, head_h=32, sel=sel)
    return m


def lfield(m, name, x, y, label, value='', w=300, dropdown=False, placeholder=False, lw=160):
    """Form row with the label to the LEFT of the box, so callouts can sit to the right."""
    m.text(x, y + 21, label, 15, True, MUTED)
    m.rect(x + lw, y, w, 32, fill=WHITE, stroke=LINE2, rx=4, sw=1.5, name=name)
    if value:
        m.text(x + lw + 10, y + 22, value, 15, False, MUTED if placeholder else TXT, italic=placeholder)
    if dropdown:
        cx = x + lw + w - 18
        m.ops.append(f'<path d="M{cx - 6} {y + 13} l6 7 l6 -7 z" fill="{MUTED}"/>')


def tab_demographics(part='a'):
    m = patient_record('demo')
    m.text(176, 232, 'Demographics', 18, True, TXT)
    m.btn('btn_edit', 780, 214, 94, 32, 'Edit', False)
    if part == 'a':
        lfield(m, 'f_lname', 176, 252, 'Last name', 'Smith')
        lfield(m, 'f_fname', 176, 298, 'First name', 'Mary')
        lfield(m, 'f_dob', 176, 344, 'Date of birth', '03/14/1941', w=170)
        lfield(m, 'f_addr', 176, 390, 'Address', '123 Sample Street, Tamarac, FL 33319', w=340)
        lfield(m, 'f_phone', 176, 436, 'Phone', '(954) 555-0100', w=200)
    else:
        m.text(176, 262, 'Name, date of birth, address and phone are shown above.', 13, False, MUTED, italic=True)
        lfield(m, 'f_lang', 176, 282, 'Preferred language', 'English', w=200, dropdown=True)
        lfield(m, 'f_emerg', 176, 328, 'Emergency contact', 'Sample Contact', w=260)
        lfield(m, 'f_payer', 176, 374, 'Insurance', '[ payer ]', w=260, dropdown=True, placeholder=True)
        lfield(m, 'f_phys', 176, 420, 'Physician', 'Sample, Jane MD', w=260)
    return m


def tab_orders(rows=None, sel=None):
    m = patient_record('orders')
    m.text(176, 230, 'Orders', 18, True, TXT)
    cols = [('Order', 280), ('Order date', 110), ('Physician', 160), ('Status', 130)]
    rows = rows or [['Home health evaluate and treat', '09/27/2026', 'Sample, Jane MD', ('chip', 'Signed', 'ok')]]
    m.table('ord_list', 176, 250, cols, rows, row_h=40, head_h=32, sel=sel)
    return m


# =========================================================================== upload dialogs
def upload_dialog(stage='empty', doctype='', filename='', rows=None, date=''):
    m = tab_docs(rows=rows)
    m.dim()
    m.rect(250, 96, 430, 388, fill=WHITE, stroke='#6B7A90', rx=10, sw=2, name='dlg')
    m.rect(251, 97, 428, 40, fill=HDR, stroke='none', rx=9)
    m.text(268, 123, 'Add document', 17, True, TXT)
    m.text(662, 124, '✕', 18, True, MUTED, 'middle')
    m.text(268, 170, 'File', 14, True, MUTED)
    m.btn('dlg_file', 268, 178, 130, 34, 'Choose file', False, 15)
    m.text(412, 201, filename if filename else 'No file chosen', 13 if filename else 14, False, TXT if filename else MUTED, italic=not filename)
    m.field('dlg_type', 268, 252, 300, 'Document type', doctype, dropdown=True, placeholder=False)
    m.field('dlg_date', 268, 320, 160, 'Document date', date)
    m.field('dlg_notes', 268, 388, 396, 'Description / notes (if offered)', '')
    m.btn('dlg_cancel', 454, 436, 100, 34, 'Cancel', False)
    m.btn('dlg_save', 566, 436, 98, 34, 'Save', True)
    return m


def type_list_open(selected=None):
    m = upload_dialog('type', doctype='', filename='SMITH_MARY_REFERRAL_20260928.pdf')
    # drop-down list open below the type box
    m.rect(268, 286, 300, 168, fill=WHITE, stroke='#6B7A90', sw=2, rx=4)
    opts = ['[ list of document types ]', 'Referral', 'Physician order', 'Face-to-face', 'Other']
    for i, o in enumerate(opts):
        y = 288 + i * 33
        if o == selected:
            m.rect(270, y, 296, 32, fill='#EAF1FF', stroke='none', name='opt_sel')
        m.text(282, y + 22, o, 15, o == selected, MUTED if i == 0 else TXT, italic=(i == 0))
    m.rib_extra = 'The real type list is set by Alora and Zenith. Verify it in live Alora.'
    return m


def win_open(filename='', selected=None):
    m = Mock('Standard Windows Open dialog used to choose a file from the computer')
    m.rect(0, 0, W, RIBBON_Y, fill='#D9E2F0', stroke='#8A96A8', sw=2)
    m.rect(90, 40, 720, 440, fill=WHITE, stroke='#6B7A90', sw=2, rx=6)
    m.rect(91, 41, 718, 34, fill='#EDEFF3', stroke='none')
    m.text(108, 64, 'Open', 16, False, TXT)
    m.text(790, 64, '✕', 16, False, MUTED, 'middle')
    m.rect(110, 86, 560, 28, fill=WHITE, stroke=LINE2, rx=3, name='win_folder')
    m.text(124, 106, 'This PC  >  Documents  >  Zenith Scans  >  Ready to upload', 14, False, TXT)
    # left pane
    m.rect(110, 126, 170, 290, fill='#F7F9FC', stroke=LINE, name='win_tree')
    for i, t in enumerate(['Quick access', 'Desktop', 'Downloads', 'Documents', 'Zenith Scans']):
        m.text(124, 152 + i * 30, t, 14, i == 4, TXT if i == 4 else MUTED)
    # file list
    files = ['SMITH_MARY_REFERRAL_20260928.pdf', 'SMITH_MARY_ORDER_20260927.pdf', 'SMITH_MARY_F2F_20260915.pdf']
    m.rect(290, 126, 500, 290, fill=WHITE, stroke=LINE, name='win_file')
    m.text(302, 148, 'Name', 13, True, MUTED)
    for i, f in enumerate(files):
        y = 160 + i * 34
        if f == selected:
            m.rect(292, y, 496, 32, fill='#CFE3FF', stroke='#7FA6E8', name='win_sel')
        m.rect(302, y + 6, 16, 20, fill='#FFFFFF', stroke='#C44', rx=2)
        m.text(328, y + 22, f, 15, False, TXT)
    m.text(110, 450, 'File name:', 14, False, TXT)
    m.rect(190, 432, 440, 28, fill=WHITE, stroke=LINE2, rx=3, name='win_filename')
    if filename:
        m.text(200, 452, filename, 14, False, TXT)
    m.btn('win_open', 650, 430, 70, 32, 'Open', True, 15)
    m.btn('win_cancel', 730, 430, 70, 32, 'Cancel', False, 15)
    m.rib_extra = 'Windows screens look a little different on each computer.'
    return m


def explorer(files, selected=None, path='This PC  >  Documents  >  Zenith Scans  >  Ready to upload', colhdr='Name'):
    """File Explorer view of the scan folder (used for the naming standard)."""
    m = Mock('Training mockup: a Windows folder listing scanned files')
    m.rect(0, 0, W, RIBBON_Y, fill='#D9E2F0', stroke='#8A96A8', sw=2)
    m.rect(60, 34, 780, 440, fill=WHITE, stroke='#6B7A90', sw=2, rx=6)
    m.rect(61, 35, 778, 34, fill='#EDEFF3', stroke='none')
    m.text(78, 58, 'Ready to upload', 16, False, TXT)
    m.rect(80, 80, 740, 28, fill=WHITE, stroke=LINE2, rx=3, name='win_folder')
    m.text(94, 100, path, 14, False, TXT)
    m.rect(80, 124, 740, 330, fill=WHITE, stroke=LINE, name='win_file')
    m.text(94, 148, colhdr, 13, True, MUTED)
    m.text(560, 148, 'Date modified', 13, True, MUTED)
    m.text(720, 148, 'Size', 13, True, MUTED)
    for i, (f, d, s) in enumerate(files):
        y = 160 + i * 36
        if f == selected:
            m.rect(82, y, 736, 34, fill='#CFE3FF', stroke='#7FA6E8', name='win_sel')
        m.rect(94, y + 7, 16, 20, fill='#FFFFFF', stroke='#C44', rx=2)
        m.text(120, y + 23, f, 15, False, TXT, name=f'file{i}')
        m.text(560, y + 23, d, 13, False, MUTED)
        m.text(720, y + 23, s, 13, False, MUTED)
    m.rib_extra = 'Windows screens look a little different on each computer.'
    return m

"""Scheduling, monitoring, QA and billing screens (training mockups; Alora documents these features by name)."""
from mock import Mock, tw, W, H, RIBBON_Y, TXT, MUTED, LINE, LINE2, WHITE, NAVY, HDR, NAVBG, SEL, BTN, BTNP, RED, GOLD
import scenes as S


def segmented(m, name, x, y, labels, active, h=32, size=14):
    """A row of choices such as Day / Week / Month. Registers name and name.<i>."""
    cx = x
    total = 0
    for i, lab in enumerate(labels):
        w = tw(lab, size, i == active) + 26
        on = i == active
        m.rect(cx, y, w, h, fill=SEL if on else WHITE, stroke=LINE2, rx=4 if on else 0, sw=1.5, name=f'{name}.{i}')
        m.text(cx + w / 2, y + h / 2 + 5, lab, size, on, TXT if on else MUTED, 'middle', italic=True)
        cx += w - 1
        total += w - 1
    m.reg(name, x, y, total + 1, h)


def schedule_calendar(view='week', highlight=None, extra_visit=False, by=2, at=(2, 1), hide=None, label='11:00 SOC visit', sub='Smith, M.'):
    """Generic schedule. by: 0 patient, 1 team member, 2 agency. at: (column, row) of the highlighted visit."""
    m = Mock('Training mockup: a generic schedule screen with view choices and a week calendar')
    m.chrome()
    m.shell('schedule')
    m.text(176, 112, 'Schedule', 24, True, NAVY)
    m.text(176, 146, 'View by', 13, True, MUTED)
    segmented(m, 'sch_viewby', 176, 152, ['Patient', 'Team member', 'Agency'], by)
    m.text(470, 146, 'Show', 13, True, MUTED)
    segmented(m, 'sch_range', 470, 152, ['Day', 'Week', 'Month', 'Cert. period'], 1)
    m.btn('sch_add', 770, 152, 106, 32, '+ Add visit', True, 14)
    gx, gy, gw, gh = 176, 208, 700, 290
    m.rect(gx, gy, gw, gh, fill=WHITE, stroke=LINE2, sw=1.5, name='sch_grid')
    days = ['Mon 28', 'Tue 29', 'Wed 30', 'Thu 01', 'Fri 02']
    cw = gw / 5
    for i, d in enumerate(days):
        m.rect(gx + i * cw, gy, cw, 30, fill=HDR, stroke=LINE2, sw=1)
        m.text(gx + i * cw + cw / 2, gy + 21, d, 14, True, TXT, 'middle')
    for i in range(1, 5):
        m.line(gx + i * cw, gy + 30, gx + i * cw, gy + gh, LINE, 1)

    def visit(col, row, lab, sb, kind='gray', name=None):
        x = gx + col * cw + 8
        y = gy + 42 + row * 62
        fill = {'gray': '#EDF1F7', 'blue': '#DCE9FF', 'gold': '#FFF0C9'}[kind]
        m.rect(x, y, cw - 16, 54, fill=fill, stroke=LINE2, rx=5, sw=1.2, name=name)
        m.text(x + 8, y + 22, lab, 13, True, TXT)
        m.text(x + 8, y + 42, sb, 12, False, MUTED)
    base = [(0, 0, '9:00 Nurse', 'M. R.'), (0, 1, '1:00 Aide', 'J. D.'), (1, 0, '8:30 PT', 'A. L.'),
            (2, 0, '10:00 Nurse', 'S. T.'), (3, 1, '2:00 Aide', 'M. R.'), (4, 0, '9:30 Nurse', 'J. D.')]
    for col, row, lab, sb in base:
        if hide and (col, row) == tuple(hide):
            continue
        visit(col, row, lab, sb)
    if extra_visit:
        visit(at[0], at[1], label, sub, 'gold', name='sch_visit')
    else:
        m.reg('sch_visit', gx + at[0] * cw + 8, gy + 42 + at[1] * 62, cw - 16, 54)
    return m


def new_visit_form(part='a', alerts=False):
    m = Mock('Training mockup: a generic add visit form')
    m.chrome()
    m.shell('schedule')
    m.text(176, 112, 'Add visit', 24, True, NAVY)
    S.lfield(m, 'f_visit_pt', 176, 140, 'Patient', 'Smith, Mary A.', w=280, lw=150)
    S.lfield(m, 'f_visit_type', 176, 186, 'Visit type', 'Start of care (RN)', w=280, dropdown=True, lw=150)
    S.lfield(m, 'f_visit_date', 176, 232, 'Date', '10/01/2026', w=170, lw=150)
    S.lfield(m, 'f_visit_time', 176, 278, 'Time', '10:00 AM', w=170, lw=150)
    S.lfield(m, 'f_visit_member', 176, 324, 'Team member', '[ RN name ]', w=280, dropdown=True, lw=150, placeholder=True)
    S.lfield(m, 'f_visit_freq', 176, 370, 'Repeat / frequency', 'Does not repeat', w=280, dropdown=True, lw=150)
    if alerts:
        m.rect(680, 140, 200, 150, fill='#FFF8E6', stroke='#D79A00', rx=8, sw=1.5, name='sch_alerts')
        m.text(692, 164, 'Alerts', 15, True, '#7A4A00')
        m.chip(692, 176, 'Conflict', 'warn', 13)
        m.skeleton(692, 214, 170, lines=3, gap=18, lh=7, color='#EBD8A8')
    m.btn('btn_cancel', 560, 430, 100, 38, 'Cancel', False)
    m.btn('btn_save', 672, 430, 120, 38, 'Save', True)
    return m


def visit_edit():
    m = Mock('Training mockup: a generic screen to change a scheduled visit')
    m.chrome()
    m.shell('schedule')
    m.text(176, 112, 'Visit details', 24, True, NAVY)
    m.text(176, 140, 'Smith, Mary A.   Start of care visit   Team member: [ RN name ]', 14, False, MUTED)
    S.lfield(m, 'f_visit_date', 176, 168, 'Date', '10/01/2026', w=170, lw=170)
    S.lfield(m, 'f_visit_time', 176, 214, 'Time', '10:00 AM', w=170, lw=170)
    S.lfield(m, 'f_visit_member', 176, 260, 'Team member', '[ RN name ]', w=280, dropdown=True, lw=170, placeholder=True)
    m.text(176, 324, 'Reason for the change', 15, True, MUTED)
    m.rect(176, 334, 480, 62, fill=WHITE, stroke=LINE2, rx=4, sw=1.5, name='sch_reason')
    m.text(186, 358, 'Patient asked for a later time. Called 09/30 at 3:15 PM.', 14, False, TXT)
    m.btn('btn_cancel', 560, 430, 100, 38, 'Cancel', False)
    m.btn('btn_save', 672, 430, 120, 38, 'Save', True)
    return m


def live_monitor():
    m = Mock('Training mockup: a generic live visit monitor with status colors')
    m.chrome()
    m.shell('schedule')
    m.text(176, 112, 'Live Monitor', 24, True, NAVY)
    cols = [('Planned', 100), ('Team member', 160), ('Patient', 130), ('Status', 280)]
    rows = [['8:00 AM', 'Aide A', 'J. D.', ('chip', 'In progress, on time', 'ok')],
            ['9:00 AM', 'Nurse B', 'M. R.', ('chip', 'Late, not clocked in', 'warn')],
            ['9:30 AM', 'Aide C', 'A. L.', ('chip', 'No-show', 'bad')],
            ['7:00 AM', 'Therapist D', 'S. T.', ('chip', 'Complete', 'done')]]
    m.table('lm_table', 176, 150, cols, rows, row_h=46, head_h=34)
    m.reg('lm_status', 176 + 390, 150, 280, 34 + 46 * 4)
    m.text(876, 150 + 34 + 46 * 4 + 28, 'Sample data. Colors and words can differ in your Alora.', 13, False, MUTED, 'end', italic=True)
    return m


def exceptions_list():
    m = Mock('Training mockup: a generic list of visits waiting for office review')
    m.chrome()
    m.shell('schedule')
    m.text(176, 112, 'EVV exceptions', 24, True, NAVY)
    cols = [('Visit', 150), ('Team member', 130), ('What does not match', 250), ('Status', 120)]
    rows = [['09/29 8:00 AM', 'Aide A', 'No clock out', ('chip', 'Needs review', 'warn')],
            ['09/29 1:00 PM', 'Nurse B', 'Clock in far from address', ('chip', 'Needs review', 'warn')],
            ['09/28 10:30 AM', 'Aide C', 'Visit shorter than planned', ('chip', 'Needs review', 'warn')]]
    m.table('ex_list', 176, 150, cols, rows, row_h=46, head_h=34)
    m.reg('ex_issue', 176 + 280, 150, 250, 34 + 46 * 3)
    m.text(876, 150 + 34 + 46 * 3 + 28, 'Sample data. Not real visits.', 13, False, MUTED, 'end', italic=True)
    return m


def exception_detail():
    m = Mock('Training mockup: a generic screen to review one visit exception')
    m.chrome()
    m.shell('schedule')
    m.text(176, 112, 'Review visit', 24, True, NAVY)
    m.text(176, 140, '09/29 8:00 AM   Aide A   J. D.', 14, False, MUTED)
    m.rect(176, 160, 700, 70, fill='#FFF8E6', stroke='#D79A00', rx=6, sw=1.5, name='ex_issue')
    m.text(190, 186, 'What does not match', 14, True, '#7A4A00')
    m.text(190, 212, 'No clock out was recorded for this visit.', 15, False, TXT)
    m.text(176, 262, 'Reason (what really happened, and how you know)', 15, True, MUTED)
    m.rect(176, 272, 700, 76, fill=WHITE, stroke=LINE2, rx=4, sw=1.5, name='ex_reason')
    m.text(186, 296, 'Team member called 09/29 at 11:20 and said the visit ended at 10:45.', 14, False, TXT)
    m.text(186, 318, 'The visit note is signed at 10:47.', 14, False, TXT)
    m.btn('ex_return', 560, 410, 150, 38, 'Send back', False)
    m.btn('ex_approve', 724, 410, 150, 38, 'Approve', True)
    return m


def qa_screen():
    m = Mock('Training mockup: a generic quality review (QA) list')
    m.chrome()
    m.shell('qa')
    m.text(176, 112, 'QA', 24, True, NAVY)
    cols = [('Patient', 150), ('Item', 190), ('Due', 110), ('Status', 160)]
    rows = [['Smith, Mary A.', 'OASIS start of care', '10/06/2026', ('chip', 'Ready for QA', 'blue')],
            ['Jones, Robert', 'Plan of care (485)', '09/30/2026', ('chip', 'Needs correction', 'warn')],
            ['Lee, Ana', 'Visit note', '09/29/2026', ('chip', 'Approved', 'ok')]]
    m.table('qa_items', 176, 150, cols, rows, row_h=46, head_h=34)
    m.btn('qa_return', 680, 344 + 40, 180, 38, 'Return for correction', False, 14)
    m.text(876, 150 + 34 + 46 * 3 + 28, 'Sample data. Not real patients.', 13, False, MUTED, 'end', italic=True)
    return m


def billing_list():
    m = Mock('Training mockup: a generic billing status list')
    m.chrome()
    m.shell('billing')
    m.text(176, 112, 'Billing', 24, True, NAVY)
    cols = [('Patient', 170), ('Period', 170), ('NOA', 120), ('Claim status', 180)]
    rows = [['Smith, Mary A.', '10/01 to 10/30', ('chip', 'Due in 4 days', 'warn'), ('chip', 'Not ready', 'bad')],
            ['Jones, Robert', '09/01 to 09/30', ('chip', 'Accepted', 'ok'), ('chip', 'Ready', 'ok')],
            ['Lee, Ana', '09/05 to 10/04', ('chip', 'Accepted', 'ok'), ('chip', 'Missing item', 'warn')]]
    m.table('bill_ready', 176, 150, cols, rows, row_h=46, head_h=34)
    m.text(876, 150 + 34 + 46 * 3 + 28, 'Sample data. Not real patients.', 13, False, MUTED, 'end', italic=True)
    return m


def noa_list():
    m = Mock('Training mockup: a generic NOA list with a create button')
    m.chrome()
    m.shell('billing')
    m.text(176, 112, 'NOA (Notice of Admission)', 24, True, NAVY)
    cols = [('Patient', 160), ('Start of care', 120), ('NOA due', 110), ('Status', 130), ('', 130)]
    rows = [['Smith, Mary A.', '10/01/2026', '10/06/2026', ('chip', 'Not sent', 'warn'), ('btn', 'Create NOA')],
            ['Jones, Robert', '09/26/2026', '10/01/2026', ('chip', 'Accepted', 'ok'), ''],
            ['Lee, Ana', '09/24/2026', '09/29/2026', ('chip', 'Accepted', 'ok'), '']]
    m.table('noa_list', 176, 150, cols, rows, row_h=46, head_h=34)
    m.reg('noa_status', 176 + 390, 150, 130, 34 + 46 * 3)
    m.text(876, 150 + 34 + 46 * 3 + 28, 'Sample data. Not real patients.', 13, False, MUTED, 'end', italic=True)
    return m


def tab_billing():
    """The Billing section of a patient record with a simple readiness list (layout is a mockup)."""
    m = S.patient_record('bill')
    m.text(176, 232, 'Billing', 18, True, TXT)
    cols = [('Item', 360), ('Status', 200), ('Date', 140)]
    rows = [['Plan of care (485) signed and dated', ('chip', 'Complete', 'ok'), '09/29/2026'],
            ['Start of care OASIS accepted', ('chip', 'Complete', 'ok'), '10/02/2026'],
            ['Notice of Admission (NOA)', ('chip', 'Missing', 'bad'), ''],
            ['Visits documented and approved (QA)', ('chip', 'In progress', 'warn'), '']]
    m.table('bill_items', 176, 250, cols, rows, row_h=40, head_h=32)
    m.text(876, 250 + 32 + 40 * 4 + 28, 'Sample data. Not a real patient.', 13, False, MUTED, 'end', italic=True)
    return m


def staff_list():
    m = Mock('Training mockup: a generic staff list with credential dates')
    m.chrome()
    m.shell('staff')
    m.text(176, 112, 'Staff', 24, True, NAVY)
    cols = [('Name', 170), ('Role', 90), ('License / credential', 170), ('Expires', 110), ('Status', 100)]
    rows = [['Sample, Nurse A.', 'RN', 'Nursing license', '11/30/2026', ('chip', 'OK', 'ok')],
            ['Sample, Aide B.', 'Aide', 'Aide certificate', '10/15/2026', ('chip', '30 days', 'warn')],
            ['Sample, Therapist C.', 'PT', 'Therapy license', '09/20/2026', ('chip', 'Expired', 'bad')]]
    m.table('staff_list', 176, 150, cols, rows, row_h=46, head_h=34)
    m.reg('staff_exp', 176 + 430, 150, 110, 34 + 46 * 3)
    m.text(876, 150 + 34 + 46 * 3 + 28, 'Sample data. Not real staff.', 13, False, MUTED, 'end', italic=True)
    return m


def blank_shell(active='dash', title='Dashboard'):
    """Any main screen with the content area left blank, for steps that only say which menu item to click."""
    m = Mock('Training mockup: a generic screen with the main menu on the left')
    m.chrome()
    m.shell(active)
    m.text(176, 112, title, 24, True, NAVY)
    m.skeleton(176, 140, 700, lines=6, gap=34, lh=10)
    m.skeleton(176, 360, 330, lines=3, gap=34, lh=10)
    return m

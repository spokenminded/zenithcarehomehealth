"""Document screens: referral form, PDF viewer, sample order, sample face-to-face, timeline, pending lists."""
from mock import Mock, tw, W, H, RIBBON_Y, TXT, MUTED, LINE, LINE2, WHITE, NAVY, HDR, NAVBG, SEL, BTN, BTNP, RED, GOLD
import scenes as S
import scenes2 as S2


def _bg(m):
    m.rect(0, 0, W, RIBBON_Y, fill='#D9E2F0', stroke='#8A96A8', sw=2)


def referral_form():
    """Generic referral entry (Alora documents intake and referral tracking; the screen itself is unverified)."""
    m = Mock('Training mockup: a generic referral entry screen')
    m.chrome()
    m.shell('patients')
    m.text(176, 112, 'Referral', 24, True, NAVY)
    m.text(176, 140, 'Patient: Smith, Mary A.   DOB 03/14/1941', 14, False, MUTED)
    S.lfield(m, 'ref_date', 176, 160, 'Referral date / time', '09/28/2026  2:40 PM', w=240)
    S.lfield(m, 'ref_src', 176, 206, 'Referral source', 'Sample Hospital', w=300)
    S.lfield(m, 'ref_phys', 176, 252, 'Referring physician', 'Sample, Jane MD', w=280)
    S.lfield(m, 'ref_reason', 176, 298, 'Reason for referral', 'Sample diagnosis', w=300)
    S.lfield(m, 'ref_status', 176, 344, 'Status', 'Pending', w=200, dropdown=True)
    m.btn('btn_save', 176, 410, 120, 38, 'Save', True)
    return m


def pdf_viewer(pages='1 of 3', title='SMITH_MARY_REFERRAL_20260928.pdf'):
    """A generic PDF viewer window (Windows, not Alora) showing a sample referral page."""
    m = Mock('Training mockup: a PDF viewer window showing a sample referral page')
    _bg(m)
    m.rect(60, 28, 780, 460, fill=WHITE, stroke='#6B7A90', sw=2, rx=6)
    m.rect(61, 29, 778, 38, fill='#EDEFF3', stroke='none')
    m.text(78, 54, title, 15, False, TXT)
    m.rect(61, 68, 778, 34, fill='#F4F6FA', stroke='none')
    m.text(400, 91, pages, 15, True, TXT, 'middle', name='pdf_pages')
    m.text(300, 91, '‹  Previous', 14, False, MUTED)
    m.text(470, 91, 'Next  ›', 14, False, MUTED)
    m.rect(110, 112, 680, 368, fill='#E8ECF1', stroke='none')
    m.paper(240, 118, 420, 356)
    m.text(450, 150, '[ Hospital name ]', 15, False, MUTED, 'middle', italic=True)
    m.text(450, 176, 'REFERRAL FOR HOME HEALTH', 16, True, NAVY, 'middle')
    m.text(262, 214, 'Patient:  Mary Smith      DOB:  03/14/1941', 15, False, TXT, name='pdf_name')
    m.text(262, 242, 'Referral date:  09/28/2026', 15, False, TXT)
    m.skeleton(262, 268, 370, lines=5, gap=22, lh=8)
    m.text(262, 410, 'Physician:  Jane Sample, MD', 15, False, TXT)
    m.reg('pdf_text', 252, 196, 400, 240)
    m.rib_extra = 'SAMPLE DOCUMENT FOR TRAINING. NOT A REAL REFERRAL.'
    return m


def filename_anatomy(good=True):
    m = Mock('Training mockup: how to build a document file name')
    _bg(m)
    m.rect(40, 30, 820, 450, fill=WHITE, stroke='#8A96A8', sw=2, rx=8)
    m.text(450, 70, 'Zenith file name pattern', 22, True, NAVY, 'middle')
    parts = [('SMITH', 'last'), ('_', None), ('MARY', 'first'), ('_', None), ('REFERRAL', 'type'), ('_', None), ('20260928', 'date'), ('.pdf', 'ext')]
    size = 34
    total = sum(tw(p, size, True) for p, _ in parts)
    x = 450 - total / 2
    y = 290
    for p, nm in parts:
        w = tw(p, size, True)
        if nm:
            m.rect(x - 3, y - size, w + 6, size + 14, fill='#FFF6DC', stroke='#D79A00', rx=4, sw=1.5, name=nm)
        m.text(x, y, p, size, True, TXT)
        x += w
    m.text(450, 370, 'LASTNAME_FIRSTNAME_DOCUMENTTYPE_YYYYMMDD.pdf', 17, False, MUTED, 'middle')
    m.text(450, 410, 'Capital letters. No spaces. Use the underscore _ between the parts.', 17, False, TXT, 'middle')
    m.rib_extra = 'ZENITH NAMING STANDARD (DRAFT). NOT AN ALORA SCREEN.'
    return m


def order_sample():
    m = Mock('Training mockup: a sample physician order with the parts to check')
    _bg(m)
    m.paper(60, 18, 540, RIBBON_Y - 36)
    m.text(330, 56, '[ Physician office name and address ]', 14, False, MUTED, 'middle', italic=True)
    m.text(330, 92, 'PHYSICIAN ORDER', 24, True, NAVY, 'middle')
    m.line(80, 106, 580, 106, NAVY, 2)
    m.text(84, 140, 'Patient:', 15, False, MUTED)
    m.text(150, 140, 'Mary Smith', 17, True, TXT, name='o_name')
    m.text(350, 140, 'DOB:', 15, False, MUTED)
    m.text(394, 140, '03/14/1941', 17, True, TXT, name='o_dob')
    m.reg('o_id', 142, 120, 420, 28)
    m.text(84, 178, 'Date of order:', 15, False, MUTED)
    m.text(200, 178, '09/27/2026', 17, True, TXT, name='o_date')
    m.text(84, 218, 'Order:', 15, False, MUTED)
    m.text(150, 218, 'Admit to home health. Evaluate and treat.', 16, False, TXT)
    m.text(150, 244, 'Skilled nursing and physical therapy as needed.', 16, False, TXT)
    m.reg('o_text', 140, 198, 450, 62)
    m.text(84, 290, 'Diagnosis:', 15, False, MUTED)
    m.text(180, 290, '[ sample diagnosis ]', 16, False, TXT, italic=True)
    m.text(84, 350, 'Physician signature:', 15, False, MUTED)
    m.line(250, 352, 560, 352, '#6B7280', 1.5)
    m.ops.append('<path d="M280 344 C300 318, 312 372, 334 338 S372 322, 392 346 S440 360, 480 330" fill="none" stroke="#1B2B4B" stroke-width="2.6" stroke-linecap="round"/>')
    m.reg('o_sig', 240, 318, 330, 44)
    m.text(84, 400, 'Printed name:', 15, False, MUTED)
    m.text(200, 400, 'Jane Sample, MD', 16, False, TXT)
    m.text(380, 400, 'NPI:', 15, False, MUTED)
    m.text(418, 400, '0000000000', 16, True, TXT, name='o_npi')
    m.text(84, 446, 'Date signed:', 15, False, MUTED)
    m.text(190, 446, '09/27/2026', 16, True, TXT, name='o_signdate')
    m.rib_extra = 'SAMPLE DOCUMENT FOR TRAINING. NOT A REAL ORDER.'
    return m


def f2f_sample():
    m = Mock('Training mockup: a sample face-to-face encounter document with the parts to check')
    _bg(m)
    m.paper(60, 18, 540, RIBBON_Y - 36)
    m.text(330, 56, '[ Physician office or hospital name ]', 14, False, MUTED, 'middle', italic=True)
    m.text(330, 90, 'FACE-TO-FACE ENCOUNTER', 22, True, NAVY, 'middle')
    m.line(80, 104, 580, 104, NAVY, 2)
    m.text(84, 136, 'Patient:', 15, False, MUTED)
    m.text(150, 136, 'Mary Smith    DOB 03/14/1941', 16, True, TXT)
    m.text(84, 174, 'Date of encounter:', 15, False, MUTED)
    m.text(236, 174, '09/15/2026', 17, True, TXT, name='f_date')
    m.text(84, 212, 'Seen by:', 15, False, MUTED)
    m.text(160, 212, 'Jane Sample, MD (physician)', 16, False, TXT, name='f_who')
    m.text(84, 256, 'Clinical findings that support the need for home health:', 14, True, TXT)
    m.text(84, 282, 'Weak after a fall. Needs help to walk and to bathe.', 15, False, TXT)
    m.text(84, 306, 'Leaving home takes a great effort.', 15, False, TXT)
    m.reg('f_find', 76, 240, 510, 84)
    m.text(84, 356, 'This visit was related to the primary reason for home health:', 14, False, TXT)
    m.rect(84, 368, 18, 18, fill=WHITE, stroke='#374151', rx=2, sw=1.8)
    m.ops.append('<path d="M88 377 l4 4 l8 -10" stroke="#1E6B3A" stroke-width="2.6" fill="none"/>')
    m.text(112, 383, 'Yes', 15, True, TXT)
    m.reg('f_rel', 76, 340, 510, 54)
    m.text(84, 430, 'Signature:', 15, False, MUTED)
    m.line(170, 432, 400, 432, '#6B7280', 1.5)
    m.ops.append('<path d="M190 424 C208 400, 220 452, 240 418 S282 406, 300 428 S340 440, 372 410" fill="none" stroke="#1B2B4B" stroke-width="2.6" stroke-linecap="round"/>')
    m.reg('f_sig', 160, 398, 250, 44)
    m.text(84, 470, 'Date signed:  09/16/2026', 15, False, TXT)
    m.rib_extra = 'SAMPLE DOCUMENT FOR TRAINING. NOT A REAL ENCOUNTER NOTE.'
    return m


def f2f_timeline():
    """The 90 days before to 30 days after the start of care window, with example dates."""
    m = Mock('Training mockup: the face-to-face window, 90 days before to 30 days after the start of care')
    _bg(m)
    m.rect(40, 40, 820, 440, fill=WHITE, stroke='#8A96A8', sw=2, rx=8)
    m.text(450, 88, 'The face-to-face visit window (example dates)', 22, True, NAVY, 'middle')
    x0, xs, x1 = 90, 560, 830
    m.rect(x0, 210, xs - x0, 40, fill='#33507F', stroke='none', name='before')
    m.rect(xs, 210, x1 - xs, 40, fill='#D4AF62', stroke='none', name='after')
    m.text((x0 + xs) / 2, 236, '90 days before', 18, True, WHITE, 'middle')
    m.text((xs + x1) / 2, 236, '30 days after', 18, True, NAVY, 'middle')
    m.line(xs, 190, xs, 270, RED, 4)
    m.text(xs, 180, 'Start of care  10/01/2026', 16, True, RED, 'middle', name='soc')
    m.text(x0, 290, '07/03/2026', 15, True, TXT, 'middle' if False else 'start')
    m.text(x1, 290, '10/31/2026', 15, True, TXT, 'end')
    # encounter marker inside the window
    ex = 410
    m.ops.append(f'<circle cx="{ex}" cy="230" r="11" fill="{WHITE}" stroke="{RED}" stroke-width="4"/>')
    m.reg('enc', ex - 14, 216, 28, 28)
    m.text(450, 440, 'The encounter must be inside this window.', 18, False, TXT, 'middle')
    m.rib_extra = 'EXAMPLE DATES ONLY. NOT AN ALORA SCREEN.'
    return m


def pending_list(kind='orders'):
    """Alora documents pending 485s, orders and OASIS shown in one place. This layout is a mockup."""
    m = Mock('Training mockup: a generic list of pending clinical items')
    m.chrome()
    m.shell('clinical')
    title = {'orders': 'Pending orders', '485': 'Pending plans of care (485)', 'oasis': 'Pending OASIS', 'all': 'Pending clinical items'}[kind]
    m.text(176, 112, title, 24, True, NAVY)
    cols = [('Patient', 210), ('Item', 210), ('Date', 110), ('Status', 170)]
    rows = [['Smith, Mary A.', 'Home health order', '09/27/2026', ('chip', 'Needs signature', 'warn')],
            ['Jones, Robert', 'Verbal order', '09/28/2026', ('chip', 'Needs signature', 'warn')],
            ['Lee, Ana', 'Home health order', '09/26/2026', ('chip', 'Signed', 'ok')]]
    if kind == '485':
        rows = [['Smith, Mary A.', 'Plan of care (485)', '09/29/2026', ('chip', 'Sent to doctor', 'blue')], ['Jones, Robert', 'Plan of care (485)', '09/25/2026', ('chip', 'Needs signature', 'warn')], ['Lee, Ana', 'Plan of care (485)', '09/24/2026', ('chip', 'Signed', 'ok')]]
    if kind == 'oasis':
        rows = [['Smith, Mary A.', 'OASIS start of care', '09/29/2026', ('chip', 'In progress', 'warn')], ['Jones, Robert', 'OASIS recertification', '09/28/2026', ('chip', 'Ready for QA', 'blue')], ['Lee, Ana', 'OASIS start of care', '09/26/2026', ('chip', 'Complete', 'ok')]]
    m.table('pend', 176, 160, cols, rows, row_h=42, head_h=34)
    m.text(176, 160 + 34 + 42 * 3 + 28, 'Sample data. Not real patients.', 13, False, MUTED, italic=True)
    return m


def alora_doc_open():
    """An uploaded document opened inside Alora's record (viewer layout is a mockup)."""
    m = S.tab_docs(rows=[['SMITH_MARY_REFERRAL_20260928.pdf', 'Referral', '09/28/2026', '09/28/2026']])
    m.dim()
    m.rect(230, 92, 480, 404, fill=WHITE, stroke='#6B7A90', sw=2, rx=10, name='viewer')
    m.rect(231, 93, 478, 38, fill=HDR, stroke='none', rx=9)
    m.text(248, 118, 'SMITH_MARY_REFERRAL_20260928.pdf', 15, True, TXT)
    m.text(690, 119, '✕', 17, True, MUTED, 'middle')
    m.text(470, 154, 'Page 1 of 3', 14, True, MUTED, 'middle', name='v_pages')
    m.paper(300, 166, 340, 320)
    m.text(470, 196, 'REFERRAL FOR HOME HEALTH', 14, True, NAVY, 'middle')
    m.text(320, 226, 'Patient:  Mary Smith    DOB:  03/14/1941', 13, False, TXT, name='v_name')
    m.skeleton(320, 250, 300, lines=6, gap=22, lh=8)
    m.rib_extra = 'The real document viewer and its buttons must be verified in live Alora.'
    return m

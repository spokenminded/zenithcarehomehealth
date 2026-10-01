"""More training screens: keyboard, menus, forms, Zenith paper forms."""
from mock import Mock, tw, W, H, RIBBON_Y, TXT, MUTED, LINE, LINE2, WHITE, NAVY, HDR, NAVBG, SEL, BTN, BTNP, RED, GOLD
import scenes as S


def keyboard():
    m = Mock('Keyboard: the Windows key and the L key lock a Windows computer')
    m.rect(0, 0, W, RIBBON_Y, fill='#E9EDF3', stroke='#8A96A8', sw=2)
    m.text(450, 70, 'Press two keys at the same time', 26, True, NAVY, 'middle')
    def key(x, y, w, label, name=None, size=18):
        m.rect(x, y, w, 56, fill=WHITE, stroke='#8492A8', rx=8, sw=2, name=name)
        m.text(x + w / 2, y + 36, label, size, True, TXT, 'middle')
    rows = [('QWERTYUIOP', 150), ('ASDFGHJKL', 175), ('ZXCVBNM', 210)]
    y = 120
    for letters, x0 in rows:
        for i, ch in enumerate(letters):
            key(x0 + i * 62, y, 56, ch, 'key_l' if ch == 'L' else None)
        y += 66
    # bottom row
    x = 150
    key(x, y, 90, 'Ctrl', size=16)
    # Windows key with four squares
    m.rect(250, y, 76, 56, fill=WHITE, stroke='#8492A8', rx=8, sw=2, name='key_win')
    for dx, dy in ((0, 0), (16, 0), (0, 16), (16, 16)):
        m.rect(270 + dx, y + 11 + dy, 14, 14, fill='#33507F', stroke='none', rx=1)
    key(336, y, 76, 'Alt', size=16)
    key(422, y, 280, 'Space', size=16)
    key(712, y, 76, 'Alt', size=16)
    m.rib_extra = 'Keyboards differ a little by computer. The two keys are always there.'
    return m


def dashboard_usermenu():
    m = S.dashboard()
    m.rect(690, 70, 200, 88, fill=WHITE, stroke='#6B7A90', sw=2, rx=6, name='umenu')
    m.text(706, 100, '[ your account ]', 15, False, MUTED, italic=True)
    m.line(690, 112, 890, 112, LINE, 1)
    m.text(706, 140, '[ log out ]', 15, True, TXT, italic=True, name='logout')
    m.reg('logout', 696, 116, 188, 34)
    return m


def patients_none(query='Smithe'):
    m = S.patients_list(results=False, query=(query, ''))
    m.rect(176, 236, 700, 120, fill='#F7F9FC', stroke=LINE2, rx=8, sw=1.5, name='pt_none')
    m.text(526, 290, 'No patients found', 20, True, MUTED, 'middle')
    m.text(526, 322, '[ wording of this message will vary ]', 14, False, MUTED, 'middle', italic=True)
    return m


def new_patient_form(part='a', filled=True):
    """part a: referral, name, birth date, address, phone. part b: insurance, physician and Save."""
    m = Mock('Training mockup: a generic new patient form')
    m.chrome()
    m.shell('patients')
    m.text(176, 112, 'New patient', 24, True, NAVY)
    v = (lambda s: s if filled else '')
    if part == 'a':
        S.lfield(m, 'f_refdate', 176, 136, 'Referral date', v('09/28/2026'), w=170)
        S.lfield(m, 'f_refsrc', 176, 180, 'Referral source', v('Sample Hospital'), w=300)
        S.lfield(m, 'f_lname', 176, 224, 'Last name', v('Smith'), w=240)
        S.lfield(m, 'f_fname', 176, 268, 'First name', v('Mary'), w=240)
        S.lfield(m, 'f_dob', 176, 312, 'Date of birth', v('03/14/1941'), w=170)
        S.lfield(m, 'f_addr', 176, 356, 'Address', v('123 Sample Street, Tamarac, FL'), w=340)
        S.lfield(m, 'f_phone', 176, 400, 'Phone', v('(954) 555-0100'), w=200)
    else:
        m.text(176, 140, 'Referral, name, birth date, address and phone are filled in above.', 13, False, MUTED, italic=True)
        S.lfield(m, 'f_payer', 176, 172, 'Insurance', v('[ payer ]'), w=280, dropdown=True, placeholder=True)
        S.lfield(m, 'f_memberid', 176, 222, 'Insurance ID', v('1AB2-CD3-EF45'), w=240)
        S.lfield(m, 'f_phys', 176, 272, 'Physician', v('Sample, Jane MD'), w=280)
        m.btn('btn_cancel', 560, 420, 100, 38, 'Cancel', False)
        m.btn('btn_save', 672, 420, 120, 38, 'Save', True)
    return m


# ---------------------------------------------------------------------------- Zenith paper forms
ZFORMS = {}   # title -> sections, filled whenever a paper form is drawn; Tab 11 prints the same forms
ZUSE = {}     # title -> list of procedure numbers that use the form
CUR = [None]  # procedure number being scanned (set by content/c11_forms.py)


def zform(title, sections, sub='', note='ZENITH FORM (PAPER). THIS IS NOT AN ALORA SCREEN.', lh=46, x0=70, w=610, header_note=None):
    """sections: list of ('h', text) | ('line', name, label) | ('two', name1, label1, name2, label2) | ('check', name, label)
    | ('text', text) | ('gap',)"""
    def _height(lh_):
        y_ = 92
        for sc_ in sections:
            k_ = sc_[0]
            y_ += {'h': 30, 'line': lh_, 'two': lh_, 'check': lh_ - 6, 'kv': lh_ - 4, 'text': 24, 'gap': 10}[k_]
        return y_
    while _height(lh) > 486 and lh > 30:
        lh -= 2
    ZFORMS.setdefault(title, sections)
    if CUR[0] and CUR[0] not in ZUSE.setdefault(title, []):
        ZUSE[title].append(CUR[0])
    m = Mock(f'Zenith form: {title}')
    m.rect(0, 0, W, RIBBON_Y, fill='#D9E2F0', stroke='#8A96A8', sw=2)
    m.paper(x0 - 10, 18, w + 20, RIBBON_Y - 36, name='paper')
    m.rect(x0, 28, w, 40, fill=NAVY, stroke='none')
    m.text(x0 + 14, 55, 'ZENITH CARE HOME HEALTH, LLC', 12, True, '#D4AF62')
    m.text(x0 + w - 14, 55, title, 17, True, WHITE, 'end')
    y = 92
    for sct in sections:
        k = sct[0]
        if k == 'h':
            m.rect(x0, y - 8, w, 24, fill='#E8ECF4', stroke='none')
            m.text(x0 + 8, y + 9, sct[1], 13, True, NAVY)
            y += 30
        elif k == 'line':
            m.text(x0 + 6, y + 14, sct[2], 14, False, TXT)
            lx = x0 + 10 + tw(sct[2], 14) + 6
            m.line(lx, y + 17, x0 + w - 6, y + 17, '#6B7280', 1.3)
            m.reg(sct[1], x0, y - 2, w, 26)
            y += lh
        elif k == 'two':
            half = w / 2
            m.text(x0 + 6, y + 14, sct[2], 14, False, TXT)
            m.line(x0 + 10 + tw(sct[2], 14) + 6, y + 17, x0 + half - 14, y + 17, '#6B7280', 1.3)
            m.reg(sct[1], x0, y - 2, half - 8, 26)
            m.reg(sct[1] + '_row', x0, y - 2, w, 26)
            m.text(x0 + half + 6, y + 14, sct[4], 14, False, TXT)
            m.line(x0 + half + 10 + tw(sct[4], 14) + 6, y + 17, x0 + w - 6, y + 17, '#6B7280', 1.3)
            m.reg(sct[3], x0 + half, y - 2, half - 6, 26)
            y += lh
        elif k == 'check':
            m.rect(x0 + 8, y, 18, 18, fill=WHITE, stroke='#374151', rx=2, sw=1.8)
            m.text(x0 + 36, y + 15, sct[2], 14, False, TXT)
            m.reg(sct[1], x0, y - 4, w, 26)
            y += lh - 6
        elif k == 'kv':
            m.text(x0 + 8, y + 14, sct[2], 14, False, MUTED)
            m.text(x0 + 250, y + 14, sct[3], 15, True, NAVY)
            m.reg(sct[1], x0, y - 4, w, 26)
            y += lh - 4
        elif k == 'text':
            m.text(x0 + 6, y + 14, sct[1], 13, False, MUTED, italic=True)
            y += 24
        elif k == 'gap':
            y += 10
    m.rib_extra = note
    m.tight = lh < 40
    return m

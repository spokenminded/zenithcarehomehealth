"""Training-mockup engine for the Zenith Alora Office Operating Manual.

Every picture this module draws is a TRAINING MOCKUP, never a real Alora screenshot. The layout is a
neutral wireframe of a desktop web application. Gray italic words describe what an area is for; they
are not Alora wording. Numbered red circles, red highlight boxes and arrows show where to click.
Each callout carries a status chip (see ui.py) so nobody mistakes a guess for a verified name.
"""
import html
import itertools
from pathlib import Path

from fontTools.ttLib import TTFont

import ui

def _find_font(name):
    # Liberation Sans has the same letter widths as Arial. It is only used to measure text so pills fit exactly.
    for d in ('/usr/share/fonts/truetype/liberation', '/usr/share/fonts/liberation', '/usr/share/fonts/truetype/liberation2',
              '/Library/Fonts', '/System/Library/Fonts/Supplemental', 'C:/Windows/Fonts'):
        for n in (name, name.replace('LiberationSans', 'Arial').replace('-Regular', '').replace('-Bold', 'bd') + '.ttf'):
            p = Path(d) / n
            if p.exists():
                return TTFont(p)
    raise SystemExit('Cannot find LiberationSans-Regular.ttf and LiberationSans-Bold.ttf (or Arial). Install the fonts-liberation package and run again.')


_REG = _find_font('LiberationSans-Regular.ttf')
_BLD = _find_font('LiberationSans-Bold.ttf')


def _adv(font):
    cmap = font.getBestCmap()
    hm = font['hmtx']
    upm = font['head'].unitsPerEm
    return cmap, hm, upm


_CM = {False: _adv(_REG), True: _adv(_BLD)}


def tw(s, size, bold=False):
    cmap, hm, upm = _CM[bold]
    total = 0
    for ch in s:
        g = cmap.get(ord(ch))
        total += hm[g][0] if g else upm * 0.5
    return total / upm * size


def esc(s):
    return html.escape(str(s), quote=True)


# palette (wireframe, deliberately not any product's branding)
TXT = '#1F2937'
MUTED = '#6B7280'
LINE = '#D5DBE5'
LINE2 = '#AAB4C3'
WHITE = '#FFFFFF'
CHROME = '#DDE3EB'
HDR = '#F1F4F8'
NAVBG = '#F7F9FC'
SEL = '#E3E9F3'
BTN = '#DDE3EC'
BTNP = '#5B6B84'
RED = '#C62828'
NAVY = '#1B2B4B'
GOLD = '#B8892F'
AMBER_BG = '#FFE9B8'
AMBER_TX = '#7A4A00'
FONT = 'Arial, "Liberation Sans", Helvetica, sans-serif'

W, H = 900, 536
RIBBON_Y = 512

CHIPS = {
    'VERIFY': ('VERIFY', AMBER_BG, AMBER_TX, '#D79A00', True),
    'FEATURE': ('ALORA FEATURE', '#DCE9FF', '#1F4B99', '#7FA6E8', False),
    'WINDOWS': ('WINDOWS', '#E7EAEE', '#374151', '#9AA5B5', False),
    'ZENITH': ('ZENITH FORM', '#E3E8F2', NAVY, '#7F8FB0', False),
    'VERIFIED': ('VERIFIED', '#DCF2E3', '#1E6B3A', '#66B27F', False),
}

_uid = itertools.count(1)

NAV_ITEMS = [
    ('dash', 'Dashboard'), ('patients', 'Patients'), ('schedule', 'Schedule'), ('clinical', 'Clinical'),
    ('qa', 'QA'), ('billing', 'Billing'), ('reports', 'Reports'), ('staff', 'Staff'), ('messages', 'Messages'),
]


class Mock:
    """One training screen. Build it with the drawing methods, add callouts, then call svg()."""

    def __init__(self, alt='Training mockup'):
        self.ops = []
        self.T = {}
        self.calls = []
        self.alt = alt
        self.id = next(_uid)

    # ------------------------------------------------------------------ primitives
    def reg(self, name, x, y, w, h):
        if name:
            self.T[name] = (x, y, w, h)

    def rect(self, x, y, w, h, fill=WHITE, stroke=LINE, rx=0, sw=1, dash=None, name=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op is not None else ''
        self.ops.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')
        self.reg(name, x, y, w, h)

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.ops.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=15, bold=False, fill=TXT, anchor='start', italic=False, name=None):
        w = tw(s, size, bold)
        x0 = x if anchor == 'start' else (x - w / 2 if anchor == 'middle' else x - w)
        st = ' font-style="italic"' if italic else ''
        wt = ' font-weight="700"' if bold else ''
        self.ops.append(f'<text x="{x}" y="{y}" font-size="{size}"{wt}{st} fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')
        self.reg(name, x0, y - size, w, size * 1.3)
        return w

    def skeleton(self, x, y, w, lines=3, gap=16, lh=7, color='#E3E8EF'):
        """Neutral gray bars standing in for text that does not matter to this step."""
        for i in range(lines):
            ww = w if i < lines - 1 else w * 0.62
            self.ops.append(f'<rect x="{x}" y="{y + i * gap}" width="{ww}" height="{lh}" rx="3.5" fill="{color}"/>')

    def chip(self, x, y, label, kind='gray', size=13):
        col = {
            'ok': ('#DCF2E3', '#1E6B3A', '#66B27F'),
            'warn': ('#FFF0C9', '#7A4A00', '#E0A400'),
            'bad': ('#FBD9D9', '#8B1A1A', '#E27C7C'),
            'gray': ('#E7EAEE', '#374151', '#B4BCC8'),
            'blue': ('#DCE9FF', '#1F4B99', '#7FA6E8'),
            'done': ('#EEF0F3', '#6B7280', '#C8CED8'),
        }[kind]
        w = tw(label, size, True) + 16
        self.ops.append(f'<rect x="{x}" y="{y}" width="{w}" height="{size + 9}" rx="{(size + 9) / 2}" fill="{col[0]}" stroke="{col[2]}" stroke-width="1"/>')
        self.ops.append(f'<text x="{x + w / 2}" y="{y + size + 1}" font-size="{size}" font-weight="700" fill="{col[1]}" text-anchor="middle">{esc(label)}</text>')
        return w

    def btn(self, name, x, y, w, h, label, primary=False, size=15):
        self.rect(x, y, w, h, fill=BTNP if primary else BTN, stroke='#8492A8' if not primary else '#46556D', rx=6, name=name)
        self.text(x + w / 2, y + h / 2 + size * 0.35, label, size, True, WHITE if primary else TXT, 'middle')

    def field(self, name, x, y, w, label, value='', h=32, dropdown=False, placeholder=False, size=15):
        self.text(x, y - 12, label, 14, True, MUTED)
        self.rect(x, y, w, h, fill=WHITE, stroke=LINE2, rx=4, sw=1.5, name=name)
        if value:
            self.text(x + 10, y + h / 2 + size * 0.35, value, size, False, MUTED if placeholder else TXT, italic=placeholder)
        if dropdown:
            cx = x + w - 18
            self.ops.append(f'<path d="M{cx - 6} {y + h / 2 - 3} l6 7 l6 -7 z" fill="{MUTED}"/>')

    def checkbox(self, x, y, label, checked=False, size=15):
        self.rect(x, y, 18, 18, fill=WHITE, stroke=LINE2, rx=3, sw=1.5)
        if checked:
            self.ops.append(f'<path d="M{x + 4} {y + 9} l4 4 l7 -8" stroke="#1E6B3A" stroke-width="2.5" fill="none"/>')
        self.text(x + 28, y + 14, label, size, False, TXT)

    def tabs(self, name, x, y, labels, active=None, h=34, size=15, pad=18):
        """labels: list of (key, text). Registers name.<key>."""
        cx = x
        self.line(x, y + h, x + 730, y + h, LINE2, 1.5)
        for key, lab in labels:
            w = tw(lab, size, key == active) + pad * 2
            on = key == active
            self.rect(cx, y, w, h, fill=WHITE if on else NAVBG, stroke=LINE2, rx=5 if on else 0, sw=1.5, name=f'{name}.{key}')
            if on:
                self.ops.append(f'<rect x="{cx + 1}" y="{y + h - 2}" width="{w - 2}" height="4" fill="{WHITE}"/>')
            self.text(cx + w / 2, y + h / 2 + size * 0.35, lab, size, on, TXT if on else MUTED, 'middle', italic=True)
            cx += w + 2
        return cx

    def table(self, name, x, y, cols, rows, row_h=34, head_h=32, sel=None, size=14):
        """cols: [(header, width)]. rows: list of rows; a cell is a string or ('chip', text, kind)."""
        tw_ = sum(c[1] for c in cols)
        self.rect(x, y, tw_, head_h + row_h * len(rows), fill=WHITE, stroke=LINE2, sw=1.5, name=name)
        self.rect(x, y, tw_, head_h, fill=HDR, stroke=LINE2, sw=1.5)
        cx = x
        for j, (hd, cw) in enumerate(cols):
            self.text(cx + 10, y + head_h / 2 + 5, hd, 13, True, MUTED, italic=True)
            self.reg(f'{name}.c{j}', cx, y, cw, head_h + row_h * len(rows))
            cx += cw
        for i, row in enumerate(rows):
            ry = y + head_h + i * row_h
            if sel is not None and i in (sel if isinstance(sel, (list, tuple, set)) else [sel]):
                self.rect(x + 1, ry, tw_ - 2, row_h, fill='#EAF1FF', stroke='none')
            self.line(x, ry, x + tw_, ry, LINE, 1)
            self.reg(f'{name}.r{i}', x, ry, tw_, row_h)
            cx = x
            for j, cell in enumerate(row):
                cw = cols[j][1]
                if isinstance(cell, tuple) and cell[0] == 'chip':
                    self.chip(cx + 10, ry + row_h / 2 - (size + 9) / 2 + 1, cell[1], cell[2], size - 1)
                elif isinstance(cell, tuple) and cell[0] == 'btn':
                    bw = tw(cell[1], size - 1, True) + 20
                    self.rect(cx + 10, ry + 5, bw, row_h - 10, fill=BTN, stroke='#8492A8', rx=5, name=f'{name}.r{i}b')
                    self.text(cx + 10 + bw / 2, ry + row_h / 2 + 5, cell[1], size - 1, True, TXT, 'middle')
                else:
                    self.text(cx + 10, ry + row_h / 2 + 5, str(cell), size, False, TXT)
                self.reg(f'{name}.r{i}c{j}', cx, ry, cw, row_h)
                cx += cw

    def paper(self, x, y, w, h, name=None):
        self.rect(x + 4, y + 5, w, h, fill='#C9D0DB', stroke='none', rx=2, op=0.6)
        self.rect(x, y, w, h, fill=WHITE, stroke=LINE2, sw=1.5, name=name)

    # ------------------------------------------------------------------ frames
    def chrome(self, url='[ Zenith\'s Alora web address ]'):
        self.rect(0, 0, W, RIBBON_Y, fill=WHITE, stroke='#8A96A8', sw=2)
        self.rect(1, 1, W - 2, 33, fill=CHROME, stroke='none')
        for i, c in enumerate(['#E08A8A', '#E6C36A', '#8CC79B']):
            self.ops.append(f'<circle cx="{18 + i * 18}" cy="17" r="5.5" fill="{c}"/>')
        self.rect(84, 5, 560, 24, fill=WHITE, stroke=LINE2, rx=12, name='addr')
        self.text(100, 22, url, 14, False, MUTED, italic=True)

    def shell(self, active=None, user='[ your name ]', search=True, searchtext='Search'):
        """Header, left menu. Returns (content_x, content_y)."""
        self.rect(1, 34, W - 2, 44, fill=HDR, stroke='none')
        self.line(1, 78, W - 1, 78, LINE2, 1.5)
        self.text(18, 62, '[ logo ]', 15, False, '#9AA5B5', italic=True)
        if search:
            self.rect(200, 42, 320, 28, fill=WHITE, stroke=LINE2, rx=14, sw=1.5, name='search')
            self.ops.append(f'<circle cx="220" cy="55" r="6" fill="none" stroke="{MUTED}" stroke-width="2"/><line x1="225" y1="60" x2="231" y2="66" stroke="{MUTED}" stroke-width="2"/>')
            self.text(242, 61, searchtext, 14, False, MUTED, italic=True)
        self.ops.append(f'<circle cx="{W - 150}" cy="56" r="12" fill="#D5DBE5"/>')
        self.text(W - 130, 62, user, 14, True, TXT, name='user')
        self.rect(1, 79, 150, RIBBON_Y - 80, fill=NAVBG, stroke='none')
        self.line(150, 79, 150, RIBBON_Y, LINE2, 1.5)
        for i, (k, lab) in enumerate(NAV_ITEMS):
            y = 92 + i * 38
            on = k == active
            if on:
                self.rect(8, y, 134, 32, fill=SEL, stroke='#B6C3DA', rx=6, sw=1.5, name=f'nav.{k}')
            else:
                self.reg(f'nav.{k}', 8, y, 134, 32)
            self.text(20, y + 22, lab, 15, on, TXT if on else MUTED, italic=True)
        self.reg('nav', 8, 92, 134, 38 * len(NAV_ITEMS))
        return 150, 78

    def ribbon(self, extra=None):
        self.rect(1, RIBBON_Y, W - 2, H - RIBBON_Y - 1, fill='#FFF6DC', stroke='none')
        self.line(1, RIBBON_Y, W - 1, RIBBON_Y, '#D79A00', 2)
        self.text(14, RIBBON_Y + 17, 'TRAINING MOCKUP. NOT AN ALORA SCREENSHOT.', 13, True, '#7A4A00')
        self.text(W - 14, RIBBON_Y + 17, extra or 'Gray italic words describe an area. They are not Alora menu names.', 12.5, False, '#7A4A00', 'end')

    def dim(self):
        """Dim everything drawn so far (used behind dialogs)."""
        self.rect(1, 35, W - 2, RIBBON_Y - 36, fill='#0F172A', stroke='none', op=0.38)

    # ------------------------------------------------------------------ callouts
    def call(self, n, target, label, at, key=None, status=None, pad=5, size=16, arrow=True, hl=True):
        """Add a numbered callout.
        target: name registered on this mock, or (x, y, w, h).
        at: (x, y) top left of the label pill, or one of 'above','below','left','right'.
        key: ui registry key used for status. key='zenith' draws a ZENITH chip, None draws no chip.
        """
        self.calls.append(dict(n=n, target=target, label=label, at=at, key=key, status=status, pad=pad, size=size, arrow=arrow, hl=hl))

    def _target(self, t):
        if isinstance(t, tuple):
            return t
        if t not in self.T:
            raise KeyError(f'unknown target {t!r}; have {sorted(self.T)[:40]}')
        return self.T[t]

    def _render_calls(self):
        hls, arrs, pills = [], [], []
        defs = (f'<defs><marker id="ah{self.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0 0 L10 5 L0 10 z" fill="{RED}"/></marker></defs>')
        for c in self.calls:
            tx, ty, tww, thh = self._target(c['target'])
            p = min(c['pad'], 2) if getattr(self, 'tight', False) else c['pad']
            hx, hy, hw, hh = tx - p, ty - p, tww + 2 * p, thh + 2 * p
            st = c['status'] or (ui.status(c['key']) if c['key'] else None)
            chip = CHIPS.get(st) if st else None
            lab = ui.label(c['key'], c['label']) if c['key'] else c['label']
            size = c['size']
            lw = tw(lab, size, True)
            cw = (tw(chip[0], 11, True) + 14) if chip else 0
            pw = max(40 + lw + 12, (cw + 34) if chip else 0)
            ph = 34
            at = c['at']
            dx = dy = 0
            if isinstance(at, tuple) and isinstance(at[0], str):
                at, dx, dy = at[0], at[1], at[2]
            if isinstance(at, str):
                if at == 'above':
                    px, py = hx, hy - ph - 28
                elif at == 'below':
                    px, py = hx, hy + hh + 28
                elif at == 'left':
                    px, py = hx - pw - 34, hy + hh / 2 - ph / 2
                elif at == 'right':
                    px, py = hx + hw + 34, hy + hh / 2 - ph / 2
                elif at == 'belowright':
                    px, py = hx + hw - pw, hy + hh + 28
                elif at == 'aboveright':
                    px, py = hx + hw - pw, hy - ph - 28
                else:
                    raise ValueError(at)
                px += dx
                py += dy
            else:
                px, py = at
            px = max(6, min(px, W - pw - 6))
            py = max(6, min(py, RIBBON_Y - ph - 14))
            if c['hl']:
                hls.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="5" fill="{RED}" fill-opacity="0.09" stroke="{RED}" stroke-width="3.5"/>')
            if c['arrow']:
                pcx, pcy = px + pw / 2, py + ph / 2
                cands = [(px + pw, pcy), (px, pcy), (pcx, py), (pcx, py + ph)]
                tcx, tcy = hx + hw / 2, hy + hh / 2
                sx, sy = min(cands, key=lambda q: (q[0] - tcx) ** 2 + (q[1] - tcy) ** 2)
                ex = min(max(sx, hx), hx + hw)
                ey = min(max(sy, hy), hy + hh)
                if abs(ex - sx) + abs(ey - sy) > 6:
                    arrs.append(f'<line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" stroke="{RED}" stroke-width="3.5" marker-end="url(#ah{self.id})"/>')
            g = [f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="17" fill="#FFFFFF" stroke="{RED}" stroke-width="2.5"/>',
                 f'<circle cx="{px + 17}" cy="{py + 17}" r="14.5" fill="{RED}"/>',
                 f'<text x="{px + 17}" y="{py + 23}" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">{c["n"]}</text>',
                 f'<text x="{px + 40}" y="{py + 22.5}" font-size="{size}" font-weight="700" fill="{NAVY}">{esc(lab)}</text>']
            if chip:
                cx = px + pw - cw - 8
                cy = py + ph - 5
                dash = ' stroke-dasharray="3 2"' if chip[4] else ''
                g.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="17" rx="8.5" fill="{chip[1]}" stroke="{chip[3]}" stroke-width="1.5"{dash}/>')
                g.append(f'<text x="{cx + cw / 2}" y="{cy + 12.5}" font-size="11" font-weight="700" fill="{chip[2]}" text-anchor="middle">{chip[0]}</text>')
            pills.append(''.join(g))
        return defs + ''.join(hls) + ''.join(arrs) + ''.join(pills)

    # ------------------------------------------------------------------ output
    def svg(self):
        if not getattr(self, '_rib', False):
            self.ribbon(getattr(self, 'rib_extra', None))
            self._rib = True
        body = ''.join(self.ops) + self._render_calls()
        return (f'<svg class="mock" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(self.alt)}" '
                f'font-family=\'{FONT}\' xmlns="http://www.w3.org/2000/svg">{body}</svg>')

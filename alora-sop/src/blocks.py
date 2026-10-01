"""Small HTML helpers used by the content modules."""
from model import md


def _m(s):
    return s if isinstance(s, str) and s.lstrip().startswith('<') else md(s)


def H(text):
    return f'<h3>{md(text)}</h3>'


def H5(text):
    return f'<h5>{md(text)}</h5>'


def P(text):
    return f'<p>{_m(text)}</p>'


def UL(items):
    return '<ul>' + ''.join(f'<li>{_m(i)}</li>' for i in items) + '</ul>'


def OL(items):
    return '<ol>' + ''.join(f'<li>{_m(i)}</li>' for i in items) + '</ol>'


def CHECKS(items, big=False):
    cls = 'checks big' if big else 'checks'
    return f'<ul class="{cls}">' + ''.join(f'<li>{_m(i)}</li>' for i in items) + '</ul>'


def TABLE(headers, rows, cls='', widths=None):
    th = ''.join(f'<th{(" style=width:" + widths[i]) if widths else ""}>{md(h)}</th>' for i, h in enumerate(headers))
    body = ''.join('<tr>' + ''.join(f'<td>{_m(c)}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="t {cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


def KBOX(title, body, cls=''):
    return f'<div class="kbox {cls}"><h6>{md(title)}</h6>{body if body.lstrip().startswith("<") else P(body)}</div>'


def GRID2(a, b):
    return f'<div class="grid2"><div>{a}</div><div>{b}</div></div>'


def GRID3(a, b, c):
    return f'<div class="grid3"><div>{a}</div><div>{b}</div><div>{c}</div></div>'


def BLANKS(n=3, label=''):
    return ''.join(f'<p>{md(label)}<span class="blank" style="min-width:4.6in"></span></p>' for _ in range(n))


def SIGN(fields):
    return '<div class="sign">' + ''.join(f'<div><div class="ln"></div><small>{md(f)}</small></div>' for f in fields) + '</div>'

"""Data model for the manual. Content modules build these objects; build.py lays them out."""
import re


class Step:
    def __init__(self, id, title, mock, do, enter=None, check=None, expect='', see='', donot=None,
                 alora='', zenith='', rule='', ifwrong='', stop=None, key_note='', astatus=None, label=None):
        self.id = id
        self.title = title
        self.mock = mock          # callable returning a mock.Mock with callouts
        self.do = do              # one line per numbered callout
        self.enter = enter
        self.check = check or []
        self.expect = expect
        self.see = see
        self.donot = donot or []
        self.alora = alora
        self.zenith = zenith
        self.rule = rule
        self.ifwrong = ifwrong
        self.stop = stop or []
        self.key_note = key_note
        self.astatus = astatus    # optional override: FEATURE, WINDOWS, ZENITH
        self.label = label        # optional step label such as 3A


class Proc:
    def __init__(self, id, tab, num, title, purpose, before, steps, final, stop, donot=None, who='', time='', extra=None):
        self.id = id
        self.tab = tab
        self.num = num            # label such as P3 or SOC 5
        self.title = title
        self.purpose = purpose
        self.before = before
        self.steps = steps
        self.final = final
        self.stop = stop
        self.donot = donot or []
        self.who = who
        self.time = time
        self.extra = extra        # optional extra html for the start page


class Text:
    """A plain page (or several): html body is already laid out by the content module."""
    def __init__(self, id, tab, title, html, kind='text', wide=False, toc=False):
        self.id = id
        self.tab = tab
        self.title = title
        self.html = html          # a string, or a function returning a string (built after all pages exist)
        self.kind = kind
        self.wide = wide
        self.toc = toc            # list this page in the Contents


class Divider:
    def __init__(self, tab, blurb, items):
        self.tab = tab
        self.blurb = blurb
        self.items = items        # list of (proc_id, label)


def md(s):
    """Tiny markup: **bold**, *italic*, [[VERIFY]] chip, [[ZENITH]] chip."""
    if s is None:
        return ''
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*(.+?)\*(?![\w*])', r'<i>\1</i>', s)
    s = re.sub(r'(?<=\w)_(?=\w)', '_\u200b', s)   # let long file names break at the underscores
    s = s.replace('[[VERIFY]]', '<span class="chip verify">VERIFY IN LIVE ALORA</span>')
    s = s.replace('[[FEATURE]]', '<span class="chip feature">ALORA FEATURE</span>')
    s = s.replace('[[ZENITH]]', '<span class="chip zenith">ZENITH STANDARD</span>')
    s = re.sub(r'\{\{pg:([\w\-]+)\}\}', r'<span class="pgref" data-pg="\1">p.?</span>', s)
    return s

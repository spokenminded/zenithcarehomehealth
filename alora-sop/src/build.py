#!/usr/bin/env python3
"""Build the Zenith Alora Office Operating Manual (HTML website version and print-ready page layout).

    python3 build.py ../zenith-alora-office-sop.html

The PDF is produced from the HTML with build_pdf.js (Chromium). Both contain the same pages.
"""
import base64
import html as _h
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import ui
from model import Proc, Text, Divider, md

HERE = Path(__file__).parent

EDITION = 'Version 2.0 DRAFT'
EDITION_DATE = 'September 2026'
DOC_NO = 'ZCHH-SOP-ALORA-OFFICE-001'

TABS = {
    1: ('Start Here', 'START'),
    2: ('Sign In and Navigate', 'SIGN IN'),
    3: ('Patient Records', 'PATIENTS'),
    4: ('Documents and Orders', 'DOCUMENTS'),
    5: ('Start of Care (SOC) Workflow', 'SOC'),
    6: ('Scheduling', 'SCHEDULE'),
    7: ('Monitoring and Review', 'MONITOR'),
    8: ('Billing and NOA', 'BILLING'),
    9: ('Daily, Weekly and Monthly Checks', 'ROUTINES'),
    10: ('Problems and Approvals', 'PROBLEMS'),
    11: ('Forms and Quick Cards', 'FORMS'),
}


def esc(s):
    return _h.escape(str(s), quote=True)


def tabmarks(cur):
    return '<div class="tabs" aria-hidden="true">' + ''.join(
        f'<span class="{"on" if t == cur else ""}">{t} {TABS[t][1]}</span>' for t in TABS) + '</div>'


def wrap(spec, pageno, inner, cls='', hdr=True, foot=True, tabs=True):
    tab = spec['tab']
    head = ''
    if hdr:
        head = (f'<header class="ph"><span class="tabn">Tab {tab} · {esc(TABS[tab][0])}</span>'
                f'<span class="pn">{esc(spec.get("hpn", ""))}</span><span class="sn">{esc(spec.get("hsn", ""))}</span></header>')
    foot_html = ''
    if foot:
        foot_html = (f'<footer class="pf"><span>Zenith Care Home Health, LLC · Alora Office Operating Manual · {EDITION} · '
                     f'{DOC_NO} · Uncontrolled when printed</span><span class="pg">Page {pageno}</span></footer>')
    return (f'<section class="page {cls}" id="p-{spec["id"]}" data-tab="{tab}" data-title="{esc(spec.get("nav", spec.get("title", "")))}">'
            f'{head}{inner}{foot_html}{tabmarks(tab) if tabs else ""}</section>')


# =============================================================================== step and procedure pages
def chips_for_step(step, m):
    """Summarize how much of this page is confirmed."""
    keys = [c['key'] for c in m.calls if c['key']]
    sts = [ui.status(k) for k in keys]
    if 'VERIFY' in sts or 'FEATURE' in sts:
        return 'VERIFY'
    if sts and all(s in ('WINDOWS', 'VERIFIED') for s in sts):
        return 'OK'
    return 'ZENITH' if not sts else 'OK'


def render_step(proc, step, idx, total):
    def build(pageno):
        m = step.mock()
        if len(step.do) != len(m.calls):
            raise SystemExit(f'step {step.id}: {len(step.do)} instructions but {len(m.calls)} callouts')
        svg = m.svg()
        keys = [c['key'] for c in m.calls if c['key']]
        sts = set(ui.status(k) for k in keys)
        do_items = ''.join(f'<li><span class="c">{i + 1}</span>{md(t)}</li>' for i, t in enumerate(step.do))
        rows = []
        rows.append(('ENTER', md(step.enter) if step.enter else 'Nothing to type on this step.', ''))
        if step.check:
            rows.append(('CHECK', '<ul style="padding-left:.16in;margin:0">' + ''.join(f'<li>{md(c)}</li>' for c in step.check) + '</ul>', ''))
        rows.append(('EXPECTED RESULT', md(step.expect), 'exp'))
        dl = '<dl class="rows">' + ''.join(f'<dt class="{c}">{k}</dt><dd>{v}</dd>' for k, v, c in rows) + '</dl>'
        left = f'<div class="box do"><h4>Do these in order (follow the red numbers)</h4><ol class="do">{do_items}</ol></div>{dl}'
        right = f'<div class="box see"><h4>What you should see</h4><p>{md(step.see)}</p></div>'
        if step.donot:
            right += '<div class="box dont"><h4>Do not do this</h4><ul>' + ''.join(f'<li>{md(d)}</li>' for d in step.donot) + '</ul></div>'
        stop = step.stop
        if step.ifwrong or stop:
            body = ''
            if step.ifwrong:
                body += f'<p>{md(step.ifwrong)}</p>'
            if stop:
                body += '<ul>' + ''.join(f'<li>{md(s)}</li>' for s in stop) + '</ul>'
            right += f'<div class="box stop"><h4>If it does not look right: stop</h4>{body}</div>'
        if step.key_note:
            right += f'<div class="box note"><h4>Note</h4><p>{md(step.key_note)}</p></div>'
        # Alora action vs Zenith standard
        if step.astatus == 'FEATURE':
            chip = '<span class="chip feature">ALORA FEATURE DOCUMENTED</span> <span class="chip verify">SCREEN NAMES: VERIFY</span>'
        elif step.astatus == 'ZENITH':
            chip = '<span class="chip zenith">ZENITH PROCESS</span>'
        elif 'VERIFY' in sts:
            chip = '<span class="chip verify">VERIFY IN LIVE ALORA</span>'
        elif 'FEATURE' in sts:
            chip = '<span class="chip feature">ALORA FEATURE DOCUMENTED</span> <span class="chip verify">CLICK PATH: VERIFY</span>'
        elif sts and sts <= {'WINDOWS'}:
            chip = '<span class="chip windows">WINDOWS</span>'
        elif sts <= {'VERIFIED'} and sts:
            chip = '<span class="chip verified">VERIFIED</span>'
        else:
            chip = '<span class="chip zenith">ZENITH PROCESS</span>'
        alora = ''
        if step.alora:
            alora = f'<div><b class="lab">Alora action {chip}</b>{md(step.alora)}</div>'
        zen = f'<div class="zen"><b class="lab">Zenith standard</b>{md(step.zenith)}</div>' if step.zenith else ''
        std = f'<div class="stdrow">{alora}{zen}</div>' if (alora or zen) else ''
        rule = f'<div class="rulebar"><span class="chip law">FEDERAL RULE</span> {md(step.rule)}</div>' if step.rule else ''
        needs_live = bool(sts & {'VERIFY', 'FEATURE'})
        real = next((p for p in sorted((HERE / 'screens').glob(f'{step.id}.*')) if p.suffix.lower() in ('.png', '.jpg', '.jpeg')), None)
        if real:
            needs_live = False
            uri = f'data:image/{"jpeg" if real.suffix.lower() != ".png" else "png"};base64,' + base64.b64encode(real.read_bytes()).decode()
            svg = (f'<img class="real" src="{uri}" alt="Annotated screenshot of live Alora for step {esc(step.title)}">'
                   '<figcaption>ANNOTATED SCREENSHOT from Zenith\'s live Alora. Numbers and boxes were added by Zenith.</figcaption>')
            chip = '<span class="chip verified">FROM LIVE ALORA</span>'
            alora = f'<div><b class="lab">Alora action {chip}</b>{md(step.alora)}</div>' if step.alora else ''
            std = f'<div class="stdrow">{alora}{zen}</div>' if (alora or zen) else ''
        live = ''
        if needs_live:
            live = ('<div class="livecheck"><span><b>LIVE ALORA CHECK</b> (Administrator): names and places match live Alora.</span>'
                    '<span><span class="cb"></span>Yes &nbsp; Initials <span class="blank"></span> Date <span class="blank"></span></span></div>')
        inner = (f'<div class="stitle"><span class="sn">Step {step.label or idx}</span><h2>{md(step.title)}</h2></div>'
                 f'<figure class="shot">{svg}</figure>'
                 f'<div class="cols"><div>{left}</div><div>{right}</div></div>{std}{rule}{live}')
        spec = dict(id=step.id, tab=proc.tab, hpn=f'{proc.num} · {proc.title}', hsn=f'Step {step.label or idx}' + ('' if step.label else f' of {total}'))
        return wrap(spec, pageno, inner, cls='step')
    return dict(id=step.id, tab=proc.tab, kind='step', html=build, nav=f'{proc.num} step {step.label or idx}: {step.title}', proc=proc.id)


def render_proc_start(proc):
    def build(pageno):
        steps = ''.join(
            f'<li><span class="n">{md(s.label) if s.label else i}</span><span class="t">{md(s.title)}</span><span class="p">{{{{pg:{s.id}}}}}</span></li>'
            for i, s in enumerate(proc.steps, 1))
        before = ''.join(f'<li>{md(b)}</li>' for b in proc.before)
        meta = ''
        if proc.who or proc.time:
            meta = ('<div class="kbox gold"><h6>Who and how long</h6>'
                    + (f'<p><b>Who:</b> {md(proc.who)}</p>' if proc.who else '')
                    + (f'<p><b>Time:</b> {md(proc.time)}</p>' if proc.time else '') + '</div>')
        method = ('<div class="method"><div>SEE IT<small>match the picture</small><span class="arr">›</span></div>'
                  '<div>CLICK IT<small>follow the red numbers</small><span class="arr">›</span></div>'
                  '<div>ENTER IT<small>type only what is asked</small><span class="arr">›</span></div>'
                  '<div>SAVE IT<small>one click, then wait</small><span class="arr">›</span></div>'
                  '<div>VERIFY IT<small>check the result</small></div></div>')
        inner = (f'<div class="pstart"><div class="ptag">Tab {proc.tab} · Procedure {md(proc.num)}</div><h1>{md(proc.title)}</h1>'
                 f'<h3>Purpose</h3><p>{md(proc.purpose)}</p>'
                 f'<div class="grid2"><div><h3>Before you start</h3><ul class="checks">{before}</ul>{meta}</div>'
                 f'<div><h3>Steps in this procedure</h3><ol class="steplist">{steps}</ol></div></div>'
                 f'{proc.extra or ""}{method}</div>')
        spec = dict(id=proc.id, tab=proc.tab, hpn=f'{proc.num} · {proc.title}', hsn='Start')
        return wrap(spec, pageno, inner, cls='pstart')
    return dict(id=proc.id, tab=proc.tab, kind='pstart', html=build, nav=f'{proc.num} {proc.title}', proc=proc.id, toc=True, label=f'{proc.num}  {proc.title}')


def render_proc_end(proc):
    def build(pageno):
        final = ''.join(f'<li>{md(f)}</li>' for f in proc.final)
        stop = ''.join(f'<li>{md(s)}</li>' for s in proc.stop)
        donot = ''
        if proc.donot:
            donot = ('<div class="kbox red"><h6>Do not do this (common mistakes)</h6><ul>'
                     + ''.join(f'<li>{md(d)}</li>' for d in proc.donot) + '</ul></div>')
        every = ('<div class="kbox"><h6>Every procedure: final check (write N/A when it does not apply)</h6><ul class="checks fivecol">'
                 '<li>Task completed</li><li>Information saved</li><li>Correct patient</li><li>Correct documents</li><li>No errors</li></ul></div>')
        inner = (f'<div class="pstart"><div class="ptag">Procedure {md(proc.num)} · Finish</div><h1>{md(proc.title)}</h1>'
                 f'<h3>Final verification</h3><ul class="checks big">{final}</ul>{every}'
                 f'<div class="kbox red" style="border-width:2px"><h6>Stop and ask the Administrator or DON if</h6><ul>{stop}</ul></div>'
                 f'{donot}'
                 '<h5>Notes (what happened, who you told, the time)</h5>'
                 + '<p class="blank wide"></p>' * 3
                 + '<div class="sign"><div><div class="ln"></div><small>Employee initials and date</small></div>'
                   '<div><div class="ln"></div><small>Reviewed by (when required)</small></div></div></div>')
        spec = dict(id=f'{proc.id}-end', tab=proc.tab, hpn=f'{proc.num} · {proc.title}', hsn='Finish')
        return wrap(spec, pageno, inner, cls='pstart')
    return dict(id=f'{proc.id}-end', tab=proc.tab, kind='pend', html=build, nav=f'{proc.num} final verification', proc=proc.id)


def expand_proc(proc):
    out = [render_proc_start(proc)]
    n = len(proc.steps)
    for i, s in enumerate(proc.steps, 1):
        out.append(render_step(proc, s, i, n))
    out.append(render_proc_end(proc))
    return out


# =============================================================================== other page kinds
def render_text(t):
    def build(pageno):
        inner = t.html() if callable(t.html) else t.html
        spec = dict(id=t.id, tab=t.tab, hpn=t.title, hsn='')
        return wrap(spec, pageno, inner, cls=t.kind, hdr=t.kind not in ('qcard', 'cover'), foot=t.kind != 'cover', tabs=t.kind != 'cover')
    return dict(id=t.id, tab=t.tab, kind=t.kind, html=build, nav=t.title, toc=t.toc, label=t.title)


def render_divider(d):
    def build(pageno):
        name, short = TABS[d.tab]
        items = ''.join(f'<li><span class="t">{md(label)}</span><span class="p">{{{{pg:{pid}}}}}</span></li>' for pid, label in d.items)
        inner = (f'<div class="dband"><div class="tn">{d.tab}</div><h1>{esc(name)}</h1><p>{md(d.blurb)}</p></div>'
                 f'<div class="dlow"><h3 style="font:700 11pt Arial;color:#1B2B4B;border-bottom:1.5px solid #D4AF62;padding-bottom:2px;margin:0 0 6px">In this tab</h3>'
                 f'<ol class="steplist" style="list-style:none">{items}</ol>'
                 f'<h5 style="font:700 9pt Arial;letter-spacing:.07em;text-transform:uppercase;color:#B8892F;margin:16px 0 3px">Notes</h5>'
                 + ''.join('<p style="border-bottom:1px solid #D5DBE5;height:.3in;margin:0"></p>' for _ in range(6)) + '</div>')
        spec = dict(id=f'tab{d.tab}', tab=d.tab, hpn='', hsn='')
        return wrap(spec, pageno, inner, cls='divider', hdr=False)
    return dict(id=f'tab{d.tab}', tab=d.tab, kind='divider', html=build, nav=f'Tab {d.tab} divider', toc=True, label=f'TAB {d.tab}  {TABS[d.tab][0].upper()}')


# =============================================================================== assemble
PROCS_ALL = []


def load_pages():
    import importlib
    specs = []
    for modname in ['c1_front', 'c2_signin', 'c3_patients', 'c4_documents', 'c5_soc', 'c6_schedule', 'c7_monitor',
                    'c8_billing', 'c9_routines', 'c10_problems', 'c11_forms']:
        try:
            mod = importlib.import_module('content.' + modname)
        except ModuleNotFoundError as e:
            if e.name == 'content.' + modname:
                print('skip (not written yet):', modname)
                continue
            raise
        for p in mod.PAGES:
            if isinstance(p, Proc):
                PROCS_ALL.append(p)
                specs.extend(expand_proc(p))
            elif isinstance(p, Divider):
                specs.append(render_divider(p))
            elif isinstance(p, Text):
                specs.append(render_text(p))
            else:
                raise TypeError(type(p))
    return specs


TOC_ID = 'toc'
TOC_PER = 38   # rows on one contents page


def toc_html(specs, pagemap, part, pages):
    rows = []
    cur_tab = None
    for s in specs:
        if s['kind'] == 'divider':
            rows.append(f'<tr class="tabrow"><td colspan="2">TAB {s["tab"]} · {esc(TABS[s["tab"]][0])}</td><td class="r">{pagemap[s["id"]]}</td></tr>')
        elif s.get('toc') and s['kind'] == 'pstart':
            rows.append(f'<tr><td class="lab" colspan="2"><a href="#p-{s["id"]}">{md(s["label"])}</a></td><td class="r">{pagemap[s["id"]]}</td></tr>')
        elif s.get('toc'):
            rows.append(f'<tr><td class="lab" colspan="2"><a href="#p-{s["id"]}">{md(s["label"])}</a></td><td class="r">{pagemap[s["id"]]}</td></tr>')
    chunk = rows[part * TOC_PER:(part + 1) * TOC_PER]
    return (f'<h1 class="ttl">{"Contents" if part == 0 else "Contents (continued)"}</h1><p class="sub">Page numbers match the number printed at the bottom of each page.</p>'
            '<table class="t tight toc"><tbody>' + ''.join(chunk) + '</tbody></table>')


def build(out_path):
    specs = load_pages()
    # reserve TOC pages after the first ones: cover (1) + document control (2) then contents
    # order: cover, doc control, toc pages..., rest
    head = [s for s in specs if s['id'] in ('cover', 'doccontrol')]
    rest = [s for s in specs if s['id'] not in ('cover', 'doccontrol')]
    n_rows = sum(1 for s in specs if s['kind'] == 'divider' or s.get('toc'))
    TOC_PAGES = max(1, -(-n_rows // TOC_PER))
    toc_specs = [dict(id=f'{TOC_ID}{i + 1}', tab=1, kind='toc', nav=f'Contents ({i + 1} of {TOC_PAGES})', part=i) for i in range(TOC_PAGES)]
    ordered = head + toc_specs + rest
    pagemap = {s['id']: i + 1 for i, s in enumerate(ordered)}
    total = len(ordered)
    htmls = []
    for i, s in enumerate(ordered):
        pageno = i + 1
        if s['kind'] == 'toc':
            inner = toc_html(specs, pagemap, s['part'], TOC_PAGES)
            sp = dict(id=s['id'], tab=1, hpn='Contents', hsn=f'{s["part"] + 1} of {TOC_PAGES}')
            page = wrap(sp, pageno, inner, cls='text')
        else:
            page = s['html'](pageno)
        htmls.append(page)
    body = '\n'.join(htmls)

    def pgsub(m):
        pid = m.group(1)
        if pid not in pagemap:
            raise KeyError(f'page reference to unknown id {pid!r}')
        return f'p.&nbsp;{pagemap[pid]}'
    missing = set()

    def pgnum(pid):
        if pid not in pagemap:
            missing.add(pid)
            return '?'
        return pagemap[pid]
    body = re.sub(r'<span class="pgref" data-pg="([\w\-]+)">p\.\?</span>', lambda m: f'<span class="pgref">p.&nbsp;{pgnum(m.group(1))}</span>', body)
    body = re.sub(r'\{\{pg:([\w\-]+)\}\}', lambda m: f'p.&nbsp;{pgnum(m.group(1))}', body)
    if missing:
        print('WARNING unresolved page references:', sorted(missing))
        if '--strict' in sys.argv:
            raise SystemExit(1)

    # sidebar
    groups = {}
    for s in ordered:
        if s['kind'] == 'toc' or s['kind'] in ('step', 'pend'):
            continue
        groups.setdefault(s['tab'], []).append(s)
    side = ['<nav class="side" id="side"><div class="brand"><img src="{logo}" alt="Zenith Care Home Health"><div><b>Alora Office<br>Operating Manual</b><small>' + EDITION + '</small></div></div>',
            '<input id="q" type="search" placeholder="Search procedures and steps" aria-label="Search">']
    for t in TABS:
        items = [s for s in ordered if s['tab'] == t and s['kind'] in ('pstart', 'text', 'form', 'qcard', 'divider') and s['kind'] != 'toc']
        links = ''.join(f'<a href="#p-{s["id"]}" data-t="{esc(s.get("nav", ""))}">{esc(s.get("nav", s["id"]))}</a>' for s in items if s['kind'] != 'divider')
        steps = ''.join(f'<a class="st" href="#p-{s["id"]}" data-t="{esc(s.get("nav", ""))}" style="padding-left:30px;font-size:8.4pt">{esc(s.get("nav", ""))}</a>'
                        for s in ordered if s['tab'] == t and s['kind'] in ('step',))
        side.append(f'<details{" open" if t == 1 else ""}><summary><span>{t}</span>{esc(TABS[t][0])}</summary>{links}{steps}</details>')
    side.append('</nav>')
    logo = base64.b64encode((HERE / 'zenith-logo.png').read_bytes()).decode()
    logo_uri = f'data:image/png;base64,{logo}'
    css = (HERE / 'style.css').read_text(encoding='utf-8')
    js = (HERE / 'app.js').read_text(encoding='utf-8')
    doc = (f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1">'
           f'<title>Zenith Alora Office Operating Manual</title>'
           '<meta name="description" content="Step-by-step office operating manual for Zenith Care Home Health staff using the Alora website on a desktop computer.">'
           f'<style>\n{css}\n</style></head><body>'
           '<div class="topbar"><button id="open" type="button">Contents</button><b>Alora Office Operating Manual</b></div>'
           '<div class="site">' + ''.join(side).replace('{logo}', logo_uri) +
           f'<main class="pages">{body.replace("{logo}", logo_uri)}</main></div>'
           f'<script>\n{js}\n</script></body></html>\n')
    Path(out_path).write_text(doc, encoding='utf-8')
    # list of steps that show a live Alora screen, for capturing real screenshots
    import csv
    rows = []
    for p in PROCS_ALL:
        for s in p.steps:
            m = s.mock()
            els = [ui.REG[c['key']][0] for c in m.calls if c['key'] and c['key'] != 'zenith' and ui.status(c['key']) in ('VERIFY', 'FEATURE')]
            if els:
                has = any((HERE / 'screens').glob(f'{s.id}.*'))
                rows.append([s.id, pagemap.get(s.id, ''), p.num, p.title, s.title, '; '.join(els), 'yes' if has else 'no'])
    with open(Path(out_path).with_name('screens-needed.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['step_id', 'page', 'procedure', 'procedure_title', 'step_title', 'alora_elements_shown', 'real_screenshot_present'])
        w.writerows(rows)
    print(f'built {out_path}: {total} pages, {len(doc) / 1024:.0f} KB; {len(rows)} steps show a live Alora screen')
    return total


if __name__ == '__main__':
    build(sys.argv[1])

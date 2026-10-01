#!/usr/bin/env python3
"""Build the AloraPlus Training Simulator into ONE self-contained HTML file (no external requests).
usage: python3 build.py [out.html]"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / 'src'
ORDER = ['core.js', 'data.js', 'docgen.js', 'shell.js', 'patients.js', 'docs.js', 'clinical.js', 'schedule.js', 'phone.js', 'hr.js', 'billing.js', 'practice.js', 'boot.js']

def main(out):
    css = (SRC / 'style.css').read_text(encoding='utf-8')
    js = []
    for name in ORDER:
        p = SRC / name
        if p.exists():
            js.append(f'/* ===== {name} ===== */\n' + p.read_text(encoding='utf-8'))
        else:
            print('skip (not written yet):', name)
    code = '\n'.join(js)
    bad = [c for c in ('—', '–') if c in code or c in css]
    if bad:
        raise SystemExit('em or en dash found in the source')
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data: blob:; frame-src data: blob:; font-src data:; connect-src 'none'; form-action 'none'; base-uri 'none'">
<title>AloraPlus Training Simulator (practice copy)</title>
<style>
{css}
</style></head><body>
<div id="simbar"></div><div id="app"></div><div id="modal-root"></div><div id="toast-root"></div><div id="phone-root"></div><div id="drawer-root"></div>
<script>
{code}
</script></body></html>
'''
    Path(out).write_text(html, encoding='utf-8')
    print(f'built {out}: {len(html) / 1024:.0f} KB')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else str(HERE / 'alora-plus-simulator.html'))

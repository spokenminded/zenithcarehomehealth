# Zenith Alora Office Operating Manual

A step-by-step standard operating procedure for **office staff** using the **Alora website on a Windows computer**.
It is not about the mobile app and not about field clinicians.

| File | What it is |
| --- | --- |
| `zenith-alora-office-sop.pdf` | Print-ready Letter pages for the office binder (tabs, page numbers, forms, quick cards). |
| `zenith-alora-office-sop.html` | The same pages as one self-contained web page with a menu and search. Put it on the website or intranet as it is. |
| `screens-needed.csv` | Every step that shows an Alora screen, with its page number and whether a real screenshot is in place. |
| `tools/annotate.html` | Browser tool that puts red numbers, boxes and arrows on a real screenshot. Nothing is uploaded. |
| `src/` | The source the two files are built from. |
| `build.sh` | Rebuilds the HTML, the PDF and the CSV. |

## Read this first: what is and is not verified

**Nothing in this edition has been checked against Zenith's live Alora account.** Alora's own training screens are not public, so the pictures are
**training mockups**: a neutral, clearly labeled wireframe that shows the *order* of the clicks, not what Alora looks like.

Every red callout carries a tag:

* `VERIFY` : nothing public confirms this name or place.
* `ALORA FEATURE` : Alora publicly documents the feature (from its website and review sites). The exact words and place are still to verify.
* `WINDOWS` and `ZENITH FORM` : a Windows window or a paper form, not an Alora screen.
* `VERIFIED` and `FROM LIVE ALORA` : appear only after you do the steps below.

Zenith standards in the text (for example "log a referral within 15 minutes") are **drafts** until the Administrator initials them on the Standards pages.

## Close the gap in three moves

1. **Live check (about 2 hours).** The Administrator works through the *Live Alora Verification Worksheet* (Tab 11 of the binder) in live Alora and writes the real names and places.
2. **Enter the answers.** Copy `src/ui_map.example.json` to `src/ui_map.json` and set `"verified": true` and `"name"` for each item that was confirmed. Rebuild. The tags turn to `VERIFIED` and the red pills show the real names. Where a sentence in the text names a button, edit that sentence in `src/content/`.
3. **Real screenshots (best).** For each row of `screens-needed.csv`:
   1. Capture the live Alora screen (use a test patient, or black out names with the tool).
   2. Open `tools/annotate.html`, add the numbers in the same order as the numbered list on the step page, and save the PNG.
   3. Put it in `src/screens/<step id>.png` (for example `up-4.png`). Rebuild. The page then shows the screenshot and says `FROM LIVE ALORA`.

Finally the Administrator signs the *Document control* page.

## Rebuild

```bash
pip install fonttools          # measures text so the labels fit exactly
sudo apt-get install fonts-liberation   # Arial-width fonts (Linux); Arial works on Windows and macOS
npm install -g playwright && npx playwright install chromium     # or set CHROMIUM=/path/to/chrome
./build.sh
```

The build stops if a page reference is broken (`--strict`) or if any printed page overflows.

## Where things are

```
src/build.py            lays out the pages (covers, procedures, forms, contents, website frame)
src/model.py            Proc (a procedure), Step, Text, Divider
src/mock.py             the training-mockup engine (screens, red numbers, arrows, status tags)
src/scenes*.py          the screens used in the pictures
src/ui.py               the registry of every Alora screen element the manual mentions and its status
src/content/c1..c11     the text, one file per tab
src/style.css           print and website styling
```

A procedure is written like this (one `Step` per picture; one `do` line for each red number; the build checks the counts match):

```python
Step('up-4', 'Start the upload', m_up_4,
     do=['Click the **add or upload button**.', 'Look at the list: is it **already there**?'],
     enter='...', check=['...'], expect='...', see='...', donot=['...'],
     alora='What the user does in Alora.', astatus='FEATURE',
     zenith='Zenith\'s own rule.', stop=['When to stop and ask.'])
```

The paper forms in Tab 11 are printed from the same definitions as the pictures of them, so the two cannot disagree.

## House rules for edits

* Never write an Alora button, menu or box name that has not been verified. Describe it in plain words and keep the tag.
* No mobile app or phone workflows. Desktop website only.
* No em dashes or en dashes anywhere. Use plain sentences. Use "they" when a person's pronoun is unknown.
* Keep each step to one picture and one action or a small group of actions.

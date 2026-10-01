# AloraPlus Training Simulator

A working practice copy of the Alora screens and workflows in **Zenith's Alora Operating Manual** (screens captured 09/30/2026). It is one HTML file. Open `alora-plus-simulator.html` in Chrome, Edge or Firefox. No install, no internet, no account.

**It is not the real Alora.** It is not affiliated with or endorsed by Alora Healthcare Systems. It copies the screens that were photographed in the manual (names, buttons, columns, order of clicks) so staff can practice. Screens that were not photographed are marked **SIMPLIFIED PRACTICE VERSION**. Menu items the manual does not cover show "Not built in this simulator".

## No real consequence

- **No network.** A Content Security Policy blocks every outside connection. The page cannot send anything anywhere.
- **Local only.** Practice data lives in this browser (localStorage). Uploaded files stay in this browser.
- **Blocked real actions.** Faxes, Generate Claims, Electronic Claim File, invoices, Post Payment, OASIS export, CAHPS export, and Features Activation never run. Clicking them explains what the real button would do and writes it in the Coach log.
- **Made-up people.** Every patient, staff member, physician and document is fictional. Every practice document says SAMPLE DOCUMENT FOR TRAINING.
- **Reset any time.** Practice guide, About, Reset all practice data.

## How to start

1. Open `alora-plus-simulator.html`.
2. Sign in with any practice login (password for all: `practice`): `admin`, `don`, `intake`, `scheduler`, `hr`, `rn`, `hha`, `biller`.
3. Use **Practice as** at the top to switch jobs without logging out.
4. Open the **Practice guide** (top bar). It has 37 tasks that follow the manual's procedures and check themselves, the sample documents, the Coach log, and save/load of progress.
5. Use **+15 min, +1 hour, +1 day** to move the practice clock. Visits become late, conflicts appear and NOA deadlines pass.
6. Open the **CareConnect phone** to clock in and out with a GPS location choice, write notes and collect signatures.

## What works

| Manual procedure | Simulator screen |
| --- | --- |
| S1, S2 Sign in, menu | Login (two failures say STOP), Home, left menu by role, global search |
| S3, O1 to O3 Patient search, demographics, referrals | Patient Demographics (blue filter button required, Enter alone does not filter), duplicate checks, + Add with approval, Cancel then Yes, Referrals tab |
| O4 Admission, insurance | Admission tabs, insurance, diagnoses, disciplines, frequency, cert periods, GoTo panel |
| O5 to O9 Documents | Electronic Health Records with real file upload, naming check, wrong-chart coaching, General Form orders, 485, Face-To-Face window, All Documents, simple forms |
| SC1 to SC4 Scheduling, Monitor, Conflicts | Scheduler (month, week, day, cert period), Appointment Details, conflict checks, recurrence, View Frequency, Batch Entry, Global Calendar, CareConnect Monitor, EVV Conflicts with GPS review |
| H1 to H7 Human Resources | Staff list, staff record (five tabs), credentials, absences with schedule overlap, communication log, CareConnect enable, folders, user access |
| N1 to N5, AI1, AI2 Clinical | Phone clock in and out, OASIS (simplified), SN note (ten tabs, validation list, signatures), aide plan of care and notes, 485, orders |
| BI1 to BI3 Billing | Pre-Billing QA computed from the records, NOA prepare and practice submit, look-only billing screens |
| AD1 to AD4 Administrator | QA Center (approve, return), folders, EVV conflict resolution with an EVV Change Reason |
| Also | AloraMail, Reports, COVID-19 screening, Setup lists, Tools, Dashboards |

## Zenith rules built in

When a step needs approval, a coaching box says who approves and offers **Stop (recommended)** or **I have approval. Continue (practice)**. Examples: new patient, delete anything, Completed visit status, Do not validate for Time Conflict, pay rates, CareConnect before credentials are checked, QA approval by non-DON, editing a completed note. Every choice is written in the Coach log.

## Build

```
python3 build.py              # writes alora-plus-simulator.html
python3 build.py /tmp/x.html  # or choose a path
```

Sources are in `src/` (`core.js`, `data.js`, `docgen.js`, `shell.js`, `patients.js`, `docs.js`, `clinical.js`, `schedule.js`, `phone.js`, `hr.js`, `billing.js`, `practice.js`, `boot.js`, `style.css`). The build rejects em dashes and en dashes and inlines everything into one file.

## Limits

It covers every screen and workflow in the manual, **not all of Alora**. Real Alora has many more screens, fields, reports and rules than the manual photographs. Where the manual is silent the simulator makes a plain, working guess and labels it. Check anything important against the live system and the Administrator.

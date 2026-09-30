"""Tab 9: daily, weekly and monthly office checks."""
import scenes as S
import scenes2 as S2
import scenes3 as S3
import scenes4 as S4
from model import Proc, Step, Divider
from blocks import *


# ============================================================================= P23 Daily office check
def m_dl_1():
    m = S.login(filled=True)
    m.call(1, 'login_user', 'Your username', ('right', 0, 0), key='login_user')
    m.call(2, 'login_pass', 'Your password', ('right', 0, 0), key='login_pass')
    m.call(3, 'login_btn', 'Login', ('right', 0, 0), key='login_btn')
    return m


def m_dl_2():
    m = S.dashboard()
    m.call(1, 'w_pending', 'Pending items', (360, 338), key='dash_pending')
    m.call(2, 'w_noa', 'NOA box', (560, 84), key='dash_noa')
    return m


def m_dl_3():
    m = S4.live_monitor()
    m.call(1, 'lm_table', 'Today\'s visits', (200, 420), key='lm_table')
    m.call(2, 'lm_status', 'Status column', (600, 92), key='lm_status')
    return m


def m_dl_4():
    m = S4.exceptions_list()
    m.call(1, 'ex_list', 'Visits waiting for review', (200, 420), key='ex_list')
    m.call(2, 'ex_issue', 'What does not match', (600, 92), key='ex_issue')
    return m


def m_dl_5():
    m = S4.schedule_calendar()
    m.call(1, 'sch_range', 'Show: day or week', ('above', 60, 0), key='sch_range')
    m.call(2, 'sch_grid', 'Today\'s column', (430, 420), key='sch_grid')
    return m


def m_dl_6():
    m = S.explorer([('SMITH_MARY_F2F_20260915.pdf', '09/28/2026 9:16 AM', '240 KB')], path='This PC  >  Documents  >  Zenith Scans  >  Ready to upload')
    m.call(1, 'win_file', 'Only files still waiting', (300, 330), key='win_file')
    return m


def m_dl_7():
    m = S2.zform('DAILY OFFICE ALORA CHECK', [
        ('h', 'DATE AND PERSON'), ('two', 'dt', 'Date:', 'emp', 'Employee:'),
        ('h', 'EVERY MORNING'), ('check', 'd_in', 'Signed in with my own login'), ('check', 'd_pend', 'Read pending items and the NOA box'),
        ('check', 'd_exc', 'Opened the exception list'), ('check', 'd_sch', 'Looked at today\'s schedule'),
        ('h', 'MIDDAY AND END OF DAY'), ('check', 'd_lm', 'Checked the Live Monitor and called about late visits'),
        ('check', 'd_scan', 'Scan folder holds only files waiting for upload'), ('check', 'd_out', 'Logged out and locked the computer'),
        ('line', 'd_prob', 'Problems reported (what, to whom, time):')], lh=38)
    m.call(1, 'd_pend', 'Pending items and NOA', ('right', 0, 0), key='zenith')
    m.call(2, 'd_scan', 'Scan folder', ('right', 0, 0), key='zenith')
    m.call(3, 'd_out', 'Log out and lock', ('right', 0, 0), key='zenith')
    return m


DAILY = Proc(
    id='daily', tab=9, num='P23', title='Daily Office Alora Check',
    purpose='A short, fixed routine that catches problems the same day: late visits, stuck items, NOAs close to their limit, and patient files left where they should not be. '
            'Do it in the same order every day. Initial the daily sheet.',
    before=['The **Daily Office Alora Check** sheet for today (Tab 11). It is also **Quick Card 6**.', 'You know P1, P2 and P28.'],
    who='The office employee on duty.', time='About 20 minutes in the morning, 5 minutes at midday, 5 minutes at the end of the day.',
    steps=[
        Step('dl-1', 'Sign in with your own login', m_dl_1,
             do=['Type your **username**.', 'Type your **password**.', 'Click **Login**.'],
             enter='Your own username and password. Never someone else\'s.',
             check=['You are signing in on a Zenith office computer.'],
             expect='The office dashboard opens.',
             see='The dashboard with your name at the top.',
             donot=['Do not use another person\'s login, even to save time.'],
             alora='Sign in to Alora. The address and the boxes must be verified.',
             zenith='Every person has a unique login. This is a HIPAA rule.',
             stop=['The login does not work after two tries.'],
             key_note='Full procedure: **P1**, {{pg:login}}.'),
        Step('dl-2', 'Read the pending items and the NOA box', m_dl_2,
             do=['Read the numbers in the **pending items** box.', 'Read the number and the deadline in the **NOA box**.'],
             check=['You wrote the numbers on the daily sheet.', 'A number that grew since yesterday is marked.'],
             expect='You know what is waiting today.',
             see='The dashboard with pending items and the NOA box.',
             alora='Alora documents pending items and an NOA widget. Their place must be verified.', astatus='FEATURE',
             zenith='An NOA due today or past due goes to billing right away (P22).',
             stop=['An NOA is due today and not sent.'],
             key_note='See **P2**, {{pg:dashboard}}, and **P22**, {{pg:noa}}.'),
        Step('dl-3', 'Check the Live Monitor', m_dl_3,
             do=['Open the **Live Monitor** and read today\'s visits.', 'Read the **status** of each visit.'],
             check=['You called about every late visit (P17).'],
             expect='You know which visits are on time, late or missed.',
             see='A list of today\'s visits with statuses.',
             alora='Alora documents a Live Monitor. Where it is must be verified.', astatus='FEATURE',
             zenith='Check in the morning, at midday and one hour before the end of the day.',
             stop=['A start of care visit is late or missed.'],
             key_note='Full procedure: **P17**, {{pg:monitor}}.'),
        Step('dl-4', 'Open the exception list', m_dl_4,
             do=['Open the list of **visits waiting for review**.', 'Read **what does not match** for each visit.'],
             check=['You started an Exception Follow-up for each new exception (P18).'],
             expect='You know how many exceptions are waiting.',
             see='A list of visits held for review.',
             alora='Alora documents that visits can be held for manual review. The list name and place must be verified.', astatus='FEATURE',
             zenith='An exception older than 2 business days is reported to the Administrator.',
             stop=['An exception is older than 2 business days.'],
             key_note='Full procedure: **P18**, {{pg:evv}}.'),
        Step('dl-5', 'Look at today\'s schedule', m_dl_5,
             do=['Choose **day** or **week** in the show choices.', 'Read today\'s column. Every visit has a team member.'],
             check=['No visit is missing a team member.', 'No team member has two visits at once.'],
             expect='You know who goes where today.',
             see='A calendar with today\'s visits.',
             alora='Schedule views by day and week. The names of the choices must be verified.', astatus='FEATURE',
             zenith='Report a visit with no team member to the DON at once.',
             stop=['A visit has no team member.', 'Two visits overlap for one person.'],
             key_note='Full procedure: **P15**, {{pg:viewschedule}}.'),
        Step('dl-6', 'Check the scan folder', m_dl_6,
             do=['Look at the **Ready to upload** folder. Only files still waiting to be uploaded belong there.'],
             check=['Anything already uploaded and verified has been removed (P10).', 'No file is on the desktop or in Downloads.'],
             expect='The folder holds only files still waiting.',
             see='A folder with few or no files.',
             donot=['Do not delete a file that is not yet verified in Alora.'],
             alora='Not an Alora step. This is a Windows folder.', astatus='ZENITH',
             zenith='Patient files are not kept on the computer longer than needed.',
             stop=['You find a patient file on the desktop, in Downloads or on a shared drive.']),
        Step('dl-7', 'Complete the daily sheet, log out and lock', m_dl_7,
             do=['Check **pending items and NOA** only if you read them.', 'Check **scan folder** only if you looked.', 'Log out of Alora, then lock the computer (Windows key + L). Check **log out and lock**.'],
             check=['Every box you checked is true.', 'Any problem is written with what, to whom and the time.'],
             expect='The Daily Office Alora Check is complete and signed.',
             see='A sheet with the checks and the problems reported.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Give the daily sheet to the Administrator at the end of the week.',
             key_note='Full procedure: **P28**, {{pg:security}}.'),
    ],
    final=['I signed in with my own login.', 'I read the pending items and the NOA box.', 'I checked the Live Monitor and the exception list.', 'I looked at today\'s schedule.',
           'The scan folder holds only files waiting for upload.', 'I logged out and locked the computer.', 'The daily sheet is complete.'],
    stop=['An NOA is due today and not sent.', 'A start of care visit is late or missed.', 'An exception is older than 2 business days.', 'A patient file is where it should not be.',
          'A screen does not look like this manual.'],
    donot=['Do not skip a step because the day is busy.', 'Do not check a box for something you did not do.', 'Do not sign in as someone else.'],
)


# ============================================================================= P24 Weekly
def m_wk_1():
    m = S3.pending_list('orders')
    m.call(1, 'pend', 'Pending items list', (220, 400), key='cl_pending')
    m.call(2, 'pend.c2', 'Date: older than 7 days?', (560, 92), key='cl_pending')
    return m


def m_wk_2():
    m = S4.schedule_calendar(by=0)
    m.call(1, 'sch_viewby.0', 'Patient view', ('above', 90, 0), key='sch_viewby')
    m.call(2, 'sch_range.3', 'Certification period', ('above', 120, 0), key='sch_range')
    return m


def m_wk_3():
    m = S2.zform('CERTIFICATION PERIOD WATCH', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'end', 'Period ends:'),
        ('h', 'RECERTIFICATION (LAST 5 DAYS OF THE 60-DAY PERIOD)'), ('line', 'win', 'Window starts (day 56):'),
        ('check', 'v', 'Recertification visit is on the schedule inside the window'), ('check', 'o', 'Recertification OASIS is on the pending list'),
        ('check', 'x', 'Not scheduled: tell the DON today'),
        ('h', 'CHECKED BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')], lh=42)
    m.call(1, 'win', 'Window starts', ('right', 0, 0), key='zenith')
    m.call(2, 'v', 'Visit inside the window', ('right', 0, 0), key='zenith')
    m.call(3, 'x', 'Not scheduled: tell DON', ('right', 0, 0), key='zenith')
    return m


def m_wk_4():
    m = S4.staff_list()
    m.call(1, 'staff_list', 'Staff list', (200, 420), key='staff_list')
    m.call(2, 'staff_exp', 'Expires', (600, 92), key='staff_list')
    return m


def m_wk_5():
    m = S2.zform('WEEKLY OFFICE ALORA CHECK', [
        ('h', 'WEEK OF'), ('two', 'dt', 'Week of:', 'emp', 'Employee:'),
        ('h', 'CHECK EACH ONE'), ('check', 'w_pend', 'Pending items older than 7 days listed and DON told'),
        ('check', 'w_freq', 'New patients\' visits compared with orders'), ('check', 'w_cert', 'Certification periods ending in 14 days checked'),
        ('check', 'w_cred', 'Staff credentials ending in 30 days listed'), ('check', 'w_qa', 'QA Log given to the DON (Friday)'),
        ('line', 'w_prob', 'Problems reported (what, to whom, date):')], lh=40)
    m.call(1, 'w_pend', 'Pending items', ('right', 0, 0), key='zenith')
    m.call(2, 'w_cert', 'Certification periods', ('right', 0, 0), key='zenith')
    m.call(3, 'w_cred', 'Staff credentials', ('right', 0, 0), key='zenith')
    return m


WEEKLY = Proc(
    id='weekly', tab=9, num='P24', title='Weekly Office Alora Check',
    purpose='Once a week, look beyond today: items that have waited too long, patients whose visits do not match their orders, certification periods about to end, and staff credentials about to expire. '
            'Do this every Friday afternoon.',
    before=['The **Weekly Office Alora Check** sheet (Tab 11).', 'The **Certification Period Watch** form (Tab 11).', 'This week\'s Daily sheets and QA Log.'],
    who='The office employee the Administrator names.', time='About 45 minutes.',
    steps=[
        Step('wk-1', 'Find items that have waited too long', m_wk_1,
             do=['Open the **pending items** list.', 'Read the **date** column. Mark any item older than 7 days.'],
             check=['You listed every item older than 7 days.'],
             expect='A list of items that have waited a week or more.',
             see='A list of pending items with dates.',
             donot=['Do not open or edit a clinical form.'],
             alora='Alora documents pending items in one place. The list and its columns must be verified.', astatus='FEATURE',
             zenith='Give the list to the DON the same day.',
             stop=['An item is older than 14 days.'],
             key_note='Full procedure: **P19**, {{pg:clinrev}}.'),
        Step('wk-2', 'Compare visits with orders', m_wk_2,
             do=['Choose **patient** in view by. Choose each **new patient** from the last two weeks.', 'Choose the **certification period** view to see all visits in the period.'],
             check=['The visits scheduled match the ordered frequency.'],
             expect='You know if any new patient has too few or too many visits.',
             see='A patient\'s visits across the period.',
             alora='Alora documents schedule views by patient and certification period. The names must be verified.', astatus='FEATURE',
             zenith='Write a mismatch on the Visit Frequency Check and tell the DON.',
             stop=['Fewer visits are scheduled than ordered.'],
             key_note='Full procedure: **P15**, {{pg:viewschedule}}.'),
        Step('wk-3', 'Watch certification periods', m_wk_3,
             do=['Write the day the recertification **window starts** (day 56).', 'Check that the **visit** is on the schedule inside the window.', 'If it is not, check the box and **tell the DON today**.'],
             check=['You counted days from the start of care date with a calendar.'],
             expect='Every period ending soon has a recertification visit scheduled.',
             see='A form for each patient whose period ends in 14 days.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='List every patient whose period ends in the next 14 days.',
             rule='The recertification assessment is done in the last 5 days of each 60-day certification period.',
             stop=['A recertification visit is not scheduled.']),
        Step('wk-4', 'Check staff credentials', m_wk_4,
             do=['Open the **staff list**.', 'Read the **expires** column. Mark any date in the next 30 days, and any date that has passed.'],
             check=['You listed every credential that expires within 30 days.'],
             expect='A list of staff whose credentials expire soon.',
             see='A list of staff with credential names and dates.',
             donot=['Do not change a staff record.'],
             alora='Alora documents HR functions. Whether this list exists and where must be verified.',
             zenith='Give the list to the Administrator the same day. Staff with an expired credential must not be scheduled.',
             stop=['A credential has expired and the person is on the schedule.']),
        Step('wk-5', 'Complete the weekly sheet', m_wk_5,
             do=['Check **pending items** after steps 1 and 2.', 'Check **certification periods** after step 3.', 'Check **staff credentials** after step 4.'],
             check=['Every box you checked is true.'],
             expect='The Weekly Office Alora Check is complete.',
             see='A sheet with the weekly checks.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Give the weekly sheet to the Administrator every Friday.'),
    ],
    final=['I listed items older than 7 days and the DON knows.', 'I compared new patients\' visits with their orders.', 'I checked every certification period ending in 14 days.',
           'I listed credentials ending in 30 days.', 'The weekly sheet is complete.'],
    stop=['An item is older than 14 days.', 'A recertification visit is not scheduled.', 'A credential is expired and the person is on the schedule.', 'Visits do not match orders.'],
    donot=['Do not skip the Friday check.', 'Do not change a clinical form or a staff record.', 'Do not check a box for something you did not do.'],
)


# ============================================================================= P25 Monthly
def m_mn_1():
    m = S.patients_list(results=True, selected=None, query=('', ''))
    m.call(1, 'pt_results.c3', 'Status column', (604, 420), key='pt_results')
    m.call(2, 'pt_results', 'Patient list', (330, 420), key='pt_results')
    return m


def m_mn_2():
    m = S4.billing_list()
    m.call(1, 'bill_ready', 'Billing list', (200, 400), key='bill_ready')
    m.call(2, 'bill_ready.c3', 'Claim status', (620, 92), key='bill_ready')
    return m


def m_mn_3():
    m = S2.zform('DISCHARGE CHECK', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'dc', 'Discharge date:'),
        ('h', 'PAPERS IN ALORA (UPLOADED AND VERIFIED)'), ('check', 'x_ord', 'Discharge order'), ('check', 'x_sum', 'Discharge summary'),
        ('h', 'STATUS AND BILLING'), ('check', 'x_st', 'Status in Alora shows discharged (set by the DON)'), ('check', 'x_bill', 'Billing told'),
        ('check', 'x_visit', 'No visits are still scheduled after the discharge date'),
        ('h', 'CHECKED BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')], lh=42)
    m.call(1, 'x_sum', 'Papers uploaded', ('right', 0, 0), key='zenith')
    m.call(2, 'x_st', 'Status set by the DON', ('right', 0, 0), key='zenith')
    m.call(3, 'x_visit', 'No later visits', ('right', 0, 0), key='zenith')
    return m


def m_mn_4():
    m = S4.staff_list()
    m.call(1, 'staff_list', 'Staff / user list', (200, 420), key='staff_list')
    return m


def m_mn_5():
    m = S2.zform('MONTHLY OFFICE ALORA CHECK', [
        ('h', 'MONTH'), ('two', 'dt', 'Month:', 'emp', 'Employee:'),
        ('h', 'CHECK EACH ONE'), ('check', 'm_census', 'Active patient list matches the DON\'s census'),
        ('check', 'm_claims', 'Every claim is ready, sent or has an owner'), ('check', 'm_dc', 'Every discharge has its papers (Discharge Check)'),
        ('check', 'm_users', 'User list reviewed by the Administrator'), ('check', 'm_prob', 'All problem reports and correction requests are closed'),
        ('line', 'm_note', 'Problems reported (what, to whom, date):')], lh=40)
    m.call(1, 'm_census', 'Active patients', ('right', 0, 0), key='zenith')
    m.call(2, 'm_users', 'User list', ('right', 0, 0), key='zenith')
    m.call(3, 'm_prob', 'Reports closed', ('right', 0, 0), key='zenith')
    return m


MONTHLY = Proc(
    id='monthly', tab=9, num='P25', title='Monthly Office Alora Check',
    purpose='Once a month, check the whole picture: who is active, which claims are stuck, whether discharges are complete, and who still has a login. '
            'Do this in the last week of the month.',
    before=['The **Monthly Office Alora Check** sheet and the **Discharge Check** form (Tab 11).', 'The DON\'s census (list of active patients).', 'The Administrator\'s list of current employees.'],
    who='The office employee the Administrator names. The Administrator reviews the user list.', time='About 90 minutes.',
    steps=[
        Step('mn-1', 'Compare the active patient list with the DON\'s census', m_mn_1,
             do=['Open the **patient list** and read the **status** column.', 'Compare it with the **DON\'s census**. Every active patient is on both lists.'],
             check=['No patient is active in Alora but not in the census, and no patient is in the census but not active in Alora.'],
             expect='The two lists match, or you know which patients do not.',
             see='A patient list with a status for each.',
             donot=['Do not change a patient\'s status. The DON does.'],
             alora='Open the patient list and read the status. The filter for active patients must be verified.',
             zenith='Give differences to the DON the same day.',
             stop=['A patient is active in one list and not in the other.']),
        Step('mn-2', 'Look at every claim', m_mn_2,
             do=['Open the **billing list** for the month.', 'Read the **claim status**. Every claim is ready, sent, or has an owner.'],
             check=['No claim is older than the Administrator\'s limit without an owner.'],
             expect='Every claim is moving.',
             see='A list of claims with statuses.',
             alora='Alora documents billing. The list and its words must be verified.', astatus='FEATURE',
             zenith='Give stuck claims to billing staff the same day.',
             stop=['A claim is stuck and close to its filing limit.'],
             key_note='Full procedure: **P21**, {{pg:billing}}.'),
        Step('mn-3', 'Check every discharge', m_mn_3,
             do=['Check the **discharge order** and **discharge summary** are uploaded and verified.', 'Check the status was set to discharged by the **DON**.', 'Check **no later visits** are on the schedule.'],
             check=['Each discharged patient has all three.'],
             expect='Every discharge this month is complete.',
             see='A Discharge Check form for each discharged patient.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='A visit scheduled after discharge is reported to the DON the same day.',
             stop=['A discharged patient still has visits on the schedule.']),
        Step('mn-4', 'Give the Administrator the user list', m_mn_4,
             do=['Open the **staff or user list** and print or show it to the Administrator.'],
             check=['The Administrator compares it with the list of current employees.'],
             expect='The Administrator confirms that nobody who has left still has a login.',
             see='A list of users and their roles.',
             donot=['Do not remove or add a user. The Administrator does.'],
             alora='Alora documents HR functions. Where the user list is must be verified.',
             zenith='An account for someone who left is a HIPAA risk. The Administrator closes it the same day.',
             rule='HIPAA requires that only authorized people can access patient information.',
             stop=['A person who left still has access.']),
        Step('mn-5', 'Complete the monthly sheet', m_mn_5,
             do=['Check **active patients** after step 1.', 'Check **user list** after the Administrator reviewed it.', 'Check **reports closed** only when every problem report and correction request is closed.'],
             check=['Every box you checked is true.'],
             expect='The Monthly Office Alora Check is complete.',
             see='A sheet with the monthly checks.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Give the monthly sheet to the Administrator by the last business day of the month.'),
    ],
    final=['The active patient list matches the DON\'s census.', 'Every claim is ready, sent or has an owner.', 'Every discharge is complete.', 'The Administrator reviewed the user list.', 'The monthly sheet is complete.'],
    stop=['The patient list does not match the census.', 'A claim is stuck near its limit.', 'A discharged patient has visits scheduled.', 'A person who left still has access.'],
    donot=['Do not change a patient status.', 'Do not remove or add a user.', 'Do not check a box for something you did not do.'],
)


PAGES = [Divider(9, 'Short, fixed routines that catch problems early: every day, every Friday and every month.',
                 [('daily', 'P23  Daily Office Alora Check'), ('weekly', 'P24  Weekly Office Alora Check'), ('monthly', 'P25  Monthly Office Alora Check')]),
         DAILY, WEEKLY, MONTHLY]

"""Tab 6: scheduling visits, viewing the schedule, changing a schedule when authorized."""
import scenes as S
import scenes2 as S2
import scenes4 as S4
from model import Proc, Step, Divider
from blocks import *


# ============================================================================= shared mocks
def m_nav_schedule():
    m = S4.blank_shell('dash', 'Dashboard')
    m.call(1, 'nav.schedule', 'Schedule menu', ('right', 0, 0), key='nav_schedule')
    return m


# ============================================================================= P14 Schedule visits
def m_sc_1():
    m = S2.zform('VISIT SCHEDULING REQUEST', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'dob', 'DOB:'),
        ('h', 'FROM THE PLAN OF CARE (WRITTEN BY THE DON)'), ('line', 'disc', 'Discipline (RN, PT, OT, ST, aide, MSW):'),
        ('line', 'freq', 'How often (example: 2 times a week for 4 weeks):'), ('line', 'first', 'First visit date:'),
        ('line', 'who', 'Team member:'),
        ('h', 'APPROVAL'), ('line', 'init', 'DON initials:')])
    m.call(1, 'freq', 'How often', ('right', 0, 0), key='zenith')
    m.call(2, 'who', 'Team member', ('right', 0, 0), key='zenith')
    m.call(3, 'init', 'DON initials', ('right', 0, 0), key='zenith')
    return m


def m_sc_3():
    m = S4.schedule_calendar()
    m.call(1, 'sch_add', 'Add visit', ('above', -40, 0), key='sch_add')
    return m


def m_sc_4():
    m = S4.new_visit_form()
    m.call(1, 'f_visit_pt', 'Patient', ('right', 0, 0), key='f_visit_pt')
    m.call(2, 'f_visit_type', 'Visit type', ('right', 0, 0), key='f_visit_type')
    m.call(3, 'f_visit_member', 'Team member', ('right', 0, 0), key='f_visit_member')
    return m


def m_sc_5():
    m = S4.new_visit_form()
    m.call(1, 'f_visit_date', 'Date', ('right', 0, 0), key='f_visit_date')
    m.call(2, 'f_visit_time', 'Time', ('right', 0, 0), key='f_visit_time')
    m.call(3, 'f_visit_freq', 'Repeat', ('right', 0, 0), key='f_visit_freq')
    return m


def m_sc_6():
    m = S4.new_visit_form(alerts=True)
    m.call(1, 'sch_alerts', 'Read every alert', ('below', 0, 0), key='sch_alerts')
    m.call(2, 'btn_save', 'Save once', ('above', 60, 16), key='btn_save')
    return m


def m_sc_7():
    m = S4.schedule_calendar(extra_visit=True, by=1, at=(1, 1), label='9:00 Aide', sub='Smith, M.')
    m.call(1, 'sch_visit', 'New visit is here', ('below', -40, 10), key='sch_visit')
    m.call(2, 'sch_viewby.1', 'Team member view', ('above', 90, 0), key='sch_viewby')
    return m


def m_sc_8():
    m = S2.zform('VISIT NOTICE LOG', [
        ('h', 'PATIENT AND VISIT'), ('two', 'pt', 'Patient:', 'vis', 'Visit (date, time):'),
        ('h', 'WHO WAS TOLD'), ('line', 'tm', 'Team member told (how, date, time):'), ('line', 'pat', 'Patient told (how, date, time):'),
        ('h', 'DONE BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')])
    m.call(1, 'tm', 'Team member told', ('right', 0, 0), key='zenith')
    m.call(2, 'pat', 'Patient told', ('right', 0, 0), key='zenith')
    m.call(3, 'emp_row', 'Initials and date', ('right', 0, 0), key='zenith')
    return m


SCHEDULE = Proc(
    id='schedule', tab=6, num='P14', title='Schedule Visits',
    purpose='To put a visit on the Alora schedule correctly: the right patient, the right discipline, the right team member, the right day and time, and the right repeat pattern. '
            'The example in this procedure is a weekly home health aide visit. A start of care visit uses the same screens (P13).',
    before=['A **Visit Scheduling Request** signed by the DON (Tab 11). It shows the discipline, how often, the first visit date and the team member.',
            'The patient\'s agreed times (from your call).', 'You are signed in (P1).'],
    who='Schedulers.', time='5 to 10 minutes for each patient.',
    steps=[
        Step('sc-1', 'Get the DON\'s request', m_sc_1,
             do=['Find **how often** the visits are ordered.', 'Find the **team member** the DON named.', 'Check the DON\'s **initials** are on the form.'],
             check=['The discipline and frequency are written in words and numbers.', 'You did not choose the team member or the frequency yourself.'],
             expect='A signed request is in your hand.',
             see='A form with the discipline, the frequency, the first visit date, the team member and the DON\'s initials.',
             donot=['Do not schedule from memory or from a verbal request.', 'Do not change the frequency to fit the calendar.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='The plan of care sets how often a patient is seen. The DON writes it on the request. Office staff never change it.',
             rule='Visits must follow the physician\'s plan of care.',
             stop=['There is no plan of care or no DON initials.']),
        Step('sc-2', 'Open the Schedule', m_nav_schedule,
             do=['Click **Schedule** in the main menu on the left.'],
             check=['You are not in the middle of another form.'],
             expect='The schedule screen opens.',
             see='A calendar with visits on it, and view choices at the top.',
             alora='Alora documents scheduling. The menu name must be verified.', astatus='FEATURE',
             zenith='Use the Alora menu to move. Do not use the browser Back arrow.',
             stop=['You cannot find Schedule, or the schedule does not open.']),
        Step('sc-3', 'Start a new visit', m_sc_3,
             do=['Click the **add visit** button.'],
             check=['You are on the schedule, not inside a patient\'s record.'],
             expect='A form to add a visit opens.',
             see='A form titled like \'Add visit\' with boxes for patient, type, date and time.',
             alora='Alora documents batch entry scheduling. The button name and where it is must be verified.', astatus='FEATURE',
             zenith='One visit form at a time. Finish or cancel a form before you start another.',
             stop=['You cannot find an add visit button.']),
        Step('sc-4', 'Choose who and what', m_sc_4,
             do=['Choose the **patient**. Check the name and date of birth.', 'Choose the **visit type** (for example home health aide).', 'Choose the **team member** from the DON\'s request.'],
             enter='Only what is on the signed request.',
             check=['The patient is the one on the request.', 'The visit type matches the discipline on the request.', 'The team member is the one the DON named.'],
             expect='Patient, visit type and team member are filled in.',
             see='The visit form with three boxes filled in.',
             donot=['Do not use a different team member because they are nearer or free.', 'Do not guess the visit type.'],
             alora='Choose the patient, the visit type and the team member. The names of the boxes and choices must be verified.', astatus='FEATURE',
             zenith='Two identifiers confirm the patient: name and date of birth.',
             stop=['The visit type or team member you need is not in the list.']),
        Step('sc-5', 'Choose when and how often', m_sc_5,
             do=['Enter the **date** of the first visit.', 'Enter the **time** you agreed with the patient.', 'Set **repeat** to match the frequency on the request.'],
             enter='Date, time and repeat pattern from the request. For example: every Monday and Thursday for 4 weeks.',
             check=['The date is not a day the patient said no to.', 'The repeat pattern gives the same number of visits as the request.'],
             expect='The form shows the date, time and repeat pattern.',
             see='The visit form with date, time and repeat filled in.',
             donot=['Do not set a repeat that gives more or fewer visits than ordered.'],
             alora='Enter a date and a time, and set a repeat. The names of these boxes must be verified.', astatus='FEATURE',
             zenith='Count the visits the repeat will create before you save. It must equal the order.',
             stop=['You cannot make the repeat match the order.']),
        Step('sc-6', 'Read the alerts, then Save', m_sc_6,
             do=['Read **every alert**. Alora can warn about a conflict, a missing authorization or a visit-frequency problem.', 'If there is no problem, click **Save** once.'],
             check=['You read each alert.', 'Nothing is saved while an alert is unexplained.'],
             expect='The form closes and the visits are saved.',
             see='A form with an alert box on the right, then the schedule after Save.',
             donot=['Do not click through an alert without reading it.', 'Do not click Save more than once.'],
             alora='Alora documents conflict and compliance alerts while scheduling. How an alert looks must be verified.', astatus='FEATURE',
             zenith='An alert is a question for the DON. You do not answer it alone.',
             ifwrong='An error message appears: do not click Save again. **Stop** and ask the Administrator.',
             stop=['An alert names a conflict, a missing authorization or a frequency problem.', 'An error message appears.']),
        Step('sc-7', 'Check the new visits on the calendar', m_sc_7,
             do=['Find the **new visit** on the calendar.', 'Use the **team member** view. Check the day, the time and the team member.'],
             check=['Each visit is there once.', 'The number of visits equals the order.', 'No visit is on a day the patient refused.'],
             expect='The visits are on the calendar, once each.',
             see='A calendar with the new visit highlighted.',
             donot=['Do not drag a visit to fix it. Go to P16.'],
             alora='Alora documents schedule views by patient, team member and agency. The view names must be verified.', astatus='FEATURE',
             zenith='Verify in the same session you scheduled.',
             stop=['A visit is missing, is there twice, or shows for the wrong person.']),
        Step('sc-8', 'Tell the team member and the patient', m_sc_8,
             do=['Write who you told on the team member line: how, and the date and time.', 'Write who you told on the patient line.', 'Write your **initials** and the date.'],
             check=['You told both people.', 'The visit on the log matches the calendar.'],
             expect='The Visit Notice Log is complete.',
             see='A log with both people named and your initials.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='A visit the team member does not know about is a missed visit. Tell them the same day.'),
    ],
    final=['The request was signed by the DON.', 'The patient, the visit type and the team member match the request.', 'The date, time and repeat pattern give the ordered number of visits.',
           'I read every alert.', 'The visits are on the calendar once each.', 'The team member and the patient know about the visits.'],
    stop=['There is no signed request.', 'An alert names a conflict, a missing authorization or a frequency problem.', 'The visit type or team member is not in the list.',
          'An error message appears.', 'The visits do not match the order.'],
    donot=['Do not schedule without a signed request.', 'Do not change the ordered frequency.', 'Do not ignore an alert.', 'Do not save twice.', 'Do not assign a team member the DON did not name.'],
)


# ============================================================================= P15 View the schedule
def m_vs_2():
    m = S4.schedule_calendar()
    m.call(1, 'sch_viewby', 'View by', ('above', 90, 0), key='sch_viewby')
    m.call(2, 'sch_range', 'Show: day or week', ('above', 40, 0), key='sch_range')
    return m


def m_vs_3():
    m = S4.schedule_calendar(extra_visit=True)
    m.call(1, 'sch_visit', 'One visit', ('below', -40, 10), key='sch_visit')
    m.call(2, (176 + 2 * 140, 208, 140, 30), 'The day', (614, 250), key='sch_grid')
    return m


def m_vs_4():
    m = S4.schedule_calendar(by=0)
    m.call(1, 'sch_viewby.0', 'Patient view', ('above', 90, 0), key='sch_viewby')
    m.call(2, 'sch_grid', 'This patient\'s visits', (430, 405), key='sch_grid')
    return m


def m_vs_5():
    m = S4.schedule_calendar(by=1)
    m.call(1, 'sch_viewby.1', 'Team member view', ('above', 90, 0), key='sch_viewby')
    m.call(2, 'sch_grid', 'This person\'s week', (430, 405), key='sch_grid')
    return m


def m_vs_6():
    m = S2.zform('VISIT FREQUENCY CHECK', [
        ('h', 'PATIENT'), ('two', 'pt', 'Patient:', 'wk', 'Week of:'),
        ('h', 'COMPARE'), ('line', 'ord', 'Ordered (from the plan of care):'), ('line', 'sch', 'Scheduled in Alora this week:'),
        ('check', 'ok', 'They match'), ('check', 'no', 'They do not match: tell the DON today'),
        ('h', 'CHECKED BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')])
    m.call(1, 'ord', 'Ordered', ('right', 0, 0), key='zenith')
    m.call(2, 'sch', 'Scheduled', ('right', 0, 0), key='zenith')
    m.call(3, 'no', 'Not matching: tell the DON', ('right', 0, 0), key='zenith')
    return m


VIEWSCHED = Proc(
    id='viewschedule', tab=6, num='P15', title='View the Schedule',
    purpose='To find visits on the Alora schedule by patient, by team member or for the whole agency, read them correctly, and check that each patient has the visits that were ordered. '
            'Viewing changes nothing, so this is a safe procedure to practice.',
    before=['You are signed in (P1).', 'The **Visit Frequency Check** form (Tab 11), if you are checking a patient.'],
    who='Any trained office employee.', time='2 to 5 minutes.',
    steps=[
        Step('vs-1', 'Open the Schedule', m_nav_schedule,
             do=['Click **Schedule** in the main menu on the left.'],
             check=['You are not inside a form.'],
             expect='The schedule screen opens.',
             see='A calendar with visits on it, and view choices at the top.',
             alora='Alora documents scheduling. The menu name must be verified.', astatus='FEATURE',
             zenith='Viewing the schedule changes nothing. You can look without fear.'),
        Step('vs-2', 'Choose how to look', m_vs_2,
             do=['Choose **view by**: patient, team member or agency.', 'Choose **show**: day, week, month or certification period.'],
             check=['The calendar changes each time you choose.'],
             expect='The calendar shows what you chose.',
             see='A calendar that matches the choice. The choice you made is highlighted.',
             alora='Alora documents schedule views by patient, caregiver or agency, and by day, week, month or certification period. The exact words and places must be verified.', astatus='FEATURE',
             zenith='Start with the **week** view. It shows the most with the least scrolling.'),
        Step('vs-3', 'Read one visit', m_vs_3,
             do=['Find **one visit** on the calendar. Read its time, its discipline and the person.', 'Find the **day** at the top of its column.'],
             check=['You can say: who goes, to which patient, on which day, at what time.'],
             expect='You can read any visit on the calendar.',
             see='A calendar with one highlighted visit and its day.',
             donot=['Do not drag a visit. Dragging can change it.'],
             alora='Read a visit on the calendar. What a visit box shows must be verified.',
             zenith='If you cannot tell who or when, ask the Administrator. Do not guess.'),
        Step('vs-4', 'See one patient\'s visits', m_vs_4,
             do=['Choose **patient** in view by and pick the patient.', 'Read this patient\'s visits for the week.'],
             check=['The patient name at the top is the one you want.', 'Two identifiers: name and date of birth.'],
             expect='Only this patient\'s visits are shown.',
             see='A calendar that shows only one patient\'s visits.',
             alora='Schedule views by patient. The name of the view must be verified.', astatus='FEATURE',
             zenith='Confirm the patient before you read or change anything.'),
        Step('vs-5', 'See one team member\'s week', m_vs_5,
             do=['Choose **team member** in view by and pick the person.', 'Read the person\'s visits for the week.'],
             check=['The team member at the top is the one you want.', 'No two visits overlap.'],
             expect='Only this person\'s visits are shown.',
             see='A calendar that shows one team member\'s visits.',
             alora='Schedule views by caregiver (team member). The name of the view must be verified.', astatus='FEATURE',
             zenith='Overlapping visits for one person are reported to the DON the same day.',
             stop=['Two visits overlap for one person.']),
        Step('vs-6', 'Compare with what was ordered', m_vs_6,
             do=['Write what was **ordered** in the plan of care.', 'Write what is **scheduled** this week.', 'If they do not match, check the box and **tell the DON today**.'],
             check=['The numbers match, or you told the DON.'],
             expect='You know if this patient\'s visits match the order.',
             see='A form with the ordered frequency and the scheduled visits side by side.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='Do this for every new patient in the first week and whenever a visit is changed.',
             rule='Visits must follow the physician\'s plan of care.',
             stop=['Fewer visits are scheduled than ordered.']),
    ],
    final=['I opened the schedule and chose a view.', 'I can read the day, time, discipline and person of a visit.', 'I saw a patient\'s visits and a team member\'s week.',
           'I compared the schedule with the order when required.', 'I changed nothing.'],
    stop=['A patient has fewer visits than ordered.', 'A visit is missing or in the wrong place.', 'Two visits overlap for one person.'],
    donot=['Do not drag visits on the calendar.', 'Do not change a visit because it looks wrong. Report it.'],
)


# ============================================================================= P16 Change a schedule (when authorized)
def m_cs_1():
    m = S2.zform('SCHEDULE CHANGE APPROVAL', [
        ('h', 'PATIENT AND VISIT'), ('two', 'pt', 'Patient:', 'old', 'Old date and time:'),
        ('h', 'THE CHANGE'), ('line', 'why', 'Reason (who asked, why):'), ('line', 'new', 'New date and time:'),
        ('line', 'mem', 'New team member (if changed):'),
        ('h', 'APPROVAL (DON OR ADMINISTRATOR)'), ('line', 'init', 'Initials and date:')])
    m.call(1, 'why', 'Reason', ('right', 0, 0), key='zenith')
    m.call(2, 'new', 'New date and time', ('right', 0, 0), key='zenith')
    m.call(3, 'init', 'Approved by', ('right', 0, 0), key='zenith')
    return m


def m_cs_2():
    m = S4.schedule_calendar(at=(0, 1))
    m.call(1, 'sch_visit', 'The visit to change', ('below', 40, 10), key='sch_visit')
    m.call(2, 'sch_range', 'Week view', ('above', 60, 0), key='sch_range')
    return m


def m_cs_3():
    m = S4.visit_edit()
    m.call(1, 'f_visit_date', 'Date', ('right', 0, 0), key='f_visit_date')
    m.call(2, 'f_visit_time', 'Time', ('right', 0, 0), key='f_visit_time')
    m.call(3, 'f_visit_member', 'Team member', ('right', 0, 0), key='f_visit_member')
    return m


def m_cs_4():
    m = S4.visit_edit()
    m.call(1, 'sch_reason', 'Reason for the change', ('right', 0, 0), key='sch_reason')
    m.call(2, 'btn_save', 'Save once', ('above', 60, 16), key='btn_save')
    return m


def m_cs_5():
    m = S4.schedule_calendar(extra_visit=True, label='1:00 Aide', sub='J. D.', at=(3, 0), hide=(0, 1))
    m.call(1, 'sch_visit', 'Visit in its new place', ('below', -40, 10), key='sch_visit')
    m.call(2, (176 + 8, 208 + 42 + 62, 124, 54), 'Old place is empty', (250, 420), key='sch_grid')
    return m


def m_cs_6():
    m = S2.zform('CHANGE NOTICE LOG', [
        ('h', 'PATIENT AND VISIT'), ('two', 'pt', 'Patient:', 'vis', 'New visit (date, time):'),
        ('h', 'WHO WAS TOLD'), ('line', 'pat', 'Patient told (how, date, time):'), ('line', 'tm', 'Team member told (how, date, time):'),
        ('line', 'don', 'DON told (date):'),
        ('h', 'DONE BY'), ('two', 'emp', 'Initials:', 'dt', 'Date:')])
    m.call(1, 'pat', 'Patient told', ('right', 0, 0), key='zenith')
    m.call(2, 'tm', 'Team member told', ('right', 0, 0), key='zenith')
    m.call(3, 'don', 'DON told', ('right', 0, 0), key='zenith')
    return m


CHANGESCHED = Proc(
    id='changeschedule', tab=6, num='P16', title='Change a Schedule When Authorized',
    purpose='To move or reassign a visit only when the DON or the Administrator has approved it in writing, and to make sure the patient and the team member both know. '
            'A careless change can cause a missed visit, a late start of care or a billing problem.',
    before=['A **Schedule Change Approval** form signed by the DON or the Administrator (Tab 11).', 'The **Change Notice Log** (Tab 11).', 'The patient\'s and team member\'s phone numbers.'],
    who='Schedulers. Only with written approval.', time='10 minutes.',
    steps=[
        Step('cs-1', 'Get the written approval first', m_cs_1,
             do=['Write the **reason**: who asked and why.', 'Write the **new date and time**.', 'Get the DON or Administrator\'s **initials**.'],
             check=['The approval is signed before you touch the schedule.', 'The visit is not a start of care visit, or the DON said the change is allowed.'],
             expect='A signed approval form is in your hand.',
             see='A form with the reason, the new date and time and the approver\'s initials.',
             donot=['Do not change a visit on a verbal request.', 'Do not change a start of care visit without the DON.'],
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='No written approval, no change. This protects the patient, the team member and Zenith.',
             rule='A late start of care visit can break the 48-hour rule. Visits must follow the plan of care.',
             stop=['The DON or Administrator is not available and the visit is today.']),
        Step('cs-2', 'Find the visit on the calendar', m_cs_2,
             do=['Find the **visit** on the calendar. Check the patient, day, time and team member against the approval form.', 'Use the **week** view so you can see the days around it.'],
             check=['It is the right visit. It is the only visit that matches.'],
             expect='You see the visit you are allowed to change.',
             see='A calendar with the visit you will change.',
             donot=['Do not change a visit that is already done.', 'Do not drag the visit to another day.'],
             alora='Find a visit on the schedule. The view names must be verified.', astatus='FEATURE',
             zenith='Two identifiers confirm the patient.',
             stop=['You find two visits that could match.']),
        Step('cs-3', 'Open the visit and change only what was approved', m_cs_3,
             do=['Change the **date** only if the approval says so.', 'Change the **time** only if the approval says so.', 'Change the **team member** only if the approval says so.'],
             enter='Only the items written on the approval form.',
             check=['Every change on screen is on the approval form.', 'You changed nothing else.'],
             expect='The new values show in the boxes.',
             see='A visit form with the new values in the boxes you changed.',
             donot=['Do not change a box that the approval does not name.', 'Do not delete the visit to start again.'],
             alora='Open a visit and edit it. How to open the visit and the box names must be verified.', astatus='FEATURE',
             zenith='Never delete a visit. If a visit must be cancelled, the DON or Administrator tells you how.',
             stop=['You cannot find how to open the visit.', 'The form offers to delete or cancel.']),
        Step('cs-4', 'Write the reason and Save', m_cs_4,
             do=['Type the **reason** in words. Use the wording on the approval form.', 'Read any alert, then click **Save** once.'],
             enter='Reason: for example \'Patient asked for a later time. Approved by DON. Date.\'',
             check=['The reason is written.', 'No alert is left unexplained.'],
             expect='The form closes and the change is saved.',
             see='The visit form with a reason and the Save button.',
             donot=['Do not leave the reason blank.', 'Do not click Save more than once.'],
             alora='Enter a reason and save. A reason box may or may not exist in Zenith\'s Alora. It must be verified.',
             zenith='Every change has a written reason.',
             ifwrong='An error message appears: do not click Save again. **Stop** and ask the Administrator.',
             stop=['There is no place for a reason.', 'An alert names a conflict or a rule.']),
        Step('cs-5', 'Check the result', m_cs_5,
             do=['Find the visit in its **new place**.', 'Check that the **old place** is empty.'],
             check=['The visit shows once.', 'The day, time and team member match the approval.'],
             expect='The visit is in its new place, once.',
             see='A calendar where the visit has moved.',
             alora='Alora documents schedule views. The view names must be verified.', astatus='FEATURE',
             zenith='Verify in the same session you changed it.',
             stop=['The visit shows twice, or in the wrong place.']),
        Step('cs-6', 'Tell the patient and the team member', m_cs_6,
             do=['Write when and how you told the **patient**.', 'Write when and how you told the **team member**.', 'Write when you told the **DON**.'],
             check=['Both people know the new time.'],
             expect='The Change Notice Log is complete.',
             see='A log with three lines filled in.',
             alora='Not an Alora step. This is a Zenith paper form.', astatus='ZENITH',
             zenith='A change nobody knows about is a missed visit. Tell both people the same day.'),
    ],
    final=['I had a signed approval before I changed anything.', 'I changed only what the approval named.', 'I wrote a reason.', 'The visit is in its new place, once.',
           'The patient, the team member and the DON know.'],
    stop=['There is no written approval.', 'The visit is a start of care visit.', 'An alert names a conflict or a rule.', 'The visit cannot be changed in Alora.', 'The change would leave the patient with fewer visits than ordered.'],
    donot=['Do not change a schedule without written approval.', 'Do not delete a visit.', 'Do not change a visit that is already done.', 'Do not drag visits.'],
)


PAGES = [Divider(6, 'Put visits on the Alora schedule, read the schedule, and change a visit only when it is approved in writing.',
                 [('schedule', 'P14  Schedule Visits'), ('viewschedule', 'P15  View the Schedule'), ('changeschedule', 'P16  Change a Schedule When Authorized')]),
         SCHEDULE, VIEWSCHED, CHANGESCHED]

"""Tab 2: Sign in and navigate."""
import scenes as S
import scenes2 as S2
from model import Proc, Step, Divider, Text
from blocks import *


# ----------------------------------------------------------------------------- P1 Log into Alora
def m_login_1():
    m = S.desktop_browser()
    m.call(1, 'browser_icon', 'Web browser icon', (128, 462), key='browser_icon')
    m.call(2, 'addr', 'Address bar', (330, 120), key='addr')
    return m


def m_login_2():
    m = S.login(filled=False)
    m.call(1, 'login_user', 'Username box', (24, 226), key='login_user')
    m.call(2, 'login_pass', 'Password box', (24, 312), key='login_pass')
    return m


def m_login_3():
    m = S.login(filled=True)
    m.call(1, 'login_btn', 'Login button', (24, 376), key='login_btn')
    return m


def m_login_4():
    m = S.dashboard()
    m.call(1, 'user', 'Your own name', (560, 100), key='user_menu')
    m.call(2, 'nav', 'Main menu', (170, 440), key='nav')
    return m


LOGIN = Proc(
    id='login', tab=2, num='P1', title='Log Into Alora',
    purpose='You must sign in with your own login before you can see any patient information. '
            'This procedure shows how to open the Alora website, sign in, and confirm that you are in the right place.',
    before=['Your **own** Alora username and password from the Administrator.',
            'The **Alora Access Sheet** with the Zenith Alora web address (Tab 1).',
            'A Zenith office computer (Windows). Not a personal computer. Not a phone.',
            'A private place to sit. Nobody can read your screen.'],
    who='Every office employee.', time='2 minutes.',
    steps=[
        Step('login-1', 'Open the Alora website', m_login_1,
             do=['Click the **web browser icon** on the taskbar at the bottom of the screen. Use the browser the Administrator told you to use.',
                 'Click the **address bar** at the top of the browser. Type the Alora web address exactly as written on the Alora Access Sheet. Press the **Enter** key.'],
             enter='The Zenith Alora web address from the Alora Access Sheet.',
             check=['The address is the same as on the Access Sheet.', 'The browser shows that the page is secure (https).'],
             expect='The Alora sign-in page opens.',
             see='A sign-in page with a box for a username, a box for a password, and a login button. The next page shows it.',
             donot=['Do not sign in from an address that came in an email or text.', 'Do not let the browser save your password.'],
             alora='Alora is a web-based system. Staff open it in a web browser. Nothing is installed on the computer.',
             astatus='FEATURE',
             zenith='Use only the address on the Alora Access Sheet. If the sheet is blank, ask the Administrator.',
             ifwrong='The page will not open, or the browser shows a security warning: close the browser and start again.',
             stop=['It happens a second time: **stop** and contact the Administrator.']),
        Step('login-2', 'Enter your username and password', m_login_2,
             do=['Click inside the **username** box. Type your own Alora username.',
                 'Click inside the **password** box. Type your own password.'],
             enter='Your own username and your own password. Nobody else\'s.',
             check=['The username on the screen is yours.', 'The password shows as dots.', 'Nobody is watching your screen.'],
             expect='Your username is in the first box. Dots are in the second box.',
             see='The sign-in page with your username in the first box and dots in the second box.',
             donot=['Do not use another person\'s login, even if they offer.', 'Do not write your password on paper near the computer.'],
             alora='Sign in with the username and password that your agency Administrator created for you in Alora.',
             zenith='Every office employee has a personal login. Sharing a login is not allowed.',
             rule='HIPAA requires that every person who uses a patient record system has a unique login.',
             ifwrong='You do not have a username or password yet: do not borrow one.',
             stop=['Ask the Administrator for your own login.']),
        Step('login-3', 'Click Login', m_login_3,
             do=['Click the **Login** button **one time**. Wait a few seconds.'],
             check=['You clicked only once.'],
             expect='The Alora dashboard opens.',
             see='A screen with a menu on the left and your name at the top right. It is called the dashboard.',
             alora='Select the login button to sign in.',
             zenith='Wait at least 10 seconds before you try again. Do not click many times.',
             ifwrong='A message says the username or password is wrong: check the letters and try **one** more time.',
             stop=['It fails a second time: **stop** and contact the Administrator.',
                   'The message says the account is locked, or asks for a code you do not know: **stop**.']),
        Step('login-4', 'Confirm you are on your own dashboard', m_login_4,
             do=['Look at the top right of the screen. Find **your own name**.',
                 'Look at the left side. Find the **main menu**.'],
             check=['The name is yours, not another person\'s.', 'No patient name is open yet.'],
             expect='You are signed in as yourself and the dashboard is open.',
             see='Your name at the top right. A menu on the left. Boxes in the middle that show work waiting.',
             donot=['Do not go on if another person\'s name is shown.'],
             alora='The dashboard is the first screen after login. Alora documents a dashboard that tracks pending work in one place.',
             astatus='FEATURE',
             zenith='Confirm your own name every time you sign in, before you open any patient.',
             ifwrong='Another name is shown: log out and **stop**. Tell the Administrator.'),
    ],
    final=['I signed in with my **own** username and password.', 'My own name is shown at the top right.',
           'The dashboard is open.', 'I did not save my password in the browser.', 'I did not share my password.'],
    stop=['You do not have your own username or password.', 'Your login fails twice.',
          'The sign-in page looks different from what the Administrator showed you, or asks for something unusual.',
          'The dashboard shows another person\'s name, or patient information you did not open.',
          'You cannot tell if the web address is correct.'],
    donot=['Do not use links from emails or texts to reach Alora.', 'Do not sign in on a personal computer or phone.',
           'Do not walk away while you are signed in. Press the **Windows key + L** to lock the computer.'],
)



# ----------------------------------------------------------------------------- P2 Understand the dashboard
def m_dash_1():
    m = S.dashboard()
    m.call(1, 'nav', 'Main menu', (170, 440), key='nav')
    m.call(2, 'search', 'Search box', (330, 84), key='search')
    m.call(3, 'user', 'Your name menu', (600, 84), key='user_menu')
    return m


def m_dash_2():
    m = S.dashboard()
    m.call(1, 'w_pending', 'Pending items box', (200, 330), key='dash_pending')
    m.call(2, 'pend.orders', 'Click one row', ('right', 0, 0), key='dash_pending')
    return m


def m_dash_3():
    m = S.dashboard()
    m.call(1, 'w_noa', 'NOA timely-filing box', (560, 84), key='dash_noa')
    m.call(2, 'noa_due', 'Five-day deadline', (560, 330), key='dash_noa')
    return m


def m_dash_4():
    m = S.patients_list(results=False, query=('', ''))
    m.call(1, 'nav.patients', 'You are here', (230, 350), key='nav_patients')
    m.call(2, 'nav.dash', 'Click to go back', (230, 300), key='nav_dash')
    return m


DASH = Proc(
    id='dashboard', tab=2, num='P2', title='Understand the Desktop Dashboard',
    purpose='The dashboard is the first screen you see after login. It shows the work that is waiting. '
            'This procedure teaches the three parts every Alora screen has, and the two dashboard boxes you will use most.',
    before=['You are signed in with your own name (P1).', 'The dashboard is open.'],
    who='Every office employee.', time='10 minutes the first time.',
    steps=[
        Step('dash-1', 'Find the menu, the search box and your name', m_dash_1,
             do=['Find the **main menu** down the left side. Each item opens a different area of Alora.',
                 'Find the **search box** at the top. You use it to look for a patient or a person.',
                 'Find **your own name** at the top right. You use it to see your account and to log out.'],
             check=['You can find all three parts without help.'],
             expect='You know where the menu, the search box and your name are.',
             see='A menu on the left, a search box at the top, your name at the top right, and boxes of work in the middle.',
             alora='Alora is a web-based system with a dashboard. The exact look, menu words and positions in Zenith\'s Alora must be confirmed.',
             zenith='Learn the three parts before you open any patient. Every other procedure in this manual starts from them.',
             ifwrong='Your screen has no search box or no menu: take a photo of the screen with your phone only if the Administrator allows it, then stop and ask.',
             key_note='Gray words in the picture only describe each area. Your Alora menu may use other words.'),
        Step('dash-2', 'Read the pending items box', m_dash_2,
             do=['Find the box that lists **pending items**: plans of care (485), orders and OASIS assessments.',
                 'Click **one row** to open the list behind it. Look, then return to the dashboard.'],
             check=['You see a number next to each kind of item.', 'You did not change anything.'],
             expect='You can see how many 485s, orders and OASIS items are waiting.',
             see='A box with rows for plans of care, orders and OASIS, each with a count.',
             donot=['Do not change an order, a plan of care or an OASIS. Office staff only look and report.'],
             alora='Alora documents that it can show pending 485 forms, orders and OASIS assessments in one place. The box name and its place on the dashboard must be verified.',
             astatus='FEATURE',
             zenith='Check this box at the start of each shift. Tell the DON about items that have been waiting more than 1 business day.',
             stop=['You do not see this box: stop and ask. Your role may not allow it.']),
        Step('dash-3', 'Read the NOA box', m_dash_3,
             do=['Find the box that shows **NOA** (Notice of Admission) work. It is about timely filing.',
                 'Read the **five-day deadline**. A late NOA lowers Medicare payment.'],
             check=['You know how many NOAs are waiting.'],
             expect='You know if an NOA is waiting and how much time is left.',
             see='A box with a number of NOAs to send and a reminder about the five-day deadline.',
             donot=['Do not send an NOA from this page unless you are the billing-authorized employee (P22).'],
             alora='Alora documents an NOA dashboard widget that tracks timely filing, and one-click NOA creation. The widget name and place must be verified.',
             astatus='FEATURE',
             rule='The NOA is due within 5 calendar days after the start of care. A late NOA reduces payment.',
             zenith='Only billing-authorized employees create or send an NOA. Everyone else looks and tells billing.'),
        Step('dash-4', 'Open an area and come back', m_dash_4,
             do=['You are in the **patients area**. The menu item is marked.',
                 'Click the **dashboard menu item** to go back to the dashboard.'],
             check=['You can go to an area and return without using the browser back arrow.'],
             expect='You are back on the dashboard.',
             see='The dashboard again, with your name at the top.',
             donot=['Do not use the browser Back arrow or Refresh while a form is open. You can lose what you typed.'],
             alora='Use the main menu to move between areas.',
             zenith='Always use the Alora menu to move around. Do not use the browser Back arrow inside a patient record.'),
    ],
    final=['I can find the main menu, the search box and my name.', 'I found the pending items box.', 'I found the NOA box.',
           'I can go to an area and return to the dashboard.', 'I did not change anything.'],
    stop=['A box mentioned here is missing from your dashboard.', 'Your role does not seem to allow what this manual tells you to do.',
          'You see a number that looks wrong (for example many items waiting for many days).'],
    donot=['Do not click buttons just to see what they do while a patient is open.', 'Do not leave a form half finished and move away.'],
)


# ----------------------------------------------------------------------------- P28 Security and HIPAA
def m_sec_1():
    m = S2.keyboard()
    m.call(1, 'key_win', 'Windows key', (190, 400), key='key_win')
    m.call(2, 'key_l', 'L key', (700, 270), key='key_l')
    return m


def m_sec_2():
    m = S2.dashboard_usermenu()
    m.call(1, 'user', 'Click your name', (430, 84), key='user_menu')
    m.call(2, 'logout', 'Log out choice', (560, 250), key='logout')
    return m


def m_sec_3():
    files = [('SMITH_MARY_REFERRAL_20260928.pdf', '09/28/2026 9:12 AM', '212 KB'),
             ('SMITH_MARY_ORDER_20260927.pdf', '09/28/2026 9:14 AM', '188 KB')]
    m = S.explorer(files, path='This PC  >  Documents  >  Zenith Scans  >  Ready to upload')
    m.call(1, 'win_file', 'Patient files waiting here', (300, 330), key='win_file')
    return m


SECURITY = Proc(
    id='security', tab=2, num='P28', title='Security and HIPAA Precautions',
    purpose='Patient information is private. This procedure shows the three habits that protect it at the office computer: lock it, log out, and keep files and paper safe.',
    before=['You are working at a Zenith office computer.', 'You have read the Zenith privacy policy (ask the Administrator).'],
    who='Every office employee, every day.', time='1 minute each time.',
    steps=[
        Step('sec-1', 'Lock the computer when you leave your seat', m_sec_1,
             do=['Hold down the **Windows key**.', 'While you hold it, press the **L** key once. Let go of both.'],
             check=['The screen changes to the lock screen.'],
             expect='The computer is locked. Nobody can see Alora or patient information.',
             see='A lock screen that asks for a password. Your work is hidden.',
             donot=['Do not leave Alora open and unlocked, even for one minute.'],
             alora='Not an Alora action. This is a Windows action.', astatus='ZENITH',
             zenith='Lock the computer every time you leave your seat, even to get water.',
             rule='HIPAA requires safeguards so that only authorized people see patient information.'),
        Step('sec-2', 'Log out of Alora at the end of the day', m_sec_2,
             do=['Click **your name** at the top right.', 'Click the **log out** choice.'],
             check=['You are back on the sign-in page.'],
             expect='You are logged out. The sign-in page is showing.',
             see='The sign-in page. Your name and all patient information are gone.',
             alora='Use your name menu to log out. The exact word for the choice must be verified.',
             zenith='Log out at the end of your shift and any time a different person will use the computer.',
             ifwrong='You cannot find the log out choice: **stop**, lock the computer (Windows key + L) and ask the Administrator.'),
        Step('sec-3', 'Keep scanned files and paper safe', m_sec_3,
             do=['Look in the scan folder for files that are already uploaded and **verified** in Alora. These can be removed.'],
             check=['No patient file stays in the scan folder after the upload is verified.', 'No patient paper is left on the desk.'],
             expect='The scan folder holds only files that still wait for upload.',
             see='A folder that has few or no files. Each file left is a patient file waiting for its turn.',
             donot=['Do not delete a file that is not yet verified in Alora.', 'Do not email or text a patient file.'],
             alora='Not an Alora action. This is a Zenith office rule.', astatus='ZENITH',
             zenith='Remove a scanned file from the scan folder only after the document is verified in Alora (P10). Follow the Administrator\'s instruction for the original paper: file it or use the locked shred bin.'),
    ],
    final=['I locked the computer when I left my seat.', 'I logged out of Alora at the end of my shift.',
           'No patient file is left in the scan folder without a reason.', 'No patient paper is left on my desk.'],
    stop=['You think someone used your login.', 'You see patient information on a screen, printer or fax you did not expect.',
          'A file or paper with patient information is lost.', 'Someone asks you for patient information and you are not sure they may have it.'],
    donot=['Do not share your password.', 'Do not take photos of patient information with a phone.', 'Do not use a personal email or text for patient information.',
           'Do not leave papers in the printer or fax tray.', 'Do not look at a patient record you do not need for your job.'],
)

HIPAA_PAGE = Text('hipaa', 2, 'HIPAA Precautions at the Office Computer', (
    '<h1 class="ttl">HIPAA precautions at the office computer</h1>'
    '<p class="sub">Read this page before your first day. Keep it in the binder.</p>'
    + GRID2(
        KBOX('Always', UL(['Use only your own login.', 'Lock the computer when you leave (Windows key + L).', 'Open only the patients you need for your job.',
                            'Check the patient name and birth date before you save anything.', 'Put papers away and close the scan folder.',
                            'Report a problem the same minute you notice it.']), 'green'),
        KBOX('Never', UL(['Share a password or let someone work under your login.', 'Take photos or screenshots of patient information on a personal phone.',
                          'Send patient information by personal email, text or social media.', 'Leave a patient screen open where visitors can read it.',
                          'Look at a record out of curiosity (family, friends, neighbors).', 'Discuss a patient where others can hear.']), 'red'))
    + H('What counts as patient information')
    + P('Any information that can point to one patient and relates to health or care: name, address, phone, birth date, insurance number, diagnosis, medicines, photos, orders, notes and scanned documents. '
        'If it can identify one patient, treat it as private.')
    + H('If something goes wrong')
    + OL(['Stop what you are doing.', 'Tell the Administrator right away. Do not wait until the end of the day.', 'Say what happened, when, and which patient. Do not guess and do not hide anything.',
          'Follow the Administrator\'s instructions.'])
    + KBOX('Federal rule', 'HIPAA requires each person to have a unique login, requires safeguards for patient information, and lets Zenith check who opened or changed a record. Act as if every click is recorded.', 'blue')
), kind='text')


HIPAA_PAGE.toc = True

PAGES = [Divider(2, 'Sign in, find your way around the dashboard, and protect patient information. Do these procedures before any other.',
                 [('login', 'P1  Log Into Alora'), ('dashboard', 'P2  Understand the Desktop Dashboard'), ('security', 'P28  Security and HIPAA Precautions'), ('hipaa', 'HIPAA precautions page')]),
         LOGIN, DASH, SECURITY, HIPAA_PAGE]

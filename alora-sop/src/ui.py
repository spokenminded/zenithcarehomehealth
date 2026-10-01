"""Registry of every screen element the manual tells staff to click or read.

Status rules (the manual never invents an Alora name):
  VERIFIED  the Administrator confirmed the name and location in live Alora (ui_map.json)
  FEATURE   Alora publicly documents this FEATURE by name, but the exact menu or button text
            and its location on screen still have to be verified in live Alora
  VERIFY    nothing public confirms the name or location. Verify in live Alora.
  WINDOWS   a standard Windows element (not Alora)
  ZENITH    a Zenith paper or printed form (not Alora)
"""
import json
from pathlib import Path

HERE = Path(__file__).parent

# key: (what it is, documented Alora feature name or None)
# Feature names below come from Alora's public product pages and review sites, as summarized in
# Appendix C of the manual. They name a feature, not a menu label.
REG = {
    # ---- browser and sign in
    'addr': ('Browser address bar', None),
    'browser_icon': ('Web browser icon', None),
    'taskbar': ('Windows taskbar', None),
    'login_user': ('Username box', None),
    'login_pass': ('Password box', None),
    'login_btn': ('Login button', None),
    'login_page': ('Alora sign in page', None),
    # ---- shell
    'dash_page': ('Dashboard', 'Dashboard'),
    'dash_pending': ('Pending 485s, orders, OASIS', 'Pending 485 forms, orders and OASIS shown in one place'),
    'dash_noa': ('NOA timely-filing widget', 'NOA dashboard widget for timely filing'),
    'dash_visits': ('Today\'s visits area', None),
    'nav': ('Main menu', None),
    'nav_dash': ('Dashboard menu item', 'Dashboard'),
    'nav_patients': ('Patients menu item', None),
    'nav_schedule': ('Schedule menu item', 'Scheduling'),
    'nav_clinical': ('Clinical menu item', None),
    'nav_qa': ('QA menu item', 'QA'),
    'nav_billing': ('Billing menu item', 'Billing'),
    'nav_reports': ('Reports menu item', None),
    'nav_staff': ('Staff menu item', 'HR functions'),
    'nav_messages': ('Messages menu item', 'Messaging'),
    'search': ('Search box (top of screen)', None),
    'user_menu': ('Your name menu', None),
    'logout': ('Log out choice', None),
    # ---- patients
    'pt_search_field': ('Patient search box', None),
    'pt_search_btn': ('Search button', None),
    'pt_results': ('Search results list', None),
    'pt_result_row': ('Correct patient row', None),
    'pt_open': ('Open patient record', None),
    'pt_banner': ('Patient name banner', None),
    'pt_tabs': ('Record sections', None),
    'tab_demo': ('Demographics section', None),
    'tab_docs': ('Documents section', 'Paperless records (scanned document storage)'),
    'tab_orders': ('Orders section', None),
    'tab_sched': ('Schedule section', None),
    'tab_clin': ('Clinical section', None),
    'tab_bill': ('Billing section', None),
    'tab_comm': ('Communication log section', 'Patient communication log'),
    'f_lname': ('Last name box', None),
    'f_fname': ('First name box', None),
    'f_dob': ('Date of birth box', None),
    'f_addr': ('Address box', None),
    'f_phone': ('Phone box', None),
    'f_lang': ('Preferred language box', None),
    'f_emerg': ('Emergency contact box', None),
    'f_payer': ('Insurance box', 'Insurance records (unlimited per patient)'),
    'f_phys': ('Physician box', 'Physician lookup from the NPI registry'),
    'f_memberid': ('Insurance ID box', None),
    'pt_none': ('No patients found message', None),
    'key_win': ('Windows key', None),
    'key_l': ('L key', None),
    'ref_date': ('Referral date and time', 'Intake and referral tracking'),
    'ref_src': ('Referral source', 'Intake and referral tracking'),
    'ref_status': ('Referral / admission status', 'Intake and referral tracking'),
    'pdf_name': ('Patient name on the page', None),
    'pdf_pages': ('Page count', None),
    'pdf_text': ('Readable text', None),
    'sch_row': ('Visit row', None),
    'lm_row_late': ('Late visit row', 'Live Monitor'),
    'lm_row_noshow': ('No-show row', 'Live Monitor'),
    'qa_row': ('QA item row', 'QA'),
    'bill_row': ('Billing row', None),
    'btn_send': ('Send button', None),
    'lm_open': ('Live Monitor (menu or link)', 'Live Monitor'),
    'bill_items': ('Patient billing items list', None),
    'staff_list': ('Staff list', 'HR functions'),
    'ex_return': ('Send back button', None),
    'f_refdate': ('Referral date box', None),
    'f_refsrc': ('Referral source box', None),
    'btn_edit': ('Edit button', None),
    'btn_save': ('Save button', None),
    'btn_new_pt': ('New patient / new referral button', 'Intake and referral tracking'),
    # ---- documents
    'docs_list': ('Document list', 'Paperless records (scanned document storage)'),
    'btn_upload': ('Add / upload document button', None),
    'dlg_file': ('Choose file button', None),
    'dlg_type': ('Document type list', None),
    'dlg_date': ('Document date box', None),
    'dlg_notes': ('Description / notes box', None),
    'dlg_save': ('Save button (upload window)', None),
    'dlg_cancel': ('Cancel button (upload window)', None),
    'doc_row': ('Document row', None),
    'doc_view': ('Open document (viewer)', None),
    'custom_docs': ('Custom Documents (Zenith forms)', 'Custom Documents'),
    # ---- windows
    'win_folder': ('Folder path (Windows)', None),
    'win_file': ('File list (Windows)', None),
    'win_filename': ('File name box (Windows)', None),
    'win_open': ('Open button (Windows)', None),
    # ---- schedule
    'sch_viewby': ('View by patient / team member / agency', 'Schedule views by patient, caregiver or agency'),
    'sch_range': ('Day / week / month / certification period', 'Schedule views by day, week, month or certification period'),
    'sch_grid': ('Schedule calendar', 'Scheduling'),
    'sch_visit': ('Visit on the calendar', None),
    'sch_add': ('Add visit button', 'Batch entry scheduling'),
    'f_visit_pt': ('Patient box (visit)', None),
    'f_visit_type': ('Visit type / discipline box', None),
    'f_visit_date': ('Visit date box', None),
    'f_visit_time': ('Visit time box', None),
    'f_visit_member': ('Team member box', None),
    'f_visit_freq': ('Repeat / frequency box', None),
    'sch_alerts': ('Scheduling alerts', 'Conflict and compliance alerts (authorization, visit frequency)'),
    'sch_reason': ('Reason for change box', None),
    # ---- monitoring
    'lm_table': ('Live Monitor list', 'Live Monitor'),
    'lm_status': ('Visit status colors', 'Color-coded delay and no-show warnings'),
    'ex_list': ('EVV exceptions list', 'Visits held for manual review before they are sent'),
    'ex_row': ('Exception row', None),
    'ex_issue': ('What does not match', None),
    'ex_reason': ('Reason box', None),
    'ex_approve': ('Approve button', None),
    # ---- clinical review and QA
    'cl_pending': ('Pending clinical items', 'Pending 485 forms, orders and OASIS shown in one place'),
    'cl_oasis': ('OASIS row', 'OASIS with scrubber'),
    'cl_485': ('Plan of care (485) row', 'Plan of care (CMS-485)'),
    'cl_order': ('Order row', None),
    'qa_area': ('QA screen', 'QA'),
    'qa_items': ('QA items list', 'QA'),
    'qa_return': ('Return for correction', None),
    # ---- billing
    'bill_ready': ('Billing status list', 'Billing for all payers'),
    'noa_widget': ('NOA widget', 'NOA dashboard widget for timely filing'),
    'noa_row': ('Patient row in NOA list', None),
    'noa_gen': ('Create NOA button', 'One-click NOA generation'),
    'noa_status': ('NOA status', None),
    'efax': ('Electronic fax tool', 'Built-in electronic faxing'),
}

# Elements that are not Alora at all. They are never "unverified Alora" items.
WINDOWS_KEYS = {'pdf_name', 'pdf_pages', 'pdf_text', 'key_win', 'key_l', 'win_folder', 'win_file', 'win_filename', 'win_open', 'addr', 'browser_icon', 'taskbar'}


def _load_overrides():
    p = HERE / 'ui_map.json'
    if p.exists():
        return json.loads(p.read_text(encoding='utf-8'))
    return {}


OVERRIDES = _load_overrides()


def status(key):
    """Return one of VERIFIED, FEATURE, VERIFY, WINDOWS, ZENITH."""
    if key is None or key == 'zenith':
        return 'ZENITH'
    if key in WINDOWS_KEYS:
        return 'WINDOWS'
    ov = OVERRIDES.get(key)
    if ov and ov.get('verified'):
        return 'VERIFIED'
    desc, feat = REG[key]
    return 'FEATURE' if feat else 'VERIFY'


def label(key, fallback=None):
    """Text shown in the callout pill. A verified real name replaces the descriptive text."""
    if key in (None, 'zenith'):
        return fallback or ''
    ov = OVERRIDES.get(key)
    if ov and ov.get('verified') and ov.get('name'):
        return ov['name']
    return fallback or REG[key][0]


def all_keys():
    return list(REG.keys())

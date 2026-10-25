import html
from collections import Counter
from datetime import date

import pandas as pd
import streamlit as st
from supabase import create_client


# ------------------------------------------------------------
# AarogyaSakhi — a beginner-friendly women's health support prototype
# ------------------------------------------------------------

st.set_page_config(
    page_title="AarogyaSakhi | Women's Health Companion",
    page_icon="🌷",
    layout="wide",
)

st.markdown(
    """
    <style>
      :root {
        --as-bg: #170d1b;
        --as-panel: #29162c;
        --as-panel-2: #38203d;
        --as-line: #754464;
        --as-text: #fff2fa;
        --as-muted: #e2cadd;
        --as-pink: #ff78b7;
        --as-pink-light: #ffc4e2;
        --as-mint: #b9f1df;
        --as-gold: #f5d4a6;
      }
      html, body, [class*="css"] { color: var(--as-text); }
      .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background:
          radial-gradient(ellipse at 8% 0%, rgba(199, 181, 255, .16), transparent 33%),
          radial-gradient(ellipse at 92% 12%, rgba(158, 223, 208, .10), transparent 28%),
          var(--as-bg);
        color: var(--as-text);
      }
      [data-testid="stHeader"] { background: rgba(23, 19, 33, .92); }
      [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1440px; padding-top: 1.5rem; padding-bottom: 3rem;
      }
      h1, h2, h3, h4, h5 { color: #fff !important; letter-spacing: -.025em; }
      h2 { margin-top: 1.1rem; }
      p, li, .stMarkdown, [data-testid="stCaptionContainer"] {
        color: var(--as-text);
      }
      [data-testid="stCaptionContainer"] p, .small-note {
        color: var(--as-muted) !important; font-size: .9rem;
      }
      a, a:visited { color: var(--as-pink-light) !important; }
      a:hover { color: #fff !important; }

      /* Strong brand hero */
      .hero {
        position: relative; overflow: hidden;
        padding: 2.1rem 2.2rem 1.9rem; border-radius: 26px;
        background: linear-gradient(118deg, #4b2348 0%, #302039 52%, #243d48 100%);
        border: 1px solid #6d4e76; margin-bottom: 1.15rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, .28);
      }
      .hero::after {
        content: ""; position: absolute; width: 260px; height: 260px;
        border-radius: 50%; right: -70px; top: -125px;
        border: 1px solid rgba(255,255,255,.13);
        box-shadow: 0 0 0 28px rgba(255,255,255,.025), 0 0 0 58px rgba(255,255,255,.02);
        pointer-events: none;
      }
      .hero-top { display:flex; flex-wrap:wrap; align-items:center; gap:.6rem; margin-bottom:1.15rem; }
      .eyebrow {
        display:inline-block; color:#ffd7ec; background:rgba(255,120,183,.17);
        border:1px solid rgba(244,181,219,.4); border-radius:999px;
        padding:.38rem .75rem; font-size:.73rem; font-weight:800; letter-spacing:.09em;
      }
      .hero-badge { color:#b9ffe8; font-size:.78rem; font-weight:700; }
      .hero h1 { margin:0 0 .55rem 0; font-size:clamp(2.5rem, 5vw, 4rem); line-height:1.02; font-weight:850; }
      .hero-accent { color:#f4b5db; }
      .hero p { margin:.5rem 0 1.2rem; max-width:760px; color:#f0eefa; font-size:1.08rem; line-height:1.65; }
      .hero-tags { display:flex; flex-wrap:wrap; gap:.55rem; }
      .hero-tags span { border:1px solid rgba(255,255,255,.18); background:rgba(10,14,30,.22); color:#f7f4ff; border-radius:999px; padding:.42rem .75rem; font-size:.8rem; }
      .prototype-note { margin:.8rem 0 1.3rem; padding:.8rem 1rem; border-radius:12px; border:1px solid #35405f; border-left:4px solid var(--as-gold); background:#151b2c; color:#e8eaf4; font-size:.88rem; line-height:1.5; }

      /* Navigation and sidebar */
      [data-testid="stSidebar"] { background:linear-gradient(180deg, #2b142b 0%, #170d1b 100%); border-right:1px solid #40304b; }
      [data-testid="stSidebar"] > div:first-child { background:transparent; }
      [data-testid="stSidebar"] * { color:var(--as-text); }
      .side-brand { display:flex; align-items:center; gap:.75rem; margin:.25rem 0 1.2rem; padding:.85rem .7rem; border-radius:16px; background:linear-gradient(110deg, rgba(255,120,183,.20), rgba(158,223,208,.08)); border:1px solid #55405f; }
      .side-logo { width:43px; height:43px; display:flex; align-items:center; justify-content:center; border-radius:14px; background:linear-gradient(145deg,#ff78b7,#b48bff); color:#fff; font-weight:900; font-size:1rem; box-shadow:0 8px 20px rgba(233,140,197,.2); }
      .side-title { font-size:1rem; font-weight:800; color:#fff; line-height:1.2; }
      .side-subtitle { font-size:.73rem; color:#bac3db; margin-top:.22rem; }
      [data-testid="stSidebar"] [data-testid="stRadio"] label { padding:.45rem .5rem; border-radius:10px; }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:#4b2850; }
      [data-testid="stSidebar"] hr { border-color:#303853; }

      /* Elevated cards, metric tiles and forms */
      .feature-card { min-height:174px; padding:1.15rem; border-radius:18px; border:1px solid #55405f; background:linear-gradient(150deg,#3b2140,#26142b); box-shadow:0 10px 25px rgba(0,0,0,.13); }
      .feature-icon { width:46px; height:46px; display:flex; align-items:center; justify-content:center; border-radius:14px; font-size:1.45rem; background:rgba(255,120,183,.20); margin-bottom:.8rem; }
      .feature-title { color:#fff; font-size:1.08rem; font-weight:800; margin-bottom:.35rem; }
      .feature-copy { color:#c4cbe0; font-size:.9rem; line-height:1.55; }
      div[data-testid="stMetric"] { background:linear-gradient(145deg,#302039,#211829); border:1px solid #55405f; padding:1rem 1.05rem; border-radius:16px; box-shadow:0 8px 22px rgba(0,0,0,.12); }
      div[data-testid="stMetricLabel"] { color:#c4cbe0 !important; }
      div[data-testid="stMetricLabel"] p { color:#c4cbe0 !important; font-size:.82rem; font-weight:650; }
      div[data-testid="stMetricValue"] { color:#fff !important; font-weight:800; }
      div[data-testid="stMetricDelta"] { color:var(--as-mint) !important; }
      [data-testid="stForm"] { border:1px solid #34405f; border-radius:18px; padding:1.1rem 1.2rem; background:rgba(41,22,44,.92); }
      label, [data-testid="stWidgetLabel"] p { color:#f2f4fb !important; font-weight:600; }
      [data-baseweb="input"] > div, [data-baseweb="textarea"] > div,
      [data-baseweb="select"] > div, [data-testid="stDateInput"] input {
        background:#241329 !important; border:1px solid #66506f !important; color:#fff !important; border-radius:10px !important;
      }
      [data-baseweb="input"] input, [data-baseweb="textarea"] textarea,
      [data-baseweb="select"] *, [data-testid="stDateInput"] input { color:#fff !important; -webkit-text-fill-color:#fff !important; }
      [data-baseweb="input"] input::placeholder, [data-baseweb="textarea"] textarea::placeholder { color:#9da8c4 !important; -webkit-text-fill-color:#9da8c4 !important; }
      [role="listbox"], [role="option"] { background:#29162c !important; color:#fff !important; }
      [data-testid="stCheckbox"] label, [data-testid="stRadio"] label { color:#f2f4fb !important; }
      [data-testid="stSlider"] [data-testid="stTickBarMin"], [data-testid="stSlider"] [data-testid="stTickBarMax"] { color:#c4cbe0 !important; }

      /* Buttons and feedback */
      .stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
        border-radius:12px; border:1px solid #6b4b79; font-weight:750; min-height:2.65rem;
        transition:transform .15s ease, box-shadow .15s ease;
      }
      .stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { transform:translateY(-1px); box-shadow:0 8px 22px rgba(255,120,183,.30); border-color:var(--as-pink); }
      button[kind="primary"], [data-testid="stFormSubmitButton"] button[kind="primary"] { background:linear-gradient(105deg,#ff78b7 0%,#d98cff 52%,#a98bff 100%) !important; color:#fff !important; border:0 !important; }
      [data-testid="stAlert"] { border-radius:14px; border:1px solid #35415f; background:#3b2140; color:#f5f7ff; }
      [data-testid="stAlert"] * { color:#f5f7ff; }
      [data-testid="stExpander"] details { border:1px solid #34405f; border-radius:14px; background:#29162c; }
      [data-testid="stExpander"] summary { color:#f7f8fc; }
      [data-testid="stDataFrame"] { border:1px solid #34405f; border-radius:12px; overflow:hidden; }
      .resource-card { padding:1.15rem; border:1px solid #34405f; border-radius:16px; background:linear-gradient(145deg,#302039,#211829); margin:.5rem 0 .8rem; }
      .resource-card h3 { margin:.1rem 0 .6rem; color:#f4b5db !important; }
      .resource-card p { color:#e1e6f5; line-height:1.55; }
      .resource-card a { font-weight:700; }
      [data-testid="stTabs"] [data-baseweb="tab-list"] { gap:.4rem; }
      [data-testid="stTabs"] button[role="tab"] { background:#29162c; border-radius:10px 10px 0 0; color:#d5c3dc; }
      [data-testid="stTabs"] button[aria-selected="true"] { color:#fff; border-bottom:3px solid var(--as-pink); }
      hr { border-color:#303853; }
      /* Smooth, accessible motion: restrained hover lift and focus rings. */
      .feature-card, .resource-card, div[data-testid="stMetric"],
      [data-testid="stExpander"] details, [data-testid="stTabs"] button[role="tab"] {
        transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease, background .18s ease;
      }
      .feature-card:hover, .resource-card:hover, div[data-testid="stMetric"]:hover {
        transform: translateY(-2px); border-color: #a86d9b;
        box-shadow: 0 12px 28px rgba(233,140,197,.10);
      }
      .stButton > button:focus-visible, .stDownloadButton > button:focus-visible,
      [data-testid="stRadio"] label:focus-within {
        outline: 2px solid #c7b5ff !important; outline-offset: 2px;
      }
      [data-testid="stSidebar"] [data-testid="stRadio"] label {
        transition: background .16s ease, border-color .16s ease, transform .16s ease;
        border: 1px solid transparent; margin: .12rem 0;
      }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background:#4b2850; border-color:#55405f; transform:translateX(2px);
      }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background:linear-gradient(100deg, rgba(233,140,197,.18), rgba(199,181,255,.10));
        border-color:#b45a8d;
      }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p { color:#fff1fa !important; font-weight:800; }
      footer { visibility:hidden; }
      @media (max-width: 768px) { .hero { padding:1.35rem; } .hero h1 { font-size:2.5rem; } .feature-card { min-height:0; } }

      /* Blush Bloom design refresh: typography, richer rose tones, and real entrance motion. */
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');
      :root {
        --as-rose: #ff78b7;
        --as-blush: #ffc4e2;
        --as-lilac: #c8a5ff;
        --as-plum: #170d1b;
      }
      html, body, [class*="css"], button, input, textarea, select {
        font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
      }
      h1, h2, h3, h4, h5, .hero h1, .feature-title, .side-title {
        font-family: 'Playfair Display', Georgia, serif !important;
      }
      h1, h2, h3 { text-shadow: 0 2px 24px rgba(255,120,183,.08); }
      .hero {
        background:
          radial-gradient(circle at 88% 10%, rgba(255,196,226,.20), transparent 28%),
          linear-gradient(125deg, #76284f 0%, #492044 48%, #32204c 100%);
        border-color: rgba(255,196,226,.42);
        box-shadow: 0 20px 60px rgba(13,4,18,.38), 0 0 35px rgba(255,120,183,.08);
        animation: asBloomIn .72s cubic-bezier(.2,.8,.2,1) both;
      }
      .hero h1 { letter-spacing: -.035em; }
      .hero-accent {
        background: linear-gradient(100deg, #ffc4e2, #d8bdff 72%, #b9f1df);
        -webkit-background-clip: text; background-clip: text; color: transparent;
      }
      .eyebrow { background:rgba(255,120,183,.19); border-color:rgba(255,196,226,.55); }
      .feature-card, .resource-card, div[data-testid="stMetric"], [data-testid="stForm"] {
        border-color: rgba(255,196,226,.22);
        box-shadow: 0 10px 28px rgba(12,4,18,.20);
        backdrop-filter: blur(8px);
      }
      .feature-card:hover, .resource-card:hover, div[data-testid="stMetric"]:hover {
        transform: translateY(-4px) scale(1.008);
        border-color: rgba(255,120,183,.8);
        box-shadow: 0 18px 38px rgba(255,120,183,.15), 0 0 0 1px rgba(200,165,255,.10);
      }
      .feature-icon { background:linear-gradient(145deg,rgba(255,120,183,.25),rgba(200,165,255,.20)); border:1px solid rgba(255,196,226,.18); }
      .feature-title, .resource-card h3 { color:#ffc4e2 !important; }
      .stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
        transition: transform .22s cubic-bezier(.2,.8,.2,1), box-shadow .22s ease, filter .22s ease, border-color .22s ease !important;
      }
      .stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        transform:translateY(-2px) scale(1.015) !important;
        box-shadow:0 10px 28px rgba(255,120,183,.32), 0 0 18px rgba(200,165,255,.16) !important;
        filter:saturate(1.12);
      }
      button[kind="primary"], [data-testid="stFormSubmitButton"] button[kind="primary"] {
        background:linear-gradient(110deg,#ff78b7 0%,#df8cff 58%,#ad8bff 100%) !important;
        box-shadow:0 6px 20px rgba(255,120,183,.16);
      }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background:linear-gradient(100deg,rgba(255,120,183,.24),rgba(200,165,255,.16));
        border-color:rgba(255,196,226,.62);
        box-shadow:inset 3px 0 0 #ff78b7;
      }
      [data-testid="stTabs"] button[role="tab"] { transition:all .2s ease; }
      [data-testid="stTabs"] button[role="tab"]:hover { color:#ffc4e2; background:#422047; }
      [data-testid="stExpander"] details { transition:all .22s ease; }
      [data-testid="stExpander"] details:hover { border-color:rgba(255,120,183,.55); }
      [data-testid="stMainBlockContainer"] > div { animation: asSoftRise .48s ease both; }
      @keyframes asBloomIn {
        from { opacity:0; transform:translateY(12px) scale(.99); }
        to { opacity:1; transform:translateY(0) scale(1); }
      }
      @keyframes asSoftRise {
        from { opacity:0; transform:translateY(7px); }
        to { opacity:1; transform:translateY(0); }
      }
      @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation-duration:.01ms !important; animation-iteration-count:1 !important; transition-duration:.01ms !important; scroll-behavior:auto !important; }
      }

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="hero-top">
        <span class="eyebrow">YOUR PERSONAL HEALTH SPACE ✨</span>
        <span class="hero-badge">♡ Your story matters</span>
      </div>
      <h1>Aarogya<span class="hero-accent">Sakhi</span></h1>
      <p><strong>Your health deserves the main character treatment.</strong><br>A calmer, clearer way to track what you notice, connect the dots, and feel more prepared for a healthcare conversation — no self-diagnosis required.</p>
      <div class="hero-tags">
        <span>♡ The Daily Debrief</span>
        <span>✧ Connect the Dots</span>
        <span>🩺 Doctor-ready reports</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """<div class="prototype-note"><strong>💗 A little transparency:</strong> This website is for education and appointment preparation, not diagnosis. Use fictional data for public demos. Entries are saved to your signed-in account. Avoid entering unnecessary identifying details.</div>""",
    unsafe_allow_html=True,
)

# Supabase sign-in is required so each person's entries stay private.
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    st.error("Add SUPABASE_URL and SUPABASE_KEY in Streamlit Cloud → App settings → Secrets.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
if st.session_state.get("supabase_access_token") and st.session_state.get("supabase_refresh_token"):
    try:
        supabase.auth.set_session(st.session_state.supabase_access_token, st.session_state.supabase_refresh_token)
    except Exception:
        for k in ("supabase_access_token", "supabase_refresh_token", "user_id", "user_email", "data_loaded"):
            st.session_state.pop(k, None)

if not st.session_state.get("user_id"):
    st.title("🌷 Welcome to AarogyaSakhi")
    st.write("Create an account or log in to save your diary and lab entries privately.")
    tab_login, tab_signup = st.tabs(["Log in", "Create account"])
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email address", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            do_login = st.form_submit_button("Log in", type="primary")
        if do_login:
            try:
                result = supabase.auth.sign_in_with_password({"email": email.strip(), "password": password})
                if result.user and result.session:
                    st.session_state.supabase_access_token = result.session.access_token
                    st.session_state.supabase_refresh_token = result.session.refresh_token
                    st.session_state.user_id = result.user.id
                    st.session_state.user_email = result.user.email
                    st.rerun()
                else:
                    st.error("No active session was returned. Check your email confirmation.")
            except Exception:
                st.error("Login failed. Check your email and password, and confirm your email if required.")
    with tab_signup:
        with st.form("signup_form"):
            new_email = st.text_input("Email address", key="signup_email")
            new_password = st.text_input("Create a password (8+ characters)", type="password", key="signup_password")
            do_signup = st.form_submit_button("Create account", type="primary")
        if do_signup:
            if len(new_password) < 8:
                st.error("Please use a password with at least 8 characters.")
            else:
                try:
                    result = supabase.auth.sign_up({"email": new_email.strip(), "password": new_password})
                    if result.user and result.session:
                        st.session_state.supabase_access_token = result.session.access_token
                        st.session_state.supabase_refresh_token = result.session.refresh_token
                        st.session_state.user_id = result.user.id
                        st.session_state.user_email = result.user.email
                        st.rerun()
                    else:
                        st.success("Account created. Check your email to confirm it, then log in.")
                except Exception:
                    st.error("Account creation failed. Check the email address and try again.")
    st.caption("Use a unique password and avoid entering unnecessary identifying details.")
    st.stop()

if not st.session_state.get("data_loaded"):
    try:
        symptoms_db = supabase.table("symptom_entries").select("*").eq("user_id", st.session_state.user_id).order("entry_date", desc=True).execute()
        labs_db = supabase.table("lab_entries").select("*").eq("user_id", st.session_state.user_id).order("created_at", desc=True).execute()
        st.session_state.symptom_entries = [{
            "_db_id": row["id"], "date": row["entry_date"], "cycle_day": row.get("cycle_day"),
            "pain": row.get("pain", 0), "fatigue": row.get("fatigue", 0), "mood": row.get("mood", "Choose not to say"),
            "symptoms": row.get("symptoms") or [], "impact": row.get("impact", "No noticeable effect"), "notes": row.get("notes") or ""
        } for row in symptoms_db.data]
        st.session_state.lab_entries = [{**(row.get("entry_data") or {}), "_db_id": row["id"]} for row in labs_db.data]
        st.session_state.last_saved_lab = st.session_state.lab_entries[0] if st.session_state.lab_entries else None
        st.session_state.data_loaded = True
    except Exception:
        st.error("Saved entries could not be loaded. Check the Supabase tables, RLS policies, and secrets.")
        st.stop()

# Entries are loaded from Supabase after authentication.
if "symptom_entries" not in st.session_state:
    st.session_state.symptom_entries = []
if "lab_entries" not in st.session_state:
    st.session_state.lab_entries = []
if "last_saved_lab" not in st.session_state:
    st.session_state.last_saved_lab = None


TEST_INFO = {
    "Hemoglobin (Hb)": {
        "meaning": "Hemoglobin is a protein in red blood cells that carries oxygen around the body. It is often reported as part of a complete blood count (CBC).",
        "questions": [
            "How should I interpret this result alongside the rest of my blood count and my symptoms?",
            "Is any follow-up needed, and what could affect this result?",
        ],
    },
    "TSH": {
        "meaning": "TSH is a signal from the brain's pituitary gland that helps regulate the thyroid. Clinicians may interpret it with symptoms and, when appropriate, a free T4 result.",
        "questions": [
            "Does this result need to be interpreted alongside free T4 or other information?",
            "Could my symptoms have another explanation, and is follow-up needed?",
        ],
    },
    "Vitamin D (25-OH)": {
        "meaning": "The 25-hydroxy vitamin D blood test is commonly used to assess vitamin D status. The result should be interpreted using the lab's own reference information and your clinical context.",
        "questions": [
            "What does this result mean against this laboratory's reference interval?",
            "Do I need any follow-up, and should I discuss food, supplements, or other factors with you?",
        ],
    },
    "Other test": {
        "meaning": "This app does not have a specific explanation for this test. Ask the clinician who ordered it or the laboratory to explain what it measures and how your result should be interpreted.",
        "questions": [
            "What does this test measure, and why was it ordered?",
            "How does my result compare with the reference interval on this report?",
            "Does it change my next steps or require follow-up?",
        ],
    },
}


def safe_text(value):
    """Escape user-entered text before inserting it into a downloadable HTML report."""
    return html.escape(str(value if value is not None else ""))


def make_printable_report(symptoms, labs):
    """Create a printable HTML health summary. Open the downloaded file and press Ctrl+P."""
    created_on = date.today().strftime("%d %b %Y")
    symptom_rows = ""
    for entry in sorted(symptoms, key=lambda item: item["date"]):
        cycle = entry["cycle_day"] if entry["cycle_day"] else "Not recorded"
        symptom_rows += (
            "<tr>"
            f"<td>{safe_text(entry['date'])}</td>"
            f"<td>{safe_text(cycle)}</td>"
            f"<td>{safe_text(entry['pain'])}/10</td>"
            f"<td>{safe_text(entry['fatigue'])}/10</td>"
            f"<td>{safe_text(entry['mood'])}</td>"
            f"<td>{safe_text(', '.join(entry['symptoms']))}</td>"
            f"<td>{safe_text(entry['impact'])}</td>"
            f"<td>{safe_text(entry['notes'])}</td>"
            "</tr>"
        )
    if not symptom_rows:
        symptom_rows = '<tr><td colspan="8">No symptom entries recorded.</td></tr>'

    lab_rows = ""
    for entry in labs:
        lab_rows += (
            "<tr>"
            f"<td>{safe_text(entry['date'])}</td>"
            f"<td>{safe_text(entry['test'])}</td>"
            f"<td>{safe_text(entry['result'])} {safe_text(entry['unit'])}</td>"
            f"<td>{safe_text(entry['reference']) or 'Not entered'}</td>"
            f"<td>{safe_text(entry['lab_flag'])}</td>"
            f"<td>{safe_text(entry['notes'])}</td>"
            "</tr>"
        )
    if not lab_rows:
        lab_rows = '<tr><td colspan="6">No lab results added.</td></tr>'

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>AarogyaSakhi Health Summary</title>
<style>
body {{ font-family: Arial, sans-serif; color: #222; margin: 28px; line-height: 1.4; }}
h1, h2 {{ color: #38245d; }}
.note {{ background: #f6f1ff; border-left: 4px solid #9b83d8; padding: 10px; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0 24px; font-size: 12px; }}
th, td {{ border: 1px solid #ccc; padding: 7px; text-align: left; vertical-align: top; }}
th {{ background: #eee8fa; }}
@media print {{ body {{ margin: 12mm; }} .no-print {{ display: none; }} tr {{ page-break-inside: avoid; }} }}
</style></head><body>
<h1>AarogyaSakhi — Personal Health Summary</h1>
<p>Prepared on {safe_text(created_on)}. This summary contains user-entered information, not a diagnosis.</p>
<div class="note"><strong>For your appointment:</strong> Please review this summary for accuracy before sharing it. Your clinician can interpret it in context.</div>
<h2>Symptom diary</h2>
<table><thead><tr><th>Date</th><th>Cycle day</th><th>Pain</th><th>Fatigue</th><th>Mood</th><th>Symptoms</th><th>Daily impact</th><th>Notes</th></tr></thead>
<tbody>{symptom_rows}</tbody></table>
<h2>Lab results entered</h2>
<table><thead><tr><th>Date</th><th>Test</th><th>Result</th><th>Lab reference interval</th><th>Lab's own flag</th><th>Notes</th></tr></thead>
<tbody>{lab_rows}</tbody></table>
<p><strong>Reminder:</strong> Reference intervals can vary by laboratory and personal circumstances. Discuss results and next steps with a qualified healthcare professional.</p>
<p class="no-print">To print or save as PDF: open this file in a browser and press Ctrl+P (Windows) or Cmd+P (Mac).</p>
</body></html>"""


st.sidebar.markdown(
    """<div class="side-brand"><div class="side-logo">AS</div><div><div class="side-title">AarogyaSakhi</div><div class="side-subtitle">Women's health companion</div></div></div><div style="color:#9ca8c7;font-size:.72rem;font-weight:800;letter-spacing:.12em;margin:0 0 .55rem .35rem;">YOUR WORKSPACE</div>""",
    unsafe_allow_html=True,
)
workspace_labels = {
    "🏠 Home · The Welcome Lounge": "Home",
    "📊 Statistics · The Bigger Picture": "Statistics & Insights",
    "📝 Symptoms · The Daily Debrief": "Symptom Diary",
    "🔮 Patterns · Connect the Dots": "Pattern Insights & Report",
    "💬 Health Guide · Let's Talk Symptoms": "Health Check-in Guide",
    "🧪 Lab Results · Translated": "Understand Lab Results",
    "💌 Resources · Your Health Library": "Help & Resources",
}
selected_workspace = st.sidebar.radio(
    "Choose a workspace — it opens when you select it",
    list(workspace_labels.keys()),
    label_visibility="visible",
    key="aarogyasakhi_workspace",
)
page = workspace_labels[selected_workspace]
st.sidebar.markdown("---")
st.sidebar.caption(f"Signed in as {st.session_state.get('user_email', 'your account')}")
if st.sidebar.button("Log out"):
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    for key in ("supabase_access_token", "supabase_refresh_token", "user_id", "user_email", "data_loaded", "symptom_entries", "lab_entries", "last_saved_lab"):
        st.session_state.pop(key, None)
    st.rerun()
st.sidebar.caption("Your diary and lab entries are saved to your account.")


if page == "Home":
    st.subheader("Hey, lovely. 💗 Let’s make sense of your health.")
    st.caption("Your health deserves the main character treatment — with reliable information, not guesswork.")
    st.write(
        "AarogyaSakhi helps you organise what you notice, see simple summaries of what you logged, "
        "and prepare questions for a healthcare professional. It does not diagnose conditions."
    )
    st.markdown("### Your little health toolkit ✨")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="feature-card"><div class="feature-icon">📝</div><div class="feature-title">The Daily Debrief 📝</div><div class="feature-copy">How are we feeling, really? Record pain, fatigue, mood, cycle day, and how symptoms affect everyday life.</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Connect the Dots 🔮</div><div class="feature-copy">Your recorded trends, made clearer — then download a health-visit summary.</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="feature-card"><div class="feature-icon">🩺</div><div class="feature-title">The Doctor’s Cheat Sheet 🩺</div><div class="feature-copy">Organise questions for a clinician. Because appointments shouldn’t feel like pop quizzes.</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Your current session")
    m1, m2 = st.columns(2)
    m1.metric("Symptom entries", len(st.session_state.symptom_entries))
    m2.metric("Lab results added", len(st.session_state.lab_entries))
    st.info("New here? Start with **📝 Symptoms · The Daily Debrief**. Then visit **🔮 Patterns · Connect the Dots** to review your entries.")
    st.caption("Urgent or severe symptoms should be assessed by a qualified healthcare professional; do not wait for an app summary.")

    st.markdown("---")
    st.markdown("### Why women’s health awareness matters 💗")
    stat1, stat2, stat3 = st.columns(3)
    with stat1:
        st.metric("PCOS prevalence", "10–13%")
        st.caption("Estimated among reproductive-aged women worldwide. WHO also estimates that up to 70% of affected women are undiagnosed.")
    with stat2:
        st.metric("Endometriosis", "~10%")
        st.caption("An estimated 190 million women of reproductive age worldwide are affected.")
    with stat3:
        st.metric("Anaemia in India", "57%")
        st.caption("Women aged 15–49, reported by NFHS-5 (2019–21).")
    st.markdown("Explore **Statistics & Insights** in the sidebar for source links and more context.")


elif page == "Statistics & Insights":
    st.subheader("📊 The Bigger Picture · Women’s Health")
    st.write("These figures show why awareness, symptom documentation, and access to clear health information matter. They are population-level estimates—not predictions about an individual user.")

    left, middle, right = st.columns(3)
    with left:
        st.metric("PCOS prevalence", "10–13%")
        st.write("WHO estimates PCOS affects about 10–13% of reproductive-aged women worldwide.")
        st.metric("PCOS awareness gap", "Up to 70%")
        st.write("WHO estimates that up to 70% of women with PCOS worldwide do not know they have it.")
    with middle:
        st.metric("Endometriosis", "~10%")
        st.write("An estimated 190 million women of reproductive age worldwide are affected by endometriosis.")
        st.info("WHO notes that delays in diagnosis are common. Symptoms and severity vary, and symptom lists cannot confirm or rule out endometriosis.")
    with right:
        st.metric("Anaemia in India", "57.0%")
        st.write("NFHS-5 (2019–21) reported anaemia among about 57% of women aged 15–49 in India.")
        st.info("This is a national survey estimate from 2019–21, not a real-time figure or a measure of any individual user's health.")

    st.markdown("### What these statistics mean for AarogyaSakhi")
    st.markdown("""
- **Notice patterns:** a symptom diary can help users describe timing, severity, and impact during a consultation. It cannot identify the cause by itself.
- **Prepare better questions:** a concise summary may help users communicate concerns they might otherwise forget.
- **Understand health information:** clear explanations can help users ask clinicians about symptoms and test results without relying on self-diagnosis.
""")

    st.markdown("### Sources")
    st.markdown("1. [WHO — Polycystic ovary syndrome (22 January 2026)](https://www.who.int/news-room/fact-sheets/detail/polycystic-ovary-syndrome/)")
    st.markdown("2. [WHO — Endometriosis (15 October 2025)](https://www.who.int/news-room/fact-sheets/detail/endometriosis)")
    st.markdown("3. [Ministry of Health and Family Welfare — Health and Family Welfare Statistics in India 2023 (NFHS-5 data, 2019–21)](https://www.mohfw.gov.in/sites/default/files/Publication%20Health%20and%20Family%20Welfare%20Statistics%20in%20India%202023.pdf)")
    st.caption("Estimates refer to different conditions, populations, and survey periods; they should not be compared as though they measured the same thing. Sources last checked for this prototype on 24 October 2026.")

    st.markdown("---")
    st.markdown("### Statistics from your current session")
    entries = st.session_state.symptom_entries
    labs = st.session_state.lab_entries
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Diary entries", len(entries))
    m2.metric("Lab results", len(labs))
    if entries:
        mean_pain = sum(int(x["pain"]) for x in entries) / len(entries)
        mean_fatigue = sum(int(x["fatigue"]) for x in entries) / len(entries)
        m3.metric("Average pain", f"{mean_pain:.1f}/10")
        m4.metric("Average fatigue", f"{mean_fatigue:.1f}/10")
        symptom_counts = Counter(symptom for row in entries for symptom in row["symptoms"])
        if symptom_counts:
            st.markdown("**Most frequently logged symptoms in this session**")
            counts_df = pd.DataFrame(symptom_counts.most_common(), columns=["Symptom", "Entries"])
            st.bar_chart(counts_df.set_index("Symptom"))
        if len(entries) >= 2:
            date_df = pd.DataFrame(entries)
            date_df["date"] = pd.to_datetime(date_df["date"])
            date_df = date_df.sort_values("date").groupby("date", as_index=True)[["pain", "fatigue"]].mean()
            date_df = date_df.rename(columns={"pain": "Pain (0–10)", "fatigue": "Fatigue (0–10)"})
            st.markdown("**Your pain and fatigue ratings over time**")
            st.line_chart(date_df)
        else:
            st.caption("Log at least two entries on different dates to begin exploring changes over time.")
    else:
        m3.metric("Average pain", "—")
        m4.metric("Average fatigue", "—")
        st.info("Your session statistics will appear here after you add symptom entries. These figures are calculated only from entries in this active session.")
    st.caption("Session statistics are descriptive only. They do not diagnose a condition, estimate disease risk, or replace clinical advice.")


elif page == "Symptom Diary":
    st.subheader("📝 The Daily Debrief")
    st.caption("How are we feeling, really? Log what you notice, one entry at a time.")
    st.write("Record what you noticed. You can leave cycle day and notes blank.")
    st.caption("Use your own descriptions. A diary can support a medical conversation, but it cannot establish the cause of symptoms.")

    with st.form("symptom_form", clear_on_submit=True):
        entry_date = st.date_input("Date", value=date.today())
        cycle_day_raw = st.text_input("Cycle day (optional; day 1 is the first day of menstrual bleeding)")
        pain = st.slider("Pain severity", min_value=0, max_value=10, value=0, help="Use your personal scale: 0 = no pain, 10 = worst pain you can imagine.")
        fatigue = st.slider("Fatigue / low energy", min_value=0, max_value=10, value=0)
        mood = st.selectbox("Mood", ["Choose not to say", "Okay", "Low", "Anxious", "Irritable", "Upset", "Mixed", "Other"])
        symptoms = st.multiselect(
            "Other symptoms you noticed",
            ["Cramps / pelvic pain", "Headache", "Bloating", "Nausea", "Bowel changes", "Urinary symptoms", "Sleep difficulty", "Skin changes", "Other"],
        )
        impact = st.selectbox(
            "Effect on daily activities",
            ["No noticeable effect", "A little", "Moderate", "A lot", "Unable to do usual activities"],
        )
        notes = st.text_area("Notes (optional; avoid names or identifying details)", max_chars=800)
        submitted = st.form_submit_button("Save my check-in 💗", type="primary")

    if submitted:
        cycle_day = None
        if cycle_day_raw.strip():
            try:
                cycle_day = int(cycle_day_raw.strip())
                if cycle_day < 1 or cycle_day > 60:
                    raise ValueError
            except ValueError:
                st.error("Cycle day must be a whole number from 1 to 60, or left blank.")
                cycle_day = "INVALID"
        if cycle_day != "INVALID":
            try:
                result = supabase.table("symptom_entries").insert({
                    "user_id": st.session_state.user_id,
                    "entry_date": entry_date.isoformat(),
                    "cycle_day": cycle_day,
                    "pain": int(pain),
                    "fatigue": int(fatigue),
                    "mood": mood,
                    "symptoms": symptoms,
                    "impact": impact,
                    "notes": notes.strip(),
                }).execute()
                st.session_state.symptom_entries.append({
                    "_db_id": result.data[0]["id"],
                    "date": entry_date.isoformat(),
                    "cycle_day": cycle_day,
                    "pain": int(pain),
                    "fatigue": int(fatigue),
                    "mood": mood,
                    "symptoms": symptoms,
                    "impact": impact,
                    "notes": notes.strip(),
                })
                st.success("Check-in saved to your account. You showed up for yourself today. 💗")
            except Exception:
                st.error("Your check-in couldn't be saved. Please try again.")

    if st.session_state.symptom_entries:
        st.markdown("---")
        st.markdown("### Your recent check-ins 🌷")
        for idx, entry in reversed(list(enumerate(st.session_state.symptom_entries))):
            with st.expander(f"{entry['date']} · Pain {entry['pain']}/10 · Fatigue {entry['fatigue']}/10"):
                st.write("**Cycle day:**", entry["cycle_day"] if entry["cycle_day"] else "Not recorded")
                st.write("**Mood:**", entry["mood"])
                st.write("**Symptoms:**", ", ".join(entry["symptoms"]) if entry["symptoms"] else "None selected")
                st.write("**Daily impact:**", entry["impact"])
                if entry["notes"]:
                    st.write("**Notes:**", entry["notes"])
                if st.button("Delete this entry", key=f"delete_symptom_{idx}"):
                    try:
                        supabase.table("symptom_entries").delete().eq("id", entry["_db_id"]).eq("user_id", st.session_state.user_id).execute()
                        st.session_state.symptom_entries.pop(idx)
                        st.rerun()
                    except Exception:
                        st.error("This entry couldn't be deleted. Please try again.")


elif page == "Pattern Insights & Report":
    st.subheader("🔮 Connect the Dots")
    st.caption("Your symptoms deserve more than a shrug. Here’s what your recorded entries show — not a diagnosis.")
    entries = st.session_state.symptom_entries
    if not entries:
        st.info("There are no diary entries yet. Add a few entries in Symptom Diary to see your personal summaries.")
    else:
        df = pd.DataFrame(entries).copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        avg_pain = df["pain"].mean()
        avg_fatigue = df["fatigue"].mean()
        high_pain_count = int((df["pain"] >= 7).sum())
        a, b, c = st.columns(3)
        a.metric("Entries logged", len(df))
        b.metric("Average pain rating", f"{avg_pain:.1f}/10")
        c.metric("Average fatigue rating", f"{avg_fatigue:.1f}/10")

        st.markdown("### Your timeline, at a glance ✨")
        chart_df = df.set_index("date")[["pain", "fatigue"]].rename(columns={"pain": "Pain (0–10)", "fatigue": "Fatigue (0–10)"})
        st.line_chart(chart_df)
        st.caption("These charts describe only the entries you recorded. They do not identify a cause or indicate a diagnosis.")

        st.markdown("### The short version 💌")
        st.write(f"You recorded **{len(df)} entries** from **{df['date'].min().date()}** to **{df['date'].max().date()}**.")
        st.write(f"Your average pain rating was **{avg_pain:.1f}/10**, and your average fatigue rating was **{avg_fatigue:.1f}/10** across the entries shown.")
        st.write(f"You rated pain at **7/10 or higher in {high_pain_count} of {len(df)} entries**. This is a summary of your own ratings, not a medical threshold.")
        counts = Counter(symptom for row in entries for symptom in row["symptoms"])
        if counts:
            common = counts.most_common(5)
            st.write("**Most frequently logged additional symptoms:** " + ", ".join(f"{name} ({count})" for name, count in common) + ".")
        else:
            st.write("No additional symptoms were selected in the entries yet.")
        st.info("Consider discussing symptoms that persist, recur, worsen, or interfere with everyday activities with a healthcare professional. The pattern alone cannot tell you why they occur.")

        st.markdown("### The Doctor’s Cheat Sheet 🩺")
        report = make_printable_report(entries, st.session_state.lab_entries)
        st.download_button(
            "Download my health summary 💌",
            data=report,
            file_name="aarogyasakhi_health_summary.html",
            mime="text/html",
            type="primary",
        )
        st.caption("Open the downloaded HTML file in a browser and press Ctrl+P to print or save it as a PDF.")
        flat_entries = []
        for entry in entries:
            flat_entries.append({
                "date": entry["date"],
                "cycle_day": entry["cycle_day"] or "",
                "pain_0_to_10": entry["pain"],
                "fatigue_0_to_10": entry["fatigue"],
                "mood": entry["mood"],
                "symptoms": ", ".join(entry["symptoms"]),
                "daily_impact": entry["impact"],
                "notes": entry["notes"],
            })
        csv_data = pd.DataFrame(flat_entries).to_csv(index=False).encode("utf-8")
        st.download_button("Download symptom entries (CSV) 📥", data=csv_data, file_name="aarogyasakhi_symptom_entries.csv", mime="text/csv")


elif page == "Health Check-in Guide":
    st.subheader("💬 Let’s Talk Symptoms")
    st.caption("A checklist for a more informed conversation — not a diagnosis.")
    st.write("Use this checklist to organise what you may want to discuss with a clinician. It does not calculate risk or diagnose PCOS, endometriosis, or thyroid disorders.")
    st.warning("Symptoms can have many causes. A checked box does not mean you have a condition, and an unchecked box does not rule one out.")

    with st.form("health_checkin_form"):
        st.markdown("#### Cycle and skin/hair changes (questions sometimes discussed during a PCOS evaluation)")
        pcos_cycle = st.checkbox("My periods are repeatedly very far apart or often missed.")
        pcos_skin = st.checkbox("Persistent acne or skin changes concern me.")
        pcos_hair = st.checkbox("I have noticed new unwanted coarse facial/body hair or scalp-hair thinning.")
        st.caption("For teenagers, menstrual patterns need to be interpreted in the context of time since the first period; a checklist alone cannot assess PCOS.")

        st.markdown("#### Pain and cycle-related symptoms (questions sometimes discussed during an endometriosis evaluation)")
        endo_pain = st.checkbox("Period-related pain affects school, work, sleep, or usual activities.")
        endo_other = st.checkbox("Pelvic pain also happens outside my period or keeps returning.")
        endo_cycle = st.checkbox("Bowel or urinary symptoms seem to recur around my period.")

        st.markdown("#### Symptoms sometimes discussed during a thyroid evaluation")
        thyroid_energy = st.checkbox("I have ongoing fatigue or an energy change that concerns me.")
        thyroid_temp = st.checkbox("I have noticed unusual sensitivity to cold or heat.")
        thyroid_body = st.checkbox("I have noticed persistent bowel changes, palpitations, or shakiness.")
        thyroid_neck = st.checkbox("I have noticed swelling or a lump at the front of my neck.")

        submitted_checkin = st.form_submit_button("Create my discussion prompts", type="primary")

    if submitted_checkin:
        selected = {
            "Cycle and skin/hair changes": [pcos_cycle, pcos_skin, pcos_hair],
            "Pain and cycle-related symptoms": [endo_pain, endo_other, endo_cycle],
            "Thyroid-related symptoms": [thyroid_energy, thyroid_temp, thyroid_body, thyroid_neck],
        }
        any_selected = any(any(values) for values in selected.values())
        if not any_selected:
            st.info("You did not select any items. You can still ask a clinician about any concern you have.")
        else:
            st.markdown("### Questions you could take to an appointment")
            if any(selected["Cycle and skin/hair changes"]):
                st.markdown("**Cycle and skin/hair changes**")
                st.write("- Could these changes have several possible causes, and what details from my history would help assess them?")
                st.write("- Would an evaluation for PCOS or another hormonal cause be appropriate for me?")
                st.write("- Depending on my history, are any tests—such as thyroid function or hormone tests—appropriate, or are they unnecessary?")
            if any(selected["Pain and cycle-related symptoms"]):
                st.markdown("**Pain and cycle-related symptoms**")
                st.write("- Could recurring pain that affects daily life need further evaluation or a referral?")
                st.write("- Would an ultrasound or another evaluation be appropriate for my symptoms? What would a normal result mean or not mean?")
                st.write("- What details should I track, and what support is available while we investigate the cause?")
            if any(selected["Thyroid-related symptoms"]):
                st.markdown("**Thyroid-related symptoms**")
                st.write("- Could my symptoms have a thyroid-related or another cause?")
                st.write("- Would TSH and, if appropriate, free T4 testing help answer this question?")
                st.write("- Is there anything in my history or medication list that affects interpretation?")
            st.info("These are conversation starters, not a list of tests you must request. A clinician can decide what evaluation is appropriate for your age, history, examination, and symptoms.")

    with st.expander("Why use a symptom diary?"):
        st.write("A dated diary can help you describe when symptoms happen, how they affect everyday life, and whether they recur. The NICE endometriosis guideline specifically notes that a pain and symptom diary can aid discussions with a clinician.")
        st.markdown("Source: [NICE — Endometriosis: diagnosis and management](https://www.nice.org.uk/guidance/ng73/chapter/Recommendations)")
    with st.expander("PCOS guidance and adolescent considerations"):
        st.write("PCOS assessment can be more nuanced during adolescence. A clinician should interpret menstrual patterns in context and consider other explanations; this checklist should not be used to diagnose PCOS.")
        st.markdown("Source: [ASRM — 2023 International evidence-based PCOS guideline recommendations](https://www.asrm.org/practice-guidance/practice-committee-documents/recommendations-from-the-2023-international-evidence-based-guideline-for-polycystic-ovary-syndrome-2023/)")


elif page == "Understand Lab Results":
    st.subheader("🧪 Lab Report, Translated")
    st.caption("Medical jargon? Not on our watch. Use these explanations as a starting point for questions, not as a diagnosis.")
    st.write("Enter the details exactly as printed on your report. AarogyaSakhi explains what a test generally measures and suggests questions to ask; it does not independently classify or diagnose your result.")
    st.caption("Reference intervals vary by laboratory, units, age, sex, pregnancy status, and clinical context. Keep the original report for your clinician.")

    with st.form("lab_form", clear_on_submit=True):
        lab_date = st.date_input("Test date", value=date.today(), key="lab_date")
        test_type = st.selectbox("Test category", list(TEST_INFO.keys()))
        test_label = st.text_input("Test name as printed (optional for common tests)")
        result_value = st.text_input("Result value (include decimals if needed)", placeholder="e.g. 12.4")
        units = st.text_input("Units exactly as printed", placeholder="e.g. g/dL, mIU/L, ng/mL")
        reference = st.text_input("Reference interval shown on the report (optional)", placeholder="Copy the lab's printed interval")
        lab_flag = st.selectbox("Does the lab mark it low/high?", ["Not sure / not shown", "Low on lab report", "Within range on lab report", "High on lab report"])
        lab_notes = st.text_area("Questions or notes for the clinician (optional)", max_chars=500)
        save_lab = st.form_submit_button("Add result to my visit summary", type="primary")

    if save_lab:
        if not result_value.strip():
            st.error("Please enter the result as shown on your report, or leave this form and return when you have it.")
        else:
            final_test_name = test_label.strip() if test_label.strip() else test_type
            lab_entry = {
                "date": lab_date.isoformat(),
                "test": final_test_name,
                "category": test_type,
                "result": result_value.strip(),
                "unit": units.strip(),
                "reference": reference.strip(),
                "lab_flag": lab_flag,
                "notes": lab_notes.strip(),
            }
            try:
                result = supabase.table("lab_entries").insert({
                    "user_id": st.session_state.user_id,
                    "entry_data": lab_entry,
                }).execute()
                saved_lab = {**lab_entry, "_db_id": result.data[0]["id"]}
                st.session_state.lab_entries.append(saved_lab)
                st.session_state.last_saved_lab = saved_lab
                st.success("Result saved to your account.")
            except Exception:
                st.error("This lab result couldn't be saved. Please try again.")

    if st.session_state.last_saved_lab:
        last_lab = st.session_state.last_saved_lab
        category = last_lab.get("category", "Other test")
        info = TEST_INFO.get(category, TEST_INFO["Other test"])
        st.markdown("---")
        st.markdown(f"### What {safe_text(last_lab['test'])} generally means")
        st.write(info["meaning"])
        st.write(f"**Your entered result:** {last_lab['result']} {last_lab['unit']}")
        if last_lab["reference"]:
            st.write(f"**Reference interval you entered:** {last_lab['reference']}")
        st.write(f"**Lab's own flag (as you entered it):** {last_lab['lab_flag']}")
        st.markdown("**Questions to ask your clinician**")
        for question in info["questions"]:
            st.write(f"- {question}")
        st.info("This app has not judged your result as normal or abnormal. A clinician should interpret it using the original report and your circumstances.")

    if st.session_state.lab_entries:
        st.markdown("### Results entered in this session")
        for i, lab in reversed(list(enumerate(st.session_state.lab_entries))):
            with st.expander(f"{lab['date']} · {lab['test']} · {lab['result']} {lab['unit']}"):
                st.write("**Lab reference interval:**", lab["reference"] or "Not entered")
                st.write("**Lab's own flag:**", lab["lab_flag"])
                if lab["notes"]:
                    st.write("**Notes:**", lab["notes"])
                if st.button("Delete this lab entry", key=f"delete_lab_{i}"):
                    try:
                        supabase.table("lab_entries").delete().eq("id", lab["_db_id"]).eq("user_id", st.session_state.user_id).execute()
                        removed = st.session_state.lab_entries.pop(i)
                        if st.session_state.last_saved_lab == removed:
                            st.session_state.last_saved_lab = st.session_state.lab_entries[0] if st.session_state.lab_entries else None
                        st.rerun()
                    except Exception:
                        st.error("This lab entry couldn't be deleted. Please try again.")
        report = make_printable_report(st.session_state.symptom_entries, st.session_state.lab_entries)
        st.download_button("Download updated printable report (HTML)", data=report, file_name="aarogyasakhi_health_summary.html", mime="text/html")


elif page == "Help & Resources":
    st.subheader("💌 Your Little Health Library")
    st.caption("Good information. Zero fear-mongering.")
    st.write("These India-focused contacts and links are included as a starting point. Confirm local availability and service details before relying on any directory.")

    st.markdown("""
    <div class="resource-card">
      <h3>Emergency support — 112</h3>
      <p>India's pan-India emergency response number for police, fire, health, and other emergency support.</p>
      <p><a href="tel:112">Call 112 from a phone</a> · <a href="https://112.gov.in/" target="_blank">Official 112 website</a></p>
    </div>
    <div class="resource-card">
      <h3>Women Helpline — 181</h3>
      <p>Support and information for women in distress, including connection to services. The Ministry's website notes that operational availability may vary; check current state/UT coverage.</p>
      <p><a href="tel:181">Call 181 from a phone</a> · <a href="https://www.wcd.gov.in/women/help" target="_blank">Ministry of Women and Child Development</a></p>
    </div>
    <div class="resource-card">
      <h3>Child Helpline — 1098</h3>
      <p>Support for children in crisis, integrated with the national emergency response system.</p>
      <p><a href="tel:1098">Call 1098 from a phone</a> · <a href="https://spniwcd.wcd.gov.in/child-helpline" target="_blank">Official Child Helpline information</a></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Reliable health information")
    st.markdown("- [NICE: Endometriosis diagnosis and management](https://www.nice.org.uk/guidance/ng73/chapter/Recommendations)")
    st.markdown("- [ASRM: International evidence-based PCOS guideline recommendations](https://www.asrm.org/practice-guidance/practice-committee-documents/recommendations-from-the-2023-international-evidence-based-guideline-for-polycystic-ovary-syndrome-2023/)")
    st.markdown("- [MedlinePlus: Health information from the US National Library of Medicine](https://medlineplus.gov/)")
    st.warning("If you are in immediate danger or have a severe or rapidly worsening health problem, use emergency services or seek urgent medical care rather than waiting for a website response.")


st.markdown("---")
st.caption("🌷 AarogyaSakhi · Your body talks. We listen. · Educational support, not a diagnostic tool.")

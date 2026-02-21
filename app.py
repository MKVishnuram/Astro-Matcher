"""
🌟 Tamil Astro Horoscope Matching Calculator
Built by Vishnuram — Software Engineer | TCE Alumni
v3.0 — Full Login · Supabase DB · History Drawer · PDF Export
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import sys, os, json, re
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

from master_data import NAKSHATRAS, RASIS, get_padham_navamsa
from matching_engine import AstroMatchingEngine
from database import (
    init_db, register_user, login_user, update_user_profile,
    save_horoscope, get_user_horoscopes,
    save_match_result, get_user_match_history,
    get_match_by_id, delete_match, get_user_stats
)
from pdf_report import generate_pdf

# ── Bootstrap DB ─────────────────────────────────────────────
init_db()

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jyotish Match · Vishnuram",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS  — Light warm background, dark content cards
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap');

/* ══════════════════════════════════════════════
   DESIGN TOKENS
══════════════════════════════════════════════ */
:root {
  --bg:        #F7F8FA;
  --surface:   #FFFFFF;
  --border:    #E5E7EB;
  --border2:   #D1D5DB;
  --text-1:    #111827;
  --text-2:    #374151;
  --text-3:    #6B7280;
  --text-4:    #9CA3AF;
  --accent:    #6366F1;
  --accent-lt: #EEF2FF;
  --amber:     #F59E0B;
  --amber-lt:  #FFFBEB;
  --green:     #10B981;
  --red:       #EF4444;
  --orange:    #F97316;
  --radius:    12px;
  --radius-lg: 18px;
  --shadow:    0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.05);
  --shadow-md: 0 4px 16px rgba(0,0,0,.08), 0 2px 6px rgba(0,0,0,.05);
  --shadow-lg: 0 10px 40px rgba(0,0,0,.10), 0 4px 12px rgba(0,0,0,.06);
}

/* ══════════════════════════════════════════════
   BASE
══════════════════════════════════════════════ */
html, body, [class*="css"] {
  font-family: 'Inter', 'DM Sans', sans-serif !important;
  background: var(--bg) !important;
  color: var(--text-1) !important;
  -webkit-font-smoothing: antialiased;
}

.main .block-container {
  background: var(--bg) !important;
  padding: 2rem 2.5rem 4rem !important;
  max-width: 1320px !important;
}

/* ══════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: #111827 !important;
  border-right: 1px solid #1F2937 !important;
  min-width: 268px !important;
  max-width: 268px !important;
}
section[data-testid="stSidebar"] * { color: #F9FAFB !important; }
section[data-testid="stSidebar"] label {
  color: #6B7280 !important;
  font-size: .7rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
}
section[data-testid="stSidebar"] input {
  background: #1F2937 !important;
  border: 1px solid #374151 !important;
  border-radius: 8px !important;
  color: white !important;
}
section[data-testid="stSidebar"] hr {
  border-color: #1F2937 !important;
  margin: 8px 0 !important;
}
/* Radio nav items */
section[data-testid="stSidebar"] [data-testid="stRadio"] label {
  background: transparent !important;
  border-radius: 8px !important;
  padding: 8px 12px !important;
  color: #9CA3AF !important;
  font-size: .88rem !important;
  font-weight: 500 !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  cursor: pointer;
  transition: all .15s;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: #1F2937 !important;
  color: white !important;
}

/* ══════════════════════════════════════════════
   TABS
══════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: var(--radius) !important;
  padding: 4px !important;
  gap: 2px !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow) !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 8px !important;
  color: var(--text-3) !important;
  font-weight: 500 !important;
  font-size: .85rem !important;
  padding: 8px 18px !important;
  transition: all .15s;
}
.stTabs [aria-selected="true"] {
  background: var(--accent) !important;
  color: white !important;
  font-weight: 600 !important;
  box-shadow: 0 2px 8px rgba(99,102,241,.3) !important;
}

/* ══════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════ */
div[data-testid="stButton"] > button {
  background: var(--accent) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-weight: 600 !important;
  font-size: .9rem !important;
  padding: .65rem 1.4rem !important;
  box-shadow: 0 2px 8px rgba(99,102,241,.25) !important;
  letter-spacing: .1px;
  transition: all .2s ease !important;
  font-family: 'Inter', sans-serif !important;
}
div[data-testid="stButton"] > button:hover {
  background: #4F46E5 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 16px rgba(99,102,241,.35) !important;
}
div[data-testid="stButton"] > button:active {
  transform: translateY(0) !important;
}

/* Secondary style buttons in sidebar (logout) */
section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
  background: #1F2937 !important;
  color: #9CA3AF !important;
  border: 1px solid #374151 !important;
  box-shadow: none !important;
  font-size: .85rem !important;
}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
  background: #374151 !important;
  color: white !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
  background: var(--surface) !important;
  color: var(--accent) !important;
  border: 1.5px solid var(--accent) !important;
  box-shadow: none !important;
}
[data-testid="stDownloadButton"] > button:hover {
  background: var(--accent-lt) !important;
}

/* ══════════════════════════════════════════════
   FORM INPUTS
══════════════════════════════════════════════ */
.main input, .main textarea {
  background: var(--surface) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-1) !important;
  font-size: .9rem !important;
  font-family: 'Inter', sans-serif !important;
  transition: border-color .15s, box-shadow .15s;
}
.main input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,.12) !important;
}
.main label {
  color: var(--text-2) !important;
  font-weight: 500 !important;
  font-size: .82rem !important;
}
.main [data-baseweb="select"] > div {
  background: var(--surface) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-1) !important;
  font-size: .9rem !important;
}
.main [data-baseweb="select"] > div:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,.12) !important;
}

/* ══════════════════════════════════════════════
   ALERTS
══════════════════════════════════════════════ */
.stAlert { border-radius: var(--radius) !important; }
[data-testid="stInfoBox"] {
  background: #EFF6FF !important;
  border: 1px solid #BFDBFE !important;
  border-radius: var(--radius) !important;
  color: #1E40AF !important;
}
[data-testid="stWarningBox"] {
  background: #FFFBEB !important;
  border: 1px solid #FDE68A !important;
  border-radius: var(--radius) !important;
  color: #92400E !important;
}
[data-testid="stErrorBox"] {
  background: #FEF2F2 !important;
  border: 1px solid #FECACA !important;
  border-radius: var(--radius) !important;
  color: #991B1B !important;
}
[data-testid="stSuccessBox"] {
  background: #ECFDF5 !important;
  border: 1px solid #A7F3D0 !important;
  border-radius: var(--radius) !important;
  color: #065F46 !important;
}

/* ══════════════════════════════════════════════
   DATAFRAME
══════════════════════════════════════════════ */
.stDataFrame {
  border-radius: var(--radius-lg) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow) !important;
  border: 1px solid var(--border) !important;
}

/* ══════════════════════════════════════════════
   MISC
══════════════════════════════════════════════ */

/* ══════════════════════════════════════════════
   MISC & DRAWER NAVIGATION (ENGINEERED FIX)
══════════════════════════════════════════════ */

/* 1. Hide default menu, footer, and those tiny default arrows */
#MainMenu, footer { visibility: hidden !important; }

/* Hide the native "close" arrow inside the sidebar */
button[data-testid="stSidebarCollapseButton"] div {
    display: none !important;
}

/* 2. Create the 'User-Aware' Floating Action Button (FAB) */
button[data-testid="stSidebarCollapseButton"] {
    background-color: #6366F1 !important; /* Your Accent Color */
    color: white !important;
    border-radius: 50% !important;
    width: 54px !important;
    height: 54px !important;
    position: fixed !important;
    top: 20px !important;
    left: 20px !important;
    z-index: 1000001 !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.5) !important;
    border: 3px solid #ffffff !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}

/* 3. Add a custom icon inside the FAB since we hid the default one */
button[data-testid="stSidebarCollapseButton"]::after {
    content: "☰"; /* A standard menu 'hamburger' icon */
    font-size: 24px;
    font-weight: bold;
    font-family: Arial, sans-serif;
}

/* Hover and Active states for better awareness */
button[data-testid="stSidebarCollapseButton"]:hover {
    transform: scale(1.15) rotate(90deg) !important;
    background-color: #4F46E5 !important;
}

/* 4. Ensure the Header is truly transparent so it doesn't block clicks */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
}

/* 5. Smooth Sidebar Drawer Transitions */
[data-testid="stSidebar"] {
    transition: all 0.3s ease !important;
    box-shadow: 5px 0 15px rgba(0,0,0,0.1) !important;
}

/* Fix for main content area layout */
[data-testid="stSidebar"][aria-expanded="false"] {
    margin-left: -268px !important; /* Forces it fully out of sight when closed */
}

iframe { border: none !important; display: block; }
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HTML IFRAME HELPER — bypasses Streamlit sanitizer
# ─────────────────────────────────────────────────────────────
def H(body: str, height: int = 100, scrolling: bool = False):
    doc = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>*{{margin:0;padding:0;box-sizing:border-box;}}
    body{{font-family:'Inter',sans-serif;background:transparent;overflow:hidden;
          -webkit-font-smoothing:antialiased;color:#111827;}}
    </style></head><body>{body}</body></html>"""
    components.html(doc, height=height, scrolling=scrolling)


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
@st.cache_data
def star_opts():
    return [f"{n['name']} ({n['tamil']})" for n in NAKSHATRAS]

@st.cache_data
def rasi_opts():
    return [f"{r['name']} ({r['tamil']}) — {r['english']}" for r in RASIS]

def sname(o): return o.split(" (")[0]
def rname(o): return o.split(" (")[0]
def gstar(n): return next((x for x in NAKSHATRAS if x["name"] == n), {})
def grasi(n): return next((x for x in RASIS    if x["name"] == n), {})

def score_color(p):
    if p >= 75: return "#00C851"
    if p >= 50: return "#FF8800"
    return "#ff4444"

def validate_email(email: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email.strip()))

def fmt_ts(ts) -> str:
    """Format UTC timestamp for display — returns ISO string for JS conversion."""
    if ts is None: return "—"
    if hasattr(ts, 'isoformat'):
        return ts.isoformat()
    return str(ts)

STAR_OPTS = star_opts()
RASI_OPTS = rasi_opts()


# ─────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────
for k, v in {
    "user":          None,
    "page":          "login",   # login | register | app | forgot
    "view_match_id": None,
    "calc_result":   None,
    "auth_tab":      "signin",  # signin | register | forgot
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# GREETING BANNER
# ─────────────────────────────────────────────────────────────
def greeting_banner(user, subtitle: str = ""):
    from datetime import datetime as _dt
    hr    = _dt.now().hour
    tod   = ("Good morning" if hr < 12 else "Good afternoon" if hr < 17
             else "Good evening" if hr < 21 else "Good night")
    dname = user.get("display_name", user.get("username", "Friend")).title()
    sub   = subtitle or "Welcome to Jyotish Match"
    H(f"""
<div style="background:#ffffff;border:1px solid #E5E7EB;border-radius:16px;
            padding:20px 24px;margin-bottom:20px;
            box-shadow:0 1px 3px rgba(0,0,0,.06);">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
    <div>
      <div style="font-size:.72rem;color:#9CA3AF;font-weight:500;margin-bottom:4px;letter-spacing:.3px;">
        {tod} ·&nbsp; Jyotish Match
      </div>
      <div style="font-size:1.5rem;font-weight:700;color:#111827;line-height:1.2;">
        Hello, <span style="color:#6366F1;">{dname}</span> 🙏
      </div>
      <div style="color:#6B7280;font-size:.84rem;margin-top:4px;">{sub}</div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;background:#F9FAFB;
                border:1px solid #E5E7EB;border-radius:12px;padding:10px 14px;">
      <div style="width:36px;height:36px;border-radius:50%;background:#6366F1;
                  display:flex;align-items:center;justify-content:center;
                  font-weight:700;font-size:.95rem;color:white;flex-shrink:0;">V</div>
      <div>
        <div style="font-weight:700;font-size:.88rem;color:#111827;">Vishnuram</div>
        <div style="font-size:.7rem;color:#9CA3AF;margin-top:1px;">Software Engineer · TCE Alumni</div>
      </div>
    </div>
  </div>
</div>""", 100)


# ─────────────────────────────────────────────────────────────
# BRAND FOOTER
# ─────────────────────────────────────────────────────────────
FOOTER_HTML = """
<div style="text-align:center;padding:16px 0 4px;border-top:1px solid #E5E7EB;margin-top:12px;">
  <span style="font-size:.72rem;color:#9CA3AF;font-weight:500;">
    Built by <strong style="color:#6366F1;">Vishnuram</strong>
    &nbsp;·&nbsp; Software Engineer &nbsp;·&nbsp; TCE Alumni
  </span>
</div>
"""



# ─────────────────────────────────────────────────────────────
# CARD BUILDERS + CHARTS + RENDER RESULTS
# ─────────────────────────────────────────────────────────────

DISCLAIMER_HTML = """
<div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:14px;
            padding:14px 18px;margin:8px 0;">
  <div style="display:flex;gap:10px;">
    <span style="font-size:1.3rem;">⚠️</span>
    <div style="color:#78350F;font-size:.85rem;line-height:1.6;">
      <strong style="color:#92400E;">Important:</strong>
        This result is based solely on algorithmic calculations developed by Vishnuram and <strong>must NOT be used to make life or marriage decisions</strong>.
        Always consult a <strong>qualified Vedic astrologer</strong> for proper guidance.
    </div>
  </div>
</div>
"""


def star_info_card(title, icon, si, name, padham, ri):
    el_c = {"Fire": "#F97316", "Earth": "#22c55e",
            "Water": "#38bdf8", "Air": "#a78bfa"}.get(ri.get("element", ""), "#6366F1")
    rows = "".join(
        f'<tr><td style="color:#9CA3AF;padding:5px 0;width:42%;font-size:.78rem;">{k}</td>'
        f'<td style="color:{vc};font-weight:600;padding:5px 0;font-size:.82rem;">{v}</td></tr>'
        for k, v, vc in [
            ("⭐ Star",   f"{si.get('name','')} ({si.get('tamil','')})", "#6366F1"),
            ("🔢 Padham", f"{padham}  · Quarter",                        "#111827"),
            ("♈ Rasi",   f"{ri.get('name','')} ({ri.get('english','')})", "#111827"),
            ("🔮 Lord",   si.get('lord', ''),                             "#8B5CF6"),
            ("🌀 Gana",   si.get('gana', ''),                             "#3B82F6"),
            ("💧 Nadi",   si.get('nadi', ''),                             "#F97316"),
            ("🐾 Yoni",   si.get('yoni', ''),                             "#10B981"),
            (f"🔥 {ri.get('element','')}", ri.get('quality', ''),         el_c),
        ]
    )
    return f"""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:14px;padding:20px;
            box-shadow:0 1px 4px rgba(0,0,0,.05);">
  <div style="display:flex;align-items:center;gap:10px;
              margin-bottom:14px;border-bottom:1px solid #F3F4F6;padding-bottom:12px;">
    <div style="width:40px;height:40px;border-radius:50%;background:#EEF2FF;
                display:flex;align-items:center;justify-content:center;
                font-size:1.3rem;flex-shrink:0;">{icon}</div>
    <div>
      <div style="font-weight:700;color:#111827;font-size:.95rem;">{title}</div>
      <div style="color:#9CA3AF;font-size:.76rem;margin-top:1px;">{name}</div>
    </div>
  </div>
  <table style="width:100%;border-collapse:collapse;">{rows}</table>
</div>"""


def score_summary_card(pct, raw_score, raw_max, verdict, vc, n_doshas, n_crit):
    vm   = {"green": "#10B981", "blue": "#6366F1", "orange": "#F59E0B", "red": "#EF4444"}
    vcol = vm.get(vc, "#EF4444")
    circ   = 3.14159 * 75
    filled = circ * (pct / 100)
    vi     = "✨" if "Excellent" in verdict else "👍" if "Good" in verdict else "🔍" if "Average" in verdict else "⚠️"
    vtext  = verdict.replace("✨","").replace("👍","").replace("🔍","").replace("⚠️","").strip()
    return f"""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:14px;padding:24px 20px;
            text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.05);">
  <div style="color:#9CA3AF;font-size:.65rem;letter-spacing:2px;
              text-transform:uppercase;margin-bottom:14px;">OVERALL MATCH SCORE</div>
  <svg width="190" height="108" viewBox="0 0 190 108" style="overflow:visible;display:block;margin:0 auto;">
    <defs>
      <linearGradient id="ag2" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#6366F1"/>
        <stop offset="100%" style="stop-color:#8B5CF6"/>
      </linearGradient>
    </defs>
    <path d="M 20 92 A 75 75 0 0 1 170 92" fill="none"
          stroke="#F3F4F6" stroke-width="14" stroke-linecap="round"/>
    <path d="M 20 92 A 75 75 0 0 1 170 92" fill="none"
          stroke="url(#ag2)" stroke-width="14" stroke-linecap="round"
          stroke-dasharray="{filled:.1f} {circ:.1f}"
          style="filter:drop-shadow(0 0 8px rgba(99,102,241,.4));"/>
    <text x="95" y="84" text-anchor="middle"
          style="fill:#111827;font-family:Inter,sans-serif;font-size:30px;font-weight:800;">{pct:.0f}%</text>
  </svg>
  <div style="color:{vcol};font-weight:700;font-size:1.1rem;margin:10px 0 8px;">{vi} {vtext}</div>
  <div style="display:flex;justify-content:center;gap:20px;
              margin-top:14px;padding-top:12px;border-top:1px solid #F3F4F6;">
    <div style="text-align:center;">
      <div style="color:#6366F1;font-weight:700;font-size:1rem;">{raw_score}/{raw_max}</div>
      <div style="color:#9CA3AF;font-size:.64rem;margin-top:2px;">Raw Score</div>
    </div>
    <div style="text-align:center;">
      <div style="color:{'#EF4444' if n_crit > 0 else '#10B981'};font-weight:700;font-size:1rem;">{n_crit}</div>
      <div style="color:#9CA3AF;font-size:.64rem;margin-top:2px;">Critical</div>
    </div>
    <div style="text-align:center;">
      <div style="color:{'#F59E0B' if n_doshas > 0 else '#10B981'};font-weight:700;font-size:1rem;">{n_doshas}</div>
      <div style="color:#9CA3AF;font-size:.64rem;margin-top:2px;">Doshas</div>
    </div>
  </div>
</div>"""


def porutham_cards_html(results):
    out = ""
    for r in results:
        bc  = score_color(r["percentage"])
        pct = r["percentage"]
        bbg = "#EF4444" if r["dosha"] else "#10B981"
        btx = "⚠️ DOSHA" if r["dosha"] else "✅ PASS"
        crit = (f'<span style="background:#EF4444;color:white;padding:2px 8px;'
                f'border-radius:20px;font-size:.64rem;font-weight:700;margin-left:6px;">🔴 CRITICAL</span>'
                if (r["is_critical"] and r["dosha"]) else "")
        out += f"""
<div style="margin-bottom:12px;background:#fff;border:1px solid #E5E7EB;
            border-left:4px solid {bc};border-radius:12px;padding:16px 18px;
            box-shadow:0 1px 3px rgba(0,0,0,.04);">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:6px;">
    <div style="flex:1;min-width:180px;">
      <span style="font-weight:700;font-size:.93rem;color:#111827;">{r['name']}</span>
      <span style="color:#9CA3AF;font-size:.78rem;margin-left:6px;">({r['tamil']})</span>{crit}
      <div style="color:#9CA3AF;font-size:.7rem;margin-top:2px;">📂 {r['category']}</div>
    </div>
    <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;">
      <span style="color:{bc};font-weight:800;font-size:1.1rem;">{r['score']}/{r['max_score']}</span>
      <span style="background:{bbg};color:white;padding:3px 11px;
                   border-radius:20px;font-size:.68rem;font-weight:600;">{btx}</span>
    </div>
  </div>
  <div style="margin-top:10px;background:#F9FAFB;border-radius:6px;height:8px;overflow:hidden;">
    <div style="width:{pct}%;background:{bc};height:8px;border-radius:6px;"></div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-top:6px;">
    <div style="color:#6B7280;font-size:.77rem;line-height:1.6;flex:1;">
      <strong style="color:#374151;">{r['compatibility']}</strong>
      <span style="color:#D1D5DB;"> — </span>
      <span>{r['details']}</span>
    </div>
    <span style="color:{bc};font-size:.74rem;font-weight:700;margin-left:10px;flex-shrink:0;">{pct:.0f}%</span>
  </div>
</div>"""
    return out


def radar_chart(results):
    cats = [r["name"].replace(" Porutham", "") for r in results]
    vals = [r["percentage"] for r in results]
    cats.append(cats[0]); vals.append(vals[0])
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals, theta=cats, fill="toself",
        fillcolor="rgba(99,102,241,.15)", line=dict(color="#6366F1", width=2.5),
        hovertemplate="%{theta}: %{r:.1f}%<extra></extra>"))
    fig.add_trace(go.Scatterpolar(r=[100]*len(cats), theta=cats, fill="toself",
        fillcolor="rgba(99,102,241,.03)", line=dict(color="rgba(99,102,241,.2)", width=1, dash="dot"),
        hoverinfo="skip"))
    fig.update_layout(
        polar=dict(bgcolor="#F9FAFB",
            radialaxis=dict(visible=True, range=[0,100],
                tickfont=dict(color="#9CA3AF", size=8),
                gridcolor="#E5E7EB"),
            angularaxis=dict(tickfont=dict(color="#374151", size=10),
                gridcolor="#E5E7EB")),
        paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
        height=380, margin=dict(t=24, b=24, l=70, r=70))
    return fig


def gauge_chart(value, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        title={"text": title, "font": {"size": 13, "color": "#6B7280"}},
        number={"suffix": "%", "font": {"size": 32, "color": "#111827"}},
        gauge={
            "axis": {"range": [0,100], "tickcolor":"#9CA3AF", "tickfont":{"color":"#9CA3AF","size":9}},
            "bar": {"color": color, "thickness": .65},
            "bgcolor": "#F9FAFB", "borderwidth": 0,
            "steps": [
                {"range":[0,40],  "color":"rgba(239,68,68,.08)"},
                {"range":[40,65], "color":"rgba(245,158,11,.08)"},
                {"range":[65,80], "color":"rgba(99,102,241,.08)"},
                {"range":[80,100],"color":"rgba(16,185,129,.08)"},
            ],
            "threshold": {"line":{"color":"#6366F1","width":2}, "value":value}
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      height=240, margin=dict(t=40,b=10,l=20,r=20), font_color="#111827")
    return fig


def bar_chart(results):
    names  = [r["name"].replace(" Porutham", "") for r in results]
    scores = [r["score"] for r in results]
    maxes  = [r["max_score"] for r in results]
    pcts   = [r["percentage"] for r in results]
    cols   = [score_color(p) for p in pcts]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Score", x=names, y=scores, marker_color=cols,
        text=[f"{s}/{m}" for s,m in zip(scores,maxes)], textposition="outside",
        textfont=dict(color="#374151", size=9),
        hovertemplate="<b>%{x}</b><br>%{customdata:.1f}%<extra></extra>", customdata=pcts))
    fig.add_trace(go.Bar(name="Max", x=names, y=[m-s for s,m in zip(scores,maxes)],
        marker_color="rgba(0,0,0,.04)", hoverinfo="skip"))
    fig.update_layout(barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=300, margin=dict(t=10,b=75,l=20,r=20), showlegend=False,
        xaxis=dict(tickfont=dict(color="#6B7280", size=9), gridcolor="#F3F4F6", tickangle=-35),
        yaxis=dict(tickfont=dict(color="#9CA3AF"), gridcolor="#F3F4F6"),
        font_color="#374151")
    return fig

#
# ─────────────────────────────────────────────────────────────
# ██  MATCH RESULTS RENDERER
# ─────────────────────────────────────────────────────────────
def render_results(summary, user, g_padham, b_padham, g_star_n, b_star_n, g_rasi_n, b_rasi_n):
    results = summary["results"]
    pct     = summary["final_percentage"]
    raw_pct = summary["raw_percentage"]
    verdict = summary["verdict"]
    vc      = summary["verdict_color"]
    g_ri    = summary["groom_rasi_details"]
    b_ri    = summary["bride_rasi_details"]

    H(DISCLAIMER_HTML, 150)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── 3-col summary ──────────────────────────────────────
    cg, cs, cb = st.columns([2.3, 3, 2.3])
    with cg:
        H(star_info_card("Groom's Horoscope", "🤵",
                         summary["groom_star_details"],
                         summary["groom"]["name"], g_padham, g_ri), 280)
    with cs:
        H(score_summary_card(pct, summary["raw_score"], summary["raw_max"],
                             verdict, vc, summary["total_doshas"],
                             len(summary["critical_doshas"])), 280)
    with cb:
        H(star_info_card("Bride's Horoscope", "👰",
                         summary["bride_star_details"],
                         summary["bride"]["name"], b_padham, b_ri), 280)

    st.markdown("<br>", unsafe_allow_html=True)

    if summary["critical_doshas"]:
        st.error(f"🔴 **Critical Doshas:** {', '.join(summary['critical_doshas'])} — Consult an experienced astrologer immediately.")
    if summary["minor_doshas"]:
        st.warning(f"🟡 **Minor Doshas:** {', '.join(summary['minor_doshas'])} — Traditional remedies (Pariharams) may be considered.")

    # ── PDF ──────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    dc1, _ = st.columns([1.5, 5])
    with dc1:
        pdf_bytes = generate_pdf(summary, user)
        fname = (f"AstroMatch_{summary['groom']['name']}_{summary['bride']['name']}"
                 f"_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
        st.download_button("📄  Download PDF Report", pdf_bytes, fname,
                           "application/pdf", use_container_width=True)

    st.markdown("---")

    # ── Tabs ─────────────────────────────────────────────
    t1, t2, t3, t4 = st.tabs([
        "📊  10 Poruthams", "📈  Charts",
        "🌙  Padham & Navamsa", "📋  Full Report",
    ])

    with t1:
        st.markdown("<br>", unsafe_allow_html=True)
        H(f'<div style="padding:2px 0;">{porutham_cards_html(results)}</div>',
          height=1460, scrolling=True)

    with t2:
        st.markdown("<br>", unsafe_allow_html=True)
        ca, cb2 = st.columns(2)
        c1 = "#10B981" if pct >= 80 else "#F59E0B" if pct >= 50 else "#EF4444"
        c2 = "#10B981" if raw_pct >= 80 else "#F59E0B" if raw_pct >= 50 else "#EF4444"
        with ca:  st.plotly_chart(gauge_chart(pct, "Weighted Match Score", c1), use_container_width=True)
        with cb2: st.plotly_chart(gauge_chart(raw_pct, "Raw Score %", c2), use_container_width=True)
        st.plotly_chart(radar_chart(results), use_container_width=True)
        st.plotly_chart(bar_chart(results), use_container_width=True)
        cat_d = {}
        for r in results:
            c = r["category"]
            cat_d.setdefault(c, {"s":0,"m":0})
            cat_d[c]["s"] += r["score"]; cat_d[c]["m"] += r["max_score"]
        pl = list(cat_d.keys())
        pv = [cat_d[c]["s"]/cat_d[c]["m"]*100 for c in pl]
        fp = go.Figure(go.Pie(labels=pl, values=pv, hole=.45,
            marker=dict(colors=["#6366F1","#8B5CF6","#3B82F6","#10B981","#F59E0B","#EF4444","#F97316","#06B6D4"]),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>"))
        fp.update_layout(title="Match Score by Life Area",
            paper_bgcolor="rgba(0,0,0,0)", font_color="#374151",
            height=320, margin=dict(t=50, b=10))
        st.plotly_chart(fp, use_container_width=True)

    with t3:
        st.markdown("<br>", unsafe_allow_html=True)
        pa  = summary["padham_analysis"]
        cs  = pa["navamsa_lord_compatibility"]
        nc  = "#10B981" if "Friendly" in cs else "#EF4444" if "Enemy" in cs else "#F59E0B"
        PM  = {1:("🔥","Dharma Padha","Career, Purpose & Social Status"),
               2:("🌍","Artha Padha","Wealth, Family & Material Comforts"),
               3:("💨","Kama Padha","Desires, Courage & Communication"),
               4:("💧","Moksha Padha","Home, Mother, Emotions & Liberation")}
        gpm = PM[pa["groom_padham"]]; bpm = PM[pa["bride_padham"]]
        H(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:14px;">
  <div style="background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:18px;">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
      <span style="font-size:1.3rem;">{gpm[0]}</span>
      <div>
        <div style="color:#6366F1;font-weight:700;font-size:.88rem;">🤵 Groom · Padham {pa['groom_padham']}</div>
        <div style="color:#F59E0B;font-size:.75rem;">{gpm[1]}</div>
      </div>
    </div>
    <div style="color:#6B7280;font-size:.78rem;line-height:1.7;">{gpm[2]}</div>
    <div style="margin-top:12px;padding-top:10px;border-top:1px solid #F3F4F6;">
      <div style="color:#9CA3AF;font-size:.65rem;letter-spacing:1px;text-transform:uppercase;">Navamsa Rasi</div>
      <div style="color:#111827;font-weight:700;font-size:.95rem;margin-top:2px;">{pa['groom_navamsa']}</div>
    </div>
  </div>
  <div style="background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:18px;">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
      <span style="font-size:1.3rem;">{bpm[0]}</span>
      <div>
        <div style="color:#EC4899;font-weight:700;font-size:.88rem;">👰 Bride · Padham {pa['bride_padham']}</div>
        <div style="color:#F59E0B;font-size:.75rem;">{bpm[1]}</div>
      </div>
    </div>
    <div style="color:#6B7280;font-size:.78rem;line-height:1.7;">{bpm[2]}</div>
    <div style="margin-top:12px;padding-top:10px;border-top:1px solid #F3F4F6;">
      <div style="color:#9CA3AF;font-size:.65rem;letter-spacing:1px;text-transform:uppercase;">Navamsa Rasi</div>
      <div style="color:#111827;font-weight:700;font-size:.95rem;margin-top:2px;">{pa['bride_navamsa']}</div>
    </div>
  </div>
</div>
<div style="background:#F9FAFB;border:1px solid {nc}44;border-radius:12px;padding:16px;text-align:center;">
  <div style="color:#9CA3AF;font-size:.67rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">Navamsa Lord Compatibility</div>
  <div style="color:{nc};font-size:1.1rem;font-weight:700;">{cs}</div>
  <div style="color:#9CA3AF;font-size:.74rem;margin-top:4px;">{pa['groom_navamsa']} ✦ {pa['bride_navamsa']}</div>
</div>""", 360)

    with t4:
        st.markdown("<br>", unsafe_allow_html=True)
        vm    = {"green":"#10B981","blue":"#6366F1","orange":"#F59E0B","red":"#EF4444"}
        v_col = vm.get(vc, "#EF4444")
        H(f"""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:14px;
            padding:22px;margin-bottom:16px;">
  <div style="font-weight:700;color:#111827;font-size:.93rem;
              border-bottom:1px solid #F3F4F6;padding-bottom:10px;margin-bottom:14px;">
    📊 Match Summary Report
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;">
    <div style="background:#EEF2FF;border-radius:10px;padding:12px;">
      <div style="color:#9CA3AF;font-size:.65rem;text-transform:uppercase;letter-spacing:1px;">Groom</div>
      <div style="color:#111827;font-weight:600;font-size:.92rem;margin-top:2px;">{summary['groom']['name']}</div>
      <div style="color:#6B7280;font-size:.75rem;margin-top:2px;">{g_star_n} · Padham {g_padham} · {g_rasi_n}</div>
    </div>
    <div style="background:#FDF2F8;border-radius:10px;padding:12px;">
      <div style="color:#9CA3AF;font-size:.65rem;text-transform:uppercase;letter-spacing:1px;">Bride</div>
      <div style="color:#111827;font-weight:600;font-size:.92rem;margin-top:2px;">{summary['bride']['name']}</div>
      <div style="color:#6B7280;font-size:.75rem;margin-top:2px;">{b_star_n} · Padham {b_padham} · {b_rasi_n}</div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;
              padding-top:12px;border-top:1px solid #F3F4F6;">
    <div style="text-align:center;background:#EEF2FF;border-radius:10px;padding:10px 4px;">
      <div style="color:#6366F1;font-weight:800;font-size:1.25rem;">{pct:.1f}%</div>
      <div style="color:#9CA3AF;font-size:.63rem;margin-top:2px;">Weighted</div>
    </div>
    <div style="text-align:center;background:#F9FAFB;border-radius:10px;padding:10px 4px;">
      <div style="color:#111827;font-weight:800;font-size:1.25rem;">{summary['raw_score']}/{summary['raw_max']}</div>
      <div style="color:#9CA3AF;font-size:.63rem;margin-top:2px;">Raw Score</div>
    </div>
    <div style="text-align:center;background:#FEF2F2;border-radius:10px;padding:10px 4px;">
      <div style="color:{'#EF4444' if summary['total_doshas'] > 0 else '#10B981'};font-weight:800;font-size:1.25rem;">{summary['total_doshas']}</div>
      <div style="color:#9CA3AF;font-size:.63rem;margin-top:2px;">Doshas</div>
    </div>
    <div style="text-align:center;background:#F9FAFB;border-radius:10px;padding:10px 4px;">
      <div style="color:{v_col};font-weight:700;font-size:.82rem;line-height:1.3;">{verdict.replace('✨','').replace('👍','').replace('🔍','').replace('⚠️','').strip()}</div>
      <div style="color:#9CA3AF;font-size:.63rem;margin-top:2px;">Verdict</div>
    </div>
  </div>
</div>""", 248)

        df = pd.DataFrame([{
            "Porutham":      r["name"],
            "Tamil":         r["tamil"],
            "Category":      r["category"],
            "Score":         r["score"],
            "Max":           r["max_score"],
            "Match %":       r["percentage"],
            "Compatibility": r["compatibility"],
            "Dosha":         "⚠️ Yes" if r["dosha"] else "✅ No",
            "Critical":      "🔴" if r["is_critical"] else "—",
        } for r in results])
        st.dataframe(df, use_container_width=True, hide_index=True,
            column_config={"Match %": st.column_config.ProgressColumn(
                "Match %", min_value=0, max_value=100, format="%.1f%%")})

        all_d = summary["critical_doshas"] + summary["minor_doshas"]
        if all_d:
            REM = {
                "Nadi Porutham":  ("#EF4444","Nadi Dosha Nivarana Puja at a Shiva temple. Gifting gold to a priest on wedding day. 1,08,000 Maha Mrityunjaya Japa."),
                "Rajju Porutham": ("#EF4444","Rajju Dosha Parihara Puja. Sacred Raksha thread ceremony. Seek blessings of 7 Sumangalis (married women)."),
                "Gana Porutham":  ("#F59E0B","Shiva-Parvathi Puja for 21 consecutive Mondays. Offer bilva leaves and light camphor."),
                "Yoni Porutham":  ("#F59E0B","Ashta Mangala Puja. Kula Devata (family deity) worship. Offer coconuts and bananas."),
                "Vedha Porutham": ("#F59E0B","Navagraha Shanti Puja. Light sesame oil lamps for 45 consecutive days."),
                "Varna Porutham": ("#6366F1","Seek blessings of elders and saints. Saraswati Puja for spiritual harmony."),
                "Stree Deerga":   ("#F59E0B","Lakshmi Puja and Suhasini blessings ceremony on an auspicious day."),
            }
            rows_html = "".join(
                f'<div style="margin-bottom:10px;padding:12px 14px;background:#F9FAFB;'
                f'border-radius:10px;border-left:3px solid {dc};">'
                f'<div style="color:#111827;font-weight:600;font-size:.82rem;margin-bottom:3px;">🙏 {d}</div>'
                f'<div style="color:#6B7280;font-size:.76rem;line-height:1.6;">{dt}</div></div>'
                for d in all_d if d in REM
                for dc, dt in [REM[d]]
            )
            H(f'''<div style="background:#fff;border:1px solid #E5E7EB;border-radius:14px;
                             padding:18px;margin-top:10px;">
  <div style="font-weight:700;color:#111827;font-size:.9rem;margin-bottom:12px;">🙏 Traditional Remedies (Pariharams)</div>
  {rows_html}
  <div style="color:#9CA3AF;font-size:.67rem;text-align:center;margin-top:10px;padding-top:8px;border-top:1px solid #F3F4F6;">
    ⚠ Traditional suggestions only. Always consult a qualified Vedic astrologer.
  </div>
</div>''', max(200, len(all_d) * 110 + 80))

    H(f"""
<div style="text-align:center;padding:16px 0 4px;border-top:1px solid #E5E7EB;margin-top:16px;">
  <span style="font-size:.72rem;color:#9CA3AF;font-weight:500;">
    Built by <strong style="color:#6366F1;">Vishnuram</strong>
    &nbsp;·&nbsp; Software Engineer &nbsp;·&nbsp; TCE Alumni
  </span>
</div>""", 50)













# ─────────────────────────────────────────────────────────────
# ██  LOGIN PAGE
# ─────────────────────────────────────────────────────────────
def page_login():
    from database import get_conn

    def reset_password(email: str, new_pw: str):
        email = email.strip().lower()
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM jyotish.app_users WHERE email=%s", (email,))
                if not cur.fetchone():
                    raise ValueError("No account found with that email address.")
                cur.execute("UPDATE jyotish.app_users SET password_hash=%s WHERE email=%s", (new_pw, email))

    tab = st.session_state.get("auth_tab", "signin")

    # ── Full page — left brand + right form ──────────────────
    _, center, _ = st.columns([1, 2.2, 1])
    with center:

        # ── Brand header ────────────────────────────────────
        H("""
<div style="text-align:center;padding:40px 0 28px;">
  <div style="display:inline-flex;align-items:center;justify-content:center;
              width:52px;height:52px;background:#6366F1;border-radius:14px;
              margin-bottom:16px;box-shadow:0 4px 14px rgba(99,102,241,.35);">
    <span style="font-size:1.6rem;">🌟</span>
  </div>
  <div style="font-size:1.75rem;font-weight:800;color:#111827;letter-spacing:-.5px;">
    Jyotish Match
  </div>
  <div style="color:#6B7280;font-size:.88rem;margin-top:6px;">
    Tamil Horoscope Matching · 10 Poruthams
  </div>
</div>""", 240)

        # ── Tab switcher ─────────────────────────────────────
        if tab != "forgot":
            t1, t2 = st.columns(2)
            with t1:
                if st.button("Sign In", use_container_width=True,
                             type="primary" if tab == "signin" else "secondary",
                             key="tab_si"):
                    st.session_state.auth_tab = "signin"; st.rerun()
            with t2:
                if st.button("Create Account", use_container_width=True,
                             type="primary" if tab == "register" else "secondary",
                             key="tab_reg"):
                    st.session_state.auth_tab = "register"; st.rerun()
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # ════════════════════════════════════════════════════
        # SIGN IN
        # ════════════════════════════════════════════════════
        if tab == "signin":
            with st.container():
                st.markdown("##### Sign in to your account")
                st.markdown("<br>", unsafe_allow_html=True)

                login_id = st.text_input("Email or Username", placeholder="you@email.com or username", key="li_id")
                login_pw = st.text_input("Password", type="password", placeholder="Your password", key="li_pw")

                c1, c2 = st.columns([3, 1.2])
                with c1:
                    login_btn = st.button("Sign In →", use_container_width=True, key="btn_login")
                with c2:
                    forgot_btn = st.button("Forgot?", use_container_width=True, key="btn_forgot")

            if forgot_btn:
                st.session_state.auth_tab = "forgot"; st.rerun()

            if login_btn:
                if not login_id.strip() or not login_pw.strip():
                    st.error("Please fill in all fields.")
                else:
                    try:
                        with st.spinner("Signing in…"):
                            user = login_user(login_id, login_pw)
                        st.session_state.user = user
                        st.session_state.auth_tab = "signin"
                        st.rerun()
                    except ValueError as e: st.error(str(e))
                    except Exception as e:  st.error(f"Login failed: {e}")

        # ════════════════════════════════════════════════════
        # REGISTER
        # ════════════════════════════════════════════════════
        elif tab == "register":
            with st.container():
                st.markdown("##### Create your account")
                st.markdown("<br>", unsafe_allow_html=True)

                r_name  = st.text_input("Full Name",        placeholder="Arjun Kumar",     key="r_name")
                r_user  = st.text_input("Username",         placeholder="arjun_kumar",     key="r_user")
                r_email = st.text_input("Email",            placeholder="arjun@email.com", key="r_email")
                c1, c2  = st.columns(2)
                with c1: r_pw  = st.text_input("Password",         type="password", placeholder="Min 6 chars", key="r_pw")
                with c2: r_pw2 = st.text_input("Confirm Password", type="password", placeholder="Re-enter",    key="r_pw2")

                reg_btn = st.button("Create Account →", use_container_width=True, key="btn_reg")

            if reg_btn:
                errs = []
                if not r_name.strip(): errs.append("Full name is required.")
                if not r_user.strip(): errs.append("Username is required.")
                elif " " in r_user:    errs.append("Username cannot have spaces.")
                if not r_email.strip():         errs.append("Email is required.")
                elif not validate_email(r_email): errs.append(f"'{r_email.strip()}' is not a valid email — use name@domain.com")
                if not r_pw.strip():   errs.append("Password is required.")
                elif len(r_pw) < 6:    errs.append("Password must be at least 6 characters.")
                elif r_pw != r_pw2:    errs.append("Passwords do not match.")
                if errs:
                    for e in errs: st.error(e)
                else:
                    try:
                        with st.spinner("Creating account…"):
                            user = register_user(r_user.strip(), r_email.strip(), r_pw, r_name.strip())
                        st.session_state.user = user
                        st.session_state.auth_tab = "signin"
                        st.rerun()
                    except ValueError as e: st.error(str(e))
                    except Exception as e:  st.error(f"Registration failed: {e}")

        # ════════════════════════════════════════════════════
        # FORGOT PASSWORD
        # ════════════════════════════════════════════════════
        elif tab == "forgot":
            with st.container():
                st.markdown("##### Reset your password")
                st.markdown("<p style='color:#6B7280;font-size:.85rem;margin:4px 0 8px'>Enter your registered email and choose a new password.</p>", unsafe_allow_html=True)

                fp_email = st.text_input("Registered Email", placeholder="you@email.com", key="fp_email")
                c1, c2   = st.columns(2)
                with c1: fp_pw  = st.text_input("New Password",     type="password", placeholder="Min 6 chars", key="fp_pw")
                with c2: fp_pw2 = st.text_input("Confirm Password", type="password", placeholder="Re-enter",    key="fp_pw2")

                bc1, bc2 = st.columns([2.5, 1])
                with bc1: reset_btn = st.button("Reset Password →", use_container_width=True, key="btn_reset")
                with bc2: back_btn  = st.button("← Back",           use_container_width=True, key="btn_back_fp")

            if back_btn:
                st.session_state.auth_tab = "signin"; st.rerun()

            if reset_btn:
                errs = []
                if not fp_email.strip():          errs.append("Email is required.")
                elif not validate_email(fp_email): errs.append(f"'{fp_email.strip()}' is not a valid email.")
                if not fp_pw.strip():  errs.append("New password is required.")
                elif len(fp_pw) < 6:   errs.append("Password must be at least 6 characters.")
                elif fp_pw != fp_pw2:  errs.append("Passwords do not match.")
                if errs:
                    for e in errs: st.error(e)
                else:
                    try:
                        reset_password(fp_email.strip(), fp_pw)
                        st.success("Password reset! Please sign in with your new password.")
                        import time; time.sleep(1.2)
                        st.session_state.auth_tab = "signin"; st.rerun()
                    except ValueError as e: st.error(str(e))
                    except Exception as e:  st.error(f"Reset failed: {e}")

        # ── Footer ───────────────────────────────────────────
        H("""
<div style="text-align:center;padding:28px 0 8px;">
  <div style="display:inline-flex;flex-direction:column;align-items:center;
              background:#F9FAFB;border:1px solid #E5E7EB;border-radius:14px;
              padding:16px 32px;">
    <div style="font-size:1.15rem;font-weight:800;color:#111827;letter-spacing:-.3px;">
      🌟 Built by <span style="color:#6366F1;">Vishnuram</span>
    </div>
    <div style="font-size:.82rem;color:#6B7280;margin-top:4px;font-weight:500;">
      Software Engineer &nbsp;·&nbsp; TCE Alumni
    </div>
  </div>
</div>""", 100)


# ─────────────────────────────────────────────────────────────
# ██  SIDEBAR
# ─────────────────────────────────────────────────────────────
def render_sidebar(user) -> str:
    with st.sidebar:

        # ── Brand ─────────────────────────────────────────
        H(f"""
<div style="padding:22px 16px 16px;">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
    <div style="width:32px;height:32px;background:#6366F1;border-radius:8px;
                display:flex;align-items:center;justify-content:center;font-size:1rem;">🌟</div>
    <div>
      <div style="font-weight:700;font-size:.95rem;color:#F9FAFB;">Jyotish Match</div>
      <div style="font-size:.65rem;color:#6B7280;margin-top:1px;">by Vishnuram · TCE Alumni</div>
    </div>
  </div>
  <div style="background:#1F2937;border-radius:10px;padding:12px 14px;">
    <div style="display:flex;align-items:center;gap:10px;">
      <div style="width:34px;height:34px;border-radius:50%;background:#6366F1;flex-shrink:0;
                  display:flex;align-items:center;justify-content:center;
                  font-weight:700;font-size:.9rem;color:white;">
        {user['display_name'][0].upper()}
      </div>
      <div>
        <div style="font-weight:600;color:#F9FAFB;font-size:.88rem;">{user['display_name']}</div>
        <div style="color:#6B7280;font-size:.7rem;margin-top:1px;">@{user['username']}</div>
      </div>
    </div>
  </div>
</div>""", 148)

        # ── Stats row ─────────────────────────────────────
        try:
            s = get_user_stats(user["id"])
            H(f"""
<div style="padding:0 16px 16px;display:grid;grid-template-columns:1fr 1fr;gap:8px;">
  <div style="background:#1F2937;border-radius:8px;padding:10px 12px;text-align:center;">
    <div style="font-weight:700;color:#A5B4FC;font-size:1.05rem;">{s['total_matches']}</div>
    <div style="color:#6B7280;font-size:.62rem;margin-top:2px;">Matches</div>
  </div>
  <div style="background:#1F2937;border-radius:8px;padding:10px 12px;text-align:center;">
    <div style="font-weight:700;color:#6EE7B7;font-size:1.05rem;">{s['best_score']}%</div>
    <div style="color:#6B7280;font-size:.62rem;margin-top:2px;">Best Score</div>
  </div>
  <div style="background:#1F2937;border-radius:8px;padding:10px 12px;text-align:center;">
    <div style="font-weight:700;color:#FCD34D;font-size:1.05rem;">{s['avg_score']}%</div>
    <div style="color:#6B7280;font-size:.62rem;margin-top:2px;">Avg Score</div>
  </div>
  <div style="background:#1F2937;border-radius:8px;padding:10px 12px;text-align:center;">
    <div style="font-weight:700;color:#FCA5A5;font-size:1.05rem;">{s['saved_horoscopes']}</div>
    <div style="color:#6B7280;font-size:.62rem;margin-top:2px;">Saved</div>
  </div>
</div>""", 110)
        except Exception:
            pass

        st.markdown("---")

        # ── Navigation ────────────────────────────────────
        nav = st.radio("Navigation", [
            "🔮  New Match",
            "📚  Match History",
            "👤  My Profile",
        ], label_visibility="collapsed", key="nav")

        st.markdown("---")

        # ── Recent matches ────────────────────────────────
        try:
            history = get_user_match_history(user["id"])
            if history:
                H("""<div style="padding:0 6px 8px;">
  <div style="font-size:.68rem;color:#6B7280;font-weight:600;
              text-transform:uppercase;letter-spacing:1px;">Recent Matches</div>
</div>""", 28)
                for m in history[:4]:
                    sc  = score_color(float(m["final_percentage"]))
                    pct = float(m["final_percentage"])
                    ts  = fmt_ts(m["matched_at"])
                    H(f"""
<div style="background:#1F2937;border-radius:8px;padding:9px 12px;
            margin-bottom:6px;border-left:3px solid {sc};">
  <div style="font-weight:600;color:#E5E7EB;font-size:.77rem;
              white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
    {m['groom_name']} · {m['bride_name']}
  </div>
  <div style="display:flex;justify-content:space-between;margin-top:4px;align-items:center;">
    <span style="color:{sc};font-weight:700;font-size:.8rem;">{pct:.0f}%</span>
    <span style="color:#4B5563;font-size:.65rem;" class="utc-time" data-utc="{ts}"></span>
  </div>
</div>
<script>
  document.querySelectorAll('.utc-time').forEach(function(el){{
    var u = el.getAttribute('data-utc');
    if(u) el.textContent = new Date(u).toLocaleDateString(undefined,{{month:'short',day:'numeric'}});
  }});
</script>""", 60)
        except Exception:
            pass

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True, key="logout_btn"):
            for k in ["user","page","view_match_id","calc_result"]:
                st.session_state[k] = None if k != "page" else "login"
            st.rerun()

        H(FOOTER_HTML, 46)

    return nav


# ─────────────────────────────────────────────────────────────
# ██  PAGE: NEW MATCH
# ─────────────────────────────────────────────────────────────
def page_new_match(user):
    greeting_banner(user, "Ready to calculate a horoscope match today?")
    H("""
<div style="padding:2px 0 14px;">
  <div style="font-size:1.4rem;font-weight:700;color:#111827;">New Match</div>
  <div style="color:#6B7280;font-size:.84rem;margin-top:3px;">
    Enter birth star details for both parties below
  </div>
</div>""", 72)

    # ── Form in two columns ────────────────────────────────────
    fc1, fc2 = st.columns(2)

    with fc1:
        st.markdown("""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:16px;padding:24px;
            margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.05);">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;
              padding-bottom:14px;border-bottom:1px solid #F3F4F6;">
    <div style="width:36px;height:36px;border-radius:50%;background:#EEF2FF;
                display:flex;align-items:center;justify-content:center;font-size:1.1rem;">🤵</div>
    <div>
      <div style="font-weight:600;color:#111827;font-size:.95rem;">Groom Details</div>
      <div style="font-size:.72rem;color:#9CA3AF;margin-top:1px;">Birth star information</div>
    </div>
  </div>""", unsafe_allow_html=True)

        groom_name = st.text_input("Full Name", placeholder="e.g. Arjun Kumar", key="gn")
        g_star_opt = st.selectbox("⭐ Nakshatra (Birth Star)", STAR_OPTS, index=0, key="gs")
        g_star_n   = sname(g_star_opt)
        g_si       = gstar(g_star_n)
        g_padham_opts = [f"Padham {i}  →  {get_padham_navamsa(g_si['id'],i)} Navamsa" for i in range(1,5)]
        g_padham_sel  = st.selectbox("🔢 Padham (Quarter)", g_padham_opts, key="gp",
                                      help="Each Nakshatra has 4 Padhams (quarters) of 3°20' each")
        g_padham      = int(g_padham_sel.split()[1])
        g_rasi_def    = next((i for i,r in enumerate(RASI_OPTS)
                              if g_si.get("rasi","").split("/")[0].strip() in r), 0)
        g_rasi_opt    = st.selectbox("♈ Rasi (Moon Sign)", RASI_OPTS, index=g_rasi_def, key="gr",
                                      help="Auto-suggested from Nakshatra. Adjust if star spans 2 Rasis.")
        st.markdown("</div>", unsafe_allow_html=True)

    with fc2:
        st.markdown("""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:16px;padding:24px;
            margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.05);">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;
              padding-bottom:14px;border-bottom:1px solid #F3F4F6;">
    <div style="width:36px;height:36px;border-radius:50%;background:#FFF0F3;
                display:flex;align-items:center;justify-content:center;font-size:1.1rem;">👰</div>
    <div>
      <div style="font-weight:600;color:#111827;font-size:.95rem;">Bride Details</div>
      <div style="font-size:.72rem;color:#9CA3AF;margin-top:1px;">Birth star information</div>
    </div>
  </div>""", unsafe_allow_html=True)

        bride_name = st.text_input("Full Name", placeholder="e.g. Priya Devi", key="bn")
        b_star_opt = st.selectbox("⭐ Nakshatra (Birth Star)", STAR_OPTS, index=3, key="bs")
        b_star_n   = sname(b_star_opt)
        b_si       = gstar(b_star_n)
        b_padham_opts = [f"Padham {i}  →  {get_padham_navamsa(b_si['id'],i)} Navamsa" for i in range(1,5)]
        b_padham_sel  = st.selectbox("🔢 Padham (Quarter)", b_padham_opts, key="bp",
                                      help="Each Nakshatra has 4 Padhams (quarters) of 3°20' each")
        b_padham      = int(b_padham_sel.split()[1])
        b_rasi_def    = next((i for i,r in enumerate(RASI_OPTS)
                              if b_si.get("rasi","").split("/")[0].strip() in r), 3)
        b_rasi_opt    = st.selectbox("♈ Rasi (Moon Sign)", RASI_OPTS, index=b_rasi_def, key="br",
                                      help="Auto-suggested from Nakshatra.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Star preview cards
    g_ri_prev = grasi(rname(g_rasi_opt))
    b_ri_prev = grasi(rname(b_rasi_opt))
    pc1, pc2 = st.columns(2)
    with pc1: H(star_info_card("Groom's Horoscope","🤵", g_si, groom_name or "Groom", g_padham, g_ri_prev), 280)
    with pc2: H(star_info_card("Bride's Horoscope","👰", b_si, bride_name or "Bride", b_padham, b_ri_prev), 280)

    st.markdown("<br>", unsafe_allow_html=True)

    # Calculate button — full width, prominent
    calc_btn = st.button("🔮  Calculate Horoscope Match", use_container_width=True, key="calc_btn")

    if not calc_btn:
        H("""
<div style="text-align:center;padding:24px;
            background:#F9FAFB;
            border-radius:14px;border:2px dashed #E5E7EB;margin-top:16px;">
  <div style="font-size:1.8rem;margin-bottom:8px;">🔮</div>
  <div style="font-weight:700;color:#374151;font-size:1rem;">Ready to calculate?</div>
  <div style="color:#6B7280;font-size:.82rem;margin-top:4px;">
    Fill in both horoscope details above and hit
    <strong style="color:#6366F1;">Calculate Horoscope Match</strong>
  </div>
</div>""", 130)
        return

    # ── Run calculation ────────────────────────────────────────
    g_rasi_n = rname(g_rasi_opt)
    b_rasi_n = rname(b_rasi_opt)

    with st.spinner("✨ Calculating 10 Poruthams..."):
        engine  = AstroMatchingEngine(
            {"name": groom_name or "Groom", "star_name": g_star_n, "padham": g_padham, "rasi_name": g_rasi_n},
            {"name": bride_name or "Bride", "star_name": b_star_n, "padham": b_padham, "rasi_name": b_rasi_n}
        )
        summary = engine.calculate_all()
        st.session_state.calc_result = summary

        # Save to DB
        gid = save_horoscope(user["id"], groom_name or "Groom", "Male",   g_star_n, g_padham, g_rasi_n)
        bid = save_horoscope(user["id"], bride_name or "Bride", "Female", b_star_n, b_padham, b_rasi_n)
        mid = save_match_result(user["id"], gid, bid, summary)

    st.success(f"✅ Match calculated and saved to your history! (Match #{mid})")
    st.markdown("---")

    render_results(summary, user, g_padham, b_padham, g_star_n, b_star_n, g_rasi_n, b_rasi_n)


# ─────────────────────────────────────────────────────────────
# ██  PAGE: MATCH HISTORY
# ─────────────────────────────────────────────────────────────
def page_history(user):
    greeting_banner(user, "Your saved match results")
    H("""
<div style="padding:2px 0 14px;">
  <div style="font-size:1.4rem;font-weight:700;color:#111827;">Match History</div>
  <div style="color:#6B7280;font-size:.84rem;margin-top:3px;">All your previous horoscope comparisons</div>
</div>""", 72)

    # If viewing a specific match
    if st.session_state.view_match_id:
        match = get_match_by_id(st.session_state.view_match_id, user["id"])
        if match:
            bc1, _ = st.columns([1, 6])
            with bc1:
                if st.button("← Back to History", key="back_btn"):
                    st.session_state.view_match_id = None
                    st.rerun()

            # UTC → browser timestamp JS
            ts_iso = fmt_ts(match["matched_at"])
            H(f"""
<div style="background:linear-gradient(135deg,#111827,#16213e);border-radius:14px;
            padding:14px 18px;margin-bottom:16px;border:1px solid rgba(255,215,0,.15);">
  <div style="color:#9CA3AF;font-size:.7rem;text-transform:uppercase;letter-spacing:1px;">Matched On</div>
  <div id="match-ts" class="utc-time" data-utc="{ts_iso}"
       style="color:#6366F1;font-weight:600;font-size:.95rem;margin-top:3px;">
    {ts_iso}
  </div>
  <script>
    (function(){{
      var el = document.getElementById('match-ts');
      if(el){{
        var d = new Date(el.getAttribute('data-utc'));
        el.textContent = d.toLocaleString(undefined, {{
          weekday:'short', year:'numeric', month:'long',
          day:'numeric', hour:'2-digit', minute:'2-digit'
        }});
      }}
    }})();
  </script>
</div>""", 76)

            s = match["summary"]
            render_results(s, user,
                           match["groom_padham"], match["bride_padham"],
                           match["groom_star"],   match["bride_star"],
                           match["groom_rasi"],   match["bride_rasi"])
        return

    # List all matches
    history = get_user_match_history(user["id"])
    if not history:
        H("""
<div style="text-align:center;padding:48px 20px;
            background:white;border-radius:20px;border:2px dashed #e8ddd0;margin-top:8px;">
  <div style="font-size:2.5rem;margin-bottom:12px;">📭</div>
  <div style="font-weight:700;color:#374151;font-size:1.05rem;">No matches yet</div>
  <div style="color:#6B7280;font-size:.84rem;margin-top:4px;">
    Go to <strong>New Match</strong> to calculate your first horoscope comparison
  </div>
</div>""", 168)
        return

    # Cards for each history item — with UTC→local JS
    for m in history:
        sc   = score_color(float(m["final_percentage"]))
        pct  = float(m["final_percentage"])
        ts   = fmt_ts(m["matched_at"])
        v_sh = m["verdict"].replace("✨","").replace("👍","").replace("🔍","").replace("⚠️","").strip()
        crit = m["critical_doshas"] if isinstance(m["critical_doshas"], list) else json.loads(m["critical_doshas"])
        mid  = m["id"]

        H(f"""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:14px;
            padding:18px 20px;margin-bottom:10px;
            border-left:4px solid {sc};
            box-shadow:0 1px 4px rgba(0,0,0,.05);">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
    <div style="flex:1;min-width:200px;">
      <div style="font-weight:600;color:#111827;font-size:.95rem;">
        🤵 {m['groom_name']} &nbsp;·&nbsp; 👰 {m['bride_name']}
      </div>
      <div style="color:#9CA3AF;font-size:.76rem;margin-top:4px;">
        {m['groom_star']} ({m['groom_rasi']})
        &nbsp;·&nbsp;
        {m['bride_star']} ({m['bride_rasi']})
      </div>
      <div style="display:flex;align-items:center;gap:10px;margin-top:5px;">
        <span class="utc-time" data-utc="{ts}"
              style="color:#9CA3AF;font-size:.73rem;">
          📅 {ts}
        </span>
        {'<span style="background:#ff4444;color:white;padding:2px 8px;border-radius:20px;font-size:.68rem;font-weight:700;">⚠️ '+str(len(crit))+' Critical Dosha(s)</span>' if crit else '<span style="background:#00C85122;color:#00C851;padding:2px 8px;border-radius:20px;font-size:.68rem;font-weight:700;border:1px solid #00C851;">✅ No Critical Doshas</span>'}
      </div>
    </div>
    <div style="text-align:right;flex-shrink:0;">
      <div style="color:{sc};font-weight:900;font-size:1.6rem;line-height:1;">{pct:.1f}%</div>
      <div style="color:#6B7280;font-size:.78rem;margin-top:3px;">{v_sh}</div>
    </div>
  </div>
  <div style="margin-top:12px;background:#F9FAFB;border-radius:6px;height:8px;overflow:hidden;">
    <div style="width:{pct}%;background:{sc};height:8px;border-radius:6px;"></div>
  </div>
</div>
<script>
  document.querySelectorAll('.utc-time').forEach(function(el){{
    var utc = el.getAttribute('data-utc');
    if(utc){{
      var d = new Date(utc);
      el.textContent = '📅 ' + d.toLocaleString(undefined, {{
        year:'numeric', month:'short', day:'numeric',
        hour:'2-digit', minute:'2-digit'
      }});
    }}
  }});
</script>""", 162)

        # Action row
        ac1, ac2, ac3 = st.columns([4, 1.2, 1.2])
        with ac2:
            if st.button("👁  View", key=f"view_{mid}", use_container_width=True):
                st.session_state.view_match_id = mid
                st.rerun()
        with ac3:
            m_full = get_match_by_id(mid, user["id"])
            if m_full:
                pdf   = generate_pdf(m_full["summary"], user)
                fname = (f"AstroMatch_{m['groom_name']}_{m['bride_name']}"
                         f"_{str(m['matched_at'])[:10]}.pdf")
                st.download_button("📄  PDF", pdf, fname, "application/pdf",
                                   key=f"pdf_{mid}", use_container_width=True)
        st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# ██  PAGE: PROFILE
# ─────────────────────────────────────────────────────────────
def page_profile(user):
    greeting_banner(user, "Manage your account")
    H("""
<div style="padding:2px 0 14px;">
  <div style="font-size:1.4rem;font-weight:700;color:#111827;">My Profile</div>
  <div style="color:#6B7280;font-size:.84rem;margin-top:3px;">Account details and statistics</div>
</div>""", 72)

    try:
        stats = get_user_stats(user["id"])
    except Exception:
        stats = {"total_matches":0,"avg_score":0,"best_score":0,"saved_horoscopes":0}

    H(f"""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;">
  {"".join(f'''<div style="background:#fff;border:1px solid #E5E7EB;border-radius:12px;
                padding:18px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.05);">
    <div style="font-size:1.7rem;font-weight:700;color:{c};">{val}</div>
    <div style="color:#9CA3AF;font-size:.73rem;margin-top:4px;font-weight:500;">{lbl}</div>
  </div>'''
  for val,lbl,c in [
    (stats['total_matches'],    'Total Matches',    '#6366F1'),
    (f"{stats['best_score']}%", 'Best Score',       '#10B981'),
    (f"{stats['avg_score']}%",  'Average Score',    '#F59E0B'),
    (stats['saved_horoscopes'], 'Saved Horoscopes', '#8B5CF6'),
  ])}
</div>""", 112)

    # Account info card
    H(f"""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:14px;padding:20px 22px;
            margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,.05);">
  <div style="font-weight:600;color:#111827;font-size:.95rem;margin-bottom:14px;">Account Information</div>
  <table style="width:100%;border-collapse:collapse;font-size:.86rem;">
    <tr style="border-bottom:1px solid #F9FAFB;">
      <td style="color:#6B7280;padding:9px 0;width:30%;">Username</td>
      <td style="color:#111827;font-weight:600;">@{user['username']}</td>
    </tr>
    <tr style="border-bottom:1px solid #F9FAFB;">
      <td style="color:#6B7280;padding:9px 0;">Email</td>
      <td style="color:#111827;font-weight:600;">{user.get('email','—')}</td>
    </tr>
    <tr style="border-bottom:1px solid #F9FAFB;">
      <td style="color:#6B7280;padding:9px 0;">Member Since</td>
      <td id="member-since" class="utc-time" data-utc="{fmt_ts(user['created_at'])}"
          style="color:#111827;font-weight:600;">{fmt_ts(user['created_at'])[:10]}</td>
    </tr>
    <tr>
      <td style="color:#6B7280;padding:9px 0;">Last Login</td>
      <td id="last-login" class="utc-time" data-utc="{fmt_ts(user.get('last_login',''))}"
          style="color:#111827;font-weight:600;">{fmt_ts(user.get('last_login',''))[:10] if user.get('last_login') else '—'}</td>
    </tr>
  </table>
  <script>
    document.querySelectorAll('.utc-time').forEach(function(el){{
      var utc=el.getAttribute('data-utc');
      if(utc && utc !== 'None' && utc.length > 5){{
        var d=new Date(utc);
        if(!isNaN(d)) el.textContent=d.toLocaleString(undefined,{{
          year:'numeric',month:'long',day:'numeric',
          hour:'2-digit',minute:'2-digit'
        }});
      }}
    }});
  </script>
</div>""", 194)

    # Edit profile
    st.subheader("✏️ Edit Profile")
    pc1, pc2 = st.columns(2)
    with pc1:
        new_name  = st.text_input("Display Name", value=user.get("display_name",""), key="pn")
        new_email = st.text_input("Email", value=user.get("email",""), key="pe")
        if st.button("💾  Save Profile", use_container_width=True, key="save_profile"):
            if new_email and not validate_email(new_email):
                st.error("Please enter a valid email address.")
            else:
                try:
                    update_user_profile(user["id"], new_name, new_email)
                    st.session_state.user["display_name"] = new_name
                    st.session_state.user["email"]        = new_email
                    st.success("✅ Profile updated successfully!")
                except Exception as e:
                    st.error(f"Update failed: {e}")

    # Saved horoscopes
    st.subheader("⭐ Saved Horoscopes")
    try:
        horoscopes = get_user_horoscopes(user["id"])
        if not horoscopes:
            st.info("No horoscopes saved yet. Run a match to save profiles automatically.")
        else:
            df = pd.DataFrame([{
                "Name": h["person_name"], "Gender": h["gender"],
                "Star": h["star_name"],   "Padham": h["padham"],
                "Rasi": h["rasi_name"],   "Saved":  str(h["created_at"])[:10],
            } for h in horoscopes])
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Could not load horoscopes: {e}")

    # Brand footer
    H(f"""
<div style="text-align:center;padding:22px 0 8px;color:#9CA3AF;font-size:.74rem;">
  🌟 Built by <strong style="color:#6366F1;">Vishnuram</strong>
  &nbsp;·&nbsp; Software Engineer &nbsp;·&nbsp; TCE Alumni
</div>""", 44)


# ─────────────────────────────────────────────────────────────
# ██  MAIN ROUTER
# ─────────────────────────────────────────────────────────────

if st.session_state.user is None:
    page_login()
else:
    nav = render_sidebar(st.session_state.user)

    if "New Match" in nav:
        page_new_match(st.session_state.user)
    elif "History" in nav:
        page_history(st.session_state.user)
    elif "Profile" in nav:
        page_profile(st.session_state.user)
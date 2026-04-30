import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CarWorthML | Smart Car Valuation",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS — Corporate Memphis 3D Claymorphic ──────────────────────────
CLAY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ── App Background ─────────────────────────── */
.stApp {
    background: #F2EDE4 !important;
}

/* ── Hide Streamlit Chrome ──────────────────── */
header[data-testid="stHeader"],
footer,
[data-testid="stDecoration"],
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
section[data-testid="stSidebarContent"] {
    display: none !important;
}

/* ── TABS ───────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF !important;
    border-radius: 100px !important;
    padding: 6px !important;
    gap: 2px !important;
    border: 2.5px solid #E0D8CE !important;
    box-shadow: 5px 5px 0px #CFC8BC !important;
    width: fit-content !important;
    margin: 20px auto 36px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 100px !important;
    padding: 10px 24px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    color: #7A6B5C !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.18s ease !important;
}

.stTabs [aria-selected="true"] {
    background: #FF6B35 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(255,107,53,0.35) !important;
}

.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ── FORM container ─────────────────────────── */
[data-testid="stForm"], [data-testid="column"] > [data-testid="stVerticalBlock"]:has(#form_col_marker) {
    background: #FFFFFF !important;
    border-radius: 28px !important;
    border: 2.5px solid #E0D8CE !important;
    box-shadow: 8px 8px 0px #CFC8BC, 0 24px 60px rgba(60,40,20,0.07) !important;
    padding: 36px 40px !important;
}

/* ── SELECTBOX ──────────────────────────────── */
div[data-baseweb="select"] > div:first-child {
    background: #F8F3EC !important;
    border: 2.5px solid #E0D8CE !important;
    border-radius: 16px !important;
    min-height: 56px !important;
    transition: border-color 0.15s !important;
}

div[data-baseweb="select"] > div:first-child:hover {
    border-color: #FF6B35 !important;
}

div[data-baseweb="select"] span {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #1A1210 !important;
}

/* ── INPUT LABELS ───────────────────────────── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSlider"] label {
    color: #5C4E3E !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
}

/* ── NUMBER INPUT ───────────────────────────── */
[data-testid="stNumberInput"] > div {
    background: #F8F3EC !important;
    border: 2.5px solid #E0D8CE !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}

[data-testid="stNumberInput"] input {
    background: transparent !important;
    border: none !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #1A1210 !important;
    padding: 16px !important;
    height: 56px !important;
}

/* ── SLIDER ─────────────────────────────────── */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, #FF6B35, #FF8C5A) !important;
}

/* ── SUBMIT / BUTTONS ───────────────────────── */
[data-testid="stFormSubmitButton"] > button,
.stButton > button {
    background: linear-gradient(145deg, #FF7A45, #FF6B35) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 100px !important;
    padding: 20px 48px !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 8px 0px #C84A10, 0 16px 40px rgba(255,107,53,0.28) !important;
    transform: translateY(0px) !important;
    transition: all 0.12s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    width: 100% !important;
    cursor: pointer !important;
}

[data-testid="stFormSubmitButton"] > button:hover,
.stButton > button:hover {
    box-shadow: 0 5px 0px #C84A10, 0 10px 25px rgba(255,107,53,0.22) !important;
    transform: translateY(3px) !important;
}

[data-testid="stFormSubmitButton"] > button:active,
.stButton > button:active {
    box-shadow: 0 1px 0px #C84A10, 0 4px 12px rgba(255,107,53,0.18) !important;
    transform: translateY(7px) !important;
}

/* ── METRICS ────────────────────────────────── */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border-radius: 22px !important;
    border: 2.5px solid #E0D8CE !important;
    box-shadow: 5px 5px 0px #CFC8BC !important;
    padding: 22px 26px !important;
}

[data-testid="stMetricLabel"] > div {
    color: #7A6B5C !important;
    font-size: 0.73rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}

[data-testid="stMetricValue"] > div {
    color: #1A1210 !important;
    font-size: 1.45rem !important;
    font-weight: 800 !important;
}

/* ── CHARTS ─────────────────────────────────── */
[data-testid="stArrowVegaLiteChart"] {
    border-radius: 20px !important;
    overflow: hidden !important;
    border: 2.5px solid #E0D8CE !important;
    box-shadow: 5px 5px 0px #CFC8BC !important;
    background: #FFFFFF !important;
    padding: 8px !important;
}

/* ── DATAFRAME ──────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 18px !important;
    border: 2.5px solid #E0D8CE !important;
    overflow: hidden !important;
    box-shadow: 4px 4px 0px #CFC8BC !important;
}

/* ── EXPANDER ───────────────────────────────── */
[data-testid="stExpander"] {
    border-radius: 16px !important;
    border: 2px solid #E0D8CE !important;
    background: #FFFFFF !important;
    box-shadow: 4px 4px 0px #CFC8BC !important;
    overflow: hidden !important;
}

/* ── CAPTION ────────────────────────────────── */
[data-testid="stCaptionContainer"] {
    color: #9A8B7C !important;
    font-size: 0.78rem !important;
}

/* ── SCROLLBAR ──────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F2EDE4; }
::-webkit-scrollbar-thumb { background: #D4CBBF; border-radius: 4px; }

/* ── GENERAL TEXT ───────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    color: #1A1210 !important;
}
</style>
"""
st.markdown(CLAY_CSS, unsafe_allow_html=True)


# ─── HELPER FUNCTIONS ───────────────────────────────────────────────────────

def clay_card(content: str, shadow_color: str = "#CFC8BC", bg: str = "#FFFFFF") -> str:
    return f"""
    <div style="
        background: {bg};
        border-radius: 28px;
        border: 2.5px solid #E0D8CE;
        box-shadow: 7px 7px 0px {shadow_color}, 0 20px 50px rgba(60,40,20,0.06);
        padding: 32px;
        margin-bottom: 20px;
    ">{content}</div>"""


def stat_card(icon: str, value: str, label: str, sublabel: str = "",
              bg: str = "#FFFFFF", shadow: str = "#CFC8BC",
              val_color: str = "#1A1210") -> str:
    return f"""
    <div style="
        background: {bg};
        border-radius: 24px;
        border: 2.5px solid #E0D8CE;
        box-shadow: 6px 6px 0px {shadow}, 0 16px 40px rgba(60,40,20,0.06);
        padding: 28px 24px;
        text-align: center;
        height: 100%;
    ">
        <div style="font-size: 2rem; margin-bottom: 10px; line-height:1;">{icon}</div>
        <div style="color:{val_color}; font-size:1.65rem; font-weight:900;
                    letter-spacing:-0.03em; line-height:1.1; margin-bottom:6px;">{value}</div>
        <div style="color:#5C4E3E; font-size:0.8rem; font-weight:700;
                    text-transform:uppercase; letter-spacing:0.06em;">{label}</div>
        <div style="color:#9A8B7C; font-size:0.73rem; margin-top:5px;">{sublabel}</div>
    </div>"""


def step_card(num: str, title: str, desc: str,
              num_bg: str = "#FFF0EA", num_color: str = "#FF6B35") -> str:
    return f"""
    <div style="
        background: #FFFFFF;
        border-radius: 24px;
        border: 2.5px solid #E0D8CE;
        box-shadow: 6px 6px 0px #CFC8BC, 0 16px 40px rgba(60,40,20,0.06);
        padding: 28px;
        height: 100%;
    ">
        <div style="
            display: inline-flex; align-items: center; justify-content: center;
            width: 44px; height: 44px;
            background: {num_bg}; border: 2px solid rgba(0,0,0,0.06);
            border-radius: 14px;
            font-size: 1rem; font-weight: 900; color: {num_color};
            margin-bottom: 18px;
        ">{num}</div>
        <div style="color:#1A1210; font-size:1.05rem; font-weight:800;
                    margin-bottom:10px;">{title}</div>
        <div style="color:#7A6B5C; font-size:0.88rem; line-height:1.65;">{desc}</div>
    </div>"""


def price_card(price: float) -> str:
    lakhs = price / 100_000
    if lakhs >= 1:
        display = f"₹{lakhs:.2f}L"
    else:
        display = f"₹{price:,.0f}"

    lines = [
        '<div style="',
        '    background: linear-gradient(145deg, #1C1640, #261E5A);',
        '    border-radius: 28px;',
        '    border: 2.5px solid #3D3280;',
        '    box-shadow: 8px 8px 0px #0E0A28, 0 24px 60px rgba(108,99,255,0.22);',
        '    padding: 44px 36px;',
        '    text-align: center;',
        '">',
        '    <div style="',
        '        color: rgba(200,190,255,0.7); font-size: 0.72rem; font-weight: 700;',
        '        letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 14px;',
        '    ">✦ Estimated Resale Value · 2026 Market</div>',
        '',
        '    <div style="',
        '        color: #FFFFFF; font-size: clamp(2.6rem, 6vw, 4rem);',
        '        font-weight: 900; letter-spacing: -0.04em; line-height: 1;',
        '        margin-bottom: 8px;',
        f'    ">{display}</div>',
        '',
        '    <div style="',
        '        color: rgba(200,190,255,0.55); font-size: 0.78rem; margin-bottom: 28px;',
        f'    ">= ₹{price:,.0f}</div>',
        '',
        '    <div style="',
        '        display: inline-flex; align-items: center; gap: 8px;',
        '        background: rgba(108,99,255,0.2); border: 1.5px solid rgba(108,99,255,0.35);',
        '        border-radius: 100px; padding: 8px 18px;',
        '">',
        '        <span style="color: #A89CFF; font-size: 0.8rem; font-weight: 600;">',
        '            ⚡ Hybrid ML + market comps',
        '        </span>',
        '    </div>',
        '</div>'
    ]
    return "".join(lines)


# ─── TABS ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🏠  Home", "🎯  Predict", "📊  Insights", "ℹ️  About"])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — HOME
# ════════════════════════════════════════════════════════════════════════════
with tab1:

    # ── HERO CARD ──────────────────────────────────────────────────────────
    hero_lines = [
        '<div style="',
        '    background: linear-gradient(135deg, #FFFFFF 0%, #FFF6EF 100%);',
        '    border-radius: 32px;',
        '    border: 2.5px solid #E0D8CE;',
        '    box-shadow: 10px 10px 0px #CFC8BC, 0 30px 80px rgba(60,40,20,0.08);',
        '    padding: 52px 56px;',
        '    margin-bottom: 28px;',
        '    display: flex;',
        '    align-items: center;',
        '    justify-content: space-between;',
        '    gap: 32px;',
        '    overflow: hidden;',
        '    position: relative;',
        '    flex-wrap: wrap;',
        '">',
        '    <!-- BG blobs -->',
        '    <div style="position:absolute;top:-60px;right:-40px;width:300px;height:300px;',
        '        background:radial-gradient(circle,rgba(255,107,53,0.10) 0%,transparent 70%);',
        '        border-radius:50%;pointer-events:none;"></div>',
        '    <div style="position:absolute;bottom:-80px;left:260px;width:240px;height:240px;',
        '        background:radial-gradient(circle,rgba(108,99,255,0.07) 0%,transparent 70%);',
        '        border-radius:50%;pointer-events:none;"></div>',
        '',
        '    <!-- Left: text -->',
        '    <div style="flex:1;min-width:260px;max-width:520px;position:relative;z-index:1;">',
        '        <div style="display:inline-flex;align-items:center;gap:8px;',
        '            background:rgba(255,107,53,0.10);border:1.5px solid rgba(255,107,53,0.22);',
        '            border-radius:100px;padding:6px 16px;margin-bottom:22px;">',
        '            <div style="width:7px;height:7px;background:#FF6B35;border-radius:50%;"></div>',
        '            <span style="color:#FF6B35;font-size:0.75rem;font-weight:700;',
        '                letter-spacing:0.06em;text-transform:uppercase;">AI-Powered Valuation</span>',
        '        </div>',
        '',
        '        <h1 style="font-size:clamp(2rem,4vw,3.2rem);font-weight:900;color:#1A1210;',
        '            letter-spacing:-0.04em;line-height:1.08;margin-bottom:16px;">',
        '            Know Your Car\'s<br>',
        '            <span style="background:linear-gradient(135deg,#FF6B35,#FF8C5A);',
        '                -webkit-background-clip:text;-webkit-text-fill-color:transparent;',
        '                background-clip:text;">True Worth.</span>',
        '        </h1>',
        '',
        '        <p style="color:#7A6B5C;font-size:1rem;line-height:1.72;',
        '            margin-bottom:26px;max-width:400px;">',
        '            India\'s accurate used car price predictor — trained on <strong style="color:#1A1210;">800+',
        '            real Quikr listings</strong> with 2026 market price correction.',
        '        </p>',
        '',
        '        <div style="display:flex;gap:10px;flex-wrap:wrap;">',
        '            <div style="background:#F8F3EC;border:2px solid #E0D8CE;border-radius:100px;',
        '                padding:8px 18px;font-size:0.81rem;font-weight:700;color:#5C4E3E;">',
        '                ✓ 25+ Brands',
        '            </div>',
        '            <div style="background:#EDFBF4;border:2px solid #B8EDD4;border-radius:100px;',
        '                padding:8px 18px;font-size:0.81rem;font-weight:700;color:#1A7040;">',
        '                ✓ 2026 Prices',
        '            </div>',
        '            <div style="background:#EEEEFF;border:2px solid #C4BEFF;border-radius:100px;',
        '                padding:8px 18px;font-size:0.81rem;font-weight:700;color:#3A30A0;">',
        '                ✓ Instant Result',
        '            </div>',
        '        </div>',
        '    </div>',
        '',
        '    <!-- Right: car SVG + floating badges -->',
        '    <div style="flex-shrink:0;position:relative;width:280px;height:190px;">',
        '        <svg viewBox="0 0 280 160" width="280" height="160" xmlns="http://www.w3.org/2000/svg">',
        '            <ellipse cx="140" cy="156" rx="112" ry="7" fill="rgba(0,0,0,0.09)"/>',
        '            <rect x="15" y="86" width="250" height="55" rx="27" fill="#FF6B35"/>',
        '            <rect x="15" y="86" width="250" height="22" rx="22" fill="#FF8C5A" opacity="0.45"/>',
        '            <path d="M64,86 Q89,40 120,35 L160,35 Q191,40 216,86 Z" fill="#FF6B35"/>',
        '            <path d="M74,86 Q97,48 124,43 L156,43 Q183,48 206,86 Z" fill="#FF8C5A" opacity="0.40"/>',
        '            <path d="M86,86 Q109,57 127,51 L153,51 Q171,57 194,86 Z" fill="#B8DEF0" opacity="0.88"/>',
        '            <path d="M96,86 Q113,67 127,62 L141,62 Q150,65 160,73"',
        '                stroke="white" stroke-width="2.5" fill="none" opacity="0.55" stroke-linecap="round"/>',
        '            <circle cx="68" cy="140" r="28" fill="#221A18"/>',
        '            <circle cx="68" cy="140" r="18" fill="#DDD8D0"/>',
        '            <circle cx="68" cy="140" r="7" fill="#221A18"/>',
        '            <circle cx="212" cy="140" r="28" fill="#221A18"/>',
        '            <circle cx="212" cy="140" r="18" fill="#DDD8D0"/>',
        '            <circle cx="212" cy="140" r="7" fill="#221A18"/>',
        '            <rect x="248" y="98" width="16" height="10" rx="5" fill="#FFD166" opacity="0.95"/>',
        '            <rect x="248" y="112" width="11" height="7" rx="3.5" fill="#FFD166" opacity="0.55"/>',
        '            <rect x="16" y="98" width="16" height="10" rx="5" fill="#FF4444" opacity="0.90"/>',
        '            <line x1="140" y1="91" x2="140" y2="134" stroke="#E85C28" stroke-width="2" opacity="0.65"/>',
        '            <rect x="154" y="112" width="17" height="4" rx="2" fill="#D85020" opacity="0.75"/>',
        '            <rect x="109" y="112" width="17" height="4" rx="2" fill="#D85020" opacity="0.75"/>',
        '            <rect x="18" y="134" width="24" height="6" rx="3" fill="#D85020" opacity="0.55"/>',
        '            <rect x="238" y="134" width="24" height="6" rx="3" fill="#D85020" opacity="0.55"/>',
        '        </svg>',
        '',
        '        <!-- Floating price tag -->',
        '        <div style="position:absolute;top:-8px;right:-14px;',
        '            background:#FFFFFF;border:2.5px solid #E0D8CE;',
        '            box-shadow:4px 4px 0px #CFC8BC;border-radius:18px;',
        '            padding:10px 16px;text-align:center;min-width:90px;">',
        '            <div style="font-size:0.62rem;font-weight:700;color:#9A8B7C;',
        '                text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px;">Est. Value</div>',
        '            <div style="font-size:1.1rem;font-weight:900;color:#FF6B35;',
        '                letter-spacing:-0.02em;">₹4.8L</div>',
        '        </div>',
        '',
        '        <!-- Floating year badge -->',
        '        <div style="position:absolute;bottom:8px;left:-12px;',
        '            background:#6C63FF;border:2.5px solid #4E46C0;',
        '            box-shadow:3px 3px 0px #3830A0;border-radius:14px;',
        '            padding:8px 14px;white-space:nowrap;">',
        '            <div style="font-size:0.7rem;font-weight:700;color:rgba(255,255,255,0.9);">📍 2026 Market</div>',
        '        </div>',
        '    </div>',
        '</div>'
    ]
    st.markdown("".join(hero_lines), unsafe_allow_html=True)

    # ── STAT CARDS ─────────────────────────────────────────────────────────
    s1, s2, s3, s4 = st.columns(4, gap="medium")
    s1.markdown(stat_card("🚗", "15k+", "Cars Analysed", "Kaggle + CarDekho data"), unsafe_allow_html=True)
    s2.markdown(stat_card("🏭", "40+", "Manufacturers", "Maruti to Mercedes",
                           bg="#FFFFFF", shadow="#CFC8BC"), unsafe_allow_html=True)
    s3.markdown(stat_card("🎯", "R² ~0.89", "Model Accuracy",
                           "Tree-based regressor",
                           bg="#FFFFFF", shadow="#CFC8BC",
                           val_color="#FF6B35"), unsafe_allow_html=True)
    s4.markdown(stat_card("⚡", "<1 sec", "Prediction Speed", "Instant valuation"), unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ── HOW IT WORKS ───────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin:12px 0 20px;">
        <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
            text-transform:uppercase;margin-bottom:8px;">How It Works</p>
        <h2 style="color:#1A1210;font-size:1.6rem;font-weight:900;letter-spacing:-0.03em;
            margin-bottom:4px;">Three steps to your valuation</h2>
        <p style="color:#7A6B5C;font-size:0.9rem;margin-bottom:0;">
            Simple inputs, smart ML, instant result.
        </p>
    </div>
    """, unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3, gap="medium")
    h1.markdown(step_card("01", "Select Your Car",
        "Pick manufacturer, model, fuel type, transmission, owner history, year, and kilometers driven.",
        "#FFF0EA", "#FF6B35"), unsafe_allow_html=True)
    h2.markdown(step_card("02", "ML Model Analyses",
        "A stronger tree-based model learns from 15k+ cleaned market listings and transaction examples.",
        "#EEEEFF", "#6C63FF"), unsafe_allow_html=True)
    h3.markdown(step_card("03", "Get Your Valuation",
        "Receive the estimated 2026 market price with context from similar car listings.",
        "#EDFBF4", "#1A7040"), unsafe_allow_html=True)

    # ── FOOTER ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:40px 0 20px;
        color:#9A8B7C;font-size:0.78rem;letter-spacing:0.03em;">
        CarWorthML · BCA Major Project · Chayan R Bisht · JEMTEC, Greater Noida · 2022–2025
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — PREDICT
# ════════════════════════════════════════════════════════════════════════════
with tab2:

    @st.cache_data
    def load_data():
        return pd.read_csv("Cleaned_Car_data.csv")

    @st.cache_resource
    def load_model():
        with open("LinearRegressionModel.pkl", "rb") as f:
            return pickle.load(f)

    @st.cache_data
    def load_meta():
        if os.path.exists("model_meta.pkl"):
            with open("model_meta.pkl", "rb") as f:
                return pickle.load(f)
        return {}

    def uses_log_transform(meta: dict) -> bool:
        return meta.get("log_transform", False)

    def format_owner_label(owner_value: str) -> str:
        mapping = {
            "first": "First Owner",
            "second": "Second Owner",
            "third": "Third Owner",
            "fourth+": "Fourth+ Owner",
            "unknown": "Unknown Owner",
        }
        return mapping.get(owner_value, str(owner_value).title())

    def build_market_snapshot(
        dataset: pd.DataFrame,
        company: str,
        car_name: str,
        fuel_type: str,
        transmission: str,
        owner: str,
        year: int,
        kms_driven: int,
    ):
        search_levels = [
            (
                "Exact model matches",
                (dataset["company"] == company)
                & (dataset["name"] == car_name)
                & (dataset["fuel_type"] == fuel_type)
                & (dataset["transmission"] == transmission)
                & (dataset["year"].between(year - 1, year + 1))
                & (dataset["kms_driven"].between(max(0, kms_driven - 20000), kms_driven + 20000)),
                0.65,
            ),
            (
                "Close model matches",
                (dataset["company"] == company)
                & (dataset["name"] == car_name)
                & (dataset["fuel_type"] == fuel_type)
                & (dataset["year"].between(year - 2, year + 2))
                & (dataset["kms_driven"].between(max(0, kms_driven - 35000), kms_driven + 35000)),
                0.50,
            ),
            (
                "Brand-level matches",
                (dataset["company"] == company)
                & (dataset["fuel_type"] == fuel_type)
                & (dataset["transmission"] == transmission)
                & (dataset["owner"] == owner)
                & (dataset["year"].between(year - 2, year + 2)),
                0.30,
            ),
        ]

        for label, mask, weight in search_levels:
            similar = dataset.loc[mask].copy()
            if len(similar) >= 3:
                return {
                    "label": label,
                    "similar": similar,
                    "weight": weight,
                    "median_price": float(similar["Price"].median()),
                    "price_min": float(similar["Price"].quantile(0.25)),
                    "price_max": float(similar["Price"].quantile(0.75)),
                }

        return None

    data_ok = model_ok = False
    try:
        df = load_data()
        data_ok = True
    except FileNotFoundError:
        st.error("❌ Cleaned_Car_data.csv not found. Run `python data_cleaning.py` first.")

    try:
        model = load_model()
        model_ok = True
    except FileNotFoundError:
        st.error("❌ LinearRegressionModel.pkl not found. Run `python model_training.py` first.")

    if data_ok and model_ok:
        meta = load_meta()
        log_transform = uses_log_transform(meta)

        st.markdown("""
        <div style="margin:8px 0 28px;">
            <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
                text-transform:uppercase;margin-bottom:6px;">Price Predictor</p>
            <h2 style="color:#1A1210;font-size:1.7rem;font-weight:900;
                letter-spacing:-0.03em;margin-bottom:4px;">Get Your Car's Market Value</h2>
            <p style="color:#7A6B5C;font-size:0.9rem;">
                Fill in your vehicle details for an instant 2026 market valuation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        form_col, result_col = st.columns([1.05, 0.95], gap="large")

        if "predict_clicked" not in st.session_state:
            st.session_state.predict_clicked = False

        # ── LEFT: FORM ─────────────────────────────────────────────────────
        with form_col:
            st.markdown("<div id='form_col_marker'></div>", unsafe_allow_html=True)
            companies_sorted = sorted(df["company"].unique())

            st.markdown("""
            <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.09em;
                text-transform:uppercase;margin-bottom:18px;">Vehicle Details</p>
            """, unsafe_allow_html=True)

            # Manufacturer
            company = st.selectbox(
                "Manufacturer",
                options=companies_sorted,
                help="Choose the car brand"
            )

            # Model filtered by company
            models_for_company = sorted(
                df[df["company"] == company]["name"].unique()
            )
            car_name = st.selectbox(
                "Model",
                options=models_for_company,
                help="Select the specific model variant"
            )

            # Fuel type
            fuel_type = st.selectbox(
                "Fuel Type",
                options=sorted(df["fuel_type"].unique()),
                help="Select fuel type"
            )

            transmission = st.selectbox(
                "Transmission",
                options=sorted(df["transmission"].unique()),
                help="Automatic vs manual affects market price meaningfully"
            )

            owner = st.selectbox(
                "Ownership History",
                options=sorted(df["owner"].unique()),
                format_func=format_owner_label,
                help="Lower-owner cars usually retain value better"
            )

            # Year
            year = st.slider(
                "Year of Manufacture",
                min_value=int(df["year"].min()),
                max_value=int(df["year"].max()),
                value=min(max(2018, int(df["year"].min())), int(df["year"].max())),
                step=1,
            )

            # KMs
            kms_driven = st.number_input(
                "Kilometers Driven",
                min_value=0,
                max_value=500_000,
                value=50_000,
                step=1_000,
            )

            st.caption(f"≈ {kms_driven // 15000} years of average Indian city driving")

            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

            if st.button("🚀  Predict Price →", use_container_width=True):
                st.session_state.predict_clicked = True

        # ── RIGHT: RESULT ──────────────────────────────────────────────────
        with result_col:

            if not st.session_state.predict_clicked:
                st.markdown("""
                <div style="
                    background: #FFFFFF;
                    border-radius: 28px;
                    border: 2.5px solid #E0D8CE;
                    box-shadow: 7px 7px 0px #CFC8BC;
                    padding: 52px 36px;
                    text-align: center;
                    min-height: 280px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                ">
                    <div style="font-size:3.5rem;margin-bottom:18px;opacity:0.18;">🚗</div>
                    <p style="color:#7A6B5C;font-size:0.92rem;line-height:1.65;max-width:220px;margin:0 auto;">
                        Fill in your car details and click
                        <strong style="color:#FF6B35;">Predict Price →</strong>
                        to see your 2026 market valuation.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            else:
                try:
                    input_df = pd.DataFrame(
                        [[car_name, company, year, 2026 - year, kms_driven, fuel_type, transmission, owner]],
                        columns=["name", "company", "year", "age", "kms_driven", "fuel_type", "transmission", "owner"],
                    )
                    pred_raw = model.predict(input_df)[0]
                    base_price = float(np.expm1(pred_raw) if log_transform else pred_raw)
                    base_price = max(base_price, 40_000.0)

                    market_snapshot = build_market_snapshot(
                        df,
                        company,
                        car_name,
                        fuel_type,
                        transmission,
                        owner,
                        year,
                        kms_driven,
                    )
                    price = base_price
                    if market_snapshot is not None:
                        weight = market_snapshot["weight"]
                        price = ((1 - weight) * base_price) + (weight * market_snapshot["median_price"])

                    # Price display card - fixed to not markdown inside clay_card
                    html_content = price_card(price)
                    st.markdown(html_content, unsafe_allow_html=True)

                    if market_snapshot is not None:
                        similar = market_snapshot["similar"]
                        st.markdown("""
                        <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;
                            letter-spacing:0.09em;text-transform:uppercase;
                            margin:22px 0 12px;">Comparable Market Listings</p>
                        """, unsafe_allow_html=True)

                        st.caption(
                            f"{market_snapshot['label']} · {len(similar)} listings used to steady the model output"
                        )
                        m1, m2, m3 = st.columns(3)
                        m1.metric("25th %ile", f"₹{market_snapshot['price_min']/100000:.1f}L")
                        m2.metric("Median", f"₹{market_snapshot['median_price']/100000:.1f}L")
                        m3.metric("75th %ile", f"₹{market_snapshot['price_max']/100000:.1f}L")

                        delta_pct = ((price - base_price) / base_price) * 100 if base_price else 0
                        st.caption(
                            f"Model-only estimate: ₹{base_price:,.0f} · "
                            f"market-adjusted estimate: ₹{price:,.0f} ({delta_pct:+.1f}%)"
                        )

                    # Summary table
                    st.markdown("""
                    <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;
                        letter-spacing:0.09em;text-transform:uppercase;
                        margin:22px 0 12px;">Input Summary</p>
                    """, unsafe_allow_html=True)

                    st.dataframe(
                        pd.DataFrame({
                            "Parameter": ["Manufacturer", "Model", "Year", "Fuel",
                                          "Transmission", "Owner", "KMs Driven", "Predicted Price"],
                            "Value": [
                                company, car_name, str(year),
                                fuel_type, transmission, format_owner_label(owner), f"{kms_driven:,} km",
                                f"₹{price:,.0f}",
                            ],
                        }),
                        use_container_width=True,
                        hide_index=True,
                    )

                except Exception as e:
                    st.markdown(clay_card(f"""
                    <p style="color:#CC4010;font-size:0.9rem;font-weight:700;margin-bottom:8px;">
                        Prediction error
                    </p>
                    <p style="color:#7A6B5C;font-size:0.84rem;margin:0;">
                        {str(e)}<br><br>
                        Try a different combination of manufacturer and model.
                    </p>
                    """), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — INSIGHTS
# ════════════════════════════════════════════════════════════════════════════
with tab3:

    @st.cache_data
    def load_data_insights():
        return pd.read_csv("Cleaned_Car_data.csv")

    try:
        df3 = load_data_insights()
        insights_ok = True
    except FileNotFoundError:
        st.error("❌ Cleaned_Car_data.csv not found.")
        insights_ok = False

    if insights_ok:

        st.markdown("""
        <div style="margin:8px 0 28px;">
            <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
                text-transform:uppercase;margin-bottom:6px;">Market Intelligence</p>
            <h2 style="color:#1A1210;font-size:1.7rem;font-weight:900;
                letter-spacing:-0.03em;margin-bottom:4px;">Market Insights</h2>
            <p style="color:#7A6B5C;font-size:0.9rem;">
                Price trends, brand comparisons, and fuel-type analysis across 816 listings.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # KPI metrics row
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total Records",   f"{len(df3):,}")
        k2.metric("Avg Price",       f"₹{df3['Price'].mean()/100000:.1f}L")
        k3.metric("Lowest",          f"₹{df3['Price'].min()/1000:.0f}K")
        k4.metric("Highest",         f"₹{df3['Price'].max()/100000:.1f}L")
        k5.metric("Brands",          f"{df3['company'].nunique()}")

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        # ── CHART 1: Avg Price by Manufacturer ─────────────────────────────
        st.markdown("""
        <div style="margin-bottom:16px;">
            <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;
                letter-spacing:0.09em;text-transform:uppercase;margin-bottom:4px;">Chart 01</p>
            <h3 style="color:#1A1210;font-size:1.15rem;font-weight:800;
                letter-spacing:-0.02em;margin-bottom:4px;">Average Resale Price by Manufacturer</h3>
            <p style="color:#7A6B5C;font-size:0.84rem;margin-bottom:0;">
                Luxury brands command highest resale. Maruti and Hyundai hold value well in mass-market.
            </p>
        </div>
        """, unsafe_allow_html=True)

        avg_co = (
            df3.groupby("company")["Price"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        avg_co.columns = ["Manufacturer", "Average Price"]
        avg_co["Average Price"] = avg_co["Average Price"].astype(int)

        c_lux, c_mass = st.columns(2, gap="large")

        lux = avg_co[avg_co["Average Price"] >= 600_000]
        mass = avg_co[avg_co["Average Price"] < 600_000]

        with c_lux:
            st.caption("Luxury & Premium segment")
            if not lux.empty:
                st.bar_chart(lux, x="Manufacturer", y="Average Price",
                             use_container_width=True, height=300, color="#FF6B35")

        with c_mass:
            st.caption("Mass market segment")
            if not mass.empty:
                st.bar_chart(mass, x="Manufacturer", y="Average Price",
                             use_container_width=True, height=300, color="#6C63FF")

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        # ── CHART 2: Fuel type ──────────────────────────────────────────────
        st.markdown("""
        <div style="margin:20px 0 16px;">
            <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;
                letter-spacing:0.09em;text-transform:uppercase;margin-bottom:4px;">Chart 02</p>
            <h3 style="color:#1A1210;font-size:1.15rem;font-weight:800;
                letter-spacing:-0.02em;margin-bottom:4px;">Price Distribution by Fuel Type</h3>
            <p style="color:#7A6B5C;font-size:0.84rem;margin-bottom:0;">
                Diesel vehicles typically fetch higher resale prices due to fuel efficiency and highway preference.
            </p>
        </div>
        """, unsafe_allow_html=True)

        f1, f2 = st.columns([1, 1], gap="large")

        with f1:
            avg_fuel = (
                df3.groupby("fuel_type")["Price"]
                .agg(["mean", "median"])
                .reset_index()
            )
            avg_fuel.columns = ["Fuel Type", "Average Price", "Median Price"]
            avg_fuel["Average Price"]    = avg_fuel["Average Price"].astype(int)
            avg_fuel["Median Price"] = avg_fuel["Median Price"].astype(int)
            st.bar_chart(
                avg_fuel,
                x="Fuel Type", y=["Average Price", "Median Price"],
                use_container_width=True, height=280,
                color=["#FF6B35", "#6C63FF"],
            )

        with f2:
            st.markdown("<p style='color:#9A8B7C;font-size:0.78rem;font-weight:600;"
                        "margin-bottom:14px;'>Listing Count by Fuel Type</p>",
                        unsafe_allow_html=True)
            fuel_counts = df3["fuel_type"].value_counts()
            total = len(df3)
            palette = {"Diesel": "#FF6B35", "Petrol": "#6C63FF", "LPG": "#FFD166"}
            for fuel, count in fuel_counts.items():
                pct = count / total * 100
                color = palette.get(fuel, "#9A8B7C")
                st.markdown(f"""
                <div style="background:#FFFFFF;border:2.5px solid #E0D8CE;
                    box-shadow:4px 4px 0px #CFC8BC;
                    border-radius:16px;padding:14px 20px;
                    margin-bottom:10px;display:flex;
                    align-items:center;justify-content:space-between;">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <div style="width:12px;height:12px;border-radius:50%;
                            background:{color};flex-shrink:0;"></div>
                        <span style="color:#1A1210;font-size:0.9rem;font-weight:700;">{fuel}</span>
                    </div>
                    <div>
                        <span style="color:#1A1210;font-size:0.9rem;font-weight:800;">{count:,}</span>
                        <span style="color:#9A8B7C;font-size:0.78rem;margin-left:6px;">({pct:.0f}%)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        # ── CHART 3: Price by Year ──────────────────────────────────────────
        st.markdown("""
        <div style="margin:20px 0 16px;">
            <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;
                letter-spacing:0.09em;text-transform:uppercase;margin-bottom:4px;">Chart 03</p>
            <h3 style="color:#1A1210;font-size:1.15rem;font-weight:800;
                letter-spacing:-0.02em;margin-bottom:4px;">Average Price by Manufacturing Year</h3>
            <p style="color:#7A6B5C;font-size:0.84rem;margin-bottom:0;">
                Newer cars depreciate less and command higher resale values in the 2026 market.
            </p>
        </div>
        """, unsafe_allow_html=True)

        price_yr = (
            df3.groupby("year")["Price"]
            .mean()
            .reset_index()
            .sort_values("year")
        )
        price_yr.columns = ["Year", "Average Price"]
        price_yr["Average Price"] = price_yr["Average Price"].astype(int)
        st.line_chart(price_yr, x="Year", y="Average Price",
                      use_container_width=True, height=300, color="#FF6B35")

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        # ── CHART 4: Top brands by listing count ───────────────────────────
        st.markdown("""
        <div style="margin:20px 0 16px;">
            <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;
                letter-spacing:0.09em;text-transform:uppercase;margin-bottom:4px;">Chart 04</p>
            <h3 style="color:#1A1210;font-size:1.15rem;font-weight:800;
                letter-spacing:-0.02em;margin-bottom:4px;">Top 10 Most Listed Manufacturers</h3>
            <p style="color:#7A6B5C;font-size:0.84rem;margin-bottom:0;">
                Maruti and Hyundai dominate resale listings — consistent with India's new car sales rankings.
            </p>
        </div>
        """, unsafe_allow_html=True)

        top10 = df3["company"].value_counts().head(10).reset_index()
        top10.columns = ["Manufacturer", "Listings"]
        st.bar_chart(top10, x="Manufacturer", y="Listings",
                     use_container_width=True, height=300, color="#4ECDC4")

        # ── RAW DATA EXPANDER ───────────────────────────────────────────────
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        with st.expander("📋  View raw dataset sample (first 20 rows)"):
            st.dataframe(df3.head(20), use_container_width=True, hide_index=True)
            st.caption(
                f"Showing 20 of {len(df3):,} records · {df3.shape[1]} columns · "
                f"Source: Quikr India used car listings (2019–2020) + 1.55× 2026 market correction"
            )


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ════════════════════════════════════════════════════════════════════════════
with tab4:

    st.markdown("""
    <div style="margin:8px 0 28px;">
        <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
            text-transform:uppercase;margin-bottom:6px;">Project Info</p>
        <h2 style="color:#1A1210;font-size:1.7rem;font-weight:900;
            letter-spacing:-0.03em;margin-bottom:4px;">About CarWorthML</h2>
        <p style="color:#7A6B5C;font-size:0.9rem;">
            BCA Major Project · JEMTEC, Greater Noida · Session 2022–2025
        </p>
    </div>
    """, unsafe_allow_html=True)

    id1, id2 = st.columns(2, gap="large")

    with id1:
        st.markdown(clay_card("""
        <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.09em;
            text-transform:uppercase;margin-bottom:18px;">Student Details</p>
        <table style="width:100%;border-collapse:collapse;">
            <tr>
                <td style="color:#9A8B7C;font-size:0.78rem;font-weight:600;
                    padding:9px 16px 9px 0;vertical-align:top;white-space:nowrap;
                    text-transform:uppercase;letter-spacing:0.04em;">Project</td>
                <td style="color:#1A1210;font-size:0.88rem;font-weight:500;padding:9px 0;line-height:1.4;">
                    CarWorthML – Used Car Price Predictor</td>
            </tr>
            <tr>
                <td style="color:#9A8B7C;font-size:0.78rem;font-weight:600;
                    padding:9px 16px 9px 0;vertical-align:top;
                    text-transform:uppercase;letter-spacing:0.04em;">Student</td>
                <td style="color:#1A1210;font-size:0.88rem;font-weight:500;padding:9px 0;">
                    Chayan R Bisht</td>
            </tr>
            <tr>
                <td style="color:#9A8B7C;font-size:0.78rem;font-weight:600;
                    padding:9px 16px 9px 0;vertical-align:top;
                    text-transform:uppercase;letter-spacing:0.04em;">Enrolment</td>
                <td style="color:#1A1210;font-size:0.88rem;font-weight:500;padding:9px 0;">
                    35625502022</td>
            </tr>
            <tr>
                <td style="color:#9A8B7C;font-size:0.78rem;font-weight:600;
                    padding:9px 16px 9px 0;vertical-align:top;
                    text-transform:uppercase;letter-spacing:0.04em;">Course</td>
                <td style="color:#1A1210;font-size:0.88rem;font-weight:500;padding:9px 0;">
                    BCA – VI Semester</td>
            </tr>
            <tr>
                <td style="color:#9A8B7C;font-size:0.78rem;font-weight:600;
                    padding:9px 16px 9px 0;
                    text-transform:uppercase;letter-spacing:0.04em;">Session</td>
                <td style="color:#1A1210;font-size:0.88rem;font-weight:500;padding:9px 0;">
                    2022 – 2025</td>
            </tr>
        </table>
        """), unsafe_allow_html=True)

    with id2:
        st.markdown(clay_card("""
        <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.09em;
            text-transform:uppercase;margin-bottom:18px;">Institution & Guide</p>
        <table style="width:100%;border-collapse:collapse;">
            <tr>
                <td style="color:#9A8B7C;font-size:0.78rem;font-weight:600;
                    padding:9px 16px 9px 0;vertical-align:top;white-space:nowrap;
                    text-transform:uppercase;letter-spacing:0.04em;">Guide</td>
                <td style="color:#1A1210;font-size:0.88rem;font-weight:500;padding:9px 0;">
                    Dr. Ruchi Agarwal</td>
            </tr>
            <tr>
                <td style="color:#9A8B7C;font-size:0.78rem;font-weight:600;
                    padding:9px 16px 9px 0;vertical-align:top;
                    text-transform:uppercase;letter-spacing:0.04em;">Role</td>
                <td style="color:#1A1210;font-size:0.88rem;font-weight:500;padding:9px 0;">
                    HOD, BCA Department</td>
            </tr>
            <tr>
                <td style="color:#9A8B7C;font-size:0.78rem;font-weight:600;
                    padding:9px 16px 9px 0;vertical-align:top;
                    text-transform:uppercase;letter-spacing:0.04em;">Institution</td>
                <td style="color:#1A1210;font-size:0.88rem;font-weight:500;padding:9px 0;line-height:1.4;">
                    JIMS Engineering Management Technical Campus (JEMTEC), Greater Noida</td>
            </tr>
            <tr>
                <td style="color:#9A8B7C;font-size:0.78rem;font-weight:600;
                    padding:9px 16px 9px 0;
                    text-transform:uppercase;letter-spacing:0.04em;">Affiliation</td>
                <td style="color:#1A1210;font-size:0.88rem;font-weight:500;padding:9px 0;">
                    GGSIPU, Delhi</td>
            </tr>
        </table>
        """), unsafe_allow_html=True)

    # ── TECH OVERVIEW ──────────────────────────────────────────────────────
    st.markdown("""
    <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.09em;
        text-transform:uppercase;margin:8px 0 16px;">Technical Overview</p>
    """, unsafe_allow_html=True)

    t1, t2 = st.columns([3, 2], gap="large")

    with t1:
        ml_pipeline_lines = [
            '<p style="color:#1A1210;font-size:1rem;font-weight:800;margin-bottom:18px;">',
            '    ML Pipeline</p>',
            '',
            '<p style="color:#7A6B5C;font-size:0.87rem;line-height:1.7;margin-bottom:16px;">',
            '    Real used-car market listings from Kaggle are merged with the local',
            '    CarDekho sample file and normalized into one clean dataset.',
            '    Brand, model, fuel type, transmission, and owner history become',
            '    model features alongside year, age, and kilometres driven.',
            '</p>',
            '<p style="color:#7A6B5C;font-size:0.87rem;line-height:1.7;margin-bottom:16px;">',
            '    Price is <strong style="color:#1A1210;">log-transformed</strong> before training —',
            '    this captures percentage-based depreciation and improves stability on expensive SUVs.',
            '    The app then uses a <strong style="color:#1A1210;">tree-based regressor</strong>',
            '    and steadies its output with nearby market comparables.',
            '</p>',
            '<div style="background:#F8F3EC;border:2px solid #E0D8CE;border-radius:14px;',
            '    padding:18px;font-family:monospace;font-size:0.8rem;color:#FF6B35;line-height:1.9;">',
            '    Input → [name, company, year, age, kms_driven, fuel_type, transmission, owner]<br>',
            '    ↓ categorical + numeric preprocessing<br>',
            '    ↓ CatBoost / ExtraTrees regressor<br>',
            '    ↓ exp() back to rupees<br>',
            '    ↓ blend with comparable market listings',
            '</div>'
        ]
        st.markdown(clay_card("".join(ml_pipeline_lines)), unsafe_allow_html=True)

    with t2:
        model_perf_lines = [
            '<p style="color:#1A1210;font-size:1rem;font-weight:800;margin-bottom:18px;">',
            '    Model Performance</p>',
            '',
            '<div style="margin-bottom:16px;">',
            '    <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;',
            '        text-transform:uppercase;letter-spacing:0.06em;margin-bottom:5px;">Algorithm</p>',
            '    <p style="color:#1A1210;font-size:0.9rem;font-weight:600;">',
            '        CatBoost / ExtraTrees hybrid</p>',
            '</div>',
            '<div style="margin-bottom:16px;">',
            '    <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;',
            '        text-transform:uppercase;letter-spacing:0.06em;margin-bottom:5px;">R² Score</p>',
            '    <p style="color:#FF6B35;font-size:1.5rem;font-weight:900;letter-spacing:-0.02em;">',
            '        ~0.89 (log-price holdout)</p>',
            '</div>',
            '<div style="margin-bottom:16px;">',
            '    <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;',
            '        text-transform:uppercase;letter-spacing:0.06em;margin-bottom:5px;">Holdout MAPE</p>',
            '    <p style="color:#1A1210;font-size:0.9rem;font-weight:600;">~19.7% on merged data</p>',
            '</div>',
            '<div style="margin-bottom:16px;">',
            '    <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;',
            '        text-transform:uppercase;letter-spacing:0.06em;margin-bottom:5px;">Dataset</p>',
            '    <p style="color:#1A1210;font-size:0.9rem;font-weight:600;">',
            '        15k+ merged Kaggle market listings + local CarDekho records</p>',
            '</div>',
            '<div>',
            '    <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;',
            '        text-transform:uppercase;letter-spacing:0.06em;margin-bottom:5px;">Price Transform</p>',
            '    <p style="color:#1A1210;font-size:0.9rem;font-weight:600;">',
            '        log(price) → exp() at inference</p>',
            '</div>'
        ]
        st.markdown(clay_card("".join(model_perf_lines)), unsafe_allow_html=True)

    # ── TECH STACK ─────────────────────────────────────────────────────────
    st.markdown("""
    <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.09em;
        text-transform:uppercase;margin:8px 0 16px;">Technology Stack</p>
    """, unsafe_allow_html=True)

    tech = [
        ("🐍", "Python 3.9+",         "Core language"),
        ("🤖", "Scikit-learn + CatBoost", "Tree ensemble pipeline and market-value model"),
        ("📊", "Pandas / NumPy",       "Data loading, cleaning, analysis"),
        ("🌐", "Streamlit 1.32",       "Web framework and UI"),
        ("📦", "Pickle",               "Model serialization"),
        ("🎨", "Custom CSS",           "Corporate Memphis 3D design"),
        ("📈", "Altair (st.bar_chart)","Market insight charts"),
        ("🔢", "NumPy (log/exp)",      "Price normalization pipeline"),
    ]

    rows = [tech[i:i+4] for i in range(0, len(tech), 4)]
    for row in rows:
        cols = st.columns(4, gap="medium")
        for col, (icon, name, desc) in zip(cols, row):
            col.markdown(f"""
            <div style="background:#FFFFFF;border:2.5px solid #E0D8CE;
                box-shadow:5px 5px 0px #CFC8BC;border-radius:20px;
                padding:20px;margin-bottom:12px;">
                <div style="font-size:1.5rem;margin-bottom:10px;">{icon}</div>
                <p style="color:#1A1210;font-size:0.88rem;font-weight:700;margin-bottom:4px;">{name}</p>
                <p style="color:#7A6B5C;font-size:0.76rem;margin:0;line-height:1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ── KNOWN LIMITATIONS ──────────────────────────────────────────────────
    st.markdown("""
    <p style="color:#9A8B7C;font-size:0.72rem;font-weight:700;letter-spacing:0.09em;
        text-transform:uppercase;margin:8px 0 16px;">Known Limitations</p>
    """, unsafe_allow_html=True)

    limitations = [
        ("No geolocation data",
         "Prices vary significantly across cities. This model does not account for city-level pricing."),
        ("Brand coverage",
         "Coverage is much broader now, but rare imports and ultra-niche trims can still be thinly represented."),
        ("Model limitations",
         "Trim, service history, accident record, and accessories are still not fully captured."),
        ("Dataset window",
         "Most market listings reflect recent ask prices, not final negotiated transaction values."),
        ("Condition not captured",
         "Accident history, service records, and physical condition significantly affect actual resale value."),
        ("No city-tier pricing",
         "Metro vs tier-2 city price differences of 10–20% are not modelled in this version."),
    ]

    lc1, lc2 = st.columns(2, gap="large")
    for i, (title, desc) in enumerate(limitations):
        col = lc1 if i % 2 == 0 else lc2
        col.markdown(f"""
        <div style="background:#FFFFFF;border-left:4px solid #FF6B35;
            border:2.5px solid #E0D8CE;border-left-width:4px;
            border-radius:16px;padding:16px 20px;margin-bottom:10px;
            box-shadow:4px 4px 0px #CFC8BC;">
            <p style="color:#1A1210;font-size:0.88rem;font-weight:700;
                margin-bottom:5px;">⚠ {title}</p>
            <p style="color:#7A6B5C;font-size:0.81rem;margin:0;line-height:1.55;">
                {desc}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── FOOTER ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:40px 0 20px;border-top:2px solid #E0D8CE;margin-top:24px;">
        <p style="color:#1A1210;font-size:1rem;font-weight:900;letter-spacing:-0.02em;
            margin-bottom:6px;">CarWorthML</p>
        <p style="color:#9A8B7C;font-size:0.8rem;margin-bottom:4px;">
            BCA Major Project · Chayan R Bisht · 35625502022
        </p>
        <p style="color:#9A8B7C;font-size:0.78rem;margin-bottom:0;">
            JEMTEC, Greater Noida · Affiliated to GGSIPU · Session 2022–2025
        </p>
        <p style="color:#CFC8BC;font-size:0.7rem;margin-top:16px;">© 2025 Chayan R Bisht</p>
    </div>
    """, unsafe_allow_html=True)

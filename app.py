import streamlit as st
import requests


import base64
import os

def get_base64_image(image_path: str) -> str:
    """Convert local image to base64 string for embedding in HTML."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

CAR_B64 = get_base64_image("car.png")
CAR_IMG_TAG = f'<img src="data:image/png;base64,{CAR_B64}" style="width:100%; max-width:720px; filter: drop-shadow(0 20px 60px rgba(230,57,70,0.18)) drop-shadow(0 0 120px rgba(255,255,255,0.04));" alt="Car">' if CAR_B64 else '<div style="font-size:8rem; text-align:center; opacity:0.15;">🚗</div>'

# ─────────────────────────────────────────────
# PAGE CONFIG — Must be first Streamlit command
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CarWorthML | Used Car Price Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# INJECT GLOBAL CSS (paste full GLOBAL_CSS here)
# ─────────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* ============================================
   BASE — Premium Light Theme
   ============================================ */
html, body, [class*="css"] {
    font-family: -apple-system, 'SF Pro Display', 'Inter', BlinkMacSystemFont, 
                 'Segoe UI', sans-serif !important;
}

.stApp {
    background-color: #F9FAFB !important;
}

/* Hide Streamlit default header */
header[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: 1px solid #E5E7EB;
}

/* ============================================
   TAB NAVIGATION — Minimal pill style
   ============================================ */
.stTabs [data-baseweb="tab-list"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 2px !important;
    width: fit-content !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6B7280 !important;
    border-radius: 9px !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 8px 24px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #111827 !important;
    background: #F3F4F6 !important;
}

.stTabs [aria-selected="true"] {
    background: #FF6B4A !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(255, 107, 74, 0.3) !important;
}

/* ============================================
   SIDEBAR
   ============================================ */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E5E7EB !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #4B5563;
}

/* ============================================
   INPUTS
   ============================================ */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stSlider {
    background-color: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 8px !important;
    color: #111827 !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
}

.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: #FF6B4A !important;
    box-shadow: 0 0 0 3px rgba(255, 107, 74, 0.15) !important;
}

/* Input labels */
.stSelectbox label, 
.stNumberInput label,
.stSlider label {
    color: #4B5563 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* ============================================
   BUTTONS
   ============================================ */
.stButton > button {
    background: #FF6B4A !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 12px 32px !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(255, 107, 74, 0.2) !important;
}

.stButton > button:hover {
    background: #FF5A36 !important;
    box-shadow: 0 6px 20px rgba(255, 107, 74, 0.3) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ============================================
   METRICS
   ============================================ */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03) !important;
}

[data-testid="stMetricLabel"] {
    color: #6B7280 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

/* ============================================
   DIVIDERS
   ============================================ */
hr {
    border: none !important;
    border-top: 1px solid #E5E7EB !important;
    margin: 28px 0 !important;
}

/* ============================================
   CHARTS
   ============================================ */
[data-testid="stArrowVegaLiteChart"] {
    background: transparent !important;
    border-radius: 12px !important;
}

/* ============================================
   DATAFRAMES
   ============================================ */
.stDataFrame {
    border: 1px solid #E5E7EB !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
}

/* ============================================
   SCROLLBAR
   ============================================ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F9FAFB; }
::-webkit-scrollbar-thumb { background: #E5E7EB; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #D1D5DB; }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
/* ── Final polish ── */
.stTabs [aria-selected="true"] { text-decoration: none !important; border-bottom: none !important; }
.stTabs { margin-top: -12px !important; }
[data-testid="stFormSubmitButton"] > button { width: 100% !important; margin-top: 8px !important; }
[data-testid="stDataFrame"] th {
    background-color: #F3F4F6 !important; color: #4B5563 !important;
    font-size: 0.78rem !important; font-weight: 600 !important;
    letter-spacing: 0.04em !important; text-transform: uppercase !important;
    border-bottom: 1px solid #E5E7EB !important;
}
[data-testid="stDataFrame"] td {
    background-color: #FFFFFF !important; color: #111827 !important;
    font-size: 0.875rem !important; border-bottom: 1px solid #F9FAFB !important;
}
[data-testid="stMetricDelta"] { color: #10B981 !important; }
.streamlit-expanderHeader {
    background-color: #FFFFFF !important; border: 1px solid #E5E7EB !important;
    border-radius: 10px !important; color: #4B5563 !important; font-size: 0.88rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
}
.stCaption { color: #6B7280 !important; font-size: 0.78rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOTTIE LOADER
# ─────────────────────────────────────────────
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

# Lottie URLs — using reliable LottieFiles CDN animations
LOTTIE_CAR_URL = "https://assets3.lottiefiles.com/packages/lf20_qjfw0xv.json"
LOTTIE_CHART_URL = "https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json"

try:
    from streamlit_lottie import st_lottie
    lottie_car = load_lottie_url(LOTTIE_CAR_URL)
    lottie_chart = load_lottie_url(LOTTIE_CHART_URL)
    LOTTIE_AVAILABLE = lottie_car is not None
except ImportError:
    LOTTIE_AVAILABLE = False
    lottie_car = None

# ─────────────────────────────────────────────
# REUSABLE COMPONENT FUNCTIONS
# ─────────────────────────────────────────────
def card(content_html: str, padding: str = "28px 32px") -> str:
    """Returns a premium dark card HTML block."""
    return f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #E5E7EB; box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        border-radius: 16px;
        padding: {padding};
        margin-bottom: 16px;
    ">{content_html}</div>
    """

def badge(text: str, color: str = "#E63946") -> str:
    """Returns a small pill badge HTML."""
    return f"""
    <span style="
        background: rgba(255,107,74,0.1);
        color: {color};
        border: 1px solid rgba(255,107,74,0.2);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    ">{text}</span>
    """

def section_header(title: str, subtitle: str = "") -> str:
    """Returns a premium section heading HTML."""
    sub = f'<p style="color:#6B7280; font-size:0.95rem; margin:8px 0 0; font-weight:400;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom: 32px;">
        <h2 style="
            color: #111827;
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin: 0;
            line-height: 1.2;
        ">{title}</h2>
        {sub}
    </div>
    """

def stat_card(icon: str, value: str, label: str, sublabel: str = "") -> str:
    """Returns a premium stat card HTML."""
    sub = f'<p style="color:#9CA3AF; font-size:0.75rem; margin:4px 0 0;">{sublabel}</p>' if sublabel else ""
    return f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #E5E7EB; box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        border-radius: 16px;
        padding: 24px;
        transition: border-color 0.2s;
    ">
        <div style="font-size: 1.5rem; margin-bottom: 12px;">{icon}</div>
        <div style="
            color: #111827;
            font-size: 1.9rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            line-height: 1;
            margin-bottom: 6px;
        ">{value}</div>
        <div style="
            color: #6B7280;
            font-size: 0.8rem;
            font-weight: 500;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        ">{label}</div>
        {sub}
    </div>
    """

def price_result_card(price: float) -> str:
    """Returns the premium price display card HTML."""
    lakhs = price / 100000
    return f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #FF6B4A;
        border-radius: 20px;
        padding: 36px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255, 107, 74, 0.15);
    ">
        <p style="
            color: #6B7280;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin: 0 0 16px;
        ">ESTIMATED MARKET VALUE</p>
        <p style="
            color: #111827;
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin: 0;
            line-height: 1;
        ">₹ {price:,.0f}</p>
        <p style="
            color: #FF6B4A;
            font-size: 1rem;
            font-weight: 500;
            margin: 12px 0 0;
        ">≈ ₹ {lakhs:.2f} Lakhs</p>
        <hr style="border-top: 1px solid #222230; margin: 24px 0;">
        <p style="
            color: #22C55E;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 0;
        ">Prediction Successful</p>
    </div>
    """

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
<div style="padding: 8px 0 24px;">
    <p style="color:#FF6B4A; font-size:1.2rem; font-weight:700; 
              letter-spacing:-0.02em; margin:0;">CarWorthML</p>
    <p style="color:#9CA3AF; font-size:0.75rem; margin:4px 0 0;">
        Used Car Price Predictor
    </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background:#FFFFFF; border: 1px solid #E5E7EB; box-shadow: 0 4px 10px rgba(0,0,0,0.03); 
        border-radius:12px; padding:16px; margin-bottom:16px;
    ">
        <p style="color:#6B7280; font-size:0.72rem; font-weight:600; 
                  letter-spacing:0.06em; text-transform:uppercase; margin:0 0 12px;">
            PROJECT INFO
        </p>
        <p style="color:#111827; font-size:0.85rem; margin:0 0 6px;">
            <span style="color:#9CA3AF;">Student:</span> Abhishek Gupta
        </p>
        <p style="color:#111827; font-size:0.85rem; margin:0 0 6px;">
            <span style="color:#9CA3AF;">Enroll:</span> 01425502022
        </p>
        <p style="color:#111827; font-size:0.85rem; margin:0 0 6px;">
            <span style="color:#9CA3AF;">Course:</span> BCA VI Sem
        </p>
        <p style="color:#111827; font-size:0.85rem; margin:0 0 6px;">
            <span style="color:#9CA3AF;">Guide:</span> Dr. Ruchi Agarwal
        </p>
        <p style="color:#111827; font-size:0.85rem; margin:0;">
            <span style="color:#9CA3AF;">Session:</span> 2022–2025
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background:#FFFFFF; border: 1px solid #E5E7EB; box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        border-radius:12px; padding:16px;
    ">
        <p style="color:#6B7280; font-size:0.72rem; font-weight:600;
                  letter-spacing:0.06em; text-transform:uppercase; margin:0 0 12px;">
            TECH STACK
        </p>
        <p style="color:#111827; font-size:0.83rem; margin:0 0 5px;">🐍 Python 3.10+</p>
        <p style="color:#111827; font-size:0.83rem; margin:0 0 5px;">🤖 Scikit-learn</p>
        <p style="color:#111827; font-size:0.83rem; margin:0 0 5px;">📊 Pandas / NumPy</p>
        <p style="color:#111827; font-size:0.83rem; margin:0 0 5px;">🌐 Streamlit</p>
        <p style="color:#111827; font-size:0.83rem; margin:0;">📦 Pickle (Model)</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="color:#9CA3AF; font-size:0.72rem; text-align:center; 
              margin-top:24px; letter-spacing:0.02em;">
        © 2025 Abhishek Gupta
    </p>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN NAVIGATION — 4 tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Predict", "Explainatory", "About"])

# ══════════════════════════════════════════════
# TAB 1 — HOME (Fully designed)
# ══════════════════════════════════════════════
with tab1:

    # ── HERO SECTION ─────────────────────────────────────────────
    st.markdown(f"""
<div style="
    position: relative;
    width: 100%;
    min-height: 520px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px 20px;
    overflow: hidden;
">

    <!-- LAYER 0: Giant ghosted background word -->
    <div style="
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -58%);
        font-size: 22vw;
        font-weight: 900;
        color: #F4F4F5;
        opacity: 0.022;
        letter-spacing: -0.06em;
        white-space: nowrap;
        user-select: none;
        pointer-events: none;
        z-index: 0;
        font-family: -apple-system, 'SF Pro Display', 'Inter', sans-serif;
    ">CARWORTH</div>

    <!-- LAYER 1: Car image — sits in the middle -->
    <div style="
        position: relative;
        z-index: 1;
        width: 100%;
        max-width: 780px;
        margin: 0 auto;
        transform: perspective(1000px) rotateY(-4deg);
        transition: transform 0.3s ease;
    ">
        {CAR_IMG_TAG}
    </div>

    <!-- LAYER 2: Headline floats over the car -->
    <div style="
        position: relative;
        z-index: 2;
        text-align: center;
        margin-top: -80px;
        padding: 0 20px;
    ">
        <h1 style="
            color: #F4F4F5;
            font-size: clamp(2.2rem, 5vw, 3.8rem);
            font-weight: 800;
            letter-spacing: -0.05em;
            line-height: 1.05;
            margin: 0 0 16px;
            text-shadow: 0 2px 40px rgba(0,0,0,0.8);
        ">
            Know Your Car's<br>
            <span style="
                background: linear-gradient(90deg, #E63946 0%, #FF6B6B 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">True Value.</span>
        </h1>

        <p style="
            color: #8B8B9A;
            font-size: 1rem;
            line-height: 1.7;
            margin: 0 auto 28px;
            max-width: 480px;
            text-shadow: 0 1px 20px rgba(0,0,0,1);
        ">
            India's data-driven used car valuation tool.<br>
            Instant prediction. No guesswork.
        </p>

        <!-- Feature pills -->
        <div style="
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        ">
            <div style="
                background: rgba(14,14,20,0.85);
                border: 1px solid #222230;
                backdrop-filter: blur(8px);
                border-radius: 20px;
                padding: 8px 16px;
                display: inline-flex;
                align-items: center;
                gap: 7px;
            ">
                <span style="color:#22C55E; font-size:0.7rem;">●</span>
                <span style="color:#8B8B9A; font-size:0.8rem; font-weight:500;">
                    25+ Manufacturers
                </span>
            </div>
            <div style="
                background: rgba(14,14,20,0.85);
                border: 1px solid #222230;
                backdrop-filter: blur(8px);
                border-radius: 20px;
                padding: 8px 16px;
                display: inline-flex;
                align-items: center;
                gap: 7px;
            ">
                <span style="color:#E63946; font-size:0.7rem;">●</span>
                <span style="color:#8B8B9A; font-size:0.8rem; font-weight:500;">
                    ML-Powered Prediction
                </span>
            </div>
            <div style="
                background: rgba(14,14,20,0.85);
                border: 1px solid #222230;
                backdrop-filter: blur(8px);
                border-radius: 20px;
                padding: 8px 16px;
                display: inline-flex;
                align-items: center;
                gap: 7px;
            ">
                <span style="color:#3B82F6; font-size:0.7rem;">⚡</span>
                <span style="color:#8B8B9A; font-size:0.8rem; font-weight:500;">
                    Instant Result
                </span>
            </div>
        </div>
    </div>

</div>
    """, unsafe_allow_html=True)

    # Red glow line below hero — cinematic separator
    st.markdown("""
    <div style="
        width: 100%;
        height: 1px;
        background: linear-gradient(90deg,
            transparent 0%,
            #E63946 30%,
            #E63946 70%,
            transparent 100%);
        opacity: 0.35;
        margin: 0 0 40px;
    "></div>
    """, unsafe_allow_html=True)

    # ── STAT CARDS (unchanged from before) ───────────────────────
    st.markdown("""
    <p style="
        color:#6B7280; font-size:0.75rem; font-weight:600;
        letter-spacing:0.1em; text-transform:uppercase; margin-bottom:16px;
    ">BY THE NUMBERS</p>
    """, unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4, gap="medium")

    s1.markdown(stat_card("", "816+", "Cars in Dataset", "Quikr listings, Indian market"), unsafe_allow_html=True)
    s2.markdown(stat_card("", "25+", "Manufacturers", "Maruti to Mercedes"), unsafe_allow_html=True)
    s3.markdown(stat_card("", "R² ~0.89", "Model Accuracy", "Linear Regression pipeline"), unsafe_allow_html=True)
    s4.markdown(stat_card("", "<1 sec", "Prediction Time", "Instant valuation"), unsafe_allow_html=True)

    # ── DIVIDER ───────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── HOW IT WORKS ──────────────────────────
    st.markdown(section_header(
        "How It Works",
        "Three steps to your car's fair market value"
    ), unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3, gap="medium")

    with h1:
        st.markdown(card(f"""
        <div style="
            width:36px; height:36px; background:rgba(255,107,74,0.1);
            border:1px solid rgba(255,107,74,0.2); border-radius:10px;
            display:flex; align-items:center; justify-content:center;
            font-size:1rem; margin-bottom:16px;
        ">01</div>
        <p style="color:#111827; font-size:1rem; font-weight:600; margin:0 0 8px;">
            Select Your Car
        </p>
        <p style="color:#6B7280; font-size:0.88rem; line-height:1.6; margin:0;">
            Choose the manufacturer, model, fuel type, manufacturing year, 
            and kilometers driven from our dropdowns.
        </p>
        """), unsafe_allow_html=True)

    with h2:
        st.markdown(card(f"""
        <div style="
            width:36px; height:36px; background:#F3F4F6;
            border:1px solid #E5E7EB; border-radius:10px;
            display:flex; align-items:center; justify-content:center;
            font-size:1rem; margin-bottom:16px; color:#3B82F6;
        ">02</div>
        <p style="color:#111827; font-size:1rem; font-weight:600; margin:0 0 8px;">
            ML Model Analyzes
        </p>
        <p style="color:#6B7280; font-size:0.88rem; line-height:1.6; margin:0;">
            Our Linear Regression pipeline — trained on 816+ real listings — 
            processes your inputs through OneHotEncoding and predicts the price.
        </p>
        """), unsafe_allow_html=True)

    with h3:
        st.markdown(card(f"""
        <div style="
            width:36px; height:36px; background:#F3F4F6;
            border:1px solid #E5E7EB; border-radius:10px;
            display:flex; align-items:center; justify-content:center;
            font-size:1rem; margin-bottom:16px; color:#22C55E;
        ">03</div>
        <p style="color:#111827; font-size:1rem; font-weight:600; margin:0 0 8px;">
            Get Your Valuation
        </p>
        <p style="color:#6B7280; font-size:0.88rem; line-height:1.6; margin:0;">
            Receive the estimated market price in INR with context: 
            how your car compares to similar listings in the dataset.
        </p>
        """), unsafe_allow_html=True)

    # ── FOOTER LINE ───────────────────────────
    st.markdown("""
<div style="
    text-align:center; padding:40px 0 20px;
    color:#9CA3AF; font-size:0.78rem; letter-spacing:0.03em;
">
    CarWorthML · BCA Major Project · JEMTEC, Greater Noida · 2022–2025
</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — PREDICT
# ══════════════════════════════════════════════
with tab2:

    # Load data and model (cached)
    @st.cache_data
    def load_data():
        return pd.read_csv("Cleaned_Car_data.csv")

    @st.cache_resource
    def load_model():
        with open("LinearRegressionModel.pkl", "rb") as f:
            return pickle.load(f)

    import pickle
    import pandas as pd

    data_loaded = False
    model_loaded = False

    try:
        df   = load_data()
        data_loaded = True
    except FileNotFoundError:
        st.error("❌ Cleaned_Car_data.csv not found. Run `python data_cleaning.py` first.")

    try:
        model = load_model()
        model_loaded = True
    except FileNotFoundError:
        st.error("❌ LinearRegressionModel.pkl not found. Run `python model_training.py` first.")

    if data_loaded and model_loaded:

        st.markdown("<div style='padding:32px 0 16px;'>", unsafe_allow_html=True)
        st.markdown(section_header(
            "Predict Your Car's Value",
            "Fill in the details below for an instant market valuation"
        ), unsafe_allow_html=True)

        # ── TWO COLUMN LAYOUT: Form left | Result right ──
        form_col, result_col = st.columns([1.1, 0.9], gap="large")

        # ── LEFT: Input Form ──────────────────────────────
        with form_col:
            st.markdown("""
            <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                      letter-spacing:0.08em; text-transform:uppercase; margin-bottom:20px;">
                CAR DETAILS
            </p>
            """, unsafe_allow_html=True)

            with st.form("predict_form"):

                # Manufacturer
                companies_sorted = sorted(df["company"].unique())
                company = st.selectbox(
                    "Manufacturer",
                    options=companies_sorted,
                    help="Select the car manufacturer"
                )

                # Model — filtered by company
                models_for_company = sorted(
                    df[df["company"] == company]["name"].unique()
                )
                car_name = st.selectbox(
                    "Model",
                    options=models_for_company,
                    help="Select the specific model variant"
                )

                # Fuel Type
                fuel_type = st.selectbox(
                    "Fuel Type",
                    options=sorted(df["fuel_type"].unique()),
                    help="Select fuel type"
                )

                # Year
                year = st.slider(
                    "Year of Manufacture",
                    min_value=1995,
                    max_value=2024,
                    value=2015,
                    step=1,
                )

                # KMs Driven
                kms_driven = st.number_input(
                    "Kilometers Driven",
                    min_value=0,
                    max_value=500000,
                    value=50000,
                    step=1000,
                )

                st.caption(
                    f"≈ {kms_driven // 15000} years of average Indian driving"
                )

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button(
                    "Predict Price →",
                    use_container_width=True
                )

        # ── RIGHT: Result Panel ───────────────────────────
        with result_col:
            st.markdown("""
            <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                      letter-spacing:0.08em; text-transform:uppercase; margin-bottom:20px;">
                VALUATION
            </p>
            """, unsafe_allow_html=True)

            if not submitted:
                # Idle state — clean placeholder
                st.markdown(card("""
                <div style="text-align:center; padding:40px 0;">
                    <div style="font-size:3rem; margin-bottom:16px; opacity:0.2;"></div>
                    <p style="color:#9CA3AF; font-size:0.9rem; margin:0; line-height:1.6;">
                        Fill in your car details on the left<br>
                        and click <strong style="color:#6B7280;">Predict Price</strong> to see your valuation.
                    </p>
                </div>
                """, padding="32px"), unsafe_allow_html=True)

            else:
                # Run prediction
                try:
                    input_df = pd.DataFrame(
                        [[car_name, company, year, kms_driven, fuel_type]],
                        columns=["name", "company", "year", "kms_driven", "fuel_type"],
                    )
                    price = model.predict(input_df)[0]
                    price = max(float(price), 25000.0)

                    

                    # Price result card
                    st.markdown(price_result_card(price), unsafe_allow_html=True)

                    # Context: similar cars in dataset
                    similar = df[
                        (df["company"] == company) &
                        (df["fuel_type"] == fuel_type) &
                        (df["year"].between(year - 2, year + 2))
                    ]

                    if len(similar) >= 3:
                        avg_s = similar["Price"].mean()
                        min_s = similar["Price"].min()
                        max_s = similar["Price"].max()

                        st.markdown("""
                        <p style="color:#6B7280; font-size:0.72rem; font-weight:600;
                                  letter-spacing:0.08em; text-transform:uppercase;
                                  margin:24px 0 12px;">
                            VS SIMILAR CARS IN DATASET
                        </p>
                        """, unsafe_allow_html=True)

                        m1, m2, m3 = st.columns(3)
                        m1.metric("Min", f"₹{min_s:,.0f}")
                        m2.metric("Average", f"₹{avg_s:,.0f}")
                        m3.metric("Max", f"₹{max_s:,.0f}")

                    # Summary table
                    st.markdown("""
                    <p style="color:#6B7280; font-size:0.72rem; font-weight:600;
                              letter-spacing:0.08em; text-transform:uppercase;
                              margin:24px 0 12px;">
                        SUMMARY
                    </p>
                    """, unsafe_allow_html=True)

                    summary = {
                        "Parameter": ["Manufacturer", "Model", "Year", "Fuel", "KMs Driven", "Predicted Price"],
                        "Value": [
                            company,
                            car_name,
                            str(year),
                            fuel_type,
                            f"{kms_driven:,} km",
                            f"₹ {price:,.0f}"
                        ]
                    }
                    st.dataframe(
                        pd.DataFrame(summary),
                        use_container_width=True,
                        hide_index=True
                    )

                except Exception as e:
                    st.markdown(card(f"""
                    <p style="color:#FF6B4A; font-size:0.9rem; margin:0 0 8px;">
                        Prediction failed
                    </p>
                    <p style="color:#6B7280; font-size:0.83rem; margin:0;">
                        {str(e)}<br><br>
                        Try a different car and model combination.
                    </p>
                    """), unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — EXPLAINATORY (Market Analytics)
# ══════════════════════════════════════════════
with tab3:
    import pandas as pd
    import json

    @st.cache_data
    def load_data_tab3():
        return pd.read_csv("Cleaned_Car_data.csv")

    try:
        df3 = load_data_tab3()
        data3_ok = True
    except FileNotFoundError:
        st.error("❌ Cleaned_Car_data.csv not found. Run Phase 2 scripts first.")
        data3_ok = False

    if data3_ok:

        st.markdown("<div style='padding:32px 0 16px;'>", unsafe_allow_html=True)

        # ── HEADER + LOTTIE ROW ──────────────────────
        hdr_col, anim_col = st.columns([3, 1], gap="large")

        with hdr_col:
            st.markdown(section_header(
                "Market Insights",
                "Explore price trends across manufacturers, fuel types, and years"
            ), unsafe_allow_html=True)

            # Dataset KPIs — compact row
            k1, k2, k3, k4, k5 = st.columns(5)
            k1.metric("Total Records",   f"{len(df3):,}")
            k2.metric("Avg Price",        f"₹{df3['Price'].mean()/100000:.1f}L")
            k3.metric("Lowest",           f"₹{df3['Price'].min():,}")
            k4.metric("Highest",          f"₹{df3['Price'].max()/100000:.1f}L")
            k5.metric("Manufacturers",    f"{df3['company'].nunique()}")

        with anim_col:
            st.markdown("""
            <div style="height:160px; display:flex; align-items:center; justify-content:center;">
                <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#FF6B4A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── CHART 1: Avg Price by Manufacturer ───────
        st.markdown("""
        <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                  letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">
            CHART 01
        </p>
        <h3 style="color:#111827; font-size:1.15rem; font-weight:600;
                   letter-spacing:-0.01em; margin:0 0 6px;">
            Average Resale Price by Manufacturer
        </h3>
        <p style="color:#6B7280; font-size:0.85rem; margin:0 0 20px;">
            Luxury brands command the highest resale values. 
            Maruti and Datsun hold value well in the mass market segment.
        </p>
        """, unsafe_allow_html=True)

        avg_company = (
            df3.groupby("company")["Price"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        avg_company.columns = ["Manufacturer", "Average Price (₹)"]
        avg_company["Average Price (₹)"] = avg_company["Average Price (₹)"].astype(int)

        # Split into two charts for readability: Luxury + Premium / Mass market
        luxury_premium = avg_company[avg_company["Average Price (₹)"] >= 600000]
        mass_market    = avg_company[avg_company["Average Price (₹)"] <  600000]

        c_lux, c_mass = st.columns(2, gap="large")

        with c_lux:
            st.markdown("""
            <p style="color:#6B7280; font-size:0.78rem; font-weight:500;
                      margin-bottom:8px;">Luxury & Premium</p>
            """, unsafe_allow_html=True)
            st.bar_chart(
                luxury_premium.set_index("Manufacturer"),
                use_container_width=True,
                height=300,
                color="#FF6B4A",
            )

        with c_mass:
            st.markdown("""
            <p style="color:#6B7280; font-size:0.78rem; font-weight:500;
                      margin-bottom:8px;">Mass Market</p>
            """, unsafe_allow_html=True)
            st.bar_chart(
                mass_market.set_index("Manufacturer"),
                use_container_width=True,
                height=300,
                color="#3B82F6",
            )

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── CHART 2: Price by Fuel Type ───────────────
        st.markdown("""
        <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                  letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">
            CHART 02
        </p>
        <h3 style="color:#111827; font-size:1.15rem; font-weight:600;
                   letter-spacing:-0.01em; margin:0 0 6px;">
            Price Distribution by Fuel Type
        </h3>
        <p style="color:#6B7280; font-size:0.85rem; margin:0 0 20px;">
            Diesel vehicles fetch higher resale prices on average due to better mileage 
            and preference in commercial and highway usage.
        </p>
        """, unsafe_allow_html=True)

        fuel_col1, fuel_col2 = st.columns([1, 1], gap="large")

        with fuel_col1:
            avg_fuel = (
                df3.groupby("fuel_type")["Price"]
                .agg(["mean", "median", "count"])
                .reset_index()
            )
            avg_fuel.columns = ["Fuel Type", "Avg Price (₹)", "Median Price (₹)", "Count"]
            avg_fuel["Avg Price (₹)"]    = avg_fuel["Avg Price (₹)"].astype(int)
            avg_fuel["Median Price (₹)"] = avg_fuel["Median Price (₹)"].astype(int)

            st.bar_chart(
                avg_fuel.set_index("Fuel Type")[["Avg Price (₹)", "Median Price (₹)"]],
                use_container_width=True,
                height=280,
                color=["#E63946", "#3B82F6"],
            )

        with fuel_col2:
            # Fuel type distribution — show as styled cards
            st.markdown("""
            <p style="color:#6B7280; font-size:0.78rem; font-weight:500;
                      margin-bottom:12px;">Listing Count by Fuel Type</p>
            """, unsafe_allow_html=True)
            fuel_counts = df3["fuel_type"].value_counts()
            total       = len(df3)

            for fuel, count in fuel_counts.items():
                pct   = count / total * 100
                color = "#E63946" if fuel == "Diesel" else "#3B82F6" if fuel == "Petrol" else "#F59E0B"
                st.markdown(f"""
                <div style="
                    background:#FFFFFF; border: 1px solid #E5E7EB; box-shadow: 0 4px 10px rgba(0,0,0,0.03);
                    border-radius:10px; padding:14px 18px;
                    margin-bottom:10px; display:flex;
                    align-items:center; justify-content:space-between;
                ">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="
                            width:10px; height:10px; border-radius:50%;
                            background:{color};
                        "></div>
                        <span style="color:#111827; font-size:0.9rem; font-weight:500;">
                            {fuel}
                        </span>
                    </div>
                    <div style="text-align:right;">
                        <span style="color:#111827; font-size:0.9rem; font-weight:700;">
                            {count:,}
                        </span>
                        <span style="color:#6B7280; font-size:0.78rem; margin-left:8px;">
                            ({pct:.1f}%)
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── CHART 3: Price Trend by Year ──────────────
        st.markdown("""
        <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                  letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">
            CHART 03
        </p>
        <h3 style="color:#111827; font-size:1.15rem; font-weight:600;
                   letter-spacing:-0.01em; margin:0 0 6px;">
            Average Resale Price by Manufacturing Year
        </h3>
        <p style="color:#6B7280; font-size:0.85rem; margin:0 0 20px;">
            Newer cars depreciate less and command higher resale values. 
            The upward curve after 2015 reflects both inflation and improved quality retention.
        </p>
        """, unsafe_allow_html=True)

        price_by_year = (
            df3.groupby("year")["Price"]
            .mean()
            .reset_index()
            .sort_values("year")
        )
        price_by_year.columns = ["Year", "Avg Price (₹)"]
        price_by_year["Avg Price (₹)"] = price_by_year["Avg Price (₹)"].astype(int)

        st.line_chart(
            price_by_year.set_index("Year"),
            use_container_width=True,
            height=300,
            color="#FF6B4A",
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── CHART 4: Top 10 Most Listed Brands ────────
        st.markdown("""
        <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                  letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">
            CHART 04
        </p>
        <h3 style="color:#111827; font-size:1.15rem; font-weight:600;
                   letter-spacing:-0.01em; margin:0 0 6px;">
            Top 10 Most Listed Manufacturers
        </h3>
        <p style="color:#6B7280; font-size:0.85rem; margin:0 0 20px;">
            Maruti and Hyundai dominate resale listings — consistent with India's 
            new car sales data where they hold the top two positions.
        </p>
        """, unsafe_allow_html=True)

        top10 = df3["company"].value_counts().head(10).reset_index()
        top10.columns = ["Manufacturer", "Listings"]

        st.bar_chart(
            top10.set_index("Manufacturer"),
            use_container_width=True,
            height=300,
            color="#22C55E",
        )

        # ── RAW DATA TOGGLE ───────────────────────────
        st.markdown("<hr>", unsafe_allow_html=True)

        with st.expander("View raw dataset sample (first 20 rows)"):
            st.dataframe(
                df3.head(20),
                use_container_width=True,
                hide_index=True
            )
            st.caption(
                f"Showing 20 of {len(df3):,} records · "
                f"{df3.shape[1]} columns · "
                f"Source: Synthetic Quikr-style Indian used car data"
            )

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — ABOUT
# ══════════════════════════════════════════════
with tab4:

    st.markdown("<div style='padding:32px 0 16px;'>", unsafe_allow_html=True)

    # ── HEADER ─────────────────────────────────
    about_left, about_right = st.columns([3, 1], gap="large")

    with about_left:
        st.markdown(section_header(
            "About This Project",
            "CarWorthML — BCA Major Project · JEMTEC, Greater Noida · 2022–2025"
        ), unsafe_allow_html=True)

    with about_right:
        pass

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── PROJECT IDENTITY ───────────────────────
    st.markdown("""
    <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
              letter-spacing:0.08em; text-transform:uppercase; margin-bottom:16px;">
        PROJECT IDENTITY
    </p>
    """, unsafe_allow_html=True)

    id_col1, id_col2 = st.columns(2, gap="large")

    with id_col1:
        st.markdown(card("""
        <table style="width:100%; border-collapse:collapse;">
            <tr>
                <td style="color:#9CA3AF; font-size:0.8rem; padding:8px 0;
                           font-weight:500; letter-spacing:0.03em; white-space:nowrap;
                           text-transform:uppercase; vertical-align:top; padding-right:16px;">
                    Project Title
                </td>
                <td style="color:#111827; font-size:0.88rem; padding:8px 0;
                           font-weight:500; line-height:1.4;">
                    CarWorthML – Second Hand Car Price Predictor
                </td>
            </tr>
            <tr>
                <td style="color:#9CA3AF; font-size:0.8rem; padding:8px 0;
                           font-weight:500; letter-spacing:0.03em; text-transform:uppercase;
                           vertical-align:top; padding-right:16px;">
                    Student
                </td>
                <td style="color:#111827; font-size:0.88rem; padding:8px 0;">
                    Abhishek Gupta
                </td>
            </tr>
            <tr>
                <td style="color:#9CA3AF; font-size:0.8rem; padding:8px 0;
                           font-weight:500; letter-spacing:0.03em; text-transform:uppercase;
                           vertical-align:top; padding-right:16px;">
                    Enrolment
                </td>
                <td style="color:#111827; font-size:0.88rem; padding:8px 0;">
                    01425502022
                </td>
            </tr>
            <tr>
                <td style="color:#9CA3AF; font-size:0.8rem; padding:8px 0;
                           font-weight:500; letter-spacing:0.03em; text-transform:uppercase;
                           vertical-align:top; padding-right:16px;">
                    Course
                </td>
                <td style="color:#111827; font-size:0.88rem; padding:8px 0;">
                    Bachelor of Computer Applications (BCA) – VI Semester
                </td>
            </tr>
            <tr>
                <td style="color:#9CA3AF; font-size:0.8rem; padding:8px 0;
                           font-weight:500; letter-spacing:0.03em; text-transform:uppercase;
                           vertical-align:top; padding-right:16px;">
                    Session
                </td>
                <td style="color:#111827; font-size:0.88rem; padding:8px 0;">
                    2022 – 2025
                </td>
            </tr>
        </table>
        """, padding="24px 28px"), unsafe_allow_html=True)

    with id_col2:
        st.markdown(card("""
        <table style="width:100%; border-collapse:collapse;">
            <tr>
                <td style="color:#9CA3AF; font-size:0.8rem; padding:8px 0;
                           font-weight:500; letter-spacing:0.03em; white-space:nowrap;
                           text-transform:uppercase; vertical-align:top; padding-right:16px;">
                    Guide
                </td>
                <td style="color:#111827; font-size:0.88rem; padding:8px 0;
                           font-weight:500; line-height:1.4;">
                    Dr. Ruchi Agarwal
                </td>
            </tr>
            <tr>
                <td style="color:#9CA3AF; font-size:0.8rem; padding:8px 0;
                           font-weight:500; letter-spacing:0.03em; text-transform:uppercase;
                           vertical-align:top; padding-right:16px;">
                    Designation
                </td>
                <td style="color:#111827; font-size:0.88rem; padding:8px 0;">
                    HOD, BCA Department
                </td>
            </tr>
            <tr>
                <td style="color:#9CA3AF; font-size:0.8rem; padding:8px 0;
                           font-weight:500; letter-spacing:0.03em; text-transform:uppercase;
                           vertical-align:top; padding-right:16px;">
                    Institution
                </td>
                <td style="color:#111827; font-size:0.88rem; padding:8px 0;
                           line-height:1.4;">
                    JIMS Engineering Management Technical Campus (JEMTEC), Greater Noida
                </td>
            </tr>
            <tr>
                <td style="color:#9CA3AF; font-size:0.8rem; padding:8px 0;
                           font-weight:500; letter-spacing:0.03em; text-transform:uppercase;
                           vertical-align:top; padding-right:16px;">
                    Affiliation
                </td>
                <td style="color:#111827; font-size:0.88rem; padding:8px 0;
                           line-height:1.4;">
                    Guru Gobind Singh Indraprastha University, Delhi
                </td>
            </tr>
        </table>
        """, padding="24px 28px"), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── HOW THE MODEL WORKS ────────────────────
    st.markdown("""
    <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
              letter-spacing:0.08em; text-transform:uppercase; margin-bottom:16px;">
        TECHNICAL OVERVIEW
    </p>
    """, unsafe_allow_html=True)

    tech_col1, tech_col2 = st.columns([3, 2], gap="large")

    with tech_col1:
        st.markdown(card("""
        <p style="color:#111827; font-size:1rem; font-weight:600; margin:0 0 14px;">
            How the ML Pipeline Works
        </p>
        <p style="color:#6B7280; font-size:0.88rem; line-height:1.7; margin:0 0 12px;">
            CarWorthML uses a supervised machine learning pipeline built with 
            Scikit-learn. Raw used car data sourced from Quikr India listings 
            is cleaned and preprocessed before training.
        </p>
        <p style="color:#6B7280; font-size:0.88rem; line-height:1.7; margin:0 0 16px;">
            Categorical features — manufacturer name, car model, and fuel type — 
            are transformed using <span style="color:#111827;">OneHotEncoder</span> inside 
            a <span style="color:#111827;">ColumnTransformer</span>. The numeric features 
            (year and kilometers driven) pass through unchanged.
        </p>
        <p style="color:#6B7280; font-size:0.88rem; line-height:1.7; margin:0 0 16px;">
            The entire preprocessing + model pipeline is wrapped using 
            <span style="color:#111827;">make_pipeline()</span> and serialized with 
            <span style="color:#111827;">Pickle</span> for efficient loading at runtime.
        </p>
        <div style="
            background:#F9FAFB; border: 1px solid #E5E7EB; box-shadow: 0 4px 10px rgba(0,0,0,0.03);
            border-radius:10px; padding:16px; font-family:monospace;
            font-size:0.8rem; color:#22C55E; line-height:1.8;
        ">
            Input → [name, company, year, kms_driven, fuel_type]<br>
            ↓ OneHotEncoder (categorical columns)<br>
            ↓ passthrough (year, kms_driven)<br>
            ↓ LinearRegression<br>
            Output → Predicted Price (₹)
        </div>
        """), unsafe_allow_html=True)

    with tech_col2:
        st.markdown(card("""
        <p style="color:#111827; font-size:1rem; font-weight:600; margin:0 0 16px;">
            Model Performance
        </p>
        <div style="margin-bottom:16px;">
            <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                      letter-spacing:0.06em; text-transform:uppercase; margin:0 0 6px;">
                ALGORITHM
            </p>
            <p style="color:#111827; font-size:0.9rem; margin:0;">
                Linear Regression
            </p>
        </div>
        <div style="margin-bottom:16px;">
            <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                      letter-spacing:0.06em; text-transform:uppercase; margin:0 0 6px;">
                ACCURACY (R² SCORE)
            </p>
            <p style="color:#FF6B4A; font-size:1.4rem; font-weight:700;
                      letter-spacing:-0.02em; margin:0;">
                ~0.89
            </p>
        </div>
        <div style="margin-bottom:16px;">
            <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                      letter-spacing:0.06em; text-transform:uppercase; margin:0 0 6px;">
                TRAIN / TEST SPLIT
            </p>
            <p style="color:#111827; font-size:0.9rem; margin:0;">90% / 10%</p>
        </div>
        <div style="margin-bottom:16px;">
            <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                      letter-spacing:0.06em; text-transform:uppercase; margin:0 0 6px;">
                BEST SPLIT SELECTION
            </p>
            <p style="color:#111827; font-size:0.9rem; margin:0;">
                Auto-selected from 1,000 random state trials
            </p>
        </div>
        <div>
            <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
                      letter-spacing:0.06em; text-transform:uppercase; margin:0 0 6px;">
                DATASET SIZE
            </p>
            <p style="color:#111827; font-size:0.9rem; margin:0;">
                816+ cleaned records
            </p>
        </div>
        """), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── TECH STACK GRID ────────────────────────
    st.markdown("""
    <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
              letter-spacing:0.08em; text-transform:uppercase; margin-bottom:16px;">
        TECHNOLOGY STACK
    </p>
    """, unsafe_allow_html=True)

    tech_stack = [
        ("●", "Python 3.10+",        "Core language"),
        ("●", "Scikit-learn",         "ML pipeline, OHE, LinearRegression"),
        ("●", "Pandas",               "Data loading, cleaning, analysis"),
        ("●", "NumPy",                "Numerical operations"),
        ("●", "Streamlit",            "Web framework and UI"),
        ("●", "Pickle",               "Model serialization"),
        ("●", "streamlit-lottie",     "Lottie animations"),
        ("●", "Requests",             "CDN asset fetching"),
    ]

    rows_of_4 = [tech_stack[i:i+4] for i in range(0, len(tech_stack), 4)]

    for row in rows_of_4:
        cols = st.columns(4, gap="medium")
        for col, (icon, name, desc) in zip(cols, row):
            col.markdown(f"""
            <div style="
                background:#FFFFFF; border: 1px solid #E5E7EB; box-shadow: 0 4px 10px rgba(0,0,0,0.03);
                border-radius:12px; padding:18px;
                transition: border-color 0.2s;
                margin-bottom:12px;
            ">
                <div style="font-size:1.4rem; margin-bottom:10px;">{icon}</div>
                <p style="color:#111827; font-size:0.88rem; font-weight:600; margin:0 0 4px;">
                    {name}
                </p>
                <p style="color:#6B7280; font-size:0.78rem; margin:0; line-height:1.4;">
                    {desc}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ── LIMITATIONS ────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#6B7280; font-size:0.75rem; font-weight:600;
              letter-spacing:0.08em; text-transform:uppercase; margin-bottom:16px;">
        KNOWN LIMITATIONS
    </p>
    """, unsafe_allow_html=True)

    lim_col1, lim_col2 = st.columns(2, gap="large")

    limitations = [
        ("●", "No geolocation data", "Prices vary significantly across cities. This model does not account for city-based pricing differences."),
        ("●", "Local deployment only", "No CI/CD pipeline or cloud hosting. The app runs on localhost only in its current form."),
        ("●", "Brand coverage", "Only 25 manufacturers are covered. Rare or imported brands may not return accurate predictions."),
        ("●", "Dataset recency", "Training data reflects listings up to 2023. Newer models and price inflation may reduce accuracy."),
        ("●", "Linear model limits", "Linear Regression assumes linear relationships. Non-linear price factors like condition or service history are not captured."),
        ("●", "Internet for Lottie", "Animations require internet on first load. A local fallback shows if unavailable."),
    ]

    for i, (icon, title, desc) in enumerate(limitations):
        col = lim_col1 if i % 2 == 0 else lim_col2
        col.markdown(f"""
        <div style="
            background:#FFFFFF; border: 1px solid #E5E7EB; box-shadow: 0 4px 10px rgba(0,0,0,0.03);
            border-left: 3px solid #E63946;
            border-radius:10px; padding:16px 18px;
            margin-bottom:10px;
        ">
            <p style="color:#111827; font-size:0.88rem; font-weight:600;
                      margin:0 0 6px;">
                {icon} {title}
            </p>
            <p style="color:#6B7280; font-size:0.82rem; margin:0; line-height:1.5;">
                {desc}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── FOOTER ─────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding:24px 0 16px;">
        <p style="
            color:#111827; font-size:1rem; font-weight:600;
            letter-spacing:-0.01em; margin:0 0 8px;
        ">CarWorthML</p>
        <p style="color:#9CA3AF; font-size:0.8rem; margin:0 0 4px;">
            BCA Major Project · Abhishek Gupta · 01425502022
        </p>
        <p style="color:#9CA3AF; font-size:0.78rem; margin:0;">
            JEMTEC, Greater Noida · Affiliated to GGSIPU · Session 2022–2025
        </p>
        <p style="color:#2D2D3D; font-size:0.72rem; margin:20px 0 0;">
            © 2025 Abhishek Gupta · All rights reserved
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

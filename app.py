import streamlit as st
from datetime import datetime

st.set_page_config(page_title="finem", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

PRIMARY = "#7B61FF"
SECONDARY = "#4DFFD2"
TEXT_SECONDARY = "#8A8A8A"
SURFACE = "#141414"
BORDER = "#222222"
BACKGROUND = "#0A0A0A"

st.markdown(f"""
<style>
    .stApp {{ background-color: {BACKGROUND}; color: white; }}
    [data-testid="stSidebar"] {{ background-color: #0D0D0D; border-right: 1px solid {BORDER}; }}
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    div[data-testid="stButton"] button {{
        background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
        color: {BACKGROUND};
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        padding: 8px;
    }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <h1 style="background:linear-gradient(135deg,{PRIMARY},{SECONDARY});-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:32px;font-weight:700;">finem</h1>
    <p style="color:{TEXT_SECONDARY};font-size:12px;">finance dashboard</p>
    <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:8px;padding:8px 12px;margin:16px 0;color:{TEXT_SECONDARY};font-size:13px;">
        📅 {datetime.now().strftime("%B %Y")}
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<h1 style="background:linear-gradient(135deg,{PRIMARY},{SECONDARY});-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:48px;font-weight:700;">finem</h1>
<p style="color:{TEXT_SECONDARY};font-size:18px;margin-bottom:32px;">Your e-commerce finance dashboard</p>
""", unsafe_allow_html=True)

tools = [
    ("🧮", "Unit Economy", "Calculate margins, CAC, ROAS and breakeven per order", "2_unit_economy"),
    ("📈", "Daily ROAS", "Track ad performance day by day with trend analysis", None),
    ("💸", "Expenses", "Manage bills, pending payments and monthly balance", None),
    ("📋", "P&L Builder", "Build monthly profit & loss with waterfall chart", None),
    ("💰", "Cash Flow", "90-day forecast with cash gap detection", None),
    ("🔄", "LTV & Retention", "Lifetime value, LTV:CAC ratio and payback period", None),
    ("⏱️", "Pacing", "Monitor ad spend pace vs monthly budget plan", None),
    ("🎯", "KPI Dashboard", "All 8 key metrics with health indicators", None),
    ("📊", "Overview", "One-screen snapshot of your business today", None),
]

col1, col2, col3 = st.columns(3)
for i, (icon, name, desc, page) in enumerate(tools):
    with [col1, col2, col3][i % 3]:
        st.markdown(f"""
        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:20px;margin-bottom:8px;">
            <p style="font-size:28px;margin:0 0 8px 0;">{icon}</p>
            <p style="font-weight:600;color:white;margin:0 0 4px 0;">{name}</p>
            <p style="color:{TEXT_SECONDARY};font-size:13px;margin:0 0 12px 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        if page:
            if st.button(f"Open {name}", key=f"btn_{i}"):
                st.switch_page(f"pages/{page}.py")
        else:
            st.markdown(f'<p style="color:{TEXT_SECONDARY};font-size:12px;text-align:center;margin-bottom:16px;">Coming soon</p>', unsafe_allow_html=True)

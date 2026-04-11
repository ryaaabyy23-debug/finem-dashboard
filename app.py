import streamlit as st
from datetime import datetime
from utils.styles import load_css, PRIMARY, SECONDARY, TEXT_SECONDARY, SURFACE, BORDER

st.set_page_config(page_title="finem", page_icon="✦", layout="wide", initial_sidebar_state="expanded")
load_css()

with st.sidebar:
    st.markdown(f"""
    <h1 style="background:linear-gradient(135deg,{PRIMARY},{SECONDARY});-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:32px;font-weight:700;margin-bottom:4px;">finem</h1>
    <p style="color:{TEXT_SECONDARY};font-size:12px;margin-top:0;">finance dashboard</p>
    <div style="background-color:{SURFACE};border:1px solid {BORDER};border-radius:8px;padding:8px 12px;margin:16px 0;font-size:13px;color:{TEXT_SECONDARY};">
        📅 {datetime.now().strftime("%B %Y")}
    </div>
    """, unsafe_allow_html=True)

    pages = [("📊","Overview"),("🧮","Unit Economy"),("📈","Daily ROAS"),("💸","Expenses"),
             ("📋","P&L Builder"),("💰","Cash Flow"),("🔄","LTV & Retention"),("⏱️","Pacing"),("🎯","KPI Dashboard")]
    for icon, name in pages:
        st.markdown(f'<div style="padding:8px 12px;border-radius:8px;margin-bottom:4px;color:{TEXT_SECONDARY};font-size:14px;">{icon} {name}</div>', unsafe_allow_html=True)

st.markdown(f"""
<h1 style="background:linear-gradient(135deg,{PRIMARY},{SECONDARY});-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:48px;font-weight:700;margin-bottom:8px;">finem</h1>
<p style="color:{TEXT_SECONDARY};font-size:18px;margin-bottom:48px;">Your e-commerce finance dashboard</p>
""", unsafe_allow_html=True)

tools = [
    ("🧮","Unit Economy","Calculate margins, CAC, ROAS and breakeven per order"),
    ("📈","Daily ROAS","Track ad performance day by day with trend analysis"),
    ("💸","Expenses","Manage bills, pending payments and monthly balance"),
    ("📋","P&L Builder","Build monthly profit & loss with waterfall chart"),
    ("💰","Cash Flow","90-day forecast with cash gap detection"),
    ("🔄","LTV & Retention","Lifetime value, LTV:CAC ratio and payback period"),
    ("⏱️","Pacing","Monitor ad spend pace vs monthly budget plan"),
    ("🎯","KPI Dashboard","All 8 key metrics with health indicators"),
    ("📊","Overview","One-screen snapshot of your business today"),
]

col1, col2, col3 = st.columns(3)
for i, (icon, name, desc) in enumerate(tools):
    with [col1, col2, col3][i % 3]:
        st.markdown(f"""
        <div style="background-color:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:20px;margin-bottom:16px;">
            <p style="font-size:28px;margin:0 0 8px 0;">{icon}</p>
            <p style="font-weight:600;color:white;margin:0 0 4px 0;">{name}</p>
            <p style="color:{TEXT_SECONDARY};font-size:13px;margin:0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

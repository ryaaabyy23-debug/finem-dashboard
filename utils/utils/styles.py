import streamlit as st

BACKGROUND     = "#0A0A0A"
SURFACE        = "#141414"
BORDER         = "#222222"
PRIMARY        = "#7B61FF"
SECONDARY      = "#4DFFD2"
TEXT_PRIMARY   = "#FFFFFF"
TEXT_SECONDARY = "#8A8A8A"
SUCCESS        = "#4DFFD2"
WARNING        = "#F5A623"
DANGER         = "#FF4D4D"

def load_css() -> None:
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {BACKGROUND}; color: {TEXT_PRIMARY}; }}
        [data-testid="stSidebar"] {{ background-color: #0D0D0D; border-right: 1px solid {BORDER}; }}
        .stNumberInput input, .stTextInput input {{ background-color: {SURFACE} !important; color: {TEXT_PRIMARY} !important; border: 1px solid {BORDER} !important; border-radius: 8px !important; }}
        .stButton > button {{ background: linear-gradient(135deg, {PRIMARY}, {SECONDARY}); color: {BACKGROUND}; border: none; border-radius: 8px; font-weight: 600; padding: 8px 24px; }}
        .stButton > button:hover {{ opacity: 0.9; }}
        [data-testid="stMetric"] {{ background-color: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 16px; }}
        .stTabs [data-baseweb="tab"] {{ background-color: {SURFACE}; color: {TEXT_SECONDARY}; }}
        .stTabs [aria-selected="true"] {{ background-color: {PRIMARY} !important; color: {TEXT_PRIMARY} !important; }}
        #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
        .gradient-text {{ background: linear-gradient(135deg, {PRIMARY}, {SECONDARY}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; }}
    </style>
    """, unsafe_allow_html=True)

def plotly_layout_defaults() -> dict:
    return dict(
        paper_bgcolor=BACKGROUND, plot_bgcolor=SURFACE,
        font=dict(color=TEXT_PRIMARY, family="system-ui, sans-serif"),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER),
        margin=dict(l=20, r=20, t=40, b=20),
    )

def metric_card(label: str, value: str, color: str = PRIMARY) -> None:
    st.markdown(f"""
    <div style="background-color:{SURFACE};border:1px solid {BORDER};border-left:3px solid {color};border-radius:12px;padding:16px 20px;margin-bottom:12px;">
        <p style="color:{TEXT_SECONDARY};font-size:12px;margin:0 0 4px 0;text-transform:uppercase;letter-spacing:0.5px;">{label}</p>
        <p style="color:{color};font-size:28px;font-weight:700;margin:0;">{value}</p>
    </div>
    """, unsafe_allow_html=True)

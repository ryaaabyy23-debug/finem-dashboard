"""
finem — Unit Economy
Per-order profitability analysis with waterfall visualization.
"""

import json
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

# ── Inline color constants ─────────────────────────────────────────────────────
PRIMARY        = "#7B61FF"
SECONDARY      = "#4DFFD2"
TEXT_PRIMARY   = "#FFFFFF"
TEXT_SECONDARY = "#8A8A8A"
SURFACE        = "#141414"
BORDER         = "#222222"
BACKGROUND     = "#0A0A0A"
SUCCESS        = "#4DFFD2"
WARNING        = "#F5A623"
DANGER         = "#FF4D4D"

# ── CSS ───────────────────────────────────────────────────────────────────────
_CSS = f"""
<style>
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {BACKGROUND};
        color: {TEXT_PRIMARY};
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}
    [data-testid="stSidebar"] {{
        background-color: {SURFACE};
        border-right: 1px solid {BORDER};
    }}
    [data-testid="stSidebar"] * {{ color: {TEXT_PRIMARY} !important; }}
    [data-testid="stHeader"] {{
        background-color: {BACKGROUND};
        border-bottom: 1px solid {BORDER};
    }}
    [data-testid="stMetric"] {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 16px 20px;
    }}
    [data-testid="stMetricLabel"] {{
        color: {TEXT_SECONDARY} !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    [data-testid="stMetricValue"] {{
        color: {TEXT_PRIMARY} !important;
        font-size: 1.6rem !important;
        font-weight: 700;
    }}
    [data-testid="stMetricDelta"] svg {{ display: none; }}
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input {{
        background-color: {SURFACE} !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT_PRIMARY} !important;
        border-radius: 8px;
    }}
    .stButton > button {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        color: {TEXT_PRIMARY};
        border-radius: 8px;
        transition: border-color 0.2s, background-color 0.2s;
    }}
    .stButton > button:hover {{
        border-color: {PRIMARY};
        background-color: {PRIMARY}22;
        color: {TEXT_PRIMARY};
    }}
    [data-testid="stTabs"] [data-baseweb="tab-list"] {{
        background-color: {SURFACE};
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }}
    [data-testid="stTabs"] [data-baseweb="tab"] {{
        background-color: transparent;
        color: {TEXT_SECONDARY};
        border-radius: 8px;
        font-weight: 500;
    }}
    [data-testid="stTabs"] [aria-selected="true"] {{
        background-color: {BORDER};
        color: {TEXT_PRIMARY} !important;
    }}
    hr {{ border-color: {BORDER}; margin: 16px 0; }}
    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
        overflow: hidden;
    }}
    [data-testid="stPlotlyChart"] {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }}
    h1, h2, h3, h4, h5, h6 {{ color: {TEXT_PRIMARY} !important; }}
    [data-testid="stSidebarNavLink"] {{
        border-radius: 8px;
        margin: 2px 0;
        padding: 6px 12px;
    }}
    [data-testid="stSidebarNavLink"]:hover {{ background-color: {BORDER}; }}
    [data-testid="stSidebarNavLink"][aria-current="page"] {{
        background-color: {PRIMARY}33;
        border-left: 3px solid {PRIMARY};
    }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: {SURFACE}; }}
    ::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {TEXT_SECONDARY}; }}
    #MainMenu, footer, [data-testid="stToolbar"] {{ display: none !important; }}
    .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}
</style>
"""

# ── Data persistence ───────────────────────────────────────────────────────────
_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "unit_economy.json"


def _load() -> dict:
    if _DATA_FILE.exists():
        try:
            return json.loads(_DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save(data: dict) -> None:
    _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    _DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ── Health color helpers ───────────────────────────────────────────────────────
def _cm_color(cm_pct: float) -> str:
    if cm_pct > 30:
        return SUCCESS
    if cm_pct > 20:
        return WARNING
    return DANGER


def _roas_color(roas: float) -> str:
    if roas > 3:
        return SUCCESS
    if roas > 2:
        return WARNING
    return DANGER


def _om_color(om_pct: float) -> str:
    if om_pct > 10:
        return SUCCESS
    if om_pct > 0:
        return WARNING
    return DANGER


# ── Page setup ────────────────────────────────────────────────────────────────
st.markdown(_CSS, unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="margin-bottom: 24px;">
        <h2 style="margin:0; font-size:1.6rem; font-weight:700; letter-spacing:-0.02em;">
            Unit Economy
        </h2>
        <p style="color:{TEXT_SECONDARY}; font-size:0.85rem; margin-top:4px;">
            Per-order profitability — contribution margin, breakeven CAC, target ROAS
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Load persisted values ─────────────────────────────────────────────────────
saved = _load()

# ── INPUTS ────────────────────────────────────────────────────────────────────
st.markdown(
    f'<p style="color:{TEXT_SECONDARY}; font-size:0.7rem; text-transform:uppercase; '
    f'letter-spacing:0.1em; margin-bottom:8px;">Inputs</p>',
    unsafe_allow_html=True,
)

col_a, col_b = st.columns(2)

with col_a:
    aov = st.number_input(
        "AOV ($)",
        min_value=0.0,
        value=float(saved.get("aov", 79.0)),
        step=1.0,
        help="Average Order Value — the average revenue you receive per order.",
    )
    landed_cogs = st.number_input(
        "Landed COGS ($)",
        min_value=0.0,
        value=float(saved.get("landed_cogs", 18.0)),
        step=0.5,
        help="Cost of goods sold including freight/duties landed at your warehouse.",
    )
    return_rate = st.number_input(
        "Return Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(saved.get("return_rate", 8.0)),
        step=0.5,
        help="Percentage of orders that are returned. Increases effective cost per net order.",
    )
    processing_fee_pct = st.number_input(
        "Processing Fees (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(saved.get("processing_fee_pct", 3.5)),
        step=0.1,
        help="Payment processor fee as % of AOV (e.g. Stripe / PayPal / Shopify Payments).",
    )

with col_b:
    fulfillment_3pl = st.number_input(
        "3PL / Fulfillment ($)",
        min_value=0.0,
        value=float(saved.get("fulfillment_3pl", 6.5)),
        step=0.25,
        help="Third-party logistics pick-pack-ship cost per order.",
    )
    packaging = st.number_input(
        "Packaging ($)",
        min_value=0.0,
        value=float(saved.get("packaging", 1.5)),
        step=0.1,
        help="Box, tissue, inserts, and other packaging materials per order.",
    )
    label = st.number_input(
        "Label / Unboxing ($)",
        min_value=0.0,
        value=float(saved.get("label", 0.5)),
        step=0.1,
        help="Custom labels, stickers, or branded unboxing extras per order.",
    )
    ncac = st.number_input(
        "New Customer Acquisition Cost / nCAC ($)",
        min_value=0.0,
        value=float(saved.get("ncac", 25.0)),
        step=1.0,
        help="Your actual blended CAC — total ad spend divided by new customers acquired.",
    )

# ── Auto-calculations ─────────────────────────────────────────────────────────
returns_dollar       = aov * (return_rate / 100)
processing_dollar    = aov * (processing_fee_pct / 100)
total_variable       = returns_dollar + processing_dollar + fulfillment_3pl + packaging + label
gross_margin         = aov - landed_cogs
cm                   = gross_margin - total_variable
cm_pct               = (cm / aov * 100) if aov else 0.0
breakeven_cac        = cm
target_roas          = (100 / cm_pct) if cm_pct else 0.0
om                   = cm - ncac
om_pct               = (om / aov * 100) if aov else 0.0

# ── Persist inputs ────────────────────────────────────────────────────────────
_save({
    "aov": aov,
    "landed_cogs": landed_cogs,
    "return_rate": return_rate,
    "processing_fee_pct": processing_fee_pct,
    "fulfillment_3pl": fulfillment_3pl,
    "packaging": packaging,
    "label": label,
    "ncac": ncac,
})

st.markdown("<br>", unsafe_allow_html=True)

# ── OUTPUTS — 4 metric cards ──────────────────────────────────────────────────
st.markdown(
    f'<p style="color:{TEXT_SECONDARY}; font-size:0.7rem; text-transform:uppercase; '
    f'letter-spacing:0.1em; margin-bottom:8px;">Results</p>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)

_cm_col   = _cm_color(cm_pct)
_roas_col = _roas_color(target_roas)
_om_col   = _om_color(om_pct)
_cac_col  = SUCCESS if ncac < breakeven_cac else DANGER

def _metric_html(label: str, value: str, sub: str, color: str) -> str:
    return (
        f'<div style="background:{SURFACE}; border:1px solid {BORDER}; '
        f'border-radius:12px; padding:20px 20px 16px 20px;">'
        f'<p style="color:{TEXT_SECONDARY}; font-size:0.72rem; text-transform:uppercase; '
        f'letter-spacing:0.08em; margin:0 0 6px 0;">{label}</p>'
        f'<p style="color:{color}; font-size:1.7rem; font-weight:700; margin:0 0 4px 0;">{value}</p>'
        f'<p style="color:{TEXT_SECONDARY}; font-size:0.75rem; margin:0;">{sub}</p>'
        f'</div>'
    )

with c1:
    st.markdown(
        _metric_html(
            "Contribution Margin",
            f"${cm:.2f}",
            f"{cm_pct:.1f}% of AOV",
            _cm_col,
        ),
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        _metric_html(
            "Breakeven CAC",
            f"${breakeven_cac:.2f}",
            f"nCAC ${ncac:.2f} — {'✓ under' if ncac < breakeven_cac else '✗ over'}",
            _cac_col,
        ),
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        _metric_html(
            "Target ROAS",
            f"{target_roas:.2f}×",
            "Min to break even on ad spend",
            _roas_col,
        ),
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        _metric_html(
            "Operating Margin",
            f"${om:.2f}",
            f"{om_pct:.1f}% of AOV",
            _om_col,
        ),
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Waterfall chart ───────────────────────────────────────────────────────────
st.markdown(
    f'<p style="color:{TEXT_SECONDARY}; font-size:0.7rem; text-transform:uppercase; '
    f'letter-spacing:0.1em; margin-bottom:8px;">Order Waterfall</p>',
    unsafe_allow_html=True,
)

wf_labels   = ["AOV", "COGS", "Returns", "Processing", "3PL", "Packaging", "Label", "Gross CM", "nCAC", "Operating Margin"]
wf_values   = [aov, -landed_cogs, -returns_dollar, -processing_dollar, -fulfillment_3pl, -packaging, -label, 0, -ncac, 0]
wf_measures = ["absolute", "relative", "relative", "relative", "relative", "relative", "relative", "total", "relative", "total"]

# Assign bar colors
wf_colors = []
for m, v in zip(wf_measures, wf_values):
    if m == "absolute":
        wf_colors.append(PRIMARY)
    elif m == "total":
        wf_colors.append(SECONDARY)
    else:
        wf_colors.append(DANGER if v < 0 else SUCCESS)

fig = go.Figure(
    go.Waterfall(
        orientation="v",
        measure=wf_measures,
        x=wf_labels,
        y=wf_values,
        text=[f"${abs(v):.2f}" if v != 0 else "" for v in wf_values],
        textposition="outside",
        textfont=dict(color=TEXT_PRIMARY, size=11),
        connector=dict(line=dict(color=BORDER, width=1, dash="dot")),
        increasing=dict(marker=dict(color=SUCCESS)),
        decreasing=dict(marker=dict(color=DANGER)),
        totals=dict(marker=dict(color=SECONDARY)),
    )
)

fig.update_layout(
    paper_bgcolor=SURFACE,
    plot_bgcolor=SURFACE,
    font=dict(family="Inter, Segoe UI, sans-serif", color=TEXT_PRIMARY),
    xaxis=dict(
        showgrid=False,
        linecolor=BORDER,
        tickfont=dict(color=TEXT_SECONDARY),
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        linecolor=BORDER,
        tickfont=dict(color=TEXT_SECONDARY),
        zeroline=False,
        tickprefix="$",
    ),
    margin=dict(l=16, r=16, t=24, b=16),
    showlegend=False,
    height=380,
)

st.plotly_chart(fig, use_container_width=True)

# ── Cost breakdown table ──────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    f'<p style="color:{TEXT_SECONDARY}; font-size:0.7rem; text-transform:uppercase; '
    f'letter-spacing:0.1em; margin-bottom:8px;">Cost Breakdown</p>',
    unsafe_allow_html=True,
)

import pandas as pd

breakdown_items = [
    ("Landed COGS",      landed_cogs,       landed_cogs / aov * 100 if aov else 0),
    ("Returns",          returns_dollar,    returns_dollar / aov * 100 if aov else 0),
    ("Processing Fees",  processing_dollar, processing_dollar / aov * 100 if aov else 0),
    ("3PL / Fulfillment", fulfillment_3pl,  fulfillment_3pl / aov * 100 if aov else 0),
    ("Packaging",        packaging,         packaging / aov * 100 if aov else 0),
    ("Label / Unboxing", label,             label / aov * 100 if aov else 0),
]

df_breakdown = pd.DataFrame(breakdown_items, columns=["Item", "Cost ($)", "% of AOV"])
df_breakdown["Cost ($)"] = df_breakdown["Cost ($)"].map("${:.2f}".format)
df_breakdown["% of AOV"] = df_breakdown["% of AOV"].map("{:.1f}%".format)

st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Monthly view ──────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="margin-bottom: 16px;">
        <h3 style="margin:0; font-size:1.15rem; font-weight:600;">Monthly Projection</h3>
        <p style="color:{TEXT_SECONDARY}; font-size:0.82rem; margin-top:4px;">
            Scale the unit economics across your monthly order volume
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

_DATA_FILE_MONTHLY = Path(__file__).resolve().parent.parent / "data" / "unit_economy_monthly.json"

def _load_monthly() -> dict:
    if _DATA_FILE_MONTHLY.exists():
        try:
            return json.loads(_DATA_FILE_MONTHLY.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}

def _save_monthly(data: dict) -> None:
    _DATA_FILE_MONTHLY.parent.mkdir(parents=True, exist_ok=True)
    _DATA_FILE_MONTHLY.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


saved_m = _load_monthly()

mc1, mc2 = st.columns(2)

with mc1:
    total_orders = st.number_input(
        "Total Orders (monthly)",
        min_value=0,
        value=int(saved_m.get("total_orders", 500)),
        step=10,
        help="Total number of orders shipped in the month.",
    )
    new_customer_pct = st.number_input(
        "New Customer Share (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(saved_m.get("new_customer_pct", 60.0)),
        step=1.0,
        help="Percentage of orders from new (first-time) customers.",
    )
    ad_spend = st.number_input(
        "Monthly Ad Spend ($)",
        min_value=0.0,
        value=float(saved_m.get("ad_spend", 5000.0)),
        step=100.0,
        help="Total paid media spend for the month.",
    )
    fixed_costs = st.number_input(
        "Monthly Fixed Costs ($)",
        min_value=0.0,
        value=float(saved_m.get("fixed_costs", 8000.0)),
        step=100.0,
        help="Rent, salaries, software subscriptions and other fixed overhead.",
    )

with mc2:
    revenue_other = st.number_input(
        "Other Revenue ($)",
        min_value=0.0,
        value=float(saved_m.get("revenue_other", 0.0)),
        step=100.0,
        help="Subscription revenue, wholesale, or any non-DTC revenue streams.",
    )
    cogs_other = st.number_input(
        "Other COGS ($)",
        min_value=0.0,
        value=float(saved_m.get("cogs_other", 0.0)),
        step=100.0,
        help="COGS associated with the other revenue line above.",
    )
    misc_variable = st.number_input(
        "Misc Variable Costs ($)",
        min_value=0.0,
        value=float(saved_m.get("misc_variable", 0.0)),
        step=50.0,
        help="Any additional per-period variable costs not captured in unit economics.",
    )

# Derived
new_orders_count    = int(total_orders * new_customer_pct / 100)
returning_share_pct = 100.0 - new_customer_pct

monthly_revenue     = total_orders * aov + revenue_other
monthly_cogs        = total_orders * landed_cogs + cogs_other
monthly_variable    = total_orders * total_variable + misc_variable
monthly_cm_total    = total_orders * cm - misc_variable
monthly_op_profit   = monthly_cm_total - ad_spend - fixed_costs

_save_monthly({
    "total_orders": total_orders,
    "new_customer_pct": new_customer_pct,
    "ad_spend": ad_spend,
    "fixed_costs": fixed_costs,
    "revenue_other": revenue_other,
    "cogs_other": cogs_other,
    "misc_variable": misc_variable,
})

st.markdown("<br>", unsafe_allow_html=True)

# Returning share label
st.markdown(
    f'<p style="color:{TEXT_SECONDARY}; font-size:0.8rem; margin-bottom:4px;">'
    f'Returning customer share: <strong style="color:{TEXT_PRIMARY};">{returning_share_pct:.1f}%</strong> '
    f'&nbsp;·&nbsp; New customers this month: <strong style="color:{TEXT_PRIMARY};">{new_orders_count:,}</strong>'
    f'</p>',
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# Monthly CM table
cm_table_data = [
    ("Total Revenue",        f"${monthly_revenue:,.2f}",   f"{100:.1f}%"),
    ("Total COGS",           f"${monthly_cogs:,.2f}",       f"{monthly_cogs/monthly_revenue*100:.1f}%" if monthly_revenue else "—"),
    ("Total Variable Costs", f"${monthly_variable:,.2f}",  f"{monthly_variable/monthly_revenue*100:.1f}%" if monthly_revenue else "—"),
    ("Contribution Margin",  f"${monthly_cm_total:,.2f}",  f"{monthly_cm_total/monthly_revenue*100:.1f}%" if monthly_revenue else "—"),
]

df_cm_table = pd.DataFrame(cm_table_data, columns=["Line", "Amount ($)", "% of Revenue"])

col_tbl1, col_tbl2 = st.columns(2)

with col_tbl1:
    st.markdown(
        f'<p style="color:{TEXT_SECONDARY}; font-size:0.7rem; text-transform:uppercase; '
        f'letter-spacing:0.1em; margin-bottom:6px;">Monthly Contribution</p>',
        unsafe_allow_html=True,
    )
    st.dataframe(df_cm_table, use_container_width=True, hide_index=True)

# Monthly operating profit table
op_table_data = [
    ("Contribution Margin", f"${monthly_cm_total:,.2f}"),
    ("Ad Spend",            f"-${ad_spend:,.2f}"),
    ("Fixed Costs",         f"-${fixed_costs:,.2f}"),
    ("Operating Profit",    f"${monthly_op_profit:,.2f}"),
]

df_op_table = pd.DataFrame(op_table_data, columns=["Line", "Amount ($)"])

with col_tbl2:
    st.markdown(
        f'<p style="color:{TEXT_SECONDARY}; font-size:0.7rem; text-transform:uppercase; '
        f'letter-spacing:0.1em; margin-bottom:6px;">Monthly Operating Profit</p>',
        unsafe_allow_html=True,
    )
    st.dataframe(df_op_table, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2 summary metric cards
_monthly_op_pct = (monthly_op_profit / monthly_revenue * 100) if monthly_revenue else 0.0
_monthly_op_col = _om_color(_monthly_op_pct)
_monthly_cm_pct = (monthly_cm_total / monthly_revenue * 100) if monthly_revenue else 0.0
_monthly_cm_col = _cm_color(_monthly_cm_pct)

ms1, ms2 = st.columns(2)

with ms1:
    st.markdown(
        _metric_html(
            "Monthly Contribution Margin",
            f"${monthly_cm_total:,.0f}",
            f"{_monthly_cm_pct:.1f}% of revenue",
            _monthly_cm_col,
        ),
        unsafe_allow_html=True,
    )

with ms2:
    st.markdown(
        _metric_html(
            "Monthly Operating Profit",
            f"${monthly_op_profit:,.0f}",
            f"{_monthly_op_pct:.1f}% of revenue",
            _monthly_op_col,
        ),
        unsafe_allow_html=True,
    )

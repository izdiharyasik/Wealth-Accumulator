"""Shared utilities for the WealthAccumulator Streamlit app."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

APP_NAME = "WealthAccumulator"
PROFILE = {
    "nationality": "Indonesian",
    "age": 25,
    "base": "Jakarta",
    "active_horizon": "3 years active, then low-touch mode",
    "risk": "Moderate-aggressive without margin",
}
ASSET_CLASSES = ["US ETFs", "IDX Stocks", "SBN/ORI Bonds", "Gold", "BTC", "USD Cash"]
COLORS = {
    "US ETFs": "#36A2EB",
    "IDX Stocks": "#4BC0C0",
    "SBN/ORI Bonds": "#FFCE56",
    "Gold": "#F5B041",
    "BTC": "#F7931A",
    "USD Cash": "#8E9AAF",
}


def setup_page(title: str, icon: str = "💰") -> None:
    st.set_page_config(page_title=f"{APP_NAME} | {title}", page_icon=icon, layout="wide")
    inject_theme()
    st.sidebar.title("💰 WealthAccumulator")
    st.sidebar.caption("Institutional-grade wealth accumulation toolkit")
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Profile: Indonesian, age 25, Jakarta-based, moderate-aggressive, "
        "no leverage, small-to-mid capital growing monthly."
    )


def inject_theme() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(135deg, #07111f 0%, #101827 50%, #172033 100%); color: #f7fafc; }
        [data-testid="stSidebar"] { background: #08111f; }
        .metric-card, .wa-card {
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 18px;
            padding: 1.1rem;
            background: rgba(255,255,255,0.055);
            box-shadow: 0 12px 30px rgba(0,0,0,0.22);
        }
        .urgency-high { color: #ff6b6b; font-weight: 700; }
        .urgency-medium { color: #ffd166; font-weight: 700; }
        .urgency-low { color: #06d6a0; font-weight: 700; }
        div[data-testid="stMetricValue"] { color: #f7fafc; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def rp(amount: float | int) -> str:
    sign = "-" if amount < 0 else ""
    return f"{sign}Rp {abs(float(amount)):,.0f}"



def allocation_from_profile(risk_score: int, horizon_months: int, usd_preference: int) -> dict[str, float]:
    """Return a target allocation tailored to the stated user profile."""
    risk = risk_score / 100
    usd = usd_preference / 100
    short_horizon = max(0, (36 - horizon_months) / 36)
    low_touch_penalty = 0.10 if horizon_months <= 12 else 0.0

    us_etfs = 30 + 25 * risk + 15 * usd - 8 * short_horizon
    idx = 18 + 18 * risk - 8 * usd - 10 * short_horizon - low_touch_penalty * 20
    bonds = 28 - 16 * risk + 16 * short_horizon + low_touch_penalty * 25
    gold = 10 + 3 * short_horizon
    btc = min(2, 0.5 + 2.0 * risk)
    usd_cash = 100 - (us_etfs + idx + bonds + gold + btc)

    raw = {
        "US ETFs": max(20, us_etfs),
        "IDX Stocks": max(5, idx),
        "SBN/ORI Bonds": max(10, bonds),
        "Gold": max(5, gold),
        "BTC": max(0, btc),
        "USD Cash": max(5, usd_cash),
    }
    raw["BTC"] = min(2, raw["BTC"])
    total = sum(raw.values())
    normalized = {asset: value / total * 100 for asset, value in raw.items()}
    if normalized["BTC"] > 2:
        excess = normalized["BTC"] - 2
        normalized["BTC"] = 2
        normalized["SBN/ORI Bonds"] += excess * 0.6
        normalized["USD Cash"] += excess * 0.4
    total = sum(normalized.values())
    return {asset: round(value / total * 100, 1) for asset, value in normalized.items()}


def allocation_table(allocation: dict[str, float], total_capital: float) -> pd.DataFrame:
    tiers = {
        "US ETFs": "Core (5–15% per ETF sleeve: VOO/QQQ)",
        "IDX Stocks": "Core/Tactical (5–15% core, 2–5% satellite)",
        "SBN/ORI Bonds": "Core defensive ballast",
        "Gold": "Hedge (1–3% per tranche)",
        "BTC": "Hedge/speculative cap (≤2%)",
        "USD Cash": "Liquidity/currency hedge",
    }
    return pd.DataFrame(
        [
            {
                "Asset": asset,
                "Target %": weight,
                "Target Amount": rp(total_capital * weight / 100),
                "Position Sizing Tier": tiers[asset],
            }
            for asset, weight in allocation.items()
        ]
    )


def pie_chart(allocation: dict[str, float], title: str) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(allocation.keys()),
                values=list(allocation.values()),
                hole=0.42,
                marker_colors=[COLORS.get(a, "#8892b0") for a in allocation],
                textinfo="label+percent",
            )
        ]
    )
    fig.update_layout(template="plotly_dark", title=title, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


def line_chart(df: pd.DataFrame, title: str) -> go.Figure:
    fig = go.Figure()
    for column in df.columns:
        if column != "Month":
            fig.add_trace(go.Scatter(x=df["Month"], y=df[column], mode="lines", name=column))
    fig.update_layout(
        template="plotly_dark",
        title=title,
        xaxis_title="Month",
        yaxis_title="Portfolio Value (IDR)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


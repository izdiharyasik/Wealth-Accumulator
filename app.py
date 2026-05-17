import streamlit as st

from utils import APP_NAME, PROFILE, setup_page

setup_page("Home", "💰")

st.title("💰 WealthAccumulator")
st.subheader("A Jakarta-to-London wealth accumulation and portfolio management cockpit")

st.markdown(
    """
    WealthAccumulator is designed for a 25-year-old Indonesian investor based in Jakarta who wants to compound capital aggressively, avoid margin-call risk, and transition into a low-touch autopilot portfolio before postgraduate study in London.
    """
)

cols = st.columns(4)
metrics = [
    ("Risk stance", PROFILE["risk"]),
    ("Horizon", PROFILE["active_horizon"]),
    ("Currency", "IDR base + USD ETF exposure"),
    ("Constraint", "Autopilot by Sep 2026"),
]
for col, (label, value) in zip(cols, metrics):
    col.metric(label, value)

st.markdown("---")
st.header("Modules")

modules = [
    ("1 — Capital Sequencing Wizard", "Prioritize debts, emergency reserves, employer match, tax-advantaged/goal funding, and investing actions."),
    ("2 — Portfolio Allocator", "Generate a no-leverage target allocation across US ETFs, IDX stocks, SBN/ORI, gold, BTC, and USD cash."),
    ("3 — Commodity Supercycle Screener", "Rank copper, lithium, nickel, silver, uranium, and natural gas with conviction tags."),
    ("4 — Market Regime Indicator", "Fetch live S&P 500 proxy data with yfinance and compare price to the 50-day moving average."),
    ("5 — Rebalancing Monitor", "Compare current holdings against target weights and produce sell/buy actions when drift exceeds ±5%."),
    ("6 — Wealth Growth Simulator", "Model conservative, base, and aggressive compounding paths with milestone markers."),
    ("7 — Pre-London Autopilot Checklist", "Track low-touch setup tasks before September 2026."),
]

for title, body in modules:
    with st.container(border=True):
        st.markdown(f"### {title}")
        st.write(body)

st.info("Use the sidebar navigation to open each module. Inputs are persisted in `st.session_state` across pages during your session.")

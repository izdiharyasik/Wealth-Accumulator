import pandas as pd
import plotly.express as px
import streamlit as st

from utils import setup_page

setup_page("Commodity Supercycle Screener", "⛏️")
st.title("⛏️ Module 3 — Commodity Supercycle Screener")
st.caption("Reference framework for commodity-linked watchlists; implementation avoids automatic buy orders and keeps the core portfolio simple.")

commodities = pd.DataFrame(
    [
        {"Commodity": "Copper", "Demand Growth %": 85, "Supply Constraint": 9, "Lead Time": 8, "Current vs Target": 7, "April 2026 Benchmark": "$12,000/t target", "Route": "Watch via diversified miners/ETFs"},
        {"Commodity": "Lithium", "Demand Growth %": 300, "Supply Constraint": 6, "Lead Time": 5, "Current vs Target": 6, "April 2026 Benchmark": "$18,000/t LCE target", "Route": "Avoid single-name concentration"},
        {"Commodity": "Nickel", "Demand Growth %": 130, "Supply Constraint": 7, "Lead Time": 6, "Current vs Target": 6, "April 2026 Benchmark": "$24,000/t target", "Route": "Indonesia-linked watchlist"},
        {"Commodity": "Silver", "Demand Growth %": 60, "Supply Constraint": 7, "Lead Time": 6, "Current vs Target": 8, "April 2026 Benchmark": "$35/oz target", "Route": "Hedge via precious metals sleeve"},
        {"Commodity": "Uranium", "Demand Growth %": 70, "Supply Constraint": 9, "Lead Time": 9, "Current vs Target": 7, "April 2026 Benchmark": "$110/lb target", "Route": "Watch; volatile policy-sensitive asset"},
        {"Commodity": "Natural Gas", "Demand Growth %": 45, "Supply Constraint": 5, "Lead Time": 4, "Current vs Target": 5, "April 2026 Benchmark": "$4.50/MMBtu target", "Route": "Avoid direct futures exposure"},
    ]
)
commodities["Demand Score"] = (commodities["Demand Growth %"] / commodities["Demand Growth %"].max() * 10).round(1)
commodities["Conviction Score"] = (
    commodities["Demand Score"] * 0.30
    + commodities["Supply Constraint"] * 0.30
    + commodities["Lead Time"] * 0.20
    + commodities["Current vs Target"] * 0.20
).round(1)
commodities["Tag"] = pd.cut(commodities["Conviction Score"], bins=[0, 6.2, 7.4, 10], labels=["AVOID", "WATCH", "BUY/ACCUMULATE WATCHLIST"])
ranked = commodities.sort_values("Conviction Score", ascending=False)

st.subheader("Demand growth reference table")
st.dataframe(ranked, use_container_width=True, hide_index=True)

fig = px.bar(ranked, x="Commodity", y="Conviction Score", color="Tag", text="Conviction Score", template="plotly_dark", title="Ranked commodity conviction list")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

st.info("For this user profile, commodity exposure should remain tactical or indirect. The autopilot core should still be US ETFs, selected IDX exposure, SBN/ORI, gold, BTC capped at 2%, and USD cash.")

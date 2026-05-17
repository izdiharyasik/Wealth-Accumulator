import pandas as pd
import plotly.express as px
import streamlit as st

from utils import setup_page

setup_page("Commodity Screener", "⛏️")
st.title("⛏️ Module 3 — Commodity Screener")
st.caption("Reference framework for commodity-linked watchlists; implementation avoids automatic buy orders and keeps the core portfolio simple.")

commodity_reasons = {
    "Copper": "7–15 year mine lead time creates structural undersupply; grids, EVs, and data centers all require it simultaneously.",
    "Lithium": "Demand is explosive (+300%) but supply is catching up via new projects; price volatility is extreme — wait for better entry.",
    "Nickel": "Indonesia export restrictions create local opportunity but global price is sensitive to policy reversals.",
    "Silver": "Dual industrial/monetary demand, solar photovoltaic growth, and the gold-silver ratio being historically stretched support the setup.",
    "Uranium": "The nuclear renaissance is real but policy-sensitive; utility contract cycles create lumpy demand signals.",
    "Natural Gas": "It is a transition fuel with a shorter runway; direct futures exposure is too volatile for a buy-and-hold profile.",
}

commodities = pd.DataFrame(
    [
        {"Commodity": "Copper", "Demand Growth %": 85, "Supply Constraint": 9, "Lead Time": 8, "Current vs Target": 7, "April 2026 Benchmark": "$12,000/t target", "Route": "Watch via diversified miners/ETFs", "Tag": "BUY"},
        {"Commodity": "Lithium", "Demand Growth %": 300, "Supply Constraint": 6, "Lead Time": 5, "Current vs Target": 6, "April 2026 Benchmark": "$18,000/t LCE target", "Route": "Avoid single-name concentration", "Tag": "WATCH"},
        {"Commodity": "Nickel", "Demand Growth %": 130, "Supply Constraint": 7, "Lead Time": 6, "Current vs Target": 6, "April 2026 Benchmark": "$24,000/t target", "Route": "Indonesia-linked watchlist", "Tag": "WATCH"},
        {"Commodity": "Silver", "Demand Growth %": 60, "Supply Constraint": 7, "Lead Time": 6, "Current vs Target": 8, "April 2026 Benchmark": "$35/oz target", "Route": "Hedge via precious metals sleeve", "Tag": "BUY"},
        {"Commodity": "Uranium", "Demand Growth %": 70, "Supply Constraint": 9, "Lead Time": 9, "Current vs Target": 7, "April 2026 Benchmark": "$110/lb target", "Route": "Watch; volatile policy-sensitive asset", "Tag": "WATCH"},
        {"Commodity": "Natural Gas", "Demand Growth %": 45, "Supply Constraint": 5, "Lead Time": 4, "Current vs Target": 5, "April 2026 Benchmark": "$4.50/MMBtu target", "Route": "Avoid direct futures exposure", "Tag": "AVOID"},
    ]
)
commodities["Demand Score"] = (commodities["Demand Growth %"] / commodities["Demand Growth %"].max() * 10).round(1)
commodities["Conviction Score"] = (
    commodities["Demand Score"] * 0.30
    + commodities["Supply Constraint"] * 0.30
    + commodities["Lead Time"] * 0.20
    + commodities["Current vs Target"] * 0.20
).round(1)
ranked = commodities.sort_values("Conviction Score", ascending=False)

st.subheader("Commodity conviction notes")
for _, row in ranked.iterrows():
    with st.expander(f"{row['Commodity']} — {row['Tag']} · conviction score {row['Conviction Score']}/10"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Demand growth", f"{row['Demand Growth %']}%")
        col2.metric("Conviction score", f"{row['Conviction Score']}/10")
        col3.metric("Tag", row["Tag"])
        st.markdown(f"**Why this tag?** {commodity_reasons[row['Commodity']]}")
        st.write(f"**Supply constraint severity:** {row['Supply Constraint']}/10 · **Lead time:** {row['Lead Time']}/10 · **Price vs target:** {row['Current vs Target']}/10")
        st.write(f"**April 2026 reference benchmark:** {row['April 2026 Benchmark']}")
        st.write(f"**Preferred route:** {row['Route']}")

fig = px.bar(ranked, x="Commodity", y="Conviction Score", color="Tag", text="Conviction Score", template="plotly_dark", title="Ranked commodity conviction list")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

st.info("For this user profile, commodity exposure should remain tactical or indirect. The core portfolio should still be US ETFs, selected IDX exposure, SBN/ORI, gold, BTC capped at 2%, and USD cash.")

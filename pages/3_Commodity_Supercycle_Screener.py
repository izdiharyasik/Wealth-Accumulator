import pandas as pd
import plotly.express as px
import streamlit as st

from utils import ACTION_STYLES, hero, next_step_banner, section_header, setup_page, status_pill, styled_action_table, terminal_layout

setup_page("Commodity Screener", "⛏️")
hero(
    "Commodity Supercycle Screener",
    "A tactical watchlist, not an auto-trader: green means accumulate, amber means research/wait, red means avoid or reduce exposure.",
    "MODULE 3 // COLOR-CORRECT SIGNALS",
)

commodity_reasons = {
    "Copper": "7–15 year mine lead time creates structural undersupply; grids, EVs, and data centers all require it simultaneously.",
    "Lithium": "Demand is explosive but supply is catching up via new projects; price volatility is extreme, so wait for a cleaner entry.",
    "Nickel": "Indonesia export restrictions create local opportunity, but global price is sensitive to policy reversals and oversupply headlines.",
    "Silver": "Dual industrial/monetary demand, solar photovoltaic growth, and a stretched gold-silver ratio support the setup.",
    "Uranium": "The nuclear renaissance is real but policy-sensitive; utility contract cycles create lumpy demand signals.",
    "Natural Gas": "It is a transition fuel with a shorter runway; direct futures exposure is too volatile for a buy-and-hold profile.",
}

commodities = pd.DataFrame(
    [
        {"Commodity": "Copper", "Demand Growth %": 85, "Supply Constraint": 9, "Lead Time": 8, "Current vs Target": 7, "April 2026 Benchmark": "$12,000/t target", "Route": "Watch via diversified miners/ETFs", "Action": "BUY"},
        {"Commodity": "Lithium", "Demand Growth %": 300, "Supply Constraint": 6, "Lead Time": 5, "Current vs Target": 6, "April 2026 Benchmark": "$18,000/t LCE target", "Route": "Avoid single-name concentration", "Action": "WATCH"},
        {"Commodity": "Nickel", "Demand Growth %": 130, "Supply Constraint": 7, "Lead Time": 6, "Current vs Target": 6, "April 2026 Benchmark": "$24,000/t target", "Route": "Indonesia-linked watchlist", "Action": "WATCH"},
        {"Commodity": "Silver", "Demand Growth %": 60, "Supply Constraint": 7, "Lead Time": 6, "Current vs Target": 8, "April 2026 Benchmark": "$35/oz target", "Route": "Hedge via precious metals sleeve", "Action": "BUY"},
        {"Commodity": "Uranium", "Demand Growth %": 70, "Supply Constraint": 9, "Lead Time": 9, "Current vs Target": 7, "April 2026 Benchmark": "$110/lb target", "Route": "Watch; volatile policy-sensitive asset", "Action": "WATCH"},
        {"Commodity": "Natural Gas", "Demand Growth %": 45, "Supply Constraint": 5, "Lead Time": 4, "Current vs Target": 5, "April 2026 Benchmark": "$4.50/MMBtu target", "Route": "Avoid direct futures exposure", "Action": "AVOID"},
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

section_header("SIGNAL LEGEND", "Natural action colors", "The app now uses the same mental model everywhere: green = constructive, amber = caution, red = do not touch/reduce.")
legend_cols = st.columns(4)
for col, action in zip(legend_cols, ["BUY", "HOLD", "WATCH", "AVOID"]):
    col.markdown(status_pill(action), unsafe_allow_html=True)
    col.caption(ACTION_STYLES[action]["label"])

section_header("RANKED TAPE", "Commodity conviction matrix", "Sorted by weighted demand, supply constraint, lead time, and price-vs-target score.")
display = ranked[["Commodity", "Action", "Conviction Score", "Demand Growth %", "Supply Constraint", "Lead Time", "Route"]]
st.dataframe(styled_action_table(display, "Action"), width="stretch", hide_index=True)

for _, row in ranked.iterrows():
    with st.expander(f"{row['Commodity']} — {row['Action']} · conviction score {row['Conviction Score']}/10"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Demand growth", f"{row['Demand Growth %']}%")
        col2.metric("Conviction score", f"{row['Conviction Score']}/10")
        col3.markdown(status_pill(row["Action"]), unsafe_allow_html=True)
        st.markdown(f"**Why this signal?** {commodity_reasons[row['Commodity']]}")
        st.write(f"**Supply constraint:** {row['Supply Constraint']}/10 · **Lead time:** {row['Lead Time']}/10 · **Price vs target:** {row['Current vs Target']}/10")
        st.write(f"**April 2026 reference benchmark:** {row['April 2026 Benchmark']}")
        st.write(f"**Preferred route:** {row['Route']}")

color_map = {action: style["color"] for action, style in ACTION_STYLES.items()}
fig = px.bar(
    ranked,
    x="Commodity",
    y="Conviction Score",
    color="Action",
    text="Conviction Score",
    color_discrete_map=color_map,
    title="Ranked commodity conviction list",
)
fig.update_traces(textposition="outside", marker_line_width=0)
st.plotly_chart(terminal_layout(fig), width="stretch")

st.info("For this user profile, commodity exposure should remain tactical or indirect. The core portfolio stays US ETFs, selected IDX exposure, SBN/ORI, gold, BTC capped at 2%, and USD cash.")
next_step_banner("Throttle tactical interest through market regime.", "If the screener says BUY but the regime is risk-off, route new cash defensively or wait for the next DCA window.", "pages/4_Market_Regime_Indicator.py", "Risk throttle")

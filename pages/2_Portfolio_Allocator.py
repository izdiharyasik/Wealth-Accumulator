import streamlit as st

from utils import allocation_from_profile, allocation_table, pie_chart, rp, setup_page

setup_page("Portfolio Allocator", "🥧")
st.title("🥧 Module 2 — Portfolio Allocator")
st.caption("Phase 3 only: 100% invested/allocated capital, no margin, autopilot-ready before London.")

col1, col2 = st.columns(2)
total_capital = col1.number_input("Total capital (IDR)", min_value=0, value=int(st.session_state.get("total_capital", 150_000_000)), step=5_000_000)
risk = col2.slider("Risk tolerance", 0, 100, int(st.session_state.get("risk", 70)), help="Moderate-aggressive profile defaults near 70.")
horizon = col1.slider("Time horizon before low-touch mode (months)", 1, 60, int(st.session_state.get("horizon", 36)))
usd_pref = col2.slider("USD exposure preference", 0, 100, int(st.session_state.get("usd_pref", 55)))

st.session_state.update(total_capital=total_capital, risk=risk, horizon=horizon, usd_pref=usd_pref)
allocation = allocation_from_profile(risk, horizon, usd_pref)
st.session_state["target_allocation"] = allocation

st.plotly_chart(pie_chart(allocation, "Recommended strategic allocation"), use_container_width=True)
st.dataframe(allocation_table(allocation, total_capital), use_container_width=True, hide_index=True)

st.info("Position sizing guardrails: keep individual core positions around 5–15%, tactical satellites around 2–5%, hedges around 1–3%, and BTC capped at 2% of portfolio value.")
st.warning("This model intentionally skips leverage phases because the user can tolerate volatility but cannot tolerate margin calls.")

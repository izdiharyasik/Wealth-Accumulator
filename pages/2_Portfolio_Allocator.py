import streamlit as st

from utils import allocation_from_profile, allocation_table, pie_chart, rp, setup_page

setup_page("Portfolio Allocator", "🥧")
st.title("🥧 Module 2 — Portfolio Allocator")
st.caption("Phase 3 only: 100% invested/allocated capital, no margin, and designed for low-touch mode.")

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


lean = "growth" if risk >= 60 and horizon >= 24 else "defensive"
if lean == "growth":
    logic = "your risk tolerance and time horizon can support higher equity beta while BTC remains capped and bonds/gold still dampen shocks."
else:
    logic = "your shorter horizon or lower risk score calls for more capital preservation through bonds, gold, and cash optionality."
st.success(f"With a risk score of {risk} and horizon of {horizon} months, your allocation leans {lean} because {logic}")

with st.expander("📖 Why this allocation?"):
    st.markdown(
        """
        **US ETFs (VOO/QQQ)**
        US ETFs provide passive beta to the deepest equity market and reduce the need to pick individual winners. SPIVA research shows that 65.2% of active funds underperform, so low-cost index exposure helps minimize fee drag and manager-selection risk.

        **IDX Stocks**
        IDX stocks create a natural home-currency hedge because part of the portfolio remains linked to IDR assets and domestic economic conditions. Exposure should be selective, with emphasis on quality Indonesian companies and commodity-linked equities where the country has structural relevance.

        **SBN/ORI Bonds**
        SBN/ORI bonds provide IDR yield, capital preservation, and a stabilizing ballast when equities sell off. They also tend to have lower correlation to global equities, which makes them useful for low-touch portfolio construction.

        **Gold**
        Gold acts as a hedge against currency stress, inflation anxiety, and equity drawdowns. It is not perfectly correlated with stocks or bonds, and commodity-supercycle dynamics can add a secondary tailwind.

        **BTC**
        BTC is capped at 1–2% because it can improve upside optionality without dominating portfolio risk. Beyond roughly a 5% allocation, volatility can rise non-linearly and start driving the portfolio instead of complementing it.

        **USD Cash**
        USD cash is a currency hedge and a source of dry powder during risk-off periods. It provides optionality for tactical deployment without forcing sales from equities, bonds, gold, or BTC.
        """
    )

import streamlit as st

from utils import allocation_from_profile, allocation_table, hero, next_step_banner, pie_chart, rp, section_header, setup_page

setup_page("Portfolio Allocator", "🥧")
hero("Portfolio Allocator", "Phase 3 capital map: fully allocated, no margin, designed for low-touch mode and clean rebalancing.", "MODULE 2 // STRATEGIC ALLOCATION")
section_header("INPUT", "Allocation controls", "Tune risk, time-to-autopilot, and USD preference while keeping BTC capped and leverage disabled.")

col1, col2 = st.columns(2)
total_capital = col1.number_input("Total capital (IDR)", min_value=0, value=int(st.session_state.get("total_capital", 150_000_000)), step=5_000_000)
risk = col2.slider("Risk tolerance", 0, 100, int(st.session_state.get("risk", 70)), help="Moderate-aggressive profile defaults near 70.")
horizon = col1.slider("Time horizon before low-touch mode (months)", 1, 60, int(st.session_state.get("horizon", 36)))
usd_pref = col2.slider("USD exposure preference", 0, 100, int(st.session_state.get("usd_pref", 55)))

st.session_state.update(total_capital=total_capital, risk=risk, horizon=horizon, usd_pref=usd_pref)
allocation = allocation_from_profile(risk, horizon, usd_pref)
st.session_state["target_allocation"] = allocation

st.plotly_chart(pie_chart(allocation, "Recommended strategic allocation"), width="stretch")
st.dataframe(allocation_table(allocation, total_capital), width="stretch", hide_index=True)

section_header("GUARDRAILS", "Sizing discipline", "Core positions 5–15%, tactical satellites 2–5%, hedges 1–3%, and BTC capped at 2% of portfolio value.")
st.warning("This model intentionally skips leverage phases because the user can tolerate volatility but cannot tolerate margin calls.")
next_step_banner("Use tactical screens only after the target allocation exists.", "Commodity and regime views should tilt new cash or watchlists, not override the strategic mix or BTC cap.", "pages/3_Commodity_Supercycle_Screener.py", "Tactical watchlist")


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

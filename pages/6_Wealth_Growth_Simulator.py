import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import line_chart, rp, setup_page

setup_page("Wealth Growth Simulator", "🚀")
st.title("🚀 Module 6 — Wealth Growth Simulator")
st.caption("Compound growth curves for conservative, base, and aggressive paths with monthly salary contributions.")

col1, col2 = st.columns(2)
starting = col1.number_input("Starting capital (IDR)", min_value=0, value=int(st.session_state.get("sim_starting", 150_000_000)), step=5_000_000)
monthly = col2.number_input("Monthly contribution (IDR)", min_value=0, value=int(st.session_state.get("sim_monthly", 8_000_000)), step=500_000)
horizon = col1.slider("Simulation horizon (months)", 1, 120, int(st.session_state.get("sim_horizon", 36)))
custom = col2.checkbox("Customize CAGR assumptions by scenario", value=bool(st.session_state.get("sim_custom", False)))

cagrs = {"Conservative (8%)": 8.0, "Base (12%)": 12.0, "Aggressive (18%)": 18.0}
if custom:
    for name, default in list(cagrs.items()):
        cagrs[name] = st.number_input(f"{name} CAGR", min_value=-50.0, max_value=100.0, value=float(st.session_state.get(f"cagr_{name}", default)), step=0.5)
        st.session_state[f"cagr_{name}"] = cagrs[name]

st.session_state.update(sim_starting=starting, sim_monthly=monthly, sim_horizon=horizon, sim_custom=custom)
months = list(range(horizon + 1))
results = {"Month": months}
for scenario, cagr in cagrs.items():
    monthly_rate = (1 + cagr / 100) ** (1 / 12) - 1
    values = []
    value = starting
    for month in months:
        if month > 0:
            value = value * (1 + monthly_rate) + monthly
        values.append(value)
    results[scenario] = values

df = pd.DataFrame(results)
fig = line_chart(df, "Projected wealth accumulation")
for milestone in [100_000_000, 500_000_000, 1_000_000_000]:
    fig.add_hline(y=milestone, line_dash="dot", annotation_text=rp(milestone), annotation_position="top left")
st.plotly_chart(fig, use_container_width=True)

summary = []
for scenario in cagrs:
    final = df[scenario].iloc[-1]
    hit = "Not reached"
    for milestone in [100_000_000, 500_000_000, 1_000_000_000]:
        reached = df[df[scenario] >= milestone]
        if not reached.empty:
            hit = f"{rp(milestone)} in month {int(reached['Month'].iloc[0])}"
    summary.append({"Scenario": scenario, "Final Value": rp(final), "Highest milestone reached": hit})
st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)

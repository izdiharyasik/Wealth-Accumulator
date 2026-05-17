from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import setup_page

setup_page("Pre-London Autopilot Checklist", "✈️")
st.title("✈️ Module 7 — Pre-London Autopilot Checklist")
st.caption("Static completion tracker for actions to finish before September 2026.")

items = [
    "Rebalance to low-touch allocation",
    "Consolidate brokers and remove duplicate accounts",
    "Set monthly DCA schedule for US ETFs / IDX core / SBN or cash",
    "Move to bond-heavy defensive posture for tuition and living-cost runway",
    "Create currency hedge plan for GBP and USD exposure",
    "Document account access, 2FA backups, beneficiaries, and emergency contacts",
    "Set calendar reminders for quarterly review only",
    "Keep BTC capped at 2% and disable margin/leverage permissions",
]

completed = 0
for item in items:
    key = "check_" + item.lower().replace(" ", "_").replace("/", "_")
    if st.checkbox(item, value=bool(st.session_state.get(key, False)), key=key):
        completed += 1

progress = completed / len(items)
st.progress(progress, text=f"{completed}/{len(items)} completed ({progress:.0%})")

fig = go.Figure(go.Indicator(mode="gauge+number", value=progress * 100, title={"text": "Autopilot readiness %"}, gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#06d6a0"}}))
fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

cutoff = date(2026, 9, 1)
days_left = (cutoff - date.today()).days
if days_left >= 0:
    st.info(f"Days until September 1, 2026 autopilot deadline: {days_left}.")
else:
    st.warning("September 1, 2026 has passed. Treat incomplete items as immediate maintenance tasks.")

st.subheader("Recommended autopilot posture")
st.dataframe(
    pd.DataFrame(
        [
            {"Area": "Portfolio", "Rule": "Quarterly review only unless ±5% drift trigger fires."},
            {"Area": "Cash", "Rule": "Maintain GBP/IDR/USD runway for tuition, rent deposits, and emergencies."},
            {"Area": "Risk", "Rule": "No leverage, no margin, no forced liquidation risk."},
            {"Area": "Execution", "Rule": "Automate DCA and SBN/ORI maturity tracking before departure."},
        ]
    ),
    use_container_width=True,
    hide_index=True,
)

import pandas as pd
import streamlit as st

from utils import ASSET_CLASSES, allocation_from_profile, hero, next_step_banner, pie_chart, rp, section_header, setup_page, styled_action_table

setup_page("Rebalancing Monitor", "⚖️")
hero("Rebalancing Monitor", "Quarterly drift control for a low-touch, no-margin portfolio. Green buys underweight assets; red sells overweight risk.", "MODULE 5 // DRIFT DISCIPLINE")
section_header("INPUT", "Current holdings", "Use this only quarterly or after a major market move — not as a daily trading prompt.")

default_target = st.session_state.get("target_allocation", allocation_from_profile(st.session_state.get("risk", 70), st.session_state.get("horizon", 36), st.session_state.get("usd_pref", 55)))

values = {}
with st.expander("📥 Enter current holdings", expanded=False):
    cols = st.columns(2)
    for idx, asset in enumerate(ASSET_CLASSES):
        values[asset] = cols[idx % 2].number_input(f"{asset} value (IDR)", min_value=0, value=int(st.session_state.get(f"holding_{asset}", 0)), step=1_000_000)
        st.session_state[f"holding_{asset}"] = values[asset]

total = sum(values.values())
if total == 0:
    st.info("Enter at least one non-zero holding to calculate drift and recommended actions.")
    st.stop()

rows = []
for asset in ASSET_CLASSES:
    current_pct = values[asset] / total * 100
    target_pct = default_target.get(asset, 0)
    target_value = total * target_pct / 100
    drift = current_pct - target_pct
    if drift > 5:
        action = "SELL"
        action_amount = values[asset] - target_value
    elif drift < -5:
        action = "BUY"
        action_amount = target_value - values[asset]
    else:
        action = "HOLD"
        action_amount = 0
    rows.append({"Asset": asset, "Current %": round(current_pct, 1), "Target %": target_pct, "Drift %": round(drift, 1), "Action": action, "Amount": action_amount})

drift_df = pd.DataFrame(rows)
section_header("OUTPUT", "Drift monitor", "Actions are color-coded consistently: BUY is green, HOLD is blue, SELL is red.")
st.dataframe(styled_action_table(drift_df.assign(Amount=drift_df["Amount"].map(rp)), "Action"), width="stretch", hide_index=True)

alerts = drift_df[drift_df["Action"] != "HOLD"]
if alerts.empty:
    st.success("All asset classes are within the ±5% drift band. No rebalance needed.")
else:
    st.warning("Rebalancing trigger active for one or more asset classes.")
    st.dataframe(styled_action_table(alerts.assign(Amount=alerts["Amount"].map(rp)), "Action"), width="stretch", hide_index=True)

current_allocation = {asset: values[asset] / total * 100 for asset in ASSET_CLASSES}
st.plotly_chart(pie_chart(current_allocation, "Current allocation"), width="stretch")
next_step_banner("Check whether the disciplined plan reaches your milestones.", "After drift actions are known, use the simulator to see how contribution rate and CAGR assumptions affect the active 3-year window.", "pages/6_Wealth_Growth_Simulator.py", "Trajectory")

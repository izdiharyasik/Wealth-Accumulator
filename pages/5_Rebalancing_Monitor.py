import pandas as pd
import streamlit as st

from utils import ASSET_CLASSES, allocation_from_profile, pie_chart, rp, setup_page

setup_page("Rebalancing Monitor", "⚖️")
st.title("⚖️ Rebalancing Monitor")
st.caption("Use this quarterly or when markets move significantly — not a daily tool.")
st.info("💡 You only need this tab when you suspect drift. Run it quarterly or after a major market move.")

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
st.subheader("Drift monitor")
st.dataframe(drift_df.assign(Amount=drift_df["Amount"].map(rp)), use_container_width=True, hide_index=True)

alerts = drift_df[drift_df["Action"] != "HOLD"]
if alerts.empty:
    st.success("All asset classes are within the ±5% drift band. No rebalance needed.")
else:
    st.warning("Rebalancing trigger active for one or more asset classes.")
    st.dataframe(alerts.assign(Amount=alerts["Amount"].map(rp)), use_container_width=True, hide_index=True)

current_allocation = {asset: values[asset] / total * 100 for asset in ASSET_CLASSES}
st.plotly_chart(pie_chart(current_allocation, "Current allocation"), use_container_width=True)

import pandas as pd
import streamlit as st

from utils import hero, next_step_banner, rp, section_header, setup_page, styled_action_table

setup_page("Capital Sequencing Wizard", "🧭")
hero("Capital Sequencing Wizard", "Nine-step financial order of operations localized for an IDR income base and a no-margin investment policy.", "MODULE 1 // CASHFLOW COMMAND")

with st.form("capital_sequence_form"):
    col1, col2 = st.columns(2)
    monthly_income = col1.number_input("Monthly income (IDR)", min_value=0, value=int(st.session_state.get("monthly_income", 20_000_000)), step=500_000)
    monthly_expenses = col2.number_input("Monthly essential expenses (IDR)", min_value=0, value=int(st.session_state.get("monthly_expenses", 10_000_000)), step=500_000)
    emergency_fund = col1.number_input("Current emergency fund (IDR)", min_value=0, value=int(st.session_state.get("emergency_fund", 30_000_000)), step=1_000_000)
    employer_match = col2.checkbox("Employer match / retirement contribution available", value=bool(st.session_state.get("employer_match", False)))
    debt_names = st.text_input("Debt names (comma separated)", value=st.session_state.get("debt_names", "Credit card, Personal loan"))
    debt_balances = st.text_input("Debt balances in IDR (comma separated)", value=st.session_state.get("debt_balances", "0, 0"))
    debt_rates = st.text_input("Debt APR % (comma separated)", value=st.session_state.get("debt_rates", "0, 0"))
    submitted = st.form_submit_button("Build action plan")

if submitted:
    st.session_state.update(
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        emergency_fund=emergency_fund,
        employer_match=employer_match,
        debt_names=debt_names,
        debt_balances=debt_balances,
        debt_rates=debt_rates,
    )

def parse_idr_numbers(text):
    values = []
    for item in text.split(","):
        cleaned = item.strip().replace("Rp", "").replace(".", "").replace(" ", "")
        values.append(float(cleaned or 0))
    return values


def parse_percent_numbers(text):
    values = []
    for item in text.split(","):
        cleaned = item.strip().replace("%", "").replace(" ", "")
        values.append(float(cleaned or 0))
    return values


names = [x.strip() for x in debt_names.split(",") if x.strip()]
balances = parse_idr_numbers(debt_balances)
rates = parse_percent_numbers(debt_rates)
debts = []
for idx, name in enumerate(names):
    balance = balances[idx] if idx < len(balances) else 0
    rate = rates[idx] if idx < len(rates) else 0
    if balance > 0:
        debts.append({"Debt": name, "Balance": balance, "APR %": rate, "Flag": "High interest" if rate > 6 else "Acceptable/low"})

free_cash_flow = max(monthly_income - monthly_expenses, 0)
target_emergency = monthly_expenses * 6
emergency_gap = max(target_emergency - emergency_fund, 0)
high_interest_debt = sum(d["Balance"] for d in debts if d["APR %"] > 6)
low_interest_debt = sum(d["Balance"] for d in debts if d["APR %"] <= 6)

steps = [
    (1, "Deductibles + immediate cash buffer", min(free_cash_flow * 0.25, max(monthly_expenses - emergency_fund, 0)), "High" if emergency_fund < monthly_expenses else "Low", "Keep at least 1 month of Jakarta expenses liquid before investing."),
    (2, "Employer match", free_cash_flow * 0.05 if employer_match else 0, "High" if employer_match else "Low", "Capture guaranteed compensation if available."),
    (3, "Pay high-interest debt >6%", min(free_cash_flow * 0.60, high_interest_debt), "High" if high_interest_debt else "Low", "Anything above the 6% threshold outranks risky assets."),
    (4, "Build 3–6 month emergency fund", min(free_cash_flow * 0.40, emergency_gap), "High" if emergency_gap else "Low", "Target six months of expenses for currency and life-transition resilience."),
    (5, "Tax/retirement wrappers or equivalents", free_cash_flow * 0.10, "Medium", "Use any available formal long-term savings vehicle without sacrificing liquidity."),
    (6, "Max moderate-return debt cleanup", min(free_cash_flow * 0.15, low_interest_debt), "Medium" if low_interest_debt else "Low", "Accelerate low-rate debt only after buffers are strong."),
    (7, "Core no-margin investing", free_cash_flow * 0.45 if high_interest_debt == 0 and emergency_gap == 0 else free_cash_flow * 0.15, "Medium", "DCA into US ETF/IDX core while preserving low-touch simplicity."),
    (8, "Major-goal sinking funds", free_cash_flow * 0.15, "Medium", "Ring-fence education, travel, housing deposits, foreign-currency setup cash, and major planned costs."),
    (9, "Tactical/aspirational bucket", free_cash_flow * 0.05, "Low", "Only after all prior steps are funded; no leverage or margin."),
]

df = pd.DataFrame(steps, columns=["Step", "Priority", "Suggested Monthly Rp", "Urgency", "Rationale"])
section_header("ACTION PLAN", "Prioritized cashflow queue", "High urgency appears red, medium amber, and low green so the next move is obvious.")
urgency_df = df.assign(**{"Suggested Monthly Rp": df["Suggested Monthly Rp"].map(rp)})
st.dataframe(styled_action_table(urgency_df, "Urgency"), width="stretch", hide_index=True)
next_step_banner("Convert the cashflow decision into a target mix.", "Once the monthly queue is clear, send deployable capital to the Portfolio Allocator so the portfolio target drives every later screen.", "pages/2_Portfolio_Allocator.py", "Strategic allocation")

if debts:
    debt_df = pd.DataFrame(debts)
    st.subheader("Debt screen")
    st.dataframe(debt_df.assign(Balance=debt_df["Balance"].map(rp)), width="stretch", hide_index=True)
    flagged = debt_df[debt_df["APR %"] > 6]
    if not flagged.empty:
        st.error(f"High-interest debt flagged above 6%: {', '.join(flagged['Debt'])}. Pause tactical investing until these are cleared.")
else:
    st.success("No debt balances entered. Core investing and major-goal reserves can move up the queue.")

st.metric("Monthly investable/free cash flow", rp(free_cash_flow))
st.metric("Emergency fund target (6 months)", rp(target_emergency), delta=f"Gap: {rp(emergency_gap)}")

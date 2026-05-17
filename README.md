# WealthAccumulator

WealthAccumulator is a Streamlit multipage wealth accumulation and portfolio management app tailored for an Indonesian investor, age 25, based in Jakarta, with a moderate-aggressive risk profile and a preference for low-touch portfolio management over the investment horizon.

The app intentionally uses a **no-leverage Phase 3 allocation**: the user can tolerate market volatility, but the portfolio must avoid margin calls and remain manageable in low-touch mode.

## Features

1. **Dashboard** — shows live macro conditions, a portfolio trajectory chart, and a curated macro/micro news feed.
2. **Capital Sequencing Wizard** — walks through a 9-step financial order of operations, flags debt above a 6% interest threshold, and recommends monthly Rupiah amounts by priority.
3. **Portfolio Allocator** — creates an allocation across US ETFs, IDX stocks, SBN/ORI bonds, gold, BTC capped at 2%, and USD cash.
4. **Commodity Screener** — ranks copper, lithium, nickel, silver, uranium, and natural gas using demand growth, supply constraints, lead time, and April 2026 benchmark targets.
5. **Market Regime Indicator** — fetches SPY or another S&P 500 proxy with `yfinance`, calculates the 50-day moving average, and displays a risk-on/risk-off signal.
6. **Rebalancing Monitor** — compares current holdings with target allocation and triggers alerts when any asset drifts more than ±5 percentage points.

## Tech Stack

- Streamlit multipage app
- Plotly charts
- yfinance for live market data
- pandas for portfolio and simulation tables
- `st.session_state` for input persistence across pages

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal.

## Project Structure

```text
app.py
utils.py
pages/
  1_Capital_Sequencing_Wizard.py
  2_Portfolio_Allocator.py
  3_Commodity_Supercycle_Screener.py
  4_Market_Regime_Indicator.py
  5_Rebalancing_Monitor.py
requirements.txt
README.md
```

## Notes

- This is an educational planning tool, not financial advice.
- Allocation logic is deliberately rule-based and transparent so it can be reviewed before low-touch mode.
- The dashboard and market regime pages depend on live data availability from Yahoo Finance through `yfinance`.

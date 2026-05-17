import pandas as pd
import streamlit as st
import yfinance as yf

from utils import PROFILE, hero, line_chart, next_step_banner, rp, section_header, setup_page, workflow_links, workflow_overview

setup_page("Dashboard", "🏠")

hero(
    "WealthAccumulator Terminal",
    "Macro-aware cockpit for aggressive compounding without leverage: grow capital, avoid forced liquidation, and transition cleanly into low-touch mode.",
    "DASHBOARD // JAKARTA BASE // NO MARGIN",
)

cols = st.columns(4)
metrics = [
    ("Risk stance", PROFILE["risk"]),
    ("Horizon", PROFILE["active_horizon"]),
    ("Currency", "IDR base + USD ETF exposure"),
    ("Operating mode", "Low-touch ready"),
]
for col, (label, value) in zip(cols, metrics):
    col.metric(label, value)

section_header("COMMAND CENTER", "One integrated workflow", "Use the app left-to-right: cashflow first, allocation second, tactical screens third, then regime/rebalance/simulation/autopilot.")
workflow_overview("Dashboard")
workflow_links()
next_step_banner(
    "Start with the next rupiah, not a disconnected tab.",
    "The Capital Sequencing Wizard decides whether cash should fill buffers, kill debt, or fund the portfolio before any screener matters.",
    "pages/1_Capital_Sequencing_Wizard.py",
    "Cashflow order",
)

section_header("SECTION 1", "Macro Conditions Panel", "Read the market like a cockpit: green is supportive, amber is caution, red is defensive.")

ASSETS = {
    "SPY": {"label": "S&P 500", "context": "equity risk appetite"},
    "GLD": {"label": "Gold", "context": "defensive hedge demand"},
    "BTC-USD": {"label": "Bitcoin", "context": "crypto risk appetite"},
    "DX-Y.NYB": {"label": "USD Index", "context": "currency pressure"},
}


@st.cache_data(ttl=900)
def load_macro_prices(tickers: tuple[str, ...]) -> pd.DataFrame:
    return yf.download(list(tickers), period="6mo", interval="1d", progress=False, auto_adjust=True, group_by="ticker")


def get_close_series(data: pd.DataFrame, ticker: str) -> pd.Series:
    if isinstance(data.columns, pd.MultiIndex):
        series = data[(ticker, "Close")]
    else:
        series = data["Close"]
    return series.dropna()

try:
    macro_data = load_macro_prices(tuple(ASSETS.keys()))
except Exception as exc:  # yfinance can fail because of connectivity or upstream rate limits.
    macro_data = pd.DataFrame()
    st.warning(f"Live macro data is unavailable right now: {exc}")

macro_rows = []
if not macro_data.empty:
    metric_cols = st.columns(4)
    for idx, (ticker, meta) in enumerate(ASSETS.items()):
        try:
            close = get_close_series(macro_data, ticker)
            latest = float(close.iloc[-1])
            previous = float(close.iloc[-2]) if len(close) > 1 else latest
            change_pct = ((latest / previous) - 1) * 100 if previous else 0
            ma50 = float(close.rolling(50).mean().dropna().iloc[-1])
            ma_label = "Above 50DMA" if latest > ma50 else "Below 50DMA"
            macro_rows.append(
                {
                    "Asset": meta["label"],
                    "Ticker": ticker,
                    "Latest": latest,
                    "1D Change %": change_pct,
                    "50DMA": ma50,
                    "Label": ma_label,
                    "Context": meta["context"],
                }
            )
            metric_cols[idx].metric(
                meta["label"],
                f"${latest:,.2f}",
                delta=f"{change_pct:+.2f}% · {ma_label}",
            )
        except Exception as exc:
            metric_cols[idx].warning(f"{meta['label']} unavailable: {exc}")

if macro_rows:
    st.subheader("Regime tape")
    for row in macro_rows:
        if row["Asset"] == "Gold":
            interpretation = "mild risk-off rotation signal" if row["Label"].startswith("Above") else "weaker defensive bid"
        elif row["Asset"] == "USD Index":
            interpretation = "tighter global liquidity pressure" if row["Label"].startswith("Above") else "easier currency backdrop for non-USD assets"
        elif row["Asset"] == "Bitcoin":
            interpretation = "speculative appetite remains supported" if row["Label"].startswith("Above") else "crypto risk appetite is cooling"
        else:
            interpretation = "risk-on equity backdrop" if row["Label"].startswith("Above") else "equity risk should be sized cautiously"
        st.write(f"• **{row['Asset']}** is trading {row['Label'].lower()} — {interpretation}.")
else:
    st.info("Macro cards will populate when yfinance data is available.")

section_header("SECTION 2", "Portfolio Trajectory", "Scenario curves for the next active compounding window before low-touch execution.")

with st.expander("✏️ Edit assumptions", expanded=False):
    col1, col2 = st.columns(2)
    starting = col1.number_input("Starting capital (IDR)", min_value=0, value=int(st.session_state.get("sim_starting", 150_000_000)), step=5_000_000)
    monthly = col2.number_input("Monthly contribution (IDR)", min_value=0, value=int(st.session_state.get("sim_monthly", 8_000_000)), step=500_000)
    horizon = col1.slider("Simulation horizon (months)", 1, 120, int(st.session_state.get("sim_horizon", 36)))
    conservative = col2.number_input("Conservative CAGR %", min_value=-50.0, max_value=100.0, value=float(st.session_state.get("cagr_conservative", 8.0)), step=0.5)
    base = col1.number_input("Base CAGR %", min_value=-50.0, max_value=100.0, value=float(st.session_state.get("cagr_base", 12.0)), step=0.5)
    aggressive = col2.number_input("Aggressive CAGR %", min_value=-50.0, max_value=100.0, value=float(st.session_state.get("cagr_aggressive", 18.0)), step=0.5)

st.session_state.update(
    sim_starting=starting,
    sim_monthly=monthly,
    sim_horizon=horizon,
    cagr_conservative=conservative,
    cagr_base=base,
    cagr_aggressive=aggressive,
)

months = list(range(horizon + 1))
scenarios = {
    f"Conservative ({conservative:g}%)": conservative,
    f"Base ({base:g}%)": base,
    f"Aggressive ({aggressive:g}%)": aggressive,
}
trajectory = {"Month": months}
for scenario, cagr in scenarios.items():
    monthly_rate = (1 + cagr / 100) ** (1 / 12) - 1
    value = starting
    values = []
    for month in months:
        if month > 0:
            value = value * (1 + monthly_rate) + monthly
        values.append(value)
    trajectory[scenario] = values

trajectory_df = pd.DataFrame(trajectory)
fig = line_chart(trajectory_df, "Portfolio trajectory")
for milestone in [100_000_000, 500_000_000, 1_000_000_000]:
    fig.add_hline(y=milestone, line_dash="dot", annotation_text=rp(milestone), annotation_position="top left")
st.plotly_chart(fig, width="stretch")
base_column = [col for col in trajectory_df.columns if col.startswith("Base")][0]
base_value = float(trajectory_df[base_column].iloc[-1])
st.caption(f"At your current Base trajectory, you reach {rp(base_value)} in {horizon} months.")

section_header("SECTION 3", "Macro News Feed", "Persistent themes to monitor without overtrading.")
news = pd.DataFrame(
    [
        {"Theme": "AI buildout", "Signal": "Sustained capex in chips, power, cooling, and cloud infrastructure.", "Implication for portfolio": "Supports US ETF beta and selected commodity-linked exposure, but avoid overconcentration."},
        {"Theme": "Commodity supercycle", "Signal": "Grid expansion, EVs, data centers, and energy security keep demand resilient.", "Implication for portfolio": "Keep tactical watchlists disciplined; gold and selected resource equities can diversify equity beta."},
        {"Theme": "USD strength/weakness", "Signal": "Dollar moves drive imported inflation, USD ETF translation, and global liquidity.", "Implication for portfolio": "USD cash provides optionality; rebalance rather than chase currency moves."},
        {"Theme": "Inflation trajectory", "Signal": "Sticky inflation favors real assets and higher nominal yields.", "Implication for portfolio": "SBN/ORI and gold can stabilize purchasing power while equities compound long term."},
        {"Theme": "Geopolitical fragmentation", "Signal": "Supply chains, sanctions, export controls, and resource nationalism remain active risks.", "Implication for portfolio": "Diversify across geographies, currencies, and asset classes; keep position sizes capped."},
        {"Theme": "Crypto institutional adoption", "Signal": "ETF flows and custody infrastructure improve access, but drawdowns remain severe.", "Implication for portfolio": "BTC can stay at 1–2%; avoid letting volatility dominate the portfolio."},
    ]
)
st.dataframe(news, width="stretch", hide_index=True)
st.caption(f"Last updated: {pd.Timestamp.now(tz='Asia/Jakarta').strftime('%Y-%m-%d %H:%M %Z')}")

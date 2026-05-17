import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from utils import hero, next_step_banner, setup_page, status_pill, terminal_layout

setup_page("Market Regime Indicator", "📈")
hero("Market Regime Indicator", "Simple risk-on/risk-off tape using live yfinance data and the S&P 500 proxy SPY by default.", "MODULE 4 // REGIME TAPE")

ticker = st.text_input("S&P 500 proxy ticker", value=st.session_state.get("regime_ticker", "SPY"))
st.session_state["regime_ticker"] = ticker

@st.cache_data(ttl=900)
def load_prices(symbol: str):
    return yf.download(symbol, period="1y", interval="1d", progress=False, auto_adjust=True)

data = load_prices(ticker)
if data.empty or "Close" not in data:
    st.error("No market data returned. Check ticker or yfinance connectivity.")
else:
    close = data["Close"]
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]
    ma50 = close.rolling(50).mean()
    latest_price = float(close.dropna().iloc[-1])
    latest_ma = float(ma50.dropna().iloc[-1])
    risk_on = latest_price > latest_ma
    signal = "RISK ON" if risk_on else "RISK OFF"
    delta = latest_price - latest_ma

    col1, col2, col3 = st.columns(3)
    col1.metric("Latest price", f"${latest_price:,.2f}")
    col2.metric("50-day moving average", f"${latest_ma:,.2f}")
    col3.markdown(status_pill(signal), unsafe_allow_html=True)
    col3.caption(f"${delta:,.2f} vs 50DMA")

    if risk_on:
        st.success("Risk-on: continue scheduled DCA into US ETF and selected IDX core positions. Avoid chasing tactical commodities beyond sizing rules.")
    else:
        st.error("Risk-off: keep DCA disciplined but route new cash first to SBN/ORI, USD cash, emergency reserves, or rebalance only if drift rules require it.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=close.index, y=close, name="Close", mode="lines"))
    fig.add_trace(go.Scatter(x=ma50.index, y=ma50, name="50DMA", mode="lines"))
    fig.update_layout(yaxis_title="USD")
    st.plotly_chart(terminal_layout(fig, f"{ticker.upper()} price vs 50DMA"), width="stretch")
    next_step_banner("Translate regime into rebalance discipline.", "Risk-on does not mean chase; risk-off does not mean panic. Use the Rebalancing Monitor to act only when drift breaks the band.", "pages/5_Rebalancing_Monitor.py", "Drift control")

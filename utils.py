"""Shared utilities for the WealthAccumulator Streamlit app."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

APP_NAME = "WealthAccumulator"
PROFILE = {
    "nationality": "Indonesian",
    "age": 25,
    "base": "Jakarta",
    "active_horizon": "3 years active, then low-touch mode",
    "risk": "Moderate-aggressive without margin",
}
ASSET_CLASSES = ["US ETFs", "IDX Stocks", "SBN/ORI Bonds", "Gold", "BTC", "USD Cash"]
COLORS = {
    "US ETFs": "#00A3FF",
    "IDX Stocks": "#00E5A8",
    "SBN/ORI Bonds": "#FFD166",
    "Gold": "#F5B041",
    "BTC": "#F7931A",
    "USD Cash": "#9AA4B2",
}
TERMINAL_COLORS = {
    "bg": "#050A12",
    "panel": "#0B1220",
    "panel_alt": "#0F1B2E",
    "border": "#23324A",
    "text": "#E6EDF7",
    "muted": "#8EA0B8",
    "accent": "#F6C343",
    "cyan": "#00A3FF",
    "green": "#00D084",
    "amber": "#FFB020",
    "red": "#FF4D4F",
    "blue": "#3B82F6",
}

MODULES = [
    {"title": "Dashboard", "icon": "🏠", "path": "app.py", "step": "00", "job": "Command center", "outcome": "See the whole system at once."},
    {"title": "Capital Sequencing Wizard", "icon": "🧭", "path": "pages/1_Capital_Sequencing_Wizard.py", "step": "01", "job": "Cashflow order", "outcome": "Know where the next rupiah goes."},
    {"title": "Portfolio Allocator", "icon": "🥧", "path": "pages/2_Portfolio_Allocator.py", "step": "02", "job": "Strategic allocation", "outcome": "Set the target mix before tactical views."},
    {"title": "Commodity Screener", "icon": "⛏️", "path": "pages/3_Commodity_Supercycle_Screener.py", "step": "03", "job": "Tactical watchlist", "outcome": "Filter themes without overtrading."},
    {"title": "Market Regime Indicator", "icon": "📈", "path": "pages/4_Market_Regime_Indicator.py", "step": "04", "job": "Risk throttle", "outcome": "Decide whether new cash leans growth or defense."},
    {"title": "Rebalancing Monitor", "icon": "⚖️", "path": "pages/5_Rebalancing_Monitor.py", "step": "05", "job": "Drift control", "outcome": "Buy underweights and trim overweights only when needed."},
    {"title": "Wealth Growth Simulator", "icon": "🚀", "path": "pages/6_Wealth_Growth_Simulator.py", "step": "06", "job": "Trajectory", "outcome": "Translate monthly actions into milestones."},
    {"title": "Pre-London Autopilot Checklist", "icon": "✈️", "path": "pages/7_Pre_London_Autopilot_Checklist.py", "step": "07", "job": "Low-touch handoff", "outcome": "Make the portfolio robust before departure."},
]

ACTION_STYLES = {
    "BUY": {"color": TERMINAL_COLORS["green"], "label": "BUY / Accumulate", "emoji": "▲"},
    "ADD": {"color": TERMINAL_COLORS["green"], "label": "ADD", "emoji": "▲"},
    "RISK ON": {"color": TERMINAL_COLORS["green"], "label": "RISK ON", "emoji": "●"},
    "HOLD": {"color": TERMINAL_COLORS["blue"], "label": "HOLD", "emoji": "▬"},
    "WATCH": {"color": TERMINAL_COLORS["amber"], "label": "WATCH", "emoji": "◆"},
    "TRIM": {"color": TERMINAL_COLORS["amber"], "label": "TRIM", "emoji": "▼"},
    "SELL": {"color": TERMINAL_COLORS["red"], "label": "SELL / Reduce", "emoji": "▼"},
    "AVOID": {"color": TERMINAL_COLORS["red"], "label": "AVOID", "emoji": "■"},
    "RISK OFF": {"color": TERMINAL_COLORS["red"], "label": "RISK OFF", "emoji": "●"},
    "HIGH": {"color": TERMINAL_COLORS["red"], "label": "HIGH", "emoji": "■"},
    "MEDIUM": {"color": TERMINAL_COLORS["amber"], "label": "MEDIUM", "emoji": "◆"},
    "LOW": {"color": TERMINAL_COLORS["green"], "label": "LOW", "emoji": "●"},
}


def setup_page(title: str, icon: str = "💰") -> None:
    st.set_page_config(page_title=f"{APP_NAME} | {title}", page_icon=icon, layout="wide")
    inject_theme()
    st.sidebar.title("WA Terminal")
    st.sidebar.caption("Bloomberg-inspired wealth cockpit")
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Profile: Indonesian, age 25, Jakarta-based, moderate-aggressive, "
        "no leverage, small-to-mid capital growing monthly."
    )
    render_workflow_sidebar(title)
    st.sidebar.markdown(
        """
        <div class="sidebar-rulebook">
            <div><b>Color language</b></div>
            <span class="dot green"></span> Buy / risk-on / healthy<br>
            <span class="dot amber"></span> Watch / caution / needs review<br>
            <span class="dot red"></span> Avoid / sell / risk-off<br>
            <span class="dot blue"></span> Hold / neutral
        </div>
        """,
        unsafe_allow_html=True,
    )


def inject_theme() -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --wa-bg: {TERMINAL_COLORS['bg']};
            --wa-panel: {TERMINAL_COLORS['panel']};
            --wa-panel-alt: {TERMINAL_COLORS['panel_alt']};
            --wa-border: {TERMINAL_COLORS['border']};
            --wa-text: {TERMINAL_COLORS['text']};
            --wa-muted: {TERMINAL_COLORS['muted']};
            --wa-accent: {TERMINAL_COLORS['accent']};
            --wa-green: {TERMINAL_COLORS['green']};
            --wa-amber: {TERMINAL_COLORS['amber']};
            --wa-red: {TERMINAL_COLORS['red']};
            --wa-blue: {TERMINAL_COLORS['blue']};
        }}
        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(0, 163, 255, 0.13), transparent 30rem),
                linear-gradient(135deg, #050A12 0%, #08111F 52%, #0E1728 100%);
            color: var(--wa-text);
        }}
        [data-testid="stSidebar"] {{ background: #050A12; border-right: 1px solid var(--wa-border); }}
        [data-testid="stSidebar"] * {{ color: var(--wa-text); }}
        h1, h2, h3 {{ letter-spacing: -0.025em; }}
        h1 {{ border-bottom: 1px solid rgba(246, 195, 67, 0.28); padding-bottom: 0.35rem; }}
        div[data-testid="stMetric"] {{
            background: linear-gradient(180deg, rgba(15, 27, 46, 0.96), rgba(7, 14, 25, 0.96));
            border: 1px solid var(--wa-border);
            border-left: 3px solid var(--wa-accent);
            border-radius: 12px;
            padding: 0.85rem 0.95rem;
            box-shadow: 0 12px 28px rgba(0,0,0,0.24);
        }}
        div[data-testid="stMetricLabel"] p {{ color: var(--wa-muted) !important; text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.73rem; }}
        div[data-testid="stMetricValue"] {{ color: var(--wa-text); font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
        div[data-testid="stDataFrame"] {{ border: 1px solid var(--wa-border); border-radius: 12px; overflow: hidden; }}
        .stAlert {{ border-radius: 12px; border: 1px solid var(--wa-border); }}
        .wa-hero, .wa-card, .wa-strip {{
            border: 1px solid var(--wa-border);
            border-radius: 14px;
            background: linear-gradient(180deg, rgba(15, 27, 46, 0.94), rgba(8, 17, 31, 0.94));
            box-shadow: 0 18px 44px rgba(0,0,0,0.28);
        }}
        .wa-hero {{ padding: 1.3rem 1.45rem; margin: 0.75rem 0 1.2rem; }}
        .wa-card {{ padding: 1rem; margin-bottom: 0.8rem; }}
        .wa-strip {{ padding: 0.75rem 1rem; border-left: 4px solid var(--wa-accent); }}
        .wa-kicker {{ color: var(--wa-accent); font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.76rem; letter-spacing: 0.12em; text-transform: uppercase; }}
        .wa-muted {{ color: var(--wa-muted); }}
        .wa-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 0.8rem; }}
        .wa-module-card {{ border: 1px solid var(--wa-border); border-radius: 14px; padding: 1rem; background: rgba(15, 27, 46, 0.78); min-height: 10.5rem; }}
        .wa-module-card.active {{ border-color: var(--wa-accent); box-shadow: 0 0 0 1px rgba(246, 195, 67, 0.30), 0 14px 36px rgba(0,0,0,0.22); }}
        .wa-module-step {{ color: var(--wa-accent); font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-weight: 800; font-size: 0.76rem; letter-spacing: 0.10em; }}
        .wa-module-title {{ margin: 0.28rem 0; font-weight: 800; font-size: 1rem; }}
        .wa-module-outcome {{ color: var(--wa-muted); font-size: 0.88rem; }}
        .wa-journey {{ margin: 0.75rem 0; padding: 0.7rem; border: 1px solid var(--wa-border); border-radius: 12px; background: rgba(15, 27, 46, 0.55); }}
        .wa-journey-row {{ display: flex; gap: 0.5rem; align-items: flex-start; padding: 0.4rem 0; border-bottom: 1px solid rgba(142,160,184,0.12); }}
        .wa-journey-row:last-child {{ border-bottom: 0; }}
        .wa-journey-row.active {{ color: var(--wa-accent); }}
        .wa-journey-step {{ min-width: 1.8rem; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-weight: 800; }}
        .wa-next-step {{ border: 1px solid rgba(246, 195, 67, 0.42); border-left: 4px solid var(--wa-accent); border-radius: 14px; padding: 1rem; background: rgba(246, 195, 67, 0.08); margin: 1rem 0; }}
        .status-pill {{
            display: inline-flex; align-items: center; gap: 0.35rem;
            padding: 0.18rem 0.56rem; border-radius: 999px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 0.78rem; font-weight: 800; letter-spacing: 0.04em;
            border: 1px solid currentColor;
            background: color-mix(in srgb, currentColor 13%, transparent);
        }}
        .sidebar-rulebook {{ border: 1px solid var(--wa-border); border-radius: 12px; padding: 0.8rem; background: rgba(15, 27, 46, 0.70); font-size: 0.82rem; line-height: 1.75; }}
        .dot {{ display: inline-block; width: 0.65rem; height: 0.65rem; border-radius: 99px; margin-right: 0.35rem; }}
        .green {{ background: var(--wa-green); }} .amber {{ background: var(--wa-amber); }} .red {{ background: var(--wa-red); }} .blue {{ background: var(--wa-blue); }}
        .urgency-high {{ color: var(--wa-red); font-weight: 800; }}
        .urgency-medium {{ color: var(--wa-amber); font-weight: 800; }}
        .urgency-low {{ color: var(--wa-green); font-weight: 800; }}
        button[kind="primary"], .stButton > button {{ border-radius: 10px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def rp(amount: float | int) -> str:
    sign = "-" if amount < 0 else ""
    return f"{sign}Rp {abs(float(amount)):,.0f}"


def get_module(title: str) -> dict[str, str]:
    return next((module for module in MODULES if module["title"] == title), MODULES[0])


def safe_page_link(path: str, label: str, *, sidebar: bool = False) -> bool:
    """Render a page link when Streamlit has multipage context; otherwise fail soft."""
    container = st.sidebar if sidebar else st
    if not hasattr(container, "page_link"):
        return False
    try:
        container.page_link(path, label=label)
    except KeyError:
        return False
    return True


def render_workflow_sidebar(active_title: str) -> None:
    """Render a persistent workflow map so pages feel like one connected product."""
    st.sidebar.markdown("### Operating workflow")
    for module in MODULES:
        label = f"{module['step']} {module['icon']} {module['job']}"
        if not safe_page_link(module["path"], label, sidebar=True):
            marker = "→" if module["title"] == active_title else "•"
            st.sidebar.write(f"{marker} {label}")

    active = get_module(active_title)
    st.sidebar.markdown(
        f"""
        <div class="wa-journey">
            <div class="wa-kicker">Current module</div>
            <div class="wa-journey-row active">
                <div class="wa-journey-step">{active['step']}</div>
                <div><b>{active['job']}</b><br><span class="wa-muted">{active['outcome']}</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("### Live assumptions")
    st.sidebar.caption(
        f"Capital {rp(st.session_state.get('total_capital', 150_000_000))} · "
        f"Monthly DCA {rp(st.session_state.get('sim_monthly', 8_000_000))} · "
        f"Risk {st.session_state.get('risk', 70)}/100"
    )


def workflow_overview(active_title: str | None = None) -> None:
    """Show the complete product map in the main canvas."""
    cards = []
    for module in MODULES:
        active_class = " active" if module["title"] == active_title else ""
        cards.append(
            f"""
            <div class="wa-module-card{active_class}">
                <div class="wa-module-step">{module['step']} · {module['icon']} {module['job']}</div>
                <div class="wa-module-title">{module['title']}</div>
                <div class="wa-module-outcome">{module['outcome']}</div>
            </div>
            """
        )
    st.markdown(f"<div class='wa-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)


def workflow_links() -> None:
    cols = st.columns(4)
    for idx, module in enumerate(MODULES):
        with cols[idx % 4]:
            if not safe_page_link(module["path"], f"{module['icon']} {module['job']}"):
                st.caption(f"{module['icon']} {module['job']}")


def next_step_banner(title: str, body: str, target_path: str | None = None, target_label: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="wa-next-step">
            <div class="wa-kicker">Connected next step</div>
            <b>{title}</b><br>
            <span class="wa-muted">{body}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if target_path and target_label:
        safe_page_link(target_path, f"Go to {target_label}")


def section_header(kicker: str, title: str, body: str | None = None) -> None:
    body_html = f"<div class='wa-muted'>{body}</div>" if body else ""
    st.markdown(
        f"""
        <div class="wa-strip">
            <div class="wa-kicker">{kicker}</div>
            <h3 style="margin: 0.1rem 0 0.15rem;">{title}</h3>
            {body_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, kicker: str = "WEALTHACCUMULATOR") -> None:
    st.markdown(
        f"""
        <div class="wa-hero">
            <div class="wa-kicker">{kicker}</div>
            <h1 style="border: 0; padding: 0; margin: 0.2rem 0;">{title}</h1>
            <div class="wa-muted" style="font-size: 1.02rem; max-width: 68rem;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_pill(status: str) -> str:
    style = ACTION_STYLES.get(str(status).upper(), {"color": TERMINAL_COLORS["muted"], "label": status, "emoji": "•"})
    return f"<span class='status-pill' style='color:{style['color']}'>{style['emoji']} {style['label']}</span>"


def styled_action_table(df: pd.DataFrame, action_column: str = "Action") -> pd.io.formats.style.Styler:
    def color_action(value: object) -> str:
        style = ACTION_STYLES.get(str(value).upper())
        if not style:
            return ""
        return f"color: {style['color']}; font-weight: 800;"

    return df.style.map(color_action, subset=[action_column])


def terminal_layout(fig: go.Figure, title: str | None = None) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,10,18,0.66)",
        font={"color": TERMINAL_COLORS["text"]},
        colorway=[TERMINAL_COLORS["green"], TERMINAL_COLORS["amber"], TERMINAL_COLORS["blue"], TERMINAL_COLORS["red"], TERMINAL_COLORS["cyan"]],
        margin={"l": 24, "r": 24, "t": 58 if title else 24, "b": 36},
        legend={"orientation": "h", "y": 1.02, "x": 0},
    )
    fig.update_xaxes(gridcolor="rgba(142,160,184,0.16)", zerolinecolor="rgba(142,160,184,0.20)")
    fig.update_yaxes(gridcolor="rgba(142,160,184,0.16)", zerolinecolor="rgba(142,160,184,0.20)")
    return fig


def allocation_from_profile(risk_score: int, horizon_months: int, usd_preference: int) -> dict[str, float]:
    """Return a target allocation tailored to the stated user profile."""
    risk = risk_score / 100
    usd = usd_preference / 100
    short_horizon = max(0, (36 - horizon_months) / 36)
    low_touch_penalty = 0.10 if horizon_months <= 12 else 0.0

    us_etfs = 30 + 25 * risk + 15 * usd - 8 * short_horizon
    idx = 18 + 18 * risk - 8 * usd - 10 * short_horizon - low_touch_penalty * 20
    bonds = 28 - 16 * risk + 16 * short_horizon + low_touch_penalty * 25
    gold = 10 + 3 * short_horizon
    btc = min(2, 0.5 + 2.0 * risk)
    usd_cash = 100 - (us_etfs + idx + bonds + gold + btc)

    raw = {
        "US ETFs": max(20, us_etfs),
        "IDX Stocks": max(5, idx),
        "SBN/ORI Bonds": max(10, bonds),
        "Gold": max(5, gold),
        "BTC": max(0, btc),
        "USD Cash": max(5, usd_cash),
    }
    raw["BTC"] = min(2, raw["BTC"])
    total = sum(raw.values())
    normalized = {asset: value / total * 100 for asset, value in raw.items()}
    if normalized["BTC"] > 2:
        excess = normalized["BTC"] - 2
        normalized["BTC"] = 2
        normalized["SBN/ORI Bonds"] += excess * 0.6
        normalized["USD Cash"] += excess * 0.4
    total = sum(normalized.values())
    return {asset: round(value / total * 100, 1) for asset, value in normalized.items()}


def allocation_table(allocation: dict[str, float], total_capital: float) -> pd.DataFrame:
    tiers = {
        "US ETFs": "Core compounder (VOO/QQQ sleeve)",
        "IDX Stocks": "Selective home-market satellite",
        "SBN/ORI Bonds": "IDR ballast and tuition runway",
        "Gold": "Currency/inflation hedge",
        "BTC": "Asymmetric option capped at ≤2%",
        "USD Cash": "Dry powder and FX hedge",
    }
    return pd.DataFrame(
        [
            {
                "Asset": asset,
                "Target %": weight,
                "Target Amount": rp(total_capital * weight / 100),
                "Role": tiers[asset],
            }
            for asset, weight in allocation.items()
        ]
    )


def pie_chart(allocation: dict[str, float], title: str) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(allocation.keys()),
                values=list(allocation.values()),
                hole=0.52,
                marker_colors=[COLORS.get(a, "#8892b0") for a in allocation],
                textinfo="label+percent",
                sort=False,
            )
        ]
    )
    return terminal_layout(fig, title)


def line_chart(df: pd.DataFrame, title: str) -> go.Figure:
    fig = go.Figure()
    for column in df.columns:
        if column != "Month":
            fig.add_trace(go.Scatter(x=df["Month"], y=df[column], mode="lines", name=column, line={"width": 3}))
    fig.update_layout(xaxis_title="Month", yaxis_title="Portfolio Value (IDR)")
    return terminal_layout(fig, title)

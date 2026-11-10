from __future__ import annotations

import os
import textwrap
import time
from datetime import date, datetime, timedelta
from html import escape
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage

from prompts import USER_PROMPT_FOR_MAIN_AGENT, WEDDING_PLANNER_AGENT_PROMPT
from models import get_model_name


APP_TITLE = "Dream Wedding Planner 💍"
MODEL_NAME = f"{get_model_name()} (Groq)"
REQUIRED_KEYS = ("GROQ_API_KEY", "TAVILY_API_KEY")

STYLE_OPTIONS = [
    "Modern",
    "Romantic",
    "Classic",
    "Garden",
    "Minimal",
    "Luxury",
    "Cultural fusion",
    "Destination",
    "Eco-conscious",
    "Black tie",
]

PRIORITY_OPTIONS = [
    "Venue shortlist",
    "Vendor research",
    "Budget allocation",
    "Guest experience",
    "Timeline",
    "Design direction",
    "Risk management",
    "Travel logistics",
]


load_dotenv()
st.set_page_config(page_title=APP_TITLE, page_icon="💍", layout="wide", initial_sidebar_state="expanded")


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #fce8ef;
            --ink-soft: #f7d1de;
            --muted: #e2a6bc;
            --line: #6b2440;
            --line-strong: #8c2f55;
            --panel: #31111f;
            --surface: #3d1627;
            --surface-strong: #4f1c34;
            --sidebar: #1d0711;
            --sidebar-field: #12040a;
            --pink-primary: #ff5c8d;
            --pink-hover: #ff7aa3;
            --gold: #f3cf65;
            --success: #2ea07d;
            --danger: #e06d67;
            --shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes floatBadge {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-4px); }
            100% { transform: translateY(0px); }
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 10% -10%, rgba(140, 47, 85, 0.35), transparent 30rem),
                linear-gradient(180deg, #240b15 0%, var(--surface) 24rem, var(--surface) 100%);
            color: var(--ink);
            animation: fadeIn 0.6s ease-out;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 1240px;
            padding-top: 1.2rem;
            padding-bottom: 3rem;
        }

        .app-header {
            align-items: center;
            background: linear-gradient(135deg, #3d1627 0%, #521c35 52%, #6b2440 100%);
            border: 1px solid var(--line);
            border-top: 4px solid var(--pink-primary);
            border-radius: 12px;
            box-shadow: var(--shadow);
            display: grid;
            gap: 1.25rem;
            grid-template-columns: minmax(0, 1fr) auto;
            padding: 1.5rem 1.75rem 1.4rem;
            margin-bottom: 1.5rem;
            animation: fadeIn 0.5s ease-out;
        }

        .app-kicker {
            color: var(--gold);
            font-size: 0.85rem;
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: 0.08rem;
            margin-bottom: 0.35rem;
        }

        .app-title {
            color: #ffffff;
            font-size: 2.45rem;
            font-weight: 800;
            line-height: 1.1;
            margin: 0 0 0.45rem;
        }

        .app-subtitle {
            color: var(--ink-soft);
            font-size: 1.02rem;
            line-height: 1.5;
            max-width: 780px;
            margin: 0;
        }

        .header-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: flex-end;
            max-width: 320px;
        }

        .header-chip {
            background: rgba(255, 92, 141, 0.18);
            border: 1px solid rgba(255, 92, 141, 0.35);
            border-radius: 999px;
            color: #ff99b8;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.3rem 0.75rem;
            white-space: nowrap;
            animation: floatBadge 3s ease-in-out infinite;
        }

        .summary-grid {
            display: grid;
            gap: 1rem;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin: 0 0 1.25rem;
        }

        .summary-card {
            background: rgba(49, 17, 31, 0.95);
            border: 1px solid var(--line);
            border-radius: 10px;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.3);
            min-height: 6rem;
            padding: 1rem 1.05rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .summary-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.45);
        }

        .summary-card .label {
            color: var(--muted);
            display: block;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }

        .summary-card .value {
            color: var(--pink-primary);
            display: block;
            font-size: 1.4rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 0.2rem;
        }

        .summary-card .note {
            color: var(--ink-soft);
            display: block;
            font-size: 0.84rem;
            line-height: 1.3;
        }

        .section-label {
            color: #ffffff;
            font-weight: 800;
            font-size: 1.1rem;
            margin: 0 0 0.75rem;
        }

        .field-group-title {
            color: var(--pink-primary);
            font-size: 0.85rem;
            font-weight: 800;
            margin: 0.4rem 0 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.05rem;
        }

        [data-testid="stForm"] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 12px;
            box-shadow: var(--shadow);
            padding: 1.25rem 1.3rem 1.35rem;
        }

        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label,
        [data-testid="stForm"] label,
        [data-testid="stForm"] p {
            color: #ffffff !important;
            font-weight: 650;
        }

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stTextArea textarea {
            background: #240b15 !important;
            border: 1px solid var(--line-strong) !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            color: #ffffff !important;
        }

        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus,
        .stTextArea textarea:focus {
            border-color: var(--pink-primary) !important;
            box-shadow: 0 0 0 3px rgba(255, 92, 141, 0.2) !important;
        }

        div[data-baseweb="select"] > div {
            background: #240b15 !important;
            border-color: var(--line-strong) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            min-height: 2.7rem;
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] svg {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        div[data-baseweb="tag"] {
            background: rgba(255, 92, 141, 0.2) !important;
            border: 1px solid rgba(255, 92, 141, 0.4) !important;
            border-radius: 6px !important;
        }

        div[data-baseweb="tag"] span {
            color: #ff99b8 !important;
            font-weight: 700 !important;
        }

        .stSlider [data-baseweb="slider"] [role="slider"] {
            background: var(--pink-primary) !important;
            border-color: #ffffff !important;
        }

        .stSlider [data-baseweb="slider"] > div {
            color: var(--pink-primary) !important;
        }

        [data-testid="stSidebar"] {
            background: var(--sidebar);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #fce8ef !important;
        }

        [data-testid="stSidebar"] .stTextInput input {
            background: var(--sidebar-field) !important;
            border-color: rgba(255, 255, 255, 0.18) !important;
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.15);
        }

        .side-panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 12px;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.3);
            padding: 1.15rem 1.25rem;
            margin-bottom: 1.15rem;
        }

        .side-panel h3 {
            color: #ffffff;
            font-size: 1.05rem;
            margin: 0 0 0.85rem;
        }

        .side-panel p {
            color: var(--muted);
            font-size: 0.94rem;
            line-height: 1.45;
            margin: 0 0 0.75rem;
        }

        .lens-grid {
            display: grid;
            gap: 0.75rem;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            margin-bottom: 0.85rem;
        }

        .lens-item {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.65rem 0.75rem;
        }

        .lens-item span {
            color: var(--muted);
            display: block;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .lens-item strong {
            color: #ffffff;
            display: block;
            font-size: 0.98rem;
            line-height: 1.25;
            margin-top: 0.15rem;
        }

        .chip-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
        }

        .soft-chip {
            background: rgba(243, 207, 101, 0.15);
            border: 1px solid rgba(243, 207, 101, 0.3);
            border-radius: 999px;
            color: #f7de94;
            font-size: 0.78rem;
            font-weight: 750;
            padding: 0.25rem 0.65rem;
        }

        .flow-row {
            border-top: 1px solid var(--line);
            padding: 0.75rem 0;
        }

        .flow-row:first-of-type {
            border-top: 0;
            padding-top: 0;
        }

        .flow-row strong {
            color: #ffffff;
            display: block;
            font-size: 0.95rem;
            margin-bottom: 0.15rem;
        }

        .flow-row span {
            color: var(--muted);
            display: block;
            font-size: 0.86rem;
            line-height: 1.35;
        }

        .key-row {
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
        }

        .key-row span:first-child {
            color: rgba(255, 232, 239, 0.85) !important;
            font-size: 0.92rem;
        }

        .badge {
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 700;
            padding: 0.16rem 0.6rem;
        }

        .badge-ready {
            background: rgba(46, 160, 125, 0.25);
            color: #5fe3c3 !important;
        }

        .badge-missing {
            background: rgba(224, 109, 103, 0.25);
            color: #ffb6ad !important;
        }

        div[data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 0.95rem 1.05rem;
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] p {
            color: var(--ink-soft) !important;
            font-weight: 650;
        }

        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] div {
            color: var(--pink-primary) !important;
        }

        .result-shell {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 12px;
            box-shadow: var(--shadow);
            padding: 1.2rem 1.3rem;
            margin-top: 0.85rem;
            color: #ffffff;
        }

        .result-title-row {
            align-items: center;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: space-between;
            margin: 0.4rem 0 0.85rem;
        }

        .result-title-row h3 {
            color: #ffffff;
            font-size: 1.15rem;
            margin: 0;
        }

        .result-title-row span {
            color: var(--muted);
            font-size: 0.86rem;
            font-weight: 650;
        }

        .empty-result {
            background: var(--panel);
            border: 1px dashed var(--line-strong);
            border-radius: 12px;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.3);
            color: var(--muted);
            padding: 1.6rem;
            text-align: center;
        }

        .empty-result strong {
            color: #ffffff;
            display: block;
            font-size: 1.05rem;
            margin-bottom: 0.35rem;
        }

        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stFormSubmitButton"] button {
            background: #3d1627;
            border: 1px solid var(--line-strong);
            border-radius: 8px;
            color: #ffffff;
            font-weight: 700;
            min-height: 2.8rem;
            transition: all 0.2s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: var(--pink-primary);
            color: var(--pink-primary);
            background: #4f1c34;
        }

        div[data-testid="stFormSubmitButton"] button {
            background: var(--pink-primary) !important;
            border-color: var(--pink-primary) !important;
            color: #ffffff !important;
        }

        div[data-testid="stFormSubmitButton"] button:hover {
            background: var(--pink-hover) !important;
            border-color: var(--pink-hover) !important;
        }

        div[data-testid="stFormSubmitButton"] button:disabled {
            background: #522135 !important;
            border-color: #522135 !important;
            color: #a37c8e !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.2);
            color: #ffffff;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.35);
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_default_form_values() -> dict[str, Any]:
    return {
        "couple_name": "Amira & Noah 💍",
        "wedding_location": "Cairo, Egypt",
        "wedding_date": date.today() + timedelta(days=240),
        "guest_count": 150,
        "currency": "USD",
        "budget_range": (40000, 70000),
        "ceremony_type": "Ceremony and reception",
        "wedding_styles": ["Romantic", "Luxury", "Garden"],
        "planning_priorities": ["Venue shortlist", "Vendor research", "Budget allocation", "Design direction"],
        "tone": "Elegant and practical",
        "must_haves": (
            "Romantic garden setup, gorgeous floral arches, live violinist, "
            "smooth guest coordination, and cinematic photography."
        ),
        "constraints": (
            "Keep the design sophisticated and dreamy while maintaining a balanced budget."
        ),
        "traditions": (
            "Blend a romantic western entrance with warm family celebration customs and special spotlight dances."
        ),
    }


def load_sample_values() -> None:
    for key, value in get_default_form_values().items():
        st.session_state[key] = value


def initialize_state() -> None:
    st.session_state.setdefault("plans", [])
    for key, value in get_default_form_values().items():
        st.session_state.setdefault(key, value)


def read_streamlit_secret(name: str) -> str | None:
    try:
        value = st.secrets.get(name)
    except Exception:
        return None
    return str(value) if value else None


def hydrate_env_from_secrets() -> None:
    for key in REQUIRED_KEYS:
        if os.getenv(key):
            continue
        secret_value = read_streamlit_secret(key)
        if secret_value:
            os.environ[key] = secret_value


def apply_key_overrides(groq_key: str, tavily_key: str) -> None:
    if groq_key.strip():
        os.environ["GROQ_API_KEY"] = groq_key.strip()
    if tavily_key.strip():
        os.environ["TAVILY_API_KEY"] = tavily_key.strip()


def key_is_ready(name: str) -> bool:
    return bool(os.getenv(name))


def format_budget_range(budget_range: tuple[int, int], currency: str) -> str:
    low, high = budget_range
    return f"{currency} {low // 1000}k - {high // 1000}k"


def format_budget_per_guest(budget_range: tuple[int, int], guest_count: int) -> str:
    if guest_count <= 0:
        return "Not set"
    low, high = budget_range
    average_budget = (low + high) / 2
    return f"{average_budget / guest_count:,.0f} per guest"


def format_days_until(target_date: date) -> str:
    days = (target_date - date.today()).days
    if days == 0:
        return "Today 🥂"
    if days == 1:
        return "Tomorrow ✨"
    if days < 0:
        return f"{abs(days)} days ago"
    return f"{days} days out"


def format_list_preview(items: list[str], fallback: str = "Flexible") -> str:
    if not items:
        return fallback
    preview = items[:2]
    suffix = f" +{len(items) - len(preview)}" if len(items) > len(preview) else ""
    return f"{', '.join(preview)}{suffix}"


def render_key_badge(label: str, ready: bool) -> None:
    status_class = "badge-ready" if ready else "badge-missing"
    status_text = "Ready" if ready else "Missing"
    st.markdown(
        f"""
        <div class="key-row">
            <span>{label}</span>
            <span class="badge {status_class}">{status_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="app-header">
            <div>
                <div class="app-kicker">✨ AI Wedding Studio ✨</div>
                <h1 class="app-title">Dream Wedding Planner 💐</h1>
                <p class="app-subtitle">
                    Craft your perfect wedding story with intelligent multi-agent planning, 
                    live vendor research, and exquisite design curation.
                </p>
            </div>
            <div class="header-chips">
                <span class="header-chip">💍 Multi-Agent Flow</span>
                <span class="header-chip">🌸 Live Search</span>
                <span class="header-chip">✨ Instant Export</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_summary(runtime_ready: bool) -> None:
    payload = get_form_payload()
    status_value = "Ready 💖" if runtime_ready else "Keys needed"
    status_note = "Agents ready to run" if runtime_ready else "Add API keys in sidebar"
    guest_note = f"{payload['guest_count']:,} guests"

    st.markdown(
        f"""
        <div class="summary-grid">
            <div class="summary-card">
                <span class="label">Runtime Status</span>
                <span class="value">{status_value}</span>
                <span class="note">{status_note}</span>
            </div>
            <div class="summary-card">
                <span class="label">Countdown</span>
                <span class="value">{format_days_until(payload["wedding_date"])}</span>
                <span class="note">{payload["wedding_date"].strftime("%b %d, %Y")}</span>
            </div>
            <div class="summary-card">
                <span class="label">Budget Estimate</span>
                <span class="value">{format_budget_range(payload["budget_range"], payload["currency"])}</span>
                <span class="note">{format_budget_per_guest(payload["budget_range"], payload["guest_count"])}</span>
            </div>
            <div class="summary-card">
                <span class="label">Primary Focus</span>
                <span class="value">{escape(format_list_preview(payload["planning_priorities"], "Balanced"))}</span>
                <span class="note">{guest_note}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> bool:
    hydrate_env_from_secrets()

    with st.sidebar:
        st.markdown("### 🛠️ Runtime & Keys")
        groq_override = st.text_input("Groq API key", type="password", key="groq_key_override")
        tavily_override = st.text_input("Tavily API key", type="password", key="tavily_key_override")
        apply_key_overrides(groq_override, tavily_override)

        groq_ready = key_is_ready("GROQ_API_KEY")
        tavily_ready = key_is_ready("TAVILY_API_KEY")
        render_key_badge("Groq", groq_ready)
        render_key_badge("Tavily", tavily_ready)

        st.divider()
        st.markdown("### 💌 Demo Controls")
        st.button("Load sample brief", use_container_width=True, on_click=load_sample_values)

        if st.button("Refresh agent clients", use_container_width=True):
            load_agent_dependencies.clear()
            st.toast("Agent clients refreshed successfully! ✨")

        st.divider()
        st.markdown("### 📂 Saved Plans")
        if st.session_state.plans:
            for plan in st.session_state.plans[:4]:
                st.caption(f"💍 {plan['title']} | {plan['created_at']}")
        else:
            st.caption("No saved plans yet.")

    return groq_ready and tavily_ready


@st.cache_resource(show_spinner=False)
def load_agent_dependencies():
    from agent import delegate_to_subagent1, delegate_to_subagent2
    from models import get_llm, llm

    model = get_llm() if get_llm is not None else llm
    return model, [delegate_to_subagent1, delegate_to_subagent2]


def build_requirements(payload: dict[str, Any]) -> str:
    budget_low, budget_high = payload["budget_range"]
    styles = ", ".join(payload["wedding_styles"]) or "Flexible"
    priorities = ", ".join(payload["planning_priorities"]) or "Balanced planning support"

    return textwrap.dedent(
        f"""
        Couple or event name: {payload["couple_name"]}
        Wedding location: {payload["wedding_location"]}
        Target date: {payload["wedding_date"].strftime("%B %d, %Y")}
        Guest count: {payload["guest_count"]}
        Budget range: {payload["currency"]} {budget_low:,} to {budget_high:,}
        Event scope: {payload["ceremony_type"]}
        Preferred style: {styles}
        Planning priorities: {priorities}
        Planner tone: {payload["tone"]}

        Must-haves:
        {payload["must_haves"].strip() or "None specified."}

        Constraints and sensitivities:
        {payload["constraints"].strip() or "None specified."}

        Cultural, family, or ceremonial details:
        {payload["traditions"].strip() or "None specified."}

        Requested final plan:
        - Executive summary with the planning concept.
        - Venue and vendor research recommendations with clear rationale.
        - Budget allocation by category.
        - Timeline from now through wedding day.
        - Risks, tradeoffs, and open questions for the couple.
        """
    ).strip()


def get_form_payload() -> dict[str, Any]:
    keys = [
        "couple_name",
        "wedding_location",
        "wedding_date",
        "guest_count",
        "currency",
        "budget_range",
        "ceremony_type",
        "wedding_styles",
        "planning_priorities",
        "tone",
        "must_haves",
        "constraints",
        "traditions",
    ]
    return {key: st.session_state[key] for key in keys}


def render_brief_form(runtime_ready: bool) -> bool:
    st.markdown('<div class="section-label">📋 Wedding Brief & Vision</div>', unsafe_allow_html=True)

    with st.form("wedding_brief_form"):
        st.markdown('<div class="field-group-title">Couple & Venue</div>', unsafe_allow_html=True)
        st.text_input("Couple or project name", key="couple_name")

        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Location", key="wedding_location")
            st.number_input("Guest count", min_value=10, max_value=1000, step=10, key="guest_count")
        with col_b:
            st.date_input("Target date", min_value=date.today(), key="wedding_date")
            st.selectbox(
                "Event scope",
                [
                    "Ceremony and reception",
                    "Reception only",
                    "Destination wedding",
                    "Multi-day wedding",
                    "Elopement plus celebration",
                ],
                key="ceremony_type",
            )

        st.markdown('<div class="field-group-title">Budget & Aesthetic</div>', unsafe_allow_html=True)
        budget_col, tone_col = st.columns([1.1, 1])
        with budget_col:
            st.selectbox("Currency", ["USD", "EUR", "GBP", "CAD", "AUD"], key="currency")
            st.slider(
                "Budget range",
                min_value=5000,
                max_value=250000,
                step=5000,
                key="budget_range",
            )
        with tone_col:
            st.selectbox(
                "Planner tone",
                ["Elegant and practical", "Luxury editorial", "Budget-conscious", "Warm and family-centered"],
                key="tone",
            )
            st.multiselect("Style direction", STYLE_OPTIONS, key="wedding_styles")

        st.markdown('<div class="field-group-title">Priorities & Special Notes</div>', unsafe_allow_html=True)
        st.multiselect("Planning priorities", PRIORITY_OPTIONS, key="planning_priorities")

        notes_a, notes_b = st.columns(2)
        with notes_a:
            st.text_area("Must-haves", height=124, key="must_haves")
            st.text_area("Traditions and family details", height=104, key="traditions")
        with notes_b:
            st.text_area("Constraints", height=244, key="constraints")

        return st.form_submit_button(
            "✨ Generate Dream Wedding Plan ✨",
            type="primary",
            use_container_width=True,
            disabled=not runtime_ready,
        )


def invoke_planner(requirements: str) -> tuple[str, float]:
    started = time.perf_counter()
    planner_model, delegation_tools = load_agent_dependencies()
    system_prompt = WEDDING_PLANNER_AGENT_PROMPT.format(requirements=requirements)
    main_agent = create_agent(
        model=planner_model,
        tools=delegation_tools,
        name="MainWeddingPlannerAgent",
        system_prompt=system_prompt,
    )
    response = main_agent.invoke({"messages": [HumanMessage(content=USER_PROMPT_FOR_MAIN_AGENT)]})
    content = response["messages"][-1].content
    return content, time.perf_counter() - started


def create_download_name(title: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in title)
    slug = "-".join(part for part in slug.split("-") if part)
    return f"{slug[:44] or 'wedding-plan'}.md"


def save_plan(title: str, requirements: str, content: str, duration: float) -> None:
    st.session_state.plans.insert(
        0,
        {
            "title": title,
            "requirements": requirements,
            "content": content,
            "duration": duration,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    )


def render_project_snapshot() -> None:
    st.markdown(
        f"""
        <div class="side-panel">
            <h3>🤖 Agent Architecture</h3>
            <div class="flow-row">
                <strong>MainWeddingPlannerAgent</strong>
                <span>Synthesizes the complete wedding master strategy.</span>
            </div>
            <div class="flow-row">
                <strong>SubAgent1 & SubAgent2</strong>
                <span>Handles live venue & vendor research simultaneously.</span>
            </div>
            <div class="flow-row">
                <strong>Tavily Search</strong>
                <span>Fetches real-time market pricing and availability.</span>
            </div>
            <div class="flow-row">
                <strong>{MODEL_NAME}</strong>
                <span>Powers intelligent reasoning and polished coordination.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_planning_lens() -> None:
    payload = get_form_payload()
    style_chips = "".join(
        f'<span class="soft-chip">{escape(style)}</span>' for style in payload["wedding_styles"]
    ) or '<span class="soft-chip">Flexible style</span>'
    priority_chips = "".join(
        f'<span class="soft-chip">{escape(priority)}</span>' for priority in payload["planning_priorities"]
    ) or '<span class="soft-chip">Balanced plan</span>'

    st.markdown(
        f"""
        <div class="side-panel">
            <h3>💍 Wedding Vision Lens</h3>
            <div class="lens-grid">
                <div class="lens-item">
                    <span>Couple</span>
                    <strong>{escape(payload["couple_name"] or "Untitled")}</strong>
                </div>
                <div class="lens-item">
                    <span>Location</span>
                    <strong>{escape(payload["wedding_location"] or "Not set")}</strong>
                </div>
                <div class="lens-item">
                    <span>Scope</span>
                    <strong>{escape(payload["ceremony_type"])}</strong>
                </div>
                <div class="lens-item">
                    <span>Countdown</span>
                    <strong>{format_days_until(payload["wedding_date"])}</strong>
                </div>
            </div>
            <p>Style direction</p>
            <div class="chip-list">{style_chips}</div>
            <p style="margin-top:0.8rem;">Planning priorities</p>
            <div class="chip-list">{priority_chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_results() -> None:
    if not st.session_state.plans:
        st.markdown(
            """
            <div class="empty-result">
                <strong>No wedding plan generated yet 🌸</strong>
                Complete your brief on the left and click generate to create your custom wedding masterplan.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    latest = st.session_state.plans[0]

    st.markdown(
        f"""
        <div class="result-title-row">
            <h3>💍 {escape(latest["title"])}</h3>
            <span>Generated {escape(latest["created_at"])}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_a, metric_b, metric_c = st.columns(3)
    metric_a.metric("Runtime", f"{latest['duration']:.1f}s")
    metric_b.metric("Brief Words", f"{len(latest['requirements'].split()):,}")
    metric_c.metric("Saved Runs", str(len(st.session_state.plans)))

    plan_tab, requirements_tab, architecture_tab = st.tabs(["✨ Wedding Masterplan", "📋 Input Brief", "⚡ Architecture"])

    with plan_tab:
        st.markdown('<div class="result-shell">', unsafe_allow_html=True)
        st.markdown(latest["content"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            "📥 Download Plan (.md)",
            data=latest["content"],
            file_name=create_download_name(latest["title"]),
            mime="text/markdown",
            use_container_width=True,
        )

    with requirements_tab:
        st.code(latest["requirements"], language="markdown")

    with architecture_tab:
        st.markdown(
            """
            ```text
            Streamlit UI (Burgundy & Pink Theme)
                -> structured wedding brief
                -> WEDDING_PLANNER_AGENT_PROMPT
                -> MainWeddingPlannerAgent
                    -> delegate_to_subagent1(query)
                        -> SubAgent1 -> Tavily search_web
                    -> delegate_to_subagent2(query)
                        -> SubAgent2 -> Tavily search_web
                -> synthesized wedding masterplan
            ```
            """
        )


def handle_submission() -> None:
    payload = get_form_payload()
    requirements = build_requirements(payload)
    title = payload["couple_name"].strip() or "Wedding plan"

    with st.status("💍 Running wedding planner agents...", expanded=True) as status:
        st.write("✨ Preparing the main planner prompt & style guidelines.")
        st.write("🤖 Loading agent dependencies and Tavily tools.")
        try:
            st.write("💐 Delegating live research and crafting your dream plan.")
            content, duration = invoke_planner(requirements)
        except Exception as exc:
            status.update(label="Planner run failed ❌", state="error")
            st.error("The planner could not complete the run. Check API keys, quotas, and Tavily access.")
            with st.expander("Technical details"):
                st.code(str(exc))
            return

        save_plan(title=title, requirements=requirements, content=content, duration=duration)
        status.update(label="✨ Your dream wedding plan is ready! 🥂", state="complete")


def main() -> None:
    inject_css()
    initialize_state()
    render_header()

    runtime_ready = render_sidebar()

    if not runtime_ready:
        st.warning("⚠️ Add Groq and Tavily API keys in `.env`, Streamlit secrets, or the sidebar to run the live agents.")

    render_dashboard_summary(runtime_ready=runtime_ready)

    left_col, right_col = st.columns([1.35, 0.8], gap="large")

    with left_col:
        submitted = render_brief_form(runtime_ready=runtime_ready)

    with right_col:
        render_planning_lens()
        render_project_snapshot()

    if submitted:
        handle_submission()

    st.markdown('<div class="section-label" style="margin-top: 1.5rem;">🌟 Latest Wedding Masterplan</div>', unsafe_allow_html=True)
    render_results()


if __name__ == "__main__":
    main()
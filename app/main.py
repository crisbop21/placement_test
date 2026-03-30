"""Streamlit entry point — language toggle and session state initialization."""

import json
import os
import streamlit as st

from config import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

# Must be the first Streamlit command
st.set_page_config(
    page_title="Sustainability Diagnostic",
    page_icon="🌿",
    layout="centered",
)


def load_i18n(lang: str) -> dict:
    """Load i18n strings for the given language."""
    i18n_path = os.path.join(os.path.dirname(__file__), "..", "i18n", f"{lang}.json")
    with open(i18n_path, encoding="utf-8") as f:
        return json.load(f)


def t(key: str) -> str:
    """Translate a key using the current language strings."""
    strings = st.session_state.get("i18n_strings", {})
    return strings.get(key, key)


def init_session_state() -> None:
    """Initialize all session state keys with defaults."""
    defaults = {
        "lang": DEFAULT_LANGUAGE,
        "i18n_strings": load_i18n(DEFAULT_LANGUAGE),
        "profile": {},
        "answers": {},
        "current_question": 0,
        "questions": [],
        "scores": {},
        "recommendations": [],
        "session_id": None,
        "pdf_ready": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_language_toggle() -> None:
    """Render the language switcher in the sidebar."""
    lang = st.sidebar.selectbox(
        t("language_label"),
        options=SUPPORTED_LANGUAGES,
        index=SUPPORTED_LANGUAGES.index(st.session_state["lang"]),
        format_func=lambda x: "Español" if x == "es" else "English",
    )
    if lang != st.session_state["lang"]:
        st.session_state["lang"] = lang
        st.session_state["i18n_strings"] = load_i18n(lang)
        st.rerun()


# --- Main app ---
init_session_state()
render_language_toggle()

st.title(t("app_title"))
st.markdown(t("welcome_message"))

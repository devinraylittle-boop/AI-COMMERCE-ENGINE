import logging

import streamlit as st
from sqlalchemy import inspect

from ai_commerce_engine.config import get_settings
from ai_commerce_engine.db import SessionLocal, engine
from ai_commerce_engine.services.audit import record_audit
from ai_commerce_engine.ui.pages import PAGES


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    st.set_page_config(page_title="AI Commerce Engine", page_icon="◈", layout="wide")
    st.markdown(
        """
        <style>
        .block-container {padding-top: 2rem; max-width: 1500px;}
        [data-testid="stMetric"] {
            background: #f7f8fa; border: 1px solid #e6e8ec;
            padding: 1rem; border-radius: .75rem;
        }
        @media (max-width: 700px) {.block-container {padding: 1rem;} h1 {font-size: 1.9rem;}}
        </style>
    """,
        unsafe_allow_html=True,
    )
    if not inspect(engine).has_table("products"):
        st.error("Database schema is missing. Run `alembic upgrade head` before starting the app.")
        st.stop()
    with st.sidebar:
        st.caption("AI COMMERCE ENGINE")
        st.write("Evidence before investment")
        selected = st.radio("Navigate", list(PAGES), label_visibility="collapsed")
        st.divider()
        st.caption("Human approval required for consequential actions.")
    with SessionLocal() as session:
        try:
            PAGES[selected](session)
        except Exception as exc:
            session.rollback()
            logging.exception("Unhandled UI error")
            record_audit(
                session,
                event_type="error",
                entity_type="application",
                entity_id=None,
                actor="system",
                action="unhandled_ui_error",
                details=type(exc).__name__,
            )
            session.commit()
            st.error("The operation could not be completed. Review the audit log and local logs.")


if __name__ == "__main__":
    main()

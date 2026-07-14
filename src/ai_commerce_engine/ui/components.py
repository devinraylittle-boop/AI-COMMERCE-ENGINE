from decimal import Decimal

import streamlit as st


def money_label(value: Decimal | float | int) -> str:
    return f"${float(value):,.2f}"


def empty_state(message: str) -> None:
    st.info(message, icon=":material/info:")


def page_header(title: str, description: str) -> None:
    st.title(title)
    st.caption(description)


import streamlit as st

from column_mapper import render_column_mapper
from dashboard import inject_custom_css, render_dashboard
from landing import render_landing


st.set_page_config(
    page_title="Plug-and-Play Analytics Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session() -> None:
    """Create the session keys used by the landing and mapping flows."""
    defaults = {
        "raw_df": None,
        "mapped_df": None,
        "data_ready": False,
        "needs_mapping": False,
        "data_source_label": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def main() -> None:
    """Route users from landing screen to mapper to dashboard."""
    init_session()
    inject_custom_css()

    if not st.session_state.data_ready and st.session_state.raw_df is None:
        render_landing()
        return

    if st.session_state.needs_mapping:
        render_column_mapper(st.session_state.raw_df)
        return

    render_dashboard(st.session_state.mapped_df)


if __name__ == "__main__":
    main()

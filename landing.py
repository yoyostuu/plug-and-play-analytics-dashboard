from __future__ import annotations

import os

import streamlit as st

from data_loader import load_demo_dataset, load_mysql_data, load_uploaded_file


def render_landing() -> None:
    """Render the startup-style product landing screen."""
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">Built for small and medium businesses</div>
          <h1>Plug-and-Play Analytics Dashboard</h1>
          <p>Upload your business data and get instant insights in seconds.</p>
          <p style="font-size:.94rem;margin-top:.55rem;">Optimized for small and medium business datasets. Recommended file size: under 100MB for best performance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    demo_col, upload_col = st.columns(2)
    with demo_col:
        _card("View Demo", "Load a ready-to-analyze ecommerce dataset automatically.", "01")
        if st.button("▶ Explore Demo Dashboard", type="primary", use_container_width=True):
            with st.spinner("Preparing demo insights..."):
                _stage_raw_data(load_demo_dataset(), "Demo ecommerce dataset")
    with upload_col:
        _card("Upload My Business Data", "Bring CSV, Excel, JSON, TSV, or Parquet data.", "02")
        uploaded = st.file_uploader("Upload business data", type=["csv", "xlsx", "xls", "json", "parquet", "tsv"], label_visibility="collapsed")
        if st.button("📂 Upload Business Data", use_container_width=True):
            if uploaded is None:
                st.warning("Choose a file to continue. For best performance, keep it under 100MB.")
            else:
                try:
                    with st.spinner("Reading your file and preparing column mapping..."):
                        _stage_raw_data(load_uploaded_file(uploaded.name, uploaded.getvalue()), f"Uploaded: {uploaded.name}")
                except Exception as exc:
                    st.error(f"Upload failed: {exc}")
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Connect MySQL Database"):
        host = st.text_input("Host", value=os.getenv("MYSQL_HOST", "localhost"))
        port = st.number_input("Port", value=int(os.getenv("MYSQL_PORT", "3306")), step=1)
        user = st.text_input("Username", value=os.getenv("MYSQL_USER", "root"))
        password = st.text_input("Password", value=os.getenv("MYSQL_PASSWORD", ""), type="password")
        database = st.text_input("Database", value=os.getenv("MYSQL_DATABASE", "ecommerce_analytics"))
        if st.button("Connect", use_container_width=True):
            try:
                with st.spinner("Connecting securely to MySQL..."):
                    _stage_raw_data(load_mysql_data(host, int(port), user, password, database), "MySQL database")
            except Exception as exc:
                st.error(f"MySQL connection failed: {exc}")


def _stage_raw_data(df, label: str) -> None:
    """Store incoming data and advance to the mapper."""
    if df.empty:
        st.error("The selected source returned no rows. Try another dataset.")
        return
    st.session_state.raw_df = df
    st.session_state.mapped_df = None
    st.session_state.needs_mapping = True
    st.session_state.data_ready = False
    st.session_state.data_source_label = label
    st.rerun()


def _card(title: str, body: str, step: str) -> None:
    """Render one premium landing option card."""
    st.markdown(
        f"""
        <div class="glass" style="padding:1.35rem;min-height:170px;margin-bottom:1rem;">
            <div class="eyebrow">Option {step}</div>
            <div class="metric-value" style="font-size:1.65rem;">{title}</div>
            <div class="section-copy" style="font-size:.95rem;margin-top:.5rem;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

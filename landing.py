from __future__ import annotations

import os

import streamlit as st

from data_loader import load_demo_dataset, load_mysql_data, load_uploaded_file
from currency_helper import render_currency_selector, CURRENCIES


def render_landing() -> None:
    """Render the startup-style product landing screen."""
    _, tcol = st.columns([8, 2])
    with tcol:
        current_theme = st.session_state.get("app_theme", "Light")
        app_theme = st.selectbox("🎨 Theme", ["Light", "Dark"], index=0 if current_theme == "Light" else 1)
        if app_theme != current_theme:
            st.session_state.app_theme = app_theme
            st.rerun()
            
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
    
    # Initialize tour session states
    if "tour_step" not in st.session_state:
        st.session_state.tour_step = 0
    if "show_tour" not in st.session_state:
        st.session_state.show_tour = False

    t_col1, t_col2, t_col3 = st.columns([3, 4, 3])
    with t_col2:
        tour_label = "🎬 Close Interactive Tour" if st.session_state.show_tour else "💡 Interactive Setup Tour"
        if st.button(tour_label, key="toggle_tour_btn", use_container_width=True):
            st.session_state.show_tour = not st.session_state.show_tour
            st.session_state.tour_step = 0
            st.rerun()

    if st.session_state.show_tour:
        _render_interactive_tour()
        st.markdown("<br>", unsafe_allow_html=True)

    demo_col, upload_col = st.columns(2)
    with demo_col:
        _card("View Demo", "Load a ready-to-analyze ecommerce dataset automatically.", "01")
        st.caption("Select Demo Currency:")
        demo_currency = render_currency_selector(
            default=st.session_state.get("selected_currency", "USD ($) 🇺🇸"),
            key="demo_currency"
        )
        if st.button("▶ Explore Demo Dashboard", type="primary", use_container_width=True):
            st.session_state.selected_currency = demo_currency
            st.session_state.currency_symbol = CURRENCIES[demo_currency]
            with st.spinner("Preparing demo insights..."):
                _stage_raw_data(load_demo_dataset(), "Demo ecommerce dataset")
    with upload_col:
        _card("Upload My Business Data", "Bring CSV, Excel, JSON, TSV, or Parquet data.", "02")
        st.caption("Select Import Currency:")
        import_currency = render_currency_selector(
            default=st.session_state.get("selected_currency", "USD ($) 🇺🇸"),
            key="import_currency"
        )
        uploaded = st.file_uploader("Upload business data", type=["csv", "xlsx", "xls", "json", "parquet", "tsv"], label_visibility="collapsed")
        if st.button("📂 Upload Business Data", use_container_width=True):
            if uploaded is None:
                st.warning("Choose a file to continue. For best performance, keep it under 100MB.")
            else:
                st.session_state.selected_currency = import_currency
                st.session_state.currency_symbol = CURRENCIES[import_currency]
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

    st.markdown("<br><hr style='opacity:0.25;'><br>", unsafe_allow_html=True)
    _render_help_section()


def _render_help_section() -> None:
    """Render a premium, high-fidelity help section with glassmorphism styling."""
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <div class="eyebrow" style="align-self: center;">RESOURCES</div>
            <h2 style="font-size: 2.2rem; margin-top: 0.5rem; color: var(--text-heading);">How to Get Started & FAQ</h2>
            <p style="color: var(--text-secondary); max-width: 600px; margin: 0.5rem auto;">
                Everything you need to know to leverage the premium plug-and-play analytics suite.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="glass" style="padding: 1.5rem; min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📂</div>
                    <div style="font: 600 1.15rem Georgia, serif; color: var(--text-heading); margin-bottom: 0.5rem;">1. Import Data</div>
                    <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.4;">
                        Upload your sales or transactions dataset in CSV, Excel, Parquet, JSON, or TSV. Ensure you have at least sales value, product name, and order date.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="glass" style="padding: 1.5rem; min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🔄</div>
                    <div style="font: 600 1.15rem Georgia, serif; color: var(--text-heading); margin-bottom: 0.5rem;">2. Map Columns</div>
                    <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.4;">
                        Our interactive Column Mapper matches your file's variables to standard dashboard slots (e.g. Sales, Profit, Categories, Regions). No code or refactoring needed!
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="glass" style="padding: 1.5rem; min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">✨</div>
                    <div style="font: 600 1.15rem Georgia, serif; color: var(--text-heading); margin-bottom: 0.5rem;">3. Analyze Insights</div>
                    <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.4;">
                        Instantly unlock KPIs, sales trendlines, RFM client segmentation, product performance grids, and interactive filtering. Download clean reports anytime.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Elegant accordion FAQs using Streamlit expanders
    st.markdown("<h3 style='font-family: Georgia, serif; color: var(--text-heading); margin-bottom: 0.8rem;'>💬 Frequently Asked Questions</h3>", unsafe_allow_html=True)
    
    with st.expander("🛡️ Is my business data safe and private?"):
        st.markdown(
            """
            <div style="font-size: 0.95rem; color: var(--text-primary); line-height: 1.5; padding: 0.5rem 0;">
                <strong>Absolutely.</strong> Your data never leaves your machine. This analytics application runs 100% locally and temporarily stores dataset schemas in secure, ephemeral Streamlit session state memory. No trackers, cloud databases, or telemetry systems are attached.
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with st.expander("📊 What is RFM Segmentation, and how does it help me?"):
        st.markdown(
            """
            <div style="font-size: 0.95rem; color: var(--text-primary); line-height: 1.5; padding: 0.5rem 0;">
                RFM stands for <strong>Recency, Frequency, and Monetary Value</strong>. By parsing your customer transactions, our engine classifies buyers into behavioral categories:
                <ul>
                    <li><strong>VIP:</strong> High-spending loyal clients who ordered very recently.</li>
                    <li><strong>Strong / High Value:</strong> Large spenders whom you can reactivate.</li>
                    <li><strong>Developing / Frequent:</strong> Regular shoppers who might buy more with high-margin incentives.</li>
                    <li><strong>Low / Standard:</strong> Occasional or new buyers.</li>
                </ul>
                Use this dashboard breakdown to customize target campaigns and optimize your marketing budget.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("💱 How do the dynamic currency conversions and theme triggers work?"):
        st.markdown(
            """
            <div style="font-size: 0.95rem; color: var(--text-primary); line-height: 1.5; padding: 0.5rem 0;">
                All metrics, Plotly plots, tooltips, dataframes, and downloadable reports react instantly to currency preferences (USD, EUR, GBP, INR, etc.) selected via the global selectors.
                The <strong>Dark and Light Mode engine</strong> dynamically injects modern CSS variables directly into the document root, altering background gradients, text colors, margins, and Plotly color scales on the fly without breaking active data filters.
            </div>
            """,
            unsafe_allow_html=True,
        )


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


def _render_interactive_tour() -> None:
    """Render a premium multi-step interactive tour to explain how the app works in a fun way."""
    steps = [
        {
            "title": "1. Import Any Raw Format 📂",
            "desc": "No pre-formatting or pre-cleaning required! Bring your business transactions via CSV, Excel sheets, Parquet columns, JSON structures, or directly connect to a local/production MySQL database. Our parser accepts standard table shapes and sets them up instantly.",
            "visual": """
                <div class="mockup-dropzone">
                    <span class="mockup-file">📄</span>
                    <p style="margin-top: 1rem; font-weight: 600; color: var(--text-heading);">your_sales_data.csv</p>
                    <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0;">Analyzing file and staging rows...</p>
                </div>
            """
        },
        {
            "title": "2. Smart Column Mapper 🔄",
            "desc": "Different headers? No problem. The interactive Column Mapper automatically maps your columns (e.g. 'rev_amt', 'transaction_date') to standard fields (Sales, Profit, Category, Region, Date). You review, adjust, and approve. Clean, dynamic matching without database or code mutations!",
            "visual": """
                <div class="mockup-mapper">
                    <div class="mapper-col" style="border-color: var(--accent-amber);">rev_amount</div>
                    <div class="mapper-line"></div>
                    <div class="mapper-col" style="border-color: var(--accent-green); font-weight: bold; background: var(--bg-active);">📊 Sales</div>
                </div>
            """
        },
        {
            "title": "3. Explore Dashboard & KPIs 📈",
            "desc": "Instantly launch a sleek analytics workspace complete with real-time currency converters, light/dark toggles, Monthly Sales areas, ranked product matrices, customer RFM breakdowns (VIP, Developing, Low), and immediate CSV reporting downloads. A complete executive intelligence platform in 30 seconds!",
            "visual": """
                <div class="mockup-dashboard">
                    <div class="mockup-kpi">
                        <span style="font-size: 0.8rem; color: var(--text-secondary);">Total Revenue</span>
                        <div style="font-size: 1.25rem; font-weight: bold; color: var(--accent-green); margin-top: 0.2rem;">$124.5K</div>
                        <span class="badge positive" style="font-size: 0.65rem; padding: 0.1rem 0.4rem;">+14.2%</span>
                    </div>
                    <div class="mockup-chart-bar">
                        <div class="chart-bar-single" style="height: 40px; --target-height: 40px;"></div>
                        <div class="chart-bar-single" style="height: 75px; --target-height: 75px; background: var(--accent-green);"></div>
                        <div class="chart-bar-single" style="height: 60px; --target-height: 60px;"></div>
                        <div class="chart-bar-single" style="height: 90px; --target-height: 90px; background: var(--accent-amber);"></div>
                    </div>
                </div>
            """
        }
    ]

    current_step = st.session_state.tour_step
    step_data = steps[current_step]

    # Generate dots indicator HTML
    dots_html = ""
    for idx in range(len(steps)):
        active_class = "active" if idx == current_step else ""
        dots_html += f'<div class="tour-dot {active_class}"></div>'

    # Render layout
    st.markdown(
        f"""
        <div class="tour-container">
            <div class="tour-steps-header">
                <div style="font-family: Georgia, serif; font-size: 1.25rem; font-weight: bold; color: var(--text-heading);">
                    {step_data["title"]}
                </div>
                <div class="tour-dot-group">
                    {dots_html}
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1.1fr; gap: 2rem; align-items: center;">
                <div style="font-size: 0.95rem; color: var(--text-primary); line-height: 1.55;">
                    {step_data["desc"]}
                </div>
                <div>
                    {step_data["visual"]}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Next / Back Controls
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([2, 2, 2, 4])
    with btn_col1:
        if st.button("⬅️ Back", disabled=(current_step == 0), use_container_width=True):
            st.session_state.tour_step = max(current_step - 1, 0)
            st.rerun()
    with btn_col2:
        if current_step < len(steps) - 1:
            if st.button("Next ➡️", type="primary", use_container_width=True):
                st.session_state.tour_step = current_step + 1
                st.rerun()
        else:
            if st.button("🎉 Finish Tour", type="primary", use_container_width=True):
                st.session_state.show_tour = False
                st.session_state.tour_step = 0
                st.rerun()
    with btn_col3:
        if st.button("❌ Close", use_container_width=True):
            st.session_state.show_tour = False
            st.session_state.tour_step = 0
            st.rerun()

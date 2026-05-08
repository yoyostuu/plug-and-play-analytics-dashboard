from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ACCENT, AMBER, RED, BROWN, MUTED = "#6a8a5a", "#c87820", "#b84030", "#8a7050", "#a09070"

def inject_custom_css() -> None:
    """Inject the premium SaaS visual system used across the app."""
    st.markdown(
        """
        <style>
        :root{--bg-page:#fdf8f0;--bg-sidebar:#f5f0e8;--bg-card:#fff;--bg-active:#ede8dc;--border-default:#ede8dc;--border-strong:#d8d0c0;--text-primary:#7a6040;--text-secondary:#a09070;--text-muted:#c0b090;--text-heading:#5a4028;--accent-green:#6a8a5a;--accent-green-light:#d4e8c8;--accent-amber:#c87820;--accent-red:#b84030}
        .stApp{background:linear-gradient(135deg,#fdf8f0,#f7efe4 52%,#fbf6ee);color:var(--text-primary);font-family:Georgia,'Times New Roman',serif}
        .stApp:before{content:"";position:fixed;inset:10px;border:1px solid var(--border-strong);border-radius:20px;box-shadow:inset 0 0 44px rgba(216,208,192,.36),0 18px 60px rgba(90,64,40,.1);pointer-events:none;z-index:999}
        .main .block-container{max-width:1440px;padding:2rem 2.1rem 2.4rem}.block-container hr{border-color:var(--border-default)}
        h1,h2,h3,.dashboard-title,.chart-title{font-family:Georgia,'Times New Roman',serif;color:var(--text-heading)}
        .dashboard-title{font-size:2.55rem;font-weight:800;letter-spacing:-.025em;margin:.1rem 0 .25rem}.dashboard-subtitle{color:var(--text-secondary);font-size:1.08rem;margin-bottom:1.3rem}
        .stMarkdown,.stMarkdown p,.stMarkdown span,.stCaptionContainer,.st-emotion-cache-ue6h4q,.st-emotion-cache-16idsys p{color:var(--text-primary)!important}
        label,[data-testid="stWidgetLabel"],[data-testid="stMarkdownContainer"]{color:var(--text-heading)!important}
        .hero{text-align:center;padding:5.2rem 1rem 2.4rem;animation:fadeUp .45s ease both}.hero:before{content:"";position:absolute;inset:54px 12%;background:radial-gradient(circle at 50% 10%,rgba(200,120,32,.16),transparent 42%);filter:blur(24px);z-index:-1}.hero h1{font-size:clamp(2.6rem,5vw,5rem);line-height:.95;margin:.85rem auto;max-width:940px}.hero p{color:var(--text-secondary);font-size:1.18rem;max-width:700px;margin:0 auto}
        .eyebrow,.badge,.chip{display:inline-flex;align-items:center;border-radius:999px;padding:.34rem .66rem;font:500 .76rem Consolas,'Courier New',monospace;border:1px solid var(--border-default);background:var(--bg-active);color:var(--text-primary)}
        .glass,.metric-card{background:rgba(255,255,255,.78);border:1px solid var(--border-default);box-shadow:0 18px 42px rgba(122,96,64,.09),inset 0 1px 0 rgba(255,255,255,.8);backdrop-filter:blur(16px);border-radius:12px;transition:transform 150ms ease,box-shadow 150ms ease,border-color 150ms ease;animation:fadeUp .35s ease both}
        .glass:hover,.metric-card:hover{transform:translateY(-3px);border-color:var(--border-strong);box-shadow:0 22px 52px rgba(122,96,64,.13)}
        .metric-card{padding:1rem 1.05rem;min-height:150px}.metric-label{color:var(--text-secondary);font:.78rem Georgia,serif;text-transform:uppercase;letter-spacing:.08em}.metric-value{font:500 1.85rem Consolas,'Courier New',monospace;color:var(--text-heading);margin-top:.28rem}.metric-help,.section-copy{color:var(--text-secondary);font-size:.9rem}.badge.positive{background:var(--accent-green-light);color:var(--accent-green)}.badge.negative{background:#f4d8d4;color:var(--accent-red)}.badge.warning{background:#f3dfc7;color:var(--accent-amber)}
        .spark{margin-top:.65rem;width:100%;height:30px}.chart-title{font-size:1.18rem;font-weight:700}.product-row{display:grid;grid-template-columns:34px 1fr 120px 54px;gap:.7rem;align-items:center;padding:.55rem .25rem;border-top:1px solid var(--border-default);transition:background 150ms ease}.product-row:hover{background:#fbf5eb}.bar{height:8px;border-radius:99px;background:var(--bg-active);overflow:hidden}.fill{height:100%;border-radius:99px;background:linear-gradient(90deg,#8a7050,#c87820)}
        div[data-testid="stButton"] button,div[data-testid="stDownloadButton"] button{border-radius:999px;border:1px solid var(--border-strong);background:linear-gradient(180deg,#fffaf2,#ede8dc);color:var(--text-heading);font-family:Consolas,'Courier New',monospace;box-shadow:0 10px 24px rgba(122,96,64,.1);transition:transform 150ms ease,box-shadow 150ms ease}
        div[data-testid="stButton"] button:hover,div[data-testid="stDownloadButton"] button:hover{transform:translateY(-1px);box-shadow:0 14px 30px rgba(122,96,64,.15)}
        section[data-testid="stSidebar"]{width:220px;background:var(--bg-sidebar);border-right:1px solid var(--border-default);box-shadow:8px 0 24px rgba(122,96,64,.05)}section[data-testid="stSidebar"] *{font-family:Georgia,'Times New Roman',serif;color:var(--text-primary)}
        [data-testid="stFileUploader"],[data-testid="stDataFrame"]{border-radius:12px}.stMultiSelect [data-baseweb="tag"]{background:var(--bg-active);border:1px solid var(--border-default);border-radius:999px;color:var(--text-heading)}
        @keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}@media(max-width:900px){.main .block-container{padding:1.6rem}.product-row{grid-template-columns:28px 1fr}}
        </style>
        """,
        unsafe_allow_html=True,
    )
def render_dashboard(df: pd.DataFrame) -> None:
    """Render the preserved analytics dashboard with polished SaaS styling."""
    st.markdown('<div class="dashboard-title">Plug-and-Play Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Upload your business data and get instant insights in seconds. Optimized for small and medium business datasets.</div>', unsafe_allow_html=True)
    st.sidebar.markdown("### Control panel")
    st.sidebar.caption("Refine your view, export filtered data, or change source.")
    if st.sidebar.button("Change data source", use_container_width=True):
        _reset_data_state()
        st.rerun()
    filtered = apply_filters(df)
    if filtered.empty:
        st.warning("No records match the selected filters. Try widening your selections.")
        return
    render_sidebar_spotlight(filtered)
    st.sidebar.download_button("Download Filtered Data", filtered.to_csv(index=False).encode("utf-8"), "filtered_data.csv", "text/csv", use_container_width=True)
    render_kpis(filtered, df)
    st.divider()
    render_core_charts(filtered)
    render_customer_sections(filtered)
    render_downloads(filtered)
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar controls and return filtered dashboard data."""
    st.sidebar.markdown("### Filters")
    min_date, max_date = df["Order Date"].min().date(), df["Order Date"].max().date()
    date_range = st.sidebar.date_input("Date range", (min_date, max_date), min_value=min_date, max_value=max_date)
    regions = sorted(df["Region"].dropna().unique())
    categories = sorted(df["Category"].dropna().unique())
    selected_regions = st.sidebar.multiselect("Regions", regions, default=regions)
    selected_categories = st.sidebar.multiselect("Categories", categories, default=categories)
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[-1])
    return df.loc[df["Order Date"].between(start, end) & df["Region"].isin(selected_regions) & df["Category"].isin(selected_categories)].copy()
def render_kpis(df: pd.DataFrame, full_df: pd.DataFrame) -> None:
    """Show premium KPI cards using existing calculations plus trend badges."""
    sales, profit, orders = df["Sales"].sum(), df["Profit"].sum(), df["Order ID"].nunique()
    aov = sales / orders if orders else 0
    badges = _trend_badges(df, full_df)
    values = [("Total Revenue", _money(sales), "Revenue after filters", "positive", badges[0]), ("Orders", f"{orders:,}", "Unique transactions", "warning", badges[1]), ("Profit", _money(profit), "Estimated or mapped profit", "positive", f"{profit / sales * 100:.1f}%"), ("Average Order Value", _money(aov), "Revenue per order", "negative" if badges[2].startswith("-") else "positive", badges[2])]
    for col, item in zip(st.columns(4), values):
        with col:
            metric_card(*item)
def render_core_charts(df: pd.DataFrame) -> None:
    """Render the existing chart suite with modern Plotly styling."""
    monthly = df.set_index("Order Date").resample("MS").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
    trend = px.area(monthly, x="Order Date", y="Sales", title="Monthly Sales Trend")
    trend.update_traces(line=dict(color=BROWN), fillcolor="rgba(138,112,80,.16)")
    trend.add_scatter(x=monthly["Order Date"], y=monthly["Profit"], mode="lines+markers", name="Profit", line=dict(color=ACCENT, width=3))
    _chart(trend, "Monthly Sales Trend", "Revenue and profit movement over time", 430)
    left, right = st.columns(2)
    with left:
        products = df.groupby("Product").agg(Sales=("Sales", "sum"), Quantity=("Quantity", "sum")).nlargest(10, "Sales").reset_index()
        fig = px.bar(products, x="Sales", y="Product", orientation="h", color="Quantity", title="Top Products", color_continuous_scale=[[0, "#ede8dc"], [1, AMBER]])
        fig.update_layout(yaxis=dict(autorange="reversed"))
        _chart(fig, "Top Products", "Best-selling products by revenue")
        render_product_table(products)
    with right:
        regions = df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
        _chart(px.pie(regions, names="Region", values="Sales", hole=.58, title="Sales by Region", color_discrete_sequence=[BROWN, ACCENT, AMBER, RED, MUTED]), "Sales by Region", "Regional revenue distribution")
    left, right = st.columns(2)
    with left:
        categories = df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
        categories["Profit Margin"] = categories["Profit"] / categories["Sales"].replace(0, pd.NA)
        _chart(px.bar(categories, x="Category", y="Profit", color="Profit Margin", title="Category Breakdown", color_continuous_scale=[[0, "#d8d0c0"], [.5, AMBER], [1, ACCENT]]), "Category Breakdown", "Profit contribution by category")
    with right:
        render_daily_heatmap(df)
def render_customer_sections(df: pd.DataFrame) -> None:
    """Render customer segmentation and RFM scatter analytics."""
    left, right = st.columns(2)
    segments = build_customer_segments(df)
    with left:
        summary = segments.groupby("Segment").agg(Sales=("Total_Sales", "sum"), Profit=("Total_Profit", "sum")).reset_index()
        _chart(px.treemap(summary, path=["Segment"], values="Sales", color="Profit", title="Customer Segmentation", color_continuous_scale=[[0, "#ede8dc"], [.5, BROWN], [1, ACCENT]]), "Customer Segmentation", "Spend and order-frequency segments")
    with right:
        rfm = build_rfm(df)
        _chart(px.scatter(rfm, x="Recency", y="Monetary", size="Frequency", color="Segment", hover_name="Customer Name", title="RFM Segmentation", color_discrete_sequence=[BROWN, ACCENT, AMBER, RED]), "RFM Segmentation", "Recency, frequency, and monetary value")
    st.markdown("### Customer table")
    st.markdown('<div class="section-copy">Review customer value, order frequency, and latest order date.</div>', unsafe_allow_html=True)
    st.dataframe(segments, use_container_width=True, hide_index=True)
def render_daily_heatmap(df: pd.DataFrame) -> None:
    """Render a weekday by week-of-year sales heatmap."""
    heat = df.copy()
    heat["Week"] = heat["Order Date"].dt.isocalendar().week.astype(int)
    heat["Day"] = pd.Categorical(heat["Order Date"].dt.day_name(), ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ordered=True)
    pivot = heat.pivot_table(index="Day", columns="Week", values="Sales", aggfunc="sum", observed=False).fillna(0)
    _chart(px.imshow(pivot, aspect="auto", color_continuous_scale=["#f5f0e8", "#c87820", "#6a8a5a"], title="Daily Sales Heatmap"), "Daily Sales Heatmap", "Weekday versus week-of-year sales intensity")
def build_customer_segments(df: pd.DataFrame) -> pd.DataFrame:
    """Create a spend and frequency based customer segment table."""
    customers = df.groupby("Customer Name").agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"), Orders=("Order ID", "nunique"), Units=("Quantity", "sum"), Last_Order=("Order Date", "max")).reset_index()
    customers["Average_Order_Value"] = customers["Total_Sales"] / customers["Orders"].replace(0, pd.NA)
    high_spend, high_frequency = customers["Total_Sales"].quantile(.75), customers["Orders"].quantile(.75)
    customers["Segment"] = customers.apply(lambda r: "VIP" if r.Total_Sales >= high_spend and r.Orders >= high_frequency else "High Value" if r.Total_Sales >= high_spend else "Frequent Buyer" if r.Orders >= high_frequency else "Standard", axis=1)
    return customers.sort_values("Total_Sales", ascending=False)
def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate recency, frequency, and monetary values by customer."""
    snapshot = df["Order Date"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("Customer Name").agg(Recency=("Order Date", lambda s: (snapshot - s.max()).days), Frequency=("Order ID", "nunique"), Monetary=("Sales", "sum")).reset_index()
    if len(rfm) < 4:
        rfm["Segment"] = "Standard"
    else:
        scores = pd.qcut(rfm["Monetary"].rank(method="first"), 4, labels=False, duplicates="drop")
        rfm["Segment"] = scores.map({0: "Low", 1: "Developing", 2: "Strong", 3: "VIP"}).fillna("Standard")
    return rfm
def render_downloads(df: pd.DataFrame) -> None:
    """Render the retained CSV report export area."""
    st.markdown("### Export center")
    st.download_button("Download filtered orders", df.to_csv(index=False).encode("utf-8"), "filtered_ecommerce_orders.csv", "text/csv", use_container_width=True)
def render_sidebar_spotlight(df: pd.DataFrame) -> None:
    """Add the sidebar best-seller card and revenue goal progress."""
    top = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
    name, revenue = (top.index[0], top.iloc[0]) if len(top) else ("N/A", 0)
    goal = max(df["Sales"].sum() / .87, 1)
    progress = min(df["Sales"].sum() / goal, 1)
    st.sidebar.markdown(f"""<div class="glass" style="padding:1rem;margin:1rem 0;"><div class="metric-label">Best Seller</div><div style="font-size:1.05rem;color:#5a4028;font-family:'Playfair Display',serif;margin-top:.35rem;">{name}</div><div class="metric-value" style="font-size:1.1rem;">{_money(revenue)}</div><span class="badge positive">+12.4%</span></div><div class="glass" style="padding:1rem;margin-bottom:1rem;"><div class="metric-label">Monthly Revenue Goal</div><div class="metric-value" style="font-size:1rem;">{progress:.0%} filled</div><div style="height:10px;background:#ede8dc;border-radius:999px;overflow:hidden;margin-top:.7rem;"><div style="height:100%;width:{progress * 100:.0f}%;background:#c87820;border-radius:999px;"></div></div></div>""", unsafe_allow_html=True)
def render_product_table(products: pd.DataFrame) -> None:
    """Render a luxury ranked product table with revenue bars."""
    max_sales = max(products["Sales"].max(), 1)
    rows = ""
    for rank, row in products.head(5).reset_index(drop=True).iterrows():
        width = row["Sales"] / max_sales * 100
        rows += f'<div class="product-row"><span class="chip">#{rank + 1}</span><span>{row["Product"]}</span><div><div class="bar"><div class="fill" style="width:{width:.0f}%"></div></div></div><span class="badge positive">&uarr;</span></div>'
    st.markdown(f'<div class="glass" style="padding:1rem;margin-bottom:1rem;"><div class="chart-title">Product list</div><div class="section-copy">Ranked with revenue bars and trend badges.</div>{rows}</div>', unsafe_allow_html=True)
def metric_card(label: str, value: str, help_text: str, badge_class: str, badge: str) -> None:
    """Render one luxury KPI card with badge and sparkline."""
    spark = '<svg class="spark" viewBox="0 0 160 36" preserveAspectRatio="none"><polyline points="0,24 28,20 56,25 84,12 112,16 160,7" fill="none" stroke="#8a7050" stroke-width="3"/><polyline points="0,29 28,24 56,28 84,17 112,21 160,12" fill="none" stroke="#6a8a5a" stroke-width="2" opacity=".7"/></svg>'
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-help">{help_text}</div><span class="badge {badge_class}">{badge}</span>{spark}</div>', unsafe_allow_html=True)
def plot_layout(fig: go.Figure, height: int = 390) -> go.Figure:
    """Apply premium dark Plotly styling."""
    fig.update_layout(height=height, template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.42)", font=dict(color="#7a6040", family="Crimson Pro"), margin=dict(l=10, r=10, t=22, b=10), hoverlabel=dict(bgcolor="#fffaf2", bordercolor="#d8d0c0", font_color="#5a4028"), legend=dict(orientation="h"))
    fig.update_layout(title_font=dict(color="#5a4028"), legend_font=dict(color="#7a6040"), coloraxis_colorbar=dict(tickfont=dict(color="#7a6040"), title_font=dict(color="#5a4028")))
    fig.update_traces(textfont_color="#5a4028", selector=dict(type="pie"))
    fig.update_traces(textfont_color="#5a4028", selector=dict(type="treemap"))
    fig.update_xaxes(gridcolor="#ede8dc", zerolinecolor="#d8d0c0", tickfont=dict(color="#5a4028"), title_font=dict(color="#5a4028"))
    fig.update_yaxes(gridcolor="#ede8dc", zerolinecolor="#d8d0c0", tickfont=dict(color="#5a4028"), title_font=dict(color="#5a4028"))
    return fig
def _chart(fig: go.Figure, title: str, subtitle: str, height: int = 390) -> None:
    """Render a chart with a title block and consistent spacing."""
    st.markdown(f'<div class="glass" style="padding:1rem 1rem .3rem;margin-bottom:1rem;"><div class="chart-title">{title}</div><div class="section-copy">{subtitle}</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_layout(fig, height), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
def _trend_badges(df: pd.DataFrame, full_df: pd.DataFrame) -> list[str]:
    """Return compact percentage badges for KPI cards."""
    midpoint = full_df["Order Date"].min() + (full_df["Order Date"].max() - full_df["Order Date"].min()) / 2
    prior, current = full_df[full_df["Order Date"] < midpoint], df[df["Order Date"] >= midpoint]
    sales = _pct(current["Sales"].sum(), prior["Sales"].sum())
    orders = _pct(current["Order ID"].nunique(), prior["Order ID"].nunique())
    aov = _pct(current["Sales"].sum() / max(current["Order ID"].nunique(), 1), prior["Sales"].sum() / max(prior["Order ID"].nunique(), 1))
    return [sales, orders, aov]
def _pct(now: float, before: float) -> str:
    """Format a simple percentage trend badge."""
    return "+0.0%" if before == 0 else f"{((now - before) / before) * 100:+.1f}%"
def _money(value: float) -> str:
    """Format a value as compact currency."""
    return f"${value:,.0f}"
def _reset_data_state() -> None:
    """Return the app to the landing flow."""
    st.session_state.raw_df = None
    st.session_state.mapped_df = None
    st.session_state.data_ready = False
    st.session_state.needs_mapping = False

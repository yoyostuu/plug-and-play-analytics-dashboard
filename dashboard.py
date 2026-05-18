from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from currency_helper import render_currency_selector, CURRENCIES

ACCENT, AMBER, RED, BROWN, MUTED = "#6a8a5a", "#c87820", "#b84030", "#8a7050", "#a09070"

def inject_custom_css() -> None:
    """Inject the premium SaaS visual system used across the app."""
    import os
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    with open(css_path, "r") as f:
        css = f.read()
        
    if st.session_state.get("app_theme") == "Dark":
        dark_override = """
        :root {
            --bg-page: #121418;
            --bg-sidebar: #1a1d24;
            --bg-card: #1f232b;
            --bg-active: #2a2f3a;
            --border-default: #334155;
            --border-strong: #475569;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --text-heading: #f8fafc;
            --accent-green: #48bb78;
            --accent-green-light: #2f855a;
            --accent-amber: #ed8936;
            --accent-amber-dark: #dd6b20;
            --accent-red: #f56565;
            
            /* Input & Dropdown High-Contrast Tokens (Dark Mode Overrides) */
            --bg-input: #1e293b;
            --text-input: #f8fafc;
            --border-input: #475569;
            --bg-dropdown: #1e293b;
            --text-dropdown: #f8fafc;
            --bg-dropdown-hover: #334155;
            --text-dropdown-hover: #ffffff;
            --bg-dropdown-selected: #ed8936;
            --text-dropdown-selected: #ffffff;
            
            --bg-page-gradient: linear-gradient(135deg, #121418, #16191f 52%, #1a1d24);
            --bg-bar-gradient: linear-gradient(90deg, #4a5568, #ed8936);
            --bg-button-gradient: linear-gradient(180deg, #1f232b, #1a1d24);
            
            --shadow-light: rgba(0, 0, 0, 0.25);
            --shadow-strong: rgba(0, 0, 0, 0.45);
            --shadow-button: rgba(0, 0, 0, 0.35);
        }
        """
        css += dark_override

    import time
    css += f"\n/* force_reload: {time.time()} */"
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
def render_dashboard(df: pd.DataFrame) -> None:
    """Render the preserved analytics dashboard with polished SaaS styling."""
    st.markdown('<div class="dashboard-title">Plug-and-Play Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Upload your business data and get instant insights in seconds. Optimized for small and medium business datasets.</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("### 💱 Currency Settings")
    selected_currency = render_currency_selector(
        default=st.session_state.get("selected_currency", "USD ($) 🇺🇸"),
        key="dashboard_currency"
    )
    st.session_state.selected_currency = selected_currency
    st.session_state.currency_symbol = CURRENCIES[selected_currency]
    
    st.sidebar.markdown("### 🎨 Theme Settings")
    current_theme = st.session_state.get("app_theme", "Light")
    app_theme = st.sidebar.radio(
        "Select Theme",
        options=["Light", "Dark"],
        index=0 if current_theme == "Light" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )
    if app_theme != current_theme:
        st.session_state.app_theme = app_theme
        st.rerun()
    
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
    
    symbol = st.session_state.get("currency_symbol", "$")
    st.dataframe(
        segments,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total_Sales": st.column_config.NumberColumn("Total Sales", format=f"{symbol}%.2f"),
            "Total_Profit": st.column_config.NumberColumn("Total Profit", format=f"{symbol}%.2f"),
            "Average_Order_Value": st.column_config.NumberColumn("AOV", format=f"{symbol}%.2f"),
        }
    )
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
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<div class="section-copy">Download your filtered and prepared orders. Current export format: <b>{st.session_state.get("selected_currency", "USD ($) 🇺🇸")}</b></div>', unsafe_allow_html=True)
    with col2:
        st.write("Change export currency:")
        selected_currency = render_currency_selector(
            default=st.session_state.get("selected_currency", "USD ($) 🇺🇸"),
            key="export_currency"
        )
        if selected_currency != st.session_state.selected_currency:
            st.session_state.selected_currency = selected_currency
            st.session_state.currency_symbol = CURRENCIES[selected_currency]
            st.rerun()
            
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
    """Apply premium dynamic Plotly styling based on current theme."""
    symbol = st.session_state.get("currency_symbol", "$")
    theme = st.session_state.get("app_theme", "Light")
    
    is_dark = theme == "Dark"
    bg = "rgba(255,255,255,.05)" if is_dark else "rgba(255,255,255,.42)"
    font_color = "#a0aec0" if is_dark else "#7a6040"
    title_color = "#f7fafc" if is_dark else "#5a4028"
    grid_color = "#2a2f3a" if is_dark else "#ede8dc"
    zero_color = "#3a4150" if is_dark else "#d8d0c0"
    hover_bg = "#1f232b" if is_dark else "#fffaf2"
    hover_border = "#3a4150" if is_dark else "#d8d0c0"
    
    fig.update_layout(height=height, template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=bg, font=dict(color=font_color, family="Crimson Pro"), margin=dict(l=10, r=10, t=22, b=10), hoverlabel=dict(bgcolor=hover_bg, bordercolor=hover_border, font_color=font_color), legend=dict(orientation="h"))
    fig.update_layout(title_font=dict(color=title_color), legend_font=dict(color=font_color), coloraxis_colorbar=dict(tickfont=dict(color=font_color), title_font=dict(color=title_color)))
    fig.update_traces(textfont_color=title_color, selector=dict(type="pie"))
    fig.update_traces(textfont_color=title_color, selector=dict(type="treemap"))
    
    # Auto-format axes with currency symbol if they contain sales, profit, or monetary fields
    x_title = fig.layout.xaxis.title.text if fig.layout.xaxis and fig.layout.xaxis.title else ""
    y_title = fig.layout.yaxis.title.text if fig.layout.yaxis and fig.layout.yaxis.title else ""
    money_keywords = ["sales", "profit", "monetary", "revenue", "value", "aov"]
    
    if any(kw in str(y_title).lower() for kw in money_keywords):
        fig.update_yaxes(tickprefix=symbol)
    if any(kw in str(x_title).lower() for kw in money_keywords):
        fig.update_xaxes(tickprefix=symbol)
        
    fig.update_xaxes(gridcolor=grid_color, zerolinecolor=zero_color, tickfont=dict(color=title_color), title_font=dict(color=title_color))
    fig.update_yaxes(gridcolor=grid_color, zerolinecolor=zero_color, tickfont=dict(color=title_color), title_font=dict(color=title_color))
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
    symbol = st.session_state.get("currency_symbol", "$")
    return f"{symbol}{value:,.0f}"
def _reset_data_state() -> None:
    """Return the app to the landing flow."""
    st.session_state.raw_df = None
    st.session_state.mapped_df = None
    st.session_state.data_ready = False
    st.session_state.needs_mapping = False

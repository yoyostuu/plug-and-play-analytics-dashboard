from __future__ import annotations

import pandas as pd
import streamlit as st


REQUIRED = ["date", "sales", "product"]
OPTIONAL = ["category", "region", "customer", "quantity", "profit", "discount", "order_id"]
KEYWORDS = {
    "date": ["date", "order_date", "invoice_date", "purchase_date", "created_at"],
    "sales": ["sales", "revenue", "amount", "total", "price", "gmv", "unitprice"],
    "product": ["product", "item", "description", "name", "title", "sku"],
    "category": ["category", "cat", "type", "department", "segment"],
    "region": ["region", "city", "state", "country", "location", "area"],
    "quantity": ["quantity", "qty", "units", "count"],
    "customer": ["customer", "user", "client", "buyer", "cust_id", "customer_id"],
    "profit": ["profit", "margin", "earnings"],
    "discount": ["discount", "markdown", "coupon"],
    "rating": ["rating", "review", "score"],
    "order_id": ["order", "order_id", "invoice", "invoice_no", "invoiceno", "id"],
}
STANDARD_NAMES = {
    "date": "Order Date",
    "sales": "Sales",
    "product": "Product",
    "category": "Category",
    "region": "Region",
    "quantity": "Quantity",
    "customer": "Customer Name",
    "profit": "Profit",
    "discount": "Discount",
    "rating": "Rating",
    "order_id": "Order ID",
}


def detect_columns(df: pd.DataFrame) -> dict[str, str | None]:
    """Suggest column mappings from common ecommerce field keywords."""
    suggestions = {}
    normalized = {col: _clean(col) for col in df.columns}
    for field, words in KEYWORDS.items():
        suggestions[field] = None
        for col, clean_col in normalized.items():
            if any(word in clean_col for word in words):
                suggestions[field] = col
                break
    return suggestions


def render_column_mapper(df: pd.DataFrame) -> None:
    """Show data preview, mapping dropdowns, validation, and launch action."""
    st.markdown('<div class="dashboard-title">Map your business data</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dashboard-subtitle">Preview your first rows, confirm the required fields, and launch instant insights.</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(df.head(5), use_container_width=True, hide_index=True)

    suggestions = detect_columns(df)
    options = ["-- Not available --"] + list(df.columns)
    mapping = {}
    left, right = st.columns(2)
    fields = REQUIRED + OPTIONAL
    for idx, field in enumerate(fields):
        container = left if idx % 2 == 0 else right
        with container:
            default = suggestions.get(field)
            index = options.index(default) if default in options else 0
            label = f"{STANDARD_NAMES[field]} {'* required' if field in REQUIRED else 'optional'}"
            value = st.selectbox(label, options, index=index, key=f"map_{field}")
            mapping[field] = None if value == "-- Not available --" else value

    missing = [STANDARD_NAMES[field] for field in REQUIRED if not mapping.get(field)]
    if missing:
        st.warning("Missing required fields: " + ", ".join(missing))

    if st.button("Launch Dashboard", type="primary", disabled=bool(missing), use_container_width=True):
        try:
            st.session_state.mapped_df = normalize_columns(df, mapping)
            st.session_state.needs_mapping = False
            st.session_state.data_ready = True
            st.rerun()
        except Exception as exc:
            st.error(f"Could not prepare dashboard data: {exc}")


def normalize_columns(df: pd.DataFrame, mapping: dict[str, str | None]) -> pd.DataFrame:
    """Convert arbitrary ecommerce data to the dashboard schema."""
    out = pd.DataFrame()
    for field in REQUIRED + OPTIONAL:
        source = mapping.get(field)
        if source:
            out[STANDARD_NAMES[field]] = df[source]

    out["Order Date"] = pd.to_datetime(out["Order Date"], errors="coerce")
    if "Quantity" not in out:
        out["Quantity"] = 1
    out["Quantity"] = pd.to_numeric(out["Quantity"], errors="coerce").fillna(1)
    out["Sales"] = pd.to_numeric(out["Sales"], errors="coerce").fillna(0)
    if _looks_like_unit_price(mapping.get("sales")):
        out["Sales"] = out["Sales"] * out["Quantity"]
    if "Profit" not in out:
        out["Profit"] = (out["Sales"] * 0.22).round(2)
    else:
        out["Profit"] = pd.to_numeric(out["Profit"], errors="coerce").fillna(0)
    if "Order ID" not in out:
        out["Order ID"] = [f"ORDER-{100000 + i}" for i in range(len(out))]
    defaults = {"Category": "Uncategorized", "Region": "All Regions", "Customer Name": "Unknown Customer"}
    for col, fallback in defaults.items():
        if col not in out:
            out[col] = fallback
    for col in ["Product", "Category", "Region", "Customer Name"]:
        out[col] = out[col].fillna("Unknown").astype(str)
    out = out.dropna(subset=["Order Date"]).copy()
    return out


def _clean(value: object) -> str:
    """Normalize column text for keyword matching."""
    return str(value).lower().replace(" ", "_").replace("-", "_")


def _looks_like_unit_price(source: str | None) -> bool:
    """Detect UCI-style unit price columns so sales becomes price times quantity."""
    if not source:
        return False
    clean = _clean(source)
    return "unitprice" in clean or "unit_price" in clean

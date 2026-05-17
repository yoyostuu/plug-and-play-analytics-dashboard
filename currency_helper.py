from __future__ import annotations

import streamlit as st
import pandas as pd

# Standard currencies mapping (Pill format display name -> symbol)
CURRENCIES = {
    "USD ($) 🇺🇸": "$",
    "EUR (€) 🇪🇺": "€",
    "GBP (£) 🇬🇧": "£",
    "INR (₹) 🇮🇳": "₹",
    "JPY (¥) 🇯🇵": "¥",
    "CAD ($) 🇨🇦": "$",
    "AUD ($) 🇦🇺": "$",
    "CNY (¥) 🇨🇳": "¥"
}

def detect_currency_from_columns(df: pd.DataFrame) -> str:
    """Analyze columns to auto-detect the matching currency as a recommended default."""
    if df is None or df.empty:
        return st.session_state.get("selected_currency", "USD ($) 🇺🇸")
        
    cols_str = " ".join([str(col) for col in df.columns]).lower()
    
    # Check for symbols or names
    if "₹" in cols_str or "inr" in cols_str or "rupee" in cols_str:
        return "INR (₹) 🇮🇳"
    elif "€" in cols_str or "eur" in cols_str or "euro" in cols_str:
        return "EUR (€) 🇪🇺"
    elif "£" in cols_str or "gbp" in cols_str or "pound" in cols_str:
        return "GBP (£) 🇬🇧"
    elif "¥" in cols_str or "jpy" in cols_str or "yen" in cols_str:
        return "JPY (¥) 🇯🇵"
    elif "cny" in cols_str or "yuan" in cols_str:
        return "CNY (¥) 🇨🇳"
    elif "cad" in cols_str:
        return "CAD ($) 🇨🇦"
    elif "aud" in cols_str:
        return "AUD ($) 🇦🇺"
    elif "$" in cols_str or "usd" in cols_str or "dollar" in cols_str:
        return "USD ($) 🇺🇸"
        
    return st.session_state.get("selected_currency", "USD ($) 🇺🇸")

def render_currency_selector(default: str = "USD ($) 🇺🇸", key: str = "currency_selector") -> str:
    """Render a searchable dropdown selector with flags and symbols."""
    options = list(CURRENCIES.keys())
    if default not in options:
        default = "USD ($) 🇺🇸"
        
    index = options.index(default)
    
    # Render minimalist searchable dropdown
    selected = st.selectbox(
        "Currency",
        options,
        index=index,
        key=key,
        label_visibility="collapsed"
    )
    return selected

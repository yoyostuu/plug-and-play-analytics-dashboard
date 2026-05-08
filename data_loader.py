from __future__ import annotations

from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
import streamlit as st
from urllib.request import urlopen

try:
    import mysql.connector
except ImportError:
    mysql = None


BASE_DIR = Path(__file__).parent
SAMPLE_PATH = BASE_DIR / "data" / "ecommerce_sales_sample.csv"
DEMO_FILES = [
    BASE_DIR / "data" / "online_retail_II.xlsx",
    BASE_DIR / "data" / "online_retail_II.csv",
]
UCI_URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"


@st.cache_data(show_spinner=False)
def load_sample_csv() -> pd.DataFrame:
    """Load the original bundled CSV dataset."""
    return pd.read_csv(SAMPLE_PATH)


@st.cache_data(show_spinner=False)
def load_demo_dataset() -> pd.DataFrame:
    """Load UCI Online Retail II, falling back to synthetic data if unavailable."""
    try:
        for path in DEMO_FILES:
            if path.exists():
                return enrich_demo_data(_read_path(path))
        if SAMPLE_PATH.exists():
            return pd.read_csv(SAMPLE_PATH)
        with urlopen(UCI_URL, timeout=18) as response:
            content = response.read()
        with ZipFile(BytesIO(content)) as archive:
            target = next(n for n in archive.namelist() if n.lower().endswith((".xlsx", ".csv")))
            with archive.open(target) as file:
                if target.lower().endswith(".csv"):
                    return enrich_demo_data(pd.read_csv(file, encoding="latin1"))
                sheets = pd.read_excel(file, sheet_name=None)
                return enrich_demo_data(pd.concat(sheets.values(), ignore_index=True))
    except Exception:
        return generate_synthetic_dataset()


@st.cache_data(show_spinner=False)
def load_uploaded_file(file_name: str, file_bytes: bytes) -> pd.DataFrame:
    """Load user files in CSV, Excel, JSON, Parquet, or TSV format."""
    suffix = Path(file_name).suffix.lower()
    buffer = BytesIO(file_bytes)
    if suffix == ".csv":
        return pd.read_csv(buffer)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(buffer)
    if suffix == ".json":
        return pd.read_json(buffer)
    if suffix == ".parquet":
        return pd.read_parquet(buffer)
    if suffix == ".tsv":
        return pd.read_csv(buffer, sep="\t")
    raise ValueError(f"Unsupported file type: {suffix}")


@st.cache_data(show_spinner=False)
def load_mysql_data(host: str, port: int, user: str, password: str, database: str) -> pd.DataFrame:
    """Load order data from a MySQL ecommerce_orders table."""
    if mysql is None:
        raise ImportError("mysql-connector-python is not installed.")
    query = "SELECT * FROM ecommerce_orders;"
    connection = mysql.connector.connect(
        host=host, port=port, user=user, password=password, database=database
    )
    try:
        return pd.read_sql(query, connection)
    finally:
        connection.close()


def _read_path(path: Path) -> pd.DataFrame:
    """Read a local demo file based on extension."""
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    sheets = pd.read_excel(path, sheet_name=None)
    return pd.concat(sheets.values(), ignore_index=True)


def enrich_demo_data(df: pd.DataFrame) -> pd.DataFrame:
    """Add dashboard-friendly fields missing from the UCI retail demo."""
    out = df.copy()
    columns = {str(col).lower().replace(" ", ""): col for col in out.columns}
    quantity = columns.get("quantity")
    price = columns.get("unitprice") or columns.get("price")
    description = columns.get("description")
    if "sales" not in columns and quantity and price:
        out["Sales"] = pd.to_numeric(out[quantity], errors="coerce") * pd.to_numeric(out[price], errors="coerce")
    if "profit" not in columns and "Sales" in out:
        out["Profit"] = (pd.to_numeric(out["Sales"], errors="coerce").fillna(0) * 0.22).round(2)
    if "category" not in columns:
        out["Category"] = _infer_categories(out[description]) if description else "General Merchandise"
    return out


def _infer_categories(series: pd.Series) -> pd.Series:
    """Infer broad retail categories from product descriptions."""
    text = series.fillna("").astype(str).str.lower()
    choices = [
        text.str.contains("bag|purse|wallet|jewellery|necklace|bracelet"),
        text.str.contains("mug|cup|plate|bowl|kitchen|cake|tea|coffee"),
        text.str.contains("christmas|heart|flower|decor|candle|light"),
        text.str.contains("toy|game|doll|child|baby"),
    ]
    labels = ["Fashion", "Home & Kitchen", "Decor", "Toys"]
    return pd.Series(np.select(choices, labels, default="General Merchandise"), index=series.index)


def generate_synthetic_dataset(rows: int = 900) -> pd.DataFrame:
    """Create a realistic fallback dataset with deterministic numpy seed 42."""
    rng = np.random.default_rng(42)
    products = np.array(["Headphones", "Desk Chair", "Air Fryer", "Laptop Stand", "Running Shoes"])
    categories = np.array(["Electronics", "Office Supplies", "Home & Kitchen", "Fashion", "Sports"])
    regions = np.array(["North", "South", "East", "West"])
    dates = pd.date_range("2024-01-01", "2025-04-30", freq="D")
    quantity = rng.integers(1, 6, rows)
    unit_price = rng.uniform(18, 620, rows).round(2)
    sales = (quantity * unit_price).round(2)
    profit = (sales * rng.uniform(0.12, 0.34, rows)).round(2)
    return pd.DataFrame(
        {
            "Order ID": [f"DEMO-{10000 + i}" for i in range(rows)],
            "Product": rng.choice(products, rows),
            "Category": rng.choice(categories, rows),
            "Sales": sales,
            "Profit": profit,
            "Quantity": quantity,
            "Region": rng.choice(regions, rows),
            "Customer Name": [f"Customer {n}" for n in rng.integers(100, 260, rows)],
            "Order Date": rng.choice(dates, rows),
        }
    )

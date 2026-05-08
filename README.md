# Plug-and-Play Analytics Dashboard

A self-service business intelligence web application that transforms raw sales data into an interactive executive dashboard with minimal setup. Built for small and medium businesses that need fast, actionable insights without a full BI infrastructure.

---

## Motivation

Small business teams often rely on CSV exports and Excel files to track sales performance. Existing BI tools either require expensive licenses or significant technical setup. This project addresses that gap by providing a lightweight, upload-and-explore analytics product that works directly with the data formats teams already use.

The core research question driving this project: *can a non-technical user go from a raw spreadsheet to a meaningful executive dashboard in under two minutes?*

---

## Features

**Data Ingestion**
- Upload CSV, Excel, JSON, TSV, or Parquet files
- Connect a live MySQL database
- Explore a built-in demo ecommerce dataset

**Intelligent Column Mapping**
- User maps required fields: Order Date, Sales, Product
- Optional fields (category, region, customer, profit, quantity, discount) enrich the analysis when available
- Sensible defaults ensure the dashboard renders even with incomplete data

**Core Analytics Modules**
- KPI summary — total revenue, order count, profit, average order value
- Monthly sales and profit trend analysis
- Top product rankings with revenue distribution
- Regional sales performance breakdown
- Category-level profitability comparison
- Customer segmentation using RFM (Recency, Frequency, Monetary) analysis
- Daily sales heatmap
- Filtered CSV export for offline review

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Web framework | Streamlit |
| Data processing | Pandas, NumPy |
| Visualization | Plotly |
| Database | MySQL |
| File formats | CSV, Excel, JSON, TSV, Parquet |

---

## Project Structure

```
.
├── app.py                  # Entry point and routing
├── landing.py              # Onboarding and data source selection
├── dashboard.py            # Main dashboard layout and charts
├── data_loader.py          # File parsing and MySQL connector
├── column_mapper.py        # Field mapping interface and validation
├── data/
│   └── ecommerce_sales_sample.csv
├── database/
│   ├── schema.sql          # Table definitions
│   ├── load_sample_data.sql
│   └── analytics_queries.sql
├── .streamlit/
│   └── config.toml         # Theme and layout config
├── requirements.txt
└── README.md
```

---

## Setup and Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/analytics-dashboard.git
cd analytics-dashboard
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the application**
```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.

---

## MySQL Setup (Optional)

**Create the schema**
```bash
mysql -u root -p < database/schema.sql
```

**Load sample data**
```bash
mysql --local-infile=1 -u root -p ecommerce_analytics < database/load_sample_data.sql
```

**Configure credentials via environment variables**
```bash
# Windows
set MYSQL_HOST=localhost
set MYSQL_PORT=3306
set MYSQL_DATABASE=ecommerce_analytics
set MYSQL_USER=root
set MYSQL_PASSWORD=your_password

# macOS / Linux
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_DATABASE=ecommerce_analytics
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
```

Reusable SQL queries for all analytics modules are in `database/analytics_queries.sql`.

---

## Design Approach

The interface follows a premium finance-product aesthetic — warm beige editorial theme, serif display typography, monospaced KPI numbers, and soft card shadows. The goal was a dashboard that reads as credible and production-ready, suitable for stakeholder presentations and founder demos.

---

## Future Work

- User authentication and saved dashboard workspaces
- Dynamic database table selection at runtime
- Scheduled email report delivery
- Time-series forecasting and anomaly detection
- Cohort retention analysis


---

## Author

Ananya Moharana — B.Tech(CSE), SOA University

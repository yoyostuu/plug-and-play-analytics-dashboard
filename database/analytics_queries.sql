USE ecommerce_analytics;

-- KPI summary: total sales, total profit, orders, and average order value.
SELECT
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM ecommerce_orders;

-- Monthly sales and profit trend.
SELECT
    DATE_FORMAT(order_date, '%Y-%m-01') AS month,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(DISTINCT order_id) AS orders
FROM ecommerce_orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m-01')
ORDER BY month;

-- Top-selling products by revenue and units sold.
SELECT
    product,
    ROUND(SUM(sales), 2) AS sales,
    SUM(quantity) AS units_sold
FROM ecommerce_orders
GROUP BY product
ORDER BY sales DESC
LIMIT 10;

-- Region-wise sales performance.
SELECT
    region,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(DISTINCT order_id) AS orders
FROM ecommerce_orders
GROUP BY region
ORDER BY sales DESC;

-- Profit analysis by category.
SELECT
    category,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS profit_margin_percent
FROM ecommerce_orders
GROUP BY category
ORDER BY profit DESC;

-- Customer segmentation source table.
SELECT
    customer_name,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units,
    MAX(order_date) AS last_order_date,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM ecommerce_orders
GROUP BY customer_name
ORDER BY total_sales DESC;

-- Example filtered query for dashboard controls.
SELECT
    order_id,
    product,
    category,
    sales,
    profit,
    quantity,
    region,
    customer_name,
    order_date
FROM ecommerce_orders
WHERE order_date BETWEEN '2024-01-01' AND '2025-12-31'
  AND region IN ('North', 'South', 'East', 'West')
  AND category IN ('Electronics', 'Fashion', 'Home & Kitchen', 'Office Supplies', 'Sports');

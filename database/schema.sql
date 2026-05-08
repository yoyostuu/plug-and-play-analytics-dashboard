CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

DROP TABLE IF EXISTS ecommerce_orders;

CREATE TABLE ecommerce_orders (
    order_id VARCHAR(20) PRIMARY KEY,
    product VARCHAR(120) NOT NULL,
    category VARCHAR(80) NOT NULL,
    sales DECIMAL(12, 2) NOT NULL,
    profit DECIMAL(12, 2) NOT NULL,
    quantity INT NOT NULL,
    region VARCHAR(40) NOT NULL,
    customer_name VARCHAR(120) NOT NULL,
    order_date DATE NOT NULL,
    INDEX idx_order_date (order_date),
    INDEX idx_region (region),
    INDEX idx_category (category)
);

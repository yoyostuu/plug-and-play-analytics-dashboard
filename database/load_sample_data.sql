USE ecommerce_analytics;

-- Option 1:
-- Use your MySQL client import wizard and map data/ecommerce_sales_sample.csv to ecommerce_orders.

-- Option 2:
-- Enable LOCAL INFILE in your MySQL client/server and run the command below.
-- Update the absolute CSV path for your machine before executing.

LOAD DATA LOCAL INFILE 'C:/Users/anamo/Documents/Codex/2026-05-08/build-a-complete-e-commerce-analytics/data/ecommerce_sales_sample.csv'
INTO TABLE ecommerce_orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@order_id, @product, @category, @sales, @profit, @quantity, @region, @customer_name, @order_date)
SET
    order_id = @order_id,
    product = @product,
    category = @category,
    sales = @sales,
    profit = @profit,
    quantity = @quantity,
    region = @region,
    customer_name = @customer_name,
    order_date = STR_TO_DATE(@order_date, '%Y-%m-%d');

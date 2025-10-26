CREATE OR REPLACE TABLE olist_fmt.sales AS
SELECT
  CAST(order_id           AS VARCHAR)       AS order_id,
  CAST(items_per_order    AS INTEGER)       AS items_per_order,
  CAST(price              AS DECIMAL(18,2)) AS price,
  CAST(freight_value      AS DECIMAL(18,2)) AS freight_value,
  CAST(order_total_value  AS DECIMAL(18,2)) AS order_total_value,
  CAST(seller_count       AS INTEGER)       AS seller_count,
  CAST(order_year         AS INTEGER)       AS order_year,
  CAST(order_month        AS VARCHAR)       AS order_month,
  CAST(order_dow          AS INTEGER)       AS order_dow
FROM olist.vw_sales;

CREATE OR REPLACE TABLE olist_fmt.logistics AS
SELECT
  CAST(v.order_id              AS VARCHAR)        AS order_id,
  CAST(v.delivery_days         AS DECIMAL(10,2))  AS delivery_days,
  CAST(v.estimated_days        AS DECIMAL(10,2))  AS estimated_days,
  CAST(v.delay_vs_estimated    AS DECIMAL(10,2))  AS delay_vs_estimated,
  CAST(v.late_days             AS DECIMAL(10,2))  AS late_days,
  CAST(v.on_time               AS BOOLEAN)        AS on_time,
  CAST(v.prep_hours            AS DECIMAL(10,2))  AS prep_hours,
  CAST(v.transit_days          AS DECIMAL(10,2))  AS transit_days,
  CAST(v.order_year            AS INTEGER)        AS order_year,
  CAST(v.order_month           AS VARCHAR)        AS order_month,
  CAST(v.order_week            AS INTEGER)        AS order_week,
  CAST(v.order_dow             AS INTEGER)        AS order_dow,
  CAST(v.purchase_hour         AS INTEGER)        AS purchase_hour,
  CAST(v.is_weekend_purchase   AS BOOLEAN)        AS is_weekend_purchase,
  CAST(v.delay_bucket          AS VARCHAR)        AS delay_bucket,
  CAST(v.delivery_days_bucket  AS VARCHAR)        AS delivery_days_bucket
FROM olist.vw_logistics AS v;

CREATE OR REPLACE TABLE olist_fmt.customer_satisfaction AS
SELECT
  CAST(order_id                    AS VARCHAR)    AS order_id,
  CAST(review_score                AS INTEGER)    AS review_score,
  CAST(review_creation_date        AS TIMESTAMP)  AS review_creation_date,
  CAST(review_answer_timestamp     AS TIMESTAMP)  AS review_answer_timestamp,
  CAST(review_after_delivery_hours AS INTEGER)    AS review_after_delivery_hours
FROM olist.vw_customer_satisfaction;

CREATE OR REPLACE TABLE olist_fmt.sellers AS
SELECT
  CAST(seller_id            AS VARCHAR)       AS seller_id,
  CAST(total_orders         AS INTEGER)       AS seller_orders,
  CAST(total_items          AS INTEGER)       AS seller_items,
  CAST(total_gmv            AS DECIMAL(18,2)) AS seller_gmv,
  CAST(avg_delivery_days    AS DECIMAL(10,2)) AS seller_avg_delivery_days,
  CAST(avg_delay            AS DECIMAL(10,2)) AS seller_avg_delay,
  CAST(avg_review_score     AS DECIMAL(10,2)) AS seller_avg_review
FROM olist.vw_sellers;

CREATE OR REPLACE TABLE olist_fmt.categories AS
SELECT
  CAST(product_category_name_english AS VARCHAR)     AS product_category_name_english,
  CAST(order_year                     AS INTEGER)     AS order_year,
  CAST(order_month                    AS VARCHAR)     AS order_month,
  CAST(category_items                 AS INTEGER)     AS category_items,
  CAST(category_orders                AS INTEGER)     AS category_orders,
  CAST(category_gmv                   AS DECIMAL(18,2)) AS category_gmv,
  CAST(category_freight               AS DECIMAL(18,2)) AS category_freight
FROM olist.vw_categories;

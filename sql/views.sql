-- VENTAS
CREATE OR REPLACE VIEW olist.vw_sales AS
SELECT
    i.order_id,
    i.item_count                               AS items_per_order,
    i.order_price_total                        AS price,
    i.order_freight_total                      AS freight_value,
    (i.order_price_total + i.order_freight_total) AS order_total_value,
    i.seller_count,
    o.order_year, o.order_month, o.order_dow
FROM olist.items i
LEFT JOIN olist.orders o USING(order_id);

-- LOGÍSTICA 
CREATE OR REPLACE VIEW olist.vw_logistics AS
SELECT
    order_id,
    delivery_days,
    estimated_days,
    delay_vs_estimated,
    late_days,
    on_time,
    CASE 
        WHEN prep_hours < 0 THEN NULL
        ELSE prep_hours
    END AS prep_hours,
    transit_days,
    order_year, order_month, order_week, order_dow,
    purchase_hour, is_weekend_purchase,
    delay_bucket, delivery_days_bucket,
    -- Columna indicadora para análisis
    CASE WHEN delivery_days IS NOT NULL THEN true ELSE false END AS was_delivered
FROM olist.orders;

-- SATISFACCIÓN 
CREATE OR REPLACE VIEW olist.vw_customer_satisfaction AS
SELECT
  r.order_id,
  r.review_score,
  CAST(r.review_creation_date    AS TIMESTAMP) AS review_creation_date,
  CAST(r.review_answer_timestamp AS TIMESTAMP) AS review_answer_timestamp,
  CASE
    WHEN o.order_delivered_customer_date IS NULL THEN NULL
    ELSE GREATEST(
      date_diff('hour',
        CAST(o.order_delivered_customer_date AS TIMESTAMP),
        CAST(r.review_creation_date          AS TIMESTAMP)
      ), 0)
  END AS review_after_delivery_hours
FROM olist.reviews r
LEFT JOIN olist.orders o USING(order_id);

-- VENDEDORES
CREATE OR REPLACE VIEW olist.vw_sellers AS
WITH base AS (
  SELECT
      s.seller_id,
      COUNT(DISTINCT oi.order_id)                    AS total_orders,
      COUNT(oi.order_item_id)                        AS total_items,
      SUM(oi.price + oi.freight_value)               AS total_gmv,
      AVG(o.delivery_days)                           AS avg_delivery_days,
      AVG(o.delay_vs_estimated)                      AS avg_delay,
      AVG(r.review_score)                            AS avg_review_score
  FROM olist.sellers s
  LEFT JOIN olist.order_items oi ON s.seller_id = oi.seller_id
  LEFT JOIN olist.orders o       ON oi.order_id = o.order_id
  LEFT JOIN olist.reviews r      ON oi.order_id = r.order_id
  GROUP BY s.seller_id
  HAVING COUNT(DISTINCT oi.order_id) > 0
)
SELECT * FROM base;

-- CATEGORÍAS POR MES
CREATE OR REPLACE VIEW olist.vw_categories AS
WITH items_cat AS (
  SELECT
    oi.order_id, oi.product_id, oi.price, oi.freight_value,
    o.order_purchase_timestamp,
    CAST(strftime(o.order_purchase_timestamp, '%Y-%m') AS VARCHAR) AS order_month,
    EXTRACT(YEAR FROM o.order_purchase_timestamp)                  AS order_year,
    p.product_category_name_english
  FROM olist.order_items oi
  LEFT JOIN olist.orders      o ON oi.order_id  = o.order_id
  LEFT JOIN olist.products_en p ON oi.product_id = p.product_id
)
SELECT
  product_category_name_english,
  order_year,
  order_month,
  COUNT(*)                 AS category_items,
  COUNT(DISTINCT order_id) AS category_orders,
  SUM(price)               AS category_gmv,
  SUM(freight_value)       AS category_freight
FROM items_cat
GROUP BY 1,2,3
ORDER BY 2,3,1;

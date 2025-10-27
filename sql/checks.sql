CREATE SCHEMA IF NOT EXISTS olist_meta;

-- Claves obligatorias no nulas
CREATE OR REPLACE VIEW olist_meta.qc_null_keys AS
SELECT 'olist_fmt.sales' AS table_name, COUNT(*) AS null_keys
FROM olist_fmt.sales WHERE order_id IS NULL
UNION ALL
SELECT 'olist_fmt.logistics', COUNT(*) FROM olist_fmt.logistics WHERE order_id IS NULL
UNION ALL
SELECT 'olist_fmt.customer_satisfaction', COUNT(*) FROM olist_fmt.customer_satisfaction WHERE order_id IS NULL;


-- Montos no negativos
CREATE OR REPLACE VIEW olist_meta.qc_negative_amounts AS
SELECT 'olist_fmt.sales' AS table_name, COUNT(*) AS invalid_rows
FROM olist_fmt.sales WHERE price < 0 OR freight_value < 0 OR order_total_value < 0
UNION ALL
SELECT 'olist_fmt.categories', COUNT(*)
FROM olist_fmt.categories WHERE category_gmv < 0 OR category_freight < 0;

-- Reglas de negocio: review_after_delivery_hours >= 0
CREATE OR REPLACE VIEW olist_meta.qc_review_after_delivery AS
SELECT COUNT(*) AS invalid_reviews
FROM olist_fmt.customer_satisfaction
WHERE review_after_delivery_hours < 0;

-- Muestra
SELECT * FROM olist_meta.qc_null_keys;
SELECT * FROM olist_meta.qc_negative_amounts;
SELECT * FROM olist_meta.qc_review_after_delivery;

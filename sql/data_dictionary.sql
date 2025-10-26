COPY (
  SELECT
    table_schema,
    table_name,
    column_name,
    ordinal_position,
    data_type,
    is_nullable
  FROM information_schema.columns
  WHERE table_schema IN ('olist', 'olist_fmt')
  ORDER BY table_schema, table_name, ordinal_position
) TO 'data/dictionary/data_dictionary.csv'
WITH (HEADER, DELIMITER ',');

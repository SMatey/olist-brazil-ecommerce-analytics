# src/pipeline/02_load_staging.py
import sys, os, duckdb
import pandas as pd
from pathlib import Path

print("Realizando carga a staging (DuckDB)...")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FEATURES_DIR = PROJECT_ROOT / "data" / "features"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROJECT_ROOT / "db" / "olist_analytics.duckdb"
os.makedirs(DB_PATH.parent, exist_ok=True)

# Conectar a DuckDB
print(f"  Conectando a base de datos: {DB_PATH}")
con = duckdb.connect(str(DB_PATH), read_only=False)
con.execute("CREATE SCHEMA IF NOT EXISTS olist")

try:
    print("  Cargando dataframes de features y processed...")
    # Cargar features (de construccion.ipynb)
    orders  = pd.read_csv(FEATURES_DIR / "features_orders.csv", parse_dates=[
        "order_purchase_timestamp","order_approved_at","order_delivered_carrier_date",
        "order_delivered_customer_date","order_estimated_delivery_date"
    ])
    items   = pd.read_csv(FEATURES_DIR / "features_items_agg.csv")
    reviews = pd.read_csv(FEATURES_DIR / "features_reviews.csv", parse_dates=[
        "review_creation_date","review_answer_timestamp"
    ])
    products_en = pd.read_csv(FEATURES_DIR / "features_products_enriched.csv")
    
    # Cargar datos limpios (de notebooks de limpieza)
    order_items = pd.read_csv(PROCESSED_DIR / "olist_order_items_clean.csv")
    sellers = pd.read_csv(PROCESSED_DIR / "olist_sellers_clean.csv")

    # Registrar dataframes en DuckDB y crear tablas permanentes en 'olist'
    to_persist = {
        "orders": orders, "items": items, "reviews": reviews,
        "order_items": order_items, "sellers": sellers, "products_en": products_en
    }
    
    print("  Creando tablas en esquema 'olist' (staging)...")
    for name, df in to_persist.items():
        print(f"    -> olist.{name}")
        con.sql(f"CREATE OR REPLACE TABLE olist.{name} AS SELECT * FROM df")

    print("  Tablas de staging creadas exitosamente.")

except FileNotFoundError as e:
    print(f"[ERROR] No se encontró el archivo: {e.filename}")
    print("  Asegúrate que el [Paso 1] (01_run_notebooks.py) se haya ejecutado correctamente.")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Ocurrió un error durante la carga a DuckDB: {e}")
    sys.exit(1)
finally:
    con.close()
    print("  Conexión a DuckDB cerrada.")

print("Carga a Staging completada.")
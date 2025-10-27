# src/infraestructura_bd/run_infra.py
from pathlib import Path
import duckdb

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SQL_DIR = ROOT / "sql"
DB_PATH = ROOT / "db" / "olist_analytics.duckdb"  

SQL_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

ORDER = [
    "schemas.sql",
    "views.sql",
    "tables.sql",
    "checks.sql",
    "data_dictionary.sql",
]

print(f"ROOT:    {ROOT}")
print(f"SQL_DIR: {SQL_DIR}")
print(f"DB:      {DB_PATH}")

con = duckdb.connect(str(DB_PATH), read_only=False)

for fname in ORDER:
    fpath = SQL_DIR / fname
    if not fpath.exists():
        print(f"[WARN] No existe: {fpath} (se omite)")
        continue
    print(f"\n>>> Ejecutando {fname}")
    sql = fpath.read_text(encoding="utf-8")
    con.execute(sql) 

con.close()
print("\nInfraestructura reconstruida.")
print("\nIniciando exportación de VISTAS 'olist.vw_*' a CSV/Parquet...")
con = duckdb.connect(str(DB_PATH), read_only=True)
OUT_DIR_VIEWS = ROOT / "data" / "views"
OUT_DIR_VIEWS.mkdir(parents=True, exist_ok=True)

views_to_export = [
    "vw_sales",
    "vw_logistics",
    "vw_customer_satisfaction",
    "vw_sellers",
    "vw_categories"
]

for view_name in views_to_export:
    # Definir rutas de salida
    parquet_path = (OUT_DIR_VIEWS / f"{view_name}.parquet").resolve()
    csv_path = (OUT_DIR_VIEWS / f"{view_name}.csv").resolve()
    
    print(f"  Exportando olist.{view_name}...")
    
    # Exportar a Parquet (como en integracion.ipynb)
    try:
        con.execute(f"""
            COPY (SELECT * FROM olist.{view_name})
            TO '{parquet_path}'
            (FORMAT PARQUET, COMPRESSION 'zstd');
        """)
    except Exception as e:
        print(f"  [ERROR] Falló la exportación Parquet de {view_name}: {e}")

    # Exportar a CSV (como en integracion.ipynb)
    try:
        con.execute(f"""
            COPY (SELECT * FROM olist.{view_name})
            TO '{csv_path}'
            (FORMAT CSV, HEADER);
        """)
    except Exception as e:
        print(f"  [ERROR] Falló la exportación CSV de {view_name}: {e}")

con.close()
print("Exportación de VISTAS completada.")

print("\nIniciando exportación de tablas 'olist_fmt' a Parquet...")
con = duckdb.connect(str(DB_PATH), read_only=True)

# Directorio de salida
OUT_DIR_FMT = ROOT / "data" / "formatted"
OUT_DIR_FMT.mkdir(parents=True, exist_ok=True)

tables_to_export = [
    "sales",
    "logistics",
    "customer_satisfaction",
    "sellers",
    "categories"
]

for table_name in tables_to_export:
    parquet_path = (OUT_DIR_FMT / f"{table_name}.parquet").resolve()
    print(f"  Exportando olist_fmt.{table_name} -> {parquet_path}")
    
    try:
        con.execute(f"""
            COPY (SELECT * FROM olist_fmt.{table_name})
            TO '{parquet_path}'
            (FORMAT PARQUET, COMPRESSION 'zstd');
        """)
    except Exception as e:
        print(f"  [ERROR] Falló la exportación de {table_name}: {e}")

con.close()
print("Exportación a Parquet completada.")
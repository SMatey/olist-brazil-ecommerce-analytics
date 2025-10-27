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

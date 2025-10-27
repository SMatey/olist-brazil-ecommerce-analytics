# src/pipeline/01_run_notebooks.py
import os
import subprocess
import sys
from pathlib import Path

print("Iniciando ejecucion de notebooks (Limpieza y Construccion)...")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

NOTEBOOKS_TO_RUN = [
    # Notebooks de limpieza de datos
    "limpieza/01_orders.ipynb",
    "limpieza/02_order_items.ipynb",
    "limpieza/03_order_payments.ipynb",
    "limpieza/04_order_reviews.ipynb",
    "limpieza/05_customers.ipynb",
    "limpieza/06_products.ipynb",
    "limpieza/07_sellers.ipynb",
    "limpieza/08_cat_tr.ipynb",

    # Notebooks de construcción de datos
    "construccion/construccion.ipynb"
]

# Se ejecutan los notebooks en el orden definido
for nb_relative_path in NOTEBOOKS_TO_RUN:
    nb_full_path = NOTEBOOKS_DIR / nb_relative_path
    
    if not nb_full_path.exists():
        print(f"  [AVISO] No se encontro el notebook, se omite: {nb_relative_path}")
        continue
    
    print(f"\n  Ejecutando: {nb_relative_path}...")
    
    command = [
        "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=-1",
        str(nb_full_path)
    ]
    
    try:
        result = subprocess.run(
            command, 
            cwd=NOTEBOOKS_DIR,
            capture_output=True, 
            text=True, 
            check=True,
            encoding='utf-8'
        )
        print(f"    -> Exito! Notebook ejecutado: {nb_relative_path}")
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Fallo la ejecución de {nb_relative_path}!")
        print(f"  (stderr): {e.stderr}")
        print("  Saliendo del pipeline.")
        sys.exit(1)

print("\nEjecucion de Notebooks completada.")
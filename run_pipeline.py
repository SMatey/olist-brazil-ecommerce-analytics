import subprocess
import sys
from pathlib import Path

print("=== INICIANDO PIPELINE DE DATOS OLIST ===")

ROOT = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable

print("  Asegurando que existan todos los directorios de salida...")
try:
    (ROOT / "data" / "processed").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "features").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "dictionary").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "views").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "formatted").mkdir(parents=True, exist_ok=True)
    (ROOT / "db").mkdir(parents=True, exist_ok=True)
    print("  Directorios de salida listos.")
except Exception as e:
    print(f"  [ERROR] No se pudieron crear los directorios: {e}")
    sys.exit(1)
    
# Lista de scripts a ejecutar en orden
scripts = [
    "src/pipeline/run_notebooks.py",
    "src/pipeline/load_staging.py",
    "src/infraestructura_bd/run_infra.py"
]

# Bucle a través de cada script y ejecutarlo
for script_path in scripts:
    script_full_path = ROOT / script_path
    
    if not script_full_path.exists():
        print(f"\n[ERROR] No se encontró el script: {script_path}")
        print("  Saliendo del pipeline.")
        sys.exit(1)

    print(f"\n--- Ejecutando: {script_path} ---")
    
    try:
        result = subprocess.run(
            [PYTHON_EXE, str(script_full_path)], 
            check=True
        )
        # Imprime la salida del script
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR FATAL] El script {script_path} falló.")
        print("--- Salida de Error (stderr): ---")
        print(e.stderr)
        print("---------------------------------")
        print("  SALIENDO DEL PIPELINE.")
        sys.exit(1) # Detiene todo el pipeline
    
    print(f"--- Fin de: {script_path} ---")

print("=== PIPELINE DE DATOS COMPLETADO CON ÉXITO ===")
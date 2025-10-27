# olist-brazil-ecommerce-analytics

Proyecto de curso **IC-8076 – Introducción al Análisis de Datos (TEC)** basado en el dataset público **Olist Brazilian E-commerce**. Aplicamos la metodología **CRISP-DM** para construir un pipeline reproducible de datos, medir KPIs operativos (logística, satisfacción, ventas) y comunicar hallazgos con buenas prácticas de visualización.

> **Alcance Parte I**: Comprensión del negocio + Comprensión de los datos (incluye `notebooks/01_eda.ipynb`, bibliografía APA 7 y documentación de calidad de datos).

---

## ✳️ Objetivo del proyecto

Habilitar análisis accionables para Olist y sus *stakeholders* (PyMEs vendedoras, clientes y operación de la plataforma) mediante:

- **Logística**: `delivery_days`, `delay_vs_estimated`, `% on_time`.
- **Satisfacción**: `review_score` y reseñas bajas (≤ 2) vs. desempeño logístico.
- **Ventas y portafolio**: AOV (ticket promedio) y categorías top + estacionalidad.
- **Vendedores**: segmentación operativa por volumen, rapidez y calificación.

---

## 🧭 Metodología (CRISP-DM)

1) **Comprensión del negocio**  
2) **Comprensión de los datos** 
3) **Preparación de los datos**  
4) **Modelado (arquitectura/pipeline de datos, no ML)**  
5) **Evaluación** (pruebas, validación, optimización)  
6) **Despliegue/Comunicación** (notebooks “limpios” y, opcional, Streamlit)

---

## 🧱 Estructura base del repositorio

```
data/
  raw/            # CSV originales de Olist
  processed/      # integraciones intermedias
  features/       # atributos derivados
  formatted/      # salidas tipadas para BI
  dictionary/     # artefactos de diccionario de datos
  views/          # exportes de vistas (CSV/Parquet)
db/
  olist_analytics.duckdb   # base analítica local (DuckDB)
figures/                   # gráficos exportados
notebooks/
  01_eda.ipynb
  construccion/
  formateo/
  integracion/
  limpieza/
sql/                       # scripts SQL del proyecto
src/
  db/infraestructura_bd/run_infra.py
  olistrep/data_cleaning.py
pipeline/
  load_staging.py
  run_notebooks.py
requirements.txt
run_pipeline.py
README.md
```

> **Nota**: trabajamos **sin** `geolocation` para esta versión. Los cortes geográficos serán por **estado/ciudad** desde `customers`/`sellers`.  
> Además, las vistas de negocio se exportan a `data/views/` como CSV/Parquet para consumo externo.

---

## 🧰 Tecnologías y herramientas

- **Python 3.11**, **Jupyter/Colab**
- **pandas**, **numpy**, **python-dateutil**
- **DuckDB** (archivo local) para SQL analítico y joins rápidos
- **matplotlib** (estático) y **plotly.express** (interactivo para EDA)
- **openpyxl** (exportes a Excel)
- **Mermaid/draw.io** para ER y flujo
- **Streamlit** (opcional) para dashboard local
- **Git/GitHub** para versionamiento
- Arquitectura **Lakehouse** con patrón **Medallion** (Bronze=`data/raw`, Silver=`data/processed`/`features`, Gold=tablas/vistas en DuckDB + exportes `formatted/` y `views/`)

---

## ⚙️ Configuración rápida

### Opción A — Local (recomendado para entregables)
```bash
# 1) Crear entorno
python -m venv .venv
# Activar: Windows
.venv\Scripts\activate
# Activar: macOS/Linux
source .venv/bin/activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Abrir Jupyter
jupyter notebook
```

### Opción B — Google Colab
1. Sube/clona el repo en tu Drive (o sincroniza `data/raw/`).  
2. Abre `notebooks/01_eda.ipynb` en Colab.  
3. La primera celda fija versiones y usa rutas para Drive si detecta Colab.

---

## ▶️ Ejecución mínima (Parte I)

1. Coloca los CSV de Olist en `data/raw/`:
   - `olist_orders_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_order_payments_dataset.csv`
   - `olist_order_reviews_dataset.csv`
   - `olist_customers_dataset.csv`
   - `olist_products_dataset.csv`
   - `olist_sellers_dataset.csv`
   - `product_category_name_translation.csv`

2. Ejecuta **`notebooks/01_eda.ipynb`** de inicio a fin.  
   - Crea vistas de lectura en DuckDB.  
   - Genera reportes de **nulos**, **PK/FK**, **reglas temporales** y **log de calidad**.  
   - Exporta resúmenes a `data/processed/`.

---

## 🚀 Ejecución end-to-end (pipeline)

```bash
# desde la raíz del repo (entorno activado e instalaciones hechas)
python run_pipeline.py
```

El pipeline es **idempotente** y orquesta:
1. Preparación de carpetas/salidas.  
2. Limpieza e integración (notebooks / `run_notebooks.py`).  
3. Carga a **DuckDB** (staging) con `pipeline/load_staging.py`.  
4. **Infraestructura SQL** con `src/db/infraestructura_bd/run_infra.py`:
   - creación de esquemas/tablas/vistas formateadas,
   - checks de calidad y
   - generación de diccionario/exportes (`formatted/`, `views/`).

---

## 📏 KPIs operativos (definiciones)

- **`delivery_days`** = `delivered_ts − purchase_ts` (días)  
- **`delay_vs_estimated`** = `delivered_ts − estimated_ts` (≤ 0 → a tiempo)  
- **`on_time`** = 1 si `delivered_ts ≤ estimated_ts`, si no 0  
- **`AOV`** (ticket promedio) = Σ `price` / # órdenes  
- **Reseña baja** = `review_score ≤ 2`

> Los KPIs se calculan desde vistas reproducibles en DuckDB y/o agregaciones en pandas. Las fórmulas y consultas quedarán trazables en los notebooks.

---

## 🔒 Alcance y limitaciones

- Sin `geolocation`: cortes por **estado/ciudad** (no distancias físicas).  
- No se modela rentabilidad (no hay costos/márgenes), sí **tiempos** y **cumplimiento de promesa**.  
- Textos de reseñas son esporádicos; el análisis principal usa **`review_score`**.

---

## 📚 Referencias (APA 7)

- Olist. (s. f.). *Olist – Plataforma para e-commerce*. https://www.olist.com  
- Meta IT. (s. f.). *Olist enhances its sales channel through digital transformation*. https://metait.ai/cases/olist  
- Bloomberg Línea. (2021, diciembre 15). *Olist se convierte en el nuevo unicornio de Brasil tras recaudar $186 millones en nueva ronda*. https://www.bloomberglinea.com/2021/12/15/olist-se-convierte-en-el-nuevo-unicornio-de-brasil-tras-recaudar-us186-millones-en-nueva-ronda/  
- Olist. (s. f.). *Brazilian E‑Commerce Public Dataset by Olist* [Conjunto de datos]. Kaggle. https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

---
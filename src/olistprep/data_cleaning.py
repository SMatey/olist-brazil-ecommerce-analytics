import pandas as pd
import numpy as np

# Función para eliminar duplicados
def remove_duplicates(df, date_column):
    """Elimina duplicados y mantiene el registro más reciente según el campo de fecha"""
    df_sorted = df.sort_values(by=date_column, ascending=False)
    return df_sorted.drop_duplicates(subset=['order_id'], keep='first')

# Función para rellenar valores nulos
def fill_missing_values(df):
    """Rellena valores nulos según las reglas especificadas: 
    - Categóricos: 'Unknown' o valor encontrado en otros registros.
    - Numéricos: Mediana.
    - Fechas: Eliminar filas con fechas nulas."""
    
    for column in df.columns:
        if df[column].dtype == 'object':  # Categóricos
            df[column] = df[column].fillna('Unknown')
        elif df[column].dtype in ['int64', 'float64']:  # Numéricos
            df[column] = df[column].fillna(df[column].median())
        elif pd.api.types.is_datetime64_any_dtype(df[column]):  # Fechas
            df[column] = df[column].dropna()  # Eliminar registros con fechas nulas
    
    return df

# Función para eliminar outliers (valores extremos)
def remove_outliers(df: pd.DataFrame,
                           numeric_columns: list[str] | None = None,
                           threshold: float = 3.0) -> pd.DataFrame:
    """
    Elimina filas que tengan outliers (|z| > threshold) en AL MENOS una
    columna numérica. Calcula z-scores una sola vez usando la media y
    desviación estándar del DataFrame original.

    Parámetros
    ----------
    df : DataFrame de entrada (no se modifica in-place).
    numeric_columns : lista de columnas numéricas a evaluar. Si None, detecta automáticamente.
    threshold : umbral de z-score (por defecto 3.0).

    Retorna
    -------
    DataFrame limpio con las filas sin outliers.
    """
    if numeric_columns is None:
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_columns:
        return df.copy()

    # Subconjunto numérico
    X = df[numeric_columns].copy()

    # Media y desviación (ddof=0 para evitar NaNs con tamaños pequeños)
    mu = X.mean()
    sigma = X.std(ddof=0)

    # Evitar división por 0 en columnas constantes
    sigma = sigma.replace(0, np.nan)

    # z-scores vectorizados
    Z = (X - mu) / sigma

    # Fila es outlier si ALGUNA columna tiene |z| > threshold
    mask_outlier_any = Z.abs().gt(threshold).any(axis=1)

    # Filtrar manteniendo las no-outliers
    df_clean = df.loc[~mask_outlier_any].copy()
    return df_clean

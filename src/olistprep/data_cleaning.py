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
            df[column] = df[column].fillna(df[column].mean())
        elif pd.api.types.is_datetime64_any_dtype(df[column]):  # Fechas
            df[column] = df[column].dropna()  
    
    return df

# Función para eliminar outliers (valores extremos)
def remove_outliers(
    df: pd.DataFrame,
    numeric_columns: list[str] | None = None,
    threshold: float = 3.0,
    ddof: int = 1,
    return_removed_index: bool = False,
) -> pd.DataFrame | tuple[pd.DataFrame, pd.Index]:
    """
    Elimina filas que tengan outliers (|z| > threshold) en AL MENOS una columna numérica.
    Calcula z-scores una sola vez usando media y desviación estándar del df recibido.

    Parámetros
    ----------
    df : DataFrame de entrada (no se modifica in-place).
    numeric_columns : columnas numéricas a evaluar. Si None, se detectan automáticamente.
    threshold : umbral de z-score (por defecto 3.0).
    ddof : grados de libertad para std (1 = default pandas.describe).
    return_removed_index : si True, también devuelve el índice de filas eliminadas.

    Retorna
    -------
    DataFrame limpio (y opcionalmente el índice de filas eliminadas).
    """
    
    if numeric_columns is None:
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_columns:
        return (df.copy(), pd.Index([])) if return_removed_index else df.copy()

    X = df[numeric_columns].copy()

    # Reemplazar inf/-inf y dejar NaN (no contarán como outliers)
    X = X.replace([np.inf, -np.inf], np.nan)

    # Media y desviación (ignora NaN). ddof=1 alinea con pandas.describe()
    mu = X.mean()
    sigma = X.std(ddof=ddof)

    # Evitar división por 0 en columnas constantes
    sigma = sigma.replace(0, np.nan)

    # Z-score vectorizado
    Z = (X - mu) / sigma

    # Fila outlier si alguna col tiene |z| > threshold
    mask_outlier_any = Z.abs().gt(threshold).any(axis=1)

    df_clean = df.loc[~mask_outlier_any].copy()
    removed_idx = df.index[mask_outlier_any]

    if return_removed_index:
        return df_clean, removed_idx
    return df_clean
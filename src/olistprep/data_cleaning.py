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
def remove_outliers(df, numeric_columns, threshold=3):
    """Elimina outliers basados en desviaciones estándar (threshold por defecto 3)."""
    for col in numeric_columns:
        mean = df[col].mean()
        std_dev = df[col].std()
        df = df[(df[col] >= mean - threshold * std_dev) & (df[col] <= mean + threshold * std_dev)]
    return df

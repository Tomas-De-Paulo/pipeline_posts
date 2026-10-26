"""Modulo de exportacion: escribe el resultado en los formatos de salida"""
import sqlite3
from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger('pipeline.exportar')

def exportar(df: pd.DataFrame, carpeta: str = "output") -> None:
    """Exportar el DataFrame a Parquet, CSV y una tabla SQLite"""
    destino = Path(carpeta)
    destino.mkdir(exist_ok=True)

    # Formatos planos
    df.to_parquet(destino / 'posts_enriquesidos.parquet', index=False)
    df.to_csv(destino / 'post_enriquesidos.csv', index=False)

    # Tabla para el equipo de BI
    with sqlite3.connect(destino / 'posts.db') as conn:
        df.to_sql('post_enriquesidos', conn, if_exists='replace', index=False)
        conn.commit()

    logger.info(f"Exportados {len(df)} posts a {destino}/ (parquet, csv, sqlite)")
    
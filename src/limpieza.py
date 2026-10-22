"""Modulo de limpieza: transforma datos crudos en datos usables."""
import pandas as pd
import logging

logger = logging.getLogger('pipeline.limpieza')

def merge_posts_usuarios(posts: pd.DataFrame, usuarios: pd.DataFrame) -> pd.DataFrame:
    """Combina posts con informacion del autos"""
    logger.info(f"Combinando {len(posts)} posts con {len(usuarios)} usuarios...")
    df = posts.merge(usuarios, on = 'user_id', how = 'left')
    sin_autor = df['autor_nombre'].isnull().sum()
    if sin_autor > 0:
        logger.warning(f"{sin_autor} posts sin autor asociado")
    return df 

def limpiar_posts(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia el DataFrame de posts enriquecido"""
    df = df.copy()
    filas_antes = len(df)
    logger.info(f"Limpiando {filas_antes} posts...")

    # 1. Eliminar duplicados
    df = df.drop_duplicates(subset = ['post_id'], keep = 'first')

    # 2. Eliminar posts sin titulo
    df = df.dropna(subset = ['title'])

    # 3. Normalizar texto
    df['title'] = df['title'].str.strip().str.capitalize()
    df['autor_nombre'] = df['autor_nombre'].str.strip().str.title()
    df['autor_ciudad'] = df['autor_ciudad'].fillna('Desconocida').str.strip().str.title()

    # 4. Crear columna de longitud del body (metrica util)
    df['body_length'] = df['body'].str.len()

    # 5. Eliminar columna email (PII - no la necesitamos en el output)
    if 'email' in df.columns:
        df = df.drop(columns = ['email'])


    filas_despues = len(df)
    logger.info(f"Limpieza completa: {filas_antes} -> {filas_despues} filas")

    return df.reset_index(drop = True)

"""Modulo de validacion: reglas de calidad que los datos DEBEN cumplir"""
import pandas as pd
import logging

logger = logging.getLogger('pipeline.validacion')


class ValidacionError(Exception):
    """Los datos no pasan las reglas de calidad"""
    pass

def validad_posts(df: pd.DataFrame) -> None:
    """Validar el DataFrame de posts contra reglas de calidad."""
    errores = []

    # Regla 1: No vacio
    if df.empty:
        errores.append("DataFrame vacio")

    # Regla 2: Columnas obligatorias
    columnas_requeridas = {'post_id', 'title', 'body', 'user_id', 'autor_nombre'}
    faltantes = columnas_requeridas - set(df.columns)
    if faltantes:
        errores.append(f"Columnas faltantes: {faltantes}")

    # Si faltan columnas, las reglas siguientes no se puede evaluar
    if errores:
        msg = "Validacion fallida:\n" + "\n".join(f"  - {e}" for e in errores)
        logger.error(msg)

    # A partir de aca las columnas existen
    # Regla 3: Sin duplicados en post_id
    duplicados = df['post_id'].duplicated().sum()
    if duplicados > 0:
        errores.append(f"{duplicados} post_id duplicados")

    # Regla 4: Titulos no vacios
    titulos_vacios = df['title'].str.strip().eq('').sum()
    if titulos_vacios > 0:
        errores.append(f"{titulos_vacios} titulos vacios")

    # Regla 5: body_length razonable (> 0)
    if 'body_length' in df.columns:
        bodies_vacios = (df['body_length'] == 0).sum()
        if bodies_vacios > 0:
            errores.append(f"{bodies_vacios} posts con body vacio")

    if errores:
        msg = "Validacion fallida:\n" + "\n".join(f"  - {e}" for e in errores)
        logger.error(msg)
        raise ValidacionError(msg)

    logger.info(f"Validacion exitosa: {len(df)} posts pasan todas las reglas")
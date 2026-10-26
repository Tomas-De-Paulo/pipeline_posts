"""Pipeline principal: orquesta todos los pasos"""
import logging
import time
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('pipeline')

from ingesta import ingerir_posts, ingerir_usuarios
from limpieza import merge_posts_usuarios, limpiar_posts
from validacion import validar_posts

def ejecutar():
    """Ejecutar el pipeline completo"""
    inicio = time.time()
    logger.info("=" * 50)
    logger.info("INICIO: Pipeline de posts enriquesidos")
    logger.info("=" * 50)

    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    try:
        # 1. Ingesta
        usuarios = ingerir_usuarios()
        posts = ingerir_posts()

        # 2. Merge
        df = merge_posts_usuarios(posts, usuarios)

        # 3. Limpieza 
        df = limpiar_posts(df)

        # 4. Validacion 
        validar_posts(df)

        # 5. Exportar
        parquet_path = output_dir / 'posts_enriquesidos.parquet'
        csv_path = output_dir / 'posts_enriquesidos.csv'

        df.to_parquet(parquet_path, index=False)
        df.to_csv(csv_path, index=False)

        duracion = time.time() - inicio
        logger.info(f"Exportados {len(df)} posts a {parquet_path}")
        logger.info(f"EXITO: Pipeline completado en {duracion:.1f}s")
        logger.info("=" * 50)

        return df

    except Exception as e:
        duracion = time.time() - inicio
        logger.critical(f"FALLO tras {duracion:.1f}s: {type(e).__name__}: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    ejecutar()
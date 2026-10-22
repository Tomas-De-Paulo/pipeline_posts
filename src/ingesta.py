"""Modulo de ingesta: extrae datos de APIs externas"""

import requests
import pandas as pd
import logging
import time

logger = logging.getLogger('pipeline.ingesta')

def pedir_con_reintentos(url: str, max_intentos: int = 3) -> list:
    """"Peticion GET robusta con reintentos y backoff exponencial"""
    for intento in range(max_intentos):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException) as e:
            if intento < max_intentos - 1:
                esperar = 2 ** intento
                logger.warning(f"Intento {intento + 1} fallido: {e}. Esperando{esperar}s...")
                time.sleep(esperar)
            else:
                logger.error(f"Todos los intentos fallaron para URL: {url}")
                raise

def ingerir_usuarios() -> pd.DataFrame:
    """"Ingiere usuarios de JSONPlaceholder."""
    logger.info("Ingiriendo usuarios...")
    data = pedir_con_reintentos("https://jsonplaceholder.typicode.com/users")
    df = pd.json_normalize(data, sep='_')
    df = df[['id', 'name', 'email', 'address_city', 'company_name']].rename(columns={
        'id': 'user_id',
        'name': 'autor_nombre',
        'address_city': 'autor_ciudad',
        'company_name': 'autor_empresa'
    })
    logger.info(f"Ingeridos {len(df)} usuarios")
    return df

def ingerir_posts() -> pd.DataFrame:
    """Ingiere posts de JSONPlaceholder."""
    logger.info("Ingeriendo posts...")
    data = pedir_con_reintentos('https://jsonplaceholder.typicode.com/posts')
    df = pd.DataFrame(data)
    df = df.rename(columns={
        'userId': 'user_id',
        'id': 'post_id' 
    })
    logger.info(f"Ingeridos {len(df)} posts")
    return df
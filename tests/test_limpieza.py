"""Tests para el módulo de limpieza."""
import pandas as pd
import pytest
from src.limpieza import limpiar_posts, merge_posts_usuarios


@pytest.fixture
def df_posts_raw():
    return pd.DataFrame({
        'post_id': [1, 2, 3],
        'user_id': [1, 1, 2],
        'title': ['  hello world  ', 'SECOND POST', 'third'],
        'body': ['Content one', 'Content two', 'Content three'],
        'autor_nombre': ['  john doe  ', '  john doe  ', 'jane smith'],
        'autor_ciudad': [None, 'New York', '  boston  '],
        'autor_empresa': ['Corp A', 'Corp A', 'Corp B']
    })


def test_limpiar_normaliza_titulos(df_posts_raw):
    resultado = limpiar_posts(df_posts_raw)
    assert resultado['title'].tolist() == ['Hello world', 'Second post', 'Third']


def test_limpiar_ciudad_nula_es_desconocida(df_posts_raw):
    resultado = limpiar_posts(df_posts_raw)
    assert 'Desconocida' in resultado['autor_ciudad'].values


def test_limpiar_crea_body_length(df_posts_raw):
    resultado = limpiar_posts(df_posts_raw)
    assert 'body_length' in resultado.columns
    assert (resultado['body_length'] > 0).all()


def test_limpiar_sin_duplicados():
    df = pd.DataFrame({
        'post_id': [1, 1, 2],
        'user_id': [1, 1, 2],
        'title': ['A', 'A duplicado', 'B'],
        'body': ['x', 'x', 'y'],
        'autor_nombre': ['Ana', 'Ana', 'Carlos'],
        'autor_ciudad': ['Madrid', 'Madrid', 'Barcelona'],
        'autor_empresa': ['X', 'X', 'Y']
    })
    resultado = limpiar_posts(df)
    assert len(resultado) == 2
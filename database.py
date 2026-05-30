# database.py
"""
Módulo para gerenciar o banco de dados SQLite.
Cria tabela, insere registros e exporta para CSV.
"""

import sqlite3
import logging
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

DB_NAME = "precos.db"


def criar_tabela():
    """
    Cria a tabela de preços se não existir.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_precos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                preco REAL NOT NULL,
                disponivel BOOLEAN NOT NULL,
                nome_produto TEXT NOT NULL
            )
        ''')
        conn.commit()
        logger.info("Tabela 'historico_precos' pronta para uso.")


def salvar_preco(preco, disponivel, nome_produto):
    """
    Salva um novo registro de preço no banco de dados.
    
    Args:
        preco (float): Preço do produto
        disponivel (bool): Disponibilidade do produto
        nome_produto (str): Nome do produto
    """
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO historico_precos (data_hora, preco, disponivel, nome_produto)
            VALUES (?, ?, ?, ?)
        ''', (data_hora, preco, disponivel, nome_produto))
        conn.commit()
        
    logger.info(f"Preço salvo no banco: R$ {preco:.2f} - {data_hora}")


def exportar_para_csv(arquivo_csv="historico_precos.csv"):
    """
    Exporta todo o histórico para um arquivo CSV.
    
    Args:
        arquivo_csv (str): Nome do arquivo CSV de saída
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            df = pd.read_sql_query("SELECT * FROM historico_precos ORDER BY data_hora", conn)
            
        df.to_csv(arquivo_csv, index=False, encoding="utf-8")
        logger.info(f"Histórico exportado para {arquivo_csv}")
    
    except Exception as e:
        logger.error(f"Erro ao exportar para CSV: {e}")


def obter_historico():
    """
    Retorna todos os registros do histórico como lista de dicionários.
    Útil para gerar gráficos.
    
    Returns:
        list: Lista de dicionários com os dados
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data_hora, preco, nome_produto FROM historico_precos ORDER BY data_hora")
        rows = cursor.fetchall()
        
    return [
        {"data_hora": row[0], "preco": row[1], "nome_produto": row[2]} 
        for row in rows
    ]

# Inicializa a tabela ao importar o módulo
criar_tabela()
# grafico.py
"""
Módulo opcional para gerar gráfico de evolução de preços.
"""

import matplotlib.pyplot as plt
import pandas as pd
from database import obter_historico
import logging

logger = logging.getLogger(__name__)


def gerar_grafico(arquivo_saida="grafico_preco.png"):
    """
    Gera um gráfico de linha com a evolução dos preços.
    
    Args:
        arquivo_saida (str): Nome do arquivo de imagem de saída
    """
    historico = obter_historico()
    
    if len(historico) < 2:
        logger.warning("Histórico insuficiente para gerar gráfico.")
        return False
    
    df = pd.DataFrame(historico)
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    
    plt.figure(figsize=(12, 6))
    plt.plot(df["data_hora"], df["preco"], marker="o", linestyle="-", color="b")
    plt.title(f"Evolução do Preço - {df['nome_produto'].iloc[0]}")
    plt.xlabel("Data e Hora")
    plt.ylabel("Preço (R$)")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    try:
        plt.savefig(arquivo_saida, dpi=300)
        logger.info(f"Gráfico salvo como {arquivo_saida}")
        plt.close()
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar gráfico: {e}")
        return False

# Se quiser gerar o gráfico ao importar
# gerar_grafico()
# alertas.py
"""
Módulo para verificar condições de alerta com base no histórico de preços.
"""

import logging
import pandas as pd
from database import obter_historico
from config import PRECO_ALVO, PERCENTUAL_QUEDA_ALERTA

logger = logging.getLogger(__name__)


def verificar_alertas(preco_atual, nome_produto):
    """
    Verifica se deve disparar algum alerta:
    - Preço abaixo do alvo
    - Queda superior a X% em relação à média recente
    
    Args:
        preco_atual (float): Preço atual do produto
        nome_produto (str): Nome do produto
    """
    historico = obter_historico()
    
    if not historico:
        logger.info("Histórico vazio. Não é possível verificar alertas.")
        return
    
    # Converter para DataFrame para facilitar análise
    df = pd.DataFrame(historico)
    
    # Alerta por preço alvo
    if preco_atual <= PRECO_ALVO:
        logger.warning(f"🚨 ALERTA: {nome_produto} está por R$ {preco_atual:.2f} (alvo: R$ {PRECO_ALVO:.2f})!")
    
    # Alerta por queda percentual
    if len(df) >= 2:
        preco_anterior = df.iloc[-2]["preco"]  # Último antes do atual
        if preco_anterior > 0:
            queda_percentual = ((preco_anterior - preco_atual) / preco_anterior) * 100
            
            if queda_percentual >= PERCENTUAL_QUEDA_ALERTA:
                logger.warning(f"📉 ALERTA: {nome_produto} caiu {queda_percentual:.1f}%! De R$ {preco_anterior:.2f} para R$ {preco_atual:.2f}")
    else:
        logger.info("Histórico insuficiente para análise de queda percentual.")

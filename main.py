# main.py
"""
Script principal para monitoramento de preços.
Utiliza argparse para controlar o modo de execução: agora, agendado ou com intervalo customizado.
"""

import argparse
import logging
import time

import schedule

from scraper import extrair_dados_produto
from database import salvar_preco
from alertas import verificar_alertas
from config import INTERVALO_PADRAO

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log_monitoramento.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def executar_monitoramento():
    """
    Função principal que executa uma rodada de monitoramento:
    - Faz scraping do produto
    - Salva no banco de dados
    - Verifica alertas
    """
    logger.info("Iniciando monitoramento...")
    
    try:
        dados = extrair_dados_produto()
        
        if dados:
            logger.info(f"Preço atual: R$ {dados['preco']:.2f} - Disponível: {dados['disponivel']}")
            salvar_preco(dados['preco'], dados['disponivel'], dados['nome'])
            verificar_alertas(dados['preco'], dados['nome'])
        else:
            logger.error("Falha ao extrair dados do produto.")
    
    except Exception as e:
        logger.error(f"Erro durante o monitoramento: {e}")


def main():
    """
    Função principal que processa os argumentos da linha de comando
    e inicia o modo de execução apropriado.
    """
    parser = argparse.ArgumentParser(description="Monitoramento de preços de produtos")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument('--now', action='store_true', help='Executa o monitoramento uma vez agora')
    grupo.add_argument('--schedule', action='store_true', help='Executa o monitoramento em intervalos agendados')
    grupo.add_argument('--interval', type=int, help='Intervalo personalizado em horas para agendamento')
    
    args = parser.parse_args()
    
    if args.now:
        executar_monitoramento()
    elif args.schedule:
        # Agendamento a cada 6 horas
        schedule.every(6).hours.do(executar_monitoramento)
        logger.info("Agendado para rodar a cada 6 horas.")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Espera 1 minuto entre verificações
    elif args.interval:
        horas = args.interval
        schedule.every(horas).hours.do(executar_monitoramento)
        logger.info(f"Agendado para rodar a cada {horas} horas.")
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    main()

# scraper.py
"""
Módulo para realizar web scraping de uma página de produto.
Extrai nome, preço e disponibilidade.
"""

import requests
from bs4 import BeautifulSoup
import logging
from config import URL_PRODUTO

logger = logging.getLogger(__name__)

# Cabeçalhos para simular um navegador real
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def extrair_dados_produto():
    """
    Realiza o scraping da página do produto e retorna um dicionário com:
    - preco (float)
    - disponivel (bool)
    - nome (str)
    
    Retorna None em caso de erro.
    """
    logger.info(f"Acessando URL: {URL_PRODUTO}")
    
    try:
        response = requests.get(URL_PRODUTO, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Levanta erro para status 4xx/5xx
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Exemplo de extração - adaptar conforme a estrutura real da página
        # AQUI VOCÊ DEVE ADAPTAR OS SELECTORES PARA O SITE ALVO
        nome_elem = soup.find("h1", class_="product-name")
        preco_elem = soup.find("span", class_="price")
        
        if not nome_elem or not preco_elem:
            logger.warning("Não foi possível encontrar elementos esperados na página.")
        # AQUI VOCÊ DEVE ADAPTAR OS SELECTORES PARA O SITE ALVO
        # Exemplos comuns por site:
        # 
        # Amazon:
        # nome_elem = soup.find("span", {"id": "productTitle"})
        # preco_elem = soup.find("span", {"class": "a-price-whole"})
        # 
        # Magazine Luiza:
        # nome_elem = soup.find("h1", {"data-testid": "product-title"})
        # preco_elem = soup.find("p", {"data-testid": "price-value"})
        # 
        # Mercado Livre:
        # nome_elem = soup.find("h1", class_="ui-pdp-title")
        # preco_elem = soup.find("span", class_="andes-money-amount__fraction")
        #
        # Exemplo genérico (ajuste conforme necessário):
        nome_elem = soup.find("h1")  # Ajuste o seletor
        preco_elem = soup.find("span", class_="price")  # Ajuste o seletor
        
        nome = nome_elem.get_text(strip=True)
        
        # Remover caracteres não numéricos do preço e converter
        preco_str = preco_elem.get_text(strip=True)
        preco = float(preco_str.replace("R$", "").replace(".", "").replace(",", "."))
        
        # Assumindo que se o preço existe, o produto está disponível
        disponivel = True
        
        logger.info(f"Dados extraídos: {nome} - R$ {preco:.2f} - Disponível: {disponivel}")
        
        return {
            "nome": nome,
            "preco": preco,
            "disponivel": disponivel
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de conexão ao acessar a página: {e}")
    except Exception as e:
        logger.error(f"Erro ao processar a página: {e}")
    
    return None

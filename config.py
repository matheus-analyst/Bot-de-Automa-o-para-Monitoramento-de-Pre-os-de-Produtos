# config.py
"""
Arquivo de configuração centralizado para o bot de monitoramento.
"""

# URL do produto a ser monitorado
# ATENÇÃO: Substitua pela URL real do produto que deseja monitorar
URL_PRODUTO = "https://exemplo.com/produto"  # ← MUDAR PARA URL REAL

# Preço alvo para alerta
PRECO_ALVO = 1000.00  # Alerta quando o preço cair abaixo deste valor

# Percentual de queda para alerta (ex: 10 = 10%)
PERCENTUAL_QUEDA_ALERTA = 10.0  # Alerta quando o preço cair mais de X%

# Intervalo padrão em horas para agendamento
INTERVALO_PADRAO = 6

# Exemplo de como usar diferentes sites:
# Para Mercado Livre, Amazon, etc., você precisará adaptar os seletores no scraper.py

# DICA: Sempre teste com --now antes de agendar

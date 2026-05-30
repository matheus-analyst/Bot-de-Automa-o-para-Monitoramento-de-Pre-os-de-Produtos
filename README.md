# Bot de Monitoramento de Preços

Um bot simples em Python para monitorar preços de produtos em sites e alertar quando há quedas significativas.

## Funcionalidades

- 🕷️ Web scraping com `requests` e `BeautifulSoup`
- 💾 Armazenamento de histórico em banco SQLite
- 🔔 Alertas no terminal por preço alvo e queda percentual
- 🕐 Agendamento com `schedule`
- 📊 Exportação para CSV e gráfico de evolução
- 📝 Logging detalhado

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual (recomendado)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate   # Windows
   ```
3. Instale as dependências
   ```bash
   pip install -r requirements.txt
   ```

## Como Rodar

Antes de rodar, configure a URL do produto em `config.py`.

### Executar agora
```bash
python main.py --now
```

### Agendar para rodar a cada 6 horas
```bash
python main.py --schedule
```

### Agendar com intervalo personalizado (ex: 3 horas)
```bash
python main.py --interval 3
```

## Configuração

Edite o arquivo `config.py`:

```python
# URL do produto (MUDAR PARA URL REAL)
URL_PRODUTO = "https://exemplo.com/produto"

# Preço alvo para alerta
PRECO_ALVO = 1000.00

# Percentual de queda para alerta
PERCENTUAL_QUEDA_ALERTA = 10.0  # 10%
```

> ⚠️ **Importante**: Os seletores no `scraper.py` precisam ser adaptados para o site específico que você quer monitorar.

## Exemplo de Saída

```
2024-01-15 10:30:22 - INFO - Iniciando monitoramento...
2024-01-15 10:30:23 - INFO - Acessando URL: https://exemplo.com/produto
2024-01-15 10:30:25 - INFO - Dados extraídos: Notebook X - R$ 2499.99 - Disponível: True
2024-01-15 10:30:25 - INFO - Preço salvo no banco: R$ 2499.99 - 2024-01-15 10:30:25
2024-01-15 10:30:25 - WARNING - 📉 ALERTA: Notebook X caiu 12.5%! De R$ 2850.00 para R$ 2499.99
```

## Gráfico de Exemplo

![Exemplo de Gráfico](grafico_preco.png)

## Histórico Exportado

O histórico é exportado para `historico_precos.csv` com todas as colunas do banco.

## O que Aprendi

- **Web Scraping**: Como extrair dados de páginas HTML com BeautifulSoup, lidando com erros de conexão e timeout.
- **SQLite com Python**: Uso do módulo `sqlite3` para criar tabelas, inserir dados e consultar registros sem precisar de um servidor.
- **Padronização de Código**: Dividir a aplicação em módulos com responsabilidades únicas (separação de preocupações).
- **Logging**: Registrar eventos importantes em arquivo e console para depuração e monitoramento.
- **Agendamento**: Usar `schedule` para automatizar tarefas recorrentes.
- **Configuração Centralizada**: Manter todas as configurações em um único arquivo para fácil manutenção.
- **Tratamento de Erros**: Prever falhas na rede, parsing e banco de dados para tornar o bot mais robusto.

## Observações

- Este bot é para fins educacionais. Alguns sites podem bloquear requisições automatizadas.
- Sempre respeite o `robots.txt` e os termos de uso dos sites.
- Para uso em produção, considere usar APIs oficiais quando disponíveis.

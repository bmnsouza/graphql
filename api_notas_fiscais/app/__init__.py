"""
Pacote principal da API GraphQL Nota Fiscal.

Estrutura do projeto:
- config.py  → Leitura de variáveis de ambiente (.env)
- db.py      → Gerenciamento do pool de conexões Oracle
- main.py    → Ponto de entrada da aplicação FastAPI
- schema/    → Definições GraphQL (tipos e queries)

Este arquivo marca o diretório 'app' como um pacote Python,
permitindo imports como:

    from app.db import fetch_all
    from app.schema import Query
"""

__version__ = "1.0.0"
__author__ = "Nota Fiscal - Equipe de Dados"

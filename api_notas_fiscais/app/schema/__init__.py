"""
Módulo de schema GraphQL da API Nota Fiscal.

Contém:
- Definições dos tipos GraphQL (types.py)
- Definições das queries e resolvers (query.py)

Esse arquivo permite que o diretório `schema` seja tratado como
um pacote Python, facilitando os imports no restante da aplicação.
"""

from app.schema.types import *
from app.schema.query import *

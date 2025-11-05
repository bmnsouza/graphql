import strawberry
from typing import List, Optional
from datetime import datetime


# ============================================
# MODELOS DE TABELAS BASEADOS NO BANCO ORACLE
# ============================================

@strawberry.type
class Endereco:
    id_endereco: Optional[int]
    logradouro: Optional[str]
    municipio: Optional[str]
    uf: Optional[str]


@strawberry.type
class Danfe:
    id_danfe: Optional[int]
    numero: Optional[str]
    valor_total: Optional[float]
    data_emissao: Optional[datetime]
    cd_contribuinte: Optional[str] = None


@strawberry.type
class Contribuinte:
    cd_contribuinte: str
    nm_fantasia: Optional[str]
    cnpj_contribuinte: str
    enderecos: Optional[List[Endereco]] = None
    danfes: Optional[List[Danfe]] = None


# ============================================
# INPUTS PARA FILTROS / PAGINAÇÃO
# ============================================

@strawberry.input
class FiltroDanfeInput:
    numero: Optional[str] = None
    valor_minimo: Optional[float] = None
    valor_maximo: Optional[float] = None
    data_inicial: Optional[datetime] = None
    data_final: Optional[datetime] = None
    cd_contribuinte: Optional[str] = None


@strawberry.type
class PaginacaoDanfe:
    total_registros: int
    proximo_cursor: Optional[int]
    danfes: List[Danfe]


# ============================================
# CONVERSORES DE NOMES (AUXILIAR)
# ============================================

def map_row_to_danfe(row: dict) -> Danfe:
    """Converte dicionário do Oracle para objeto Danfe."""
    return Danfe(
        id_danfe=row.get("id_danfe"),
        numero=row.get("numero"),
        valor_total=row.get("valor_total"),
        data_emissao=row.get("data_emissao"),
        cd_contribuinte=row.get("cd_contribuinte")
    )


def map_row_to_endereco(row: dict) -> Endereco:
    """Converte dicionário do Oracle para objeto Endereco."""
    return Endereco(
        id_endereco=row.get("id_endereco"),
        logradouro=row.get("logradouro"),
        municipio=row.get("municipio"),
        uf=row.get("uf")
    )


def map_row_to_contribuinte(row: dict) -> Contribuinte:
    """Converte dicionário do Oracle para objeto Contribuinte."""
    return Contribuinte(
        cd_contribuinte=row.get("cd_contribuinte"),
        nm_fantasia=row.get("nm_fantasia"),
        cnpj_contribuinte=row.get("cnpj_contribuinte")
    )

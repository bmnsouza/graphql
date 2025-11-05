import strawberry
from typing import List, Optional
from app.db import fetch_all, fetch_one
from app.schema.types import Contribuinte, Danfe, Endereco, FiltroDanfeInput, PaginacaoDanfe


@strawberry.type
class Query:
    # ===========================
    # LISTA DE CONTRIBUINTES
    # ===========================
    @strawberry.field
    async def get_contribuintes(self, limit: int = 10) -> List[Contribuinte]:
        sql = """
            SELECT cd_contribuinte, nm_fantasia, cnpj_contribuinte
            FROM NOTA_FISCAL.CONTRIBUINTE
            WHERE ROWNUM <= :limit
        """
        contribs = fetch_all(sql, {"limit": limit})
        contribuintes_result = []

        for c in contribs:
            enderecos_db = fetch_all(
                "SELECT id_endereco, logradouro, municipio, uf FROM NOTA_FISCAL.ENDERECO WHERE cd_contribuinte = :cd",
                {"cd": c["cd_contribuinte"]}
            )
            danfes_db = fetch_all(
                "SELECT id_danfe, numero, valor_total, data_emissao FROM NOTA_FISCAL.DANFE WHERE cd_contribuinte = :cd",
                {"cd": c["cd_contribuinte"]}
            )

            c["enderecos"] = [Endereco(**e) for e in enderecos_db]
            c["danfes"] = [Danfe(**d) for d in danfes_db]
            contribuintes_result.append(Contribuinte(**c))

        return contribuintes_result

    # ===========================
    # CONSULTA POR CNPJ
    # ===========================
    @strawberry.field
    async def get_contribuinte_por_cnpj(self, cnpj: str) -> Optional[Contribuinte]:
        sql = """
            SELECT cd_contribuinte, nm_fantasia, cnpj_contribuinte
            FROM NOTA_FISCAL.CONTRIBUINTE
            WHERE cnpj_contribuinte = :cnpj
        """
        result = fetch_all(sql, {"cnpj": cnpj})
        if not result:
            return None

        c = result[0]
        enderecos_db = fetch_all(
            "SELECT id_endereco, logradouro, municipio, uf FROM NOTA_FISCAL.ENDERECO WHERE cd_contribuinte = :cd",
            {"cd": c["cd_contribuinte"]}
        )
        danfes_db = fetch_all(
            "SELECT id_danfe, numero, valor_total, data_emissao FROM NOTA_FISCAL.DANFE WHERE cd_contribuinte = :cd",
            {"cd": c["cd_contribuinte"]}
        )

        c["enderecos"] = [Endereco(**e) for e in enderecos_db]
        c["danfes"] = [Danfe(**d) for d in danfes_db]
        return Contribuinte(**c)

    # ===========================
    # LISTAR DANFES DIRETAMENTE
    # ===========================
    @strawberry.field
    async def get_danfes(self, limit: int = 50) -> List[Danfe]:
        sql = """
            SELECT id_danfe, numero, valor_total, data_emissao, cd_contribuinte
            FROM NOTA_FISCAL.DANFE
            WHERE ROWNUM <= :limit
            ORDER BY data_emissao DESC
        """
        danfes = fetch_all(sql, {"limit": limit})
        return [Danfe(**d) for d in danfes]

    # ===========================
    # FILTRO E PAGINAÇÃO DE DANFEs
    # ===========================
    @strawberry.field
    async def get_danfes_filtradas(
        self,
        filtro: Optional[FiltroDanfeInput] = None,
        cursor: Optional[int] = None,
        limite: int = 50
    ) -> PaginacaoDanfe:
        """
        Retorna DANFEs com filtros e paginação cursor-based.
        """
        base_sql = """
            SELECT id_danfe, numero, valor_total, data_emissao, cd_contribuinte
            FROM NOTA_FISCAL.DANFE
            WHERE 1=1
        """
        params = {}

        if filtro:
            if filtro.numero:
                base_sql += " AND numero = :num"
                params["num"] = filtro.numero
            if filtro.valor_minimo is not None:
                base_sql += " AND valor_total >= :vmin"
                params["vmin"] = filtro.valor_minimo
            if filtro.valor_maximo is not None:
                base_sql += " AND valor_total <= :vmax"
                params["vmax"] = filtro.valor_maximo
            if filtro.data_inicial:
                base_sql += " AND data_emissao >= :dini"
                params["dini"] = filtro.data_inicial
            if filtro.data_final:
                base_sql += " AND data_emissao <= :dfim"
                params["dfim"] = filtro.data_final
            if filtro.cd_contribuinte:
                base_sql += " AND cd_contribuinte = :cd"
                params["cd"] = filtro.cd_contribuinte

        if cursor:
            base_sql += " AND id_danfe > :cursor"
            params["cursor"] = cursor

        base_sql += " ORDER BY id_danfe FETCH FIRST :limite ROWS ONLY"
        params["limite"] = limite

        danfes = fetch_all(base_sql, params)
        total = fetch_one("SELECT COUNT(*) AS qtd FROM NOTA_FISCAL.DANFE")
        total_registros = total["qtd"] if total else 0
        proximo_cursor = danfes[-1]["id_danfe"] if danfes else None

        return PaginacaoDanfe(
            total_registros=total_registros,
            proximo_cursor=proximo_cursor,
            danfes=[Danfe(**d) for d in danfes]
        )

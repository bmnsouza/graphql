import strawberry
from typing import Optional
from app.db import get_pool
from app.logger import log_sql
from app.schema.types import Contribuinte, Danfe, Endereco


@strawberry.type
class Mutation:
    # ======================================================
    # Criar Contribuinte
    # ======================================================
    @strawberry.mutation
    async def criar_contribuinte(
        self,
        cd_contribuinte: str,
        nm_fantasia: Optional[str],
        cnpj_contribuinte: str
    ) -> Contribuinte:
        sql = """
            INSERT INTO NOTA_FISCAL.CONTRIBUINTE
                (cd_contribuinte, nm_fantasia, cnpj_contribuinte)
            VALUES (:cd, :nm, :cnpj)
        """

        pool = get_pool()
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, {
                    "cd": cd_contribuinte,
                    "nm": nm_fantasia,
                    "cnpj": cnpj_contribuinte
                })
                conn.commit()

        log_sql(sql, {"cd": cd_contribuinte, "nm": nm_fantasia, "cnpj": cnpj_contribuinte}, 0)
        return Contribuinte(cd_contribuinte=cd_contribuinte, nm_fantasia=nm_fantasia, cnpj_contribuinte=cnpj_contribuinte)

    # ======================================================
    # Criar Endereço
    # ======================================================
    @strawberry.mutation
    async def criar_endereco(
        self,
        cd_contribuinte: str,
        logradouro: str,
        municipio: str,
        uf: str
    ) -> Endereco:
        sql = """
            INSERT INTO NOTA_FISCAL.ENDERECO
                (cd_contribuinte, logradouro, municipio, uf)
            VALUES (:cd, :log, :mun, :uf)
            RETURNING id_endereco INTO :id
        """

        pool = get_pool()
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                id_out = cursor.var(int)
                cursor.execute(sql, {
                    "cd": cd_contribuinte,
                    "log": logradouro,
                    "mun": municipio,
                    "uf": uf,
                    "id": id_out
                })
                conn.commit()
                id_endereco = id_out.getvalue()[0] if id_out.getvalue() else None

        log_sql(sql, {"cd": cd_contribuinte, "log": logradouro, "mun": municipio, "uf": uf}, 0)
        return Endereco(id_endereco=id_endereco, logradouro=logradouro, municipio=municipio, uf=uf)

    # ======================================================
    # Criar DANFE
    # ======================================================
    @strawberry.mutation
    async def criar_danfe(
        self,
        cd_contribuinte: str,
        numero: str,
        valor_total: float
    ) -> Danfe:
        sql = """
            INSERT INTO NOTA_FISCAL.DANFE
                (cd_contribuinte, numero, valor_total, data_emissao)
            VALUES (:cd, :num, :valor, SYSDATE)
            RETURNING id_danfe, data_emissao INTO :id, :data
        """

        pool = get_pool()
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                id_out = cursor.var(int)
                data_out = cursor.var(str)
                cursor.execute(sql, {
                    "cd": cd_contribuinte,
                    "num": numero,
                    "valor": valor_total,
                    "id": id_out,
                    "data": data_out
                })
                conn.commit()
                id_danfe = id_out.getvalue()[0] if id_out.getvalue() else None
                data_emissao = data_out.getvalue()[0] if data_out.getvalue() else None

        log_sql(sql, {"cd": cd_contribuinte, "num": numero, "valor": valor_total}, 0)
        return Danfe(
            id_danfe=id_danfe,
            numero=numero,
            valor_total=valor_total,
            data_emissao=data_emissao,
            cd_contribuinte=cd_contribuinte
        )

    # ======================================================
    # Atualizar Contribuinte
    # ======================================================
    @strawberry.mutation
    async def atualizar_contribuinte(
        self,
        cd_contribuinte: str,
        nova_fantasia: str
    ) -> str:
        sql = """
            UPDATE NOTA_FISCAL.CONTRIBUINTE
            SET nm_fantasia = :fantasia
            WHERE cd_contribuinte = :cd
        """

        pool = get_pool()
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, {"fantasia": nova_fantasia, "cd": cd_contribuinte})
                rowcount = cursor.rowcount
                conn.commit()

        log_sql(sql, {"cd": cd_contribuinte, "fantasia": nova_fantasia}, 0)
        if rowcount == 0:
            return f"Contribuinte {cd_contribuinte} não encontrado."
        return f"Contribuinte {cd_contribuinte} atualizado com sucesso."

    # ======================================================
    # Atualizar Endereço
    # ======================================================
    @strawberry.mutation
    async def atualizar_endereco(
        self,
        id_endereco: int,
        novo_logradouro: str,
        novo_municipio: str,
        nova_uf: str
    ) -> str:
        sql = """
            UPDATE NOTA_FISCAL.ENDERECO
            SET logradouro = :logradouro, municipio = :municipio, uf = :uf
            WHERE id_endereco = :id
        """

        pool = get_pool()
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, {"logradouro": novo_logradouro, "municipio": novo_municipio, "uf": nova_uf, "id": id_endereco})
                rowcount = cursor.rowcount
                conn.commit()

        log_sql(sql, {"id": id_endereco, "logradouro": novo_logradouro, "municipio": novo_municipio, "uf": nova_uf}, 0)
        if rowcount == 0:
            return f"Endereço {id_endereco} não encontrado."
        return f"Endereço {id_endereco} atualizado com sucesso."

    # ======================================================
    # Atualizar DANFE
    # ======================================================
    @strawberry.mutation
    async def atualizar_danfe(
        self,
        id_danfe: int,
        novo_numero: str,
        novo_valor: float
    ) -> str:
        sql = """
            UPDATE NOTA_FISCAL.DANFE
            SET numero = :numero, valor_total = :valor
            WHERE id_danfe = :id
        """

        pool = get_pool()
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, {"numero": novo_numero, "valor": novo_valor, "id": id_danfe})
                rowcount = cursor.rowcount
                conn.commit()

        log_sql(sql, {"id": id_danfe, "numero": novo_numero, "valor": novo_valor}, 0)
        if rowcount == 0:
            return f"DANFE {id_danfe} não encontrado."
        return f"DANFE {id_danfe} atualizado com sucesso."

    # ======================================================
    # Excluir Contribuinte
    # ======================================================
    @strawberry.mutation
    async def excluir_contribuinte(self, cd_contribuinte: str) -> str:
        sql = "DELETE FROM NOTA_FISCAL.CONTRIBUINTE WHERE cd_contribuinte = :cd"

        pool = get_pool()
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, {"cd": cd_contribuinte})
                rowcount = cursor.rowcount
                conn.commit()

        log_sql(sql, {"cd": cd_contribuinte}, 0)
        if rowcount == 0:
            return f"Contribuinte {cd_contribuinte} não encontrado."
        return f"Contribuinte {cd_contribuinte} excluído com sucesso."

    # ======================================================
    # Excluir Endereço
    # ======================================================
    @strawberry.mutation
    async def excluir_endereco(self, id_endereco: int) -> str:
        sql = "DELETE FROM NOTA_FISCAL.ENDERECO WHERE id_endereco = :id"

        pool = get_pool()
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, {"id": id_endereco})
                rowcount = cursor.rowcount
                conn.commit()

        log_sql(sql, {"id": id_endereco}, 0)
        if rowcount == 0:
            return f"Endereço {id_endereco} não encontrado."
        return f"Endereço {id_endereco} excluído com sucesso."

    # ======================================================
    # Excluir DANFE
    # ======================================================
    @strawberry.mutation
    async def excluir_danfe(self, id_danfe: int) -> str:
        sql = "DELETE FROM NOTA_FISCAL.DANFE WHERE id_danfe = :id"

        pool = get_pool()
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, {"id": id_danfe})
                rowcount = cursor.rowcount
                conn.commit()

        log_sql(sql, {"id": id_danfe}, 0)
        if rowcount == 0:
            return f"DANFE {id_danfe} não encontrado."
        return f"DANFE {id_danfe} excluído com sucesso."

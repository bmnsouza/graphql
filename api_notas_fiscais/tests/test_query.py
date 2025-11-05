import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_contribuintes(monkeypatch):
    """
    Testa a query GraphQL 'getContribuintes' validando o retorno
    dos três primeiros registros simulados.
    """

    # Simula dados retornados do banco
    fake_data = [
        {"cd_contribuinte": "270000011", "nm_fantasia": "MACIEIRA MENEZES", "cnpj_contribuinte": "12345678000199"},
        {"cd_contribuinte": "270000020", "nm_fantasia": None, "cnpj_contribuinte": "98765432000177"},
        {"cd_contribuinte": "270000054", "nm_fantasia": "SUPERMERCADO PRUDENTE", "cnpj_contribuinte": "55443322000111"},
    ]

    # 🔹 Mock da função fetch_all (para não precisar de Oracle real)
    async def fake_fetch_all(sql, params=None):
        return fake_data

    # Substitui função real pela fake
    from app import db
    monkeypatch.setattr(db, "fetch_all", fake_fetch_all)

    # Query GraphQL simulada
    query = """
    {
      getContribuintes(limit: 3) {
        cd_contribuinte
        nm_fantasia
        cnpj_contribuinte
      }
    }
    """

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/graphql", json={"query": query})

    assert response.status_code == 200
    result = response.json()["data"]["getContribuintes"]

    # Valida estrutura e dados
    assert len(result) == 3
    assert result[0]["cd_contribuinte"] == "270000011"
    assert result[2]["nm_fantasia"] == "SUPERMERCADO PRUDENTE"

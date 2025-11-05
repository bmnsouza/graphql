# API GraphQL Nota Fiscal

API de consulta a dados de Notas Fiscais construída com **FastAPI**, **Strawberry GraphQL** e **Oracle Database**.

---

## Requisitos
- Python 3.13.3
- Oracle Client / Instant Client configurado
- Banco de dados Oracle 11g ou superior
- Pacotes Python (ver `requirements.txt`)

---

## Instalação
```bash
git clone api_notas_fiscais
cd api_notas_fiscais
pip install -r requirements.txt
```

---

## Iniciar servidor
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

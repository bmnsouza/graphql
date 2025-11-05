from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
import strawberry
import time
import uuid

from app.schema.query import Query
from app.schema.mutation import Mutation
from app.db import init_pool
from app.logger import app_logger
from app import config


# ==========================================================
# CONFIGURAÇÃO DO SCHEMA GRAPHQL
# ==========================================================
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

# ==========================================================
# CONFIGURAÇÃO PRINCIPAL DO FASTAPI
# ==========================================================
app = FastAPI(
    title="API GraphQL Notas Fiscais",
    description="API com auditoria SQL, logs e alta performance.",
    version="1.0"
)

app.include_router(graphql_app, prefix="/graphql")


# ==========================================================
# EVENTO DE INICIALIZAÇÃO (cria pool de conexões)
# ==========================================================
@app.on_event("startup")
async def startup_event():
    """Executado na inicialização da API."""
    init_pool()
    # Log seguro e formatado do ambiente
    masked_pwd = "*****" if config.ORACLE_PASSWORD else None
    app_logger.info("==========================================")
    app_logger.info("🚀 API GraphQL Notas Fiscais iniciada!")
    app_logger.info(f"📡 Host: {config.API_HOST}")
    app_logger.info(f"🔌 Porta: {config.API_PORT}")
    app_logger.info(f"🗄️  Oracle User: {config.ORACLE_USER}")
    app_logger.info(f"🛠️  Oracle DSN: {config.ORACLE_DSN}")
    app_logger.info(f"🔒 Oracle Password: {masked_pwd}")
    app_logger.info("==========================================")
    app_logger.info("Pool Oracle inicializado e API pronta para uso.")


# ==========================================================
# MIDDLEWARE DE AUDITORIA / LOG DE REQUISIÇÕES
# ==========================================================
@app.middleware("http")
async def log_request_timing(request: Request, call_next):
    """Auditoria e métricas de tempo por requisição HTTP."""
    request_id = str(uuid.uuid4())[:8]
    start = time.perf_counter()
    app_logger.info(f"[{request_id}] Início da requisição: {request.method} {request.url.path}")

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    app_logger.info(
        f"[{request_id}] Finalizada em {duration_ms:.2f} ms - Status {response.status_code}"
    )

    return response


# ==========================================================
# ENDPOINT PRINCIPAL (teste rápido)
# ==========================================================
@app.get("/")
def root():
    return {
        "message": "API GraphQL Notas Fiscais em execução com auditoria SQL e logs de performance."
    }


# ==========================================================
# EXECUÇÃO DIRETA (porta/host do .env)
# ==========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )

import time
import oracledb
from app import config
from app.logger import log_sql

pool = None


def init_pool():
    """Inicializa o pool de conexões Oracle (modo síncrono)."""
    global pool
    if not pool:
        pool = oracledb.create_pool(
            user=config.ORACLE_USER,
            password=config.ORACLE_PASSWORD,
            dsn=config.ORACLE_DSN,
            min=1,
            max=5,
            increment=1
        )


def get_pool():
    """Retorna o pool atual."""
    if not pool:
        raise RuntimeError("O pool de conexões ainda não foi inicializado.")
    return pool


def fetch_all(sql: str, params=None):
    """Executa SELECT e retorna todos os registros com log."""
    conn = pool.acquire()
    params = params or {}
    try:
        start = time.perf_counter()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        columns = [col[0].lower() for col in cursor.description]
        rows = cursor.fetchall()
        duration_ms = (time.perf_counter() - start) * 1000
        log_sql(sql, params, duration_ms)
        return [dict(zip(columns, row)) for row in rows]
    finally:
        pool.release(conn)


def fetch_one(sql: str, params=None):
    """Executa SELECT único com log."""
    conn = pool.acquire()
    params = params or {}
    try:
        start = time.perf_counter()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        duration_ms = (time.perf_counter() - start) * 1000
        log_sql(sql, params, duration_ms)
        if row:
            columns = [col[0].lower() for col in cursor.description]
            return dict(zip(columns, row))
    finally:
        pool.release(conn)

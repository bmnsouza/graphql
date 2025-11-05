import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timezone, timedelta

# Diretório de logs
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# ================================
#  CONFIGURAÇÃO DE FORMATOS
# ================================
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# UTC-3 (Horário de Brasília)
BRASIL_TZ = timezone(timedelta(hours=-3))

def time_converter(*args):
    return datetime.now(BRASIL_TZ).timetuple()

# ================================
#  ARQUIVOS DE LOG
# ================================
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
SQL_LOG_FILE = os.path.join(LOG_DIR, "sql.log")

# ================================
#  LOGGER PRINCIPAL DA APLICAÇÃO
# ================================
app_logger = logging.getLogger("app_logger")
app_logger.setLevel(logging.INFO)

# Rotação diária (mantém 7 dias)
app_handler = TimedRotatingFileHandler(APP_LOG_FILE, when="midnight", interval=1, backupCount=7, encoding="utf-8")
app_handler.suffix = "%Y-%m-%d"
app_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
app_handler.converter = time_converter

# Evita logs duplicados
if not app_logger.hasHandlers():
    app_logger.addHandler(app_handler)

# ================================
#  LOGGER DE SQL / PERFORMANCE
# ================================
sql_logger = logging.getLogger("sql_logger")
sql_logger.setLevel(logging.INFO)

sql_handler = TimedRotatingFileHandler(SQL_LOG_FILE, when="midnight", interval=1, backupCount=7, encoding="utf-8")
sql_handler.suffix = "%Y-%m-%d"
sql_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
sql_handler.converter = time_converter

if not sql_logger.hasHandlers():
    sql_logger.addHandler(sql_handler)

# ================================
#  FUNÇÕES AUXILIARES DE LOG
# ================================
def log_sql(sql: str, params: dict, duration_ms: float):
    """Registra consultas SQL com parâmetros e tempo de execução."""
    msg = f"[SQL] {sql.strip()} | Params: {params} | Tempo: {duration_ms:.2f} ms"
    sql_logger.info(msg)

def log_info(message: str):
    app_logger.info(message)

def log_error(message: str):
    app_logger.error(message)

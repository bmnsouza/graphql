from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# =====================================
# CONFIGURAÇÃO DO ORACLE
# =====================================
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")

# =====================================
# CONFIGURAÇÃO DA API
# =====================================
API_HOST = os.getenv("API_HOST")
API_PORT = int(os.getenv("API_PORT"))

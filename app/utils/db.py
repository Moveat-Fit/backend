import os
from dotenv import load_dotenv
import pyodbc

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def get_db_connection():
    server = os.getenv('SERVER')
    uid = os.getenv('UID')
    pwd = os.getenv('PWD')
    database = os.getenv('DATABASE')

    connection_string = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"UID={uid};"
        f"PWD={pwd};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string)
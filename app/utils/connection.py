import os
from dotenv import load_dotenv

# Carregar o arquivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

# Validar carregamento
print("Host:", os.getenv("MYSQL_HOST"))
print("Username:", os.getenv("MYSQL_USER"))
print("Database:", os.getenv("MYSQL_DB"))

import mysql.connector

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORDp"),
    database=os.getenv("MYSQL_DB"),
)

print("Conexão bem-sucedida!")
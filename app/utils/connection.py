import os
import pymysql
from dotenv import load_dotenv

# Carregar o arquivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

# Validar carregamento
print("Host:", os.getenv("MYSQL_HOST"))
print("Username:", os.getenv("MYSQL_USER"))
print("Database:", os.getenv("MYSQL_DB"))

try:
    # Conexão com o banco usando pymysql
    connection = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Conexão bem-sucedida!")
except pymysql.MySQLError as e:
    print("Erro ao conectar ao banco de dados:", e)

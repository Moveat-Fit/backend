import os
from dotenv import load_dotenv
import mysql.connector

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def get_db_connection():
    host = os.getenv('DB_HOST', '127.0.0.1')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', 'ymw2yWp*')
    database = os.getenv('DB_DATABASE', 'db_moveat')

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    return connection

connection = get_db_connection()
print("Conexão bem-sucedida!")
connection.close()
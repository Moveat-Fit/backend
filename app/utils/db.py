import mysql.connector
from dotenv import load_dotenv
import os

def connect_database():
    load_dotenv()
    try:
        cnxn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
        )
        print("Conexão estabelecida com MySQL.")
        return cnxn
    except mysql.connector.Error as e:
        print("Erro ao conectar ao MySQL", e)
        return None

connection = connect_database()
if connection:
    print("Banco de dados conectado com sucesso!")
else:
    print("Falha na conexão com o banco.")
import mysql.connector
from dotenv import load_dotenv
import os
from contextlib import contextmanager

load_dotenv()

def get_db_config():
    return {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DB"),
    }

def connect_database():
    config = get_db_config()
    try:
        connection = mysql.connector.connect(**config)
        print("Conexão estabelecida com MySQL.")
        return connection
    except mysql.connector.Error as e:
        print("Erro ao conectar ao MySQL", e)
        return None

@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = connect_database()
        yield connection
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Conexão fechada.")

def execute_query(query, params=None):
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                connection.commit()
                return cursor.rowcount
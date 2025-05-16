import pymysql
from dotenv import load_dotenv
import os
from contextlib import contextmanager
from decimal import Decimal

load_dotenv()


def get_db_config():
    return {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DB"),
        "cursorclass": pymysql.cursors.DictCursor
    }


def connect_database():
    config = get_db_config()
    try:
        connection = pymysql.connect(**config)
        print("Conexão estabelecida com MySQL.")
        return connection
    except pymysql.MySQLError as e:
        print("Erro ao conectar ao MySQL", e)
        return None


@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = connect_database()
        yield connection
    finally:
        if connection:
            connection.close()
            print("Conexão fechada.")


def execute_query(query, params=None, return_id=False):
    """
    Executa uma query no banco de dados

    Args:
        query (str): Query SQL a ser executada
        params (tuple, optional): Parâmetros para a query
        return_id (bool, optional): Se True, retorna o ID do último registro inserido

    Returns:
        - Para SELECT: Lista de dicionários com os resultados
        - Para INSERT/UPDATE/DELETE:
            - Se return_id=True: ID do último registro inserido
            - Se return_id=False: Número de linhas afetadas
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # Para consultas SELECT
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()

                # Para outras operações
                connection.commit()

                if return_id:
                    # Retorna o último ID inserido (para INSERT)
                    return cursor.lastrowid
                else:
                    # Retorna o número de linhas afetadas (para UPDATE/DELETE)
                    return cursor.rowcount

            except pymysql.MySQLError as err:
                print(f"Error: {err}")
                print(f"Query: {query}")
                print(f"Params: {params}")
                connection.rollback()
                raise

# python can't serialize a decimal into JSON, so it needs to be converted to float

def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

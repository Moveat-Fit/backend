import pyodbc
from flask_restful import Resource
from app.utils.db import connect_database
import datetime

class TestConnection(Resource):
    def get(self):
        connection = None
        cursor = None
        try:
            connection = connect_database()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")  # Executa uma consulta simples para testar a conexão
            cursor.fetchone()  # Busca o resultado para garantir que a consulta foi executada
            return {'message': 'Conexão com o banco de dados bem-sucedida'}, 200
        except pyodbc.Error as e:
            return {'error': str(e)}, 500
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
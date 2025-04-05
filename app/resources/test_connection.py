from flask_restful import Resource
from flask import jsonify
from app.utils.db import connect_database

class TestConnection(Resource):
    def get(self):
        connection = connect_database()
        if connection:
            connection.close()
            return jsonify({"message": "Conexão bem-sucedida com o banco de dados"})
        else:
            return jsonify({"message": "Falha na conexão com o banco de dados"}), 500
from flask import jsonify
from flask_restful import Resource

class PublicResource(Resource):
    def get(self):
        return jsonify(message="Esta é uma rota pública")
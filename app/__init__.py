from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config
from .resources.user import ProfessionalRegistration, ProfessionalLogin, PatientLogin, PatientRegistration, PatientList, PatientDetails, DeletePatient, UpdatePatient
from .resources.protected import ProtectedResource
from .resources.public import PublicResource
from .resources.test_connection import TestConnection
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    jwt = JWTManager(app)
    api = Api(app)

    # Adicionando recursos à API
    api.add_resource(ProfessionalRegistration, '/register')
    api.add_resource(ProfessionalLogin, '/professional')
    api.add_resource(PatientLogin, '/patient')
    api.add_resource(PatientRegistration, '/register/patient')
    api.add_resource(ProtectedResource, '/protected')
    api.add_resource(PublicResource, '/public')
    api.add_resource(TestConnection, '/test-connection')
    api.add_resource(PatientList, '/patients/<int:professional_id>')
    api.add_resource(PatientDetails, '/patient/<int:id>')
    api.add_resource(DeletePatient, '/deletePatient/<int:id>')
    # api.add_resource(UpdatePatient, '/patient/<int:id>/update')
    api.add_resource(UpdatePatient, '/register/patient/<int:id>') 

    # Tratamento de erros
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(error="Endpoint não encontrado"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify(error="Erro interno do servidor"), 500

    return app
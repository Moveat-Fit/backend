from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
from flask_cors import CORS
import os
from dotenv import load_dotenv


app = Flask(__name__)
api = Api(app)
CORS(app)  # Habilita CORS para todas as rotas

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'd7c4d51f08d4f352273c3f549bdd7fcd4195b5355b1718dfdddcc7dde012b427'  # Troque por uma chave secreta real
jwt = JWTManager(app)


load_dotenv()

def get_db_connection():
    server = os.getenv('SERVER')
    uid = os.getenv('UID')
    pwd = os.getenv('PWD')
    database = os.getenv('DATABASE')

    connection_string = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"UID={uid};"
        f"PWD={pwd};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        cpf = data.get('cpf')
        cellphone = data.get('cellphone')
        crn = data.get('crn', None)  # Opcional, pode ser None
        cref = data.get('cref', None)  # Opcional, pode ser None
        user_type = data.get('user_type')

        # Verificação de campos obrigatórios
        required_fields = [name, email, password, cpf, cellphone, user_type]
        if not all(required_fields):
            return {'message': 'Todos os campos obrigatórios devem ser preenchidos'}, 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:100000', salt_length=8)

        cnxn = get_db_connection()
        cursor = cnxn.cursor()
        try:
            cursor.execute("""
                INSERT INTO tb_Users (Name, Email, Password, CPF, CellPhone, CRN, CREF, UserType) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, email, hashed_password, cpf, cellphone, crn, cref, user_type))
            cnxn.commit()
            return {'message': 'Usuário registrado com sucesso'}, 201
        except pyodbc.IntegrityError as e:
            return {'message': f'Erro de integridade de dados: {str(e)}'}, 409
        except pyodbc.Error as e:
            return {'message': f'Erro ao registrar usuário: {str(e)}'}, 500
        finally:
            cursor.close()
            cnxn.close()

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        login = data.get('login')  # Pode ser email, CPF ou celular
        password = data.get('password')

        if not login or not password:
            return {'message': 'Login e senha são obrigatórios'}, 400

        cnxn = get_db_connection()
        cursor = cnxn.cursor()
        try:
            # Tenta encontrar o usuário por email, CPF ou celular
            cursor.execute("""
                SELECT Password FROM tb_Users 
                WHERE Email = ? OR CPF = ? OR CellPhone = ?
            """, (login, login, login))
            user = cursor.fetchone()
            if user and check_password_hash(user.Password, password):
                access_token = create_access_token(identity=login)
                return {'access_token': access_token}, 200
            else:
                return {'message': 'Credenciais inválidas'}, 401
        except pyodbc.Error as e:
            return {'message': f'Erro ao fazer login: {str(e)}'}, 500
        finally:
            cursor.close()
            cnxn.close()

# Nova rota protegida de exemplo
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user)

# Nova rota pública de exemplo
class PublicResource(Resource):
    def get(self):
        return jsonify(message="Esta é uma rota pública")

# Nova rota de teste para verificar a conexão
class TestConnection(Resource):
    def get(self):
        try:
            cnxn = get_db_connection()
            cursor = cnxn.cursor()
            cursor.execute("SELECT 1")  # Executa uma query simples para testar a conexão
            return jsonify(message="Conexão com o backend estabelecida com sucesso!")
        except pyodbc.Error as e:
            return jsonify(message=f"Falha na conexão com o banco de dados: {str(e)}"), 500
        finally:
            cursor.close()
            cnxn.close()

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResource, '/protected')
api.add_resource(PublicResource, '/public')
api.add_resource(TestConnection, '/test-connection')

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return jsonify(error="Endpoint não encontrado"), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="Erro interno do servidor"), 500

if __name__ == '__main__':
    app.run(debug=True)
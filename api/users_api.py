from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)  # Habilita CORS para todas as rotas

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'd7c4d51f08d4f352273c3f549bdd7fcd4195b5355b1718dfdddcc7dde012b427'  # Troque por uma chave secreta real
jwt = JWTManager(app)

# Conexão ao banco de dados
def get_db_connection():
    return pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=BRASLBRJ0108KD5;"
        "Database=db_MoveEat;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type')  # Nutricionista ou Aluno

        if not all([name, email, password, user_type]):
            return {'message': 'Todos os campos são obrigatórios'}, 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:100000', salt_length=8)

        cnxn = get_db_connection()
        cursor = cnxn.cursor()
        try:
            cursor.execute("INSERT INTO tb_Users (Name, Email, Password, UserType) VALUES (?, ?, ?, ?)",
                           (name, email, hashed_password, user_type))
            cnxn.commit()
            return {'message': 'Usuário registrado com sucesso'}, 201
        except pyodbc.IntegrityError:
            return {'message': 'Email já cadastrado'}, 409
        except pyodbc.Error as e:
            return {'message': f'Erro ao registrar usuário: {str(e)}'}, 500
        finally:
            cursor.close()
            cnxn.close()

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'Email e senha são obrigatórios'}, 400

        cnxn = get_db_connection()
        cursor = cnxn.cursor()
        try:
            cursor.execute("SELECT Password FROM tb_Users WHERE Email = ?", (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user.Password, password):
                access_token = create_access_token(identity=email)
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
        return jsonify(message="Conexão com o backend estabelecida com sucesso!")

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
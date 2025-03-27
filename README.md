# API de Gerenciamento de Usuários
 Esta API fornece endpoints para o registro de profissionais e pacientes, autenticação e acesso a recursos protegidos e públicos utilizando Flask, Flask-RESTful e JWT.

# Configuração e Dependências
Flask: Framework web para construir aplicações web.

Flask-RESTful: Extensão para a criação de APIs RESTful de forma simples.

Flask-JWT-Extended: Gerenciamento de tokens JWT para autenticação.

Flask-CORS: Suporte a Cross-Origin Resource Sharing.

mysql-connector-python: Conexão com banco de dados MySQL.

python-dotenv: Carregamento de variáveis de ambiente de um arquivo .env.

werkzeug.security: Utilitários de segurança para hashing de senhas.

# Conexão com o Banco de Dados
A API utiliza um banco de dados MySQL. O arquivo db.py gerencia a conexão:

```python
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
 ```
# Inicialização da Aplicação
A aplicação é inicializada com as seguintes configurações, incluindo habilitação de CORS, configuração de JWT e criação de endpoints da API:

```python
from flask import Flask, jsonify

from flask_restful import Api

from flask_jwt_extended import JWTManager

from flask_cors import CORS

from .config import Config

from .resources.user import ProfessionalRegistration, ProfessionalLogin, PatientLogin, PatientRegistration

from .resources.protected import ProtectedResource

from .resources.public import PublicResource

from .resources.test_connection import TestConnection

def create_app():
    app = Flask(_name_)
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

    # Tratamento de erros
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(error="Endpoint não encontrado"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify(error="Erro interno do servidor"), 500

    return app
    
    #CMD
    #Command:  CD C:\Users\<seu usuario>\diretorio
    python run.py
   ```
# Recursos da API
1. Registro de Profissional (POST /register)
Registra um novo profissional no sistema.

Parâmetros (JSON):
full_name: Nome completo do profissional.

email: Email do profissional.

password: Senha do profissional.

cpf: CPF do profissional.

phone: Número de telefone.

regional_council_type: Tipo de conselho regional (CRN/CREF).

regional_council: Número do conselho regional.

Respostas:
201: Profissional registrado com sucesso.

400: Campos obrigatórios ausentes ou inválidos.

409: Email, CPF ou telefone já registrado.

500: Erro interno do servidor.

2. Login de Profissional (POST /professional)
Autentica um profissional e retorna um token JWT.

Parâmetros (JSON):
login: Email, CPF ou telefone do profissional.

password: Senha do profissional.

Respostas:
200: Login bem-sucedido, retorna token JWT.

400: Credenciais incompletas.

401: Credenciais inválidas.

500: Erro interno do servidor.

3. Registro de Paciente (POST /register/patient)
Registra um paciente no sistema (apenas para profissionais autenticados).

Parâmetros (JSON):
full_name: Nome completo do paciente.

birth_date: Data de nascimento (YYYY-MM-DD).

gender: Gênero (M, F ou O).

email: Email do paciente.

password: Senha do paciente.

mobile: Número de telefone (11 dígitos).

cpf: CPF do paciente (11 dígitos).

weight: Peso do paciente (kg).

height: Altura do paciente (metros).

note: Nota opcional.

Requer autenticação JWT de um profissional.

Respostas:
201: Paciente registrado com sucesso.

400: Erros de validação nos campos.

409: Email, CPF ou telefone já registrado.

403: Acesso não autorizado (se não for um profissional).

500: Erro interno do servidor.

4. Login de Paciente (POST /patient)
Autentica um paciente e retorna um token JWT.

Parâmetros (JSON):
login: Email, CPF ou telefone do paciente.

password: Senha do paciente.

Respostas:
200: Login bem-sucedido, retorna token JWT.

400: Credenciais incompletas.

401: Credenciais inválidas.

500: Erro interno do servidor.

5. Rota Protegida (GET /protected)
Exemplo de rota protegida que requer autenticação JWT.

Respostas:
200: Retorna a identidade do usuário logado.

401: Acesso não autorizado (token ausente ou inválido).

6. Rota Pública (GET /public)
Exemplo de rota pública acessível sem autenticação.

Respostas:
200: Mensagem de rota pública.

7. Teste de Conexão com o Banco (GET /test-connection)
Testa a conexão com o banco de dados.

Respostas:
200: Conexão estabelecida com sucesso.

500: Falha na conexão com o banco de dados.

## Segurança
Senhas são armazenadas com hash utilizando werkzeug.security.

Autenticação baseada em tokens JWT.

CORS habilitado para todas as rotas.

## Notas Importantes
A chave secreta JWT deve ser alterada para uma chave segura em ambiente de produção.

As credenciais do banco de dados são carregadas de variáveis de ambiente para maior segurança.

Certifique-se de que o MySQL está instalado e configurado corretamente.
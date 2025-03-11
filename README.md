# API de Gerenciamento de Usuários
Esta API fornece endpoints para o registro de usuários, autenticação e acesso a recursos protegidos e públicos utilizando Flask, Flask-RESTful e JWT.

## Configuração e Dependências
Flask: Framework web para construir aplicações web.

Flask-RESTful: Extensão para a criação de APIs RESTful de forma simples.

Flask-JWT-Extended: Gerenciamento de tokens JWT para autenticação.

Flask-CORS: Suporte a Cross-Origin Resource Sharing, permitindo que recursos restritos em uma página web sejam recuperados por outro domínio.

pyodbc: Conexão com banco de dados SQL Server.

python-dotenv: Carregamento de variáveis de ambiente de um arquivo .env.

werkzeug.security: Utilitários de segurança para hashing de senhas.

## Inicialização da Aplicação
A aplicação é inicializada com as seguintes configurações, que incluem habilitação de CORS, configuração de JWT e criação de endpoints da API:


```python
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.resources import UserRegistration, UserLogin, ProtectedResource, PublicResource, TestConnection

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Habilita CORS para todas as rotas
    jwt = JWTManager(app)  # Configuração do JWT
    api = Api(app)

    # Adicionando recursos à API
    api.add_resource(UserRegistration, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(ProtectedResource, '/protected')
    api.add_resource(PublicResource, '/public')
    api.add_resource(TestConnection, '/test-connection')

    return app
 ```
## Recursos da API
### 1. UserRegistration (POST /register)
Registra um novo usuário no sistema.

### Parâmetros (JSON):
name: Nome do usuário.

email: Email do usuário.

password: Senha do usuário.

cpf: CPF do usuário.

cellphone: Número de celular.

crn: Número CRN (profissional).

cref: Número CREF (profissional).

user_type: Tipo de usuário.

## Respostas:
201: Usuário registrado com sucesso.

400: Campos obrigatórios ausentes ou inválidos.

409: Erro de integridade de dados (usuário já registrado).

500: Erro interno do servidor.

### 2. UserLogin (POST /login)
Autentica um usuário e retorna um token JWT.

### Parâmetros (JSON):
login: Email, CPF ou celular do usuário.

password: Senha do usuário.

## Respostas:
200: Login bem-sucedido, retorna token JWT.

400: Credenciais incompletas.

401: Credenciais inválidas.

500: Erro interno do servidor.

### 3. ProtectedResource (GET /protected)
Exemplo de rota protegida que requer autenticação JWT.

## Respostas:
200: Retorna a identidade do usuário logado.

401: Acesso não autorizado (token ausente ou inválido).

### 4. PublicResource (GET /public)
Exemplo de rota pública acessível sem autenticação.

## Respostas:
200: Mensagem de rota pública.
### 5. TestConnection (GET /test-connection)
Testa a conexão com o banco de dados.

## Respostas:
200: Conexão estabelecida com sucesso.

500: Falha na conexão com o banco de dados.

## Tratamento de Erros
404: Endpoint não encontrado.

500: Erro interno do servidor.

## Segurança
Senhas são armazenadas com hash usando werkzeug.security.

Autenticação baseada em tokens JWT.

CORS habilitado para todas as rotas.

## Execução
Para iniciar a aplicação em modo de desenvolvimento:


```python
if __name__ == '__main__':
    app.run(debug=True)
```
# Notas Importantes
A chave secreta JWT deve ser alterada para uma chave segura em ambiente de produção.
As credenciais do banco de dados são carregadas de variáveis de ambiente para maior segurança.
Certifique-se de que o ODBC Driver 18 for SQL Server está instalado e configurado corretamente.

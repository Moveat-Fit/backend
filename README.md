# Módulo de Conexão com o Banco de Dados

Este módulo fornece uma função para estabelecer uma conexão com um banco de dados SQL Server usando o pyodbc.

## Dependências

- os: Para acessar variáveis de ambiente
- dotenv: Para carregar variáveis de ambiente de um arquivo .env
- pyodbc: Para estabelecer a conexão com o SQL Server

## Configuração

1. Instale as dependências necessárias:
pip install python-dotenv pyodbc



2. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
SERVER=seu_servidor UID=seu_usuario PWD=sua_senha DATABASE=seu_banco_de_dados



3. Certifique-se de ter o ODBC Driver 18 for SQL Server instalado no seu sistema.

## Uso

Para se conectar no banco, use a função `get_db_connection()` no seu script:

```python
import os
from dotenv import load_dotenv
import pyodbc

# Carrega as variáveis de ambiente do arquivo .env
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
```


## Consultas
Para fazer queries no banco:
```python
# Estabelecer uma conexão
conn = get_db_connection()

# Use a conexão para executar queries
cursor = conn.cursor()
cursor.execute("SELECT * FROM db_Moveat.dbo.tb_Users")

# Não se esqueça de fechar a conexão quando terminar
conn.close()
```
## Detalhes da Função get_db_connection()
Esta função realiza as seguintes operações:

Carrega as variáveis de ambiente do arquivo .env.
Recupera as credenciais e detalhes do servidor do ambiente.
Constrói a string de conexão para o SQL Server.
Estabelece e retorna uma conexão com o banco de dados.
### Parâmetros
A função não aceita parâmetros diretos. Todas as configurações são obtidas de variáveis de ambiente.
### Retorno
Retorna um objeto de conexão pyodbc que pode ser usado para interagir com o banco de dados.

### Exceções
Pode lançar pyodbc.Error se houver problemas ao estabelecer a conexão.
Segurança
As credenciais do banco de dados são armazenadas em variáveis de ambiente, não no código.
A opção TrustServerCertificate=yes é usada. Em ambientes de produção, considere configurar certificados SSL apropriadamente.
### Notas Adicionais
Este módulo usa o ODBC Driver 18 for SQL Server. Ajuste o driver conforme necessário para sua configuração.
Certifique-se de que o arquivo .env está incluído no .gitignore para evitar o compartilhamento acidental de credenciais.

Para mais informações sobre pyodbc e conexões SQL Server, consulte:
#### Documentação do pyodbc: https://github.com/mkleehammer/pyodbc/wiki
#### Drivers ODBC da Microsoft: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server


# API de Gerenciamento de Usuários

Esta API fornece endpoints para registro de usuários, autenticação e recursos protegidos/públicos utilizando Flask, Flask-RESTful e JWT.

## Configuração e Dependências

- Flask: Framework web
- Flask-RESTful: Extensão para criar APIs RESTful
- Flask-JWT-Extended: Gerenciamento de tokens JWT
- Flask-CORS: Suporte a Cross-Origin Resource Sharing
- pyodbc: Conexão com banco de dados SQL Server
- python-dotenv: Carregamento de variáveis de ambiente
- werkzeug.security: Hashing de senhas

## Inicialização da Aplicação

```python
app = Flask(__name__)
api = Api(app)
CORS(app)  # Habilita CORS para todas as rotas

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'd7c4d51f08d4f352273c3f549bdd7fcd4195b5355b1718dfdddcc7dde012b427'
jwt = JWTManager(app)

load_dotenv() #variáveis
```
## Conexão com o Banco de Dados
A função get_db_connection() estabelece uma conexão com o banco de dados SQL Server usando credenciais armazenadas em variáveis de ambiente.

## Recursos da API
### 1. UserRegistration (POST /register)
Registra um novo usuário no sistema.

## Parâmetros (JSON):

name: Nome do usuário
email: Email do usuário
password: Senha do usuário
cpf: CPF do usuário
cellphone: Número de celular
crn: Número CRN (opcional)
cref: Número CREF (opcional)
user_type: Tipo de usuário
Respostas:

201: Usuário registrado com sucesso
400: Campos obrigatórios ausentes
409: Erro de integridade de dados
500: Erro interno do servidor

### 2. UserLogin (POST /login)
Autentica um usuário e retorna um token JWT.

## Parâmetros (JSON):

login: Email, CPF ou celular do usuário
password: Senha do usuário
Respostas:

200: Login bem-sucedido, retorna token JWT
400: Credenciais incompletas
401: Credenciais inválidas
500: Erro interno do servidor
### 3. ProtectedResource (GET /protected)
Exemplo de rota protegida que requer autenticação JWT.

Respostas:

200: Retorna a identidade do usuário logado
401: Acesso não autorizado (token ausente ou inválido)
### 4. PublicResource (GET /public)
Exemplo de rota pública acessível sem autenticação.

Respostas:

200: Mensagem de rota pública
### 5. TestConnection (GET /test-connection)
Testa a conexão com o banco de dados.

Respostas:

200: Conexão estabelecida com sucesso
500: Falha na conexão com o banco de dados
### Tratamento de Erros
404: Endpoint não encontrado
500: Erro interno do servidor
### Segurança
Senhas são armazenadas com hash usando werkzeug.security
Autenticação baseada em tokens JWT
CORS habilitado para todas as rotas
### Execução
Para iniciar a aplicação em modo de desenvolvimento:

```python
if __name__ == '__main__':
    app.run(debug=True)
```
# Notas Importantes
A chave secreta JWT deve ser alterada para uma chave segura em ambiente de produção.
As credenciais do banco de dados são carregadas de variáveis de ambiente para maior segurança.
Certifique-se de que o ODBC Driver 18 for SQL Server está instalado e configurado corretamente.




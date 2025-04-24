# Moveat-Fit Backend

## Estrutura do Projeto | Descrições

- `app/`: Diretório principal da aplicação
  - `resources/`: Contém os recursos da API
    - `protected.py`: Implementa recursos protegidos por autenticação
    - `public.py`: Implementa recursos públicos
    - `test_connection.py`: Testa a conexão com o banco de dados
    - `user.py`: Gerencia operações relacionadas a usuários (registro, login, etc.)
  - `utils/`: Utilitários da aplicação
    - `connection.py`: Gerencia a conexão com o banco de dados
    - `db.py`: Funções auxiliares para operações no banco de dados
    - `schema.py`: Define o schema do banco de dados
  - `__init__.py`: Inicializa a aplicação Flask
  - `config.py`: Configurações da aplicação
- `run.py`: Ponto de entrada para executar a aplicação

## Funcionalidades

1. Registro e login de profissionais de saúde
2. Registro e login de pacientes
3. Listagem de pacientes por profissional
4. Rotas protegidas e públicas
5. Teste de conexão com o banco de dados

## Configuração

1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
MYSQL_HOST=seu_host MYSQL_USER=seu_usuario MYSQL_PASSWORD=sua_senha MYSQL_DB=seu_banco_de_dados JWT_SECRET_KEY=sua_chave_secreta



2. Instale as dependências:
pip install -r requirements.txt



3. Execute o script para criar as tabelas no banco de dados:
python -c "from app.utils.schema import create_tables, connect_database; create_tables(connect_database())"



## Executando o Projeto

Para iniciar o servidor de desenvolvimento:
python run.py



O servidor estará disponível em `http://127.0.0.1:5000`.

## Endpoints da API

- `POST /register`: Registro de profissionais
- `POST /professional`: Login de profissionais
- `POST /patient`: Login dex pacientes
- `POST /register/patient`: Registro de pacientes (requer autenticação de profissional)
- `POST /deletePatient/<patient_id>`: Deleta pacientes de um profissional específico
- `GET /protected`: Rota protegida (requer autenticação)
- `GET /public`: Rota pública
- `GET /test-connection`: Testa a conexão com o banco de dados
- `GET /patients/<professional_id>`: Lista pacientes de um profissional específico





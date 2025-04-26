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
4. Deleção de pacientes por profissional
5. Alteração dos dados de pacientes por profissional
6. Rotas protegidas e públicas
7. Teste de conexão com o banco de dados

## Configuração

#### 1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
MYSQL_HOST=seu_host 

MYSQL_USER=seu_usuario 

MYSQL_PASSWORD=sua_senha 

MYSQL_DB=seu_banco_de_dados 

JWT_SECRET_KEY=sua_chave_secreta
```


#### 2. Instale as dependências:
```
pip install -r requirements.txt
```




## Executando o Projeto

Para iniciar o servidor de desenvolvimento, execute:
```
python run.py
```

Este código acima realiza duas tarefas principais: inicializa o banco de dados e suas operações e executa a aplicação Flask.

```
from app import create_app
from app.utils.schema import connect_database, create_tables

app = create_app()

# Função para inicializar o banco de dados
def initialize_database():
    connection = connect_database()
    if connection:
        create_tables(connection)

if __name__ == "__main__":
    # Inicializa o banco de dados antes de iniciar o app
    initialize_database()
    app.run(debug=True)
```
Em resumo, o código configura e inicia o ambiente necessário para a aplicação funcionar, garantindo que o banco de dados esteja pronto antes de iniciar o servidor.


O servidor estará disponível em `http://127.0.0.1:5000`.

## Endpoints da API

- `POST /register`: Registro de profissionais
- `POST /professional`: Login de profissionais
- `POST /patient`: Login de pacientes
- `POST /register/patient`: Registro de pacientes (requer autenticação de profissional)
- `POST /deletePatient/<patient_id>`: Deleta pacientes de um profissional específico
- `GET /protected`: Rota protegida (requer autenticação)
- `GET /public`: Rota pública
- `GET /test-connection`: Testa a conexão com o banco de dados
- `GET /patients/<professional_id>`: Lista pacientes de um profissional específico


### POST /register
Body da Requisição:


```
{
  "full_name": "Nome Completo",
  "email": "email@example.com",
  "password": "Senha123!",
  "cpf": "12345678901",
  "phone": "11987654321",
  "regional_council_type": "CRN",
  "regional_council": "12345"
}
```
#### Resposta Esperada:

Sucesso (201):
```
{
  "message": "Profissional registrado com sucesso",
  "access_token": "<jwt_token>"
}
```
Erro (400/409): Mensagens de erro específicas para validação ou conflitos de dados.

### POST /professional
Body da Requisição:


```
{
  "login": "email@example.com",
  "password": "Senha123!"
}
```
#### Resposta Esperada:

Sucesso (200):

```
{
  "access_token": "<jwt_token>"
}
```

Erro (401/400): Credenciais inválidas ou campos obrigatórios ausentes.
### POST /patient
Body da Requisição:


```
{
  "login": "email@example.com",
  "password": "Senha123!"
}
```
#### Resposta Esperada:

Sucesso (200):

```
{
  "access_token": "<jwt_token>"
}
```
Erro (401/400): Credenciais inválidas ou campos obrigatórios ausentes.
### POST /register/patient
Body da Requisição:


```
{
  "full_name": "Nome Completo",
  "birth_date": "1990-01-01",
  "gender": "M",
  "email": "email@example.com",
  "password": "Senha123!",
  "mobile": "11987654321",
  "cpf": "12345678901",
  "weight": 70.5,
  "height": 1.75,
  "note": "Nota sobre o paciente"
}
```
#### Resposta Esperada:

Sucesso (201):

```
{
  "message": "Paciente registrado com sucesso"
}
```
Erro (400/409): Mensagens de erro específicas para validação ou conflitos de dados.
### DELETE /deletePatient/<patient_id>
#### Resposta Esperada:

Sucesso (200):

```
{
  "message": "Paciente deletado com sucesso"
}
```
Erro (404): Paciente não encontrado ou não pertence ao profissional.
### PUT /patient/<id>/update
Body da Requisição:


```
{
  "full_name": "Novo Nome Completo",
  "birth_date": "1990-01-01",
  "gender": "M",
  "email": "novoemail@example.com",
  "mobile": "11987654321",
  "cpf": "12345678901",
  "weight": 70.5,
  "height": 1.75,
  "note": "Nota atualizada"
}
```
#### Resposta Esperada:

Sucesso (200):

```
{
  "message": "Dados do paciente atualizados com sucesso"
}
```
Erro (400/404): Mensagens de erro específicas para validação ou paciente não encontrado.
### GET /patients/<professional_id>
#### Resposta Esperada:

Sucesso (200):

```
{
  "patients": [
    {
      "id": 1,
      "full_name": "Nome Completo",
      "birth_date": "1990-01-01",
      "gender": "M",
      "email": "email@example.com",
      "mobile": "11987654321",
      "cpf": "12345678901",
      "weight": "70.5",
      "height": "1.75",
      "note": "Nota sobre o paciente",
      "professional_id": 1,
      "created_at": "2023-01-01 12:00:00",
      "updated_at": "2023-01-01 12:00:00"
    }
  ]
}
```
Erro (404): Nenhum paciente encontrado para este profissional.
### GET /protected
#### Resposta Esperada:

Sucesso (200): Conteúdo protegido acessível.
Erro (401): Autenticação necessária.
### GET /public
#### Resposta Esperada:

Sucesso (200): Conteúdo público acessível.
### GET /test-connection
#### Resposta Esperada:

Sucesso (200): Conexão com o banco de dados bem-sucedida.
Erro (500): Erro ao conectar ao banco de dados.



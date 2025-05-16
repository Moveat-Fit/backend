# Moveat-Fit Backend

## Estrutura do Projeto

**Diretório ******\`\`******:** Diretório principal da aplicação

* `resources/`: Contém os recursos da API

  * `protected.py`: Implementa recursos protegidos por autenticação
  * `public.py`: Implementa recursos públicos
  * `test_connection.py`: Testa a conexão com o banco de dados
  * `user.py`: Gerencia operações relacionadas a usuários (registro, login, etc.)

* `utils/`: Utilitários da aplicação

  * `connection.py`: Gerencia a conexão com o banco de dados
  * `db.py`: Funções auxiliares para operações no banco de dados
  * `schema.py`: Define o schema do banco de dados

* `__init__.py`: Inicializa a aplicação Flask

* `config.py`: Configurações da aplicação

* `run.py`: Ponto de entrada para executar a aplicação

## Funcionalidades

* Registro e login de profissionais de saúde
* Registro e login de pacientes
* Listagem, deleção e alteração de pacientes por profissional
* Rotas protegidas e públicas
* Teste de conexão com o banco de dados
* Gerenciamento de Planos Alimentares:

  * Criação, consulta, atualização, exclusão
  * Listagem por paciente

## Configuração

1. Crie um arquivo `.env` na raiz do projeto com as variáveis:

```env
MYSQL_HOST=seu_host
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
MYSQL_DB=seu_banco_de_dados
JWT_SECRET_KEY=sua_chave_secreta
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando o Projeto

Para iniciar o servidor de desenvolvimento, execute:

```bash
python run.py
```

Esse código inicializa o banco de dados e a aplicação Flask:

```python
from app import create_app
from app.utils.schema import connect_database, create_tables

app = create_app()

def initialize_database():
    connection = connect_database()
    if connection:
        create_tables(connection)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
```

Servidor disponível em: `http://127.0.0.1:5000`

---

## Endpoints da API

### Autenticação e Usuários

* **POST** `/register`: Registro de profissionais
* **POST** `/professional`: Login de profissionais
* **POST** `/patient`: Login de pacientes
* **POST** `/register/patient`: Registro de pacientes (requer autenticação)

### Gerenciamento de Pacientes

* **PUT** `/patient/<patient_id>/update`: Atualiza dados do paciente
* **DELETE** `/deletePatient/<patient_id>`: Deleta paciente
* **GET** `/patients/<professional_id>`: Lista pacientes de um profissional
* **GET** `/patient/<patient_id>`: Detalhes de um paciente

### Planos Alimentares

* **POST** `/meal-plans`: Cria plano alimentar
* **GET** `/meal-plans/<meal_plan_id>`: Detalhes de um plano
* **PUT** `/meal-plans/<meal_plan_id>`: Atualiza plano alimentar
* **DELETE** `/meal-plans/<meal_plan_id>`: Remove plano alimentar
* **GET** `/patients/<patient_id>/meal-plans`: Lista planos do paciente

### Utilitários

* **GET** `/protected`: Rota protegida (requer autenticação)
* **GET** `/public`: Rota pública
* **GET** `/test-connection`: Testa conexão com banco de dados

---

## Exemplos de Requisições e Respostas

### POST /register

```json
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

**Resposta 201:**

```json
{
  "message": "Profissional registrado com sucesso",
  "access_token": "<jwt_token>"
}
```

### POST /professional

```json
{
  "login": "email@example.com",
  "password": "Senha123!"
}
```

**Resposta 200:**

```json
{
  "access_token": "<jwt_token>"
}
```

### POST /patient

```json
{
  "login": "email@example.com",
  "password": "Senha123!"
}
```

**Resposta 200:**

```json
{
  "access_token": "<jwt_token>"
}
```

### POST /register/patient

```json
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

**Resposta 201:**

```json
{
  "message": "Paciente registrado com sucesso"
}
```

### DELETE /deletePatient/\<patient\_id>

**Resposta 200:**

```json
{
  "message": "Paciente deletado com sucesso"
}
```

### PUT /patient/\<patient\_id>/update

```json
{
  "full_name": "Novo Nome",
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

**Resposta 200:**

```json
{
  "message": "Dados do paciente atualizados com sucesso"
}
```

### GET /patients/\<professional\_id>

**Resposta 200:**

```json
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

### GET /patient/\<patient\_id>

**Resposta 200:**

```json
{
  "patient": {
    "id": 1,
    "full_name": "Nome Completo",
    "birth_date": "1990-01-01",
    "gender": "M",
    "email": "email@example.com",
    "phone": "11987654321",
    "cpf": "12345678901",
    "weight": "70.5",
    "height": "1.75",
    "note": "Nota sobre o paciente",
    "professional_id": 1,
    "created_at": "2023-01-01 12:00:00",
    "updated_at": "2023-01-01 12:00:00"
  }
}
```

### POST /meal-plans

```json
{
  "patient_id": 1,
  "plan_name": "Plano Nutricional",
  "start_date": "2023-01-01",
  "end_date": "2023-02-01",
  "goals": "Perda de peso",
  "entries": [
    {
      "meal_type_id": 1,
      "day_of_plan": "2023-01-01",
      "time_scheduled": "08:00",
      "notes": "Café da manhã",
      "foods": [
        {
          "food_id": 1,
          "prescribed_quantity_grams": 100,
          "display_portion": "1 xícara",
          "preparation_notes": "Sem açúcar"
        }
      ]
    }
  ]
}
```

**Resposta 201:**

```json
{
  "message": "Plano alimentar criado com sucesso",
  "meal_plan_id": 1
}
```

### GET /meal-plans/\<meal\_plan\_id>

**Resposta 200:**

```json
{
  "meal_plan": {
    "id": 1,
    "patient_id": 1,
    "professional_id": 1,
    "plan_name": "Plano Nutricional",
    "start_date": "2023-01-01",
    "end_date": "2023-02-01",
    "goals": "Perda de peso",
    "created_at": "2023-01-01 12:00:00",
    "updated_at": "2023-01-01 12:00:00",
    "entries": [
      {
        "id": 1,
        "meal_type_id": 1,
        "meal_type_name": "Café da Manhã",
        "day_of_plan": "2023-01-01",
        "time_scheduled": "08:00",
        "notes": "Café da manhã",
        "foods": [
          {
            "id": 1,
            "food_id": 1,
            "food_name": "Ovos",
            "prescribed_quantity_grams": 100,
            "display_portion": "1 xícara",
            "preparation_notes": "Sem açúcar"
          }
        ]
      }
    ]
  }
}
```

### PUT /meal-plans/\<meal\_plan\_id>

```json
{
  "plan_name": "Plano Atualizado",
  "start_date": "2023-01-02",
  "end_date": "2023-02-02",
  "goals": "Novas metas"
}
```

**Resposta 200:**

```json
{
  "message": "Plano alimentar atualizado com sucesso"
}
```

### DELETE /meal-plans/\<meal\_plan\_id>

**Resposta 200:**

```json
{
  "message": "Plano alimentar deletado com sucesso"
}
```

### GET /patients/\<patient\_id>/meal-plans

**Resposta 200:**

```json
{
  "meal_plans": [
    {
      "id": 1,
      "plan_name": "Plano Nutricional",
      "start_date": "2023-01-01",
      "end_date": "2023-02-01",
      "goals": "Perda de peso",
      "created_at": "2023-01-01 12:00:00",
      "updated_at": "2023-01-01 12:00:00"
    }
  ]
}
```

### GET /protected

**Resposta 200:** Conteúdo protegido acessível.

### GET /public

**Resposta 200:** Conteúdo público acessível.

### GET /test-connection

**Resposta 200:** Conexão com o banco de dados bem-sucedida.

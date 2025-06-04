# Documentação Moveat Backend

- [Documentação Moveat Backend](#documentação-moveat-backend)
  - [Visão Geral](#visão-geral)
  - [Tecnologias Utilizadas](#tecnologias-utilizadas)
  - [Instalação](#instalação)
  - [Executando a Aplicação](#executando-a-aplicação)
- [Endpoints da API](#endpoints-da-api)
  - [Autenticação](#autenticação)
    - [Cadastro de Profissional](#cadastro-de-profissional)
    - [Login de Profissional](#login-de-profissional)
    - [Cadastro de Paciente](#cadastro-de-paciente)
    - [Login de Paciente](#login-de-paciente)
  - [Pacientes](#pacientes)
    - [Detalhes do Paciente](#detalhes-do-paciente)
    - [Listar Pacientes de um Profissional](#listar-pacientes-de-um-profissional)
    - [Atualizar Paciente](#atualizar-paciente)
    - [Deletar Paciente](#deletar-paciente)
  - [Planos Alimentares](#planos-alimentares)
    - [Criar Plano Alimentar](#criar-plano-alimentar)
    - [Obter Plano Alimentar](#obter-plano-alimentar)
    - [Atualizar Plano Alimentar](#atualizar-plano-alimentar)
    - [Deletar Plano Alimentar](#deletar-plano-alimentar)
  - [Alimentos](#alimentos)
    - [Listar Alimentos](#listar-alimentos)
  - [Observações Gerais](#observações-gerais)

<br>


##  Visão Geral

Esta API serve como backend para um sistema nutricional, permitindo o cadastro e gerenciamento de profissionais de nutrição, pacientes, alimentos e planos alimentares.



## Tecnologias Utilizadas

* Python 3.11+
* Flask
* Flask-RESTful
* MySQL
* SQLAlchemy
* Pydantic
* python-dotenv
* JWT (Json Web Token)


## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sistema-nutricional-api.git
cd sistema-nutricional-api
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente criando um arquivo `.env` com as seguintes chaves:

```
MYSQL_HOST=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DB=
```


## Executando a Aplicação

```bash
python app.py
```

A aplicação será iniciada em `http://localhost:5000/`

<br>

# Endpoints da API

## Autenticação

### Cadastro de Profissional
**POST** `/api/professional/register`

- **Descrição:** Cadastra um novo profissional.
- **Campos obrigatórios:**
  - full_name (string, mínimo 3 caracteres)
  - email (string, formato válido)
  - password (string, mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número, 1 especial)
  - cpf (string, 11 dígitos numéricos)
  - phone (string, 11 dígitos numéricos)
  - regional_council_type (string)
  - regional_council (string)
-   **Request**
```json
{
  "full_name": "Maria Silva",
  "email": "maria@exemplo.com",
  "password": "Senha@123",
  "cpf": "12345678901",
  "phone": "11999999999",
  "regional_council_type": "CRN",
  "regional_council": "12345"
}
```
- **Responses**
  - Sucesso:
    - 201:
      ```json
      { "message": "Profissional registrado com sucesso", "access_token": "..." }
      ```
  - Erro:
    - 400:
      ```json
      { "message": "O campo full_name é obrigatório" }
      { "message": "Formato de CPF inválido" }
      ```
    - 409:
      ```json
      { "message": "Email, CPF ou número de telefone já registrado" }
      ```

---

### Login de Profissional
**POST** `/api/professional/login`

- **Descrição:** Realiza login do profissional.
- **Campos obrigatórios:**
  - login (string: email, cpf ou telefone)
  - password (string)
-   **Request**
```json
{
  "login": "maria@exemplo.com",
  "password": "Senha@123"
}
```
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "access_token": "..." }
      ```
  - Erro:
    - 400:
      ```json
      { "message": "E-mail e senha são obrigatórios" }
      ```
    - 401:
      ```json
      { "message": "Credenciais inválidas" }
      ```

---

### Cadastro de Paciente
**POST** `/api/patient/register` (requer autenticação de profissional)

- **Descrição:** Cadastra um novo paciente.
- **Campos obrigatórios:**
  - full_name (string, mínimo 3 caracteres)
  - birth_date (string, formato YYYY-MM-DD)
  - gender (string: M, F ou O)
  - email (string, formato válido)
  - password (string, mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número, 1 especial)
  - phone (string, 11 dígitos numéricos)
  - cpf (string, 11 dígitos numéricos)
  - weight (float, >0 e <=500)
  - height (float, >0 e <=3)
  - note (string, opcional)
-   **Request**
```json
{
  "full_name": "João Souza",
  "birth_date": "2000-01-01",
  "gender": "M",
  "email": "joao@exemplo.com",
  "password": "Senha@123",
  "phone": "11988888888",
  "cpf": "98765432100",
  "weight": 70.5,
  "height": 1.75,
  "note": "Paciente com histórico de diabetes"
}
```
- **Responses**
  - Sucesso:
    - 201:
      ```json
      { "message": "Paciente registrado com sucesso", "patient_id": 1 }
      ```
  - Erro:
    - 400:
      ```json
      { "message": "Nome completo deve ter pelo menos 3 caracteres" }
      { "message": "Data de nascimento deve estar no formato YYYY-MM-DD" }
      { "message": "Peso deve ser um número válido" }
      ```
    - 409:
      ```json
      { "message": "Email, CPF ou número de telefone já registrado" }
      ```

---

### Detalhes do Profissional
**GET** `/api/professional/details` (requer autenticação)

- **Descrição:** Retorna os dados do profissional autenticado.
- **Responses**
  - Sucesso:
    - 200:
      ```json
      {
        "id": "1",
        "full_name": "Maria Silva",
        "email": "maria@exemplo.com",
        "cpf": "12345678901",
        "phone": "11999999999",
        "regional_council_type": "CRN",
        "regional_council": "12345",
        "created_at": "2024-06-01 10:30:00",
        "updated_at": "2024-06-10 15:45:00"
      }
      ```
  - Erro:
    - 403:
      ```json
      { "message": "Acesso não autorizado" }
      ```
    - 404:
      ```json
      { "message": "Profissional não encontrado" }
      ```
    - 500:
      ```json
      { "message": "Erro ao obter dados do profissional: <detalhes>" }
      ```



---
### Login de Paciente
**POST** `/api/patient/login`

- **Descrição:** Realiza login do paciente.
- **Campos obrigatórios:**
  - login (string: email, cpf ou telefone)
  - password (string)
-   **Request**
```json
{
  "login": "joao@exemplo.com",
  "password": "Senha@123"
}
```
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "access_token": "..." }
      ```
  - Erro:
    - 400:
      ```json
      { "message": "Login e senha são obrigatórios" }
      ```
    - 401:
      ```json
      { "message": "Credenciais inválidas" }
      ```



## Pacientes

### Detalhes do Paciente
**GET** `/api/patient/<id>`

- **Descrição:** Retorna os dados de um paciente pelo ID.
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "patient": { ...dados do paciente... } }
      ```
  - Erro:
    - 404:
      ```json
      { "message": "O paciente com id <id> não foi encontrado." }
      ```

---

### Listar Pacientes de um Profissional
**GET** `/api/patients/<professional_id>`

- **Descrição:** Lista todos os pacientes de um profissional.
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "patients": [ ... ] }
      ```
  - Erro:
    - 404:
      ```json
      { "message": "Nenhum paciente encontrado para este profissional" }
      ```

---

### Atualizar Paciente
**PUT** `/api/patient/<id>` (requer autenticação de profissional)

- **Descrição:** Atualiza os dados de um paciente.
- Campos aceitos: full_name, birth_date, gender, email, phone, cpf, weight, height, note (todos opcionais, mas pelo menos um deve ser enviado)
-   **Request**
```json
{
  "full_name": "João Souza Atualizado",
  "weight": 72.0
}
```
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "message": "Dados do paciente atualizados com sucesso" }
      ```
  - Erro:
    - 400:
      ```json
      { "message": "Nenhum campo válido para atualização" }
      { "message": "Peso deve ser um número válido" }
      ```
    - 404:
      ```json
      { "message": "Paciente não encontrado ou não pertence ao profissional" }
      ```
    - 409:
      ```json
      { "message": "Email já registrado" }
      { "message": "CPF já registrado" }
      { "message": "Número de telefone já registrado" }
      ```

---

### Deletar Paciente
**DELETE** `/api/patient/<id>` (requer autenticação de profissional)

- **Descrição:** Remove um paciente.
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "message": "Paciente deletado com sucesso" }
      ```
  - Erro:
    - 404:
      ```json
      { "message": "Paciente não encontrado ou não pertence ao profissional" }
      ```

---

## Planos Alimentares

### Criar Plano Alimentar
**POST** `/api/mealplan` (requer autenticação de profissional)

- **Descrição:** Cria um novo plano alimentar para um paciente.
- **Campos obrigatórios:**
  - patient_id (int)
  - plan_name (string)
  - start_date (string, YYYY-MM-DD)
  - end_date (string, YYYY-MM-DD)
  - goals (string)
  - entries (lista de refeições)
  - foods (lista de alimentos por refeição)
- **Request**
```json
{
  "patient_id": 1,
  "plan_name": "Plano de Emagrecimento",
  "start_date": "2024-06-01",
  "end_date": "2024-06-30",
  "goals": "Perder peso",
  "entries": [
    {
      "meal_type_name": "Café da manhã",
      "day_of_plan": "2024-06-01",
      "time_scheduled": "08:00",
      "notes": "Sem açucar",
      "foods": [
        {
          "food_name": "Pão francês",
          "prescribed_quantity": 1.0,
          "unit_measure": "unidade",
          "energy_value_kcal": 120,
          "preparation_notes": "Retirar o miolo"
        }
      ]
    }
  ]
}
```
- **Responses**
  - Sucesso:
    - 201:
      ```json
      { "message": "Plano alimentar criado com sucesso", "meal_plan_id": 1 }
      ```
  - Erro:
    - 400:
      ```json
      { "message": "O campo 'Nome do plano' é obrigatório e não pode ser vazio" }
      { "message": "Data de início e data de término devem estar no formato YYYY-MM-DD" }
      { "message": "Quantidade prescrita deve ser maior que 0" }
      ```
    - 409:
      ```json
      { "message": "Paciente já possui plano alimentar" }
      ```
    - 500:
      ```json
      { "message": "Erro ao criar plano alimentar: <detalhes>" }
      ```

---

### Obter Plano Alimentar
**GET** `/api/mealplan/<meal_plan_id>` (requer autenticação)

- **Descrição:** Retorna detalhes de um plano alimentar.
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "meal_plan": { ...dados do plano alimentar... } }
      ```
  - Erro:
    - 404:
      ```json
      { "message": "Plano alimentar não encontrado ou acesso não autorizado" }
      ```
    - 500:
      ```json
      { "message": "Erro ao obter plano alimentar: <detalhes>" }
      ```

---

### Atualizar Plano Alimentar
**PUT** `/api/mealplan/<meal_plan_id>` (requer autenticação de profissional)

- **Descrição:** Atualiza informações básicas do plano alimentar.
- Campos aceitos: plan_name, start_date, end_date, goals
-   **Request**
```json
{
  "plan_name": "Plano Atualizado",
  "goals": "Manter peso"
}
```
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "message": "Plano alimentar atualizado com sucesso" }
      ```
  - Erro:
    - 404:
      ```json
      { "message": "Plano alimentar não encontrado ou não pertence ao profissional" }
      ```
    - 500:
      ```json
      { "message": "Erro ao atualizar plano alimentar: <detalhes>" }
      ```

---

### Deletar Plano Alimentar
**DELETE** `/api/mealplan/<meal_plan_id>` (requer autenticação de profissional)

- **Descrição:** Remove um plano alimentar.
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "message": "Plano alimentar deletado com sucesso" }
      ```
  - Erro:
    - 404:
      ```json
      { "message": "Plano alimentar não encontrado ou não pertence ao profissional" }
      ```
    - 500:
      ```json
      { "message": "Erro ao deletar plano alimentar: <detalhes>" }
      ```


## Alimentos

### Listar Alimentos
**GET** `/api/foods` (requer autenticação)

- **Descrição:** Lista todos os alimentos cadastrados, com grupo e nutrientes.
- **Responses**
  - Sucesso:
    - 200:
      ```json
      { "foods": [ ... ] }
      ```
  - Erro:
    - 500:
      ```json
      { "message": "Erro ao listar alimentos: <detalhes>" }
      ```

---

## Observações Gerais
- Todos os **Campos obrigatórios** são validados manualmente.
- Status HTTP seguem o padrão REST (200, 201, 400, 401, 403, 404, 409, 500).
- Para endpoints protegidos, envie o token JWT no header `Authorization: Bearer <token>`.

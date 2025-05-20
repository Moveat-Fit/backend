# Documentação Moveat-Fit Backend

## 📌 Sumário

* [Visão Geral](#visão-geral)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Instalação](#instalação)
* [Executando a Aplicação](#executando-a-aplicação)
* [Endpoints da API](#endpoints-da-api)
* [Exemplos de Requisições e Respostas](#exemplos-de-requisições-e-respostas)

---

## 📖 Visão Geral

Esta API serve como backend para um sistema nutricional, permitindo o cadastro e gerenciamento de profissionais de nutrição, pacientes, alimentos e planos alimentares.

---

## 🧰 Tecnologias Utilizadas

* Python 3.11+
* Flask
* Flask-RESTful
* MySQL
* SQLAlchemy
* Pydantic
* python-dotenv
* JWT (Json Web Token)

---

## 💾 Instalação

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
DB_HOST=localhost
DB_PORT=3306
DB_USER=usuario
DB_PASSWORD=senha
DB_NAME=nome_do_banco
SECRET_KEY=chave_secreta
```

---

## 🚀 Executando a Aplicação

```bash
python app.py
```

A aplicação será iniciada em `http://localhost:5000/`

---

## 📡 Endpoints da API

### 👤 Profissionais

* `POST /register`: Criação de um novo profissional
* `POST /professional`: Login de profissional

### 🧑 Pacientes

* `POST /register/patient`: Cadastro de paciente
* `GET /patients`: Lista todos os pacientes (auth JWT)
* `GET /patients/<id>`: Detalhes de um paciente (auth JWT)

### 🍽️ Planos Alimentares

* `POST /meal-plans`: Criação de plano alimentar
* `GET /meal-plans/<patient_id>`: Listagem por paciente

---

## 📬 Exemplos de Requisições e Respostas

### 🔐 POST `/register`

**Campos obrigatórios:**

* `full_name` (string)
* `email` (string)
* `password` (string)
* `cpf` (string)
* `phone` (string)
* `regional_council_type` (string)
* `regional_council` (string)

**Requisição:**

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

**Respostas:**

* `201 Created`:

```json
{
  "message": "Profissional registrado com sucesso",
  "access_token": "<jwt_token>"
}
```

* `400 Bad Request`:

```json
{
  "error": "Campos obrigatórios ausentes ou inválidos"
}
```

* `409 Conflict`:

```json
{
  "error": "Usuário já existente"
}
```

---

### 🔐 POST `/professional`

**Campos obrigatórios:**

* `login` (string)
* `password` (string)

**Requisição:**

```json
{
  "login": "email@example.com",
  "password": "Senha123!"
}
```

**Respostas:**

* `200 OK`:

```json
{
  "access_token": "<jwt_token>"
}
```

* `401 Unauthorized`:

```json
{
  "error": "Credenciais inválidas"
}
```

---

### 👶 POST `/register/patient`

**Campos obrigatórios:**

* `full_name`, `birth_date`, `gender`, `email`, `password`, `mobile`, `cpf`, `weight`, `height`

**Requisição:**

```json
{
  "full_name": "Nome Paciente",
  "birth_date": "1990-01-01",
  "gender": "M",
  "email": "paciente@example.com",
  "password": "Senha123!",
  "mobile": "11999999999",
  "cpf": "98765432100",
  "weight": 70.5,
  "height": 1.75,
  "note": "Paciente com meta de emagrecimento"
}
```

**Respostas:**

* `201 Created`:

```json
{
  "message": "Paciente registrado com sucesso"
}
```

* `400 Bad Request`:

```json
{
  "error": "Campos obrigatórios ausentes ou inválidos"
}
```

* `401 Unauthorized`:

```json
{
  "error": "Token JWT ausente ou inválido"
}
```

---

### 📋 POST `/meal-plans`

**Campos obrigatórios:**

* `patient_id`, `plan_name`, `start_date`, `end_date`, `goals`, `entries[]`
* Dentro de `entries[]`: `meal_type_id`, `day_of_plan`, `time_scheduled`, `foods[]`
* Dentro de `foods[]`: `food_id`, `prescribed_quantity_grams`, `display_portion`

**Requisição:**

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

**Respostas:**

* `201 Created`:

```json
{
  "message": "Plano alimentar criado com sucesso",
  "meal_plan_id": 1
}
```

* `400 Bad Request`:

```json
{
  "error": "Dados inválidos para criação do plano"
}
```

* `401 Unauthorized`:

```json
{
  "error": "Token JWT ausente ou inválido"
}
```

---

## ⚠️ Códigos de Status Comuns

| Código | Significado  | Quando ocorre                                   |
| ------ | ------------ | ----------------------------------------------- |
| 200    | OK           | Requisição bem-sucedida                         |
| 201    | Created      | Recurso criado com sucesso                      |
| 400    | Bad Request  | Dados ausentes, inválidos ou malformados        |
| 401    | Unauthorized | Token JWT ausente, inválido ou expirado         |
| 404    | Not Found    | Recurso não encontrado                          |
| 409    | Conflict     | Conflito de dados, como e-mail ou CPF duplicado |

---

Caso queira expandir com outros endpoints, posso continuar. Basta me avisar! ✅

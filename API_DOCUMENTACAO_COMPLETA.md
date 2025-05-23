# Documentação Completa da API - Sistema de Nutrição

---

## Autenticação

### Cadastro de Profissional
**POST** `/api/professional/register`

- Descrição: Cadastra um novo profissional.
- Campos obrigatórios:
  - full_name (string, mínimo 3 caracteres)
  - email (string, formato válido)
  - password (string, mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número, 1 especial)
  - cpf (string, 11 dígitos numéricos)
  - phone (string, 11 dígitos numéricos)
  - regional_council_type (string)
  - regional_council (string)
- Exemplo de payload:
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
- Respostas:
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

- Descrição: Realiza login do profissional.
- Campos obrigatórios:
  - login (string: email, cpf ou telefone)
  - password (string)
- Exemplo de payload:
```json
{
  "login": "maria@exemplo.com",
  "password": "Senha@123"
}
```
- Respostas:
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

- Descrição: Cadastra um novo paciente.
- Campos obrigatórios:
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
- Exemplo de payload:
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
- Respostas:
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

### Login de Paciente
**POST** `/api/patient/login`

- Descrição: Realiza login do paciente.
- Campos obrigatórios:
  - login (string: email, cpf ou telefone)
  - password (string)
- Exemplo de payload:
```json
{
  "login": "joao@exemplo.com",
  "password": "Senha@123"
}
```
- Respostas:
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

---

## Pacientes

### Detalhes do Paciente
**GET** `/api/patient/<id>`

- Descrição: Retorna os dados de um paciente pelo ID.
- Respostas:
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

- Descrição: Lista todos os pacientes de um profissional.
- Respostas:
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

- Descrição: Atualiza os dados de um paciente.
- Campos aceitos: full_name, birth_date, gender, email, phone, cpf, weight, height, note (todos opcionais, mas pelo menos um deve ser enviado)
- Exemplo de payload:
```json
{
  "full_name": "João Souza Atualizado",
  "weight": 72.0
}
```
- Respostas:
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

- Descrição: Remove um paciente.
- Respostas:
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

- Descrição: Cria um novo plano alimentar para um paciente.
- Campos obrigatórios:
  - patient_id (int)
  - plan_name (string)
  - start_date (string, YYYY-MM-DD)
  - end_date (string, YYYY-MM-DD)
  - goals (string)
  - entries (lista de refeições)
- Exemplo de payload:
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
      "notes": "Evitar açúcar",
      "foods": [
        {
          "food_id": 10,
          "prescribed_quantity_grams": 50,
          "display_portion": "1 fatia",
          "preparation_notes": "Grelhado"
        }
      ]
    }
  ]
}
```
- Respostas:
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
      { "message": "Quantidade prescrita (g) deve ser maior que 0 no alimento 1 da entrada 1" }
      ```
    - 500:
      ```json
      { "message": "Erro ao criar plano alimentar: <detalhes>" }
      ```

---

### Obter Plano Alimentar
**GET** `/api/mealplan/<meal_plan_id>` (requer autenticação)

- Descrição: Retorna detalhes de um plano alimentar.
- Respostas:
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

- Descrição: Atualiza informações básicas do plano alimentar.
- Campos aceitos: plan_name, start_date, end_date, goals
- Exemplo de payload:
```json
{
  "plan_name": "Plano Atualizado",
  "goals": "Manter peso"
}
```
- Respostas:
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

- Descrição: Remove um plano alimentar.
- Respostas:
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

---

### Listar Planos Alimentares de um Paciente
**GET** `/api/patient/<patient_id>/mealplans` (requer autenticação)

- Descrição: Lista todos os planos alimentares de um paciente.
- Respostas:
  - Sucesso:
    - 200:
      ```json
      { "meal_plans": [ ... ] }
      ```
  - Erro:
    - 404:
      ```json
      { "message": "Paciente não encontrado ou acesso não autorizado" }
      ```
    - 500:
      ```json
      { "message": "Erro ao listar planos alimentares: <detalhes>" }
      ```

---

## Alimentos

### Listar Alimentos
**GET** `/api/foods` (requer autenticação)

- Descrição: Lista todos os alimentos cadastrados, com grupo e nutrientes.
- Respostas:
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
- Todos os campos obrigatórios são validados manualmente.
- Mensagens de erro são sempre em português e amigáveis.
- Status HTTP seguem o padrão REST (200, 201, 400, 401, 403, 404, 409, 500).
- Para endpoints protegidos, envie o token JWT no header `Authorization: Bearer <token>`.

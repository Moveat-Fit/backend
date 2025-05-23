# Documentação dos Endpoints de Usuário

## 1. Cadastro de Profissional

- **Endpoint:** `/professional/register` (POST)
- **Campos obrigatórios:**
  - `full_name` (string)
  - `email` (string)
  - `password` (string)
  - `cpf` (string, 11 dígitos)
  - `phone` (string, 11 dígitos)
  - `regional_council_type` (string)
  - `regional_council` (string)
- **Mensagens de sucesso:**
  - 201: `{"message": "Profissional registrado com sucesso", "access_token": <token>}`
- **Mensagens de erro:**
  - 400: Campo obrigatório ausente, formato inválido ou senha inválida
  - 409: `{"message": "Email, CPF ou número de telefone já registrado"}`
  - 500: Erro interno do servidor

---

## 2. Login de Profissional

- **Endpoint:** `/professional/login` (POST)
- **Campos obrigatórios:**
  - `login` (string, pode ser email, cpf ou telefone)
  - `password` (string)
- **Mensagens de sucesso:**
  - 200: `{"access_token": <token>}`
- **Mensagens de erro:**
  - 400: `{"message": "E-mail e senha são obrigatórios"}`
  - 401: `{"message": "Credenciais inválidas"}`
  - 500: Erro interno do servidor

---

## 3. Login de Paciente

- **Endpoint:** `/patient/login` (POST)
- **Campos obrigatórios:**
  - `login` (string, pode ser email, cpf ou telefone)
  - `password` (string)
- **Mensagens de sucesso:**
  - 200: `{"access_token": <token>}`
- **Mensagens de erro:**
  - 400: `{"message": "Login e senha são obrigatórios"}`
  - 401: `{"message": "Credenciais inválidas"}`
  - 500: Erro interno do servidor

---

## 4. Cadastro de Paciente

- **Endpoint:** `/patient/register` (POST, requer autenticação de profissional)
- **Campos obrigatórios:**
  - `full_name` (string)
  - `birth_date` (string, formato YYYY-MM-DD)
  - `gender` (M, F ou O)
  - `email` (string)
  - `password` (string)
  - `phone` (string, 11 dígitos)
  - `cpf` (string, 11 dígitos)
  - `weight` (float)
  - `height` (float)
- **Mensagens de sucesso:**
  - 201: `{"message": "Paciente registrado com sucesso", "patient_id": <id>}`
- **Mensagens de erro:**
  - 400: Campo obrigatório ausente, formato inválido ou valor fora do permitido
  - 403: `{"message": "Acesso não autorizado"}`
  - 409: `{"message": "Email, CPF ou número de telefone já registrado"}`
  - 500: Erro interno do servidor

---

## 5. Detalhes do Paciente

- **Endpoint:** `/patient/<id>` (GET)
- **Mensagens de sucesso:**
  - 200: `{"patient": {...}}`
- **Mensagens de erro:**
  - 404: `{"message": "O paciente com id <id> não foi encontrado."}`
  - 500: Erro interno do servidor

---

## 6. Listar Pacientes de um Profissional

- **Endpoint:** `/patients/<professional_id>` (GET)
- **Mensagens de sucesso:**
  - 200: `{"patients": [...]}`
- **Mensagens de erro:**
  - 404: `{"message": "Nenhum paciente encontrado para este profissional"}`
  - 500: Erro interno do servidor

---

## 7. Deletar Paciente

- **Endpoint:** `/patient/<id>` (DELETE, requer autenticação de profissional)
- **Mensagens de sucesso:**
  - 200: `{"message": "Paciente deletado com sucesso"}`
- **Mensagens de erro:**
  - 404: `{"message": "Paciente não encontrado ou não pertence ao profissional"}`
  - 500: Erro interno do servidor

---

## 8. Atualizar Paciente

- **Endpoint:** `/patient/<id>` (PUT, requer autenticação de profissional)
- **Campos permitidos:**
  - `full_name`, `birth_date`, `gender`, `email`, `phone`, `cpf`, `weight`, `height`, `note`
- **Mensagens de sucesso:**
  - 200: `{"message": "Dados do paciente atualizados com sucesso"}`
- **Mensagens de erro:**
  - 400: Campo inválido ou valor fora do permitido
  - 404: `{"message": "Paciente não encontrado ou não pertence ao profissional"}`
  - 409: Duplicidade de email, cpf ou telefone
  - 500: Erro interno do servidor

---

## 9. Plano Alimentar (CRUD)

### Criar Plano Alimentar
- **Endpoint:** `/mealplan` (POST, requer autenticação de profissional)
- **Campos obrigatórios:**
  - `patient_id`, `start_date`, `entries` (lista de refeições)
- **Mensagens de sucesso:**
  - 201: `{"message": "Plano alimentar criado com sucesso", "meal_plan_id": <id>}`
- **Mensagens de erro:**
  - 403: `{"message": "Acesso não autorizado"}`
  - 404: `{"message": "Paciente não encontrado ou não pertence ao profissional"}`
  - 500: Erro interno do servidor

### Obter Plano Alimentar
- **Endpoint:** `/mealplan/<meal_plan_id>` (GET, autenticado)
- **Mensagens de sucesso:**
  - 200: `{"meal_plan": {...}}`
- **Mensagens de erro:**
  - 404: `{"message": "Plano alimentar não encontrado ou acesso não autorizado"}`
  - 500: Erro interno do servidor

### Atualizar Plano Alimentar
- **Endpoint:** `/mealplan/<meal_plan_id>` (PUT, requer autenticação de profissional)
- **Campos permitidos:**
  - `plan_name`, `start_date`, `end_date`, `goals`
- **Mensagens de sucesso:**
  - 200: `{"message": "Plano alimentar atualizado com sucesso"}`
- **Mensagens de erro:**
  - 403: `{"message": "Acesso não autorizado"}`
  - 404: `{"message": "Plano alimentar não encontrado ou não pertence ao profissional"}`
  - 500: Erro interno do servidor

### Deletar Plano Alimentar
- **Endpoint:** `/mealplan/<meal_plan_id>` (DELETE, requer autenticação de profissional)
- **Mensagens de sucesso:**
  - 200: `{"message": "Plano alimentar deletado com sucesso"}`
- **Mensagens de erro:**
  - 403: `{"message": "Acesso não autorizado"}`
  - 404: `{"message": "Plano alimentar não encontrado ou não pertence ao profissional"}`
  - 500: Erro interno do servidor

### Listar Planos Alimentares de um Paciente
- **Endpoint:** `/mealplans/<patient_id>` (GET, autenticado)
- **Mensagens de sucesso:**
  - 200: `{"meal_plans": [...]}`
- **Mensagens de erro:**
  - 404: `{"message": "Paciente não encontrado ou acesso não autorizado"}`
  - 500: Erro interno do servidor

---

## 10. Listar Alimentos

- **Endpoint:** `/foods` (GET, autenticado)
- **Mensagens de sucesso:**
  - 200: `{"foods": [...]}`
- **Mensagens de erro:**
  - 500: Erro interno do servidor

# Documentação da API (MoveEat)
## Visão Geral
Esta API fornece endpoints para registro de usuários, autenticação e acesso a recursos protegidos e públicos.

# Base URL
http://localhost:5000

## Endpoints
### 1. Registro de Usuário
Endpoint: /register Método: POST

### Body:
JSON
{
  "name": "Nome do Usuário",
  "email": "usuario@exemplo.com",
  "password": "senha123",
  "user_type": "Nutricionista ou Aluno"
}
Resposta de Sucesso:
Código: 201 Created
Conteúdo: { "message": "Usuário registrado com sucesso" }
Respostas de Erro:

Código: 400 Bad Request
Conteúdo: { "message": "Todos os campos são obrigatórios" }
Código: 409 Conflict
Conteúdo: { "message": "Email já cadastrado" }
Código: 500 Internal Server Error
Conteúdo: { "message": "Erro ao registrar usuário: [detalhes do erro]" }


### 2. Login de Usuário
Endpoint: /login Método: POST

### Body:
JSON
{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
Resposta de Sucesso:

Código: 200 OK
Conteúdo: { "access_token": "[token JWT]" }
Respostas de Erro:

Código: 400 Bad Request
Conteúdo: { "message": "Email e senha são obrigatórios" }
Código: 401 Unauthorized
Conteúdo: { "message": "Credenciais inválidas" }
Código: 500 Internal Server Error
Conteúdo: { "message": "Erro ao fazer login: [detalhes do erro]" }


### 3. Recurso Protegido
Endpoint: /protected Método: GET

### Headers:
Authorization: Bearer [token JWT]
Resposta de Sucesso:

Código: 200 OK
Conteúdo: { "logged_in_as": "email@do.usuario" }
Resposta de Erro:

Código: 401 Unauthorized
Conteúdo: { "msg": "Token JWT ausente ou inválido" }


### 4. Recurso Público
Endpoint: /public Método: GET

Resposta de Sucesso:

Código: 200 OK
Conteúdo: { "message": "Esta é uma rota pública" }


### 5. Teste de Conexão
Endpoint: /test-connection Método: GET

Resposta de Sucesso:

Código: 200 OK
Conteúdo: { "message": "Conexão com o backend estabelecida com sucesso!" }


# Notas Adicionais
Todos os endpoints que retornam dados enviam as respostas no formato JSON.
Para endpoints protegidos, é necessário incluir o token JWT no header Authorization como um Bearer token.
O servidor retorna códigos de erro HTTP apropriados junto com mensagens descritivas em caso de falhas.
CORS está habilitado para todas as rotas, permitindo requisições de diferentes origens.


# Tratamento de Erros
404 Not Found: Retornado quando um endpoint não é encontrado.
Conteúdo: { "error": "Endpoint não encontrado" }
500 Internal Server Error: Retornado para erros internos do servidor.
Conteúdo: { "error": "Erro interno do servidor" }

# API Documentation

Base URL: http://localhost:5000

## Endpoints:

1. Login
   - URL: /login
   - Method: POST
   - Body: { "email": "user@example.com", "password": "password123" }
   - Response: { "access_token": "eyJhbGci..." }

2. Protected Resource
   - URL: /protected
   - Method: GET
   - Headers: Authorization: Bearer <access_token>
   - Response: { "logged_in_as": "user@example.com" }

3. Public Resource
   - URL: /public
   - Method: GET
   - Response: { "message": "Esta é uma rota pública" }

4. Test Connection
   - URL: /test-connection
   - Method: GET
   - Response: { "message": "Conexão com o backend estabelecida com sucesso!" }

## Error Handling:
- 404: { "error": "Endpoint não encontrado" }
- 500: { "error": "Erro interno do servidor" }

## Authentication:
Para acessar rotas protegidas, inclua o token JWT no header da requisição:
Authorization: Bearer <access_token>

from flask_restful import Resource
from flask import request
import pyodbc
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.utils.db import connect_database  

def validate_password(password):
    """
    Verifica se a senha atende a vários critérios de segurança.
    Retorna um booleano indicando se a senha é válida ou não,
    e uma mensagem descrevendo o status da validação.
    """
    criteria = {
        'length': {'regex': r'.{8,}', 'message': 'A senha deve ter pelo menos 8 caracteres'},
        'uppercase': {'regex': r'[A-Z]', 'message': 'A senha deve conter pelo menos uma letra maiúscula'},
        'lowercase': {'regex': r'[a-z]', 'message': 'A senha deve conter pelo menos uma letra minúscula'},
        'number': {'regex': r'[0-9]', 'message': 'A senha deve conter pelo menos um número'},
        'special': {'regex': r'[!@#$%^&*(),.?":{}|<>]', 'message': 'A senha deve conter pelo menos um caractere especial'}
    }

    error_messages = []

    for key, value in criteria.items():
        if not re.search(value['regex'], password):
            error_messages.append(value['message'])

    if not error_messages:
        return True, 'Senha válida'
    else:
        return False, ' '.join(error_messages)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        cpf = data.get('cpf')
        cellphone = data.get('cellphone')
        crn = data.get('crn', None)
        cref = data.get('cref', None)
        user_type = data.get('user_type')

        if not re.match(r'^[0-9]{11}$', cpf):
            return {'message': 'Formato de CPF inválido'}, 400
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return {'message': 'Formato de e-mail inválido'}, 400
        if len(cellphone) != 11:
            return {'message': 'O número de telefone deve ter 11 caracteres'}, 400

        password_valid, password_message = validate_password(password)
        if not password_valid:
            return {'message': password_message}, 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:100000', salt_length=8)

        cnxn = connect_database  ()
        cursor = cnxn.cursor()
        try:
            cursor.execute("SELECT * FROM tb_Users WHERE Email = %s OR CPF = %s OR CellPhone = %s", (email, cpf, cellphone))
            if cursor.fetchone():
                return {'message': 'Email, CPF ou número de telefone já registrado'}, 409

            cursor.execute("""
                INSERT INTO tb_Users (Name, Email, Password, CPF, CellPhone, CRN, CREF, UserType) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, hashed_password, cpf, cellphone, crn, cref, user_type))

            cnxn.commit()
            return {'message': 'Usuário registrado com sucesso'}, 201
        except pyodbc.IntegrityError as e:
            return {'message': f'Erro de integridade de dados: {str(e)}'}, 409
        except pyodbc.Error as e:
            return {'message': f'Erro ao registrar usuário: {str(e)}'}, 500
        finally:
            cursor.close()
            cnxn.close()

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        login = data.get('login')  # Pode ser email, CPF ou celular
        password = data.get('password')

        if not login or not password:
            return {'message': 'Login e senha são obrigatórios'}, 400

        cnxn = connect_database  ()
        cursor = cnxn.cursor()
        try:
            cursor.execute("""
                SELECT Password FROM tb_Users 
                WHERE Email = %s OR CPF = %s OR CellPhone = %s
            """, (login, login, login))

            user = cursor.fetchone()
            if user and check_password_hash(user['Password'], password):
                access_token = create_access_token(identity=login)
                return {'access_token': access_token}, 200
            else:
                return {'message': 'Credenciais inválidas'}, 401
        except pyodbc.Error as e:
            return {'message': f'Erro ao fazer login: {str(e)}'}, 500
        finally:
            cursor.close()
            cnxn.close()
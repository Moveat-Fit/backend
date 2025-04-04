from flask_restful import Resource
from flask import request
import pyodbc
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.utils.db import connect_database
from datetime import datetime
import mysql.connector

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

class ProfessionalRegistration(Resource):
    def post(self):
        data = request.get_json()

        # Campos obrigatórios
        required_fields = ['full_name', 'email', 'password', 'cpf', 'phone', 'regional_council_type', 'regional_council']
        missing_or_empty = [field for field in required_fields if not data.get(field)]

        if missing_or_empty:
            return {'message': 'Campos obrigatórios ausentes ou inválidos', 'missing_fields': missing_or_empty}, 400

        # Extração e validação de cada campo
        full_name = data['full_name']
        email = data['email']
        password = data['password']
        cpf = data['cpf']
        phone = data['phone']
        regional_council_type = data['regional_council_type']
        regional_council = data['regional_council']

        # Validações de formato
        if not re.match(r'^[0-9]{11}$', cpf):
            return {'message': 'Formato de CPF inválido'}, 400
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return {'message': 'Formato de e-mail inválido'}, 400
        if len(phone) != 11:
            return {'message': 'O número de telefone deve ter 11 caracteres'}, 400

        # Validação da senha
        password_valid, password_message = validate_password(password)
        if not password_valid:
            return {'message': password_message}, 400

        # Hash da senha
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:100000', salt_length=8)

        # Conexão com o banco de dados e inserção
        cnxn = connect_database()
        cursor = cnxn.cursor()
        try:
            cursor.execute("SELECT * FROM tb_professionals WHERE email = %s OR cpf = %s OR phone = %s", (email, cpf, phone))
            if cursor.fetchone():
                return {'message': 'Email, CPF ou número de telefone já registrado'}, 409

            cursor.execute("""
                INSERT INTO tb_professionals (full_name, email, password, cpf, phone, regional_council_type, regional_council, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """, (full_name, email, hashed_password, cpf, phone, regional_council_type, regional_council))

            cnxn.commit()
            access_token = create_access_token(identity=email, additional_claims={"role": "professional"})
            return {'message': 'Profissional registrado com sucesso', 'access_token': access_token}, 201
        except Exception as e:
            cnxn.rollback()
            return {'message': str(e)}, 500
        finally:
            cursor.close()
            cnxn.close()

class ProfessionalLogin(Resource):
    def post(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return {'message': 'E-mail e senha são obrigatórios'}, 400

        cnxn = connect_database()
        cursor = cnxn.cursor()
        try:
            cursor.execute("SELECT id, password FROM tb_professionals WHERE email = %s OR cpf = %s OR phone = %s", (login, login, login))
            professional = cursor.fetchone()
            if professional and check_password_hash(professional[1], password):
                access_token = create_access_token(identity=str(professional[0]), additional_claims={"role": "professional"})
                return {'access_token': access_token}, 200
            else:
                return {'message': 'Credenciais inválidas'}, 401
        except pyodbc.Error as e:
            return {'message': f'Erro ao fazer login: {str(e)}'}, 500
        finally:
            cursor.close()
            cnxn.close()

class PatientLogin(Resource):
    def post(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return {'message': 'Login e senha são obrigatórios'}, 400

        cnxn = connect_database()
        cursor = cnxn.cursor()
        try:
            cursor.execute("SELECT id, password FROM tb_patients WHERE email = %s OR cpf = %s OR mobile = %s", (login, login, login))
            patient = cursor.fetchone()
            if patient and check_password_hash(patient[1], password):
                access_token = create_access_token(identity=str(patient[0]), additional_claims={"role": "patient"})
                return {'access_token': access_token}, 200
            else:
                return {'message': 'Credenciais inválidas'}, 401
        except pyodbc.Error as e:
            return {'message': f'Erro ao fazer login: {str(e)}'}, 500
        finally:
            cursor.close()
            cnxn.close()


class PatientRegistration(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims.get('role') != 'professional':
            return {'message': 'Acesso não autorizado'}, 403

        data = request.get_json()

        # Validações para cada campo
        errors = {}

        # Full Name
        full_name = data.get('full_name')
        if not full_name or len(full_name.strip()) < 3:
            errors['full_name'] = 'Nome completo deve ter pelo menos 3 caracteres'

        # Birth Date
        birth_date = data.get('birth_date')
        try:
            datetime.strptime(birth_date, '%Y-%d-%m')
        except ValueError:
            errors['birth_date'] = 'Data de nascimento deve estar no formato YYYY/DD/MM'

        # Gender
        gender = data.get('gender')
        if gender not in ['M', 'F', 'O']:
            errors['gender'] = 'Gênero deve ser M, F ou O'

        # Email
        email = data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            errors['email'] = 'Formato de e-mail inválido'

        # Password
        password = data.get('password')
        password_valid, password_message = validate_password(password)
        if not password_valid:
            errors['password'] = password_message

        # Mobile
        mobile = data.get('mobile')
        if not re.match(r'^[0-9]{11}$', mobile):
            errors['mobile'] = 'O número de telefone deve ter 11 dígitos numéricos'

        # CPF
        cpf = data.get('cpf')
        if not re.match(r'^[0-9]{11}$', cpf):
            errors['cpf'] = 'CPF deve ter 11 dígitos numéricos'

        # Weight
        weight = data.get('weight')
        try:
            weight = float(weight)
            if weight <= 0 or weight > 500:  # Assumindo um limite máximo de 500 kg
                errors['weight'] = 'Peso deve ser um número positivo e menor que 500'
        except (ValueError, TypeError):
            errors['weight'] = 'Peso deve ser um número válido'

        # Height
        height = data.get('height')
        try:
            height = float(height)
            if height <= 0 or height > 3:  # Assumindo que a altura está em metros e o máximo é 3 metros
                errors['height'] = 'Altura deve ser um número positivo entre 0 e 3'
        except (ValueError, TypeError):
            errors['height'] = 'Altura deve ser um número válido'

        # Note (opcional)
        note = data.get('note')

        if errors:
            return {'message': 'Erros de validação', 'errors': errors}, 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:100000', salt_length=8)

        cnxn = connect_database()
        cursor = cnxn.cursor()
        try:
            cursor.execute("SELECT * FROM tb_patients WHERE email = %s OR cpf = %s OR mobile = %s",
                           (email, cpf, mobile))
            if cursor.fetchone():
                return {'message': 'Email, CPF ou número de telefone já registrado'}, 409

            cursor.execute("""
                INSERT INTO tb_patients (full_name, birth_date, gender, email, password, mobile, cpf, weight, height, note, professional_id, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """, (
            full_name, birth_date, gender, email, hashed_password, mobile, cpf, weight, height, note, current_user))

            cnxn.commit()
            return {'message': 'Paciente registrado com sucesso'}, 201
        except pyodbc.IntegrityError as e:
            return {'message': f'Erro de integridade de dados: {str(e)}'}, 409
        except pyodbc.Error as e:
            return {'message': f'Erro ao registrar paciente: {str(e)}'}, 500
        finally:
            cursor.close()
            cnxn.close()


class PatientList(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(f"current_user: {current_user}")
        cnxn = connect_database()
        cursor = cnxn.cursor(dictionary=True)

        try:
            query = """
                SELECT 
                    id,
                    full_name,
                    DATE_FORMAT(birth_date, '%Y-%m-%d') AS birth_date,
                    gender,
                    email,
                    mobile,
                    cpf,
                    CAST(weight AS CHAR) AS weight,
                    CAST(height AS CHAR) AS height,
                    note,
                    professional_id,
                    DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at,
                    DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at
                FROM tb_patients
                WHERE professional_id = %(professional_id)s
            """
            params = {'professional_id': current_user}
            cursor.execute(query, params)
            patients = cursor.fetchall()

            return {'patients': patients}, 200

        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            return {'message': f'Erro ao buscar pacientes: {str(e)}'}, 500

        finally:
            cursor.close()
            cnxn.close()
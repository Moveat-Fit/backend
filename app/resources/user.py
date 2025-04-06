from flask_restful import Resource
from flask import request
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.utils.db import execute_query
from datetime import datetime
import logging

def validate_password(password):
    criteria = {
        'length': {'regex': r'.{8,}', 'message': 'A senha deve ter pelo menos 8 caracteres'},
        'uppercase': {'regex': r'[A-Z]', 'message': 'A senha deve conter pelo menos uma letra maiúscula'},
        'lowercase': {'regex': r'[a-z]', 'message': 'A senha deve conter pelo menos uma letra minúscula'},
        'number': {'regex': r'[0-9]', 'message': 'A senha deve conter pelo menos um número'},
        'special': {'regex': r'[!@#$%^&*(),.?":{}|<>]', 'message': 'A senha deve conter pelo menos um caractere especial'}
    }

    for key, value in criteria.items():
        if not re.search(value['regex'], password):
            return False, value['message']

    return True, 'Senha válida'

class ProfessionalRegistration(Resource):
    def post(self):
        data = request.get_json()

        required_fields = ['full_name', 'email', 'password', 'cpf', 'phone', 'regional_council_type', 'regional_council']
        for field in required_fields:
            if not data.get(field):
                return {'message': f'O campo {field} é obrigatório'}, 400

        full_name = data['full_name']
        email = data['email']
        password = data['password']
        cpf = data['cpf']
        phone = data['phone']
        regional_council_type = data['regional_council_type']
        regional_council = data['regional_council']

        if not re.match(r'^[0-9]{11}$', cpf):
            return {'message': 'Formato de CPF inválido'}, 400
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return {'message': 'Formato de e-mail inválido'}, 400
        if len(phone) != 11:
            return {'message': 'O número de telefone deve ter 11 caracteres'}, 400

        password_valid, password_message = validate_password(password)
        if not password_valid:
            return {'message': password_message}, 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:100000', salt_length=8)

        try:
            check_query = "SELECT * FROM tb_professionals WHERE email = %s OR cpf = %s OR phone = %s"
            result = execute_query(check_query, (email, cpf, phone))
            if result:
                return {'message': 'Email, CPF ou número de telefone já registrado'}, 409

            insert_query = """
                INSERT INTO tb_professionals (full_name, email, password, cpf, phone, regional_council_type, regional_council, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            execute_query(insert_query, (full_name, email, hashed_password, cpf, phone, regional_council_type, regional_council))

            access_token = create_access_token(identity=email, additional_claims={"role": "professional"})
            return {'message': 'Profissional registrado com sucesso', 'access_token': access_token}, 201
        except Exception as e:
            return {'message': str(e)}, 500

class ProfessionalLogin(Resource):
    def post(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return {'message': 'E-mail e senha são obrigatórios'}, 400

        try:
            query = """
                SELECT id, full_name, email, password, cpf, phone, regional_council_type, regional_council
                FROM tb_professionals
                WHERE email = %s OR cpf = %s OR phone = %s
            """
            result = execute_query(query, (login, login, login))
            if result and check_password_hash(result[0]['password'], password):
                user_data = {
                    'id': str(result[0]['id']),
                    'full_name': result[0]['full_name'],
                    'email': result[0]['email'],
                    'cpf': result[0]['cpf'],
                    'phone': result[0]['phone'],
                    'regional_council_type': result[0]['regional_council_type'],
                    'regional_council': result[0]['regional_council'],
                    'role': 'professional'
                }
                access_token = create_access_token(identity=str(result[0]['id']), additional_claims=user_data)
                return {'access_token': access_token}, 200
            else:
                return {'message': 'Credenciais inválidas'}, 401
        except Exception as e:
            return {'message': f'Erro ao fazer login: {str(e)}'}, 500

class PatientLogin(Resource):
    def post(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return {'message': 'Login e senha são obrigatórios'}, 400

        try:
            query = """
                SELECT id, full_name, birth_date, gender, email, password, mobile, cpf, weight, height
                FROM tb_patients
                WHERE email = %s OR cpf = %s OR mobile = %s
            """
            result = execute_query(query, (login, login, login))
            if result and check_password_hash(result[0]['password'], password):
                user_data = {
                    'id': str(result[0]['id']),
                    'full_name': result[0]['full_name'],
                    'birth_date': result[0]['birth_date'].isoformat() if result[0]['birth_date'] else None,
                    'gender': result[0]['gender'],
                    'email': result[0]['email'],
                    'mobile': result[0]['mobile'],
                    'cpf': result[0]['cpf'],
                    'weight': float(result[0]['weight']) if result[0]['weight'] else None,
                    'height': float(result[0]['height']) if result[0]['height'] else None,
                    'role': 'patient'
                }
                access_token = create_access_token(identity=str(result[0]['id']), additional_claims=user_data)
                return {'access_token': access_token}, 200
            else:
                return {'message': 'Credenciais inválidas'}, 401
        except Exception as e:
            return {'message': f'Erro ao fazer login: {str(e)}'}, 500

class PatientRegistration(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims.get('role') != 'professional':
            return {'message': 'Acesso não autorizado'}, 403

        data = request.get_json()

        full_name = data.get('full_name')
        if not full_name or len(full_name.strip()) < 3:
            return {'message': 'Nome completo deve ter pelo menos 3 caracteres'}, 400

        birth_date = data.get('birth_date')
        try:
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        except ValueError:
            return {'message': 'Data de nascimento deve estar no formato YYYY-MM-DD'}, 400

        gender = data.get('gender')
        if gender not in ['M', 'F', 'O']:
            return {'message': 'Gênero deve ser M, F ou O'}, 400

        email = data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return {'message': 'Formato de e-mail inválido'}, 400

        password = data.get('password')
        password_valid, password_message = validate_password(password)
        if not password_valid:
            return {'message': password_message}, 400

        mobile = data.get('mobile')
        if not re.match(r'^[0-9]{11}$', mobile):
            return {'message': 'O número de telefone deve ter 11 dígitos numéricos'}, 400

        cpf = data.get('cpf')
        if not re.match(r'^[0-9]{11}$', cpf):
            return {'message': 'CPF deve ter 11 dígitos numéricos'}, 400

        weight = data.get('weight')
        try:
            weight = float(weight)
            if weight <= 0 or weight > 500:
                return {'message': 'Peso deve ser um número positivo e menor que 500'}, 400
        except (ValueError, TypeError):
            return {'message': 'Peso deve ser um número válido'}, 400

        height = data.get('height')
        try:
            height = float(height)
            if height <= 0 or height > 3:
                return {'message': 'Altura deve ser um número positivo entre 0 e 3'}, 400
        except (ValueError, TypeError):
            return {'message': 'Altura deve ser um número válido'}, 400

        note = data.get('note')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:100000', salt_length=8)

        try:
            check_query = "SELECT * FROM tb_patients WHERE email = %s OR cpf = %s OR mobile = %s"
            result = execute_query(check_query, (email, cpf, mobile))
            if result:
                return {'message': 'Email, CPF ou número de telefone já registrado'}, 409

            insert_query = """
                INSERT INTO tb_patients (full_name, birth_date, gender, email, password, mobile, cpf, weight, height, note, professional_id, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            execute_query(insert_query, (full_name, birth_date, gender, email, hashed_password, mobile, cpf, weight, height, note, current_user))

            return {'message': 'Paciente registrado com sucesso'}, 201
        except Exception as e:
            return {'message': f'Erro ao registrar paciente: {str(e)}'}, 500

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PatientList(Resource):
    def get(self, professional_id):
        logger.debug(f"Received request for professional_id: {professional_id}")
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
            logger.debug(f"Executing query with professional_id: {professional_id}")
            patients = execute_query(query, {'professional_id': professional_id})
            logger.debug(f"Query result: {patients}")

            if patients:
                return {'patients': patients}, 200
            else:
                return {'message': 'Nenhum paciente encontrado para este profissional'}, 404
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
            return {'message': f'Erro ao buscar pacientes: {str(e)}'}, 500
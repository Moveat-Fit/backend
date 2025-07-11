from flask_restful import Resource
from flask import request, jsonify
import re
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.utils.db import execute_query
from datetime import datetime, date
import logging
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import List, Optional
from app.utils.db import convert_decimal

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
                SELECT id, full_name, birth_date, gender, email, password, phone, cpf, weight, height
                FROM tb_patients
                WHERE email = %s OR cpf = %s OR phone = %s
            """
            result = execute_query(query, (login, login, login))
            if result and check_password_hash(result[0]['password'], password):
                user_data = {
                    'id': str(result[0]['id']),
                    'full_name': result[0]['full_name'],
                    'birth_date': result[0]['birth_date'].isoformat() if result[0]['birth_date'] else None,
                    'gender': result[0]['gender'],
                    'email': result[0]['email'],
                    'phone': result[0]['phone'],
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

        phone = data.get('phone')
        if not re.match(r'^[0-9]{11}$', phone):
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
            check_query = "SELECT * FROM tb_patients WHERE email = %s OR cpf = %s OR phone = %s"
            result = execute_query(check_query, (email, cpf, phone))
            if result:
                return {'message': 'Email, CPF ou número de telefone já registrado'}, 409

            insert_query = """
                        INSERT INTO tb_patients (full_name, birth_date, gender, email, password, phone, 
                        cpf, weight, height, note, professional_id, created_at, updated_at) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    """
            execute_query(insert_query, (full_name, birth_date, gender, email, hashed_password,
                                         phone, cpf, weight, height, note, current_user))

            # Consultar o paciente recém-inserido usando campos únicos
            get_patient_query = """
                        SELECT id FROM tb_patients 
                        WHERE email = %s AND cpf = %s AND phone = %s
                        ORDER BY created_at DESC LIMIT 1
                    """
            result = execute_query(get_patient_query, (email, cpf, phone))
            patient_id = result[0]['id'] if result else None

            if patient_id is None:
                return {'message': 'Erro ao obter ID do paciente'}, 500

            return {'message': 'Paciente registrado com sucesso', 'patient_id': patient_id}, 201

        except Exception as e:
            return {'message': f'Erro ao registrar paciente: {str(e)}'}, 500

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PatientDetails(Resource):
    def get(self, id):
        logger.debug(f"Received request for patient ID: {id}")
        try:
            query = """
                SELECT
                    id,
                    full_name,
                    DATE_FORMAT(birth_date, '%%Y-%%m-%%d') AS birth_date,
                    gender,
                    email,
                    phone,
                    cpf,
                    CAST(weight AS CHAR) AS weight,
                    CAST(height AS CHAR) AS height,
                    note,
                    professional_id,
                    DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS created_at,
                    DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS updated_at
                FROM tb_patients
                WHERE id = %(id)s
            """
            logger.debug(f"Executing query with patient id: {id}")
            patientDetails = execute_query(query, {'id': id})
            logger.debug(f"Query result: {patientDetails}")


            if not patientDetails != None or not len(patientDetails) > 0:
                return {'message': f'O paciente com id {id} não foi encontrado.'}, 404

            return {'patient': patientDetails}, 200

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
            return {'message': f'Erro ao buscar paciente: {str(e)}'}, 500

class PatientList(Resource):
    def get(self, professional_id):
        logger.debug(f"Received request for professional_id: {professional_id}")
        try:
            query = """
                SELECT
                    id,
                    full_name,
                    DATE_FORMAT(birth_date, '%%Y-%%m-%%d') AS birth_date,
                    gender,
                    email,
                    phone,
                    cpf,
                    CAST(weight AS CHAR) AS weight,
                    CAST(height AS CHAR) AS height,
                    note,
                    professional_id,
                    DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS created_at,
                    DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS updated_at
                FROM tb_patients
                WHERE professional_id = %(professional_id)s
            """
            logger.debug(f"Executing query with professional_id: {professional_id}")
            patients = execute_query(query, {'professional_id': professional_id})
            logger.debug(f"Query result: {patients}")

            if patients or patients.__sizeof__() > 0:
                return {'patients': patients}, 200
            else:
                return {'message': 'Nenhum paciente encontrado para este profissional'}, 404
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
            return {'message': f'Erro ao buscar pacientes: {str(e)}'}, 500

class DeletePatient(Resource):
    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        try:
            # Verificar se o paciente pertence ao profissional logado
            check_query = "SELECT id FROM tb_patients WHERE id = %s AND professional_id = %s"
            result = execute_query(check_query, (id, current_user))
            if not result:
                return {'message': 'Paciente não encontrado ou não pertence ao profissional'}, 404

            # Deletar o paciente
            delete_query = "DELETE FROM tb_patients WHERE id = %s"
            execute_query(delete_query, (id,))
            return {'message': 'Paciente deletado com sucesso'}, 200
        except Exception as e:
            return {'message': f'Erro ao deletar paciente: {str(e)}'}, 500

class UpdatePatient(Resource):
    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        data = request.get_json()

        try:
            # Verificar se o paciente pertence ao profissional logado
            check_query = "SELECT id FROM tb_patients WHERE id = %s AND professional_id = %s"
            result = execute_query(check_query, (id, current_user))
            if not result:
                return {'message': 'Paciente não encontrado ou não pertence ao profissional'}, 404

            # Verificar duplicidade de campos únicos antes da atualização
            if any(field in data for field in ['email', 'cpf', 'phone']):
                check_duplicates_query = """
                            SELECT email, cpf, phone FROM tb_patients 
                            WHERE id != %s AND (
                                email = %s OR 
                                cpf = %s OR 
                                phone = %s
                            )
                        """
                duplicate_check = execute_query(
                    check_duplicates_query,
                    (
                        id,
                        data.get('email', ''),
                        data.get('cpf', ''),
                        data.get('phone', '')
                    )
                )

                if duplicate_check:
                    duplicate_record = duplicate_check[0]
                    if 'email' in data and data['email'] == duplicate_record['email']:
                        return {'message': 'Email já registrado'}, 409
                    if 'cpf' in data and data['cpf'] == duplicate_record['cpf']:
                        return {'message': 'CPF já registrado'}, 409
                    if 'phone' in data and data['phone'] == duplicate_record['phone']:
                        return {'message': 'Número de telefone já registrado'}, 409

            # Resto do código de validação permanece o mesmo
            fields_to_update = []
            values = []

            if 'full_name' in data:
                full_name = data['full_name']
                if not full_name or len(full_name.strip()) < 3:
                    return {'message': 'Nome completo deve ter pelo menos 3 caracteres'}, 400
                fields_to_update.append('full_name = %s')
                values.append(full_name)

            if 'birth_date' in data:
                try:
                    birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
                    fields_to_update.append('birth_date = %s')
                    values.append(birth_date)
                except ValueError:
                    return {'message': 'Data de nascimento deve estar no formato YYYY-MM-DD'}, 400

            if 'gender' in data:
                gender = data['gender']
                if gender not in ['M', 'F', 'O']:
                    return {'message': 'Gênero deve ser M, F ou O'}, 400
                fields_to_update.append('gender = %s')
                values.append(gender)

            if 'email' in data:
                email = data['email']
                if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                    return {'message': 'Formato de e-mail inválido'}, 400
                fields_to_update.append('email = %s')
                values.append(email)

            if 'phone' in data:
                phone = data['phone']
                if not re.match(r'^[0-9]{11}$', phone):
                    return {'message': 'O número de telefone deve ter 11 dígitos numéricos'}, 400
                fields_to_update.append('phone = %s')
                values.append(phone)

            if 'cpf' in data:
                cpf = data['cpf']
                if not re.match(r'^[0-9]{11}$', cpf):
                    return {'message': 'CPF deve ter 11 dígitos numéricos'}, 400
                fields_to_update.append('cpf = %s')
                values.append(cpf)

            if 'weight' in data:
                try:
                    weight = float(data['weight'])
                    if weight <= 0 or weight > 500:
                        return {'message': 'Peso deve ser um número positivo e menor que 500'}, 400
                    fields_to_update.append('weight = %s')
                    values.append(weight)
                except (ValueError, TypeError):
                    return {'message': 'Peso deve ser um número válido'}, 400

            if 'height' in data:
                try:
                    height = float(data['height'])
                    if height <= 0 or height > 3:
                        return {'message': 'Altura deve ser um número positivo entre 0 e 3'}, 400
                    fields_to_update.append('height = %s')
                    values.append(height)
                except (ValueError, TypeError):
                    return {'message': 'Altura deve ser um número válido'}, 400

            if 'note' in data:
                fields_to_update.append('note = %s')
                values.append(data['note'])

            if not fields_to_update:
                return {'message': 'Nenhum campo válido para atualização'}, 400

            # Atualizar os dados do paciente
            update_query = f"UPDATE tb_patients SET {', '.join(fields_to_update)}, updated_at = NOW() WHERE id = %s"
            values.append(id)
            execute_query(update_query, tuple(values))

            return {'message': 'Dados do paciente atualizados com sucesso'}, 200

        except Exception as e:
            # Log do erro para debugging
            logging.error(f"Erro na atualização do paciente: {str(e)}")
            return {'message': 'Erro ao atualizar dados do paciente'}, 500

# Plano Alimentar

class MealPlanFood(BaseModel):
    food_id: int
    prescribed_quantity_grams: float = Field(..., gt=0)
    display_portion: str
    preparation_notes: Optional[str] = None

class MealPlanEntry(BaseModel):
    meal_type_name: str
    day_of_plan: date
    time_scheduled: str
    notes: Optional[str] = None
    foods: List[MealPlanFood]

class MealPlanCreate(BaseModel):
    patient_id: int
    plan_name: str
    start_date: date
    end_date: date
    goals: str
    entries: List[MealPlanEntry]

class MealPlanUpdate(BaseModel):
    plan_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    goals: Optional[str] = None


class CreateMealPlan(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims.get('role') != 'professional':
            return {'message': 'Acesso não autorizado'}, 403

        data = request.get_json()

        # verificação: paciente já possui plano alimentar?
        patient_id = data.get('patient_id')
        check_patient_query = "SELECT id FROM tb_patient_meal_plans WHERE patient_id = %s"
        existing_plan = execute_query(check_patient_query, (patient_id,))
        if existing_plan:
            return {'message': 'Este paciente já possui um plano alimentar cadastrado'}, 409

        # validação: campos obrigatórios
        required_fields = ['patient_id', 'plan_name', 'start_date', 'end_date', 'entries']
        for field in required_fields:
            if not data.get(field) or (isinstance(data.get(field), str) and not data.get(field).strip()):
                return {'message': f"O campo '{field}' é obrigatório e não pode ser vazio"}, 400

        if not isinstance(data['entries'], list) or not data['entries']:
            return {'message': 'entries deve ser uma lista não vazia'}, 400

        # validação: existência dos alimentos
        for idx, entry in enumerate(data['entries']):
            for field in ['meal_type_name', 'day_of_plan', 'time_scheduled', 'foods']:
                if not entry.get(field) or (isinstance(entry.get(field), str) and not entry.get(field).strip()):
                    return {'message': f"O campo '{field}' é obrigatório e não pode ser vazio"}, 400

            if not isinstance(entry['foods'], list) or not entry['foods']:
                return {'message': f"Alimentos é obrigatório na entrada {idx+1} e não pode ser vazio"}, 400

            for fidx, food in enumerate(entry['foods']):
                for field in ['food_name', 'prescribed_quantity', 'unit_measure', 'energy_value_kcal']:
                    if food.get(field) in [None, ""]:
                        return {'message': f"O campo '{field}' é obrigatório no alimento {fidx+1} da entrada {idx+1} e não pode ser vazio"}, 400

                # Checagem de existência do alimento
                food_name = food['food_name']
                food_id_query = "SELECT id FROM tb_foods WHERE name = %s"
                food_id_result = execute_query(food_id_query, (food_name,))
                if not food_id_result:
                    return {'message': f"Alimento '{food_name}' não encontrado no banco de dados"}, 400

        try:
            # cria plano alimentar
            insert_meal_plan_query = """
                INSERT INTO tb_patient_meal_plans
                    (patient_id, professional_id, plan_name, start_date, end_date, goals)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            meal_plan_id = execute_query(
                insert_meal_plan_query,
                (
                    data['patient_id'],
                    current_user,
                    data['plan_name'],
                    data['start_date'],
                    data['end_date'],
                    data['goals']
                ),
                return_id=True
            )

            if not meal_plan_id:
                return {'message': 'Erro ao criar plano alimentar'}, 500

            for entry in data['entries']:
                insert_entry_query = """
                    INSERT INTO tb_meal_plan_entries
                        (meal_plan_id, meal_type_name, day_of_plan, time_scheduled, notes, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                """
                entry_id = execute_query(
                    insert_entry_query,
                    (
                        meal_plan_id,
                        entry['meal_type_name'],
                        entry['day_of_plan'],
                        entry['time_scheduled'],
                        entry.get('notes')
                    ),
                    return_id=True
                )

                if not entry_id:
                    return {'message': 'Erro ao criar entrada do plano alimentar'}, 500

                for food in entry['foods']:
                    # Buscar o food_id pelo food_name
                    food_id_query = "SELECT id FROM tb_foods WHERE name = %s"
                    food_id_result = execute_query(food_id_query, (food['food_name'],))
                    food_id = food_id_result[0]['id']

                    prescribed_quantity = float(food['prescribed_quantity'])
                    unit_measure = food['unit_measure']

                    insert_food_query = """
                        INSERT INTO tb_meal_plan_foods
                        (meal_plan_entry_id, food_id, prescribed_portion, prescribed_unit_measure, prescribed_quantity_grams, preparation_notes, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                    """
                    execute_query(
                        insert_food_query,
                        (
                            entry_id,
                            food_id,
                            prescribed_quantity,
                            unit_measure,
                            prescribed_quantity,
                            food.get('preparation_notes')
                        )
                    )

            return {'message': 'Plano alimentar criado com sucesso', 'meal_plan_id': meal_plan_id}, 201

        except Exception as e:
            logger.error(f"Erro ao criar plano alimentar: {str(e)}", exc_info=True)
            return {'message': f'Erro ao criar plano alimentar: {str(e)}'}, 500


class GetMealPlan(Resource):
    @jwt_required()
    def get(self, patient_id):
        try:
            current_user = get_jwt_identity()
            claims = get_jwt()

            plan_query = """
                SELECT 
                    id, patient_id, professional_id, plan_name,
                    DATE_FORMAT(start_date, '%%Y-%%m-%%d') as start_date,
                    DATE_FORMAT(end_date, '%%Y-%%m-%%d') as end_date,
                    goals,
                    DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i:%%s') as created_at,
                    DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:%%i:%%s') as updated_at
                FROM tb_patient_meal_plans
                WHERE patient_id = %s
                LIMIT 1
            """
            plan_result = execute_query(plan_query, (patient_id,))
            if not plan_result:
                return {'message': 'Plano alimentar não encontrado'}, 404

            plan_info = plan_result[0]

            # Permissão: profissional só vê seus pacientes, paciente só vê seu próprio plano
            if claims.get('role') == 'professional' and plan_info['professional_id'] != int(current_user):
                return {'message': 'Acesso não autorizado'}, 403
            if claims.get('role') == 'patient' and plan_info['patient_id'] != int(current_user):
                return {'message': 'Acesso não autorizado'}, 403

            # Busca todas as entradas do plano alimentar
            entries_query = """
                SELECT 
                    mpe.id, 
                    mpe.meal_type_name,
                    DATE_FORMAT(mpe.day_of_plan, '%%Y-%%m-%%d') as day_of_plan,
                    TIME_FORMAT(mpe.time_scheduled, '%%H:%%i') as time_scheduled,
                    mpe.notes
                FROM tb_meal_plan_entries mpe
                WHERE mpe.meal_plan_id = %s
                ORDER BY mpe.day_of_plan, mpe.time_scheduled
            """
            entries = execute_query(entries_query, (plan_info['id'],))

            for entry in entries:
                foods_query = """
                    SELECT 
                        f.name as food_name,
                        mpf.prescribed_quantity_grams as prescribed_quantity,
                        mpf.prescribed_unit_measure as unit_measure,
                        f.energy_value_kcal,
                        mpf.preparation_notes
                    FROM tb_meal_plan_foods mpf
                    JOIN tb_foods f ON mpf.food_id = f.id
                    WHERE mpf.meal_plan_entry_id = %s
                """
                foods_result = execute_query(foods_query, (entry['id'],))
                foods = []
                for food in foods_result:
                    foods.append({
                        "food_name": food['food_name'],
                        "prescribed_quantity": float(food['prescribed_quantity']) if food['prescribed_quantity'] is not None else None,
                        "unit_measure": food['unit_measure'],
                        "energy_value_kcal": float(food['energy_value_kcal']) if food['energy_value_kcal'] is not None else None,
                        "preparation_notes": food['preparation_notes']
                    })
                entry['foods'] = foods

            plan_info['entries'] = entries

            return {'meal_plan': convert_decimal(plan_info)}, 200

        except Exception as e:
            logger.error(f"Erro ao obter plano alimentar: {str(e)}", exc_info=True)
            return {'message': f'Erro ao obter plano alimentar: {str(e)}'}, 500


class UpdateMealPlan(Resource):
    @jwt_required()
    def put(self, patient_id):
        try:
            current_user = get_jwt_identity()
            claims = get_jwt()
            if claims.get('role') != 'professional':
                return {'message': 'Acesso não autorizado'}, 403

            data = request.get_json()

            check_plan_query = """
                SELECT id FROM tb_patient_meal_plans
                WHERE patient_id = %s AND professional_id = %s
            """
            plan = execute_query(check_plan_query, (patient_id, current_user))
            if not plan:
                return {'message': 'Plano alimentar não encontrado ou não pertence ao profissional'}, 404

            meal_plan_id = plan[0]['id']

            update_fields = []
            update_values = []
            for field in ['plan_name', 'start_date', 'end_date', 'goals']:
                if data.get(field) is not None:
                    update_fields.append(f"{field} = %s")
                    update_values.append(data[field])
            if update_fields:
                update_query = f"""
                    UPDATE tb_patient_meal_plans
                    SET {', '.join(update_fields)}, updated_at = NOW()
                    WHERE id = %s
                """
                update_values.append(meal_plan_id)
                execute_query(update_query, tuple(update_values))

            # Atualizar entradas e alimentos (entries)
            if 'entries' in data and isinstance(data['entries'], list):
                # Remove todas as entradas e alimentos antigos
                get_entries_query = "SELECT id FROM tb_meal_plan_entries WHERE meal_plan_id = %s"
                old_entries = execute_query(get_entries_query, (meal_plan_id,))
                for entry in old_entries:
                    execute_query("DELETE FROM tb_meal_plan_foods WHERE meal_plan_entry_id = %s", (entry['id'],))
                execute_query("DELETE FROM tb_meal_plan_entries WHERE meal_plan_id = %s", (meal_plan_id,))

                # Insere as novas entradas e alimentos
                for entry in data['entries']:
                    insert_entry_query = """
                        INSERT INTO tb_meal_plan_entries
                            (meal_plan_id, meal_type_name, day_of_plan, time_scheduled, notes, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                    """
                    entry_id = execute_query(
                        insert_entry_query,
                        (
                            meal_plan_id,
                            entry['meal_type_name'],
                            entry['day_of_plan'],
                            entry['time_scheduled'],
                            entry.get('notes')
                        ),
                        return_id=True
                    )
                    for food in entry['foods']:
                        food_id_query = "SELECT id FROM tb_foods WHERE name = %s"
                        food_id_result = execute_query(food_id_query, (food['food_name'],))
                        if not food_id_result:
                            return {'message': f"Alimento '{food['food_name']}' não encontrado no banco de dados"}, 400
                        food_id = food_id_result[0]['id']
                        prescribed_quantity = float(food['prescribed_quantity'])
                        unit_measure = food['unit_measure']
                        insert_food_query = """
                            INSERT INTO tb_meal_plan_foods
                            (meal_plan_entry_id, food_id, prescribed_portion, prescribed_unit_measure, prescribed_quantity_grams, preparation_notes, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                        """
                        execute_query(
                            insert_food_query,
                            (
                                entry_id,
                                food_id,
                                prescribed_quantity,
                                unit_measure,
                                prescribed_quantity,
                                food.get('preparation_notes')
                            )
                        )

            return {'message': 'Plano alimentar atualizado com sucesso'}, 200

        except Exception as e:
            logger.error(f"Erro ao atualizar plano alimentar: {str(e)}", exc_info=True)
            return {'message': f'Erro ao atualizar plano alimentar: {str(e)}'}, 500

class DeleteMealPlan(Resource):
    @jwt_required()
    def delete(self, patient_id):
        try:
            current_user = get_jwt_identity()
            claims = get_jwt()

            if claims.get('role') != 'professional':
                return {'message': 'Acesso não autorizado'}, 403


            check_plan_query = """
                SELECT id FROM tb_patient_meal_plans
                WHERE patient_id = %s AND professional_id = %s
            """
            plan = execute_query(check_plan_query, (patient_id, current_user))
            if not plan:
                return {'message': 'Plano alimentar não encontrado ou não pertence ao profissional'}, 404

            meal_plan_id = plan[0]['id']

            # Deletar alimentos das refeições do plano
            delete_foods_query = """
                DELETE mpf FROM tb_meal_plan_foods mpf
                JOIN tb_meal_plan_entries mpe ON mpf.meal_plan_entry_id = mpe.id
                WHERE mpe.meal_plan_id = %s
            """
            execute_query(delete_foods_query, (meal_plan_id,))

            # Deletar refeições do plano
            delete_entries_query = "DELETE FROM tb_meal_plan_entries WHERE meal_plan_id = %s"
            execute_query(delete_entries_query, (meal_plan_id,))

            # Deletar o plano
            delete_query = "DELETE FROM tb_patient_meal_plans WHERE id = %s"
            execute_query(delete_query, (meal_plan_id,))

            return {'message': 'Plano alimentar deletado com sucesso'}, 200

        except Exception as e:
            logger.error(f"Erro ao deletar plano alimentar: {str(e)}", exc_info=True)
            return {'message': f'Erro ao deletar plano alimentar: {str(e)}'}, 500



class FoodList(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            claims = get_jwt()

            query = """
                SELECT 
                    id,
                    name,
                    food_group_name,
                    default_portion_grams,
                    energy_value_kcal,
                    portion,
                    unit_measure
                FROM tb_foods
                ORDER BY id ASC
            """

            foods = execute_query(query)

            result = []
            for food in foods:
                default_portion = {
                    "grams": float(food['default_portion_grams']) if food['default_portion_grams'] is not None else None,
                    "energy_value_kcal": float(food['energy_value_kcal']) if food['energy_value_kcal'] is not None else None,
                    "portion": float(food['portion']) if food['portion'] is not None else None,
                    "unit_measure": food['unit_measure']
                }
                formatted_food = {
                    "id": food['id'],
                    "name": food['name'],
                    "food_group": food['food_group_name'],
                    "default_portion": default_portion
                }
                result.append(formatted_food)

            return result, 200

        except Exception as e:
            logger.error(f"Erro ao listar alimentos: {str(e)}", exc_info=True)
            return {'message': f'Erro ao listar alimentos: {str(e)}'}, 500

class ProfessionalDetails(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            claims = get_jwt()

            # Verificar se o usuário é um profissional
            if claims.get('role') != 'professional':
                return {'message': 'Acesso não autorizado'}, 403

            # Consultar os dados do profissional
            query = """
                SELECT 
                    id,
                    full_name,
                    email,
                    cpf,
                    phone,
                    regional_council_type,
                    regional_council,
                    DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS created_at,
                    DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS updated_at
                FROM tb_professionals
                WHERE id = %s
            """
            professional = execute_query(query, (current_user,))

            if not professional:
                return {'message': 'Profissional não encontrado'}, 404

            # Formatar os dados de retorno
            professional_data = {
                'id': str(professional[0]['id']),
                'full_name': professional[0]['full_name'],
                'email': professional[0]['email'],
                'cpf': professional[0]['cpf'],
                'phone': professional[0]['phone'],
                'regional_council_type': professional[0]['regional_council_type'],
                'regional_council': professional[0]['regional_council'],
                'created_at': professional[0]['created_at'],
                'updated_at': professional[0]['updated_at']
            }

            return professional_data, 200

        except Exception as e:
            logger.error(f"Erro ao obter dados do profissional: {str(e)}", exc_info=True)
            return {'message': f'Erro ao obter dados do profissional: {str(e)}'}, 500
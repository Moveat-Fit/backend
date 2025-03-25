from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.utils.db import connect_database

class PatientRegistration(Resource):
    @jwt_required()
    def post(self):
        # Acessar a identidade do usuário atual e verificar se é um profissional
        claims = get_jwt()
        if claims.get('role') != 'professional':
            return {'message': 'Acesso negado. Apenas profissionais podem registrar pacientes.'}, 403

        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        cpf = data.get('cpf')
        cellphone = data.get('cellphone')

        # Aqui você pode adicionar mais validações conforme necessário

        hashed_password = generate_password_hash('senha_inicial', method='pbkdf2:sha256:100000', salt_length=8)

        cnxn = connect_database()
        cursor = cnxn.cursor()
        try:
            cursor.execute("SELECT * FROM tb_Patients WHERE Email = %s OR CPF = %s OR CellPhone = %s", (email, cpf, cellphone))
            if cursor.fetchone():
                return {'message': 'Email, CPF ou número de telefone já registrado'}, 409

            cursor.execute("""
                INSERT INTO tb_Patients (Name, Email, Password, CPF, CellPhone) 
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, hashed_password, cpf, cellphone))

            cnxn.commit()
            return {'message': 'Paciente registrado com sucesso'}, 201
        except Exception as e:
            return {'message': f'Erro ao registrar paciente: {str(e)}'}, 500
        finally:
            cursor.close()
            cnxn.close()

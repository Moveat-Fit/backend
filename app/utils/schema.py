import pymysql
from dotenv import load_dotenv
import os
import decimal

load_dotenv()

def connect_database():
    try:
        cnxn = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Conexão estabelecida.")
        return cnxn
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def create_tables(cnxn):
    if cnxn is None:
        print("Não foi possível criar as tabelas, pois a conexão falhou.")
        return

    sql_commands = [

        "DROP TABLE IF EXISTS tb_meal_plan_foods;",
        "DROP TABLE IF EXISTS tb_food_nutrients;",

        "DROP TABLE IF EXISTS tb_foods;",
        "DROP TABLE IF EXISTS tb_food_groups;",
        "DROP TABLE IF EXISTS tb_nutrients;",
        "DROP TABLE IF EXISTS tb_meal_types;",

        """
        CREATE TABLE IF NOT EXISTS tb_professionals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            cpf CHAR(11) UNIQUE NOT NULL,
            phone VARCHAR(15) NOT NULL,
            regional_council_type VARCHAR(50) NOT NULL,
            regional_council VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT uq_professional_council UNIQUE (regional_council_type, regional_council),
            CONSTRAINT chk_prof_full_name CHECK (CHAR_LENGTH(TRIM(full_name)) > 0),
            CONSTRAINT chk_prof_email CHECK (email LIKE '%_@__%.__%'),
            CONSTRAINT chk_prof_phone CHECK (CHAR_LENGTH(TRIM(phone)) >= 10)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL,
            gender ENUM('M', 'F', 'Other') NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(15) NOT NULL,
            cpf CHAR(11) UNIQUE NOT NULL,
            weight DECIMAL(5,2) NOT NULL,
            height DECIMAL(3,2) NOT NULL,
            note TEXT,
            professional_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (professional_id) REFERENCES tb_professionals(id) ON DELETE RESTRICT,
            CONSTRAINT chk_patient_full_name CHECK (CHAR_LENGTH(TRIM(full_name)) > 0),
            CONSTRAINT chk_patient_email CHECK (email LIKE '%_@__%.__%'),
            CONSTRAINT chk_patient_phone CHECK (CHAR_LENGTH(TRIM(phone)) >= 10)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_foods (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            food_group_name VARCHAR(100),
            default_portion_grams DECIMAL(7,2) NULL,
            energy_value_kcal DECIMAL(7,2) NULL,
            portion DECIMAL(7,2) NULL,
            unit_measure VARCHAR(50) NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_patient_meal_plans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            professional_id INT NOT NULL,
            plan_name VARCHAR(255) NOT NULL DEFAULT 'Plano Nutricional Padrão',
            start_date DATE NOT NULL,
            end_date DATE,
            goals TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES tb_patients(id) ON DELETE CASCADE,
            FOREIGN KEY (professional_id) REFERENCES tb_professionals(id) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_meal_plan_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            meal_plan_id INT NOT NULL,
            meal_type_name VARCHAR(100) NOT NULL,
            day_of_plan DATE NOT NULL,
            time_scheduled TIME NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (meal_plan_id) REFERENCES tb_patient_meal_plans(id) ON DELETE CASCADE,
            UNIQUE KEY uq_meal_entry (meal_plan_id, meal_type_name, day_of_plan)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_meal_plan_foods (
            id INT AUTO_INCREMENT PRIMARY KEY,
            meal_plan_entry_id INT NOT NULL,
            food_id INT NOT NULL,
            prescribed_portion DECIMAL(7,2) NOT NULL,
            prescribed_unit_measure VARCHAR(50) NOT NULL,  
            prescribed_quantity_grams DECIMAL(7,2) NOT NULL,
            preparation_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (meal_plan_entry_id) REFERENCES tb_meal_plan_entries(id) ON DELETE CASCADE,
            FOREIGN KEY (food_id) REFERENCES tb_foods(id) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    ]

    try:
        cursor = cnxn.cursor()
        
        for command_index, command in enumerate(sql_commands):
            try:

                cursor.execute(command)
            except pymysql.MySQLError as e:
                if e.args[0] == 1051 and "DROP TABLE IF EXISTS" in command.upper():
                    print(
                        f"  Info: Tabela para DROP '{command.strip()[:50]}...' não existia ou já removida.")
                else:
                    print(
                        f"  Erro ao executar comando: {command.strip()[:100]}... \n  ERRO: {e}")

        print("Estrutura das tabelas verificada/atualizada com sucesso.")
    except pymysql.MySQLError as e:
        print(f"Erro geral ao criar/atualizar as tabelas: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


def insert_initial_data(cnxn):
    """Insere dados iniciais na tabela tb_foods"""
    if cnxn is None:
        print("Não foi possível inserir os dados iniciais, pois a conexão falhou.")
        return

    foods_data_tuples = [
        ('Feijão carioca cozido', 'Vegetais', 140.0, 98.0, 1.0, 'concha cheia'),
        ('Arroz branco cozido', 'Cereais', 45.0, 58.0, 1.0, 'colher de arroz cheia'),
        ('Batata inglesa cozida', 'Cereais', 30.0, 15.0, 1.0, 'colher de sopa cheia'),
        ('Batata doce cozida', 'Cereais', 42.0, 38.0, 1.0, 'colher de sopa cheia'),
        ('Macarrão cozido', 'Cereais', 50.0, 63.0, 1.0, 'colher de servir cheia'),
        ('Pão francês', 'Cereais', 50.0, 150.0, 1.0, 'unidade'),
        ('Pão de forma tradicional', 'Cereais', 25.0, 65.0, 1.0, 'fatia'),
        ('Goma de tapioca', 'Cereais', 15.0, 43.0, 1.0, 'colher de sopa rasa'),
        ('Abóbora cozida', 'Vegetais', 36.0, 18.0, 1.0, 'colher de sopa cheia'),
        ('Berinjela cozida', 'Vegetais', 75.0, 20.0, 1.0, 'colher de servir cheia'),
        ('Cenoura cozida (picada)', 'Vegetais', 25.0, 4.0, 1.0, 'colher de sopa cheia'),
        ('Beterraba cozida', 'Vegetais', 38.0, 17.0, 1.0, 'colher de servir cheia'),
        ('Brócolis cozido (picado)', 'Vegetais', 15.0, 4.0, 1.0, 'colher de sopa cheia'),
        ('Melão', 'Frutas', 70.0, 17.0, 1.0, 'fatia pequena'),
        ('Melancia', 'Frutas', 100.0, 29.0, 1.0, 'fatia pequena'),
        ('Morango', 'Frutas', 12.0, 4.0, 1.0, 'unidade média'),
        ('Abacaxi', 'Frutas', 75.0, 37.0, 1.0, 'fatia média'),
        ('Kiwi', 'Frutas', 76.0, 44.0, 1.0, 'unidade média'),
        ('Uva', 'Frutas', 350.0, 196.0, 1.0, 'cacho médio'),
        ('Ovos de galinha, cozidos', 'Proteínas', 50.0, 63.0, 1.0, 'unidade média'),
        ('Frango grelhado (peito)', 'Proteínas', 100.0, 150.0, 1.0, 'filé médio'),
        ('Patinho bovino, grelhado/moído', 'Proteínas', 110.0, 231.0, 1.0, 'filé médio'),
        ('Tilápia cozida', 'Proteínas', 55.0, 59.0, 1.0, 'filé médio'),
        ('Whey Protein Concentrado (pó)', 'Proteínas', 30.0, 114.0, 1.0, 'scoop'),
        ('Iogurte desnatado (Zero)', 'Laticínios', 200.0, 127.0, 1.0, 'copo (200ml)'),
        ('Requeijão cremoso light', 'Laticínios', 30.0, 54.0, 1.0, 'colher de sopa cheia'),
        ('Margarina com sal', 'Gorduras', 8.0, 43.0, 1.0, 'colher de chá cheia'),
        ('Azeite de oliva extra virgem', 'Gorduras', 12.0, 71.0, 1.0, 'colher de sopa'),
        ('Pasta de Amendoim integral', 'Gorduras', 15.0, 93.0, 1.0, 'colher de sopa'),
        ('Castanha do Pará', 'Gorduras', 4.0, 27.0, 1.0, 'unidade'),
        ('Doce de leite pastoso', 'Açúcares', 20.0, 64.0, 1.0, 'colher de sopa'),
        ('Chocolate ao leite', 'Açúcares', 30.0, 161.0, 1.0, 'barra pequena')
    ]

    food_values_to_insert = []
    for food_item in foods_data_tuples:
        name, food_group_name_val, default_grams_val, energy_kcal_val, unit_measure_val, portion_val = food_item
        decimal_default_grams = decimal.Decimal(str(default_grams_val)) if default_grams_val is not None else None
        decimal_energy_kcal = decimal.Decimal(str(energy_kcal_val)) if energy_kcal_val is not None else None
        decimal_unit_measure = decimal.Decimal(str(unit_measure_val)) if unit_measure_val is not None else None
        
        food_values_to_insert.append(
            (name, food_group_name_val, decimal_default_grams, decimal_energy_kcal, decimal_unit_measure, portion_val)
        )

    sql_insert_foods = """
    INSERT IGNORE INTO tb_foods (name, food_group_name, default_portion_grams, energy_value_kcal, portion, unit_measure) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor = cnxn.cursor()

        if food_values_to_insert:
            try:
                print(
                    f"Tentando inserir/ignorar {len(food_values_to_insert)} registros em tb_foods...")
                cursor.executemany(sql_insert_foods, food_values_to_insert)
                print(f"Processamento de tb_foods concluído.")
            except pymysql.MySQLError as e:
                print(
                    f"Erro ao inserir dados em tb_foods com executemany: {e}")

        print("Dados iniciais para tb_foods verificados/inseridos com sucesso.")

    except pymysql.MySQLError as e:
        print(f"Erro geral ao inserir dados iniciais: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


def setup_database():
    print("Iniciando configuração do banco de dados...")
    connection = connect_database()
    if connection:
        create_tables(connection)
        insert_initial_data(connection)
        if connection.open:
            connection.close()
            print("Conexão com o banco de dados fechada.")
        print("Configuração do banco de dados concluída.")
    else:
        print("Não foi possível configurar o banco de dados devido a falha na conexão inicial.")


if __name__ == "__main__":
    
    setup_database()
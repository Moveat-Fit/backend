import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def connect_database():
    try:
        cnxn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
        )
        print("Conexão estabelecida")
        return cnxn
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def create_tables(cnxn):
    if cnxn is None:
        print("Não foi possível criar as tabelas, pois a conexão falhou.")
        return

    sql_commands = [
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
            CONSTRAINT chk_full_name_prof CHECK (CHAR_LENGTH(TRIM(full_name)) > 0),
            CONSTRAINT chk_email_prof CHECK (CHAR_LENGTH(TRIM(email)) > 0),
            CONSTRAINT chk_password_prof CHECK (CHAR_LENGTH(TRIM(password)) > 0),
            CONSTRAINT chk_phone_prof CHECK (CHAR_LENGTH(TRIM(phone)) > 0),
            CONSTRAINT chk_reg_council_type_prof CHECK (CHAR_LENGTH(TRIM(regional_council_type)) > 0),
            CONSTRAINT chk_reg_council_prof CHECK (CHAR_LENGTH(TRIM(regional_council)) > 0)
        )
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
            FOREIGN KEY (professional_id) REFERENCES tb_professionals(id),
            CONSTRAINT chk_full_name_patient CHECK (CHAR_LENGTH(TRIM(full_name)) > 0),
            CONSTRAINT chk_email_patient CHECK (CHAR_LENGTH(TRIM(email)) > 0),
            CONSTRAINT chk_password_patient CHECK (CHAR_LENGTH(TRIM(password)) > 0),
            CONSTRAINT chk_phone_patient CHECK (CHAR_LENGTH(TRIM(phone)) > 0)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_food_groups (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_foods (
            id INT AUTO_INCREMENT PRIMARY KEY,
            food_group_id INT,
            name VARCHAR(255) NOT NULL,
            default_portion VARCHAR(100),
            FOREIGN KEY (food_group_id) REFERENCES tb_food_groups(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_meal_types (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_patient_meal_plans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE,
            FOREIGN KEY (patient_id) REFERENCES tb_patients(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_meal_plan_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            meal_plan_id INT NOT NULL,
            meal_type_id INT NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY (meal_plan_id) REFERENCES tb_patient_meal_plans(id),
            FOREIGN KEY (meal_type_id) REFERENCES tb_meal_types(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_meal_plan_foods (
            meal_plan_entry_id INT NOT NULL,
            food_id INT NOT NULL,
            portion VARCHAR(100),
            PRIMARY KEY (meal_plan_entry_id, food_id),
            FOREIGN KEY (meal_plan_entry_id) REFERENCES tb_meal_plan_entries(id),
            FOREIGN KEY (food_id) REFERENCES tb_foods(id)
        )
        """
    ]

    try:
        cursor = cnxn.cursor()
        for sql in sql_commands:
            cursor.execute(sql)
        cnxn.commit()
        print("Tabelas criadas com sucesso.")
    except mysql.connector.Error as e:
        print(f"Erro ao criar as tabelas: {e}")
    finally:
        cursor.close()

def insert_initial_data(cnxn):
    if cnxn is None:
        print("Não foi possível inserir os dados iniciais, pois a conexão falhou.")
        return

    insert_commands = [
        """
        INSERT INTO tb_food_groups (name) VALUES 
        ('Cereais'),
        ('Proteínas'),
        ('Frutas'),
        ('Vegetais'),
        ('Laticínios')
        """,
        """
        INSERT INTO tb_foods (food_group_id, name, default_portion) VALUES 
        (1, 'Arroz', '100g'),
        (1, 'Feijão', '80g'),
        (2, 'Frango grelhado', '150g'),
        (3, 'Maçã', '1 unidade'),
        (3, 'Banana', '1 unidade'),
        (4, 'Alface', '50g'),
        (4, 'Cenoura', '80g'),
        (5, 'Leite', '200ml'),
        (5, 'Queijo', '30g')
        """,
        """
        INSERT INTO tb_meal_types (name) VALUES 
        ('Café da manhã'),
        ('Almoço'),
        ('Jantar'),
        ('Lanche')
        """
    ]

    try:
        cursor = cnxn.cursor()
        for sql in insert_commands:
            cursor.execute(sql)
        cnxn.commit()
        print("Dados iniciais inseridos com sucesso.")
    except mysql.connector.Error as e:
        print(f"Erro ao inserir dados iniciais: {e}")
    finally:
        cursor.close()

def setup_database():
    connection = connect_database()
    if connection:
        create_tables(connection)
        insert_initial_data(connection)
        connection.close()
    else:
        print("Não foi possível configurar o banco de dados devido a falha na conexão.")

# Executar a configuração do banco de dados
setup_database()

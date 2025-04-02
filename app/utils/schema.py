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
        print("Erro ao conectar ao MySQL:", e)
        return None


def create_tables(cnxn):
    if cnxn is None:
        print("Não foi possível criar as tabelas, pois a conexão falhou.")
        return

    sql_commands = [
        """
        CREATE TABLE IF NOT EXISTS TB_PROFESSIONALS (
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
        CREATE TABLE IF NOT EXISTS TB_PATIENTS (
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
        FOREIGN KEY (professional_id) REFERENCES TB_PROFESSIONALS(id),
        CONSTRAINT chk_full_name_patient CHECK (CHAR_LENGTH(TRIM(full_name)) > 0),
        CONSTRAINT chk_email_patient CHECK (CHAR_LENGTH(TRIM(email)) > 0),
        CONSTRAINT chk_password_patient CHECK (CHAR_LENGTH(TRIM(password)) > 0),
        CONSTRAINT chk_phone_patient CHECK (CHAR_LENGTH(TRIM(phone)) > 0)
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
        print("Erro ao criar tabelas:", e)
    finally:
        cursor.close()
        cnxn.close()




connection = connect_database()
create_tables(connection)
import mysql.connector


def connect_database():
    try:
        cnxn = mysql.connector.connect(
            host="localhost",
            database="db_moveat",
            user="root",
            password="ymw2yWp*"
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
        CREATE TABLE tb_Users (
            UserID INT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(100) NOT NULL,
            Email VARCHAR(100) UNIQUE NOT NULL,
            Password VARCHAR(255) NOT NULL,
            CPF VARCHAR(11) UNIQUE,
            CellPhone VARCHAR(15) UNIQUE,
            CRN VARCHAR(10) UNIQUE NULL,
            CREF VARCHAR(10) UNIQUE NULL,
            UserType VARCHAR(50),
            CreatedAt DATETIME DEFAULT NOW(),
            CHECK (UserType IN ('Nutricionista', 'Personal Trainer', 'Paciente'))
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

import pyodbc

def create_database():
    try:
        # Conectar ao servidor sem especificar um banco de dados
        cnxn = pyodbc.connect(
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=BRASLBRJ0108KD5;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        cnxn.autocommit = True

        # Criar um novo cursor
        cursor = cnxn.cursor()

        # Executar o comando para criar o banco de dados
        cursor.execute('CREATE DATABASE db_MoveEat_teste_teste')
        print("Banco de dados 'db_MoveEat_teste_teste' criado com sucesso.")

        # Fechar o cursor e a conexão
        cursor.close()
        cnxn.close()

    except Exception as e:
        print("Erro ao criar o banco de dados:", str(e))

# Chamar a função para criar o banco de dados
create_database()



def connect_to_database():
    try:
        cnxn = pyodbc.connect(
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=BRASLBRJ0108KD5;"
            "Database=db_MoveEat_teste_teste;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    except pyodbc.Error as e:
        print("Erro ao conectar ao SQL Server:", e)
        return None
    else:
        print("Conexão estabelecida com sucesso.")
        return cnxn

# Chamada da função
connection = connect_to_database()

def create_tables(cnxn):
    sql_commands = [
        """
        CREATE TABLE tb_Users (
            UserID INT PRIMARY KEY IDENTITY,
            Name NVARCHAR(100),
            Email NVARCHAR(100) UNIQUE,
            Password NVARCHAR(100),
            UserType NVARCHAR(50),  -- 'patient' or 'professional'
            DateTime DATETIME DEFAULT GETDATE()
        );
        """,
        """
        CREATE TABLE tb_PatientProfile (
            PatientID INT PRIMARY KEY IDENTITY,
            UserID INT FOREIGN KEY REFERENCES tb_Users(UserID),
            BirthDate DATETIME,
            Gender NVARCHAR(50),
            Height INT,
            CurrentWeight INT
        );
        """,
        """
        CREATE TABLE tb_ProfessionalProfile (
            ProfessionalID INT PRIMARY KEY IDENTITY,
            UserID INT FOREIGN KEY REFERENCES tb_Users(UserID),
            Specialty NVARCHAR(100),
            ProfessionalRegistration NVARCHAR(100),
            Description NVARCHAR(255),
            YearsExperience INT
        );
        """
    ]
    cursor = cnxn.cursor()
    for sql in sql_commands:
        cursor.execute(sql)
    cnxn.commit()
    print("Tabelas criadas com sucesso.")

# Chamada da função
connection = connect_to_database()
if connection:
    create_tables(connection)
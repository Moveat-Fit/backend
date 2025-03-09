import pyodbc

def connect_database():
    try:
        cnxn = pyodbc.connect(
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=database-moveat.c70ksemu8pdk.us-east-2.rds.amazonaws.com;"
            "Database=db_Moveat;"
            "UID=admin_moveat;"  
            "PWD=Pescarolepedro2!;"  
            "TrustServerCertificate=yes;"
        )
        print("Conexão estabelecida")
        return cnxn
    except pyodbc.Error as e:
        print("Erro ao conectar ao SQL Server:", e)
        return None

def create_tables(cnxn):
    if cnxn is None:
        print("Não foi possível criar as tabelas, pois a conexão falhou.")
        return
    
    sql_commands = [
        """
        CREATE TABLE tb_Users (
            UserID INT PRIMARY KEY IDENTITY(1,1),
            Name NVARCHAR(100) NOT NULL,
            Email NVARCHAR(100) UNIQUE NOT NULL,
            Password NVARCHAR(255) NOT NULL,
            CPF VARCHAR(11) UNIQUE,
            CellPhone VARCHAR(15) UNIQUE,
            CRN VARCHAR(10) UNIQUE NULL,
            CREF VARCHAR(10) UNIQUE NULL,
            UserType NVARCHAR(50) CHECK (UserType IN ('Nutricionista', 'Personal Trainer', 'Paciente')),
            CreatedAt DATETIME DEFAULT GETDATE()
        )
        """
    ]
    
    try:
        cursor = cnxn.cursor()
        for sql in sql_commands:
            cursor.execute(sql)
        cnxn.commit()
        print("Tabelas criadas com sucesso.")
    except pyodbc.Error as e:
        print("Erro ao criar tabelas:", e)
    finally:
        cursor.close()
        cnxn.close()

# Conectar ao banco e criar as tabelas
connection = connect_database()
create_tables(connection)

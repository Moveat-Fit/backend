import pyodbc
def connect_to_database():
    try:
        cnxn = pyodbc.connect(
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=BRASLBRJ0108KD5;"
            "Database=db_MoveEat;"
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



















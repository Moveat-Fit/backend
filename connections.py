import pyodbc


def connect_database():
    try:
        cnxn = pyodbc.connect(
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=database-moveat.c70ksemu8pdk.us-east-2.rds.amazonaws.com;"
            "UID=admin_moveat;"  # Username
            "PWD=Pescarolepedro2!;"  # Password
            "TrustServerCertificate=yes;"
        )
    except pyodbc.Error as e:
        print("Erro ao conectar ao SQL Server:", e)
        return None
    else:
        print("Conexão estabelecida")
    return cnxn


connection = connect_database()
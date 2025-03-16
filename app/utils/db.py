import mysql.connector

def connect_database():
    try:
        cnxn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ymw2yWp*",
            database="db_moveat"
        )
        print("Conexão estabelecida com MySQL.")
        return cnxn
    except mysql.connector.Error as e:
        print("Erro ao conectar ao MySQL", e)
        return None

connection = connect_database()
if connection:
    print("Banco de dados conectado com sucesso!")
else:
    print("Falha na conexão com o banco.")
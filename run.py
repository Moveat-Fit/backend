from app import create_app
from app.utils.schema import connect_database, create_tables

app = create_app()

# Função para inicializar o banco de dados
def initialize_database():
    connection = connect_database()
    if connection:
        create_tables(connection)

if __name__ == "__main__":
    # Inicializa o banco de dados antes de iniciar o app
    initialize_database()
    app.run(debug=True)
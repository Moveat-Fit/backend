from app import create_app
from app.utils.schema import setup_database

app = create_app()

if __name__ == "__main__":
    setup_database()  # cria as tabelas e insere os dados iniciais
    app.run(debug=True)
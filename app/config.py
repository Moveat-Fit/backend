import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_default_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Definindo a validade do token para 1 hora
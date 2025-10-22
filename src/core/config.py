import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# chave de API do Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente 'GOOGLE_API_KEY' não foi definida. "
                     "Por favor, crie um arquivo .env e adicione-a.")
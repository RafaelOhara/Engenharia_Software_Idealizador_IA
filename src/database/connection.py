# import sqlite3
# import os

# # Define o caminho do banco de dados (relativo a este arquivo)
# DB_FILE_PATH = os.path.join(
#     os.path.dirname(__file__), '..', '..', 'data', 'plataforma_inovacao.db'
# )

# def get_db_connection():
#     """
#     Cria e retorna uma conexão com o banco de dados SQLite.
#     A conexão é configurada para retornar linhas como dicionários.
#     """
#     try:
#         # Verifica se o arquivo do banco de dados existe
#         if not os.path.exists(DB_FILE_PATH):
#             raise FileNotFoundError(f"Arquivo do banco de dados não encontrado em: {DB_FILE_PATH}")
            
#         conn = sqlite3.connect(DB_FILE_PATH)
        
#         # Faz a conexão retornar dicionários (ex: {'id': 1, 'nome': 'Teste'})
#         # em vez de tuplas (ex: (1, 'Teste')). Isso é MUITO útil.
#         conn.row_factory = sqlite3.Row 
        
#         # Habilita o suporte a chaves estrangeiras
#         conn.execute("PRAGMA foreign_keys = ON;")
        
#         return conn
        
#     except sqlite3.Error as e:
#         print(f"Erro ao conectar ao banco de dados: {e}")
#         return None
#     except FileNotFoundError as e:
#         print(e)
#         print("Por favor, execute o script 'scripts/create_database.py' e 'scripts/populate_database.py' primeiro.")
#         return None
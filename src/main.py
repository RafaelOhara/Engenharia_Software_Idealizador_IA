from fastapi import FastAPI
from src.api.routes import router as api_router # Importa o roteador
from fastapi.middleware.cors import CORSMiddleware # <<< 1. IMPORTE ISSO

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="Microsserviço de Sugestão de Talentos com IA",
    description="Um microsserviço que analisa projetos e sugere perfis de colaboradores faltantes, "
                  "conforme especificado no projeto da Universidade Presbiteriana Mackenzie.",
    version="1.0.0"
)

# ======================================================================
# <<< 2. ADICIONE ESTE BLOCO DE CÓDIGO (MIDDLEWARE DE CORS)
# ======================================================================

# Define quais "origens" (sites) podem fazer requisições para esta API.
origins = [
    # Para testes locais, permita tudo:
    "*", 
    
    # === QUANDO FOR PARA PRODUÇÃO, SEJA MAIS RESTRITO ===
    # "http://localhost",
    # "http://localhost:5500", # Exemplo se você usa Live Server
    # "http://127.0.0.1:5500",
    # "https://seu-site-de-frontend.com", # O domínio do seu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Permite as origens da lista
    allow_credentials=True,    # Permite cookies (se usar)
    allow_methods=["*"],       # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],       # Permite todos os cabeçalhos
)
# ======================================================================


# Inclui as rotas definidas em 'src/api/routes.py'
# Adiciona um prefixo global /api/v1 para todas essas rotas
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    Endpoint raiz. Útil para verificar se o serviço está no ar.
    """
    return {"status": "Microsserviço de Sugestão de Talentos está no ar!"}

from fastapi import FastAPI
from src.api.routes import router as api_router # Importa o roteador

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="Microsserviço de Sugestão de Talentos com IA",
    description="Um microsserviço que analisa projetos e sugere perfis de colaboradores faltantes, "
                "conforme especificado no projeto da Universidade Presbiteriana Mackenzie.",
    version="1.0.0"
)

# Inclui as rotas definidas em 'src/api/routes.py'
# Adiciona um prefixo global /api/v1 para todas essas rotas
# (Ex: a URL final será /api/v1/projetos/1/sugestoes)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    Endpoint raiz. Útil para verificar se o serviço está no ar.
    """
    return {"status": "Microsserviço de Sugestão de Talentos está no ar!"}
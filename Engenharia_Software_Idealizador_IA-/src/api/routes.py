from fastapi import APIRouter, HTTPException
from src.logic.suggestion_logic import generate_suggestions_for_project

# Cria um "roteador". Você pode pensar nele como um mini-app
# que agrupa endpoints relacionados.
router = APIRouter()

@router.get("/projetos/{project_id}/sugestoes")
def get_project_suggestions(project_id: int):
    """
    Endpoint principal da API.
    Recebe um ID de projeto pela URL, chama a lógica de negócio
    e retorna as sugestões da IA.
    """
    
    # Chama a função "maestro" que você criou no passo anterior
    resultado, status_code = generate_suggestions_for_project(project_id)
    
    # Se a lógica de negócio retornar um erro (ex: 404, 500),
    # o FastAPI o transforma em uma resposta de erro HTTP clara.
    if status_code != 200:
        raise HTTPException(
            status_code=status_code, 
            detail=resultado.get("erro", "Ocorreu um erro interno no servidor.")
        )
    
    # Se tudo deu certo (status 200), retorna o JSON com as sugestões
    return resultado
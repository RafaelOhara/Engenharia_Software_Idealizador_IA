from fastapi import APIRouter, HTTPException
# Importar a lógica principal (não muda)
from src.logic.suggestion_logic import generate_suggestions_for_project
# NOVO: Importar o modelo Pydantic que criamos no repository
# O FastAPI vai usá-lo para validar o corpo da requisição
from src.database.repository import Projeto 

# Cria um "roteador". Você pode pensar nele como um mini-app
# que agrupa endpoints relacionados.
router = APIRouter()

# Método mudou de @router.get para @router.post
# A URL mudou de "/projetos/{project_id}/sugestoes" para "/projetos/sugestoes"
@router.post("/projetos/sugestoes")
def gerar_sugestoes_projeto(projeto_data: Projeto):
    """
    Endpoint principal da API.
    
    Recebe um JSON completo do projeto no CORPO (BODY) da requisição.
    O FastAPI valida automaticamente se o JSON bate com o modelo 'Projeto'.
    
    Chama a lógica de negócio e retorna as sugestões da IA.
    """
    
    # Agora chamamos a lógica passando o dicionário do objeto Pydantic
    # .model_dump() converte o objeto 'projeto_data' de volta para um dict,
    # que é o que a sua função 'generate_suggestions_for_project' espera.
    resultado, status_code = generate_suggestions_for_project(projeto_data.model_dump())
    
    # Esta parte da lógica de erro continua igual e é uma boa prática.
    # Se a lógica de negócio retornar um erro (ex: 400, 500),
    # o FastAPI o transforma em uma resposta de erro HTTP clara.
    if status_code != 200:
        raise HTTPException(
            status_code=status_code, 
            detail=resultado.get("erro", "Ocorreu um erro interno no servidor.")
        )
    
    # Se tudo deu certo (status 200), retorna o JSON com as sugestões
    return resultado

# --- CÓDIGO ANTIGO COMENTADO PARA REFERÊNCIA ---

# from fastapi import APIRouter, HTTPException
# from src.logic.suggestion_logic import generate_suggestions_for_project

# # Cria um "roteador". Você pode pensar nele como um mini-app
# # que agrupa endpoints relacionados.
# router = APIRouter()

# @router.get("/projetos/{project_id}/sugestoes")
# def get_project_suggestions(project_id: int):
#     """
#     Endpoint principal da API.
#     Recebe um ID de projeto pela URL, chama a lógica de negócio
#     e retorna as sugestões da IA.
#     """
    
#     # Chama a função "maestro" que você criou no passo anterior
#     resultado, status_code = generate_suggestions_for_project(project_id)
    
#     # Se a lógica de negócio retornar um erro (ex: 404, 500),
#     # o FastAPI o transforma em uma resposta de erro HTTP clara.
#     if status_code != 200:
#         raise HTTPException(
#             status_code=status_code, 
#             detail=resultado.get("erro", "Ocorreu um erro interno no servidor.")
#         )
    
#     # Se tudo deu certo (status 200), retorna o JSON com as sugestões
#     return resultado
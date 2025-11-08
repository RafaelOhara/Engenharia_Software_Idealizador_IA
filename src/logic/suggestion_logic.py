from src.database import repository
from src.services import ia_service

# Importa os modelos Pydantic para validação
from src.database.repository import Projeto
from pydantic import ValidationError
from typing import Dict, Any, Tuple

def generate_suggestions_for_project(json_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """
    1. Valida o JSON recebido usando o modelo Pydantic.
    2. Extrai os dados do objeto validado (usando as novas funções do repository).
    3. Envia os dados para a IA.
    4. Retorna o resultado.
    """
    
    # --- 1. Validar o JSON de entrada ---
    try:
        projeto_validado = Projeto(**json_data)
    except ValidationError as e:
        # Se o JSON for inválido (faltando campos, tipos errados)
        return {"erro": "JSON de entrada inválido", "detalhes": e.errors()}, 400
        
    # --- 2. Extrair dados (usando as novas funções do repository) ---
    project_details = repository.get_project_details(projeto_validado)
    team_competencies = repository.get_team_competencies(projeto_validado)
    
    descricao_projeto = project_details['descricao_projeto']

    # --- 3. Chamar o serviço de IA (esta chamada não mudou) ---
    sugestoes_ia = ia_service.get_ia_suggestions(
        descricao_projeto=descricao_projeto,
        competencias_atuais=team_competencies
    )

    # --- 4. Retornar o resultado ---
    if "erro" in sugestoes_ia:
        return {"erro": f"Falha ao gerar sugestões de IA: {sugestoes_ia['erro']}"}, 500

    response_data = {
        "id_projeto": projeto_validado.id_projeto,
        "descricao_projeto": project_details['descricao_projeto'],
        "categoria_projeto": project_details['categoria_projeto']
    }
    
    response_data.update(sugestoes_ia)
    
    return response_data, 200


#Bloco de teste
if __name__ == "__main__":
    print("--- Testando suggestion_logic (Modo JSON) ---")
    
    json_recebido_teste = {
      "id_projeto": 1,
      "descricao_projeto": "Um app para organizar equipes de engenharia.",
      "categoria_projeto": "Engenharia",
      "participantes": [
        {"collaborator_email": "ana@email.com", "contributed_skill_name": "React", "contributed_skill_level": 3},
        {"collaborator_email": "ana@email.com", "contributed_skill_name": "Figma", "contributed_skill_level": 2},
        {"collaborator_email": "bruno@email.com", "contributed_skill_name": "Docker", "contributed_skill_level": 2}
      ]
    }
    
    print(f"Gerando sugestões para o Projeto ID: {json_recebido_teste['id_projeto']} (Aguarde...)")
    
    resultado, status_code = generate_suggestions_for_project(json_recebido_teste)
    
    print(f"\nStatus da Resposta: {status_code}")
    print("--- Resultado ---")
    
    if status_code == 200:
        import json
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        print(resultado)

# codigo comentado antigo para referência
# from src.database import repository
# from src.services import ia_service

# def generate_suggestions_for_project(project_id: int):
#     """
#     1. Busca os dados do projeto no banco de dados.
#     2. Busca as competências da equipe atual no banco.
#     3. Envia os dados para a IA.
#     4. Retorna o resultado.
#     """
    
#     #Buscar dados do projeto ---
#     project_details = repository.get_project_details(project_id)
    
#     if not project_details:
#         # Se o projeto não existe, retorna um erro claro
#         return {"erro": f"Projeto com ID {project_id} não encontrado."}, 404
        
#     #Buscar competências da equipe ---
#     team_competencies = repository.get_team_competencies(project_id)
    
#     # Extrai a descrição do projeto
#     descricao_projeto = project_details['descricao_projeto']

#     #Chamar o serviço de IA ---
#     sugestoes_ia = ia_service.get_ia_suggestions(
#         descricao_projeto=descricao_projeto,
#         competencias_atuais=team_competencies
#     )

#     #Retornar o resultado
#     if "erro" in sugestoes_ia:
#         # Repassa um erro se a API da IA falhar
#         return {"erro": f"Falha ao gerar sugestões de IA: {sugestoes_ia['erro']}"}, 500
#     # Cria a base da resposta com os detalhes do projeto que já buscamos
#     response_data = {
#         "id_projeto": project_id,
#         "descricao_projeto": project_details['descricao_projeto'],
#         "categoria_projeto": project_details['categoria_projeto']
#     }
    
#     # Adiciona as sugestões da IA (que é um dict {'sugestoes': [...]})
#     # ao nosso dicionário de resposta.
#     response_data.update(sugestoes_ia)
    
#     # Se tudo deu certo, retorna o dicionário completo
#     return response_data, 200


# #Bloco de teste
# if __name__ == "__main__":
#     print("--- Testando suggestion_logic ---")
    
#     # Vamos testar com o Projeto 1 (App de Músicos)
#     # Este projeto tem 2 membros e 5 competências
#     projeto_id_teste = 1
    
#     print(f"Gerando sugestões para o Projeto ID: {projeto_id_teste} (Aguarde...)")
    
#     # Chama a função principal
#     resultado, status_code = generate_suggestions_for_project(projeto_id_teste)
    
#     print(f"\nStatus da Resposta: {status_code}")
#     print("--- Resultado ---")
    
#     if status_code == 200:
#         import json
#         print(json.dumps(resultado, indent=2, ensure_ascii=False))
#     else:
#         print(resultado)
        
#     # Teste de um projeto que não existe
#     print("\n--- Testando projeto inexistente ---")
#     projeto_id_teste_erro = 9999
#     resultado_erro, status_code_erro = generate_suggestions_for_project(projeto_id_teste_erro)
#     print(f"Status da Resposta: {status_code_erro}")
#     print(f"Resultado: {resultado_erro}")
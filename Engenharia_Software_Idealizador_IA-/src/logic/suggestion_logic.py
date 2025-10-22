from src.database import repository
from src.services import ia_service

def generate_suggestions_for_project(project_id: int):
    """
    1. Busca os dados do projeto no banco de dados.
    2. Busca as competências da equipe atual no banco.
    3. Envia os dados para a IA.
    4. Retorna o resultado.
    """
    
    #Buscar dados do projeto ---
    project_details = repository.get_project_details(project_id)
    
    if not project_details:
        # Se o projeto não existe, retorna um erro claro
        return {"erro": f"Projeto com ID {project_id} não encontrado."}, 404
        
    #Buscar competências da equipe ---
    team_competencies = repository.get_team_competencies(project_id)
    
    # Extrai a descrição do projeto
    descricao_projeto = project_details['descricao_projeto']

    #Chamar o serviço de IA ---
    sugestoes_ia = ia_service.get_ia_suggestions(
        descricao_projeto=descricao_projeto,
        competencias_atuais=team_competencies
    )

    #Retornar o resultado
    if "erro" in sugestoes_ia:
        # Repassa um erro se a API da IA falhar
        return {"erro": f"Falha ao gerar sugestões de IA: {sugestoes_ia['erro']}"}, 500

    # Se tudo deu certo, retorna as sugestões da IA
    return sugestoes_ia, 200


#Bloco de teste
if __name__ == "__main__":
    print("--- Testando suggestion_logic ---")
    
    # Vamos testar com o Projeto 1 (App de Músicos)
    # Este projeto tem 2 membros e 5 competências
    projeto_id_teste = 1
    
    print(f"Gerando sugestões para o Projeto ID: {projeto_id_teste} (Aguarde...)")
    
    # Chama a função principal
    resultado, status_code = generate_suggestions_for_project(projeto_id_teste)
    
    print(f"\nStatus da Resposta: {status_code}")
    print("--- Resultado ---")
    
    if status_code == 200:
        import json
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        print(resultado)
        
    # Teste de um projeto que não existe
    print("\n--- Testando projeto inexistente ---")
    projeto_id_teste_erro = 9999
    resultado_erro, status_code_erro = generate_suggestions_for_project(projeto_id_teste_erro)
    print(f"Status da Resposta: {status_code_erro}")
    print(f"Resultado: {resultado_erro}")
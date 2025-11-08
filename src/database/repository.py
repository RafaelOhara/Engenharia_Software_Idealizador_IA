# Removido: import sqlite3
# Removido: from .connection import get_db_connection
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Set

# --- 1. Modelos Pydantic para validar o JSON recebido ---

class ParticipacaoHabilidade(BaseModel):
    """
    Representa um item individual na lista 'participantes' do JSON.
    """
    collaborator_email: EmailStr
    contributed_skill_name: str
    contributed_skill_level: int

class Projeto(BaseModel):
    """
    Representa o objeto JSON principal que seu microsserviço recebe.
    """
    id_projeto: int
    descricao_projeto: str
    categoria_projeto: str
    participantes: List[ParticipacaoHabilidade]

# --- 2. Funções Refatoradas (Agora recebem o objeto do projeto) ---

def get_project_details(projeto_objeto: Projeto) -> Dict[str, Any]:
    """
    Extrai os detalhes de um objeto de projeto já validado.
    (Substitui a query "SELECT ... FROM Projetos")
    """
    return {
        "descricao_projeto": projeto_objeto.descricao_projeto,
        "categoria_projeto": projeto_objeto.categoria_projeto
    }

def get_team_competencies(projeto_objeto: Projeto) -> List[str]:
    """
    Extrai a lista de competências únicas dos participantes.
    (Substitui a query SQL com JOINs e DISTINCT)
    """
    if not projeto_objeto.participantes:
        return []

    # Um "set" automaticamente ignora duplicatas (fazendo o papel do "SELECT DISTINCT")
    competencias_unicas: Set[str] = set()
    
    for participacao in projeto_objeto.participantes:
        competencias_unicas.add(participacao.contributed_skill_name)
        
    return list(competencias_unicas)

# --- 3. Bloco de teste (Simulando o recebimento do JSON) ---
if __name__ == "__main__":
    print("--- Testando Repositório (Modo JSON) ---")

    json_recebido = {
      "id_projeto": 1,
      "descricao_projeto": "Um app para organizar equipes.",
      "categoria_projeto": "Engenharia",
      "participantes": [
        {"collaborator_email": "ana@email.com", "contributed_skill_name": "React", "contributed_skill_level": 3},
        {"collaborator_email": "ana@email.com", "contributed_skill_name": "Figma", "contributed_skill_level": 2},
        {"collaborator_email": "bruno@email.com", "contributed_skill_name": "Docker", "contributed_skill_level": 2}
      ]
    }
    
    try:
        projeto_validado = Projeto(**json_recebido)

        print(f"\nBuscando detalhes do Projeto {projeto_validado.id_projeto}...")
        detalhes = get_project_details(projeto_validado)
        print(f"  Descrição: {detalhes['descricao_projeto']}")
            
        print(f"\nBuscando competências da equipe do Projeto {projeto_validado.id_projeto}...")
        competencias = get_team_competencies(projeto_validado)
        print(f"  Competências encontradas: {competencias}")
            
    except Exception as e:
        print(f"Erro de validação do JSON: {e}")
        
# --- Código Original (Comentado para referência) ---
# import sqlite3
# from .connection import get_db_connection

# def get_project_details(project_id: int):
#     """
#     Busca os detalhes de um projeto específico pelo ID.
#     """
#     conn = get_db_connection()
#     if conn is None:
#         return None
        
#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT descricao_projeto, categoria_projeto FROM Projetos WHERE id_projeto = ?",
#             (project_id,)
#         )
#         projeto = cursor.fetchone() # apenas 1 resultado
        
#         if projeto:
#             return dict(projeto) # Converte objeto para dicionário
#         else:
#             return None # Projeto não encontrado
            
#     except sqlite3.Error as e:
#         print(f"Erro ao buscar projeto: {e}")
#         return None
#     finally:
#         conn.close()

# def get_team_competencies(project_id: int):
#     """
#     Busca a lista de todas as competências únicas dos membros de um projeto.
#     Esta é a consulta-chave para a sua IA.
#     """
#     conn = get_db_connection()
#     if conn is None:
#         return []

#     try:
#         cursor = conn.cursor()
#         # 1. JUNTA Equipes com Usuario_Competencias pelo CPF do colaborador.
#         # 2. JUNTA o resultado com Competencias pelo ID da competência.
#         # 3. FILTRA pelo ID do projeto e status 'Aceito'.
#         # 4. Seleciona DISTINTAMENTE (sem repetição) o nome da competência.
#         query = """
#             SELECT DISTINCT c.nome_competencia
#             FROM Equipes AS e
#             JOIN Usuario_Competencias AS uc ON e.cpf_colaborador_fk = uc.cpf_usuario_fk
#             JOIN Competencias AS c ON uc.id_competencia_fk = c.id_competencia
#             WHERE e.id_projeto_fk = ? AND e.status_convite = 'Aceito';
#         """
        
#         cursor.execute(query, (project_id,))
        
#         # fetchall() retorna uma lista de Rows (ex: [{'nome_competencia': 'Python'}, ...])
#         competencias_rows = cursor.fetchall() 
        
#         # Converte a lista de Rows em uma lista simples de strings
#         lista_de_competencias = [row['nome_competencia'] for row in competencias_rows]
        
#         return lista_de_competencias
            
#     except sqlite3.Error as e:
#         print(f"Erro ao buscar competências da equipe: {e}")
#         return []
#     finally:
#         conn.close()

# # --- Bloco de teste (para verificar se está funcionando) ---
# if __name__ == "__main__":
#     print("--- Testando Repositório ---")
    
#     # teste com o Projeto 1
#     projeto_id_teste = 1
    
#     print(f"\nBuscando detalhes do Projeto {projeto_id_teste}...")
#     detalhes = get_project_details(projeto_id_teste)
#     if detalhes:
#         print(f"  Descrição: {detalhes['descricao_projeto'][:50]}...")
#         print(f"  Categoria: {detalhes['categoria_projeto']}")
#     else:
#         print("  Projeto não encontrado.")
        
#     print(f"\nBuscando competências da equipe do Projeto {projeto_id_teste}...")
#     competencias = get_team_competencies(projeto_id_teste)
#     if competencias:
#         print(f"  Competências encontradas ({len(competencias)}):")
#         for comp in competencias:
#             print(f"    - {comp}")
#     else:
#         print("  Nenhuma competência encontrada para a equipe deste projeto.")


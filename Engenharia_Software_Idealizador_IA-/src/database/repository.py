import sqlite3
from .connection import get_db_connection

def get_project_details(project_id: int):
    """
    Busca os detalhes de um projeto específico pelo ID.
    """
    conn = get_db_connection()
    if conn is None:
        return None
        
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT descricao_projeto, categoria_projeto FROM Projetos WHERE id_projeto = ?",
            (project_id,)
        )
        projeto = cursor.fetchone() # apenas 1 resultado
        
        if projeto:
            return dict(projeto) # Converte objeto para dicionário
        else:
            return None # Projeto não encontrado
            
    except sqlite3.Error as e:
        print(f"Erro ao buscar projeto: {e}")
        return None
    finally:
        conn.close()

def get_team_competencies(project_id: int):
    """
    Busca a lista de todas as competências únicas dos membros de um projeto.
    Esta é a consulta-chave para a sua IA.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        # 1. JUNTA Equipes com Usuario_Competencias pelo CPF do colaborador.
        # 2. JUNTA o resultado com Competencias pelo ID da competência.
        # 3. FILTRA pelo ID do projeto e status 'Aceito'.
        # 4. Seleciona DISTINTAMENTE (sem repetição) o nome da competência.
        query = """
            SELECT DISTINCT c.nome_competencia
            FROM Equipes AS e
            JOIN Usuario_Competencias AS uc ON e.cpf_colaborador_fk = uc.cpf_usuario_fk
            JOIN Competencias AS c ON uc.id_competencia_fk = c.id_competencia
            WHERE e.id_projeto_fk = ? AND e.status_convite = 'Aceito';
        """
        
        cursor.execute(query, (project_id,))
        
        # fetchall() retorna uma lista de Rows (ex: [{'nome_competencia': 'Python'}, ...])
        competencias_rows = cursor.fetchall() 
        
        # Converte a lista de Rows em uma lista simples de strings
        lista_de_competencias = [row['nome_competencia'] for row in competencias_rows]
        
        return lista_de_competencias
            
    except sqlite3.Error as e:
        print(f"Erro ao buscar competências da equipe: {e}")
        return []
    finally:
        conn.close()

# --- Bloco de teste (para verificar se está funcionando) ---
if __name__ == "__main__":
    print("--- Testando Repositório ---")
    
    # teste com o Projeto 1
    projeto_id_teste = 1
    
    print(f"\nBuscando detalhes do Projeto {projeto_id_teste}...")
    detalhes = get_project_details(projeto_id_teste)
    if detalhes:
        print(f"  Descrição: {detalhes['descricao_projeto'][:50]}...")
        print(f"  Categoria: {detalhes['categoria_projeto']}")
    else:
        print("  Projeto não encontrado.")
        
    print(f"\nBuscando competências da equipe do Projeto {projeto_id_teste}...")
    competencias = get_team_competencies(projeto_id_teste)
    if competencias:
        print(f"  Competências encontradas ({len(competencias)}):")
        for comp in competencias:
            print(f"    - {comp}")
    else:
        print("  Nenhuma competência encontrada para a equipe deste projeto.")
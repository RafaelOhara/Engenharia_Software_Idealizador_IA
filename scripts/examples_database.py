import sqlite3
import os

# Define o caminho para o banco de dados (assumindo que está na 'data/')
DB_DIR = 'data'
DB_NAME = 'plataforma_inovacao.db'
DB_PATH = os.path.join(DB_DIR, DB_NAME)

def popular_banco_de_dados():
    """
    Popula o banco de dados com um conjunto expandido de dados de exemplo.
    Usa 'INSERT OR IGNORE' para não duplicar dados se for executado novamente.
    """
    
    # Garante que a pasta 'data' exista
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    try:
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()

        # Ativa o suporte a chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON;")

        # --- 1. Inserir Usuarios (Expandido) ---
        lista_usuarios = [
            # Originais
            ('11111111111', 'Ana Silva', 'ana.silva@email.com', 'hash123', 'Gerente de Produto com 5 anos de experiência.', 'github.com/ana', 'Idealizador'),
            ('22222222222', 'Bruno Costa', 'bruno.costa@email.com', 'hash123', 'Dev Backend especialista em Python e Node.js.', 'github.com/bruno', 'Colaborador'),
            ('33333333333', 'Carla Dias', 'carla.dias@email.com', 'hash123', 'Designer UX/UI focada em apps mobile.', 'behance.net/carla', 'Colaborador'),
            ('44444444444', 'Diego Fernandes', 'diego.f@email.com', 'hash123', 'Desenvolvedor Mobile com experiência em Flutter.', 'github.com/diego', 'Colaborador'),
            ('99999999999', 'Admin Mackenzie', 'admin@mackenzie.br', 'hash_admin', 'Conta de administração da plataforma.', None, 'Admin'),
            
            # Novos Usuários
            ('55555555555', 'Eduardo Moreira', 'eduardo.m@email.com', 'hash123', 'Engenheiro de Dados Pleno.', 'github.com/eduardo', 'Colaborador'),
            ('66666666666', 'Fabia Lima', 'fabia.lima@email.com', 'hash123', 'Especialista em Marketing Digital e SEO.', 'linkedin.com/fabia', 'Colaborador'),
            ('77777777777', 'Gabriel Santos', 'gabriel.s@email.com', 'hash123', 'Desenvolvedor Frontend com foco em Vue.js.', 'github.com/gabriel', 'Colaborador'),
            ('88888888888', 'Helena Oliveira', 'helena.o@email.com', 'hash123', 'Cientista de Dados com mestrado em IA.', 'github.com/helena', 'Colaborador'),
            ('12345678901', 'Lucas Mendes', 'lucas.m@email.com', 'hash123', 'Idealizador com background em finanças.', 'linkedin.com/lucas', 'Idealizador'),
            ('23456789012', 'Mariana Alves', 'mariana.a@email.com', 'hash123', 'Idealizadora, focada em projetos de impacto social.', 'linkedin.com/mariana', 'Idealizador'),
            ('34567890123', 'Pedro Rocha', 'pedro.r@email.com', 'hash123', 'Engenheiro de QA e automação de testes.', 'github.com/pedro', 'Colaborador'),
            ('45678901234', 'Sofia Costa', 'sofia.c@email.com', 'hash123', 'DevOps e especialista em nuvem AWS.', 'github.com/sofia', 'Colaborador'),
            ('56789012345', 'Thiago Pereira', 'thiago.p@email.com', 'hash123', 'Advogado especializado em startups e LGPD.', 'linkedin.com/thiago', 'Colaborador'),
            ('67890123456', 'Vanessa Gomes', 'vanessa.g@email.com', 'hash123', 'Scrum Master e especialista em metodologias ágeis.', 'linkedin.com/vanessa', 'Colaborador')
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO Usuarios 
                (cpf, nome_completo, email, senha_hash, resumo_profissional, link_portfolio, tipo_usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, lista_usuarios)
        print(f"Inseridos {cursor.rowcount} usuários (ou já existiam).")

        # --- 2. Inserir Competencias (Expandido) ---
        lista_competencias = [
            # Originais
            (1, 'Python', 'Habilidade'),
            (2, 'Node.js', 'Habilidade'),
            (3, 'Banco de Dados SQL', 'Habilidade'),
            (4, 'Design UX/UI', 'Habilidade'),
            (5, 'React', 'Habilidade'),
            (6, 'Flutter', 'Habilidade'),
            (7, 'Swift', 'Habilidade'),
            (8, 'Análise de Negócios', 'Habilidade'),
            
            # Novas Competências
            (9, 'Engenharia de Dados', 'Habilidade'),
            (10, 'Marketing Digital', 'Habilidade'),
            (11, 'SEO', 'Habilidade'),
            (12, 'Vue.js', 'Habilidade'),
            (13, 'Machine Learning', 'Habilidade'),
            (14, 'Inteligência Artificial', 'Habilidade'),
            (15, 'Finanças', 'Habilidade'),
            (16, 'Gestão de Projetos Sociais', 'Habilidade'),
            (17, 'Testes de Software', 'Habilidade'),
            (18, 'Automação de Testes', 'Habilidade'),
            (19, 'AWS', 'Habilidade'),
            (20, 'Docker', 'Habilidade'),
            (21, 'Direito Digital', 'Habilidade'),
            (22, 'LGPD', 'Habilidade'),
            (23, 'Scrum', 'Habilidade'),
            (24, 'Gestão Ágil', 'Habilidade')
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO Competencias
                (id_competencia, nome_competencia, tipo_competencia)
            VALUES (?, ?, ?)
        """, lista_competencias)
        print(f"Inseridas {cursor.rowcount} competências (ou já existiam).")

        # --- 3. Inserir Projetos (Expandido) ---
        lista_projetos = [
            # Originais
            (1, 'App de Músicos', 
             'Um aplicativo mobile para conectar músicos amadores para formarem bandas e marcarem ensaios.', 
             'Música/Tecnologia', '11111111111', 'Buscando Equipe'), # Idealizadora: Ana
            (2, 'Plataforma E-learning IA', 
             'Sistema web para ensino de programação com IA para correção de exercícios.',
             'Educação/IA', '11111111111', 'Em Andamento'), # Idealizadora: Ana
             
            # Novos Projetos
            (3, 'Fintech de Microcrédito',
             'Plataforma para facilitar microcrédito P2P para pequenos empreendedores.',
             'Finanças/Tecnologia', '12345678901', 'Buscando Equipe'), # Idealizador: Lucas
            (4, 'ONG Connect',
             'Marketplace para conectar voluntários a ONGs e projetos sociais.',
             'Social/Voluntariado', '23456789012', 'Buscando Equipe'), # Idealizadora: Mariana
            (5, 'Health Monitor Dashboard',
             'Dashboard de monitoramento de saúde para empresas usando dados de wearables.',
             'Saúde/Big Data', '11111111111', 'Buscando Equipe'), # Idealizadora: Ana
            (6, 'LegalTech LGPD',
             'Ferramenta SaaS para ajudar PMEs a se adequarem à LGPD.',
             'Direito/Tecnologia', '12345678901', 'Buscando Equipe') # Idealizador: Lucas
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO Projetos
                (id_projeto, nome_projeto, descricao_projeto, categoria_projeto, cpf_idealizador_fk, status_projeto)
            VALUES (?, ?, ?, ?, ?, ?)
        """, lista_projetos)
        print(f"Inseridos {cursor.rowcount} projetos (ou já existiam).")
        
        # --- 4. Associar Competencias aos Usuarios (Expandido) ---
        lista_user_comps = [
            # Ana (Idealizadora)
            ('11111111111', 8), ('11111111111', 24),
            # Bruno (Dev Backend)
            ('22222222222', 1), ('22222222222', 2), ('22222222222', 3),
            # Carla (Designer)
            ('33333333333', 4), ('33333333333', 5),
            # Diego (Dev Mobile)
            ('44444444444', 6), ('44444444444', 7),
            # Eduardo (Eng. Dados)
            ('55555555555', 9), ('55555555555', 1), ('55555555555', 13),
            # Fabia (Marketing)
            ('66666666666', 10), ('66666666666', 11),
            # Gabriel (Frontend)
            ('77777777777', 12), ('77777777777', 5),
            # Helena (Cientista Dados)
            ('88888888888', 13), ('88888888888', 14), ('88888888888', 1),
            # Lucas (Idealizador Fin)
            ('12345678901', 15), ('12345678901', 8),
            # Mariana (Idealizadora Social)
            ('23456789012', 16),
            # Pedro (QA)
            ('34567890123', 17), ('34567890123', 18),
            # Sofia (DevOps)
            ('45678901234', 19), ('45678901234', 20),
            # Thiago (Advogado)
            ('56789012345', 21), ('56789012345', 22),
            # Vanessa (Scrum Master)
            ('67890123456', 23), ('67890123456', 24)
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO Usuario_Competencias
                (cpf_usuario_fk, id_competencia_fk)
            VALUES (?, ?)
        """, lista_user_comps)
        print(f"Inseridas {cursor.rowcount} associações usuário-competência (ou já existiam).")

        # --- 5. Montar Equipes (Expandido) ---
        lista_equipes = [
            # Projeto 1 (App de Músicos) - Equipe atual
            (1, '22222222222', 'Desenvolvedor Backend', 'Aceito'), # Bruno
            (1, '33333333333', 'Designer UX/UI', 'Aceito'),    # Carla
            
            # Projeto 2 (E-learning IA)
            (2, '22222222222', 'Desenvolvedor Backend', 'Aceito'), # Bruno
            (2, '88888888888', 'Cientista de Dados', 'Aceito'), # Helena
            (2, '67890123456', 'Scrum Master', 'Pendente'), # Vanessa
            
            # Projeto 3 (Fintech)
            (3, '45678901234', 'Engenheira DevOps', 'Aceito'), # Sofia
            (3, '22222222222', 'Desenvolvedor Backend', 'Pendente'), # Bruno
            (3, '34567890123', 'Engenheiro de QA', 'Pendente'), # Pedro
            
            # Projeto 4 (ONG Connect)
            (4, '77777777777', 'Desenvolvedor Frontend', 'Aceito'), # Gabriel
            
            # Projeto 6 (LegalTech)
            (6, '56789012345', 'Consultor Jurídico', 'Aceito') # Thiago
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO Equipes
                (id_projeto_fk, cpf_colaborador_fk, funcao_no_projeto, status_convite)
            VALUES (?, ?, ?, ?)
        """, lista_equipes)
        print(f"Inseridas {cursor.rowcount} associações de equipe (ou já existiam).")

        # Salva as alterações
        conexao.commit()
        print(f"\nBanco de dados '{DB_PATH}' populado com sucesso!")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao popular o banco de dados: {e}")
        if 'conexao' in locals():
            conexao.rollback() # Desfaz alterações em caso de erro
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if 'conexao' in locals() and conexao:
            conexao.close()

# --- Bloco de Execução ---
if __name__ == "__main__":
    popular_banco_de_dados()
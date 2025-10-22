import sqlite3

def criar_banco_de_dados():
    """
    Cria e configura o banco de dados 'plataforma_inovacao.db' 
    com todas as tabelas necessárias para o projeto.
    """
    nome_do_arquivo_db = 'plataforma_inovacao.db'
    
    try:
        # Conecta ao banco de dados (cria o arquivo se não existir)
        conexao = sqlite3.connect(nome_do_arquivo_db) 
        cursor = conexao.cursor()

        # --- HABILITAR SUPORTE A CHAVES ESTRANGEIRAS ---
        # Essencial para garantir a integridade dos dados (ex: um projeto 
        # só pode ser ligado a um usuário que existe)
        cursor.execute("PRAGMA foreign_keys = ON;")

        # --- TABELA 1: Usuarios ---
        # Armazena todos os usuários da plataforma.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                cpf TEXT PRIMARY KEY,
                nome_completo TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                resumo_profissional TEXT,
                link_portfolio TEXT,
                tipo_usuario TEXT NOT NULL CHECK(tipo_usuario IN ('Idealizador', 'Colaborador', 'Admin'))
            );
        """)

        # --- TABELA 2: Competencias ---
        # Lista mestra de todas as habilidades e interesses.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Competencias (
                id_competencia INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_competencia TEXT UNIQUE NOT NULL,
                tipo_competencia TEXT NOT NULL CHECK(tipo_competencia IN ('Habilidade', 'Interesse'))
            );
        """)

        # --- TABELA 3: Projetos ---
        # Armazena os projetos. Depende de 'Usuarios'.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Projetos (
                id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_projeto TEXT NOT NULL,
                descricao_projeto TEXT NOT NULL,
                categoria_projeto TEXT,
                cpf_idealizador_fk TEXT NOT NULL,
                status_projeto TEXT NOT NULL CHECK(status_projeto IN ('Buscando Equipe', 'Em Andamento', 'Concluído')),
                
                FOREIGN KEY (cpf_idealizador_fk) REFERENCES Usuarios (cpf)
            );
        """)

        # --- TABELA 4: Usuario_Competencias (Tabela de Junção) ---
        # Conecta usuários às suas competências. Depende de 'Usuarios' e 'Competencias'.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuario_Competencias (
                cpf_usuario_fk TEXT NOT NULL,
                id_competencia_fk INTEGER NOT NULL,
                
                PRIMARY KEY (cpf_usuario_fk, id_competencia_fk),
                FOREIGN KEY (cpf_usuario_fk) REFERENCES Usuarios (cpf),
                FOREIGN KEY (id_competencia_fk) REFERENCES Competencias (id_competencia)
            );
        """)

        # --- TABELA 5: Equipes (Tabela de Junção) ---
        # Conecta usuários (colaboradores) aos projetos. Depende de 'Usuarios' e 'Projetos'.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Equipes (
                id_associacao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_projeto_fk INTEGER NOT NULL,
                cpf_colaborador_fk TEXT NOT NULL,
                funcao_no_projeto TEXT,
                status_convite TEXT NOT NULL DEFAULT 'Pendente' CHECK(status_convite IN ('Pendente', 'Aceito', 'Recusado')),
                
                FOREIGN KEY (id_projeto_fk) REFERENCES Projetos (id_projeto),
                FOREIGN KEY (cpf_colaborador_fk) REFERENCES Usuarios (cpf)
            );
        """)

        # Salva as alterações no banco de dados
        conexao.commit()
        print(f"Banco de dados '{nome_do_arquivo_db}' e tabelas verificados/criados com sucesso.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao criar ou acessar o banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        # Fecha a conexão com o banco, mesmo se ocorrer um erro
        if 'conexao' in locals() and conexao:
            conexao.close()

# --- Bloco de Execução ---
# Este código só será executado quando você rodar o script diretamente.
if __name__ == "__main__":
    criar_banco_de_dados()
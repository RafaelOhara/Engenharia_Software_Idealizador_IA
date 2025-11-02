# Engenharia_Software_Idealizador_IA
Microsserviço de Sugestão de Talentos com IA
Um microsserviço que utiliza Inteligência Artificial para analisar a descrição de um projeto e as competências da equipe atual, recomendando os perfis profissionais que estão faltando para sua execução.

# Objetivo
O objetivo deste microsserviço é auxiliar idealizadores de projeto e equipes a identificar lacunas de habilidades em seus times.

Ao fornecer o ID de um projeto existente, a API analisa a descrição textual do projeto E as competências da equipe atual (ambos lidos de um banco de dados compartilhado) para recomendar perfis profissionais (ex: "Desenvolvedor Mobile Sênior", "Engenheiro de DevOps") que são cruciais para o sucesso da iniciativa. 

# Como Funciona
O serviço expõe um endpoint de API que recebe um ID de projeto. Internamente, o processo ocorre da seguinte forma:

Recebimento do ID: A API recebe uma requisição GET com o ID do projeto (ex: /api/v1/projetos/1/sugestoes).

Consulta ao Banco de Dados: O serviço consulta um banco de dados SQLite para buscar:

A descrição textual do projeto.

A lista de funções (cargos) da equipe atual.

A lista de competências (skills) da equipe atual.

Processamento com IA: A descrição do projeto e a lista de competências atuais são enviadas para a API do Google Gemini com um prompt estruturado, solicitando a análise e a sugestão de 3 perfis faltantes.

Recomendação: O sistema retorna um objeto JSON completo contendo os dados do projeto, a lista da equipe atual e as sugestões geradas pela IA.

# Tecnologias Utilizadas
Linguagem: Python 3.11+

Framework da API: FastAPI

Modelo de IA: Google Gemini (via API google-generativeai)

Banco de Dados: SQLite3

Servidor: Uvicorn

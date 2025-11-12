# Engenharia_Software_Idealizador_IA

# Microsserviço de Sugestão de Talentos com IA

Um microsserviço que utiliza Inteligência Artificial para analisar a descrição de um projeto e as competências da equipe atual, recomendando os perfis profissionais que estão faltando para sua execução.

---

# Deploy (Link da API)

A API está hospedada e pode ser acessada através do seguinte endpoint base:

**[https://seu-link-de-deploy-aqui.azurewebsites.net](https://seu-link-de-deploy-aqui.azurewebsites.net)**

---

# Objetivo

O objetivo deste microsserviço é auxiliar idealizadores de projeto e equipes a identificar lacunas de habilidades em seus times.

Ao **enviar um objeto JSON** contendo os detalhes de um projeto (descrição, categoria) e a lista de seus participantes com suas respectivas habilidades, a API analisa esses dados para recomendar perfis profissionais (ex: "Desenvolvedor Mobile Sênior", "Engenheiro de DevOps") que são cruciais para o sucesso da iniciativa.

Este serviço é **"stateless"**: ele não armazena dados e não depende de um banco de dados próprio. Ele apenas recebe, processa e responde.

# Como Funciona

O serviço expõe um endpoint de API que recebe um JSON. Internamente, o processo ocorre da seguinte forma:

1.  **Recebimento do JSON:** A API recebe uma requisição `POST` no endpoint `/projetos/sugestoes`. O corpo (body) da requisição deve conter o JSON com os dados do projeto.
2.  **Validação de Dados:** O JSON recebido é validado pelo FastAPI usando Pydantic para garantir que a estrutura (descrição, categoria, lista de participantes) está correta.
3.  **Processamento com IA:** A descrição do projeto e a lista de competências (extraídas do JSON) são enviadas para a API do Google Gemini com um prompt estruturado, solicitando a análise e a sugestão de 3 perfis faltantes.
4.  **Recomendação:** O sistema retorna um objeto JSON completo contendo os dados do projeto e as sugestões geradas pela IA.

# Tecnologias Utilizadas

* **Linguagem:** Python 3.11+
* **Framework da API:** FastAPI
* **Validação de Dados:** Pydantic
* **Modelo de IA:** Google Gemini (via API `google-generativeai`)
* **Servidor:** Uvicorn

---
# Uso da API

### `POST /projetos/sugestoes`

Este é o endpoint principal. Ele recebe um JSON com os dados do projeto e retorna as sugestões da IA.

#Exemplo de JSON (Body da Requisição)

Você deve enviar um JSON neste formato:

```json
{
  "id_projeto": 1,
  "descricao_projeto": "Um app para organizar equipes e alocar tarefas de engenharia.",
  "categoria_projeto": "Engenharia",
  "participantes": [
    {
      "collaborator_email": "ana@email.com",
      "contributed_skill_name": "React",
      "contributed_skill_level": 3
    },
    {
      "collaborator_email": "ana@email.com",
      "contributed_skill_name": "Figma",
      "contributed_skill_level": 2
    },
    {
      "collaborator_email": "bruno@email.com",
      "contributed_skill_name": "Docker",
      "contributed_skill_level": 2
    }
  ]
}

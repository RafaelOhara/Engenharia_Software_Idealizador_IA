import google.generativeai as genai
import json
from src.core.config import GOOGLE_API_KEY


def _build_prompt(descricao_projeto: str, competencias_atuais: list[str]) -> str:
    """
    Cria o prompt estruturado para enviar à IA.
    """
    if not competencias_atuais:
        competencias_str = "Nenhuma competência informada."
    else:
        competencias_str = ", ".join(competencias_atuais)

    prompt = f"""
        Você é um especialista em recrutamento técnico (Tech Recruiter) e formação de equipes para startups de tecnologia.
        Sua tarefa é analisar a descrição de um projeto e as competências da equipe atual.

        Com base nisso, sugira 3 (três) perfis ou papéis que estão faltando e que são cruciais para o sucesso do projeto. 
        Para cada sugestão, forneça uma breve justificativa.

        **Descrição do Projeto:**
        "{descricao_projeto}"

        **Competências da Equipe Atual:**
        [{competencias_str}]

        Responda APENAS com um objeto JSON válido, seguindo este formato exato:
        {{
          "sugestoes": [
            {{"perfil_sugerido": "Nome do Perfil 1", "justificativa": "Explicação do porquê este perfil é necessário."}},
            {{"perfil_sugerido": "Nome do Perfil 2", "justificativa": "Explicação do porquê este perfil é necessário."}},
            {{"perfil_sugerido": "Nome do Perfil 3", "justificativa": "Explicação do porquê este perfil é necessário."}}
          ]
        }}
    """
    return prompt

def get_ia_suggestions(descricao_projeto: str, competencias_atuais: list[str]) -> dict:
    """
    Envia o prompt para a API do Gemini e retorna a resposta como um dicionário.
    """
    # A configuração acontece SÓ quando a função é chamada.
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        print(f"Erro ao configurar a API do Gemini: {e}")
        return {"erro": f"Falha ao configurar API do Gemini: {str(e)}"}

    prompt = _build_prompt(descricao_projeto, competencias_atuais)

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip().lstrip("```json\n").rstrip("\n```")
        sugestoes_dict = json.loads(response_text)
        return sugestoes_dict

    except json.JSONDecodeError:
        print(f"Erro: A resposta da IA não foi um JSON válido. Resposta recebida:\n{response.text}")
        return {"erro": "A resposta da IA não estava no formato JSON esperado."}
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return {"erro": f"Erro na API: {str(e)}"}
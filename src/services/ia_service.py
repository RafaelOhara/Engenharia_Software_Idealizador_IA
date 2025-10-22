# Salve este arquivo como: src/services/ia_service.py

import google.generativeai as genai
import json
from src.core.config import GOOGLE_API_KEY

# Configura a API do Google com a chave
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash') # Usando o modelo mais recente e rápido
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")
    model = None

def _build_prompt(descricao_projeto: str, competencias_atuais: list[str]) -> str:
    """
    Cria o prompt estruturado para enviar à IA.
    """
    # Converte a lista de competências em uma string formatada
    if not competencias_atuais:
        competencias_str = "Nenhuma competência informada."
    else:
        competencias_str = ", ".join(competencias_atuais)

    # O prompt é a parte mais importante:
    # Ele dá um "papel" à IA e define o formato de saída (JSON)
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
    if not model:
        return {"erro": "API do Gemini não configurada corretamente."}

    prompt = _build_prompt(descricao_projeto, competencias_atuais)
    
    try:
        # Envia o prompt para o modelo
        response = model.generate_content(prompt)
        
        # Extrai o texto da resposta e remove "limpa" para garantir que é JSON
        response_text = response.text.strip().lstrip("```json\n").rstrip("\n```")
        
        # Converte a string JSON em um dicionário Python
        sugestoes_dict = json.loads(response_text)
        
        return sugestoes_dict

    except json.JSONDecodeError:
        print(f"Erro: A resposta da IA não foi um JSON válido. Resposta recebida:\n{response.text}")
        return {"erro": "A resposta da IA não estava no formato JSON esperado."}
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return {"erro": f"Erro na API: {str(e)}"}

# --- Bloco de teste (para verificar se este arquivo está funcionando) ---
if __name__ == "__main__":
    print("--- Testando ia_service ---")
    
    # Simula os dados que viriam do banco de dados para o Projeto 1
    # (O projeto com 5 competências que testamos antes)
    projeto_teste_desc = "Um aplicativo mobile para conectar músicos amadores para formarem bandas e marcarem ensaios."
    equipe_teste_comps = ["Python", "Node.js", "Banco de Dados SQL", "Design UX/UI", "React"]
    
    print(f"Descrição: {projeto_teste_desc}")
    print(f"Competências: {equipe_teste_comps}")
    print("\nChamando API do Gemini (aguarde)...")
    
    sugestoes = get_ia_suggestions(projeto_teste_desc, equipe_teste_comps)
    
    print("\n--- Resposta da IA (formatada) ---")
    if "erro" in sugestoes:
        print(f"Erro: {sugestoes['erro']}")
    else:
        # Imprime de forma bonita
        print(json.dumps(sugestoes, indent=2, ensure_ascii=False))
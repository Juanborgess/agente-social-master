from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import prompts  

load_dotenv()

def gerar_copy_social(nicho, produto, objetivo, tipo="single"):
    """
    Função que decide qual 'cérebro' usar com base no tipo de post.
    tipo: 'single' (Padrão) ou 'carousel'
    """
    
    if tipo == "carousel":
        print(f"🔄 Ativando modo CARROSSEL para: {nicho}")
        sistema = prompts.CAROUSEL_SYSTEM_PROMPT
        instrucao_extra = "Formato obrigatório: CARROSSEL DE 5 A 7 SLIDES com instruções de design slide a slide."
    else:
        print(f"⚡ Ativando modo POST ÚNICO para: {nicho}")
        sistema = prompts.SOCIAL_MEDIA_SYSTEM_PROMPT
        instrucao_extra = "Formato obrigatório: POST ÚNICO (Imagem/Reels) com framework PAS."

    user_request = f"""
    CONTEXTO DO PROJETO:
    - Nicho Alvo: {nicho}
    - Produto/Serviço: {produto}
    - Objetivo: {objetivo}
    
    {instrucao_extra}
    
    Siga estritamente a estrutura de resposta (JSON implícito) definida no seu System Prompt.
    """

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"), 
        description=sistema,
        markdown=True
    )

    response = agent.run(user_request)
    return response.content

if __name__ == "__main__":
    print("--- 🧪 Testando Modo Carrossel ---")
    res = gerar_copy_social("Advogados", "Consultoria", "Vender mais", tipo="carousel")
    print(res)
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import prompts 

load_dotenv()

def gerar_copy_social(nicho, produto, objetivo):
    """
    Função modular que cria o agente, executa a tarefa e retorna a resposta.
    """
    
    user_request = f"""
    CONTEXTO DO PEDIDO:
    - Nicho Alvo: {nicho}
    - Produto Ofertado: {produto}
    - Objetivo do Post: {objetivo}
    
    Crie o roteiro agora seguindo suas instruções de sistema.
    """

    # Configuração do Agente
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"), 
        description=prompts.SOCIAL_MEDIA_SYSTEM_PROMPT,
        markdown=True
    )

    # Execução
    response = agent.run(user_request)
    return response.content

# --- BLOCO DE TESTE INTERNO ---
# Este bloco 'if' só roda se eu executar este arquivo diretamente.
# Se este arquivo for importado por outro (no futuro), isso não roda.
if __name__ == "__main__":
    print("--- 🧪 Iniciando Teste de Texto (Modo Econômico) ---")
    
    resultado = gerar_copy_social(
        nicho="Advogados Tributaristas",
        produto="Automação de Atendimento com IA",
        objetivo="Mostrar que eles perdem clientes por demora no WhatsApp"
    )
    
    print("\n" + resultado)
    print("\n--- ✅ Fim do Teste ---")
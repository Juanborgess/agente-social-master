from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERRO CRÍTICO: Chave de API não encontrada! Verifique o arquivo .env")
else:
    print(f"Sucesso: Chave carregada (Inicia com: {api_key[:5]}...)")

agent = Agent(
    model=OpenAIChat(id="GPT-4o-mini"),
    description="Você é um estrategista de Marketing Digital focado em vendas High Ticket. Suas respostas são diretas e focadas em conversão.",
    markdown=True, 
)

print("\n--- 🤖 Testando Geração de Texto ---")
agent.print_response(
    "Aja como um especialista. Escreva apenas uma 'Headline' (título chamativo) para um post de Instagram focado em Advogados Tributaristas que querem escalar seus escritórios.", 
    stream=True
)
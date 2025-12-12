# agente_imagem.py
import os
import requests
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def criar_prompt_visual(nicho, objetivo):
    """
    Usa um Agente Agno (Diretor de Arte) para escrever um prompt técnico para o DALL-E.
    """
    diretor_arte = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        description="Você é um Diretor de Arte premiado especialista em fotografia para redes sociais corporativas.",
        instructions=[
            "Sua tarefa é criar um PROMPT VISUAL para uma IA geradora de imagens (DALL-E 3).",
            "O prompt deve ser em INGLÊS para melhor qualidade.",
            "Estilo: Fotorealista, Cinematográfico, Iluminação de Estúdio, 4k.",
            "Não inclua texto na imagem.",
            "Evite clichês de banco de imagens (pessoas apertando as mãos, sorrisos falsos).",
            "Foque em metáforas visuais ou ambientes profissionais de alto padrão.",
            "Retorne APENAS o texto do prompt, sem introduções."
        ],
        markdown=False
    )
    
    msg = f"Crie um prompt visual para um post focado em: {nicho}. O conceito do post é: {objetivo}."
    response = diretor_arte.run(msg)
    return response.content

def gerar_imagem(prompt_visual):
    """
    Envia o prompt para o DALL-E 3 e retorna a URL da imagem.
    """
    print(f"\n🎨 Desenhando: {prompt_visual[:100]}...")
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_visual,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")
        return None

def download_imagem(url, nome_arquivo):
    """
    Baixa a imagem da URL e salva na pasta local.
    """
    if not url: return
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(nome_arquivo, 'wb') as f:
            f.write(response.content)
        print(f"✅ Imagem salva com sucesso: {nome_arquivo}")
    else:
        print("❌ Erro ao baixar a imagem.")

# --- BLOCO DE TESTE ---
if __name__ == "__main__":
    print("--- 🎨 Iniciando Teste de Imagem (Isso custa aprox $0.04) ---")
    
    nicho_teste = "Advogados Tributaristas"
    objetivo_teste = "Medo de perder prazos e clientes por desorganização"
    
    print("1. Criando conceito visual...")
    prompt_dalle = criar_prompt_visual(nicho_teste, objetivo_teste)
    print(f"--> Prompt Gerado (Diretor): {prompt_dalle}")
    
    url_imagem = gerar_imagem(prompt_dalle)
    
    if url_imagem:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_final = f"teste_imagem_{timestamp}.png"
        download_imagem(url_imagem, nome_final)
        
        try:
            os.startfile(nome_final) 
        except:
            pass
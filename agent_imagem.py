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
    Usa um Agente Agno (Diretor de Arte Sênior) para escrever um prompt TÉCNICO e VISCERAL para o DALL-E 3.
    """
    diretor_arte = Agent(
        model=OpenAIChat(id="gpt-4o-mini"), 
        description="You are an award-winning Photography Director for high-end luxury brands (like Rolex, Forbes, Architectural Digest). You hate stock photos.",
        instructions=[
            "YOUR TASK: Create a detailed, photographic prompt in ENGLISH for DALL-E 3 based on the user's niche and objective.",
            
            "--- STYLE GUIDELINES (CRITICAL) ---",
            "1. VISUAL STYLE: Documentary-style editorial photography. Use terms like 'Shot on film', 'Grain', 'Natural texture'.",
            "2. CAMERA/LENS: Specify the look. E.g., '85mm lens with shallow depth of field' (creates blurry background focus), or 'Leica M6'.",
            "3. LIGHTING: NEVER use flat lighting. Use 'Moody lighting', 'Chiaroscuro' (dramatic contrast), 'Golden hour light streaming through a window', or 'Cinematic shadows'.",
            "4. COMPOSITION: Rule of thirds, minimalist, or intense close-up (macro).",
            
            "--- CONTENT GUIDELINES ---",
            "5. METAPHOR OVER LITERAL: If the objective is about 'losing time/money', DO NOT show a stressed person looking at a clock. Show a luxurious hourglass on an oak desk with sand running out fast, with a blurry city skyline in the background.",
            "6. SETTING: The environment must scream 'High Ticket'. Luxurious offices, modern architecture, minimalist studios, dark wood, marble, sophisticated textures.",
            "7. NEGATIVE CONSTRAINTS: NO text, NO generic smiling people shaking hands, NO sterile 3D renders, NO cartoonish colors. Keep it serious and sophisticated.",
            
            "--- FINAL OUTPUT FORMAT ---",
            "Return ONLY the raw English prompt text. No introductions."
        ],
        markdown=False
    )
    
    msg = f"PROJECT CONTEXT:\nTarget Niche: {nicho}\nObjective of the visual: {objetivo}\n\nCreate the DALL-E 3 prompt now, focusing on a sophisticated, dramatic, and metaphorical image."
    response = diretor_arte.run(msg)
    return response.content

def gerar_imagem(prompt_visual):
    """
    Envia o prompt para o DALL-E 3 e retorna a URL da imagem.
    """
    print(f"\n🎨 Desenhando no DALL-E 3 com o novo prompt de alta performance...")
    # print(f"DEBUG PROMPT: {prompt_visual}") # Descomente se quiser ver o prompt inglês no terminal
    
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
        print(f"Erro crítico ao gerar imagem: {e}")
        return None

def download_imagem(url, nome_arquivo):
    """
    Baixa a imagem da URL e salva na pasta local.
    """
    if not url: return
    
    try:
        response = requests.get(url, timeout=30) 
        if response.status_code == 200:
            with open(nome_arquivo, 'wb') as f:
                f.write(response.content)
            print(f"✅ Imagem salva com sucesso: {nome_arquivo}")
        else:
            print(f"❌ Erro ao baixar a imagem. Status: {response.status_code}")
    except Exception as e:
         print(f"❌ Erro de conexão no download: {e}")

if __name__ == "__main__":
    print("--- 🎨 Testando NOVO Diretor de Arte (Custo ~ $0.04) ---")
    
    nicho_teste = "Advogados Tributaristas de Alto Padrão"
    objetivo_teste = "Transmitir a sensação de urgência e dinheiro sendo perdido por falta de gestão."
    
    print("1. Criando conceito visual PRO...")
    prompt_dalle = criar_prompt_visual(nicho_teste, objetivo_teste)
    print(f"\n--> Prompt Gerado (Inglês): {prompt_dalle}\n")
    
    # as linhas abaixo geram imagem real (gasta créditos)
    # url_imagem = gerar_imagem(prompt_dalle)
    # if url_imagem:
    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     nome_final = f"teste_imagem_pro_{timestamp}.png"
    #     download_imagem(url_imagem, nome_final)
    #     try: os.startfile(nome_final) 
    #     except: pass
import os
from datetime import datetime
import agent_texto  
import agent_imagem

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=================================================")
    print("🚀 AGENTE SOCIAL MEDIA MASTER - HIGH TICKET V1.0")
    print("=================================================")
    
    # 1. COLETA DE DADOS (Inputs)
    nicho = input("\n1. Qual o Nicho-Alvo? (Ex: Advogados): ")
    produto = input("2. Qual o Produto/Serviço? (Ex: Automação): ")
    objetivo = input("3. Qual o Objetivo do Post? (Ex: Medo de perder cliente): ")

    print("\n-------------------------------------------------")
    print("🧠 O Agente de Texto está trabalhando...")
    print("-------------------------------------------------")

    # 2. GERAÇÃO DE TEXTO (Copy)
    try:
        texto_final = agent_texto.gerar_copy_social(nicho, produto, objetivo)
        
        print("\n" + "="*20 + " ROTEIRO SUGERIDO " + "="*20)
        print(texto_final)
        print("="*60)
        
    except Exception as e:
        print(f"❌ Erro ao gerar texto: {e}")
        return

    # 3. MOMENTO DE APROVAÇÃO (O "Checkpoint")
    print("\n-------------------------------------------------")
    decisao = input("👉 Gostou do texto? Deseja gerar a imagem agora? (s/n): ").strip().lower()

    if decisao != 's':
        print("\n🛑 Operação cancelada pelo usuário. Nenhum custo de imagem gerado.")
        return

    # 4. GERAÇÃO DE IMAGEM (Visual)
    print("\n🎨 O Diretor de Arte está criando o conceito...")
    try:
        prompt_visual = agent_imagem.criar_prompt_visual(nicho, objetivo)
        print(f"--> Conceito Visual: {prompt_visual}")
        
        print("\n🎨 Desenhando no DALL-E 3 (Aguarde alguns segundos)...")
        url_imagem = agent_imagem.gerar_imagem(prompt_visual)
        
        if url_imagem:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"post_{timestamp}.png"
            
            agent_imagem.download_imagem(url_imagem, nome_arquivo)
            
            try:
                os.startfile(nome_arquivo)
            except:
                print(f"Imagem salva em: {nome_arquivo}")
                
            print("\n✅ CICLO CONCLUÍDO COM SUCESSO!")
            
    except Exception as e:
        print(f"❌ Erro na geração de imagem: {e}")

if __name__ == "__main__":
    main()
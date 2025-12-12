from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import agent_texto 
import agent_imagem 

app = FastAPI(
    title="Agente Social Master API",
    description="API High Ticket para geração de conteúdo estratégico.",
    version="1.0"
)

class PedidoRoteiro(BaseModel):
    nicho: str
    produto: str
    objetivo: str

class PedidoImagem(BaseModel):
    nicho: str
    objetivo: str

@app.post("/gerar-roteiro")
def rota_gerar_texto(pedido: PedidoRoteiro):
    """
    Recebe nicho/produto/objetivo e retorna o Copy pronto.
    """
    try:
        print(f"📝 Recebendo pedido de texto para: {pedido.nicho}")
        texto = agent_texto.gerar_copy_social(pedido.nicho, pedido.produto, pedido.objetivo)
        return {"status": "sucesso", "roteiro": texto}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/gerar-imagem")
def rota_gerar_imagem(pedido: PedidoImagem):
    """
    Recebe o conceito aprovado e gera a URL da imagem no DALL-E.
    """
    try:
        print(f"🎨 Recebendo pedido de imagem para: {pedido.nicho}")
        
        prompt_visual = agent_imagem.criar_prompt_visual(pedido.nicho, pedido.objetivo)
        
        url_imagem = agent_imagem.gerar_imagem(prompt_visual)
        
        if not url_imagem:
            raise HTTPException(status_code=500, detail="Falha ao gerar imagem na OpenAI")

        return {
            "status": "sucesso", 
            "prompt_usado": prompt_visual,
            "url_imagem": url_imagem
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"mensagem": "API Agente Social Master está ONLINE 🚀"}
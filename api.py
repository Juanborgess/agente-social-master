# api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import agent_texto 
import agent_imagem 

app = FastAPI(
    title="Agente Social Master API",
    description="API High Ticket para geração de conteúdo estratégico.",
    version="1.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PedidoRoteiro(BaseModel):
    nicho: str
    produto: str
    objetivo: str
    tipo: str = "single"  

class PedidoImagem(BaseModel):
    nicho: str
    objetivo: str


@app.post("/gerar-roteiro")
def rota_gerar_texto(pedido: PedidoRoteiro):
    """
    Recebe o pedido e o TIPO de conteúdo (single ou carousel).
    """
    try:
        texto = agent_texto.gerar_copy_social(
            pedido.nicho, 
            pedido.produto, 
            pedido.objetivo,
            pedido.tipo 
        )
        return {"status": "sucesso", "roteiro": texto}
    except Exception as e:
        print(f"Erro no servidor: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gerar-imagem")
def rota_gerar_imagem(pedido: PedidoImagem):
    try:
        prompt_visual = agent_imagem.criar_prompt_visual(pedido.nicho, pedido.objetivo)
        url_imagem = agent_imagem.gerar_imagem(prompt_visual)
        
        if not url_imagem:
            raise HTTPException(status_code=500, detail="Falha ao gerar imagem")

        return {
            "status": "sucesso", 
            "prompt_usado": prompt_visual,
            "url_imagem": url_imagem
        }
    except Exception as e:
        print(f"Erro imagem: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"mensagem": "API Agente Social Master v1.1 ONLINE 🚀"}
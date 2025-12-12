const API_URL = "http://127.0.0.1:8000";

const inputs = {
    nicho: document.getElementById('nicho'),
    produto: document.getElementById('produto'),
    objetivo: document.getElementById('objetivo')
};

const btns = {
    texto: document.getElementById('btnGerarTexto'),
    imagem: document.getElementById('btnGerarImagem')
};

const sections = {
    texto: document.getElementById('resultTextoSection'),
    imagem: document.getElementById('resultImagemSection')
};

const outputs = {
    texto: document.getElementById('textoOutput'),
    imagem: document.getElementById('imageOutput'),
    loadingImg: document.getElementById('imageLoading')
};

let estadoAtual = {
    nicho: "",
    objetivo: ""
};

btns.texto.addEventListener('click', async () => {
    
    if(!inputs.nicho.value || !inputs.produto.value || !inputs.objetivo.value) {
        alert("⚠️ Por favor, preencha todos os campos da estratégia.");
        return;
    }

    const textoOriginal = btns.texto.innerText;
    btns.texto.innerText = "⏳ Criando Estratégia...";
    btns.texto.disabled = true; 
    
    outputs.texto.innerText = ""; 
    sections.texto.classList.add('hidden');
    sections.imagem.classList.add('hidden');

    estadoAtual.nicho = inputs.nicho.value;
    estadoAtual.objetivo = inputs.objetivo.value;

    try {
        const modoSelecionado = document.querySelector('input[name="tipoConteudo"]:checked').value;
        
        console.log("Enviando pedido no modo:", modoSelecionado); 

        const response = await fetch(`${API_URL}/gerar-roteiro`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nicho: inputs.nicho.value,
                produto: inputs.produto.value,
                objetivo: inputs.objetivo.value,
                tipo: modoSelecionado 
            })
        });

        const data = await response.json();

        if (data.status === "sucesso") {
            sections.texto.classList.remove('hidden');
            typeWriter(data.roteiro, outputs.texto);
        } else {
            alert("Erro na geração: " + data.detail);
        }

    } catch (error) {
        console.error(error);
        alert("Erro de conexão. Verifique se o backend (uvicorn) está rodando.");
    } finally {
        btns.texto.innerText = textoOriginal;
        btns.texto.disabled = false;
    }
});

btns.imagem.addEventListener('click', async () => {
    btns.imagem.classList.add('hidden');
    sections.imagem.classList.remove('hidden');
    outputs.loadingImg.classList.remove('hidden');
    outputs.imagem.innerHTML = ""; 

    try {
        const response = await fetch(`${API_URL}/gerar-imagem`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nicho: estadoAtual.nicho,
                objetivo: estadoAtual.objetivo
            })
        });

        const data = await response.json();

        if (data.status === "sucesso") {
            const img = document.createElement('img');
            img.src = data.url_imagem;
            img.alt = "Imagem gerada por IA";
            
            img.onload = () => {
                outputs.loadingImg.classList.add('hidden');
                outputs.imagem.appendChild(img);
            };
        } else {
            alert("Erro ao gerar imagem.");
            btns.imagem.classList.remove('hidden');
        }

    } catch (error) {
        console.error(error);
        alert("Erro de conexão.");
        btns.imagem.classList.remove('hidden');
    }
});

function typeWriter(text, element) {
    let i = 0;
    element.innerHTML = "";
    const speed = 5; 

    function type() {
        if (i < text.length) {
            if (text.charAt(i) === '\n') {
                element.innerHTML += '<br>';
            } else {
                element.innerHTML += text.charAt(i);
            }
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}
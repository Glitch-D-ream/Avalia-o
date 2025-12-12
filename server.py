#!/usr/bin/env python3
"""ASCENSÃO DO CULTIVO DIGITAL - Servidor FastAPI com WebSockets
Versão Aprimorada: Captura de Tráfego Desacoplada em um cliente externo.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from scapy.all import get_if_list # Scapy ainda é útil para obter interfaces

from web_data_collector import WebDataCollector
import subprocess
import platform
import psutil
from datetime import datetime
from pathlib import Path
import logging
import sys
import os

# Adicionar diretório atual ao path para importar módulos locais
sys.path.insert(0, os.path.dirname(__file__))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar threading para o módulo de phishing
import threading

# Importar módulos de análise avançada (com tratamento de erro)
try:
    from network_scanner_advanced import NmapScanner, NetworkVulnerabilityAnalyzer
    logger.info("Módulo network_scanner_advanced carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar network_scanner_advanced: {e}")
    NmapScanner = None
    NetworkVulnerabilityAnalyzer = None

try:
    from wifi_security_analyzer import WiFiSecurityAnalyzer, WiFiNetwork, WPA2HandshakeSimulator
    logger.info("Módulo wifi_security_analyzer carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar wifi_security_analyzer: {e}")
    WiFiSecurityAnalyzer = None
    WiFiNetwork = None
    WPA2HandshakeSimulator = None

try:
    from mobile_integration import mobile_manager, MobileCommandExecutor, MobileCommand
    logger.info("Módulo mobile_integration carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar mobile_integration: {e}")
    mobile_manager = None
    MobileCommandExecutor = None
    MobileCommand = None

# Configurar FastAPI
app = FastAPI(title="ASCENSÃO - CULTIVO DIGITAL API", version="v15.0")

# Rota de saúde simples
@app.get("/")
async def serve_health_check():
    return {"message": "Backend está rodando. Frontend não está montado."}

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

    async def broadcast(self, data: dict):
        """Envia dados para todos os clientes conectados"""
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.error(f"Erro ao enviar dados: {e}")

manager = ConnectionManager()

# ============================================================================
# MÓDULO 1: RECEBIMENTO DE DADOS DE TRÁFEGO (DO CLIENTE EXTERNO)
# ============================================================================

# Variáveis para armazenar dados de tráfego recebidos
traffic_data_store = []
protocol_stats_store = {
    "HTTP": 0,
    "HTTPS": 0,
    "DNS": 0,
    "ARP": 0,
    "TCP": 0,
    "UDP": 0,
    "Other": 0
}

# ============================================================================
# ENDPOINTS REST API
# ============================================================================

@app.post("/api/traffic/realtime")
async def receive_traffic_data(data: dict):
    """Recebe dados de pacotes do cliente de captura e faz broadcast via WebSocket"""
    global traffic_data_store, protocol_stats_store
    
    packets = data.get("packets", [])
    
    for packet in packets:
        # 1. Armazenar o pacote
        traffic_data_store.append(packet)
        
        # 2. Atualizar estatísticas
        protocol = packet.get("protocol", "Other")
        protocol_stats_store[protocol] = protocol_stats_store.get(protocol, 0) + 1
        
        # 3. Enviar dados para o Dashboard via WebSocket
        await manager.broadcast({
            "type": "traffic_update",
            "data": packet,
            "stats": protocol_stats_store
        })
        
        # 4. Análise de Credenciais em Texto Plano (Alerta)
        if packet.get("credential_alert"):
            await manager.broadcast({
                "type": "vulnerability_alert",
                "severity": "CRITICAL",
                "name": "Credenciais em Texto Plano Detectadas",
                "description": f"Credenciais foram detectadas em tráfego HTTP não criptografado de {packet.get('src_ip')} para {packet.get('dst_ip')}. Dados: {packet.get('payload_snippet')}",
                "timestamp": packet.get("timestamp")
            })
        
    # Manter o histórico limitado
    traffic_data_store = traffic_data_store[-100:]
    
    return {"status": "success", "received_count": len(packets)}

@app.get("/api/network/interfaces")
async def get_interfaces():
    """Obter lista de interfaces de rede disponíveis"""
    try:
        interfaces = [iface for iface in get_if_list()]
        return {"interfaces": interfaces}
    except Exception as e:
        logger.error(f"Erro ao obter interfaces de rede: {e}")
        return {"interfaces": ["Wi-Fi", "Ethernet", "eth0", "wlan0"]}

@app.get("/api/traffic/stats")
async def get_traffic_stats():
    """Obter estatísticas de tráfego"""
    return {
        "total_packets": len(traffic_data_store),
        "protocol_stats": protocol_stats_store,
        "recent_packets": traffic_data_store[-10:]  # Últimos 10
    }

# MÓDULO 2: SIMULADOR DE FORÇA BRUTA ÉTICA (REMOVIDO DEVIDO A ERRO DE IMPORTAÇÃO)



# ============================================================================
# MÓDULO 3: PHISHING REAL (NÍVEL AVANÇADO)
# ============================================================================

# Importar o módulo real de phishing
try:
    from real_phishing_module import RealPhishingModule
    logger.info("Módulo real_phishing_module carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar real_phishing_module: {e}")
    RealPhishingModule = None

# Variável global para o módulo de phishing
phishing_module = RealPhishingModule() if RealPhishingModule else None

@app.post("/api/phishing/start")
async def start_phishing_attack(target_url: str):
    """Inicia o ataque de phishing real (clonagem e captura)"""
    if not phishing_module:
        return {"status": "error", "message": "Módulo de phishing real não carregado."}
    
    # O módulo real de phishing inicia um servidor HTTP para servir a página clonada
    # e capturar as credenciais.
    try:
        phishing_module.start_attack(target_url)
        
        # O módulo real de phishing deve retornar a URL do servidor falso
        return {"status": "running", "fake_url": phishing_module.get_fake_server_url()}
    except Exception as e:
        logger.error(f"Erro ao iniciar ataque de phishing: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/phishing/status")
async def get_phishing_status():
    """Obtém o status e credenciais capturadas do phishing real"""
    if not phishing_module:
        return {"status": "error", "message": "Módulo de phishing real não carregado."}
    
    return phishing_module.get_status()

@app.post("/api/phishing/stop")
async def stop_phishing_attack():
    """Para o ataque de phishing real"""
    if not phishing_module:
        return {"status": "error", "message": "Módulo de phishing real não carregado."}
    
    try:
        phishing_module.stop_attack()
        return {"status": "idle", "message": "Servidor de Phishing parado com sucesso."}
    except Exception as e:
        logger.error(f"Erro ao parar ataque de phishing: {e}")
        return {"status": "error", "message": str(e)}

# ============================================================================
# MÓDULO 4: INTEGRAÇÃO COM OWASP ZAP REAL (NÍVEL AVANÇADO)
# ============================================================================

# Configurações do ZAP (devem ser ajustadas conforme o ambiente)
# ATENÇÃO: A API Key deve ser obtida do ZAP Desktop
ZAP_API_KEY = 'SUA_API_KEY_AQUI' 
ZAP_PROXY_HOST = '127.0.0.1'
ZAP_PROXY_PORT = 8080

# Instanciar o ZAP Real
try:
    from zapv2 import ZAPv2
    zap = ZAPv2(
        apikey=ZAP_API_KEY, 
        proxies={
            'http': f'http://{ZAP_PROXY_HOST}:{ZAP_PROXY_PORT}', 
            'https': f'http://{ZAP_PROXY_HOST}:{ZAP_PROXY_PORT}'
        }
    )
    logger.info("OWASP ZAP Real instanciado com sucesso.")
except ImportError:
    logger.error("Biblioteca zapv2 não instalada. Execute 'pip install python-owasp-zap-v2.4'")
    zap = None
except Exception as e:
    logger.error(f"Erro ao instanciar ZAPv2: {e}")
    zap = None

@app.post("/api/zap/scan/start")
async def start_zap_scan(target_url: str):
    """Inicia um scan ativo do OWASP ZAP Real"""
    if not zap:
        return {"status": "error", "message": "ZAP Real não está instanciado. Verifique a chave de API e o proxy."}
    
    logger.info(f"Iniciando scan ativo do ZAP contra: {target_url}")
    
    # Iniciar o scan ativo em background
    async def run_scan():
        try:
            # Primeiro, garantir que o site está no contexto (opcional, mas recomendado)
            zap.urlopen(target_url)
            
            # Iniciar o scan ativo
            scan_id = zap.ascan.scan(url=target_url)
            
            # Monitorar o progresso e enviar updates via WebSocket
            while int(zap.ascan.status(scan_id)) < 100:
                progress = zap.ascan.status(scan_id)
                await manager.broadcast({
                    "type": "zap_progress",
                    "progress": progress,
                    "target": target_url
                })
                await asyncio.sleep(5)
            
            # Scan concluído, obter resultados
            results = zap.core.alerts(baseurl=target_url)
            
            await manager.broadcast({
                "type": "zap_scan_completed",
                "data": {
                    "status": "COMPLETED",
                    "target_url": target_url,
                    "alerts": results
                }
            })
            logger.info(f"Scan ZAP concluído para {target_url}. Alertas encontrados: {len(results)}")
            
        except Exception as e:
            logger.error(f"Erro durante o scan ZAP: {e}")
            await manager.broadcast({
                "type": "zap_scan_error",
                "message": str(e)
            })

    asyncio.create_task(run_scan())
    
    return {"status": "scan_started", "target": target_url, "message": "Scan ativo do ZAP Real iniciado em background."}

@app.get("/api/zap/scan/status")
async def get_zap_scan_status(target_url: str = None):
    """Obtém o status atual e os alertas do ZAP Real"""
    if not zap:
        return {"status": "error", "message": "ZAP Real não está instanciado."}
    
    try:
        # Obter status do último scan
        status = zap.ascan.status()
        
        # Obter alertas
        alerts = zap.core.alerts(baseurl=target_url) if target_url else zap.core.alerts()
        
        return {
            "status": "RUNNING" if int(status) < 100 else "COMPLETED",
            "progress": status,
            "alerts_count": len(alerts),
            "alerts": alerts
        }
    except Exception as e:
        logger.error(f"Erro ao obter status do ZAP: {e}")
        return {"status": "error", "message": str(e)}

# ============================================================================
# MÓDULO 6: EXPLORAÇÃO AVANÇADA (CONCEITO C2/PÓS-EXPLORAÇÃO)
# ============================================================================

# Importar o módulo de exploração avançada
try:
    from advanced_exploitation_module import exploitation_module
    logger.info("Módulo de Exploração Avançada carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar AdvancedExploitationModule: {e}")
    exploitation_module = None

@app.post("/api/exploit/generate_payload")
async def generate_payload(target_url: str):
    """Gera um payload de pós-exploração para o alvo."""
    if not exploitation_module:
        return {"status": "error", "message": "Módulo de Exploração Avançada não carregado."}
    
    result = exploitation_module.generate_payload(target_url)
    return result

@app.post("/api/exploit/send_command")
async def send_exploit_command(command: str):
    """Envia um comando de pós-exploração para o alvo (simulado)."""
    if not exploitation_module:
        return {"status": "error", "message": "Módulo de Exploração Avançada não carregado."}
    
    result = exploitation_module.send_command(command)
    return result

@app.get("/api/exploit/status")
async def get_exploit_status():
    """Obtém o status da sessão de exploração."""
    if not exploitation_module:
        return {"status": "error", "message": "Módulo de Exploração Avançada não carregado."}
    
    return exploitation_module.get_status()

# ============================================================================
# MÓDULO 7: EXPLORAÇÃO REAL COM SQLMAP
# ============================================================================

# Importar o módulo SQLMap
try:
    from sqlmap_module import sqlmap_module
    logger.info("Módulo SQLMap carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar SQLMapModule: {e}")
    sqlmap_module = None

@app.post("/api/sqlmap/scan/start")
async def start_sqlmap_scan(target_url: str):
    """Inicia um scan de SQL Injection com SQLMap"""
    if not sqlmap_module:
        return {"status": "error", "message": "Módulo SQLMap não carregado."}
    
    result = sqlmap_module.start_scan(target_url)
    return result

@app.get("/api/sqlmap/scan/status")
async def get_sqlmap_status():
    """Obtém o status e resultados do scan SQLMap"""
    if not sqlmap_module:
        return {"status": "error", "message": "Módulo SQLMap não carregado."}
    
    return sqlmap_module.get_status()

# ============================================================================
# WebSocket Endpoint
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Apenas mantém a conexão aberta para receber broadcasts
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ============================================================================
# Inicialização
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando servidor FastAPI em http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)

# ============================================================================
# MÓDULO 4: COLETOR DE DADOS WEB (OSINT)
# ============================================================================

# Importar o coletor de dados web
try:
    from web_data_collector import WebDataCollector
    logger.info("Módulo web_data_collector carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar web_data_collector: {e}")
    WebDataCollector = None

# Variável global para o coletor de dados web
web_collector = WebDataCollector() if WebDataCollector else None

@app.post("/api/data/collect")
async def start_web_data_collection(target_url: str):
    """Inicia a coleta de dados web (OSINT) no alvo."""
    global web_collector
    
    if not web_collector:
        return {"status": "error", "message": "Módulo de coleta web não carregado."}
    
    logger.info(f"Iniciando coleta de dados web no alvo: {target_url}")
    
    # A coleta é síncrona, idealmente rodaria em um executor
    results = web_collector.collect_data(target_url)
    
    # Enviar os resultados via WebSocket
    await manager.broadcast({
        "type": "web_data_collection_result",
        "data": results
    })
    
    return {"status": "completed", "results": results}

# ============================================================================
# MÓDULO 6: INTEGRAÇÃO MÓVEL (COLETA DE DADOS)
# ============================================================================

# Montar o APIRouter do módulo mobile_integration
if mobile_manager:
    from mobile_integration import router as mobile_router
    app.include_router(mobile_router)
    logger.info("Rotas de Integração Móvel montadas em /api/mobile")

# Importar o explorador SSH
try:
    from exploit_ssh import SSHExploit
    logger.info("Módulo exploit_ssh carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar exploit_ssh: {e}")
    SSHExploit = None

@app.post("/api/exploit/ssh_brute")
async def start_ssh_brute_exploit(target_ip: str, username: str = "root", password_list_str: str = "password,admin,123456"):
    """Inicia um ataque de força bruta SSH contra um alvo."""
    
    if not SSHExploit:
        return {"status": "error", "message": "Módulo de exploração SSH não carregado."}
    
    password_list = password_list_str.split(',')
    exploit = SSHExploit(target_ip, username, password_list)
    
    logger.info(f"Iniciando exploração SSH contra: {target_ip}")
    
    # Executar o ataque em um executor para não bloquear o loop de eventos
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(None, exploit.brute_force_attack)
    
    # Enviar os resultados via WebSocket
    await manager.broadcast({
        "type": "ssh_exploit_result",
        "data": results
    })
    
    return {"status": "completed", "results": results}

# ============================================================================
# MÓDULO 7: OSINT AVANÇADO (theHarvester)
# ============================================================================

# Importar o módulo theHarvester
try:
    from theharvester_module import theharvester_module
    logger.info("Módulo theHarvester carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar theHarvester: {e}")
    theharvester_module = None

@app.post("/api/osint/harvester/run")
async def run_harvester_scan(domain: str, sources: str = "all"):
    """Inicia um scan de OSINT com theHarvester."""
    
    if not theharvester_module:
        return {"status": "error", "message": "Módulo theHarvester não carregado."}
    
    logger.info(f"Iniciando scan theHarvester contra: {domain} com fontes: {sources}")
    
    # Executar o ataque em um executor para não bloquear o loop de eventos
    results = await theharvester_module.run_scan(domain, sources)
    
    # Enviar os resultados via WebSocket
    await manager.broadcast({
        "type": "harvester_result",
        "data": results
    })
    
    return results

# ============================================================================
# MÓDULO 8: EXPLORAÇÃO AVANÇADA (Metasploit RPC)
# ============================================================================

# Importar o módulo Metasploit
try:
    from metasploit_module import metasploit_exploit
    logger.info("Módulo Metasploit carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar Metasploit: {e}")
    metasploit_exploit = None

@app.post("/api/metasploit/connect")
async def connect_metasploit():
    """Tenta conectar ao serviço msfrpcd."""
    if not metasploit_exploit:
        return {"status": "error", "message": "Módulo Metasploit não carregado."}
    
    if metasploit_exploit.connect():
        return {"status": "success", "message": "Conexão com Metasploit RPC estabelecida."}
    else:
        return {"status": "error", "message": "Falha ao conectar ao Metasploit RPC. Verifique se o msfrpcd está rodando."}

@app.post("/api/metasploit/run_auxiliary")
async def run_metasploit_auxiliary(module_name: str, target_host: str, target_port: int, options: dict = None):
    """Inicia um módulo auxiliar do Metasploit (e.g., scanner)."""
    
    if not metasploit_exploit:
        return {"status": "error", "message": "Módulo Metasploit não carregado."}
    
    logger.info(f"Iniciando módulo Metasploit {module_name} contra: {target_host}:{target_port}")
    
    # Executar o módulo
    results = metasploit_exploit.run_auxiliary_module(module_name, target_host, target_port, options)
    
    # Enviar os resultados via WebSocket
    await manager.broadcast({
        "type": "metasploit_result",
        "data": results
    })
    
    return results

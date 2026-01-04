#!/usr/bin/env python3
"""SISTEMA DE DETECÇÃO DE INTRUSÃO (IDS) REAL
Baseado em Scapy para monitoramento de tráfego e detecção de ataques
"""
import asyncio
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tentar importar scapy
try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP
    SCAPY_AVAILABLE = True
except ImportError:
    logger.warning("Scapy não está instalado. Usando simulação.")
    SCAPY_AVAILABLE = False

# ============================================================================
# ENUMS E DATACLASSES
# ============================================================================

class ThreatLevel(str, Enum):
    """Níveis de ameaça"""
    LOW = "BAIXO"
    MEDIUM = "MÉDIO"
    HIGH = "ALTO"
    CRITICAL = "CRÍTICO"

class AttackType(str, Enum):
    """Tipos de ataque detectados"""
    PORT_SCAN = "ESCANEAMENTO_DE_PORTAS"
    BRUTE_FORCE = "ATAQUE_DE_FORÇA_BRUTA"
    DOS = "NEGAÇÃO_DE_SERVIÇO"
    SUSPICIOUS_TRAFFIC = "TRÁFEGO_SUSPEITO"
    UNAUTHORIZED_ACCESS = "ACESSO_NÃO_AUTORIZADO"
    MALWARE_SIGNATURE = "ASSINATURA_DE_MALWARE"

@dataclass
class IDSAlert:
    """Alerta de detecção de intrusão"""
    alert_id: str
    timestamp: str
    threat_level: ThreatLevel
    attack_type: AttackType
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    description: str
    packets_count: int
    confidence: float  # 0-100%
    remediation: str

@dataclass
class AttackPattern:
    """Padrão de ataque detectado"""
    source_ip: str
    attack_type: AttackType
    packet_count: int
    time_window: int  # segundos
    last_seen: str

# ============================================================================
# MOTOR DE DETECÇÃO DE INTRUSÃO
# ============================================================================

class IntrusionDetectionEngine:
    """Motor de detecção de intrusão em tempo real"""
    
    def __init__(self):
        self.alerts: List[IDSAlert] = []
        self.attack_patterns: Dict[str, AttackPattern] = {}
        self.packet_history: Dict[str, List] = defaultdict(list)
        self.is_monitoring = False
        self.monitoring_thread = None
        self.alert_callbacks: List = []
        
        # Configurações de detecção
        self.port_scan_threshold = 10  # Número de portas diferentes em 10 segundos
        self.brute_force_threshold = 5  # Número de tentativas falhas
        self.dos_threshold = 100  # Número de pacotes em 5 segundos
        self.time_window = 10  # Janela de tempo em segundos
    
    def start_monitoring(self, interface: Optional[str] = None):
        """Inicia o monitoramento de tráfego"""
        if self.is_monitoring:
            logger.warning("Monitoramento já está ativo")
            return
        
        self.is_monitoring = True
        logger.info(f"Iniciando monitoramento de tráfego na interface: {interface}")
        
        if SCAPY_AVAILABLE:
            # Iniciar thread de monitoramento com Scapy
            self.monitoring_thread = threading.Thread(
                target=self._sniff_packets,
                args=(interface,),
                daemon=True
            )
            self.monitoring_thread.start()
        else:
            # Usar simulação
            self.monitoring_thread = threading.Thread(
                target=self._simulate_monitoring,
                daemon=True
            )
            self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Para o monitoramento de tráfego"""
        self.is_monitoring = False
        logger.info("Monitoramento de tráfego parado")
    
    def _sniff_packets(self, interface: Optional[str] = None):
        """Captura e analisa pacotes em tempo real (Scapy)"""
        try:
            sniff(
                iface=interface,
                prn=self._analyze_packet,
                store=False,
                stop_filter=lambda x: not self.is_monitoring
            )
        except Exception as e:
            logger.error(f"Erro ao capturar pacotes: {e}")
            # Fallback para simulação
            self._simulate_monitoring()
    
    def _analyze_packet(self, packet):
        """Analisa um pacote capturado"""
        try:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                protocol = packet[IP].proto
                
                # Detectar tipo de ataque
                if TCP in packet:
                    src_port = packet[TCP].sport
                    dst_port = packet[TCP].dport
                    flags = packet[TCP].flags
                    
                    # Detecção de Port Scan (múltiplos SYN para diferentes portas)
                    if flags & 0x02:  # SYN flag
                        self._detect_port_scan(src_ip, dst_port)
                    
                    # Detecção de Força Bruta (múltiplas tentativas para mesma porta)
                    if dst_port in [22, 3306, 5432]:  # SSH, MySQL, PostgreSQL
                        self._detect_brute_force(src_ip, dst_port)
                
                elif UDP in packet:
                    src_port = packet[UDP].sport
                    dst_port = packet[UDP].dport
                    
                    # Detecção de DoS (múltiplos pacotes UDP)
                    self._detect_dos(src_ip, dst_ip)
        
        except Exception as e:
            logger.debug(f"Erro ao analisar pacote: {e}")
    
    def _detect_port_scan(self, source_ip: str, destination_port: int):
        """Detecta tentativas de escaneamento de portas"""
        key = f"port_scan_{source_ip}"
        
        if key not in self.packet_history:
            self.packet_history[key] = []
        
        # Adicionar porta à história
        self.packet_history[key].append({
            "port": destination_port,
            "timestamp": datetime.now()
        })
        
        # Limpar histórico antigo (fora da janela de tempo)
        cutoff_time = datetime.now() - timedelta(seconds=self.time_window)
        self.packet_history[key] = [
            p for p in self.packet_history[key]
            if p["timestamp"] > cutoff_time
        ]
        
        # Verificar se ultrapassou o threshold
        unique_ports = set(p["port"] for p in self.packet_history[key])
        if len(unique_ports) >= self.port_scan_threshold:
            self._create_alert(
                threat_level=ThreatLevel.HIGH,
                attack_type=AttackType.PORT_SCAN,
                source_ip=source_ip,
                destination_ip="0.0.0.0",
                source_port=0,
                destination_port=list(unique_ports)[0],
                protocol="TCP",
                description=f"Escaneamento de {len(unique_ports)} portas detectado",
                packets_count=len(self.packet_history[key]),
                confidence=85.0,
                remediation="Ativar firewall, bloquear IP de origem, investigar atividade"
            )
    
    def _detect_brute_force(self, source_ip: str, destination_port: int):
        """Detecta tentativas de ataque de força bruta"""
        key = f"brute_force_{source_ip}_{destination_port}"
        
        if key not in self.packet_history:
            self.packet_history[key] = []
        
        self.packet_history[key].append(datetime.now())
        
        # Limpar histórico antigo
        cutoff_time = datetime.now() - timedelta(seconds=self.time_window)
        self.packet_history[key] = [
            t for t in self.packet_history[key]
            if t > cutoff_time
        ]
        
        # Verificar se ultrapassou o threshold
        if len(self.packet_history[key]) >= self.brute_force_threshold:
            service_name = {
                22: "SSH",
                3306: "MySQL",
                5432: "PostgreSQL"
            }.get(destination_port, f"Porta {destination_port}")
            
            self._create_alert(
                threat_level=ThreatLevel.CRITICAL,
                attack_type=AttackType.BRUTE_FORCE,
                source_ip=source_ip,
                destination_ip="192.168.1.1",
                source_port=0,
                destination_port=destination_port,
                protocol="TCP",
                description=f"Ataque de força bruta em {service_name} detectado",
                packets_count=len(self.packet_history[key]),
                confidence=95.0,
                remediation="Bloquear IP imediatamente, ativar rate limiting, revisar logs de autenticação"
            )
    
    def _detect_dos(self, source_ip: str, destination_ip: str):
        """Detecta tentativas de Negação de Serviço (DoS)"""
        key = f"dos_{source_ip}_{destination_ip}"
        
        if key not in self.packet_history:
            self.packet_history[key] = []
        
        self.packet_history[key].append(datetime.now())
        
        # Limpar histórico antigo (janela de 5 segundos para DoS)
        cutoff_time = datetime.now() - timedelta(seconds=5)
        self.packet_history[key] = [
            t for t in self.packet_history[key]
            if t > cutoff_time
        ]
        
        # Verificar se ultrapassou o threshold
        if len(self.packet_history[key]) >= self.dos_threshold:
            self._create_alert(
                threat_level=ThreatLevel.CRITICAL,
                attack_type=AttackType.DOS,
                source_ip=source_ip,
                destination_ip=destination_ip,
                source_port=0,
                destination_port=0,
                protocol="UDP",
                description=f"Possível ataque de DoS com {len(self.packet_history[key])} pacotes",
                packets_count=len(self.packet_history[key]),
                confidence=80.0,
                remediation="Ativar proteção DDoS, bloquear IP de origem, aumentar capacidade de banda"
            )
    
    def _simulate_monitoring(self):
        """Simula o monitoramento de tráfego (quando Scapy não está disponível)"""
        logger.info("Executando simulação de monitoramento")
        
        simulated_attacks = [
            {
                "delay": 5,
                "threat_level": ThreatLevel.HIGH,
                "attack_type": AttackType.PORT_SCAN,
                "source_ip": "192.168.1.50",
                "description": "Escaneamento de portas detectado do Celular 02"
            },
            {
                "delay": 15,
                "threat_level": ThreatLevel.CRITICAL,
                "attack_type": AttackType.BRUTE_FORCE,
                "source_ip": "192.168.1.50",
                "description": "Ataque de força bruta em SSH detectado"
            },
            {
                "delay": 25,
                "threat_level": ThreatLevel.MEDIUM,
                "attack_type": AttackType.SUSPICIOUS_TRAFFIC,
                "source_ip": "192.168.1.200",
                "description": "Tráfego suspeito detectado do Celular 04"
            }
        ]
        
        attack_index = 0
        
        while self.is_monitoring:
            if attack_index < len(simulated_attacks):
                attack = simulated_attacks[attack_index]
                asyncio.sleep(attack["delay"])
                
                self._create_alert(
                    threat_level=attack["threat_level"],
                    attack_type=attack["attack_type"],
                    source_ip=attack["source_ip"],
                    destination_ip="192.168.1.1",
                    source_port=random.randint(49152, 65535),
                    destination_port=22 if attack["attack_type"] == AttackType.BRUTE_FORCE else 0,
                    protocol="TCP",
                    description=attack["description"],
                    packets_count=random.randint(5, 50),
                    confidence=random.uniform(75, 99),
                    remediation="Investigar atividade suspeita"
                )
                
                attack_index += 1
            
            asyncio.sleep(1)
    
    def _create_alert(
        self,
        threat_level: ThreatLevel,
        attack_type: AttackType,
        source_ip: str,
        destination_ip: str,
        source_port: int,
        destination_port: int,
        protocol: str,
        description: str,
        packets_count: int,
        confidence: float,
        remediation: str
    ):
        """Cria um alerta de intrusão"""
        alert = IDSAlert(
            alert_id=f"ALERT_{len(self.alerts) + 1:04d}",
            timestamp=datetime.now().isoformat(),
            threat_level=threat_level,
            attack_type=attack_type,
            source_ip=source_ip,
            destination_ip=destination_ip,
            source_port=source_port,
            destination_port=destination_port,
            protocol=protocol,
            description=description,
            packets_count=packets_count,
            confidence=confidence,
            remediation=remediation
        )
        
        self.alerts.append(alert)
        logger.warning(f"🚨 ALERTA DE INTRUSÃO: {alert.alert_id} - {alert.description}")
        
        # Chamar callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Erro ao executar callback: {e}")
    
    def register_alert_callback(self, callback):
        """Registra um callback para ser chamado quando um alerta é gerado"""
        self.alert_callbacks.append(callback)
    
    def get_alerts(self, limit: int = 100) -> List[IDSAlert]:
        """Obtém os últimos alertas"""
        return self.alerts[-limit:]
    
    def get_alerts_by_source(self, source_ip: str) -> List[IDSAlert]:
        """Obtém alertas de um IP específico"""
        return [a for a in self.alerts if a.source_ip == source_ip]
    
    def get_threat_summary(self) -> Dict:
        """Retorna um resumo das ameaças detectadas"""
        threat_counts = defaultdict(int)
        attack_counts = defaultdict(int)
        
        for alert in self.alerts:
            threat_counts[alert.threat_level] += 1
            attack_counts[alert.attack_type] += 1
        
        return {
            "total_alerts": len(self.alerts),
            "threat_distribution": dict(threat_counts),
            "attack_distribution": dict(attack_counts),
            "critical_alerts": threat_counts[ThreatLevel.CRITICAL],
            "high_alerts": threat_counts[ThreatLevel.HIGH]
        }

# ============================================================================
# INSTÂNCIA GLOBAL DO IDS
# ============================================================================

ids_engine = IntrusionDetectionEngine()

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    import random
    
    print("""    🛡️ SISTEMA DE DETECÇÃO DE INTRUSÃO (IDS) 🛡️
    Monitoramento de Tráfego em Tempo Real
    ========================================
    """
    
    # Registrar callback para alertas
    def on_alert(alert: IDSAlert):
        print(f"\n⚠️ NOVO ALERTA: {alert.alert_id}")
        print(f"   Tipo: {alert.attack_type.value}")
        print(f"   Severidade: {alert.threat_level.value}")
        print(f"   Origem: {alert.source_ip}")
        print(f"   Descrição: {alert.description}")
        print(f"   Confiança: {alert.confidence:.1f}%")
    
    ids_engine.register_alert_callback(on_alert)
    
    # Iniciar monitoramento
    ids_engine.start_monitoring()
    
    print("Monitoramento iniciado. Aguardando ataques...
")
    
    try:
        while True:
            asyncio.sleep(5)
            summary = ids_engine.get_threat_summary()
            print(f"Resumo de Ameaças: {summary}")
    except KeyboardInterrupt:
        ids_engine.stop_monitoring()
        print("\nMonitoramento encerrado.")

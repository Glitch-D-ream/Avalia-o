#!/usr/bin/env python3
"""MÓDULO DE ANÁLISE AVANÇADA DE TRÁFEGO
Categorização de Protocolos, Geo-IP Simulado e Análise de Padrões
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import json

@dataclass
class Packet:
    """Representação de um pacote de rede"""
    timestamp: str
    src_ip: str
    dst_ip: str
    protocol: str
    port: int
    size: int
    payload: str = ""

class ProtocolAnalyzer:
    """Analisa e categoriza protocolos de rede"""
    
    PROTOCOL_MAPPING = {
        80: "HTTP",
        443: "HTTPS",
        53: "DNS",
        22: "SSH",
        21: "FTP",
        25: "SMTP",
        110: "POP3",
        143: "IMAP",
        3306: "MySQL",
        5432: "PostgreSQL",
        6379: "Redis",
        27017: "MongoDB"
    }
    
    @staticmethod
    def identify_protocol(port: int, payload: str = "") -> str:
        """Identifica o protocolo baseado na porta e payload"""
        if port in ProtocolAnalyzer.PROTOCOL_MAPPING:
            return ProtocolAnalyzer.PROTOCOL_MAPPING[port]
        
        # Análise de payload para detecção mais precisa
        if payload:
            if b"HTTP" in payload.encode() or b"GET" in payload.encode():
                return "HTTP"
            elif b"TLS" in payload.encode() or b"SSL" in payload.encode():
                return "HTTPS"
            elif b"DNS" in payload.encode():
                return "DNS"
        
        return "Unknown"

class GeoIPSimulator:
    """Simula mapeamento Geo-IP para fins educacionais"""
    
    GEO_DATABASE = {
        "8.8.8.8": {"country": "USA", "city": "Mountain View", "lat": 37.4220, "lon": -122.0841},
        "1.1.1.1": {"country": "USA", "city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
        "208.67.222.222": {"country": "USA", "city": "San Francisco", "lat": 37.7749, "lon": -122.4194},
        "9.9.9.9": {"country": "USA", "city": "New York", "lat": 40.7128, "lon": -74.0060},
        "192.168.1.1": {"country": "Rede Local", "city": "Laboratório", "lat": 0, "lon": 0},
        "192.168.1.10": {"country": "Rede Local", "city": "Laboratório", "lat": 0, "lon": 0},
        "192.168.1.50": {"country": "Rede Local", "city": "Laboratório", "lat": 0, "lon": 0},
        "192.168.1.200": {"country": "Rede Local", "city": "Laboratório", "lat": 0, "lon": 0},
    }
    
    @staticmethod
    def get_location(ip: str) -> Dict:
        """Obtém localização simulada de um IP"""
        if ip in GeoIPSimulator.GEO_DATABASE:
            return GeoIPSimulator.GEO_DATABASE[ip]
        
        # Simular localização aleatória para IPs desconhecidos
        return {
            "country": "Desconhecido",
            "city": "Desconhecido",
            "lat": 0,
            "lon": 0
        }

class TrafficPatternAnalyzer:
    """Analisa padrões de tráfego para detecção de anomalias"""
    
    def __init__(self):
        self.traffic_history: List[Packet] = []
        self.anomalies: List[Dict] = []
    
    def add_packet(self, packet: Packet):
        """Adiciona um pacote ao histórico"""
        self.traffic_history.append(packet)
        self._detect_anomalies(packet)
    
    def _detect_anomalies(self, packet: Packet):
        """Detecta anomalias no tráfego"""
        anomalies = []
        
        # Anomalia 1: Tráfego HTTP em texto plano
        if packet.protocol == "HTTP":
            anomalies.append({
                "type": "UNENCRYPTED_TRAFFIC",
                "severity": "ALTO",
                "description": f"Tráfego HTTP em texto plano detectado de {packet.src_ip}",
                "recommendation": "Use HTTPS para criptografar dados"
            })
        
        # Anomalia 2: Múltiplas conexões para a mesma porta (possível força bruta)
        same_port_count = sum(1 for p in self.traffic_history if p.port == packet.port)
        if same_port_count > 10:
            anomalies.append({
                "type": "BRUTE_FORCE_ATTEMPT",
                "severity": "CRÍTICO",
                "description": f"Múltiplas tentativas de conexão na porta {packet.port}",
                "recommendation": "Implementar rate limiting e autenticação forte"
            })
        
        # Anomalia 3: Tráfego DNS suspeito
        if packet.protocol == "DNS" and packet.size > 512:
            anomalies.append({
                "type": "DNS_AMPLIFICATION",
                "severity": "MÉDIO",
                "description": "Possível ataque de amplificação DNS detectado",
                "recommendation": "Configurar firewall para filtrar DNS suspeito"
            })
        
        self.anomalies.extend(anomalies)
    
    def get_traffic_summary(self) -> Dict:
        """Retorna um resumo do tráfego"""
        protocol_count = {}
        total_size = 0
        
        for packet in self.traffic_history:
            protocol_count[packet.protocol] = protocol_count.get(packet.protocol, 0) + 1
            total_size += packet.size
        
        return {
            "total_packets": len(self.traffic_history),
            "total_data": f"{total_size / 1024:.2f} KB",
            "protocol_distribution": protocol_count,
            "anomalies_detected": len(self.anomalies)
        }

class AdvancedTrafficReport:
    """Gera relatórios detalhados de tráfego"""
    
    @staticmethod
    def generate_report(packets: List[Packet], anomalies: List[Dict]) -> Dict:
        """Gera um relatório completo de tráfego"""
        
        # Análise de protocolos
        protocol_analyzer = ProtocolAnalyzer()
        protocol_distribution = {}
        
        for packet in packets:
            protocol = protocol_analyzer.identify_protocol(packet.port, packet.payload)
            protocol_distribution[protocol] = protocol_distribution.get(protocol, 0) + 1
        
        # Análise de Geo-IP
        geoip_simulator = GeoIPSimulator()
        destination_locations = {}
        
        for packet in packets:
            location = geoip_simulator.get_location(packet.dst_ip)
            country = location["country"]
            destination_locations[country] = destination_locations.get(country, 0) + 1
        
        # Compilar relatório
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_packets": len(packets),
                "total_anomalies": len(anomalies),
                "protocol_distribution": protocol_distribution,
                "destination_locations": destination_locations
            },
            "anomalies": anomalies,
            "recommendations": AdvancedTrafficReport._generate_recommendations(anomalies)
        }
        
        return report
    
    @staticmethod
    def _generate_recommendations(anomalies: List[Dict]) -> List[str]:
        """Gera recomendações baseadas nas anomalias detectadas"""
        recommendations = []
        
        if any(a["type"] == "UNENCRYPTED_TRAFFIC" for a in anomalies):
            recommendations.append("✅ Implementar HTTPS em todos os serviços web")
        
        if any(a["type"] == "BRUTE_FORCE_ATTEMPT" for a in anomalies):
            recommendations.append("✅ Configurar rate limiting e autenticação forte")
        
        if any(a["type"] == "DNS_AMPLIFICATION" for a in anomalies):
            recommendations.append("✅ Filtrar DNS suspeito no firewall")
        
        if not recommendations:
            recommendations.append("✅ Nenhuma anomalia crítica detectada. Continue monitorando.")
        
        return recommendations

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Criar analisador de padrões
    analyzer = TrafficPatternAnalyzer()
    
    # Simular pacotes
    packets = [
        Packet(
            timestamp=datetime.now().isoformat(),
            src_ip="192.168.1.200",
            dst_ip="8.8.8.8",
            protocol="HTTP",
            port=80,
            size=1024,
            payload="GET / HTTP/1.1"
        ),
        Packet(
            timestamp=datetime.now().isoformat(),
            src_ip="192.168.1.200",
            dst_ip="1.1.1.1",
            protocol="HTTPS",
            port=443,
            size=2048,
            payload="TLS Handshake"
        ),
        Packet(
            timestamp=datetime.now().isoformat(),
            src_ip="192.168.1.200",
            dst_ip="8.8.8.8",
            protocol="DNS",
            port=53,
            size=512,
            payload="DNS Query"
        )
    ]
    
    # Adicionar pacotes ao analisador
    for packet in packets:
        analyzer.add_packet(packet)
    
    # Gerar relatório
    report = AdvancedTrafficReport.generate_report(packets, analyzer.anomalies)
    
    print(json.dumps(report, indent=2, default=str))

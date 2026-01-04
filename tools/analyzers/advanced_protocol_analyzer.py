#!/usr/bin/env python3
"""MÓDULO ADVANCED PROTOCOL ANALYZER (APA)
Ferramenta "Cinzenta" de Análise Profunda de Protocolos
Análise de comportamento de protocolos em nível de aplicação
"""
import logging
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS E DATACLASSES
# ============================================================================

class ProtocolType(str, Enum):
    """Tipos de protocolo identificados"""
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    FTP = "FTP"
    SSH = "SSH"
    SMTP = "SMTP"
    POP3 = "POP3"
    IMAP = "IMAP"
    DNS = "DNS"
    TELNET = "TELNET"
    UNKNOWN = "UNKNOWN"

class RiskLevel(str, Enum):
    """Nível de risco de um protocolo"""
    CRITICAL = "CRITICAL"  # Sem encriptação, transmite credenciais
    HIGH = "HIGH"  # Encriptação fraca ou vulnerável
    MEDIUM = "MEDIUM"  # Encriptação moderna mas com possíveis falhas
    LOW = "LOW"  # Encriptação forte e bem implementada
    SECURE = "SECURE"  # Encriptação forte com proteções adicionais

@dataclass
class ProtocolSignature:
    """Assinatura de um protocolo identificado"""
    protocol: ProtocolType
    port: int
    banner: str
    confidence: float  # 0-100%
    risk_level: RiskLevel
    vulnerability_count: int
    details: Dict

@dataclass
class ProtocolAnalysisResult:
    """Resultado da análise de um protocolo"""
    timestamp: str
    source_ip: str
    destination_ip: str
    destination_port: int
    protocol: ProtocolType
    risk_level: RiskLevel
    vulnerabilities: List[str]
    recommendations: List[str]
    payload_hash: str
    payload_size: int
    encryption_detected: bool
    authentication_detected: bool

# ============================================================================
# ANALISADOR AVANÇADO DE PROTOCOLOS
# ============================================================================

class AdvancedProtocolAnalyzer:
    """Analisador avançado de protocolos de aplicação"""
    
    def __init__(self):
        self.protocol_signatures = self._load_signatures()
        self.vulnerability_database = self._load_vulnerabilities()
        self.analysis_history = []
    
    def _load_signatures(self) -> Dict[ProtocolType, Dict]:
        """Carrega assinaturas de protocolos conhecidos"""
        return {
            ProtocolType.HTTP: {
                "ports": [80, 8080, 8000],
                "keywords": ["GET", "POST", "HTTP/", "Content-Type"],
                "risk": RiskLevel.CRITICAL,
                "description": "HTTP sem encriptação - Transmite dados em texto plano"
            },
            ProtocolType.HTTPS: {
                "ports": [443, 8443],
                "keywords": ["TLS", "SSL", "Certificate"],
                "risk": RiskLevel.MEDIUM,
                "description": "HTTPS com encriptação TLS/SSL"
            },
            ProtocolType.FTP: {
                "ports": [21],
                "keywords": ["220", "USER", "PASS", "FTP"],
                "risk": RiskLevel.CRITICAL,
                "description": "FTP sem encriptação - Credenciais transmitidas em texto plano"
            },
            ProtocolType.SSH: {
                "ports": [22],
                "keywords": ["SSH-2.0", "OpenSSH", "PuTTY"],
                "risk": RiskLevel.LOW,
                "description": "SSH com encriptação forte"
            },
            ProtocolType.SMTP: {
                "ports": [25, 587, 465],
                "keywords": ["220", "SMTP", "MAIL FROM"],
                "risk": RiskLevel.HIGH,
                "description": "SMTP - Email sem encriptação (ou com encriptação opcional)"
            },
            ProtocolType.DNS: {
                "ports": [53],
                "keywords": ["DNS", "Query", "Response"],
                "risk": RiskLevel.HIGH,
                "description": "DNS sem encriptação - Permite DNS Spoofing"
            },
            ProtocolType.TELNET: {
                "ports": [23],
                "keywords": ["telnet", "login", "password"],
                "risk": RiskLevel.CRITICAL,
                "description": "TELNET sem encriptação - Extremamente inseguro"
            }
        }
    
    def _load_vulnerabilities(self) -> Dict[ProtocolType, List[str]]:
        """Carrega banco de dados de vulnerabilidades conhecidas"""
        return {
            ProtocolType.HTTP: [
                "CVE-2019-11358: jQuery vulnerability",
                "MITM Attack: Sem encriptação, dados podem ser interceptados",
                "Session Hijacking: Cookies transmitidos em texto plano",
                "Credential Exposure: Senhas transmitidas em texto plano"
            ],
            ProtocolType.HTTPS: [
                "CVE-2014-0160: Heartbleed (OpenSSL)",
                "SSL Strip Attack: Downgrade de HTTPS para HTTP",
                "Certificate Pinning Bypass: Em alguns navegadores",
                "HSTS Bypass: Se HSTS não estiver ativado"
            ],
            ProtocolType.FTP: [
                "Credential Exposure: Usuário e senha em texto plano",
                "MITM Attack: Dados transferidos sem encriptação",
                "Brute Force: Fácil de atacar com força bruta",
                "Port Scanning: Porta 21 é facilmente identificável"
            ],
            ProtocolType.SSH: [
                "Weak Key Exchange: Se configurado com algoritmos antigos",
                "Brute Force: Possível com senhas fracas",
                "Key Reuse: Risco se a chave privada for comprometida"
            ],
            ProtocolType.DNS: [
                "DNS Spoofing: Sem DNSSEC, respostas podem ser falsificadas",
                "DNS Hijacking: Redirecionamento para sites maliciosos",
                "DNS Leak: Vazamento de consultas DNS em VPN"
            ],
            ProtocolType.TELNET: [
                "Credential Exposure: Credenciais em texto plano",
                "MITM Attack: Todos os dados em texto plano",
                "Session Hijacking: Fácil de sequestrar sessões",
                "Port Scanning: Porta 23 é facilmente identificável"
            ]
        }
    
    def analyze_payload(self, payload: bytes, source_ip: str, dest_ip: str, dest_port: int) -> Optional[ProtocolAnalysisResult]:
        """Analisa um payload para identificar o protocolo e vulnerabilidades"""
        
        try:
            # Tentar decodificar o payload como texto
            payload_str = payload.decode('utf-8', errors='ignore')
        except Exception:
            payload_str = ""
        
        # Identificar o protocolo
        protocol, confidence = self._identify_protocol(payload_str, dest_port)
        
        # Obter informações do protocolo
        protocol_info = self.protocol_signatures.get(protocol, {})
        risk_level = protocol_info.get("risk", RiskLevel.UNKNOWN)
        
        # Detectar encriptação e autenticação
        encryption_detected = self._detect_encryption(payload_str)
        authentication_detected = self._detect_authentication(payload_str, protocol)
        
        # Obter vulnerabilidades
        vulnerabilities = self.vulnerability_database.get(protocol, [])
        
        # Gerar recomendações
        recommendations = self._generate_recommendations(protocol, risk_level)
        
        # Calcular hash do payload
        payload_hash = hashlib.sha256(payload).hexdigest()[:16]
        
        result = ProtocolAnalysisResult(
            timestamp=datetime.now().isoformat(),
            source_ip=source_ip,
            destination_ip=dest_ip,
            destination_port=dest_port,
            protocol=protocol,
            risk_level=risk_level,
            vulnerabilities=vulnerabilities[:3],  # Top 3 vulnerabilidades
            recommendations=recommendations,
            payload_hash=payload_hash,
            payload_size=len(payload),
            encryption_detected=encryption_detected,
            authentication_detected=authentication_detected
        )
        
        self.analysis_history.append(result)
        return result
    
    def _identify_protocol(self, payload: str, port: int) -> Tuple[ProtocolType, float]:
        """Identifica o protocolo baseado no payload e porta"""
        
        # Verificar por assinaturas conhecidas
        for protocol, sig in self.protocol_signatures.items():
            # Verificar porta
            if port in sig.get("ports", []):
                return protocol, 95.0
            
            # Verificar keywords
            keywords = sig.get("keywords", [])
            matches = sum(1 for kw in keywords if kw.lower() in payload.lower())
            
            if matches >= 2:
                confidence = min(90.0, 50.0 + (matches * 10))
                return protocol, confidence
        
        # Se nenhum protocolo foi identificado, retornar UNKNOWN
        return ProtocolType.UNKNOWN, 0.0
    
    def _detect_encryption(self, payload: str) -> bool:
        """Detecta se o payload contém dados encriptados"""
        
        # Verificar por indicadores de encriptação
        encryption_indicators = [
            "TLS", "SSL", "HTTPS", "SSH-2.0", "Certificate",
            "BEGIN CERTIFICATE", "END CERTIFICATE", "ENCRYPTED"
        ]
        
        for indicator in encryption_indicators:
            if indicator.lower() in payload.lower():
                return True
        
        # Verificar se o payload é binário (possível encriptação)
        non_ascii_count = sum(1 for c in payload if ord(c) > 127)
        if non_ascii_count > len(payload) * 0.3:
            return True
        
        return False
    
    def _detect_authentication(self, payload: str, protocol: ProtocolType) -> bool:
        """Detecta se o payload contém mecanismos de autenticação"""
        
        auth_keywords = [
            "USER", "PASS", "PASSWORD", "AUTH", "LOGIN", "AUTHENTICATE",
            "Authorization", "Bearer", "Basic", "Digest", "OAuth"
        ]
        
        for keyword in auth_keywords:
            if keyword.lower() in payload.lower():
                return True
        
        return False
    
    def _generate_recommendations(self, protocol: ProtocolType, risk_level: RiskLevel) -> List[str]:
        """Gera recomendações baseadas no protocolo e nível de risco"""
        
        recommendations = []
        
        if risk_level == RiskLevel.CRITICAL:
            recommendations.append(f"⚠️ CRÍTICO: {protocol.value} é extremamente inseguro. Migre para uma alternativa segura imediatamente.")
        elif risk_level == RiskLevel.HIGH:
            recommendations.append(f"⚠️ ALTO RISCO: {protocol.value} possui vulnerabilidades conhecidas. Considere usar uma alternativa mais segura.")
        elif risk_level == RiskLevel.MEDIUM:
            recommendations.append(f"⚠️ MÉDIO RISCO: {protocol.value} pode ser vulnerável a certos ataques. Mantenha o software atualizado.")
        
        # Recomendações específicas por protocolo
        if protocol == ProtocolType.HTTP:
            recommendations.append("✓ Use HTTPS em vez de HTTP")
            recommendations.append("✓ Ative HSTS (HTTP Strict Transport Security)")
            recommendations.append("✓ Implemente Certificate Pinning")
        elif protocol == ProtocolType.FTP:
            recommendations.append("✓ Use SFTP (SSH File Transfer Protocol) em vez de FTP")
            recommendations.append("✓ Use FTPS (FTP sobre SSL/TLS)")
        elif protocol == ProtocolType.TELNET:
            recommendations.append("✓ Use SSH em vez de TELNET")
            recommendations.append("✓ Desative o TELNET completamente")
        elif protocol == ProtocolType.DNS:
            recommendations.append("✓ Implemente DNSSEC")
            recommendations.append("✓ Use DNS sobre HTTPS (DoH)")
            recommendations.append("✓ Use DNS sobre TLS (DoT)")
        
        return recommendations
    
    def get_analysis_report(self) -> Dict:
        """Gera um relatório de análise completo"""
        
        if not self.analysis_history:
            return {"error": "Nenhuma análise realizada ainda"}
        
        # Contar protocolos
        protocol_counts = {}
        risk_counts = {}
        
        for analysis in self.analysis_history:
            protocol = analysis.protocol.value
            risk = analysis.risk_level.value
            
            protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        # Calcular estatísticas
        total_analyses = len(self.analysis_history)
        critical_count = risk_counts.get(RiskLevel.CRITICAL.value, 0)
        high_count = risk_counts.get(RiskLevel.HIGH.value, 0)
        
        return {
            "total_analyses": total_analyses,
            "protocol_distribution": protocol_counts,
            "risk_distribution": risk_counts,
            "critical_findings": critical_count,
            "high_findings": high_count,
            "average_payload_size": sum(a.payload_size for a in self.analysis_history) // total_analyses if total_analyses > 0 else 0,
            "encryption_percentage": (sum(1 for a in self.analysis_history if a.encryption_detected) / total_analyses * 100) if total_analyses > 0 else 0
        }

# ============================================================================
# INSTÂNCIA GLOBAL
# ============================================================================

protocol_analyzer = AdvancedProtocolAnalyzer()

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""    🔬 ADVANCED PROTOCOL ANALYZER (APA) 🔬
    Ferramenta "Cinzenta" de Análise Profunda de Protocolos
    ======================================================
    """
    
    # Exemplo 1: Análise de HTTP
    print("\n[1] Analisando HTTP (Inseguro)...")
    http_payload = b"GET / HTTP/1.1\r\nHost: example.com\r
Authorization: Basic dXNlcjpwYXNz\r
"    result = protocol_analyzer.analyze_payload(http_payload, "192.168.1.200", "192.168.1.1", 80)
    
    if result:
        print(f"  Protocolo: {result.protocol.value}")
        print(f"  Nível de Risco: {result.risk_level.value}")
        print(f"  Encriptação: {'Sim' if result.encryption_detected else 'Não'}")
        print(f"  Autenticação: {'Sim' if result.authentication_detected else 'Não'}")
        print(f"  Vulnerabilidades: {len(result.vulnerabilities)}")
        print(f"  Recomendações:")
        for rec in result.recommendations[:2]:
            print(f"    - {rec}")
    
    # Exemplo 2: Análise de HTTPS
    print("\n[2] Analisando HTTPS (Seguro)...")
    https_payload = b"TLS 1.2 Handshake\x16\x03\x01\x00\x4a\x01\x00\x00\x46\x03\x03"
    result = protocol_analyzer.analyze_payload(https_payload, "192.168.1.200", "192.168.1.1", 443)
    
    if result:
        print(f"  Protocolo: {result.protocol.value}")
        print(f"  Nível de Risco: {result.risk_level.value}")
        print(f"  Encriptação: {'Sim' if result.encryption_detected else 'Não'}")
    
    # Relatório final
    print("\n[3] Relatório de Análise:")
    report = protocol_analyzer.get_analysis_report()
    print(f"  Total de Análises: {report['total_analyses']}")
    print(f"  Achados Críticos: {report['critical_findings']}")
    print(f"  Achados de Alto Risco: {report['high_findings']}")
    print(f"  Percentual de Encriptação: {report['encryption_percentage']:.1f}%")

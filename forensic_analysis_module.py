#!/usr/bin/env python3
"""MÓDULO DE ANÁLISE FORENSE REAL
Análise de Artefatos de Rede Capturados Durante Ataques MITM
Equivalente educacional a ferramentas como Volatility Framework
"""
import logging
import hashlib
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import base64
import urllib.parse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS E DATACLASSES
# ============================================================================

class ArtifactType(str, Enum):
    """Tipos de artefatos de rede"""
    HTTP_COOKIE = "HTTP_COOKIE"
    HTTP_HEADER = "HTTP_HEADER"
    HTTP_BODY = "HTTP_BODY"
    CREDENTIALS = "CREDENTIALS"
    SESSION_TOKEN = "SESSION_TOKEN"
    CACHE_DATA = "CACHE_DATA"
    DNS_QUERY = "DNS_QUERY"
    TLS_CERTIFICATE = "TLS_CERTIFICATE"
    ENCRYPTION_KEY = "ENCRYPTION_KEY"

class ForensicSeverity(str, Enum):
    """Nível de severidade de um artefato forense"""
    CRITICAL = "CRITICAL"  # Credenciais, chaves de encriptação
    HIGH = "HIGH"  # Tokens de sessão, dados sensíveis
    MEDIUM = "MEDIUM"  # Dados de navegação, metadados
    LOW = "LOW"  # Informações públicas, logs

@dataclass
class NetworkArtifact:
    """Artefato de rede capturado"""
    timestamp: str
    artifact_type: ArtifactType
    source_ip: str
    destination_ip: str
    destination_host: str
    artifact_value: str
    artifact_hash: str
    severity: ForensicSeverity
    interpretation: str
    exploitation_risk: str
    mitigation: str

@dataclass
class ForensicSession:
    """Sessão de análise forense"""
    session_id: str
    start_time: str
    artifacts: List[NetworkArtifact]
    total_artifacts: int
    critical_findings: int
    high_findings: int
    evidence_summary: Dict

# ============================================================================
# ANALISADOR FORENSE
# ============================================================================

class ForensicAnalyzer:
    """Analisador forense de artefatos de rede capturados"""
    
    def __init__(self):
        self.forensic_sessions = {}
        self.artifact_patterns = self._load_patterns()
        self.known_cookies = self._load_known_cookies()
    
    def _load_patterns(self) -> Dict[ArtifactType, Dict]:
        """Carrega padrões de detecção de artefatos"""
        return {
            ArtifactType.HTTP_COOKIE: {
                "pattern": r"Set-Cookie:\s*([^;]+)",
                "keywords": ["session", "auth", "token", "user"],
                "severity": ForensicSeverity.HIGH
            },
            ArtifactType.SESSION_TOKEN: {
                "pattern": r"(Bearer|Authorization):\s*([^\s]+)",
                "keywords": ["bearer", "jwt", "oauth"],
                "severity": ForensicSeverity.CRITICAL
            },
            ArtifactType.CREDENTIALS: {
                "pattern": r"(username|password|user|pass)=([^&\s]+)",
                "keywords": ["login", "auth", "credential"],
                "severity": ForensicSeverity.CRITICAL
            },
            ArtifactType.DNS_QUERY: {
                "pattern": r"(DNS|query):\s*([^\s]+)",
                "keywords": ["dns", "query", "resolve"],
                "severity": ForensicSeverity.MEDIUM
            }
        }
    
    def _load_known_cookies(self) -> Dict[str, Dict]:
        """Carrega banco de dados de cookies conhecidos"""
        return {
            "PHPSESSID": {"app": "PHP", "risk": "HIGH"},
            "JSESSIONID": {"app": "Java", "risk": "HIGH"},
            "ASPSESSIONID": {"app": "ASP.NET", "risk": "HIGH"},
            "session_id": {"app": "Generic", "risk": "HIGH"},
            "_ga": {"app": "Google Analytics", "risk": "LOW"},
            "_fbp": {"app": "Facebook Pixel", "risk": "LOW"},
            "csrf_token": {"app": "CSRF Protection", "risk": "MEDIUM"}
        }
    
    def create_forensic_session(self, session_id: str) -> ForensicSession:
        """Cria uma nova sessão de análise forense"""
        session = ForensicSession(
            session_id=session_id,
            start_time=datetime.now().isoformat(),
            artifacts=[],
            total_artifacts=0,
            critical_findings=0,
            high_findings=0,
            evidence_summary={}
        )
        
        self.forensic_sessions[session_id] = session
        logger.info(f"Sessão forense criada: {session_id}")
        return session
    
    def analyze_http_payload(
        self,
        session_id: str,
        payload: bytes,
        source_ip: str,
        destination_ip: str,
        destination_host: str
    ) -> List[NetworkArtifact]:
        """Analisa um payload HTTP para extrair artefatos forenses"""
        
        if session_id not in self.forensic_sessions:
            self.create_forensic_session(session_id)
        
        artifacts = []
        
        try:
            payload_str = payload.decode('utf-8', errors='ignore')
        except Exception:
            payload_str = ""
        
        # Extrair cookies
        cookies = self._extract_cookies(payload_str, source_ip, destination_ip, destination_host)
        artifacts.extend(cookies)
        
        # Extrair tokens de sessão
        tokens = self._extract_session_tokens(payload_str, source_ip, destination_ip, destination_host)
        artifacts.extend(tokens)
        
        # Extrair credenciais
        credentials = self._extract_credentials(payload_str, source_ip, destination_ip, destination_host)
        artifacts.extend(credentials)
        
        # Extrair headers HTTP
        headers = self._extract_http_headers(payload_str, source_ip, destination_ip, destination_host)
        artifacts.extend(headers)
        
        # Adicionar à sessão
        for artifact in artifacts:
            self.forensic_sessions[session_id].artifacts.append(artifact)
            
            if artifact.severity == ForensicSeverity.CRITICAL:
                self.forensic_sessions[session_id].critical_findings += 1
            elif artifact.severity == ForensicSeverity.HIGH:
                self.forensic_sessions[session_id].high_findings += 1
        
        self.forensic_sessions[session_id].total_artifacts = len(self.forensic_sessions[session_id].artifacts)
        
        return artifacts
    
    def _extract_cookies(
        self,
        payload: str,
        source_ip: str,
        destination_ip: str,
        destination_host: str
    ) -> List[NetworkArtifact]:
        """Extrai cookies HTTP do payload"""
        
        artifacts = []
        
        # Padrão para Set-Cookie
        cookie_pattern = r"Set-Cookie:\s*([^;]+)"
        matches = re.findall(cookie_pattern, payload, re.IGNORECASE)
        
        for match in matches:
            cookie_name = match.split('=')[0].strip()
            cookie_value = match.split('=')[1].strip() if '=' in match else ""
            
            # Verificar se é um cookie conhecido
            known_cookie = self.known_cookies.get(cookie_name, {})
            risk = known_cookie.get("risk", "MEDIUM")
            app = known_cookie.get("app", "Unknown")
            
            severity = ForensicSeverity.HIGH if risk == "HIGH" else ForensicSeverity.MEDIUM
            
            artifact = NetworkArtifact(
                timestamp=datetime.now().isoformat(),
                artifact_type=ArtifactType.HTTP_COOKIE,
                source_ip=source_ip,
                destination_ip=destination_ip,
                destination_host=destination_host,
                artifact_value=f"{cookie_name}={cookie_value}",
                artifact_hash=hashlib.sha256(f"{cookie_name}={cookie_value}".encode()).hexdigest()[:16],
                severity=severity,
                interpretation=f"Cookie de {app}. Valor: {cookie_value[:20]}...",
                exploitation_risk=f"Um atacante pode usar este cookie para sequestrar a sessão do usuário.",
                mitigation=f"Ativar flags 'Secure' e 'HttpOnly' no cookie {cookie_name}. Implementar SameSite."
            )
            
            artifacts.append(artifact)
        
        return artifacts
    
    def _extract_session_tokens(
        self,
        payload: str,
        source_ip: str,
        destination_ip: str,
        destination_host: str
    ) -> List[NetworkArtifact]:
        """Extrai tokens de sessão (Bearer, JWT, etc.)"""
        
        artifacts = []
        
        # Padrão para Bearer tokens
        token_pattern = r"(Authorization|Bearer):\s*([^\s\r\n]+)"
        matches = re.findall(token_pattern, payload, re.IGNORECASE)
        
        for match in matches:
            token_type = match[0]
            token_value = match[1]
            
            # Tentar decodificar JWT
            is_jwt = self._is_jwt(token_value)
            jwt_payload = self._decode_jwt(token_value) if is_jwt else None
            
            severity = ForensicSeverity.CRITICAL
            
            artifact = NetworkArtifact(
                timestamp=datetime.now().isoformat(),
                artifact_type=ArtifactType.SESSION_TOKEN,
                source_ip=source_ip,
                destination_ip=destination_ip,
                destination_host=destination_host,
                artifact_value=token_value,
                artifact_hash=hashlib.sha256(token_value.encode()).hexdigest()[:16],
                severity=severity,
                interpretation=f"Token {token_type} capturado. {'JWT identificado.' if is_jwt else 'Token opaco.'} Valor: {token_value[:30]}...",
                exploitation_risk=f"Um atacante pode usar este token para impersonar o usuário e acessar recursos protegidos.",
                mitigation=f"Implementar token rotation. Usar short-lived tokens. Implementar refresh tokens com validade longa."
            )
            
            artifacts.append(artifact)
        
        return artifacts
    
    def _extract_credentials(
        self,
        payload: str,
        source_ip: str,
        destination_ip: str,
        destination_host: str
    ) -> List[NetworkArtifact]:
        """Extrai credenciais (usuário/senha) do payload"""
        
        artifacts = []
        
        # Padrão para credenciais em URL encoding
        cred_pattern = r"(username|user|login|email)=([^&\s]+)&?(password|pass|pwd)=([^&\s]+)"
        matches = re.findall(cred_pattern, payload, re.IGNORECASE)
        
        for match in matches:
            username = urllib.parse.unquote(match[1])
            password = urllib.parse.unquote(match[3])
            
            severity = ForensicSeverity.CRITICAL
            
            artifact = NetworkArtifact(
                timestamp=datetime.now().isoformat(),
                artifact_type=ArtifactType.CREDENTIALS,
                source_ip=source_ip,
                destination_ip=destination_ip,
                destination_host=destination_host,
                artifact_value=f"{username}:{password}",
                artifact_hash=hashlib.sha256(f"{username}:{password}".encode()).hexdigest()[:16],
                severity=severity,
                interpretation=f"Credenciais capturadas em texto plano. Usuário: {username}",
                exploitation_risk=f"Um atacante pode usar estas credenciais para acessar a conta do usuário e todos os seus dados.",
                mitigation=f"Sempre transmitir credenciais via HTTPS. Implementar autenticação de dois fatores (2FA). Usar OAuth/OIDC em vez de senhas."
            )
            
            artifacts.append(artifact)
        
        return artifacts
    
    def _extract_http_headers(
        self,
        payload: str,
        source_ip: str,
        destination_ip: str,
        destination_host: str
    ) -> List[NetworkArtifact]:
        """Extrai headers HTTP sensíveis"""
        
        artifacts = []
        
        sensitive_headers = [
            "Authorization", "X-API-Key", "X-Auth-Token", "X-Access-Token",
            "User-Agent", "Referer", "X-Forwarded-For"
        ]
        
        for header in sensitive_headers:
            pattern = f"{header}:\\s*([^\r\n]+)"
            matches = re.findall(pattern, payload, re.IGNORECASE)
            
            for match in matches:
                severity = ForensicSeverity.HIGH if header == "Authorization" else ForensicSeverity.MEDIUM
                
                artifact = NetworkArtifact(
                    timestamp=datetime.now().isoformat(),
                    artifact_type=ArtifactType.HTTP_HEADER,
                    source_ip=source_ip,
                    destination_ip=destination_ip,
                    destination_host=destination_host,
                    artifact_value=f"{header}: {match}",
                    artifact_hash=hashlib.sha256(f"{header}:{match}".encode()).hexdigest()[:16],
                    severity=severity,
                    interpretation=f"Header HTTP '{header}' capturado. Valor: {match[:40]}...",
                    exploitation_risk=f"Informações sensíveis podem ser extraídas deste header.",
                    mitigation=f"Remover headers sensíveis em respostas. Implementar Content Security Policy (CSP)."
                )
                
                artifacts.append(artifact)
        
        return artifacts
    
    def _is_jwt(self, token: str) -> bool:
        """Verifica se um token é um JWT"""
        parts = token.split('.')
        return len(parts) == 3
    
    def _decode_jwt(self, token: str) -> Optional[Dict]:
        """Tenta decodificar um JWT (sem verificar assinatura)"""
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            # Decodificar payload (segunda parte)
            payload = parts[1]
            # Adicionar padding se necessário
            payload += '=' * (4 - len(payload) % 4)
            
            decoded = base64.urlsafe_b64decode(payload)
            return json.loads(decoded)
        except Exception:
            return None
    
    def get_forensic_report(self, session_id: str) -> Dict:
        """Gera um relatório forense completo"""
        
        if session_id not in self.forensic_sessions:
            return {"error": "Sessão não encontrada"}
        
        session = self.forensic_sessions[session_id]
        
        # Agrupar artefatos por tipo
        artifacts_by_type = {}
        for artifact in session.artifacts:
            artifact_type = artifact.artifact_type.value
            if artifact_type not in artifacts_by_type:
                artifacts_by_type[artifact_type] = []
            artifacts_by_type[artifact_type].append(asdict(artifact))
        
        return {
            "session_id": session_id,
            "start_time": session.start_time,
            "total_artifacts": session.total_artifacts,
            "critical_findings": session.critical_findings,
            "high_findings": session.high_findings,
            "artifacts_by_type": artifacts_by_type,
            "artifacts": [asdict(a) for a in session.artifacts]
        }

# ============================================================================
# INSTÂNCIA GLOBAL
# ============================================================================

forensic_analyzer = ForensicAnalyzer()

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""    🔬 ANÁLISE FORENSE REAL 🔬
    Análise de Artefatos de Rede Capturados
    ======================================
    """
    
    # Criar sessão forense
    session = forensic_analyzer.create_forensic_session("FORENSIC_001")
    
    # Exemplo de payload HTTP com artefatos
    http_payload = b"""    POST /login HTTP/1.1
    Host: example.com
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
    Set-Cookie: PHPSESSID=abc123def456; Path=/; HttpOnly
    
    username=admin&password=senha123
    """    
    # Analisar payload
    print("\n[1] Analisando payload HTTP...")
    artifacts = forensic_analyzer.analyze_http_payload(
        session_id="FORENSIC_001",
        payload=http_payload,
        source_ip="192.168.1.200",
        destination_ip="192.168.1.1",
        destination_host="example.com"
    )
    
    print(f"\n[2] Artefatos Capturados: {len(artifacts)}")
    for artifact in artifacts:
        print(f"\n  Tipo: {artifact.artifact_type.value}")
        print(f"  Severidade: {artifact.severity.value}")
        print(f"  Valor: {artifact.artifact_value[:50]}...")
        print(f"  Risco: {artifact.exploitation_risk[:60]}...")
    
    # Gerar relatório
    print("\n[3] Relatório Forense:")
    report = forensic_analyzer.get_forensic_report("FORENSIC_001")
    print(f"  Total de Artefatos: {report['total_artifacts']}")
    print(f"  Achados Críticos: {report['critical_findings']}")
    print(f"  Achados de Alto Risco: {report['high_findings']}")

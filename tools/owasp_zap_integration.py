#!/usr/bin/env python3
"""MÓDULO DE INTEGRAÇÃO OWASP ZAP
Análise de Vulnerabilidade de Aplicação (DAST) Real
Integração com a API do OWASP ZAP para testes de segurança de aplicações web
"""
import logging
import subprocess
import json
import time
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import os
import platform

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS E DATACLASSES
# ============================================================================

class VulnerabilitySeverity(str, Enum):
    """Nível de severidade de uma vulnerabilidade"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"

class VulnerabilityType(str, Enum):
    """Tipos de vulnerabilidade detectadas pelo ZAP"""
    XSS = "Cross-Site Scripting (XSS)"
    SQL_INJECTION = "SQL Injection"
    CSRF = "Cross-Site Request Forgery (CSRF)"
    INSECURE_HEADERS = "Insecure HTTP Headers"
    WEAK_AUTHENTICATION = "Weak Authentication"
    SENSITIVE_DATA_EXPOSURE = "Sensitive Data Exposure"
    BROKEN_ACCESS_CONTROL = "Broken Access Control"
    SECURITY_MISCONFIGURATION = "Security Misconfiguration"
    XXE = "XML External Entity (XXE)"
    INSECURE_DESERIALIZATION = "Insecure Deserialization"

@dataclass
class Vulnerability:
    """Vulnerabilidade detectada pelo ZAP"""
    id: str
    name: str
    severity: VulnerabilitySeverity
    type: VulnerabilityType
    url: str
    parameter: str
    attack: str
    evidence: str
    description: str
    solution: str
    cwe_id: str
    owasp_risk: str

@dataclass
class DastScanResult:
    """Resultado de um escaneamento DAST"""
    scan_id: str
    target_url: str
    start_time: str
    end_time: Optional[str]
    status: str  # "running", "completed", "failed"
    vulnerabilities_found: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    vulnerabilities: List[Vulnerability]

# ============================================================================
# GERENCIADOR DE INTEGRAÇÃO ZAP
# ============================================================================

class OWASPZAPIntegration:
    """Integração com a API do OWASP ZAP"""
    
    def __init__(self, zap_host: str = "127.0.0.1", zap_port: int = 8080):
        self.zap_host = zap_host
        self.zap_port = zap_port
        self.zap_url = f"http://{zap_host}:{zap_port}"
        self.api_key = self._get_api_key()
        self.zap_available = self._check_zap_availability()
        self.active_scans = {}
    
    def _get_api_key(self) -> str:
        """Obtém a chave de API do ZAP"""
        # Tentar obter a chave de API do arquivo de configuração do ZAP
        try:
            if platform.system() == "Windows":
                config_path = os.path.expanduser("~\\.ZAP\\options.xml")
            else:
                config_path = os.path.expanduser("~/.ZAP/options.xml")
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    content = f.read()
                    # Procurar pela chave de API
                    if 'api.key' in content:
                        # Extrair a chave (formato simplificado)
                        import re
                        match = re.search(r'api\.key["\']?\s*[=:]\s*["\']?([^"\'>\s]+)', content)
                        if match:
                            return match.group(1)
        except Exception as e:
            logger.warning(f"Erro ao obter chave de API do ZAP: {e}")
        
        # Retornar uma chave padrão se não encontrada
        return "changeme"
    
    def _check_zap_availability(self) -> bool:
        """Verifica se o ZAP está disponível e acessível"""
        try:
            response = requests.get(
                f"{self.zap_url}/JSON/core/action/version",
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"ZAP encontrado: {response.json()}")
                return True
        except Exception as e:
            logger.warning(f"ZAP não disponível: {e}")
        
        return False
    
    def start_zap_daemon(self) -> bool:
        """Inicia o ZAP em modo daemon (headless)"""
        if self.zap_available:
            logger.info("ZAP já está em execução")
            return True
        
        try:
            if platform.system() == "Windows":
                # Windows
                zap_path = self._find_zap_windows()
                if zap_path:
                    subprocess.Popen(
                        [zap_path, "-daemon", "-port", str(self.zap_port)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    logger.info(f"ZAP iniciado em modo daemon na porta {self.zap_port}")
                    time.sleep(5)  # Aguardar inicialização
                    return self._check_zap_availability()
            else:
                # Linux/macOS
                subprocess.Popen(
                    ["zaproxy", "-daemon", "-port", str(self.zap_port)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                logger.info(f"ZAP iniciado em modo daemon na porta {self.zap_port}")
                time.sleep(5)
                return self._check_zap_availability()
        
        except Exception as e:
            logger.error(f"Erro ao iniciar ZAP: {e}")
        
        return False
    
    def _find_zap_windows(self) -> Optional[str]:
        """Encontra o caminho do ZAP no Windows"""
        common_paths = [
            "C:\\Program Files\\OWASP\\Zed Attack Proxy\\zaproxy.exe",
            "C:\\Program Files (x86)\\OWASP\\Zed Attack Proxy\\zaproxy.exe",
            os.path.expanduser("~\\AppData\\Local\\OWASP\\Zed Attack Proxy\\zaproxy.exe")
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def start_scan(self, target_url: str, scan_type: str = "full") -> Optional[str]:
        """Inicia um escaneamento no alvo especificado"""
        
        if not self.zap_available:
            logger.error("ZAP não está disponível")
            return None
        
        try:
            # Criar um novo contexto
            context_id = self._create_context(target_url)
            
            # Iniciar o escaneamento
            if scan_type == "full":
                # Escaneamento completo: Spider + Active Scan
                scan_id = self._start_spider(target_url, context_id)
                if scan_id:
                    # Aguardar conclusão do Spider
                    self._wait_for_spider(scan_id)
                    
                    # Iniciar Active Scan
                    active_scan_id = self._start_active_scan(target_url, context_id)
                    return active_scan_id
            
            elif scan_type == "quick":
                # Escaneamento rápido: apenas Active Scan
                return self._start_active_scan(target_url, context_id)
        
        except Exception as e:
            logger.error(f"Erro ao iniciar escaneamento: {e}")
        
        return None
    
    def _create_context(self, target_url: str) -> Optional[str]:
        """Cria um contexto no ZAP"""
        try:
            params = {
                "apikey": self.api_key,
                "contextName": f"context_{int(time.time())}"
            }
            
            response = requests.get(
                f"{self.zap_url}/JSON/context/action/newContext",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("contextId")
        
        except Exception as e:
            logger.error(f"Erro ao criar contexto: {e}")
        
        return None
    
    def _start_spider(self, target_url: str, context_id: str) -> Optional[str]:
        """Inicia o Spider (rastreador) do ZAP"""
        try:
            params = {
                "apikey": self.api_key,
                "url": target_url,
                "contextId": context_id
            }
            
            response = requests.get(
                f"{self.zap_url}/JSON/spider/action/scan",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("scan")
        
        except Exception as e:
            logger.error(f"Erro ao iniciar Spider: {e}")
        
        return None
    
    def _wait_for_spider(self, scan_id: str, timeout: int = 300):
        """Aguarda a conclusão do Spider"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                params = {"apikey": self.api_key, "scanId": scan_id}
                response = requests.get(
                    f"{self.zap_url}/JSON/spider/view/status",
                    params=params,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = int(data.get("status", 0))
                    
                    if status == 100:
                        logger.info(f"Spider concluído (Scan ID: {scan_id})")
                        return True
                    
                    logger.info(f"Spider em progresso: {status}%")
            
            except Exception as e:
                logger.error(f"Erro ao verificar status do Spider: {e}")
            
            time.sleep(5)
        
        logger.warning(f"Spider expirou (Scan ID: {scan_id})")
        return False
    
    def _start_active_scan(self, target_url: str, context_id: str) -> Optional[str]:
        """Inicia o Active Scan (teste de vulnerabilidades) do ZAP"""
        try:
            params = {
                "apikey": self.api_key,
                "url": target_url,
                "contextId": context_id,
                "recurse": "true"
            }
            
            response = requests.get(
                f"{self.zap_url}/JSON/ascan/action/scan",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("scan")
        
        except Exception as e:
            logger.error(f"Erro ao iniciar Active Scan: {e}")
        
        return None
    
    def get_scan_status(self, scan_id: str) -> Dict:
        """Obtém o status de um escaneamento"""
        try:
            params = {"apikey": self.api_key, "scanId": scan_id}
            response = requests.get(
                f"{self.zap_url}/JSON/ascan/view/status",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "scan_id": scan_id,
                    "status": int(data.get("status", 0)),
                    "progress": int(data.get("progress", 0))
                }
        
        except Exception as e:
            logger.error(f"Erro ao obter status do escaneamento: {e}")
        
        return {"scan_id": scan_id, "status": 0, "progress": 0}
    
    def get_vulnerabilities(self, scan_id: Optional[str] = None) -> List[Vulnerability]:
        """Obtém as vulnerabilidades encontradas"""
        vulnerabilities = []
        
        try:
            params = {"apikey": self.api_key}
            response = requests.get(
                f"{self.zap_url}/JSON/core/view/alerts",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                alerts = data.get("alerts", [])
                
                for alert in alerts:
                    severity = self._map_severity(alert.get("riskcode", "0"))
                    
                    vuln = Vulnerability(
                        id=alert.get("id", ""),
                        name=alert.get("name", ""),
                        severity=severity,
                        type=self._map_vulnerability_type(alert.get("name", "")),
                        url=alert.get("url", ""),
                        parameter=alert.get("param", ""),
                        attack=alert.get("attack", ""),
                        evidence=alert.get("evidence", ""),
                        description=alert.get("description", ""),
                        solution=alert.get("solution", ""),
                        cwe_id=alert.get("cweid", ""),
                        owasp_risk=alert.get("riskdesc", "")
                    )
                    
                    vulnerabilities.append(vuln)
        
        except Exception as e:
            logger.error(f"Erro ao obter vulnerabilidades: {e}")
        
        return vulnerabilities
    
    def _map_severity(self, risk_code: str) -> VulnerabilitySeverity:
        """Mapeia o código de risco do ZAP para severidade"""
        risk_map = {
            "3": VulnerabilitySeverity.HIGH,
            "2": VulnerabilitySeverity.MEDIUM,
            "1": VulnerabilitySeverity.LOW,
            "0": VulnerabilitySeverity.INFORMATIONAL
        }
        return risk_map.get(str(risk_code), VulnerabilitySeverity.LOW)
    
    def _map_vulnerability_type(self, name: str) -> VulnerabilityType:
        """Mapeia o nome da vulnerabilidade para o tipo"""
        name_lower = name.lower()
        
        if "xss" in name_lower or "cross-site scripting" in name_lower:
            return VulnerabilityType.XSS
        elif "sql" in name_lower or "injection" in name_lower:
            return VulnerabilityType.SQL_INJECTION
        elif "csrf" in name_lower or "cross-site request" in name_lower:
            return VulnerabilityType.CSRF
        elif "header" in name_lower:
            return VulnerabilityType.INSECURE_HEADERS
        elif "authentication" in name_lower:
            return VulnerabilityType.WEAK_AUTHENTICATION
        elif "sensitive" in name_lower or "exposure" in name_lower:
            return VulnerabilityType.SENSITIVE_DATA_EXPOSURE
        elif "access" in name_lower:
            return VulnerabilityType.BROKEN_ACCESS_CONTROL
        elif "configuration" in name_lower:
            return VulnerabilityType.SECURITY_MISCONFIGURATION
        elif "xxe" in name_lower or "xml" in name_lower:
            return VulnerabilityType.XXE
        elif "deserialization" in name_lower:
            return VulnerabilityType.INSECURE_DESERIALIZATION
        else:
            return VulnerabilityType.SECURITY_MISCONFIGURATION
    
    def generate_report(self, vulnerabilities: List[Vulnerability]) -> Dict:
        """Gera um relatório das vulnerabilidades"""
        
        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "INFORMATIONAL": 0
        }
        
        type_counts = {}
        
        for vuln in vulnerabilities:
            severity_counts[vuln.severity.value] += 1
            
            type_name = vuln.type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        return {
            "total_vulnerabilities": len(vulnerabilities),
            "severity_distribution": severity_counts,
            "vulnerability_types": type_counts,
            "critical_findings": severity_counts["CRITICAL"],
            "high_findings": severity_counts["HIGH"],
            "vulnerabilities": [asdict(v) for v in vulnerabilities]
        }

# ============================================================================
# INSTÂNCIA GLOBAL
# ============================================================================

zap_integration = OWASPZAPIntegration()

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""    🔍 OWASP ZAP INTEGRATION 🔍
    Análise de Vulnerabilidade de Aplicação (DAST) Real
    ================================================
    """
    
    # Verificar disponibilidade do ZAP
    print(f"\n[1] Verificando disponibilidade do ZAP...")
    print(f"  ZAP Disponível: {'Sim' if zap_integration.zap_available else 'Não'}")
    
    if not zap_integration.zap_available:
        print(f"\n[2] Tentando iniciar ZAP em modo daemon...")
        if zap_integration.start_zap_daemon():
            print(f"  ZAP iniciado com sucesso!")
        else:
            print(f"  ERRO: ZAP não pôde ser iniciado. Instale o OWASP ZAP.")
    
    # Iniciar escaneamento (exemplo)
    if zap_integration.zap_available:
        print(f"\n[3] Iniciando escaneamento de vulnerabilidades...")
        target = "http://192.168.1.10:3000"
        scan_id = zap_integration.start_scan(target, scan_type="quick")
        
        if scan_id:
            print(f"  Escaneamento iniciado (ID: {scan_id})")
            
            # Aguardar conclusão
            print(f"\n[4] Aguardando conclusão do escaneamento...")
            while True:
                status = zap_integration.get_scan_status(scan_id)
                print(f"  Progresso: {status['progress']}%")
                
                if status['status'] == 100:
                    break
                
                time.sleep(5)
            
            # Obter vulnerabilidades
            print(f"\n[5] Vulnerabilidades encontradas:")
            vulns = zap_integration.get_vulnerabilities(scan_id)
            
            for vuln in vulns[:5]:  # Mostrar as primeiras 5
                print(f"\n  Nome: {vuln.name}")
                print(f"  Severidade: {vuln.severity.value}")
                print(f"  URL: {vuln.url}")
                print(f"  Solução: {vuln.solution[:100]}...")
            
            # Gerar relatório
            print(f"\n[6] Relatório:")
            report = zap_integration.generate_report(vulns)
            print(f"  Total de Vulnerabilidades: {report['total_vulnerabilities']}")
            print(f"  Críticas: {report['critical_findings']}")
            print(f"  Altas: {report['high_findings']}")

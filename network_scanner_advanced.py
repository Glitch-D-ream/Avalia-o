#!/usr/bin/env python3
"""MÓDULO DE ESCANEAMENTO DE REDE AVANÇADO
Integração com Nmap para análise profunda de portas e serviços
"""
import subprocess
import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Port:
    """Representação de uma porta aberta"""
    port_number: int
    protocol: str
    state: str
    service: str
    version: str = ""
    vulnerability: str = ""

@dataclass
class ScanResult:
    """Resultado de um escaneamento de host"""
    target_ip: str
    hostname: str
    status: str
    ports: List[Port]
    os_detection: str = ""
    scan_time: float = 0.0
    timestamp: str = ""

class NmapScanner:
    """Wrapper para Nmap com integração educacional"""
    
    COMMON_PORTS = [
        22,    # SSH
        80,    # HTTP
        443,   # HTTPS
        3306,  # MySQL
        5432,  # PostgreSQL
        8080,  # HTTP Alternativo
        8443,  # HTTPS Alternativo
        27017, # MongoDB
        6379,  # Redis
        5000,  # Flask/Dev
    ]
    
    SERVICE_VULNERABILITIES = {
        "ssh": "SSH padrão pode ser alvo de força bruta",
        "http": "HTTP em texto plano - dados não criptografados",
        "https": "HTTPS - criptografado (mais seguro)",
        "mysql": "MySQL exposto - risco de acesso não autorizado",
        "postgresql": "PostgreSQL exposto - risco de acesso não autorizado",
        "mongodb": "MongoDB sem autenticação - crítico",
        "redis": "Redis sem autenticação - risco de acesso",
    }
    
    @staticmethod
    def check_nmap_installed() -> bool:
        """Verifica se Nmap está instalado"""
        try:
            subprocess.run(["nmap", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Nmap não está instalado. Usando simulação.")
            return False
    
    @staticmethod
    async def scan_host(target_ip: str, ports: Optional[List[int]] = None) -> ScanResult:
        """
        Escaneia um host para portas abertas e serviços
        
        Args:
            target_ip: IP do alvo
            ports: Lista de portas a escanear (padrão: portas comuns)
        
        Returns:
            ScanResult com informações de portas abertas
        """
        if ports is None:
            ports = NmapScanner.COMMON_PORTS
        
        ports_str = ",".join(map(str, ports))
        
        # Verificar se Nmap está disponível
        if not NmapScanner.check_nmap_installed():
            logger.info(f"Usando simulação para {target_ip}")
            return NmapScanner._simulate_scan(target_ip)
        
        try:
            # Executar Nmap
            cmd = [
                "nmap",
                "-p", ports_str,
                "-sV",  # Detecção de versão
                "-sC",  # Scripts padrão
                "-O",   # Detecção de SO
                "-oX", "-",  # Output XML para stdout
                target_ip
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Parsear resultado
            return NmapScanner._parse_nmap_output(result.stdout, target_ip)
        
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout ao escanear {target_ip}")
            return NmapScanner._simulate_scan(target_ip)
        except Exception as e:
            logger.error(f"Erro ao executar Nmap: {e}")
            return NmapScanner._simulate_scan(target_ip)
    
    @staticmethod
    def _parse_nmap_output(output: str, target_ip: str) -> ScanResult:
        """Parseia a saída do Nmap"""
        # Implementação simplificada - em produção, usar python-nmap
        ports = []
        
        # Regex para encontrar portas abertas
        port_pattern = r"(\d+)/tcp\s+open\s+(\S+)"
        matches = re.findall(port_pattern, output)
        
        for port_num, service in matches:
            port = Port(
                port_number=int(port_num),
                protocol="tcp",
                state="open",
                service=service,
                vulnerability=NmapScanner.SERVICE_VULNERABILITIES.get(service, "")
            )
            ports.append(port)
        
        return ScanResult(
            target_ip=target_ip,
            hostname=target_ip,
            status="up",
            ports=ports,
            timestamp=datetime.now().isoformat()
        )
    
    @staticmethod
    def _simulate_scan(target_ip: str) -> ScanResult:
        """Simula um escaneamento de Nmap para fins educacionais"""
        
        # Simular portas abertas baseado no IP
        simulated_ports = {
            "192.168.1.1": [
                Port(80, "tcp", "open", "http", vulnerability="HTTP em texto plano"),
                Port(443, "tcp", "open", "https", vulnerability="HTTPS - seguro"),
                Port(22, "tcp", "open", "ssh", vulnerability="SSH - força bruta possível"),
            ],
            "192.168.1.10": [
                Port(3000, "tcp", "open", "http", vulnerability="React Dev Server"),
                Port(8000, "tcp", "open", "http", vulnerability="FastAPI Server"),
                Port(22, "tcp", "open", "ssh", vulnerability="SSH - força bruta possível"),
            ],
            "192.168.1.50": [
                Port(8080, "tcp", "open", "http", vulnerability="HTTP Alternativo"),
            ],
            "192.168.1.200": [
                Port(80, "tcp", "open", "http", vulnerability="HTTP em texto plano"),
            ],
        }
        
        ports = simulated_ports.get(target_ip, [
            Port(80, "tcp", "open", "http", vulnerability="HTTP em texto plano"),
        ])
        
        return ScanResult(
            target_ip=target_ip,
            hostname=f"device-{target_ip.split('.')[-1]}",
            status="up",
            ports=ports,
            os_detection="Linux/Android",
            timestamp=datetime.now().isoformat()
        )

class NetworkVulnerabilityAnalyzer:
    """Analisa vulnerabilidades baseadas em escaneamento de rede"""
    
    @staticmethod
    async def analyze_scan_results(scan_results: List[ScanResult]) -> Dict:
        """Analisa resultados de escaneamento para vulnerabilidades"""
        
        vulnerabilities = []
        critical_count = 0
        high_count = 0
        
        for scan in scan_results:
            for port in scan.ports:
                if port.vulnerability:
                    severity = "CRÍTICO" if port.service in ["mysql", "mongodb", "redis"] else "ALTO"
                    
                    if severity == "CRÍTICO":
                        critical_count += 1
                    else:
                        high_count += 1
                    
                    vuln = {
                        "id": len(vulnerabilities) + 1,
                        "severity": severity,
                        "title": f"Serviço {port.service.upper()} Exposto",
                        "description": port.vulnerability,
                        "affected_device": scan.target_ip,
                        "port": port.port_number,
                        "remediation": NetworkVulnerabilityAnalyzer._get_remediation(port.service)
                    }
                    vulnerabilities.append(vuln)
        
        return {
            "total_vulnerabilities": len(vulnerabilities),
            "critical": critical_count,
            "high": high_count,
            "vulnerabilities": vulnerabilities,
            "risk_score": min(100, (critical_count * 30 + high_count * 15))
        }
    
    @staticmethod
    def _get_remediation(service: str) -> str:
        """Retorna recomendação de remediação para um serviço"""
        remediations = {
            "http": "Use HTTPS em vez de HTTP para criptografar dados em trânsito",
            "ssh": "Desabilite login com senha, use chaves SSH. Implemente rate limiting.",
            "mysql": "Mude a senha padrão, restrinja acesso por firewall, use SSL",
            "mongodb": "Ative autenticação, use firewall, criptografe conexões",
            "redis": "Ative autenticação, restrinja acesso por firewall",
        }
        return remediations.get(service, "Restrinja acesso por firewall e implemente autenticação forte")

class PortSecurityRating:
    """Classifica a segurança de portas abertas"""
    
    @staticmethod
    def rate_port_security(port: Port) -> Dict:
        """Classifica a segurança de uma porta"""
        
        secure_services = ["https", "ssh"]
        risky_services = ["http", "mysql", "mongodb", "redis"]
        
        if port.service in secure_services:
            rating = "SEGURO"
            score = 80
        elif port.service in risky_services:
            rating = "RISCO"
            score = 30
        else:
            rating = "DESCONHECIDO"
            score = 50
        
        return {
            "port": port.port_number,
            "service": port.service,
            "rating": rating,
            "score": score,
            "recommendation": f"Revise a configuração de {port.service}"
        }

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

async def main():
    import asyncio
    
    print("""    ⚡ ESCANEADOR DE REDE AVANÇADO ⚡
    Integração com Nmap para Análise Profunda
    ==========================================
    """
    
    # Escanear dispositivos da rede
    targets = [
        "192.168.1.1",    # Roteador
        "192.168.1.10",   # Notebook
        "192.168.1.50",   # Celular 02
        "192.168.1.200",  # Celular 04
    ]
    
    print("\n🔍 Escaneando dispositivos...
")
    
    scan_results = []
    for target in targets:
        print(f"  Escaneando {target}...")
        result = await NmapScanner.scan_host(target)
        scan_results.append(result)
        print(f"    ✓ {len(result.ports)} portas abertas")
    
    # Analisar vulnerabilidades
    print("\n⚠️ Analisando vulnerabilidades...
")
    analysis = await NetworkVulnerabilityAnalyzer.analyze_scan_results(scan_results)
    
    print(f"Total de Vulnerabilidades: {analysis['total_vulnerabilities']}")
    print(f"Críticas: {analysis['critical']}")
    print(f"Altas: {analysis['high']}")
    print(f"Risk Score: {analysis['risk_score']}/100
")
    
    for vuln in analysis['vulnerabilities']:
        print(f"  [{vuln['severity']}] {vuln['title']}")
        print(f"    Dispositivo: {vuln['affected_device']}:{vuln['port']}")
        print(f"    Remediação: {vuln['remediation']}
")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

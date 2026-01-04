#!/usr/bin/env python3
"""
WebVuln AI Analyzer - Analisador Avançado de Vulnerabilidades Web
Ferramenta criativa e funcional para análise profunda de aplicações web
AVISO: Apenas para fins educacionais em ambientes controlados.
"""

import requests
import re
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

class WebVulnAnalyzer:
    """Analisador avançado de vulnerabilidades web"""
    
    def __init__(self, target_url, timeout=15):
        """
        Inicializa o analisador
        
        Args:
            target_url: URL do alvo
            timeout: Timeout para requisições (segundos)
        """
        self.target_url = target_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.vulnerabilities = []
        self.endpoints = []
        self.js_files = []
        self.technologies = {}
        
    def full_scan(self):
        """
        Executa scan completo do alvo
        
        Returns:
            dict: Relatório completo de vulnerabilidades
        """
        print(f"\n🔍 WebVuln AI Analyzer - Scan Completo")
        print(f"🎯 Alvo: {self.target_url}")
        print("="*80)
        
        results = {
            "target": self.target_url,
            "timestamp": datetime.now().isoformat(),
            "vulnerabilities": [],
            "security_headers": {},
            "cookies": {},
            "javascript_analysis": {},
            "api_endpoints": [],
            "technologies": {},
            "risk_score": 0
        }
        
        try:
            # 1. Análise de Headers de Segurança
            print("\n[1/7] 🛡️  Analisando headers de segurança...")
            results["security_headers"] = self.analyze_security_headers()
            
            # 2. Análise de Cookies
            print("[2/7] 🍪 Analisando cookies...")
            results["cookies"] = self.analyze_cookies()
            
            # 3. Análise de JavaScript
            print("[3/7] 📜 Analisando arquivos JavaScript...")
            results["javascript_analysis"] = self.analyze_javascript()
            
            # 4. Descoberta de Endpoints de API
            print("[4/7] 🔗 Descobrindo endpoints de API...")
            results["api_endpoints"] = self.discover_api_endpoints()
            
            # 5. Detecção de Tecnologias
            print("[5/7] 🔧 Detectando tecnologias...")
            results["technologies"] = self.detect_technologies()
            
            # 6. Análise de SSL/TLS
            print("[6/7] 🔒 Analisando SSL/TLS...")
            results["ssl_analysis"] = self.analyze_ssl()
            
            # 7. Teste de Métodos HTTP
            print("[7/7] 📡 Testando métodos HTTP...")
            results["http_methods"] = self.test_http_methods()
            
            # Compilar vulnerabilidades
            results["vulnerabilities"] = self.vulnerabilities
            results["total_vulnerabilities"] = len(self.vulnerabilities)
            
            # Calcular score de risco
            results["risk_score"] = self.calculate_risk_score()
            
            print(f"\n✅ Scan completo!")
            print(f"📊 Vulnerabilidades encontradas: {len(self.vulnerabilities)}")
            print(f"⚠️  Risk Score: {results['risk_score']}/100")
            
        except Exception as e:
            results["error"] = str(e)
            print(f"\n❌ Erro durante scan: {e}")
        
        return results
    
    def analyze_security_headers(self):
        """Analisa headers de segurança"""
        try:
            response = self.session.get(self.target_url, timeout=self.timeout, verify=False)
            headers = response.headers
            
            security_headers = {
                "X-Frame-Options": headers.get("X-Frame-Options", "AUSENTE"),
                "X-Content-Type-Options": headers.get("X-Content-Type-Options", "AUSENTE"),
                "Strict-Transport-Security": headers.get("Strict-Transport-Security", "AUSENTE"),
                "Content-Security-Policy": headers.get("Content-Security-Policy", "AUSENTE"),
                "X-XSS-Protection": headers.get("X-XSS-Protection", "AUSENTE"),
                "Referrer-Policy": headers.get("Referrer-Policy", "AUSENTE"),
                "Permissions-Policy": headers.get("Permissions-Policy", "AUSENTE")
            }
            
            # Adicionar vulnerabilidades para headers ausentes
            for header, value in security_headers.items():
                if value == "AUSENTE":
                    self.vulnerabilities.append({
                        "type": "Missing Security Header",
                        "severity": "MEDIUM",
                        "header": header,
                        "description": f"Header de segurança {header} não encontrado",
                        "recommendation": f"Adicionar header {header} para melhorar segurança"
                    })
            
            return security_headers
            
        except Exception as e:
            print(f"  ❌ Erro ao analisar headers: {e}")
            return {}
    
    def analyze_cookies(self):
        """Analisa configuração de cookies"""
        try:
            response = self.session.get(self.target_url, timeout=self.timeout, verify=False)
            cookies_analysis = {}
            
            for cookie in response.cookies:
                cookie_info = {
                    "name": cookie.name,
                    "value": cookie.value[:20] + "..." if len(cookie.value) > 20 else cookie.value,
                    "secure": cookie.secure,
                    "httponly": cookie.has_nonstandard_attr('HttpOnly'),
                    "samesite": cookie.get_nonstandard_attr('SameSite', 'None')
                }
                
                cookies_analysis[cookie.name] = cookie_info
                
                # Verificar vulnerabilidades
                if not cookie.secure:
                    self.vulnerabilities.append({
                        "type": "Insecure Cookie",
                        "severity": "HIGH",
                        "cookie": cookie.name,
                        "description": f"Cookie {cookie.name} não tem flag Secure",
                        "recommendation": "Adicionar flag Secure para proteger cookie em HTTPS"
                    })
                
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    self.vulnerabilities.append({
                        "type": "Cookie Without HttpOnly",
                        "severity": "MEDIUM",
                        "cookie": cookie.name,
                        "description": f"Cookie {cookie.name} não tem flag HttpOnly",
                        "recommendation": "Adicionar flag HttpOnly para proteger contra XSS"
                    })
            
            return cookies_analysis
            
        except Exception as e:
            print(f"  ❌ Erro ao analisar cookies: {e}")
            return {}
    
    def analyze_javascript(self):
        """Analisa arquivos JavaScript em busca de informações sensíveis"""
        try:
            response = self.session.get(self.target_url, timeout=self.timeout, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            js_analysis = {
                "total_files": 0,
                "external_files": [],
                "inline_scripts": 0,
                "api_endpoints_found": [],
                "sensitive_data": []
            }
            
            # Encontrar scripts externos
            for script in soup.find_all('script', src=True):
                js_url = urljoin(self.target_url, script['src'])
                js_analysis["external_files"].append(js_url)
                self.js_files.append(js_url)
                
                # Analisar conteúdo do arquivo JS
                try:
                    js_response = self.session.get(js_url, timeout=self.timeout, verify=False)
                    js_content = js_response.text
                    
                    # Procurar por endpoints de API
                    api_patterns = [
                        r'["\']https?://[^"\']+/api/[^"\']+["\']',
                        r'["\']\/api\/[^"\']+["\']',
                        r'fetch\(["\']([^"\']+)["\']',
                        r'axios\.[a-z]+\(["\']([^"\']+)["\']'
                    ]
                    
                    for pattern in api_patterns:
                        matches = re.findall(pattern, js_content)
                        for match in matches:
                            endpoint = match.strip('"\'')
                            if endpoint not in js_analysis["api_endpoints_found"]:
                                js_analysis["api_endpoints_found"].append(endpoint)
                    
                    # Procurar por dados sensíveis
                    sensitive_patterns = {
                        "API Keys": r'["\']api[_-]?key["\']:\s*["\']([^"\']+)["\']',
                        "Tokens": r'["\']token["\']:\s*["\']([^"\']+)["\']',
                        "Passwords": r'["\']password["\']:\s*["\']([^"\']+)["\']',
                        "Secrets": r'["\']secret["\']:\s*["\']([^"\']+)["\']'
                    }
                    
                    for data_type, pattern in sensitive_patterns.items():
                        matches = re.findall(pattern, js_content, re.IGNORECASE)
                        if matches:
                            js_analysis["sensitive_data"].append({
                                "type": data_type,
                                "file": js_url,
                                "count": len(matches)
                            })
                            
                            self.vulnerabilities.append({
                                "type": "Sensitive Data in JavaScript",
                                "severity": "CRITICAL",
                                "data_type": data_type,
                                "file": js_url,
                                "description": f"{data_type} encontrado em arquivo JavaScript",
                                "recommendation": "Remover dados sensíveis do código cliente"
                            })
                    
                except Exception as e:
                    print(f"  ⚠️  Erro ao analisar {js_url}: {e}")
            
            # Contar scripts inline
            js_analysis["inline_scripts"] = len(soup.find_all('script', src=False))
            js_analysis["total_files"] = len(js_analysis["external_files"])
            
            return js_analysis
            
        except Exception as e:
            print(f"  ❌ Erro ao analisar JavaScript: {e}")
            return {}
    
    def discover_api_endpoints(self):
        """Descobre endpoints de API"""
        endpoints = []
        
        # Endpoints comuns para testar
        common_endpoints = [
            "/api/login", "/api/register", "/api/user", "/api/users",
            "/api/auth", "/api/token", "/api/v1/login", "/api/v1/register",
            "/api/profile", "/api/settings", "/api/data"
        ]
        
        for endpoint in common_endpoints:
            full_url = urljoin(self.target_url, endpoint)
            try:
                response = self.session.get(full_url, timeout=5, verify=False)
                if response.status_code != 404:
                    endpoint_info = {
                        "url": full_url,
                        "status_code": response.status_code,
                        "methods_allowed": response.headers.get("Allow", "Unknown"),
                        "content_type": response.headers.get("Content-Type", "Unknown")
                    }
                    endpoints.append(endpoint_info)
                    print(f"  ✅ Encontrado: {endpoint} (HTTP {response.status_code})")
            except:
                pass
        
        return endpoints
    
    def detect_technologies(self):
        """Detecta tecnologias usadas no site"""
        try:
            response = self.session.get(self.target_url, timeout=self.timeout, verify=False)
            headers = response.headers
            content = response.text
            
            technologies = {
                "server": headers.get("Server", "Unknown"),
                "powered_by": headers.get("X-Powered-By", "Unknown"),
                "frameworks": [],
                "libraries": []
            }
            
            # Detectar frameworks JavaScript
            js_frameworks = {
                "React": r'react',
                "Vue": r'vue',
                "Angular": r'angular',
                "jQuery": r'jquery'
            }
            
            for framework, pattern in js_frameworks.items():
                if re.search(pattern, content, re.IGNORECASE):
                    technologies["frameworks"].append(framework)
            
            # Detectar bibliotecas
            libraries = {
                "Bootstrap": r'bootstrap',
                "Tailwind": r'tailwind',
                "Font Awesome": r'font-awesome'
            }
            
            for library, pattern in libraries.items():
                if re.search(pattern, content, re.IGNORECASE):
                    technologies["libraries"].append(library)
            
            return technologies
            
        except Exception as e:
            print(f"  ❌ Erro ao detectar tecnologias: {e}")
            return {}
    
    def analyze_ssl(self):
        """Analisa configuração SSL/TLS"""
        ssl_info = {
            "https_enabled": self.target_url.startswith("https://"),
            "certificate_valid": False
        }
        
        if ssl_info["https_enabled"]:
            try:
                # Testar com verificação de certificado
                response = requests.get(self.target_url, timeout=self.timeout, verify=True)
                ssl_info["certificate_valid"] = True
            except requests.exceptions.SSLError:
                ssl_info["certificate_valid"] = False
                self.vulnerabilities.append({
                    "type": "Invalid SSL Certificate",
                    "severity": "HIGH",
                    "description": "Certificado SSL inválido ou expirado",
                    "recommendation": "Renovar certificado SSL"
                })
        else:
            self.vulnerabilities.append({
                "type": "No HTTPS",
                "severity": "CRITICAL",
                "description": "Site não usa HTTPS",
                "recommendation": "Implementar HTTPS para proteger dados em trânsito"
            })
        
        return ssl_info
    
    def test_http_methods(self):
        """Testa métodos HTTP permitidos"""
        methods_to_test = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
        allowed_methods = []
        
        for method in methods_to_test:
            try:
                response = self.session.request(method, self.target_url, timeout=5, verify=False)
                if response.status_code != 405:  # 405 = Method Not Allowed
                    allowed_methods.append({
                        "method": method,
                        "status_code": response.status_code
                    })
            except:
                pass
        
        # Verificar se métodos perigosos estão habilitados
        dangerous_methods = ["PUT", "DELETE", "PATCH"]
        for method_info in allowed_methods:
            if method_info["method"] in dangerous_methods:
                self.vulnerabilities.append({
                    "type": "Dangerous HTTP Method Enabled",
                    "severity": "MEDIUM",
                    "method": method_info["method"],
                    "description": f"Método HTTP {method_info['method']} está habilitado",
                    "recommendation": f"Desabilitar método {method_info['method']} se não for necessário"
                })
        
        return allowed_methods
    
    def calculate_risk_score(self):
        """Calcula score de risco baseado nas vulnerabilidades"""
        score = 0
        
        severity_weights = {
            "CRITICAL": 25,
            "HIGH": 15,
            "MEDIUM": 8,
            "LOW": 3
        }
        
        for vuln in self.vulnerabilities:
            severity = vuln.get("severity", "LOW")
            score += severity_weights.get(severity, 0)
        
        # Limitar score a 100
        return min(score, 100)
    
    def generate_report(self, output_file="webvuln_report.json"):
        """Gera relatório em JSON"""
        report = self.full_scan()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Relatório salvo em: {output_file}")
        return report


# Exemplo de uso
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "https://example.com"
        print(f"⚠️  Nenhum alvo especificado, usando exemplo: {target}")
        print(f"💡 Uso: python3 webvuln_analyzer.py <URL>")
        print()
    
    analyzer = WebVulnAnalyzer(target)
    report = analyzer.generate_report()
    
    print("\n" + "="*80)
    print("📊 RESUMO DO SCAN")
    print("="*80)
    print(f"🎯 Alvo: {report['target']}")
    print(f"⚠️  Risk Score: {report['risk_score']}/100")
    print(f"🐛 Total de Vulnerabilidades: {report['total_vulnerabilities']}")
    
    if report['vulnerabilities']:
        print("\n🔴 Top 5 Vulnerabilidades:")
        for i, vuln in enumerate(report['vulnerabilities'][:5], 1):
            print(f"  {i}. [{vuln['severity']}] {vuln['type']}")
            print(f"     {vuln['description']}")

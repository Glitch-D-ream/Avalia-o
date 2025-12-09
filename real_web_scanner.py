#!/usr/bin/env python3.11
"""
Scanner de Vulnerabilidades Web - REAL E FUNCIONAL
Para uso educacional em ambientes controlados
"""

import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class RealWebScanner:
    """Scanner real de vulnerabilidades web"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.vulnerabilities = []
        
    def scan_target(self, url):
        """Escaneia um alvo real"""
        print(f"\n🔍 Iniciando scan em: {url}")
        print("="*80)
        
        results = {
            "target": url,
            "timestamp": datetime.now().isoformat(),
            "vulnerabilities": [],
            "security_headers": {},
            "forms": [],
            "cookies": {},
            "ssl_info": {}
        }
        
        try:
            # 1. Verificar headers de segurança
            print("\n[1/6] Verificando headers de segurança...")
            results["security_headers"] = self.check_security_headers(url)
            
            # 2. Analisar formulários
            print("[2/6] Analisando formulários...")
            results["forms"] = self.analyze_forms(url)
            
            # 3. Verificar cookies
            print("[3/6] Verificando cookies...")
            results["cookies"] = self.analyze_cookies(url)
            
            # 4. Testar métodos HTTP
            print("[4/6] Testando métodos HTTP...")
            results["http_methods"] = self.test_http_methods(url)
            
            # 5. Verificar SSL/TLS
            print("[5/6] Verificando SSL/TLS...")
            results["ssl_info"] = self.check_ssl(url)
            
            # 6. Detectar tecnologias
            print("[6/6] Detectando tecnologias...")
            results["technologies"] = self.detect_technologies(url)
            
            # Compilar vulnerabilidades encontradas
            results["vulnerabilities"] = self.vulnerabilities
            results["total_vulnerabilities"] = len(self.vulnerabilities)
            
            print("\n✅ Scan completo!")
            print(f"📊 Total de vulnerabilidades encontradas: {len(self.vulnerabilities)}")
            
        except Exception as e:
            results["error"] = str(e)
            print(f"\n❌ Erro durante scan: {e}")
        
        return results
    
    def check_security_headers(self, url):
        """Verifica headers de segurança"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            headers = response.headers
            
            security_headers = {
                "X-Frame-Options": headers.get("X-Frame-Options", "AUSENTE"),
                "X-Content-Type-Options": headers.get("X-Content-Type-Options", "AUSENTE"),
                "Strict-Transport-Security": headers.get("Strict-Transport-Security", "AUSENTE"),
                "Content-Security-Policy": headers.get("Content-Security-Policy", "AUSENTE"),
                "X-XSS-Protection": headers.get("X-XSS-Protection", "AUSENTE"),
                "Referrer-Policy": headers.get("Referrer-Policy", "AUSENTE"),
            }
            
            # Adicionar vulnerabilidades para headers ausentes
            for header, value in security_headers.items():
                if value == "AUSENTE":
                    self.vulnerabilities.append({
                        "type": "Missing Security Header",
                        "severity": "MEDIUM",
                        "header": header,
                        "description": f"Header de segurança {header} não encontrado"
                    })
            
            return security_headers
            
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_forms(self, url):
        """Analisa formulários na página"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')
            forms = soup.find_all('form')
            
            form_data = []
            for form in forms:
                form_info = {
                    "action": form.get('action', ''),
                    "method": form.get('method', 'GET').upper(),
                    "inputs": []
                }
                
                # Analisar inputs
                for input_tag in form.find_all('input'):
                    input_info = {
                        "name": input_tag.get('name', ''),
                        "type": input_tag.get('type', 'text'),
                        "value": input_tag.get('value', '')
                    }
                    form_info["inputs"].append(input_info)
                    
                    # Verificar se é campo de senha sem HTTPS
                    if input_info["type"] == "password" and not url.startswith("https://"):
                        self.vulnerabilities.append({
                            "type": "Insecure Password Transmission",
                            "severity": "HIGH",
                            "description": "Campo de senha em formulário sem HTTPS"
                        })
                
                form_data.append(form_info)
            
            return form_data
            
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_cookies(self, url):
        """Analisa cookies do site"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            cookies = {}
            
            for cookie in response.cookies:
                cookie_info = {
                    "value": cookie.value,
                    "secure": cookie.secure,
                    "httponly": cookie.has_nonstandard_attr('HttpOnly'),
                    "samesite": cookie.get_nonstandard_attr('SameSite', 'None')
                }
                cookies[cookie.name] = cookie_info
                
                # Verificar cookies inseguros
                if not cookie.secure:
                    self.vulnerabilities.append({
                        "type": "Insecure Cookie",
                        "severity": "MEDIUM",
                        "cookie": cookie.name,
                        "description": f"Cookie {cookie.name} sem flag Secure"
                    })
                
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    self.vulnerabilities.append({
                        "type": "Cookie without HttpOnly",
                        "severity": "MEDIUM",
                        "cookie": cookie.name,
                        "description": f"Cookie {cookie.name} sem flag HttpOnly"
                    })
            
            return cookies
            
        except Exception as e:
            return {"error": str(e)}
    
    def test_http_methods(self, url):
        """Testa métodos HTTP permitidos"""
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'PATCH']
        allowed_methods = []
        
        for method in methods:
            try:
                response = requests.request(method, url, timeout=5, verify=False)
                if response.status_code != 405:  # Method Not Allowed
                    allowed_methods.append(method)
                    
                    # Métodos perigosos
                    if method in ['PUT', 'DELETE', 'TRACE']:
                        self.vulnerabilities.append({
                            "type": "Dangerous HTTP Method",
                            "severity": "HIGH",
                            "method": method,
                            "description": f"Método HTTP perigoso {method} está habilitado"
                        })
            except:
                pass
        
        return allowed_methods
    
    def check_ssl(self, url):
        """Verifica configuração SSL/TLS"""
        if not url.startswith("https://"):
            self.vulnerabilities.append({
                "type": "No HTTPS",
                "severity": "CRITICAL",
                "description": "Site não usa HTTPS"
            })
            return {"https": False}
        
        return {"https": True, "note": "Verificação SSL básica realizada"}
    
    def detect_technologies(self, url):
        """Detecta tecnologias usadas no site"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            headers = response.headers
            content = response.text
            
            technologies = {
                "server": headers.get("Server", "Unknown"),
                "powered_by": headers.get("X-Powered-By", "Unknown"),
                "frameworks": []
            }
            
            # Detectar frameworks comuns
            if "react" in content.lower():
                technologies["frameworks"].append("React")
            if "vue" in content.lower():
                technologies["frameworks"].append("Vue.js")
            if "angular" in content.lower():
                technologies["frameworks"].append("Angular")
            if "jquery" in content.lower():
                technologies["frameworks"].append("jQuery")
            
            # Server header exposto é uma vulnerabilidade de information disclosure
            if technologies["server"] != "Unknown":
                self.vulnerabilities.append({
                    "type": "Information Disclosure",
                    "severity": "LOW",
                    "description": f"Server header exposto: {technologies['server']}"
                })
            
            return technologies
            
        except Exception as e:
            return {"error": str(e)}
    
    def generate_report(self, results):
        """Gera relatório formatado"""
        print("\n" + "="*80)
        print("📋 RELATÓRIO DE VULNERABILIDADES")
        print("="*80)
        print(f"\n🎯 Alvo: {results['target']}")
        print(f"⏰ Data/Hora: {results['timestamp']}")
        print(f"\n🔴 Total de Vulnerabilidades: {results['total_vulnerabilities']}")
        print("\n" + "-"*80)
        
        # Agrupar por severidade
        critical = [v for v in results['vulnerabilities'] if v['severity'] == 'CRITICAL']
        high = [v for v in results['vulnerabilities'] if v['severity'] == 'HIGH']
        medium = [v for v in results['vulnerabilities'] if v['severity'] == 'MEDIUM']
        low = [v for v in results['vulnerabilities'] if v['severity'] == 'LOW']
        
        if critical:
            print(f"\n🔴 CRÍTICAS ({len(critical)}):")
            for v in critical:
                print(f"  • {v['type']}: {v['description']}")
        
        if high:
            print(f"\n🟠 ALTAS ({len(high)}):")
            for v in high:
                print(f"  • {v['type']}: {v['description']}")
        
        if medium:
            print(f"\n🟡 MÉDIAS ({len(medium)}):")
            for v in medium:
                print(f"  • {v['type']}: {v['description']}")
        
        if low:
            print(f"\n🔵 BAIXAS ({len(low)}):")
            for v in low:
                print(f"  • {v['type']}: {v['description']}")
        
        print("\n" + "="*80)
        
        # Salvar em JSON
        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório salvo em: {filename}")

def main():
    """Função principal"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3.11 real_web_scanner.py <URL>")
        print("Exemplo: python3.11 real_web_scanner.py https://example.com")
        sys.exit(1)
    
    target_url = sys.argv[1]
    
    scanner = RealWebScanner()
    results = scanner.scan_target(target_url)
    scanner.generate_report(results)

if __name__ == "__main__":
    main()

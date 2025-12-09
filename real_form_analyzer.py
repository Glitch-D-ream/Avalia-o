#!/usr/bin/env python3.11
"""
Analisador de Formulários e Cookies - REAL E FUNCIONAL
Ferramenta educacional para análise de segurança web
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class RealFormAnalyzer:
    """Analisador real de formulários e cookies"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.findings = []
        
    def analyze_site(self, url):
        """Analisa um site completo"""
        print(f"\n🔍 Analisando: {url}")
        print("="*80)
        
        results = {
            "target": url,
            "timestamp": datetime.now().isoformat(),
            "forms": [],
            "cookies": {},
            "inputs": [],
            "security_issues": [],
            "recommendations": []
        }
        
        try:
            # 1. Analisar formulários
            print("\n[1/4] Analisando formulários...")
            results["forms"] = self.analyze_forms(url)
            
            # 2. Analisar cookies
            print("[2/4] Analisando cookies...")
            results["cookies"] = self.analyze_cookies(url)
            
            # 3. Analisar campos de entrada
            print("[3/4] Analisando campos de entrada...")
            results["inputs"] = self.analyze_inputs(url)
            
            # 4. Testar vulnerabilidades comuns
            print("[4/4] Testando vulnerabilidades...")
            results["security_issues"] = self.test_vulnerabilities(url)
            
            # Gerar recomendações
            results["recommendations"] = self.generate_recommendations(results)
            
            print("\n✅ Análise completa!")
            
        except Exception as e:
            results["error"] = str(e)
            print(f"\n❌ Erro durante análise: {e}")
        
        return results
    
    def analyze_forms(self, url):
        """Analisa todos os formulários da página"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')
            forms = soup.find_all('form')
            
            form_data = []
            for idx, form in enumerate(forms, 1):
                action = form.get('action', '')
                method = form.get('method', 'GET').upper()
                
                # Resolver URL completa da action
                if action:
                    action_url = urljoin(url, action)
                else:
                    action_url = url
                
                form_info = {
                    "id": idx,
                    "action": action_url,
                    "method": method,
                    "inputs": [],
                    "has_csrf_token": False,
                    "security_issues": []
                }
                
                # Analisar inputs
                for input_tag in form.find_all(['input', 'textarea', 'select']):
                    input_info = {
                        "name": input_tag.get('name', ''),
                        "type": input_tag.get('type', 'text'),
                        "id": input_tag.get('id', ''),
                        "required": input_tag.has_attr('required'),
                        "placeholder": input_tag.get('placeholder', '')
                    }
                    form_info["inputs"].append(input_info)
                    
                    # Verificar token CSRF
                    if 'csrf' in input_info["name"].lower() or 'token' in input_info["name"].lower():
                        form_info["has_csrf_token"] = True
                
                # Verificar problemas de segurança
                if not form_info["has_csrf_token"] and method == "POST":
                    form_info["security_issues"].append("Sem proteção CSRF")
                
                if not action_url.startswith("https://"):
                    form_info["security_issues"].append("Formulário não usa HTTPS")
                
                # Verificar campos de senha
                password_fields = [i for i in form_info["inputs"] if i["type"] == "password"]
                if password_fields and not action_url.startswith("https://"):
                    form_info["security_issues"].append("Campo de senha sem HTTPS")
                
                form_data.append(form_info)
                
                print(f"  ✓ Formulário {idx}: {method} -> {action_url}")
                if form_info["security_issues"]:
                    for issue in form_info["security_issues"]:
                        print(f"    ⚠️  {issue}")
            
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
                    "value": cookie.value[:20] + "..." if len(cookie.value) > 20 else cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                    "secure": cookie.secure,
                    "httponly": cookie.has_nonstandard_attr('HttpOnly'),
                    "samesite": cookie.get_nonstandard_attr('SameSite', 'None'),
                    "expires": str(cookie.expires) if cookie.expires else "Session",
                    "security_issues": []
                }
                
                # Verificar problemas de segurança
                if not cookie.secure:
                    cookie_info["security_issues"].append("Sem flag Secure")
                
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    cookie_info["security_issues"].append("Sem flag HttpOnly")
                
                if cookie.get_nonstandard_attr('SameSite', 'None') == 'None':
                    cookie_info["security_issues"].append("SameSite não configurado")
                
                cookies[cookie.name] = cookie_info
                
                print(f"  🍪 Cookie: {cookie.name}")
                if cookie_info["security_issues"]:
                    for issue in cookie_info["security_issues"]:
                        print(f"    ⚠️  {issue}")
            
            return cookies
            
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_inputs(self, url):
        """Analisa todos os campos de entrada"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            inputs = []
            for input_tag in soup.find_all(['input', 'textarea']):
                input_info = {
                    "type": input_tag.get('type', 'text'),
                    "name": input_tag.get('name', ''),
                    "id": input_tag.get('id', ''),
                    "placeholder": input_tag.get('placeholder', ''),
                    "maxlength": input_tag.get('maxlength', 'unlimited'),
                    "pattern": input_tag.get('pattern', 'none'),
                    "autocomplete": input_tag.get('autocomplete', 'on'),
                    "security_notes": []
                }
                
                # Verificar questões de segurança
                if input_info["type"] == "password" and input_info["autocomplete"] == "on":
                    input_info["security_notes"].append("Autocomplete habilitado em senha")
                
                if input_info["maxlength"] == "unlimited":
                    input_info["security_notes"].append("Sem limite de tamanho")
                
                inputs.append(input_info)
            
            return inputs
            
        except Exception as e:
            return {"error": str(e)}
    
    def test_vulnerabilities(self, url):
        """Testa vulnerabilidades comuns"""
        issues = []
        
        try:
            response = self.session.get(url, timeout=10, verify=False)
            content = response.text.lower()
            
            # Verificar informações sensíveis no código fonte
            if 'password' in content or 'senha' in content:
                issues.append({
                    "type": "Information Disclosure",
                    "severity": "LOW",
                    "description": "Palavras relacionadas a senha encontradas no código fonte"
                })
            
            if 'api_key' in content or 'apikey' in content:
                issues.append({
                    "type": "Information Disclosure",
                    "severity": "HIGH",
                    "description": "Possível API key exposta no código fonte"
                })
            
            # Verificar comentários HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            comments = soup.find_all(string=lambda text: isinstance(text, str) and '<!--' in str(text))
            if comments:
                issues.append({
                    "type": "Information Disclosure",
                    "severity": "LOW",
                    "description": f"{len(comments)} comentários HTML encontrados"
                })
            
            # Verificar scripts inline
            inline_scripts = soup.find_all('script', src=False)
            if inline_scripts:
                issues.append({
                    "type": "Security Best Practice",
                    "severity": "MEDIUM",
                    "description": f"{len(inline_scripts)} scripts inline encontrados (CSP risk)"
                })
            
        except Exception as e:
            issues.append({"error": str(e)})
        
        return issues
    
    def generate_recommendations(self, results):
        """Gera recomendações de segurança"""
        recommendations = []
        
        # Baseado nos formulários
        for form in results.get("forms", []):
            if not form.get("has_csrf_token", False):
                recommendations.append("Implementar proteção CSRF em formulários POST")
            if "Formulário não usa HTTPS" in form.get("security_issues", []):
                recommendations.append("Usar HTTPS para todos os formulários")
        
        # Baseado nos cookies
        for cookie_name, cookie_data in results.get("cookies", {}).items():
            if "Sem flag Secure" in cookie_data.get("security_issues", []):
                recommendations.append(f"Adicionar flag Secure ao cookie {cookie_name}")
            if "Sem flag HttpOnly" in cookie_data.get("security_issues", []):
                recommendations.append(f"Adicionar flag HttpOnly ao cookie {cookie_name}")
        
        return list(set(recommendations))  # Remover duplicatas
    
    def generate_report(self, results):
        """Gera relatório formatado"""
        print("\n" + "="*80)
        print("📋 RELATÓRIO DE ANÁLISE DE FORMULÁRIOS E COOKIES")
        print("="*80)
        print(f"\n🎯 Alvo: {results['target']}")
        print(f"⏰ Data/Hora: {results['timestamp']}")
        
        print(f"\n📝 Formulários encontrados: {len(results['forms'])}")
        print(f"🍪 Cookies encontrados: {len(results['cookies'])}")
        print(f"⚠️  Problemas de segurança: {len(results['security_issues'])}")
        
        if results['recommendations']:
            print(f"\n💡 RECOMENDAÇÕES ({len(results['recommendations'])}):")
            for rec in results['recommendations']:
                print(f"  • {rec}")
        
        print("\n" + "="*80)
        
        # Salvar em JSON
        filename = f"form_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório salvo em: {filename}")

def main():
    """Função principal"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3.11 real_form_analyzer.py <URL>")
        print("Exemplo: python3.11 real_form_analyzer.py https://example.com")
        sys.exit(1)
    
    target_url = sys.argv[1]
    
    analyzer = RealFormAnalyzer()
    results = analyzer.analyze_site(target_url)
    analyzer.generate_report(results)

if __name__ == "__main__":
    main()

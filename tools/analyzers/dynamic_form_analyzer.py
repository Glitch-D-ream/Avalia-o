#!/usr/bin/env python3.11
"""
Analisador Dinâmico de Formulários e Cookies - Para SPAs
Usa renderização JavaScript para encontrar elementos dinâmicos.
"""

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DynamicFormAnalyzer:
    """Analisa formulários e cookies em Single Page Applications (SPAs)"""
    
    def __init__(self):
        self.session = HTMLSession()
        self.findings = []
        
    def analyze_site(self, url):
        """Analisa um site completo com renderização JS"""
        print(f"\n🔍 Analisando Dinamicamente: {url}")
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
            # 1. Renderizar a página com JS
            print("[1/4] Renderizando página com JavaScript (pode demorar)...")
            r = self.session.get(url, timeout=20)
            # Renderizar a página para executar o JS e carregar o formulário
            r.html.render(sleep=5, timeout=15) 
            
            # Usar o HTML renderizado
            soup = BeautifulSoup(r.html.html, 'html.parser')
            
            # 2. Analisar formulários
            print("[2/4] Analisando formulários no HTML renderizado...")
            results["forms"] = self._analyze_forms_from_soup(soup, url)
            
            # 3. Analisar cookies
            print("[3/4] Analisando cookies...")
            results["cookies"] = self._analyze_cookies_from_response(r)
            
            # 4. Analisar campos de entrada
            print("[4/4] Analisando campos de entrada...")
            results["inputs"] = self._analyze_inputs_from_soup(soup)
            
            # Gerar recomendações
            results["recommendations"] = self._generate_recommendations(results)
            
            print("\n✅ Análise dinâmica completa!")
            
        except Exception as e:
            results["error"] = str(e)
            print(f"\n❌ Erro durante análise dinâmica: {e}")
        
        return results
    
    def _analyze_forms_from_soup(self, soup, base_url):
        """Função auxiliar para analisar formulários"""
        forms = soup.find_all('form')
        form_data = []
        for idx, form in enumerate(forms, 1):
            action = form.get('action', '')
            method = form.get('method', 'GET').upper()
            
            if action:
                action_url = urljoin(base_url, action)
            else:
                action_url = base_url
            
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
                }
                form_info["inputs"].append(input_info)
                
                if 'csrf' in input_info["name"].lower() or 'token' in input_info["name"].lower():
                    form_info["has_csrf_token"] = True
            
            # Verificar problemas de segurança
            if not form_info["has_csrf_token"] and method == "POST":
                form_info["security_issues"].append("Sem proteção CSRF")
            
            if not action_url.startswith("https://"):
                form_info["security_issues"].append("Formulário não usa HTTPS")
            
            password_fields = [i for i in form_info["inputs"] if i["type"] == "password"]
            if password_fields and not action_url.startswith("https://"):
                form_info["security_issues"].append("Campo de senha sem HTTPS")
            
            form_data.append(form_info)
            
            print(f"  ✓ Formulário {idx}: {method} -> {action_url}")
            if form_info["security_issues"]:
                for issue in form_info["security_issues"]:
                    print(f"    ⚠️  {issue}")
        
        return form_data

    def _analyze_cookies_from_response(self, response):
        """Função auxiliar para analisar cookies"""
        cookies = {}
        for cookie in response.cookies:
            cookie_info = {
                "value": cookie.value[:20] + "..." if len(cookie.value) > 20 else cookie.value,
                "domain": cookie.domain,
                "secure": cookie.secure,
                "httponly": cookie.has_nonstandard_attr('HttpOnly'),
                "samesite": cookie.get_nonstandard_attr('SameSite', 'None'),
                "security_issues": []
            }
            
            if not cookie.secure:
                cookie_info["security_issues"].append("Sem flag Secure")
            
            if not cookie.has_nonstandard_attr('HttpOnly'):
                cookie_info["security_issues"].append("Sem flag HttpOnly")
            
            cookies[cookie.name] = cookie_info
            
            print(f"  🍪 Cookie: {cookie.name}")
            if cookie_info["security_issues"]:
                for issue in cookie_info["security_issues"]:
                    print(f"    ⚠️  {issue}")
        
        return cookies

    def _analyze_inputs_from_soup(self, soup):
        """Função auxiliar para analisar inputs"""
        inputs = []
        for input_tag in soup.find_all(['input', 'textarea']):
            input_info = {
                "type": input_tag.get('type', 'text'),
                "name": input_tag.get('name', ''),
                "id": input_tag.get('id', ''),
                "placeholder": input_tag.get('placeholder', ''),
                "security_notes": []
            }
            
            if input_info["type"] == "password" and input_tag.get('autocomplete', 'on') == "on":
                input_info["security_notes"].append("Autocomplete habilitado em senha")
            
            inputs.append(input_info)
        
        return inputs

    def _generate_recommendations(self, results):
        """Função auxiliar para gerar recomendações"""
        recommendations = []
        
        for form in results.get("forms", []):
            if "Sem proteção CSRF" in form.get("security_issues", []):
                recommendations.append("Implementar proteção CSRF em formulários POST")
            if "Formulário não usa HTTPS" in form.get("security_issues", []):
                recommendations.append("Usar HTTPS para todos os formulários")
        
        for cookie_name, cookie_data in results.get("cookies", {}).items():
            if "Sem flag Secure" in cookie_data.get("security_issues", []):
                recommendations.append(f"Adicionar flag Secure ao cookie {cookie_name}")
            if "Sem flag HttpOnly" in cookie_data.get("security_issues", []):
                recommendations.append(f"Adicionar flag HttpOnly ao cookie {cookie_name}")
        
        return list(set(recommendations))
    
    def generate_report(self, results):
        """Gera relatório formatado"""
        print("\n" + "="*80)
        print("📋 RELATÓRIO DE ANÁLISE DINÂMICA (SPA)")
        print("="*80)
        print(f"\n🎯 Alvo: {results['target']}")
        print(f"⏰ Data/Hora: {results['timestamp']}")
        
        print(f"\n📝 Formulários encontrados: {len(results['forms'])}")
        print(f"🍪 Cookies encontrados: {len(results['cookies'])}")
        
        if results['recommendations']:
            print(f"\n💡 RECOMENDAÇÕES ({len(results['recommendations'])}):")
            for rec in results['recommendations']:
                print(f"  • {rec}")
        
        print("\n" + "="*80)
        
        # Salvar em JSON
        filename = f"dynamic_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório salvo em: {filename}")

def main():
    """Função principal"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3.11 dynamic_form_analyzer.py <URL>")
        print("Exemplo: python3.11 dynamic_form_analyzer.py https://example.com")
        sys.exit(1)
    
    target_url = sys.argv[1]
    
    analyzer = DynamicFormAnalyzer()
    results = analyzer.analyze_site(target_url)
    analyzer.generate_report(results)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Dynamic Form Hunter - Analisador de Formulários Dinâmicos em SPAs
Ferramenta criativa para detectar formulários gerados por JavaScript
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

class DynamicFormHunter:
    """Caçador de formulários dinâmicos em SPAs"""
    
    def __init__(self, target_url, timeout=15):
        """
        Inicializa o caçador
        
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
        self.forms_found = []
        self.js_files = []
        self.api_endpoints = []
        
    def hunt(self):
        """
        Executa caça completa de formulários
        
        Returns:
            dict: Relatório de formulários encontrados
        """
        print(f"\n🎯 Dynamic Form Hunter - Iniciando Caça")
        print(f"🌐 Alvo: {self.target_url}")
        print("="*80)
        
        report = {
            "target": self.target_url,
            "timestamp": datetime.now().isoformat(),
            "static_forms": [],
            "dynamic_forms": [],
            "js_files": [],
            "api_endpoints": [],
            "validation_rules": [],
            "total_forms": 0
        }
        
        try:
            # 1. Detectar formulários estáticos (HTML)
            print("\n[1/5] 📄 Detectando formulários estáticos...")
            report["static_forms"] = self.detect_static_forms()
            
            # 2. Analisar JavaScript para formulários dinâmicos
            print("[2/5] 📜 Analisando JavaScript...")
            report["js_files"] = self.analyze_javascript()
            
            # 3. Detectar endpoints de API
            print("[3/5] 🔗 Detectando endpoints de API...")
            report["api_endpoints"] = self.detect_api_endpoints()
            
            # 4. Extrair regras de validação
            print("[4/5] ✅ Extraindo regras de validação...")
            report["validation_rules"] = self.extract_validation_rules()
            
            # 5. Inferir formulários dinâmicos
            print("[5/5] 🔍 Inferindo formulários dinâmicos...")
            report["dynamic_forms"] = self.infer_dynamic_forms()
            
            report["total_forms"] = len(report["static_forms"]) + len(report["dynamic_forms"])
            
            print(f"\n✅ Caça completa!")
            print(f"📊 Formulários estáticos: {len(report['static_forms'])}")
            print(f"📊 Formulários dinâmicos: {len(report['dynamic_forms'])}")
            print(f"📊 Endpoints de API: {len(report['api_endpoints'])}")
            
        except Exception as e:
            report["error"] = str(e)
            print(f"\n❌ Erro durante caça: {e}")
        
        return report
    
    def detect_static_forms(self):
        """Detecta formulários HTML estáticos"""
        try:
            response = self.session.get(self.target_url, timeout=self.timeout, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            forms = []
            for form in soup.find_all('form'):
                form_info = {
                    "type": "static",
                    "action": form.get('action', ''),
                    "method": form.get('method', 'GET').upper(),
                    "fields": [],
                    "has_password": False,
                    "has_email": False
                }
                
                # Extrair campos
                for input_tag in form.find_all(['input', 'textarea', 'select']):
                    field = {
                        "name": input_tag.get('name', ''),
                        "type": input_tag.get('type', 'text'),
                        "id": input_tag.get('id', ''),
                        "required": input_tag.has_attr('required'),
                        "placeholder": input_tag.get('placeholder', '')
                    }
                    form_info["fields"].append(field)
                    
                    # Detectar campos especiais
                    if field["type"] == "password":
                        form_info["has_password"] = True
                    if field["type"] == "email" or "email" in field["name"].lower():
                        form_info["has_email"] = True
                
                forms.append(form_info)
                print(f"  ✅ Formulário estático: {form_info['method']} {form_info['action']}")
            
            return forms
            
        except Exception as e:
            print(f"  ❌ Erro ao detectar formulários estáticos: {e}")
            return []
    
    def analyze_javascript(self):
        """Analisa arquivos JavaScript"""
        try:
            response = self.session.get(self.target_url, timeout=self.timeout, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            js_files = []
            
            # Encontrar scripts externos
            for script in soup.find_all('script', src=True):
                js_url = urljoin(self.target_url, script['src'])
                js_files.append({
                    "url": js_url,
                    "type": "external"
                })
                self.js_files.append(js_url)
            
            # Analisar scripts inline
            for script in soup.find_all('script', src=False):
                if script.string:
                    js_files.append({
                        "content": script.string[:500],  # Primeiros 500 caracteres
                        "type": "inline"
                    })
            
            print(f"  ✅ Arquivos JS encontrados: {len(js_files)}")
            return js_files
            
        except Exception as e:
            print(f"  ❌ Erro ao analisar JavaScript: {e}")
            return []
    
    def detect_api_endpoints(self):
        """Detecta endpoints de API no JavaScript"""
        endpoints = []
        
        # Padrões de endpoints comuns
        patterns = [
            r'["\']https?://[^"\']+/api/[^"\']+["\']',
            r'["\']\/api\/[^"\']+["\']',
            r'fetch\(["\']([^"\']+)["\']',
            r'axios\.[a-z]+\(["\']([^"\']+)["\']',
            r'\.post\(["\']([^"\']+)["\']',
            r'\.get\(["\']([^"\']+)["\']'
        ]
        
        for js_url in self.js_files:
            try:
                response = self.session.get(js_url, timeout=self.timeout, verify=False)
                js_content = response.text
                
                for pattern in patterns:
                    matches = re.findall(pattern, js_content)
                    for match in matches:
                        endpoint = match.strip('"\'')
                        if endpoint and endpoint not in [e["url"] for e in endpoints]:
                            endpoints.append({
                                "url": endpoint,
                                "source": js_url,
                                "method": "POST" if "post" in pattern else "GET"
                            })
                            print(f"  ✅ Endpoint encontrado: {endpoint}")
            except Exception as e:
                print(f"  ⚠️  Erro ao analisar {js_url}: {e}")
        
        self.api_endpoints = endpoints
        return endpoints
    
    def extract_validation_rules(self):
        """Extrai regras de validação do JavaScript"""
        validation_rules = []
        
        # Padrões de validação comuns
        patterns = {
            "email": r'["\']email["\'].*?pattern.*?["\']([^"\']+)["\']',
            "password": r'["\']password["\'].*?minLength.*?(\d+)',
            "phone": r'["\']phone["\'].*?pattern.*?["\']([^"\']+)["\']',
            "required": r'required:\s*(true|false)',
            "minLength": r'minLength:\s*(\d+)',
            "maxLength": r'maxLength:\s*(\d+)'
        }
        
        for js_url in self.js_files:
            try:
                response = self.session.get(js_url, timeout=self.timeout, verify=False)
                js_content = response.text
                
                for rule_type, pattern in patterns.items():
                    matches = re.findall(pattern, js_content, re.IGNORECASE)
                    if matches:
                        validation_rules.append({
                            "type": rule_type,
                            "value": matches[0],
                            "source": js_url
                        })
                        print(f"  ✅ Regra de validação: {rule_type} = {matches[0]}")
            except Exception as e:
                print(f"  ⚠️  Erro ao extrair validações: {e}")
        
        return validation_rules
    
    def infer_dynamic_forms(self):
        """Infere formulários dinâmicos baseado em endpoints e validações"""
        dynamic_forms = []
        
        # Agrupar endpoints por tipo (login, register, etc.)
        login_keywords = ['login', 'signin', 'auth', 'authenticate']
        register_keywords = ['register', 'signup', 'create', 'account']
        
        for endpoint in self.api_endpoints:
            endpoint_url = endpoint["url"].lower()
            
            # Detectar formulário de login
            if any(keyword in endpoint_url for keyword in login_keywords):
                form = {
                    "type": "dynamic",
                    "form_type": "login",
                    "action": endpoint["url"],
                    "method": endpoint["method"],
                    "fields": [
                        {
                            "name": "username",
                            "type": "text",
                            "required": True,
                            "inferred": True
                        },
                        {
                            "name": "password",
                            "type": "password",
                            "required": True,
                            "inferred": True
                        }
                    ]
                }
                dynamic_forms.append(form)
                print(f"  ✅ Formulário dinâmico inferido: LOGIN em {endpoint['url']}")
            
            # Detectar formulário de registro
            elif any(keyword in endpoint_url for keyword in register_keywords):
                form = {
                    "type": "dynamic",
                    "form_type": "register",
                    "action": endpoint["url"],
                    "method": endpoint["method"],
                    "fields": [
                        {
                            "name": "username",
                            "type": "text",
                            "required": True,
                            "inferred": True
                        },
                        {
                            "name": "email",
                            "type": "email",
                            "required": True,
                            "inferred": True
                        },
                        {
                            "name": "password",
                            "type": "password",
                            "required": True,
                            "inferred": True
                        }
                    ]
                }
                dynamic_forms.append(form)
                print(f"  ✅ Formulário dinâmico inferido: REGISTER em {endpoint['url']}")
        
        return dynamic_forms
    
    def generate_payloads(self, form):
        """Gera payloads de teste para um formulário"""
        payloads = []
        
        if form["form_type"] == "login":
            payloads = [
                {"username": "admin", "password": "admin"},
                {"username": "admin", "password": "admin123"},
                {"username": "test", "password": "test"},
                {"username": "user", "password": "password"}
            ]
        elif form["form_type"] == "register":
            payloads = [
                {
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "Test123!"
                }
            ]
        
        return payloads
    
    def save_report(self, output_file="form_hunter_report.json"):
        """Salva relatório em JSON"""
        report = self.hunt()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório salvo em: {output_file}")
        return report


# Exemplo de uso
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "https://99jogo66.com/?id=211995351"
        print(f"⚠️  Nenhum alvo especificado, usando alvo do concurso: {target}")
        print(f"💡 Uso: python3 dynamic_form_hunter.py <URL>")
        print()
    
    hunter = DynamicFormHunter(target)
    report = hunter.save_report()
    
    print("\n" + "="*80)
    print("📊 RESUMO DA CAÇA")
    print("="*80)
    print(f"🎯 Alvo: {report['target']}")
    print(f"📄 Formulários estáticos: {len(report['static_forms'])}")
    print(f"🔍 Formulários dinâmicos: {len(report['dynamic_forms'])}")
    print(f"🔗 Endpoints de API: {len(report['api_endpoints'])}")
    print(f"✅ Regras de validação: {len(report['validation_rules'])}")
    
    if report['dynamic_forms']:
        print("\n🎯 Formulários Dinâmicos Encontrados:")
        for i, form in enumerate(report['dynamic_forms'], 1):
            print(f"  {i}. {form['form_type'].upper()} - {form['action']}")
            print(f"     Campos: {', '.join([f['name'] for f in form['fields']])}")

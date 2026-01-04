#!/usr/bin/env python3
"""
Advanced SPA Analyzer - Análise Profissional de Single Page Applications
Autor: ASCENSÃO - CULTIVO DIGITAL v4.0
Descrição: Ferramenta avançada para análise de SPAs modernas (Vue, React, Angular)
           usando Selenium para renderização completa e interceptação de rede.
"""

import json
import time
import re
from datetime import datetime
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from bs4 import BeautifulSoup

class AdvancedSPAAnalyzer:
    """Analisador avançado de Single Page Applications"""
    
    def __init__(self, target_url, headless=True):
        self.target_url = target_url
        self.headless = headless
        self.driver = None
        self.network_logs = []
        self.api_endpoints = []
        self.forms_found = []
        self.credentials_endpoints = []
        self.websockets = []
        self.local_storage = {}
        self.session_storage = {}
        self.cookies = []
        
    def setup_driver(self):
        """Configura o Selenium WebDriver com capacidades de interceptação de rede"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Habilitar logging de rede
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL', 'browser': 'ALL'})
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(30)
        
        print("✅ Selenium WebDriver configurado com sucesso")
        
    def load_page(self):
        """Carrega a página e aguarda renderização completa"""
        print(f"🌐 Carregando página: {self.target_url}")
        self.driver.get(self.target_url)
        
        # Aguardar carregamento inicial
        time.sleep(3)
        
        # Aguardar Vue/React/Angular inicializar
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            print("✅ Página carregada completamente")
        except TimeoutException:
            print("⚠️  Timeout ao carregar página, continuando...")
            
    def capture_network_traffic(self):
        """Captura todo o tráfego de rede (XHR, Fetch, WebSocket)"""
        print("📡 Capturando tráfego de rede...")
        
        logs = self.driver.get_log('performance')
        
        for entry in logs:
            try:
                log = json.loads(entry['message'])['message']
                
                # Capturar requisições de rede
                if log['method'] == 'Network.requestWillBeSent':
                    request = log['params']['request']
                    url = request['url']
                    method = request['method']
                    
                    # Filtrar apenas requisições relevantes
                    if any(keyword in url.lower() for keyword in ['api', 'login', 'auth', 'register', 'user', 'account']):
                        network_entry = {
                            'url': url,
                            'method': method,
                            'headers': request.get('headers', {}),
                            'postData': request.get('postData', None),
                            'timestamp': datetime.now().isoformat()
                        }
                        self.network_logs.append(network_entry)
                        
                        # Identificar endpoints de API
                        if '/api/' in url or method in ['POST', 'PUT', 'PATCH']:
                            self.api_endpoints.append({
                                'url': url,
                                'method': method,
                                'type': self._classify_endpoint(url)
                            })
                            
                # Capturar WebSockets
                elif log['method'] == 'Network.webSocketCreated':
                    ws_url = log['params']['url']
                    self.websockets.append(ws_url)
                    
            except Exception as e:
                continue
                
        print(f"✅ Tráfego capturado: {len(self.network_logs)} requisições")
        print(f"✅ Endpoints de API encontrados: {len(self.api_endpoints)}")
        print(f"✅ WebSockets detectados: {len(self.websockets)}")
        
    def _classify_endpoint(self, url):
        """Classifica o tipo de endpoint baseado na URL"""
        url_lower = url.lower()
        
        if any(keyword in url_lower for keyword in ['login', 'signin', 'auth']):
            return 'LOGIN'
        elif any(keyword in url_lower for keyword in ['register', 'signup', 'create']):
            return 'REGISTER'
        elif any(keyword in url_lower for keyword in ['user', 'profile', 'account']):
            return 'USER_INFO'
        elif any(keyword in url_lower for keyword in ['password', 'reset', 'forgot']):
            return 'PASSWORD'
        else:
            return 'OTHER'
            
    def find_dynamic_forms(self):
        """Encontra formulários dinâmicos renderizados por JavaScript"""
        print("🔍 Procurando formulários dinâmicos...")
        
        # Procurar por todos os formulários
        forms = self.driver.find_elements(By.TAG_NAME, 'form')
        
        for idx, form in enumerate(forms):
            try:
                form_data = {
                    'id': form.get_attribute('id') or f'form_{idx}',
                    'action': form.get_attribute('action') or 'dynamic',
                    'method': form.get_attribute('method') or 'POST',
                    'fields': []
                }
                
                # Encontrar todos os inputs
                inputs = form.find_elements(By.TAG_NAME, 'input')
                for input_elem in inputs:
                    field = {
                        'type': input_elem.get_attribute('type'),
                        'name': input_elem.get_attribute('name'),
                        'id': input_elem.get_attribute('id'),
                        'placeholder': input_elem.get_attribute('placeholder'),
                        'required': input_elem.get_attribute('required') is not None
                    }
                    form_data['fields'].append(field)
                    
                self.forms_found.append(form_data)
                
            except Exception as e:
                continue
                
        print(f"✅ Formulários encontrados: {len(self.forms_found)}")
        
        # Procurar por botões de login/registro mesmo sem formulário
        self._find_login_buttons()
        
    def _find_login_buttons(self):
        """Procura por botões de login/registro"""
        keywords = ['login', 'entrar', 'signin', 'register', 'cadastro', 'signup']
        
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        buttons += self.driver.find_elements(By.CSS_SELECTOR, '[role="button"]')
        
        for button in buttons:
            try:
                text = button.text.lower()
                if any(keyword in text for keyword in keywords):
                    print(f"  🎯 Botão encontrado: '{button.text}'")
                    
                    # Tentar clicar e ver o que acontece
                    self._test_button_interaction(button)
                    
            except Exception as e:
                continue
                
    def _test_button_interaction(self, button):
        """Testa interação com botão para revelar formulários"""
        try:
            # Scroll até o botão
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.5)
            
            # Clicar no botão
            button.click()
            time.sleep(2)
            
            # Capturar novos elementos que apareceram
            self.find_dynamic_forms()
            self.capture_network_traffic()
            
        except Exception as e:
            pass
            
    def extract_javascript_endpoints(self):
        """Extrai endpoints de API do código JavaScript"""
        print("📜 Analisando código JavaScript...")
        
        # Obter todos os scripts
        scripts = self.driver.find_elements(By.TAG_NAME, 'script')
        
        endpoint_patterns = [
            r'["\']/(api|auth|login|register|user)/[^"\']+["\']',
            r'https?://[^"\']+/(api|auth|login|register)[^"\']*',
            r'endpoint["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'url["\']?\s*[:=]\s*["\']([^"\']+)["\']'
        ]
        
        for script in scripts:
            try:
                content = script.get_attribute('innerHTML')
                if not content:
                    continue
                    
                for pattern in endpoint_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match[0] if match else ''
                        
                        # Limpar e validar
                        endpoint = match.strip('\'"')
                        if endpoint and len(endpoint) > 5:
                            full_url = urljoin(self.target_url, endpoint)
                            if full_url not in [e['url'] for e in self.api_endpoints]:
                                self.api_endpoints.append({
                                    'url': full_url,
                                    'method': 'UNKNOWN',
                                    'type': self._classify_endpoint(full_url),
                                    'source': 'javascript'
                                })
                                
            except Exception as e:
                continue
                
        print(f"✅ Endpoints extraídos do JavaScript: {len([e for e in self.api_endpoints if e.get('source') == 'javascript'])}")
        
    def extract_storage_data(self):
        """Extrai dados do localStorage e sessionStorage"""
        print("💾 Extraindo dados de armazenamento...")
        
        # LocalStorage
        try:
            local_storage = self.driver.execute_script("return window.localStorage;")
            self.local_storage = dict(local_storage) if local_storage else {}
            print(f"  ✅ LocalStorage: {len(self.local_storage)} itens")
        except Exception as e:
            print(f"  ⚠️  Erro ao acessar localStorage: {e}")
            
        # SessionStorage
        try:
            session_storage = self.driver.execute_script("return window.sessionStorage;")
            self.session_storage = dict(session_storage) if session_storage else {}
            print(f"  ✅ SessionStorage: {len(self.session_storage)} itens")
        except Exception as e:
            print(f"  ⚠️  Erro ao acessar sessionStorage: {e}")
            
        # Cookies
        self.cookies = self.driver.get_cookies()
        print(f"  ✅ Cookies: {len(self.cookies)} itens")
        
    def detect_framework(self):
        """Detecta o framework JavaScript usado"""
        print("🔧 Detectando framework...")
        
        frameworks = {
            'Vue': 'window.Vue || document.querySelector("[data-v-]")',
            'React': 'window.React || document.querySelector("[data-reactroot]")',
            'Angular': 'window.ng || document.querySelector("[ng-version]")',
            'jQuery': 'window.jQuery',
            'Svelte': 'document.querySelector("[data-svelte]")'
        }
        
        detected = []
        for name, check in frameworks.items():
            try:
                result = self.driver.execute_script(f'return !!({check});')
                if result:
                    detected.append(name)
                    print(f"  ✅ Framework detectado: {name}")
            except:
                pass
                
        return detected
        
    def test_api_endpoints(self):
        """Testa endpoints de API descobertos"""
        print("🧪 Testando endpoints de API...")
        
        credentials_keywords = ['login', 'auth', 'register', 'signin', 'signup']
        
        for endpoint in self.api_endpoints:
            url = endpoint['url']
            
            # Verificar se é endpoint de credenciais
            if any(keyword in url.lower() for keyword in credentials_keywords):
                self.credentials_endpoints.append(endpoint)
                print(f"  🎯 Endpoint de credenciais: {endpoint['method']} {url}")
                
                # Testar endpoint
                self._test_endpoint(endpoint)
                
    def _test_endpoint(self, endpoint):
        """Testa um endpoint específico"""
        url = endpoint['url']
        method = endpoint.get('method', 'POST')
        
        # Payload de teste
        test_payloads = [
            {'username': 'admin', 'password': 'admin'},
            {'email': 'test@test.com', 'password': '123456'},
            {'user': 'admin', 'pass': 'admin123'}
        ]
        
        for payload in test_payloads:
            try:
                if method == 'POST':
                    response = requests.post(url, json=payload, timeout=5, verify=False)
                elif method == 'GET':
                    response = requests.get(url, params=payload, timeout=5, verify=False)
                else:
                    continue
                    
                print(f"    📊 Status: {response.status_code} | Payload: {payload}")
                
                # Analisar resposta
                if response.status_code in [200, 201]:
                    print(f"    ✅ Resposta positiva! Possível vulnerabilidade")
                elif response.status_code == 401:
                    print(f"    🔒 Autenticação necessária (esperado)")
                elif response.status_code == 400:
                    print(f"    ⚠️  Bad Request - endpoint válido mas payload incorreto")
                    
            except Exception as e:
                print(f"    ❌ Erro ao testar: {str(e)[:50]}")
                
    def generate_report(self):
        """Gera relatório completo da análise"""
        report = {
            'target': self.target_url,
            'timestamp': datetime.now().isoformat(),
            'analysis': {
                'frameworks_detected': self.detect_framework(),
                'network_requests': len(self.network_logs),
                'api_endpoints': len(self.api_endpoints),
                'forms_found': len(self.forms_found),
                'credentials_endpoints': len(self.credentials_endpoints),
                'websockets': len(self.websockets)
            },
            'api_endpoints': self.api_endpoints,
            'credentials_endpoints': self.credentials_endpoints,
            'forms': self.forms_found,
            'websockets': self.websockets,
            'storage': {
                'localStorage': self.local_storage,
                'sessionStorage': self.session_storage,
                'cookies': [{'name': c['name'], 'value': c['value'][:50]} for c in self.cookies]
            },
            'network_logs': self.network_logs[:50]  # Limitar para não ficar muito grande
        }
        
        # Salvar relatório
        report_file = 'advanced_spa_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\n💾 Relatório salvo em: {report_file}")
        
        return report
        
    def full_analysis(self):
        """Executa análise completa"""
        print("=" * 80)
        print("🚀 Advanced SPA Analyzer - Análise Completa")
        print("=" * 80)
        
        try:
            # 1. Configurar driver
            self.setup_driver()
            
            # 2. Carregar página
            self.load_page()
            
            # 3. Detectar framework
            self.detect_framework()
            
            # 4. Aguardar carregamento completo
            time.sleep(5)
            
            # 5. Capturar tráfego de rede
            self.capture_network_traffic()
            
            # 6. Encontrar formulários dinâmicos
            self.find_dynamic_forms()
            
            # 7. Extrair endpoints do JavaScript
            self.extract_javascript_endpoints()
            
            # 8. Extrair dados de armazenamento
            self.extract_storage_data()
            
            # 9. Testar endpoints de API
            self.test_api_endpoints()
            
            # 10. Gerar relatório
            report = self.generate_report()
            
            print("\n" + "=" * 80)
            print("📊 RESUMO DA ANÁLISE")
            print("=" * 80)
            print(f"🎯 Alvo: {self.target_url}")
            print(f"📡 Requisições de rede: {len(self.network_logs)}")
            print(f"🔗 Endpoints de API: {len(self.api_endpoints)}")
            print(f"🔑 Endpoints de credenciais: {len(self.credentials_endpoints)}")
            print(f"📝 Formulários: {len(self.forms_found)}")
            print(f"🌐 WebSockets: {len(self.websockets)}")
            print(f"💾 LocalStorage: {len(self.local_storage)} itens")
            print(f"🍪 Cookies: {len(self.cookies)} itens")
            
            if self.credentials_endpoints:
                print("\n🎯 ENDPOINTS DE CREDENCIAIS ENCONTRADOS:")
                for endpoint in self.credentials_endpoints:
                    print(f"  • {endpoint['method']} {endpoint['url']} ({endpoint['type']})")
                    
            return report
            
        finally:
            if self.driver:
                self.driver.quit()
                print("\n✅ Análise concluída e driver fechado")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3 advanced_spa_analyzer.py <URL>")
        print("Exemplo: python3 advanced_spa_analyzer.py https://99jogo66.com/?id=211995351")
        sys.exit(1)
        
    target_url = sys.argv[1]
    headless = '--no-headless' not in sys.argv
    
    analyzer = AdvancedSPAAnalyzer(target_url, headless=headless)
    analyzer.full_analysis()

if __name__ == '__main__':
    main()

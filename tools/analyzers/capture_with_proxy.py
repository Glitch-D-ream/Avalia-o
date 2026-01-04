#!/usr/bin/env python3
"""
Script para fazer requisições ao site alvo através do proxy SOCKS4
e capturar o tráfego com o ZAP.
"""

import requests
import json
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configuração do proxy SOCKS4
PROXY_SOCKS4 = "socks4://177.126.89.63:4145"

# Configuração do site alvo
TARGET_URL = "https://99jogo66.com/?id=211995351"
LOGIN_ENDPOINT = "https://99jogo66.com/api/login"
REGISTER_ENDPOINT = "https://99jogo66.com/api/register"

# Configuração do ZAP
ZAP_HOST = "127.0.0.1"
ZAP_PORT = 8080
ZAP_URL = f"http://{ZAP_HOST}:{ZAP_PORT}"

def create_session_with_proxy():
    """Cria uma sessão requests com proxy SOCKS4"""
    session = requests.Session()
    
    # Configurar retry strategy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS", "POST"],
        backoff_factor=1
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Configurar proxy
    session.proxies = {
        "http": PROXY_SOCKS4,
        "https": PROXY_SOCKS4
    }
    
    # Configurar headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    return session

def test_site_access():
    """Testa o acesso ao site alvo através do proxy"""
    print("[*] Testando acesso ao site alvo através do proxy SOCKS4...")
    
    session = create_session_with_proxy()
    
    try:
        response = session.get(TARGET_URL, timeout=10, verify=False)
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Tamanho da resposta: {len(response.content)} bytes")
        
        # Procurar por endpoints de API no HTML
        if "api" in response.text.lower():
            print("[+] Encontradas referências a API no HTML")
            
            # Procurar por URLs de API
            import re
            api_urls = re.findall(r'["\']([^"\']*api[^"\']*)["\']', response.text, re.IGNORECASE)
            if api_urls:
                print("[+] URLs de API encontradas:")
                for url in api_urls[:5]:
                    print(f"    - {url}")
        
        return True
    except Exception as e:
        print(f"[-] Erro ao acessar o site: {e}")
        return False

def test_login_endpoint():
    """Testa o endpoint de login com dados de teste"""
    print("\n[*] Testando o endpoint de login...")
    
    session = create_session_with_proxy()
    
    # Dados de teste
    test_data = {
        "account": "test_user",
        "password": "test_password"
    }
    
    try:
        response = session.post(
            LOGIN_ENDPOINT,
            json=test_data,
            timeout=10,
            verify=False,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Resposta: {response.text[:500]}")
        
        # Tentar parsear como JSON
        try:
            json_response = response.json()
            print(f"[+] Resposta JSON: {json.dumps(json_response, indent=2)[:500]}")
        except:
            pass
        
        return response
    except Exception as e:
        print(f"[-] Erro ao testar endpoint de login: {e}")
        return None

def get_zap_history():
    """Obtém o histórico de requisições capturadas pelo ZAP"""
    print("\n[*] Obtendo histórico de requisições do ZAP...")
    
    try:
        response = requests.get(f"{ZAP_URL}/JSON/core/view/messages", timeout=10)
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            print(f"[+] Total de requisições capturadas: {len(messages)}")
            
            # Filtrar requisições POST
            post_requests = [m for m in messages if m.get("method") == "POST"]
            print(f"[+] Requisições POST capturadas: {len(post_requests)}")
            
            # Salvar em arquivo
            with open("zap_captured_traffic.json", "w") as f:
                json.dump(messages, f, indent=2)
            print(f"[+] Tráfego salvo em 'zap_captured_traffic.json'")
            
            return messages
    except Exception as e:
        print(f"[-] Erro ao obter histórico do ZAP: {e}")
    
    return []

def main():
    print("="*80)
    print("CAPTURA DE TRÁFEGO COM PROXY SOCKS4 E OWASP ZAP")
    print("="*80)
    
    # Testar acesso ao site
    if not test_site_access():
        print("\n❌ Não foi possível acessar o site alvo.")
        return
    
    # Testar endpoint de login
    test_login_endpoint()
    
    # Obter histórico do ZAP
    time.sleep(2)
    get_zap_history()
    
    print("\n✅ Captura de tráfego concluída!")

if __name__ == "__main__":
    main()

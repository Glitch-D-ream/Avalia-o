#!/usr/bin/env python3
"""
Script para testar endpoints de API diretamente através do proxy SOCKS4
e capturar o tráfego com o OWASP ZAP.
"""

import requests
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuração do proxy SOCKS4
PROXY_SOCKS4 = "socks4://177.126.89.63:4145"

# Configuração do site alvo
TARGET_BASE = "https://99jogo66.com"
ENDPOINTS = [
    "/api/login",
    "/api/register",
    "/api/auth/login",
    "/api/auth/register",
    "/api/user/login",
    "/api/user/register",
    "/api/v1/login",
    "/api/v1/register",
    "/api/v1/auth/login",
    "/api/v1/auth/register",
]

# Configuração do ZAP
ZAP_URL = "http://127.0.0.1:8080"

def create_session_with_proxy():
    """Cria uma sessão requests com proxy SOCKS4"""
    session = requests.Session()
    
    # Configurar retry strategy
    retry_strategy = Retry(
        total=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/json'
    })
    
    return session

def test_endpoints():
    """Testa os endpoints de API"""
    print("="*80)
    print("TESTE DE ENDPOINTS DE API COM PROXY SOCKS4")
    print("="*80)
    
    session = create_session_with_proxy()
    
    # Dados de teste
    test_payloads = [
        {"account": "test_user", "password": "test_password"},
        {"username": "test_user", "password": "test_password"},
        {"email": "test@test.com", "password": "test_password"},
        {"phone": "11999999999", "password": "test_password"},
        {"account": "test_user", "password": "test_password", "code": ""},
        {"account": "test_user", "password": "test_password", "captcha": ""},
    ]
    
    results = []
    
    for endpoint in ENDPOINTS:
        full_url = TARGET_BASE + endpoint
        print(f"\n[*] Testando: {full_url}")
        
        for i, payload in enumerate(test_payloads):
            try:
                response = session.post(
                    full_url,
                    json=payload,
                    timeout=10,
                    verify=False
                )
                
                status = response.status_code
                print(f"    [+] Payload {i+1}: Status {status}")
                
                if status != 404 and status != 405:
                    print(f"        Resposta: {response.text[:200]}")
                    results.append({
                        "endpoint": endpoint,
                        "payload": payload,
                        "status": status,
                        "response": response.text[:500]
                    })
            
            except Exception as e:
                print(f"    [-] Erro: {str(e)[:100]}")
    
    # Salvar resultados
    with open("api_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] Resultados salvos em 'api_test_results.json'")
    
    return results

def get_zap_history():
    """Obtém o histórico de requisições capturadas pelo ZAP"""
    print("\n[*] Capturando histórico do ZAP...")
    try:
        response = requests.get(f"{ZAP_URL}/JSON/core/view/messages", timeout=10)
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            print(f"[+] Total de requisições capturadas: {len(messages)}")
            
            # Filtrar requisições POST para endpoints de API
            api_requests = [m for m in messages if "/api/" in m.get("url", "") and m.get("method") == "POST"]
            print(f"[+] Requisições POST para /api/: {len(api_requests)}")
            
            if api_requests:
                print("\n[*] Requisições de API encontradas:")
                for i, req in enumerate(api_requests[:10], 1):
                    print(f"\n--- Requisição {i} ---")
                    print(f"URL: {req.get('url', 'N/A')}")
                    print(f"Status: {req.get('status', 'N/A')}")
                    print(f"Corpo: {req.get('requestBody', 'N/A')[:300]}")
                    print(f"Resposta: {req.get('responseBody', 'N/A')[:300]}")
            
            # Salvar em arquivo
            with open("zap_api_traffic.json", "w") as f:
                json.dump(messages, f, indent=2)
            print(f"\n[+] Tráfego completo do ZAP salvo em 'zap_api_traffic.json'")
    except Exception as e:
        print(f"[-] Erro ao obter histórico do ZAP: {e}")

def main():
    print("\n[*] Iniciando testes de API...")
    time.sleep(1)
    
    results = test_endpoints()
    
    print("\n[*] Aguardando 3 segundos antes de capturar histórico do ZAP...")
    time.sleep(3)
    
    get_zap_history()
    
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para usar a API do OWASP ZAP para capturar o tráfego de login/registro
do site alvo através de um proxy HTTP.
"""

import requests
import time
import json
from urllib.parse import urljoin
import subprocess

# Configuração do ZAP
ZAP_HOST = "127.0.0.1"
ZAP_PORT = 8080
ZAP_URL = f"http://{ZAP_HOST}:{ZAP_PORT}"

# Configuração do site alvo
TARGET_URL = "https://99jogo66.com/?id=211995351"
TARGET_BASE = "https://99jogo66.com"

# Proxy SOCKS4 para contornar restrição geográfica
PROXY_SOCKS4 = "socks4://177.126.89.63:4145"

def test_zap_connection():
    """Testa se o ZAP está disponível"""
    try:
        response = requests.get(f"{ZAP_URL}/JSON/core/view/version", timeout=5)
        if response.status_code == 200:
            print(f"✅ ZAP conectado: {response.json()}")
            return True
    except Exception as e:
        print(f"❌ Erro ao conectar ao ZAP: {e}")
    return False

def get_zap_history():
    """Obtém o histórico de requisições capturadas pelo ZAP"""
    try:
        response = requests.get(f"{ZAP_URL}/JSON/core/view/messages", timeout=10)
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            return messages
    except Exception as e:
        print(f"Erro ao obter histórico do ZAP: {e}")
    return []

def filter_login_requests(messages):
    """Filtra requisições de login/registro do histórico"""
    login_requests = []
    
    for msg in messages:
        request_body = msg.get("requestBody", "")
        response_body = msg.get("responseBody", "")
        request_header = msg.get("requestHeader", "")
        method = msg.get("method", "")
        url = msg.get("url", "")
        
        # Procurar por requisições POST que contêm dados de login
        if method == "POST" and ("login" in url.lower() or "register" in url.lower() or "auth" in url.lower()):
            login_requests.append({
                "url": url,
                "method": method,
                "request_header": request_header,
                "request_body": request_body,
                "response_body": response_body[:500]  # Primeiros 500 caracteres
            })
        
        # Procurar por requisições que contêm campos de login/senha
        if "password" in request_body.lower() or "account" in request_body.lower():
            if method == "POST":
                login_requests.append({
                    "url": url,
                    "method": method,
                    "request_header": request_header,
                    "request_body": request_body,
                    "response_body": response_body[:500]
                })
    
    return login_requests

def main():
    print("[*] Iniciando captura de tráfego com OWASP ZAP...")
    
    # Testar conexão com ZAP
    if not test_zap_connection():
        print("❌ Não foi possível conectar ao ZAP. Certifique-se de que está em execução.")
        return
    
    print("\n[*] Aguardando 5 segundos para capturar tráfego...")
    time.sleep(5)
    
    # Obter histórico de requisições
    print("\n[*] Obtendo histórico de requisições capturadas...")
    messages = get_zap_history()
    print(f"[+] Total de requisições capturadas: {len(messages)}")
    
    # Filtrar requisições de login
    print("\n[*] Filtrando requisições de login/registro...")
    login_requests = filter_login_requests(messages)
    
    if login_requests:
        print(f"\n✅ Encontradas {len(login_requests)} requisições de login/registro:")
        
        for i, req in enumerate(login_requests, 1):
            print(f"\n--- Requisição {i} ---")
            print(f"URL: {req['url']}")
            print(f"Método: {req['method']}")
            print(f"Headers:\n{req['request_header'][:300]}")
            print(f"Corpo da Requisição:\n{req['request_body'][:300]}")
            print(f"Resposta (primeiros 300 caracteres):\n{req['response_body']}")
    else:
        print("\n❌ Nenhuma requisição de login/registro foi capturada.")
        print("[*] Mostrando todas as requisições capturadas:")
        for i, msg in enumerate(messages[:5], 1):
            print(f"\n--- Requisição {i} ---")
            print(f"URL: {msg.get('url', 'N/A')}")
            print(f"Método: {msg.get('method', 'N/A')}")
            print(f"Corpo: {msg.get('requestBody', 'N/A')[:200]}")
    
    # Salvar o histórico em um arquivo JSON
    with open("zap_history.json", "w") as f:
        json.dump(messages, f, indent=2)
    print(f"\n[+] Histórico completo salvo em 'zap_history.json'")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para encontrar o endpoint de login/registro do site alvo
através de análise de requisições HTTP e captura de tráfego.

O script fará requisições para o site alvo através do proxy mitmdump
e tentará identificar o endpoint de login/registro.
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin, urlparse

# Configuração do proxy
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8080
PROXY_URL = f"http://{PROXY_HOST}:{PROXY_PORT}"

# URL alvo
TARGET_URL = "https://99jogo66.com/?id=211995351"
TARGET_HOST = "99jogo66.com"

# Configurar o proxy para as requisições
proxies = {
    "http": PROXY_URL,
    "https": PROXY_URL,
}

# Desabilitar verificação de certificado SSL (para o mitmproxy)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def make_request(url, method="GET", data=None, headers=None):
    """
    Faz uma requisição HTTP através do proxy mitmdump.
    """
    try:
        if headers is None:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            }
        
        if method == "GET":
            response = requests.get(
                url,
                proxies=proxies,
                verify=False,
                timeout=10,
                headers=headers
            )
        elif method == "POST":
            response = requests.post(
                url,
                proxies=proxies,
                verify=False,
                timeout=10,
                headers=headers,
                data=data
            )
        
        return response
    except Exception as e:
        print(f"Erro ao fazer requisição: {e}")
        return None

def analyze_html_for_endpoints(html_content):
    """
    Analisa o HTML para encontrar endpoints de API ou formulários de login.
    """
    endpoints = []
    
    # Procura por padrões comuns de endpoints
    import re
    
    # Procura por URLs em atributos action de formulários
    form_actions = re.findall(r'action=["\']([^"\']+)["\']', html_content)
    endpoints.extend(form_actions)
    
    # Procura por URLs em fetch/XMLHttpRequest
    api_calls = re.findall(r'(?:fetch|XMLHttpRequest|axios)\(["\']([^"\']+)["\']', html_content)
    endpoints.extend(api_calls)
    
    # Procura por URLs em data-url ou data-endpoint
    data_urls = re.findall(r'data-(?:url|endpoint|api)=["\']([^"\']+)["\']', html_content)
    endpoints.extend(data_urls)
    
    # Procura por strings de API comuns
    api_patterns = re.findall(r'(?:api|endpoint|login|register|auth)["\']?\s*:\s*["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    endpoints.extend(api_patterns)
    
    return list(set(endpoints))  # Remove duplicatas

def test_common_endpoints():
    """
    Testa endpoints comuns de login/registro.
    """
    common_endpoints = [
        "/api/login",
        "/api/register",
        "/api/auth/login",
        "/api/auth/register",
        "/api/user/login",
        "/api/user/register",
        "/login",
        "/register",
        "/auth/login",
        "/auth/register",
        "/user/login",
        "/user/register",
        "/api/v1/login",
        "/api/v1/register",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
    ]
    
    print("\n[*] Testando endpoints comuns...")
    for endpoint in common_endpoints:
        url = urljoin(TARGET_URL, endpoint)
        print(f"  Testando: {url}", end=" ... ")
        response = make_request(url, method="POST", data={"test": "test"})
        if response:
            print(f"Status: {response.status_code}")
            if response.status_code != 404:
                print(f"    ✓ Endpoint encontrado! Status: {response.status_code}")
        else:
            print("Erro na requisição")

def main():
    print("[*] Iniciando análise do site alvo...")
    print(f"[*] URL Alvo: {TARGET_URL}")
    print(f"[*] Proxy: {PROXY_URL}")
    print(f"[*] Aguarde o mitmdump estar rodando na porta {PROXY_PORT}...")
    
    time.sleep(2)
    
    # Passo 1: Fazer uma requisição GET para obter o HTML da página
    print("\n[*] Fazendo requisição GET para a página inicial...")
    response = make_request(TARGET_URL)
    
    if response is None:
        print("[-] Erro ao acessar o site. Verifique se o proxy mitmdump está rodando.")
        sys.exit(1)
    
    print(f"[+] Resposta recebida. Status: {response.status_code}")
    
    # Passo 2: Analisar o HTML para encontrar endpoints
    print("\n[*] Analisando HTML para encontrar endpoints...")
    endpoints = analyze_html_for_endpoints(response.text)
    
    if endpoints:
        print("[+] Endpoints encontrados:")
        for endpoint in endpoints:
            print(f"  - {endpoint}")
    else:
        print("[-] Nenhum endpoint encontrado na análise do HTML")
    
    # Passo 3: Testar endpoints comuns
    test_common_endpoints()
    
    # Passo 4: Ler o log do mitmdump para verificar requisições POST capturadas
    print("\n[*] Verificando log de requisições POST capturadas pelo mitmdump...")
    try:
        with open("mitm_post_requests.log", "r") as f:
            log_content = f.read()
            if log_content:
                print("[+] Requisições POST capturadas:")
                print(log_content)
            else:
                print("[-] Nenhuma requisição POST capturada ainda")
    except FileNotFoundError:
        print("[-] Arquivo de log não encontrado. O mitmdump pode não estar capturando tráfego.")
    
    print("\n[*] Análise concluída!")
    print("[*] Próximas etapas:")
    print("  1. Abra o navegador e acesse o site através do proxy")
    print("  2. Tente fazer um login ou registro")
    print("  3. O endpoint será capturado no arquivo mitm_post_requests.log")

if __name__ == "__main__":
    main()

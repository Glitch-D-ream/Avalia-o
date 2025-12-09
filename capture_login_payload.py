#!/usr/bin/env python3
"""
Script para capturar o payload exato de login/registro
fazendo requisições diretas através do proxy SOCKS4.
"""

import requests
import json
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import socks
import socket

# Configuração do proxy SOCKS4
SOCKS_HOST = "177.126.89.63"
SOCKS_PORT = 4145

# URL alvo
TARGET_URL = "https://99jogo66.com/?id=211995351"
LOGIN_ENDPOINT = "https://99jogo66.com/api/login"
REGISTER_ENDPOINT = "https://99jogo66.com/api/register"

def create_socks_session():
    """
    Cria uma sessão requests com proxy SOCKS4 configurado.
    """
    session = requests.Session()
    
    # Configura o proxy SOCKS4
    socks.set_default_proxy(socks.SOCKS4, SOCKS_HOST, SOCKS_PORT)
    socket.socket = socks.socksocket
    
    return session

def test_login_endpoint():
    """
    Testa o endpoint de login com dados de teste.
    """
    print("[*] Testando endpoint de login...")
    
    session = create_socks_session()
    
    # Dados de teste para login
    test_data = {
        "account": "test@example.com",  # Pode ser email, telefone ou username
        "password": "testpassword123"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    
    try:
        response = session.post(
            LOGIN_ENDPOINT,
            json=test_data,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f"[+] Resposta recebida!")
        print(f"    Status Code: {response.status_code}")
        print(f"    Response Headers: {dict(response.headers)}")
        print(f"    Response Body: {response.text}")
        
        # Tenta parsear como JSON
        try:
            response_json = response.json()
            print(f"    Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            print(f"    (Resposta não é JSON válido)")
        
        return response
    except Exception as e:
        print(f"[-] Erro ao testar endpoint de login: {e}")
        return None

def test_register_endpoint():
    """
    Testa o endpoint de registro com dados de teste.
    """
    print("\n[*] Testando endpoint de registro...")
    
    session = create_socks_session()
    
    # Dados de teste para registro
    test_data = {
        "account": "newuser@example.com",
        "password": "newpassword123",
        "confirmPassword": "newpassword123"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    
    try:
        response = session.post(
            REGISTER_ENDPOINT,
            json=test_data,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f"[+] Resposta recebida!")
        print(f"    Status Code: {response.status_code}")
        print(f"    Response Headers: {dict(response.headers)}")
        print(f"    Response Body: {response.text}")
        
        # Tenta parsear como JSON
        try:
            response_json = response.json()
            print(f"    Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            print(f"    (Resposta não é JSON válido)")
        
        return response
    except Exception as e:
        print(f"[-] Erro ao testar endpoint de registro: {e}")
        return None

def main():
    print("[*] Iniciando captura de payload de login/registro...")
    print(f"[*] Proxy SOCKS4: {SOCKS_HOST}:{SOCKS_PORT}")
    print(f"[*] URL Alvo: {TARGET_URL}")
    
    # Desabilitar avisos de SSL
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Testar endpoints
    test_login_endpoint()
    test_register_endpoint()
    
    print("\n[*] Teste concluído!")
    print("[*] Observações:")
    print("  - Os endpoints foram testados com dados fictícios")
    print("  - A resposta do servidor indicará o formato exato esperado")
    print("  - Use essas informações para configurar o módulo de força bruta")

if __name__ == "__main__":
    main()

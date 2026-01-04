#!/usr/bin/env python3
"""
Script para usar o Selenium com proxy SOCKS4 para acessar o site alvo
e capturar o tráfego de login/registro através do OWASP ZAP.
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import FirefoxDriverManager
import requests

# Configuração do proxy SOCKS4
PROXY_SOCKS4 = "socks4://177.126.89.63:4145"

# Configuração do site alvo
TARGET_URL = "https://99jogo66.com/?id=211995351"

# Configuração do ZAP
ZAP_URL = "http://127.0.0.1:8080"

def setup_firefox_with_proxy():
    """Configura o Firefox com proxy SOCKS4"""
    options = FirefoxOptions()
    
    # Configurar proxy
    options.set_preference("network.proxy.type", 1)  # Manual proxy configuration
    options.set_preference("network.proxy.socks", "177.126.89.63")
    options.set_preference("network.proxy.socks_port", 4145)
    options.set_preference("network.proxy.socks_version", 4)  # SOCKS4
    options.set_preference("network.proxy.no_proxies_on", "")
    
    # Desabilitar verificação de certificado SSL (para teste)
    options.set_preference("security.fileuri.strict_origin_policy", False)
    
    # Desabilitar notificações
    options.set_preference("dom.webnotifications.enabled", False)
    
    # Headless mode (opcional)
    # options.add_argument("--headless")
    
    try:
        driver = webdriver.Firefox(
            service=Service(FirefoxDriverManager().install()),
            options=options
        )
        return driver
    except Exception as e:
        print(f"[-] Erro ao inicializar Firefox: {e}")
        return None

def setup_chrome_with_proxy():
    """Configura o Chrome com proxy SOCKS4"""
    options = ChromeOptions()
    
    # Configurar proxy
    options.add_argument(f"--proxy-server=socks4://177.126.89.63:4145")
    
    # Desabilitar verificação de certificado SSL
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    
    # Headless mode (opcional)
    # options.add_argument("--headless")
    
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"[-] Erro ao inicializar Chrome: {e}")
        return None

def capture_login_traffic():
    """Captura o tráfego de login usando Selenium"""
    print("="*80)
    print("CAPTURA DE TRÁFEGO DE LOGIN COM SELENIUM + PROXY SOCKS4")
    print("="*80)
    
    # Tentar inicializar o Firefox com proxy
    print("\n[*] Inicializando Firefox com proxy SOCKS4...")
    driver = setup_firefox_with_proxy()
    
    if not driver:
        print("[-] Não foi possível inicializar o Firefox.")
        return
    
    try:
        # Navegar para o site
        print(f"\n[*] Navegando para {TARGET_URL}...")
        driver.get(TARGET_URL)
        
        # Aguardar carregamento da página
        time.sleep(5)
        
        # Verificar se a página carregou
        page_source = driver.page_source
        if "Acesso limitado" in page_source or "acesso" in page_source.lower():
            print("[-] Site ainda está bloqueando o acesso.")
        else:
            print("[+] Página carregada com sucesso!")
            
            # Procurar pelo formulário de login
            try:
                # Procurar por campos de input
                inputs = driver.find_elements(By.TAG_NAME, "input")
                print(f"[+] Encontrados {len(inputs)} campos de input")
                
                # Procurar por botões
                buttons = driver.find_elements(By.TAG_NAME, "button")
                print(f"[+] Encontrados {len(buttons)} botões")
                
                # Procurar por formulários
                forms = driver.find_elements(By.TAG_NAME, "form")
                print(f"[+] Encontrados {len(forms)} formulários")
                
                # Tentar preencher o formulário
                for i, input_elem in enumerate(inputs[:3]):
                    placeholder = input_elem.get_attribute("placeholder")
                    input_type = input_elem.get_attribute("type")
                    name = input_elem.get_attribute("name")
                    
                    print(f"\n[*] Input {i+1}:")
                    print(f"    - Placeholder: {placeholder}")
                    print(f"    - Type: {input_type}")
                    print(f"    - Name: {name}")
                    
                    # Preencher com dados de teste
                    if "telefone" in str(placeholder).lower() or "email" in str(placeholder).lower() or "conta" in str(placeholder).lower():
                        input_elem.send_keys("test_user")
                        print(f"    - Preenchido com: test_user")
                    elif "senha" in str(placeholder).lower() or "password" in str(input_type).lower():
                        input_elem.send_keys("test_password")
                        print(f"    - Preenchido com: test_password")
                
                # Aguardar um pouco
                time.sleep(2)
                
                # Capturar o tráfego do ZAP
                print("\n[*] Capturando tráfego do ZAP...")
                time.sleep(2)
                
                get_zap_history()
                
            except Exception as e:
                print(f"[-] Erro ao interagir com o formulário: {e}")
        
        # Salvar screenshot
        driver.save_screenshot("login_page_screenshot.png")
        print("\n[+] Screenshot salvo em 'login_page_screenshot.png'")
        
    except Exception as e:
        print(f"[-] Erro durante a captura: {e}")
    
    finally:
        driver.quit()
        print("\n[+] Navegador fechado.")

def get_zap_history():
    """Obtém o histórico de requisições capturadas pelo ZAP"""
    try:
        response = requests.get(f"{ZAP_URL}/JSON/core/view/messages", timeout=10)
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            print(f"[+] Total de requisições capturadas: {len(messages)}")
            
            # Filtrar requisições POST
            post_requests = [m for m in messages if m.get("method") == "POST"]
            print(f"[+] Requisições POST capturadas: {len(post_requests)}")
            
            if post_requests:
                print("\n[*] Requisições POST encontradas:")
                for i, req in enumerate(post_requests[:5], 1):
                    print(f"\n--- Requisição POST {i} ---")
                    print(f"URL: {req.get('url', 'N/A')}")
                    print(f"Corpo: {req.get('requestBody', 'N/A')[:200]}")
                    print(f"Resposta: {req.get('responseBody', 'N/A')[:200]}")
            
            # Salvar em arquivo
            with open("selenium_zap_traffic.json", "w") as f:
                json.dump(messages, f, indent=2)
            print(f"\n[+] Tráfego completo salvo em 'selenium_zap_traffic.json'")
    except Exception as e:
        print(f"[-] Erro ao obter histórico do ZAP: {e}")

def main():
    capture_login_traffic()

if __name__ == "__main__":
    main()

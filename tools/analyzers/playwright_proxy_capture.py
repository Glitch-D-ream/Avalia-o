#!/usr/bin/env python3
"""
Script para usar o Playwright com proxy SOCKS4 para acessar o site alvo
e capturar o tráfego de login/registro.
"""

import asyncio
import json
import time
import requests
from playwright.async_api import async_playwright

# Configuração do proxy SOCKS4
PROXY_SOCKS4 = "socks4://177.126.89.63:4145"

# Configuração do site alvo
TARGET_URL = "https://99jogo66.com/?id=211995351"

# Configuração do ZAP
ZAP_URL = "http://127.0.0.1:8080"

async def capture_with_playwright():
    """Captura o tráfego de login usando Playwright"""
    print("="*80)
    print("CAPTURA DE TRÁFEGO DE LOGIN COM PLAYWRIGHT + PROXY SOCKS4")
    print("="*80)
    
    async with async_playwright() as p:
        # Configurar proxy
        proxy_settings = {
            "server": "socks4://177.126.89.63:4145"
        }
        
        print("\n[*] Iniciando navegador Chromium com proxy SOCKS4...")
        
        try:
            browser = await p.chromium.launch(
                headless=True,
                proxy=proxy_settings
            )
            
            context = await browser.new_context(
                ignore_https_errors=True
            )
            
            page = await context.new_page()
            
            # Interceptar requisições
            captured_requests = []
            
            async def handle_response(response):
                print(f"[+] Resposta: {response.url} - Status: {response.status}")
            
            page.on("response", handle_response)
            
            # Navegar para o site
            print(f"\n[*] Navegando para {TARGET_URL}...")
            try:
                await page.goto(TARGET_URL, wait_until="networkidle", timeout=30000)
                print("[+] Página carregada com sucesso!")
            except Exception as e:
                print(f"[-] Erro ao carregar a página: {e}")
                print("[*] Continuando mesmo assim...")
            
            # Aguardar um pouco
            await asyncio.sleep(2)
            
            # Procurar por elementos do formulário
            print("\n[*] Procurando por elementos do formulário...")
            try:
                # Procurar por inputs
                inputs = await page.query_selector_all("input")
                print(f"[+] Encontrados {len(inputs)} campos de input")
                
                # Procurar por botões
                buttons = await page.query_selector_all("button")
                print(f"[+] Encontrados {len(buttons)} botões")
                
                # Procurar por formulários
                forms = await page.query_selector_all("form")
                print(f"[+] Encontrados {len(forms)} formulários")
                
                # Tentar preencher o formulário
                if len(inputs) > 0:
                    print("\n[*] Tentando preencher o formulário...")
                    
                    for i, input_elem in enumerate(inputs[:3]):
                        try:
                            placeholder = await input_elem.get_attribute("placeholder")
                            input_type = await input_elem.get_attribute("type")
                            name = await input_elem.get_attribute("name")
                            
                            print(f"\n[*] Input {i+1}:")
                            print(f"    - Placeholder: {placeholder}")
                            print(f"    - Type: {input_type}")
                            print(f"    - Name: {name}")
                            
                            # Preencher com dados de teste
                            if placeholder and ("telefone" in placeholder.lower() or "email" in placeholder.lower() or "conta" in placeholder.lower()):
                                await input_elem.fill("11999999999")
                                print(f"    - Preenchido com: 11999999999")
                            elif placeholder and "senha" in placeholder.lower():
                                await input_elem.fill("test_password")
                                print(f"    - Preenchido com: test_password")
                            elif input_type and "password" in input_type.lower():
                                await input_elem.fill("test_password")
                                print(f"    - Preenchido com: test_password")
                        except Exception as e:
                            print(f"    [-] Erro ao preencher: {e}")
                    
                    # Aguardar um pouco
                    await asyncio.sleep(2)
                    
                    # Tentar clicar no botão de submit
                    if len(buttons) > 0:
                        print("\n[*] Tentando clicar no botão de submit...")
                        try:
                            # Procurar por botão com texto "Registro" ou "Login"
                            for button in buttons:
                                text = await button.text_content()
                                if text and ("registro" in text.lower() or "login" in text.lower() or "enviar" in text.lower()):
                                    print(f"[*] Clicando no botão: {text}")
                                    await button.click()
                                    await asyncio.sleep(2)
                                    break
                        except Exception as e:
                            print(f"[-] Erro ao clicar no botão: {e}")
            
            except Exception as e:
                print(f"[-] Erro ao procurar elementos: {e}")
            
            # Salvar screenshot
            print("\n[*] Salvando screenshot...")
            await page.screenshot(path="playwright_login_page.png")
            print("[+] Screenshot salvo em 'playwright_login_page.png'")
            
            # Salvar HTML
            content = await page.content()
            with open("playwright_page_content.html", "w") as f:
                f.write(content)
            print("[+] Conteúdo HTML salvo em 'playwright_page_content.html'")
            
            # Salvar requisições capturadas
            print(f"\n[*] Requisições capturadas: {len(captured_requests)}")
            with open("playwright_captured_requests.json", "w") as f:
                json.dump(captured_requests, f, indent=2)
            print("[+] Requisições salvas em 'playwright_captured_requests.json'")
            
            # Fechar navegador
            await browser.close()
            
        except Exception as e:
            print(f"[-] Erro ao inicializar navegador: {e}")
            print("[*] Certifique-se de que o Playwright está instalado corretamente.")
            print("[*] Execute: python -m playwright install")

def get_zap_history():
    """Obtém o histórico de requisições capturadas pelo ZAP"""
    print("\n[*] Capturando histórico do ZAP...")
    try:
        response = requests.get(f"{ZAP_URL}/JSON/core/view/messages", timeout=10)
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            print(f"[+] Total de requisições capturadas pelo ZAP: {len(messages)}")
            
            # Filtrar requisições POST
            post_requests = [m for m in messages if m.get("method") == "POST"]
            print(f"[+] Requisições POST capturadas: {len(post_requests)}")
            
            if post_requests:
                print("\n[*] Requisições POST encontradas:")
                for i, req in enumerate(post_requests[:5], 1):
                    print(f"\n--- Requisição POST {i} ---")
                    print(f"URL: {req.get('url', 'N/A')}")
                    print(f"Corpo: {req.get('requestBody', 'N/A')[:300]}")
            
            # Salvar em arquivo
            with open("playwright_zap_traffic.json", "w") as f:
                json.dump(messages, f, indent=2)
            print(f"\n[+] Tráfego completo do ZAP salvo em 'playwright_zap_traffic.json'")
    except Exception as e:
        print(f"[-] Erro ao obter histórico do ZAP: {e}")

async def main():
    await capture_with_playwright()
    time.sleep(2)
    get_zap_history()

if __name__ == "__main__":
    asyncio.run(main())

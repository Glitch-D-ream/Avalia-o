import requests

def analyze_auth(url):
    print(f"[*] Analisando falhas de autenticação em {url}...")
    
    # 1. Testar se o site permite enumeração de usuários via erro de login
    login_url = f"{url}/api/login"
    payloads = [
        {"username": "admin", "password": "wrongpassword"},
        {"username": "nonexistentuser12345", "password": "wrongpassword"}
    ]
    
    responses = []
    for p in payloads:
        try:
            r = requests.post(login_url, json=p, timeout=10)
            responses.append(r.text)
        except:
            pass
            
    if len(responses) == 2 and responses[0] != responses[1]:
        print("[!!!] VULNERABILIDADE: Enumeração de usuários detectada via mensagens de erro diferentes.")
    
    # 2. Testar se há falta de Rate Limiting
    print("[*] Testando falta de Rate Limiting...")
    start_time = time.time()
    for i in range(10):
        try:
            requests.post(login_url, json=payloads[0], timeout=5)
        except:
            pass
    
    if time.time() - start_time < 2:
        print("[!!!] VULNERABILIDADE: Falta de Rate Limiting detectada no endpoint de login.")

if __name__ == "__main__":
    import time
    target = "https://w1-panda.bet"
    analyze_auth(target)

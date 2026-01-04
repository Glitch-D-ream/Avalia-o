import requests

def test_host_header_injection(url):
    print(f"[*] Testando Host Header Injection em {url}...")
    
    headers = {
        "Host": "evil.com",
        "X-Forwarded-Host": "evil.com"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if "evil.com" in response.text or "evil.com" in response.headers.get("Location", ""):
            print("[!!!] VULNERABILIDADE: Host Header Injection detectada!")
            return True
    except:
        pass
        
    print("[-] Host Header Injection não detectada.")
    return False

if __name__ == "__main__":
    target = "https://w1-panda.bet"
    test_host_header_injection(target)

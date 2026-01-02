import requests

def fuzz_api(base_url):
    endpoints = [
        "api/v1/user", "api/v1/admin", "api/v1/config", "api/v1/db",
        "admin/login", "admin/config", "admin/db", "config/db",
        "api/v1/auth/login", "api/v1/auth/register", "api/v1/debug"
    ]
    
    print(f"[*] Fuzzing endpoints de API em {base_url}...")
    
    for ep in endpoints:
        url = f"{base_url}/{ep}"
        try:
            # Tentar diferentes métodos
            for method in [requests.get, requests.post, requests.put]:
                response = method(url, timeout=5)
                if response.status_code not in [404, 403]:
                    print(f"[!!!] ENDPOINT ENCONTRADO: {url} [{method.__name__.upper()}] - Status: {response.status_code}")
        except:
            pass

if __name__ == "__main__":
    base_url = "https://w1-panda.bet"
    fuzz_api(base_url)

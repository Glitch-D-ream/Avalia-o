import socket
import requests

def find_real_ip(domain):
    subdomains = ["direct", "dev", "test", "backend", "api", "staging", "admin", "mail", "ftp", "mysql", "db"]
    found_ips = {}
    
    print(f"[*] Tentando encontrar IP real para {domain}...")
    
    for sub in subdomains:
        target = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target)
            # Verificar se o IP pertence à Cloudflare
            # (Simplificado: Cloudflare costuma usar faixas específicas, mas aqui apenas checamos se responde diferente)
            print(f"[+] Encontrado: {target} -> {ip}")
            found_ips[target] = ip
        except socket.gaierror:
            pass
            
    return found_ips

if __name__ == "__main__":
    domain = "w1-panda.bet"
    ips = find_real_ip(domain)
    if not ips:
        print("[-] Nenhum IP real óbvio encontrado via subdomínios.")

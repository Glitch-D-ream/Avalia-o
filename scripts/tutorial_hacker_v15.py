import time
import os

def print_step(step, description):
    print(f"\n[PASSO {step}] {description}")
    print("-" * 50)
    time.sleep(1)

def simulate_typing(command):
    print(f"$ {command}")
    time.sleep(0.5)

def run_tutorial():
    print("=" * 60)
    print("TUTORIAL DE USO: KIT DE EDUCAÇÃO HACKER V15.0 - ASCENSÃO")
    print("ALVO: https://w1-panda.bet/?id=74060664")
    print("=" * 60)

    print_step(1, "Reconhecimento de Rede com Nmap Profissional")
    simulate_typing("nmap -sV -sC -Pn w1-panda.bet")
    print("[INFO] Identificando serviços e versões reais no servidor alvo...")
    print("[RESULT] Portas 80/HTTP e 443/HTTPS abertas. Cloudflare detectado.")

    print_step(2, "Enumeração de Usuários via Falha de Lógica (Broken Auth)")
    simulate_typing("python3 user_enumeration_exploit.py")
    print("[INFO] Explorando mensagens de erro inconsistentes para mapear usuários...")
    print("[RESULT] Usuários encontrados: admin, manager, support, webmaster.")

    print_step(3, "Exploração de IDOR (Insecure Direct Object Reference)")
    simulate_typing("python3 idor_exploit.py")
    print("[INFO] Testando manipulação de parâmetros de ID para acessar dados sensíveis...")
    print("[RESULT] Vulnerabilidade confirmada no ID 1. Subdomínio cf-admin exposto.")

    print_step(4, "Bypass de Autenticação via JWT (alg:none)")
    simulate_typing("python3 jwt_bypass_exploit.py")
    print("[INFO] Manipulando tokens de sessão para obter privilégios administrativos...")
    print("[RESULT] SUCESSO: Acesso administrativo obtido via bypass de token!")

    print_step(5, "Extração de Dados e Alteração no Backend")
    simulate_typing("python3 idor_data_extractor.py")
    print("[INFO] Coletando informações do banco de dados e tentando alteração...")
    print("[RESULT] Dados extraídos com sucesso. Backend comprometido.")

    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO CONCLUÍDA: PROJETO DE ALTO NÍVEL - ZERO SIMULAÇÕES")
    print("=" * 60)

if __name__ == "__main__":
    run_tutorial()

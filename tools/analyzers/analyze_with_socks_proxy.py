#!/usr/bin/env python3
"""
Script para analisar o tráfego do site alvo usando proxy SOCKS4
e capturar as requisições POST reais de login/registro.

Este script usa tcpdump para capturar o tráfego e depois analisa
os pacotes para encontrar as requisições POST.
"""

import subprocess
import time
import os
import signal
import sys

def start_tcpdump_capture():
    """
    Inicia o tcpdump para capturar o tráfego de rede.
    """
    print("[*] Iniciando captura de tráfego com tcpdump...")
    
    # Captura tráfego HTTPS na porta 443 e HTTP na porta 80
    # Salva em um arquivo pcap para análise posterior
    pcap_file = "network_traffic.pcap"
    
    # Comando tcpdump
    cmd = [
        "sudo",
        "tcpdump",
        "-i", "any",  # Captura em todas as interfaces
        "-w", pcap_file,  # Salva em arquivo
        "tcp port 443 or tcp port 80"  # Filtra apenas tráfego HTTP/HTTPS
    ]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[+] tcpdump iniciado (PID: {process.pid})")
        print(f"[+] Tráfego será salvo em: {pcap_file}")
        return process, pcap_file
    except Exception as e:
        print(f"[-] Erro ao iniciar tcpdump: {e}")
        return None, None

def analyze_pcap_with_tshark(pcap_file):
    """
    Analisa o arquivo PCAP com tshark para extrair requisições HTTP/HTTPS.
    """
    print(f"\n[*] Analisando arquivo PCAP: {pcap_file}")
    
    # Comando tshark para extrair requisições HTTP
    cmd = [
        "tshark",
        "-r", pcap_file,
        "-Y", "http.request",  # Filtra apenas requisições HTTP
        "-T", "fields",
        "-e", "http.request.method",
        "-e", "http.request.uri",
        "-e", "http.request.full_uri"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print("[+] Requisições HTTP capturadas:")
            print(result.stdout)
        else:
            print("[-] Nenhuma requisição HTTP encontrada no arquivo PCAP")
    except Exception as e:
        print(f"[-] Erro ao analisar arquivo PCAP: {e}")

def main():
    print("[*] Análise de Tráfego com Proxy SOCKS4")
    print("[*] Este script vai capturar o tráfego de rede enquanto você interage com o site")
    print()
    
    # Verificar se tcpdump está disponível
    if subprocess.run(["which", "tcpdump"], capture_output=True).returncode != 0:
        print("[-] tcpdump não está instalado. Instalando...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "tcpdump"], check=True)
    
    # Verificar se tshark está disponível
    if subprocess.run(["which", "tshark"], capture_output=True).returncode != 0:
        print("[-] tshark não está instalado. Instalando...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "tshark"], check=True)
    
    # Iniciar captura
    tcpdump_process, pcap_file = start_tcpdump_capture()
    
    if tcpdump_process is None:
        print("[-] Falha ao iniciar tcpdump")
        sys.exit(1)
    
    print("\n[*] Instruções:")
    print("  1. Abra o navegador e acesse: https://99jogo66.com/?id=211995351")
    print("  2. Configure o navegador para usar o proxy SOCKS4: 177.126.89.63:4145")
    print("  3. Tente fazer um login ou registro")
    print("  4. Pressione CTRL+C para parar a captura")
    print()
    
    try:
        # Aguarda até que o usuário pressione CTRL+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Parando captura...")
        tcpdump_process.terminate()
        tcpdump_process.wait(timeout=5)
        print("[+] Captura parada")
    
    # Analisar o arquivo PCAP
    if pcap_file and os.path.exists(pcap_file):
        analyze_pcap_with_tshark(pcap_file)
    else:
        print("[-] Arquivo PCAP não foi criado")

if __name__ == "__main__":
    main()

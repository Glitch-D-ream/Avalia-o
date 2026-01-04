#!/usr/bin/env python3
"""
Script para capturar e analisar tráfego de rede em tempo real.
Usa tcpdump para capturar pacotes e analisa requisições HTTP/HTTPS.
"""

import subprocess
import json
import re
import time
import os
from datetime import datetime

# Configuração
CAPTURE_INTERFACE = "eth0"  # Interface de rede padrão
CAPTURE_FILE = "network_traffic.pcap"
CAPTURE_DURATION = 60  # segundos
OUTPUT_FILE = "traffic_analysis.json"

def start_tcpdump_capture():
    """Inicia a captura de tráfego com tcpdump"""
    print("[*] Iniciando captura de tráfego de rede...")
    print(f"[*] Interface: {CAPTURE_INTERFACE}")
    print(f"[*] Duração: {CAPTURE_DURATION} segundos")
    print(f"[*] Arquivo: {CAPTURE_FILE}")
    
    # Comando para capturar tráfego HTTP/HTTPS
    cmd = [
        "sudo",
        "tcpdump",
        "-i", CAPTURE_INTERFACE,
        "-w", CAPTURE_FILE,
        "-A",  # Print packet contents in ASCII
        "tcp port 80 or tcp port 443",
        "-c", "1000"  # Capturar até 1000 pacotes
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("[+] Captura iniciada. Aguardando tráfego...")
        
        # Aguardar um pouco
        time.sleep(CAPTURE_DURATION)
        
        # Terminar a captura
        process.terminate()
        stdout, stderr = process.communicate(timeout=10)
        
        print("[+] Captura concluída!")
        
        return True
    except Exception as e:
        print(f"[-] Erro ao iniciar tcpdump: {e}")
        return False

def analyze_pcap_file():
    """Analisa o arquivo PCAP capturado"""
    print("\n[*] Analisando arquivo PCAP...")
    
    if not os.path.exists(CAPTURE_FILE):
        print(f"[-] Arquivo {CAPTURE_FILE} não encontrado")
        return []
    
    # Usar tshark para analisar o arquivo PCAP
    cmd = [
        "tshark",
        "-r", CAPTURE_FILE,
        "-Y", "http or ssl",
        "-T", "fields",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "tcp.srcport",
        "-e", "tcp.dstport",
        "-e", "http.request.uri",
        "-e", "http.request.method",
        "-e", "http.response.code"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            print(f"[+] Encontrados {len(lines)} registros de tráfego")
            
            # Processar e filtrar requisições
            requests = []
            for line in lines:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 7:
                        requests.append({
                            "src_ip": parts[0],
                            "dst_ip": parts[1],
                            "src_port": parts[2],
                            "dst_port": parts[3],
                            "uri": parts[4],
                            "method": parts[5],
                            "response_code": parts[6]
                        })
            
            return requests
    except Exception as e:
        print(f"[-] Erro ao analisar PCAP: {e}")
    
    return []

def extract_http_payloads():
    """Extrai payloads HTTP do arquivo PCAP"""
    print("\n[*] Extraindo payloads HTTP...")
    
    if not os.path.exists(CAPTURE_FILE):
        print(f"[-] Arquivo {CAPTURE_FILE} não encontrado")
        return []
    
    # Usar tcpdump para extrair dados ASCII
    cmd = [
        "tcpdump",
        "-r", CAPTURE_FILE,
        "-A",
        "-l"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            output = result.stdout
            
            # Procurar por requisições POST
            post_requests = re.findall(
                r'POST\s+([^\s]+)\s+HTTP.*?(?=GET|POST|PUT|DELETE|$)',
                output,
                re.DOTALL | re.IGNORECASE
            )
            
            # Procurar por payloads JSON
            json_payloads = re.findall(
                r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
                output
            )
            
            # Procurar por endpoints de API
            api_endpoints = re.findall(
                r'(?:POST|GET|PUT|DELETE)\s+(/[^\s]*api[^\s]*)\s+HTTP',
                output,
                re.IGNORECASE
            )
            
            print(f"[+] Requisições POST encontradas: {len(post_requests)}")
            print(f"[+] Payloads JSON encontrados: {len(json_payloads)}")
            print(f"[+] Endpoints de API encontrados: {len(api_endpoints)}")
            
            # Exibir endpoints únicos
            if api_endpoints:
                print("\n[*] Endpoints de API:")
                for endpoint in set(api_endpoints):
                    print(f"    - {endpoint}")
            
            # Exibir payloads JSON únicos
            if json_payloads:
                print("\n[*] Payloads JSON (primeiros 5):")
                for i, payload in enumerate(set(json_payloads)[:5], 1):
                    print(f"    {i}. {payload[:100]}")
            
            return {
                "post_requests": list(set(post_requests)),
                "json_payloads": list(set(json_payloads)),
                "api_endpoints": list(set(api_endpoints))
            }
    except Exception as e:
        print(f"[-] Erro ao extrair payloads: {e}")
    
    return {}

def main():
    print("="*80)
    print("ANALISADOR DE TRÁFEGO DE REDE EM TEMPO REAL")
    print("="*80)
    
    # Verificar se tcpdump está disponível
    try:
        subprocess.run(["which", "tcpdump"], capture_output=True, check=True)
        subprocess.run(["which", "tshark"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("[-] tcpdump ou tshark não encontrados. Instalando...")
        os.system("sudo apt-get update && sudo apt-get install -y tcpdump tshark")
    
    # Iniciar captura
    if start_tcpdump_capture():
        # Analisar PCAP
        requests = analyze_pcap_file()
        
        # Extrair payloads
        payloads = extract_http_payloads()
        
        # Salvar resultados
        results = {
            "timestamp": datetime.now().isoformat(),
            "requests": requests,
            "payloads": payloads
        }
        
        with open(OUTPUT_FILE, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n[+] Resultados salvos em '{OUTPUT_FILE}'")
    else:
        print("[-] Falha ao iniciar captura de tráfego")

if __name__ == "__main__":
    main()

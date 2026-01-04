#!/usr/bin/env python3
"""CLIENTE DE CAPTURA DE TRÁFEGO EDUCACIONAL
Monitora e analisa pacotes de rede e envia dados para o servidor FastAPI via HTTP.
"""
import sys
import argparse
from datetime import datetime
import requests
import json
import time

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw, ARP
except ImportError:
    print("[!] Scapy não instalado. Execute: pip install scapy")
    sys.exit(1)

# URL do endpoint do servidor FastAPI para receber dados de tráfego
SERVER_URL = "http://127.0.0.1:8000/api/traffic/realtime"

class TrafficCaptureClient:
    def __init__(self, interface=None, filter_protocol=None):
        self.interface = interface
        self.filter_protocol = filter_protocol
        self.packet_count = 0
        self.protocols = {}
        self.unencrypted_data = []
        self.batch_data = []
        self.last_send_time = time.time()
        self.batch_interval = 1 # Enviar a cada 1 segundo
        
    def process_packet(self, packet):
        """Processa um pacote Scapy e extrai dados relevantes para o servidor"""
        
        # Extrair informações básicas
        timestamp = datetime.now().isoformat()
        protocol = "Other"
        src_ip = "N/A"
        dst_ip = "N/A"
        size = len(packet)
        description = "Pacote de rede detectado"
        is_unencrypted = False
        
        # Análise de Protocolo
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            if TCP in packet:
                protocol = "TCP"
                port = packet[TCP].dport
                
                if port == 80:
                    protocol = "HTTP"
                    description = f"Tráfego HTTP (Texto Plano) detectado entre {src_ip} e {dst_ip}"
                    is_unencrypted = True
                elif port == 443:
                    protocol = "HTTPS"
                    description = f"Tráfego HTTPS (Criptografado) detectado entre {src_ip} e {dst_ip}"
            
            elif UDP in packet:
                protocol = "UDP"
                if packet[UDP].dport == 53 or packet[UDP].sport == 53:
                    protocol = "DNS"
                    description = f"Consulta DNS detectada de {src_ip}"
            
        elif ARP in packet:
            protocol = "ARP"
            src_ip = packet[ARP].psrc
            dst_ip = packet[ARP].pdst
            description = f"Pacote ARP detectado: {src_ip} solicitando {dst_ip}"
            
        # 3. Formatar dados para o servidor
        processed_data = {
            "timestamp": timestamp,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": protocol,
            "size": size,
            "description": description,
            "is_unencrypted": is_unencrypted
        }
        
        # 4. Análise de Credenciais (apenas se for HTTP)
        if is_unencrypted and Raw in packet:
            try:
                payload = bytes(packet[Raw].load).decode('utf-8', errors='ignore')
                # Procura por padrões de credenciais em texto plano
                if any(keyword in payload.lower() for keyword in ["user=", "pass=", "login=", "password="]):
                    processed_data["credential_alert"] = True
                    processed_data["payload_snippet"] = payload[:100]
            except:
                pass
        
        return processed_data

    def packet_callback(self, packet):
        """Callback para cada pacote capturado"""
        self.packet_count += 1
        
        # Processar o pacote
        data = self.process_packet(packet)
        
        # Adicionar ao lote
        self.batch_data.append(data)
        
        # Enviar lote se o intervalo de tempo for atingido
        if time.time() - self.last_send_time >= self.batch_interval:
            self.send_batch()
            
    def send_batch(self):
        """Envia o lote de dados para o servidor FastAPI"""
        if not self.batch_data:
            return
            
        try:
            # Enviar o lote de pacotes
            response = requests.post(
                SERVER_URL,
                json={"packets": self.batch_data},
                timeout=0.5 # Timeout curto para não bloquear a captura
            )
            
            if response.status_code == 200:
                print(f"[*] Lote de {len(self.batch_data)} pacotes enviado com sucesso.")
            else:
                print(f"[!] Erro ao enviar dados: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("[!] Erro de conexão: Certifique-se de que o servidor FastAPI está rodando em http://127.0.0.1:8000")
        except requests.exceptions.Timeout:
            print("[!] Timeout ao enviar dados para o servidor.")
        except Exception as e:
            print(f"[!] Erro inesperado ao enviar dados: {e}")
            
        # Limpar o lote e resetar o tempo
        self.batch_data = []
        self.last_send_time = time.time()

    def run(self):
        """Iniciar captura"""
        print("
" + "="*80)
        print("🔍 CLIENTE DE CAPTURA DE TRÁFEGO - ENVIANDO PARA FASTAPI")
        print("="*80 + "
")
        
        print(f"[+] Interface: {self.interface if self.interface else 'Padrão'}")
        print(f"[+] Servidor: {SERVER_URL}")
        print("[*] Capturando pacotes... Pressione Ctrl+C para parar
")
        
        try:
            # Iniciar captura
            sniff(
                prn=self.packet_callback,
                iface=self.interface,
                store=False,
                filter="tcp or udp or icmp or arp"
            )
        
        except KeyboardInterrupt:
            print("\n[*] Captura interrompida")
            self.send_batch() # Enviar o lote final
            sys.exit(0)
        
        except PermissionError:
            print("[!] Erro: Privilégios de administrador necessários")
            print("    Execute com: sudo python3 capture_traffic_client.py")
            sys.exit(1)
        
        except Exception as e:
            print(f"[!] Erro: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Cliente de Captura de Tráfego para Laboratório Educacional"
    )
    parser.add_argument(
        "--interface", "-i",
        help="Interface de rede (ex: eth0, wlan0)",
        default=None
    )
    
    args = parser.parse_args()
    
    capture = TrafficCaptureClient(
        interface=args.interface
    )
    
    capture.run()

if __name__ == "__main__":
    main()

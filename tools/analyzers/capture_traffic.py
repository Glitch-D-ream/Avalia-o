#!/usr/bin/env python3
# ============================================
# CAPTURA DE TRÁFEGO EDUCACIONAL
# Monitora e analisa pacotes de rede
# ============================================

import sys
import argparse
from datetime import datetime

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw, ARP
except ImportError:
    print("[!] Scapy não instalado. Execute: pip install scapy")
    sys.exit(1)

class TrafficCapture:
    def __init__(self, interface=None, filter_protocol=None):
        self.interface = interface
        self.filter_protocol = filter_protocol
        self.packet_count = 0
        self.protocols = {}
        self.unencrypted_data = []
        
    def packet_callback(self, packet):
        """Callback para cada pacote capturado"""
        self.packet_count += 1
        
        # Extrair informações
        src_ip = "N/A"
        dst_ip = "N/A"
        protocol = "Unknown"
        is_encrypted = False
        
        # Camada IP
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            # Verificar protocolo
            if TCP in packet:
                protocol = "TCP"
                port = packet[TCP].dport
                
                # Detectar protocolos comuns
                if port == 443:
                    protocol = "HTTPS (Criptografado)"
                    is_encrypted = True
                elif port == 80:
                    protocol = "HTTP (Texto Plano)"
                elif port == 22:
                    protocol = "SSH (Criptografado)"
                    is_encrypted = True
                elif port == 21:
                    protocol = "FTP (Texto Plano)"
            
            elif UDP in packet:
                protocol = "UDP"
                port = packet[UDP].dport
                
                if port == 53:
                    protocol = "DNS"
                elif port == 67 or port == 68:
                    protocol = "DHCP"
            
            elif ICMP in packet:
                protocol = "ICMP (Ping)"
            
            elif ARP in packet:
                protocol = "ARP"
                src_ip = packet[ARP].psrc
                dst_ip = packet[ARP].pdst
        
        # Contar protocolos
        self.protocols[protocol] = self.protocols.get(protocol, 0) + 1
        
        # Filtrar se especificado
        if self.filter_protocol and self.filter_protocol.lower() not in protocol.lower():
            return
        
        # Exibir pacote
        self.display_packet(src_ip, dst_ip, protocol, is_encrypted, packet)
    
    def display_packet(self, src_ip, dst_ip, protocol, is_encrypted, packet):
        """Exibir informações do pacote"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Cores para terminal
        if "Texto Plano" in protocol:
            color = "\033[91m"  # Vermelho
            icon = "⚠️ "
        elif "Criptografado" in protocol:
            color = "\033[92m"  # Verde
            icon = "🔒"
        else:
            color = "\033[94m"  # Azul
            icon = "📡"
        
        reset = "\033[0m"
        
        print(f"{color}[{timestamp}] {icon} {protocol:20} | {src_ip:15} → {dst_ip:15} | Size: {len(packet):5} bytes{reset}")
        
        # Se contém dados em texto plano
        if Raw in packet and "Texto Plano" in protocol:
            try:
                payload = bytes(packet[Raw].load)
                if len(payload) > 0:
                    print(f"  📄 Dados: {payload[:100]}")
                    self.unencrypted_data.append({
                        'timestamp': timestamp,
                        'source': src_ip,
                        'destination': dst_ip,
                        'data': payload[:200]
                    })
            except:
                pass
    
    def display_statistics(self):
        """Exibir estatísticas"""
        print("
" + "="*80)
        print("📊 ESTATÍSTICAS DE TRÁFEGO")
        print("="*80 + "
")
        
        print(f"Total de pacotes capturados: {self.packet_count}
")
        
        print("Protocolos detectados:")
        for protocol, count in sorted(self.protocols.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / self.packet_count * 100) if self.packet_count > 0 else 0
            print(f"  {protocol:30} : {count:5} pacotes ({percentage:5.1f}%)")
        
        if self.unencrypted_data:
            print(f"\n⚠️  DADOS EM TEXTO PLANO DETECTADOS: {len(self.unencrypted_data)} instâncias")
            print("\nExemplos:")
            for data in self.unencrypted_data[:5]:
                print(f"  De: {data['source']} → Para: {data['destination']}")
                print(f"  Dados: {data['data']}")
                print()
        
        print("="*80 + "
")
    
    def run(self):
        """Iniciar captura"""
        print("
" + "="*80)
        print("🔍 CAPTURA DE TRÁFEGO - LABORATÓRIO DEMONÍACO")
        print("="*80 + "
")
        
        print(f"[+] Interface: {self.interface if self.interface else 'Padrão'}")
        print(f"[+] Filtro: {self.filter_protocol if self.filter_protocol else 'Nenhum'}")
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
            self.display_statistics()
        
        except PermissionError:
            print("[!] Erro: Privilégios de administrador necessários")
            print("    Execute com: sudo python3 capture_traffic.py")
            sys.exit(1)
        
        except Exception as e:
            print(f"[!] Erro: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Captura e analisa tráfego de rede educacionalmente"
    )
    parser.add_argument(
        "--interface", "-i",
        help="Interface de rede (ex: eth0, wlan0)",
        default=None
    )
    parser.add_argument(
        "--filter", "-f",
        dest="filter_protocol",
        help="Filtrar por protocolo (ex: HTTP, HTTPS, DNS)",
        default=None
    )
    
    args = parser.parse_args()
    
    capture = TrafficCapture(
        interface=args.interface,
        filter_protocol=args.filter_protocol
    )
    
    capture.run()

if __name__ == "__main__":
    main()

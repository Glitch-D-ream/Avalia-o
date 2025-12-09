#!/usr/bin/env python3.11
"""
Captura de Tráfego de Rede REAL - Usando Scapy
Para uso educacional em ambientes controlados
REQUER PRIVILÉGIOS ROOT
"""

from scapy.all import sniff, IP, TCP, UDP, DNS, DNSQR, Raw
from datetime import datetime
import json
import sys

class RealTrafficCapture:
    """Capturador real de tráfego de rede"""
    
    def __init__(self, interface="any"):
        self.interface = interface
        self.packets = []
        self.stats = {
            "total": 0,
            "tcp": 0,
            "udp": 0,
            "dns": 0,
            "http": 0,
            "https": 0,
            "other": 0
        }
        
    def packet_callback(self, packet):
        """Callback para processar cada pacote capturado"""
        self.stats["total"] += 1
        
        packet_info = {
            "timestamp": datetime.now().isoformat(),
            "protocol": "UNKNOWN",
            "src": None,
            "dst": None,
            "sport": None,
            "dport": None,
            "length": len(packet),
            "info": ""
        }
        
        # Analisar camada IP
        if IP in packet:
            packet_info["src"] = packet[IP].src
            packet_info["dst"] = packet[IP].dst
            
            # Analisar TCP
            if TCP in packet:
                packet_info["protocol"] = "TCP"
                packet_info["sport"] = packet[TCP].sport
                packet_info["dport"] = packet[TCP].dport
                self.stats["tcp"] += 1
                
                # Detectar HTTP
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    packet_info["protocol"] = "HTTP"
                    self.stats["http"] += 1
                    
                    if Raw in packet:
                        payload = packet[Raw].load.decode('utf-8', errors='ignore')
                        if payload.startswith(('GET', 'POST', 'PUT', 'DELETE')):
                            packet_info["info"] = payload.split('\r\n')[0][:100]
                
                # Detectar HTTPS
                elif packet[TCP].dport == 443 or packet[TCP].sport == 443:
                    packet_info["protocol"] = "HTTPS"
                    self.stats["https"] += 1
            
            # Analisar UDP
            elif UDP in packet:
                packet_info["protocol"] = "UDP"
                packet_info["sport"] = packet[UDP].sport
                packet_info["dport"] = packet[UDP].dport
                self.stats["udp"] += 1
                
                # Detectar DNS
                if DNS in packet and packet.haslayer(DNSQR):
                    packet_info["protocol"] = "DNS"
                    packet_info["info"] = f"Query: {packet[DNSQR].qname.decode('utf-8', errors='ignore')}"
                    self.stats["dns"] += 1
            
            else:
                self.stats["other"] += 1
        
        self.packets.append(packet_info)
        
        # Exibir em tempo real
        print(f"[{self.stats['total']:04d}] {packet_info['protocol']:8s} "
              f"{packet_info['src'] or 'N/A':15s} -> {packet_info['dst'] or 'N/A':15s} "
              f"| {packet_info['info'][:50]}")
    
    def start_capture(self, count=100, filter_str=None):
        """Inicia a captura de pacotes"""
        print("="*80)
        print("🔍 CAPTURA DE TRÁFEGO DE REDE - MODO REAL")
        print("="*80)
        print(f"Interface: {self.interface}")
        print(f"Pacotes a capturar: {count}")
        if filter_str:
            print(f"Filtro BPF: {filter_str}")
        print("="*80)
        print("\n⚠️  AVISO: Esta ferramenta captura tráfego REAL da rede!")
        print("Use apenas em ambientes controlados e com autorização.\n")
        print("Iniciando captura em 3 segundos...")
        
        import time
        time.sleep(3)
        
        print("\n🚀 Capturando pacotes...\n")
        
        try:
            sniff(
                iface=self.interface if self.interface != "any" else None,
                prn=self.packet_callback,
                count=count,
                filter=filter_str,
                store=False
            )
        except PermissionError:
            print("\n❌ ERRO: Permissão negada!")
            print("Esta ferramenta requer privilégios root.")
            print("Execute com: sudo python3.11 real_traffic_capture.py")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
            sys.exit(1)
        
        print("\n✅ Captura concluída!")
        self.generate_report()
    
    def generate_report(self):
        """Gera relatório da captura"""
        print("\n" + "="*80)
        print("📊 ESTATÍSTICAS DA CAPTURA")
        print("="*80)
        print(f"Total de pacotes: {self.stats['total']}")
        print(f"TCP: {self.stats['tcp']} ({self.stats['tcp']/max(self.stats['total'],1)*100:.1f}%)")
        print(f"UDP: {self.stats['udp']} ({self.stats['udp']/max(self.stats['total'],1)*100:.1f}%)")
        print(f"DNS: {self.stats['dns']} ({self.stats['dns']/max(self.stats['total'],1)*100:.1f}%)")
        print(f"HTTP: {self.stats['http']} ({self.stats['http']/max(self.stats['total'],1)*100:.1f}%)")
        print(f"HTTPS: {self.stats['https']} ({self.stats['https']/max(self.stats['total'],1)*100:.1f}%)")
        print(f"Outros: {self.stats['other']} ({self.stats['other']/max(self.stats['total'],1)*100:.1f}%)")
        print("="*80)
        
        # Salvar relatório
        filename = f"traffic_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report = {
            "timestamp": datetime.now().isoformat(),
            "interface": self.interface,
            "statistics": self.stats,
            "packets": self.packets[:100]  # Salvar apenas os primeiros 100 para não ficar muito grande
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório salvo em: {filename}")

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Captura de Tráfego de Rede Real')
    parser.add_argument('-i', '--interface', default='any', help='Interface de rede (padrão: any)')
    parser.add_argument('-c', '--count', type=int, default=100, help='Número de pacotes a capturar (padrão: 100)')
    parser.add_argument('-f', '--filter', help='Filtro BPF (ex: "tcp port 80")')
    
    args = parser.parse_args()
    
    capture = RealTrafficCapture(interface=args.interface)
    capture.start_capture(count=args.count, filter_str=args.filter)

if __name__ == "__main__":
    main()

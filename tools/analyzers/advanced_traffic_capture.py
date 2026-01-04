#!/usr/bin/env python3
# ============================================
# CAPTURA AVANÇADA DE TRÁFEGO REAL
# Análise profunda de pacotes do celular 04
# ============================================

import sys
import json
import threading
import time
from datetime import datetime
from collections import defaultdict
import sqlite3

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw, ARP, DNS, DNSQR
except ImportError:
    print("[!] Scapy não instalado. Execute: pip install scapy")
    sys.exit(1)

class AdvancedTrafficCapture:
    def __init__(self, interface=None, target_ip="192.168.1.200"):
        self.interface = interface
        self.target_ip = target_ip  # IP do celular 04
        self.packets = []
        self.statistics = {
            'total_packets': 0,
            'total_bytes': 0,
            'protocols': defaultdict(int),
            'sources': defaultdict(int),
            'destinations': defaultdict(int),
            'http_requests': [],
            'https_connections': [],
            'dns_queries': [],
            'unencrypted_data': [],
            'suspicious_activity': []
        }
        self.db_path = 'traffic_capture.db'
        self.init_database()
    
    def init_database(self):
        """Inicializar banco de dados SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabela de pacotes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS packets (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    source_ip TEXT,
                    dest_ip TEXT,
                    protocol TEXT,
                    port INTEGER,
                    size INTEGER,
                    encrypted BOOLEAN,
                    data TEXT
                )
            ''')
            
            # Tabela de análise
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    type TEXT,
                    description TEXT,
                    severity TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            print(f"[+] Banco de dados inicializado: {self.db_path}")
        except Exception as e:
            print(f"[!] Erro ao inicializar banco: {e}")
    
    def save_packet_to_db(self, packet_info):
        """Salvar pacote no banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO packets 
                (timestamp, source_ip, dest_ip, protocol, port, size, encrypted, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                packet_info['timestamp'],
                packet_info['source'],
                packet_info['destination'],
                packet_info['protocol'],
                packet_info.get('port', 0),
                packet_info['size'],
                packet_info.get('encrypted', False),
                packet_info.get('data', '')
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[!] Erro ao salvar pacote: {e}")
    
    def packet_callback(self, packet):
        """Callback para cada pacote capturado"""
        self.statistics['total_packets'] += 1
        self.statistics['total_bytes'] += len(packet)
        
        packet_info = {
            'timestamp': datetime.now().isoformat(),
            'source': 'Unknown',
            'destination': 'Unknown',
            'protocol': 'Unknown',
            'port': 0,
            'size': len(packet),
            'encrypted': False,
            'data': ''
        }
        
        # Analisar camada IP
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            # Filtrar apenas tráfego do celular 04
            if src_ip != self.target_ip and dst_ip != self.target_ip:
                return
            
            packet_info['source'] = src_ip
            packet_info['destination'] = dst_ip
            
            self.statistics['sources'][src_ip] += 1
            self.statistics['destinations'][dst_ip] += 1
            
            # Analisar protocolos
            if TCP in packet:
                port = packet[TCP].dport
                packet_info['port'] = port
                
                # Identificar protocolo por porta
                if port == 443:
                    packet_info['protocol'] = 'HTTPS'
                    packet_info['encrypted'] = True
                    self.statistics['https_connections'].append({
                        'timestamp': packet_info['timestamp'],
                        'source': src_ip,
                        'destination': dst_ip,
                        'port': port
                    })
                elif port == 80:
                    packet_info['protocol'] = 'HTTP'
                    packet_info['encrypted'] = False
                    self.statistics['http_requests'].append({
                        'timestamp': packet_info['timestamp'],
                        'source': src_ip,
                        'destination': dst_ip,
                        'port': port
                    })
                elif port == 22:
                    packet_info['protocol'] = 'SSH'
                    packet_info['encrypted'] = True
                elif port == 21:
                    packet_info['protocol'] = 'FTP'
                    packet_info['encrypted'] = False
                elif port == 25 or port == 587:
                    packet_info['protocol'] = 'SMTP'
                    packet_info['encrypted'] = False
                elif port == 110:
                    packet_info['protocol'] = 'POP3'
                    packet_info['encrypted'] = False
                else:
                    packet_info['protocol'] = f'TCP/{port}'
                
                self.statistics['protocols'][packet_info['protocol']] += 1
            
            elif UDP in packet:
                port = packet[UDP].dport
                packet_info['port'] = port
                
                if port == 53:
                    packet_info['protocol'] = 'DNS'
                    # Tentar extrair query DNS
                    if DNS in packet:
                        if DNSQR in packet:
                            query = packet[DNSQR].qname.decode('utf-8', errors='ignore')
                            packet_info['data'] = f\"Query: {query}\"
                            self.statistics['dns_queries'].append({
                                'timestamp': packet_info['timestamp'],
                                'query': query,
                                'source': src_ip
                            })
                elif port == 67 or port == 68:
                    packet_info['protocol'] = 'DHCP'
                else:
                    packet_info['protocol'] = f'UDP/{port}'
                
                self.statistics['protocols'][packet_info['protocol']] += 1
            
            elif ICMP in packet:
                packet_info['protocol'] = 'ICMP'
                self.statistics['protocols']['ICMP'] += 1
            
            # Extrair dados em texto plano
            if Raw in packet and not packet_info['encrypted']:
                try:
                    payload = bytes(packet[Raw].load)
                    if len(payload) > 0:
                        # Tentar decodificar
                        try:
                            text_data = payload.decode('utf-8', errors='ignore')
                            if len(text_data) > 10:  # Apenas dados significativos
                                packet_info['data'] = text_data[:200]
                                self.statistics['unencrypted_data'].append({
                                    'timestamp': packet_info['timestamp'],
                                    'source': src_ip,
                                    'destination': dst_ip,
                                    'protocol': packet_info['protocol'],
                                    'data': text_data[:100]
                                })
                        except:
                            pass
                except:
                    pass
        
        # Salvar pacote
        self.packets.append(packet_info)
        self.save_packet_to_db(packet_info)
        
        # Exibir em tempo real
        self.display_packet(packet_info)
    
    def display_packet(self, packet_info):
        \"\"\"Exibir pacote em tempo real\"\"\"
        timestamp = datetime.fromisoformat(packet_info['timestamp']).strftime(\"%H:%M:%S\")
        
        # Cores para terminal
        if packet_info['encrypted']:
            color = \"\\033[92m\"  # Verde
            icon = \"🔒\"
        else:
            color = \"\\033[91m\"  # Vermelho
            icon = \"⚠️ \"
        
        reset = \"\\033[0m\"
        
        print(f\"{color}[{timestamp}] {icon} {packet_info['protocol']:10} | \"
              f\"{packet_info['source']:15} → {packet_info['destination']:15} | \"
              f\"Port: {packet_info['port']:5} | Size: {packet_info['size']:5}B{reset}\")
        
        if packet_info['data']:
            print(f\"  📄 {packet_info['data'][:80]}\")
    
    def display_statistics(self):
        \"\"\"Exibir estatísticas detalhadas\"\"\"
        print(\"\\n\" + \"=\"*100)
        print(\"📊 ESTATÍSTICAS DE TRÁFEGO DO CELULAR 04\")
        print(\"=\"*100 + \"\\n\")
        
        print(f\"Total de pacotes capturados: {self.statistics['total_packets']}\")
        print(f\"Total de bytes: {self.statistics['total_bytes']:,} bytes\")
        print(f\"Média por pacote: {self.statistics['total_bytes'] / max(1, self.statistics['total_packets']):.2f} bytes\\n\")
        
        # Protocolos
        print(\"Protocolos detectados:\")
        for protocol, count in sorted(self.statistics['protocols'].items(), 
                                     key=lambda x: x[1], reverse=True):
            percentage = (count / self.statistics['total_packets'] * 100) if self.statistics['total_packets'] > 0 else 0
            print(f\"  {protocol:20} : {count:6} pacotes ({percentage:5.1f}%)\")
        
        # Conexões HTTPS (seguras)
        print(f\"\\n🔒 Conexões HTTPS (Criptografadas): {len(self.statistics['https_connections'])}\")
        for conn in self.statistics['https_connections'][:5]:
            print(f\"  {conn['timestamp']} | {conn['source']} → {conn['destination']}:{conn['port']}\")
        
        # Requisições HTTP (inseguras)
        print(f\"\\n⚠️  Requisições HTTP (Texto Plano): {len(self.statistics['http_requests'])}\")
        for req in self.statistics['http_requests'][:5]:
            print(f\"  {req['timestamp']} | {req['source']} → {req['destination']}:{req['port']}\")
        
        # Queries DNS
        print(f\"\\n🔍 Queries DNS: {len(self.statistics['dns_queries'])}\")
        for query in self.statistics['dns_queries'][:10]:
            print(f\"  {query['timestamp']} | Query: {query['query']}\")
        
        # Dados em texto plano
        if self.statistics['unencrypted_data']:
            print(f\"\\n⚠️  DADOS EM TEXTO PLANO DETECTADOS: {len(self.statistics['unencrypted_data'])} instâncias\")
            print(\"\\nExemplos:\")
            for data in self.statistics['unencrypted_data'][:5]:
                print(f\"  {data['timestamp']} | {data['protocol']}\")
                print(f\"  {data['source']} → {data['destination']}\")
                print(f\"  Dados: {data['data'][:100]}\")
                print()
        
        print(\"=\"*100 + \"\\n\")
    
    def export_report(self, filename=\"traffic_report.json\"):
        \"\"\"Exportar relatório em JSON\"\"\"
        report = {
            'timestamp': datetime.now().isoformat(),
            'target_device': self.target_ip,
            'summary': {
                'total_packets': self.statistics['total_packets'],
                'total_bytes': self.statistics['total_bytes'],
                'protocols': dict(self.statistics['protocols']),
                'https_connections': len(self.statistics['https_connections']),
                'http_requests': len(self.statistics['http_requests']),
                'dns_queries': len(self.statistics['dns_queries']),
                'unencrypted_data': len(self.statistics['unencrypted_data'])
            },
            'details': {
                'https_connections': self.statistics['https_connections'][:20],
                'http_requests': self.statistics['http_requests'][:20],
                'dns_queries': self.statistics['dns_queries'][:20],
                'unencrypted_data': self.statistics['unencrypted_data'][:10]
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f\"[+] Relatório exportado: {filename}\")
        except Exception as e:
            print(f\"[!] Erro ao exportar: {e}\")
    
    def run(self):
        \"\"\"Iniciar captura\"\"\"
        print(\"\\n\" + \"=\"*100)
        print(\"🔍 CAPTURA AVANÇADA DE TRÁFEGO - CELULAR 04 (VÍTIMA)\")
        print(\"=\"*100 + \"\\n\")
        
        print(f\"[+] Alvo: {self.target_ip}\")
        print(f\"[+] Interface: {self.interface if self.interface else 'Padrão'}\")
        print(\"[*] Capturando pacotes REAIS... Pressione Ctrl+C para parar\\n\")
        
        try:
            sniff(
                prn=self.packet_callback,
                iface=self.interface,
                store=False,
                filter=f\"host {self.target_ip}\"
            )
        
        except KeyboardInterrupt:
            print(\"\\n\
[*] Captura interrompida\")
            self.display_statistics()
            self.export_report()
        
        except PermissionError:
            print(\"[!] Erro: Privilégios de administrador necessários\")
            print(\"    Execute com: sudo python3 advanced_traffic_capture.py\")
            sys.exit(1)
        
        except Exception as e:
            print(f\"[!] Erro: {e}\")
            sys.exit(1)

if __name__ == \"__main__\":
    import argparse
    
    parser = argparse.ArgumentParser(
        description=\"Captura avançada de tráfego REAL do celular 04\"
    )
    parser.add_argument(
        \"--interface\", \"-i\",
        help=\"Interface de rede (ex: eth0, wlan0)\",
        default=None
    )
    parser.add_argument(
        \"--target\", \"-t\",
        help=\"IP do celular 04 (vítima)\",
        default=\"192.168.1.200\"
    )
    
    args = parser.parse_args()
    
    capture = AdvancedTrafficCapture(
        interface=args.interface,
        target_ip=args.target
    )
    
    capture.run()


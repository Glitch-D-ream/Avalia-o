#!/usr/bin/env python3
"""
TrafficSpy Live - Capturador de Tráfego HTTP/HTTPS em Tempo Real
Ferramenta criativa para análise de tráfego de rede e detecção de credenciais
AVISO: Apenas para fins educacionais em ambientes controlados.
REQUER: Permissões de root/admin para captura de pacotes
"""

import sys
import time
import json
from datetime import datetime
from collections import defaultdict
import re

try:
    from scapy.all import sniff, IP, TCP, Raw, get_if_list
    SCAPY_AVAILABLE = True
except ImportError:
    print("❌ Scapy não está instalado. Instale com: sudo pip3 install scapy")
    SCAPY_AVAILABLE = False
    sys.exit(1)


class TrafficSpyLive:
    """Capturador de tráfego em tempo real"""
    
    def __init__(self, interface="eth0", target_host=None):
        """
        Inicializa o capturador
        
        Args:
            interface: Interface de rede para capturar
            target_host: Host específico para filtrar (opcional)
        """
        self.interface = interface
        self.target_host = target_host
        self.packets_captured = 0
        self.credentials_found = []
        self.http_requests = []
        self.statistics = defaultdict(int)
        self.start_time = None
        
    def packet_callback(self, packet):
        """Callback para processar cada pacote capturado"""
        self.packets_captured += 1
        
        # Verificar se é pacote IP com TCP
        if packet.haslayer(IP) and packet.haslayer(TCP):
            ip_layer = packet[IP]
            tcp_layer = packet[TCP]
            
            # Filtrar por host alvo se especificado
            if self.target_host:
                if self.target_host not in [ip_layer.src, ip_layer.dst]:
                    return
            
            # Verificar se é tráfego HTTP (porta 80)
            if tcp_layer.dport == 80 or tcp_layer.sport == 80:
                self.statistics["http_packets"] += 1
                
                if packet.haslayer(Raw):
                    payload = packet[Raw].load
                    try:
                        payload_str = payload.decode('utf-8', errors='ignore')
                        
                        # Detectar requisições HTTP
                        if payload_str.startswith(('GET ', 'POST ', 'PUT ', 'DELETE ')):
                            self.analyze_http_request(ip_layer, tcp_layer, payload_str)
                        
                        # Detectar credenciais em texto plano
                        self.detect_credentials(ip_layer, payload_str)
                        
                    except Exception as e:
                        pass
            
            # Verificar se é tráfego HTTPS (porta 443)
            elif tcp_layer.dport == 443 or tcp_layer.sport == 443:
                self.statistics["https_packets"] += 1
            
            # Outras portas comuns
            elif tcp_layer.dport in [21, 22, 23, 25, 110, 143]:
                self.statistics["other_protocols"] += 1
        
        # Mostrar progresso a cada 100 pacotes
        if self.packets_captured % 100 == 0:
            self.print_statistics()
    
    def analyze_http_request(self, ip_layer, tcp_layer, payload):
        """Analisa requisição HTTP"""
        lines = payload.split('\r\n')
        if not lines:
            return
        
        # Primeira linha contém método e URL
        request_line = lines[0]
        method = request_line.split()[0] if request_line.split() else "UNKNOWN"
        
        # Extrair headers
        headers = {}
        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        
        # Extrair body (após linha vazia)
        body = ""
        if '\r\n\r\n' in payload:
            body = payload.split('\r\n\r\n', 1)[1]
        
        request_info = {
            "timestamp": datetime.now().isoformat(),
            "src_ip": ip_layer.src,
            "dst_ip": ip_layer.dst,
            "method": method,
            "request_line": request_line,
            "headers": headers,
            "body": body[:200],  # Limitar tamanho do body
            "has_credentials": False
        }
        
        # Verificar se há credenciais no body
        if any(keyword in body.lower() for keyword in ['password', 'pass', 'pwd', 'user', 'login']):
            request_info["has_credentials"] = True
            print(f"\n⚠️  [ALERTA] Possíveis credenciais em requisição HTTP!")
            print(f"    {ip_layer.src} -> {ip_layer.dst}")
            print(f"    Método: {method}")
            print(f"    Body: {body[:100]}...")
        
        self.http_requests.append(request_info)
    
    def detect_credentials(self, ip_layer, payload):
        """Detecta credenciais em texto plano"""
        # Padrões comuns de credenciais
        patterns = {
            "username": r'(?:user|username|login|email)[:=]\s*([^\s&]+)',
            "password": r'(?:pass|password|pwd|senha)[:=]\s*([^\s&]+)',
            "token": r'(?:token|auth|authorization)[:=]\s*([^\s&]+)',
            "api_key": r'(?:api_key|apikey|key)[:=]\s*([^\s&]+)'
        }
        
        credentials = {}
        for cred_type, pattern in patterns.items():
            matches = re.findall(pattern, payload, re.IGNORECASE)
            if matches:
                credentials[cred_type] = matches[0]
        
        if credentials:
            credential_info = {
                "timestamp": datetime.now().isoformat(),
                "src_ip": ip_layer.src,
                "dst_ip": ip_layer.dst,
                "credentials": credentials,
                "protocol": "HTTP (INSEGURO)"
            }
            
            self.credentials_found.append(credential_info)
            
            print(f"\n🔴 [CREDENCIAIS DETECTADAS]")
            print(f"    Origem: {ip_layer.src}")
            print(f"    Destino: {ip_layer.dst}")
            print(f"    Dados: {json.dumps(credentials, indent=4)}")
            print(f"    ⚠️  ALERTA: Credenciais transmitidas em texto plano (HTTP)!")
    
    def print_statistics(self):
        """Imprime estatísticas em tempo real"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        packets_per_sec = self.packets_captured / elapsed if elapsed > 0 else 0
        
        print(f"\r📊 Pacotes: {self.packets_captured} | "
              f"HTTP: {self.statistics['http_packets']} | "
              f"HTTPS: {self.statistics['https_packets']} | "
              f"Credenciais: {len(self.credentials_found)} | "
              f"Taxa: {packets_per_sec:.1f} pkt/s", end='')
    
    def start_capture(self, packet_count=0, timeout=None):
        """
        Inicia captura de pacotes
        
        Args:
            packet_count: Número de pacotes para capturar (0 = infinito)
            timeout: Timeout em segundos (None = sem timeout)
        """
        if not SCAPY_AVAILABLE:
            print("❌ Scapy não disponível")
            return
        
        print(f"\n🔍 TrafficSpy Live - Iniciando Captura")
        print("="*80)
        print(f"🌐 Interface: {self.interface}")
        if self.target_host:
            print(f"🎯 Alvo: {self.target_host}")
        print(f"📦 Pacotes: {'Ilimitado' if packet_count == 0 else packet_count}")
        print(f"⏱️  Timeout: {'Sem limite' if timeout is None else f'{timeout}s'}")
        print("\n⚠️  Pressione Ctrl+C para parar a captura")
        print("="*80)
        
        self.start_time = time.time()
        
        try:
            # Filtro BPF para capturar apenas TCP
            bpf_filter = "tcp"
            if self.target_host:
                bpf_filter += f" and host {self.target_host}"
            
            sniff(
                iface=self.interface,
                prn=self.packet_callback,
                filter=bpf_filter,
                count=packet_count,
                timeout=timeout,
                store=False  # Não armazenar pacotes na memória
            )
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Captura interrompida pelo usuário")
        except PermissionError:
            print("\n❌ Erro: Permissão negada. Execute com sudo/root")
        except Exception as e:
            print(f"\n❌ Erro durante captura: {e}")
        finally:
            self.print_final_report()
    
    def print_final_report(self):
        """Imprime relatório final"""
        print("\n\n" + "="*80)
        print("📊 RELATÓRIO FINAL - TrafficSpy Live")
        print("="*80)
        
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        print(f"\n⏱️  Tempo de captura: {elapsed:.2f}s")
        print(f"📦 Total de pacotes capturados: {self.packets_captured}")
        print(f"📡 Pacotes HTTP (inseguro): {self.statistics['http_packets']}")
        print(f"🔒 Pacotes HTTPS (seguro): {self.statistics['https_packets']}")
        print(f"🔧 Outros protocolos: {self.statistics['other_protocols']}")
        
        print(f"\n🔴 Credenciais encontradas: {len(self.credentials_found)}")
        if self.credentials_found:
            print("\n⚠️  ALERTA: As seguintes credenciais foram transmitidas em texto plano:")
            for i, cred in enumerate(self.credentials_found, 1):
                print(f"\n  {i}. [{cred['timestamp']}]")
                print(f"     {cred['src_ip']} -> {cred['dst_ip']}")
                print(f"     Dados: {json.dumps(cred['credentials'], indent=8)}")
        
        print(f"\n📝 Requisições HTTP capturadas: {len(self.http_requests)}")
        if self.http_requests:
            print("\n🌐 Últimas 5 requisições HTTP:")
            for i, req in enumerate(self.http_requests[-5:], 1):
                print(f"\n  {i}. {req['method']} - {req['src_ip']} -> {req['dst_ip']}")
                print(f"     {req['request_line']}")
                if req['has_credentials']:
                    print(f"     ⚠️  Contém possíveis credenciais!")
    
    def save_report(self, output_file="trafficspy_report.json"):
        """Salva relatório em JSON"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "interface": self.interface,
            "target_host": self.target_host,
            "packets_captured": self.packets_captured,
            "statistics": dict(self.statistics),
            "credentials_found": self.credentials_found,
            "http_requests": self.http_requests[-50:]  # Últimas 50 requisições
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório salvo em: {output_file}")
        return report
    
    @staticmethod
    def list_interfaces():
        """Lista interfaces de rede disponíveis"""
        if not SCAPY_AVAILABLE:
            print("❌ Scapy não disponível")
            return []
        
        interfaces = get_if_list()
        print("\n🌐 Interfaces de rede disponíveis:")
        for i, iface in enumerate(interfaces, 1):
            print(f"  {i}. {iface}")
        return interfaces


# Exemplo de uso
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="TrafficSpy Live - Captura de Tráfego em Tempo Real")
    parser.add_argument("-i", "--interface", default="eth0", help="Interface de rede (padrão: eth0)")
    parser.add_argument("-t", "--target", help="Host alvo para filtrar")
    parser.add_argument("-c", "--count", type=int, default=0, help="Número de pacotes (0 = ilimitado)")
    parser.add_argument("-T", "--timeout", type=int, help="Timeout em segundos")
    parser.add_argument("-l", "--list", action="store_true", help="Listar interfaces disponíveis")
    
    args = parser.parse_args()
    
    if args.list:
        TrafficSpyLive.list_interfaces()
        sys.exit(0)
    
    # Verificar se está rodando como root
    if sys.platform != "win32":
        import os
        if os.geteuid() != 0:
            print("⚠️  AVISO: Este script requer permissões de root")
            print("💡 Execute com: sudo python3 trafficspy_live.py")
            sys.exit(1)
    
    spy = TrafficSpyLive(interface=args.interface, target_host=args.target)
    spy.start_capture(packet_count=args.count, timeout=args.timeout)
    spy.save_report()

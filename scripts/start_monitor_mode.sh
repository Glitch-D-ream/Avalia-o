#!/bin/bash
# Script para iniciar o modo monitor na interface Wi-Fi

INTERFACE=$1

if [ -z "$INTERFACE" ]; then
    echo "Uso: $0 <interface>"
    echo "Exemplo: $0 wlan0"
    exit 1
fi

echo "Parando o gerenciador de rede..."
sudo systemctl stop NetworkManager

echo "Derrubando a interface $INTERFACE..."
sudo ip link set $INTERFACE down

echo "Iniciando o modo monitor em $INTERFACE..."
sudo iw dev $INTERFACE set type monitor

echo "Subindo a interface $INTERFACE..."
sudo ip link set $INTERFACE up

# O nome da interface pode mudar para wlan0mon ou permanecer o mesmo dependendo do driver
# O aircrack-ng geralmente usa o nome original, mas é bom verificar
echo "Verificando o status da interface..."
iw dev $INTERFACE info

echo "Modo monitor iniciado. Use $INTERFACE para os ataques."
echo "Para parar: sudo ip link set $INTERFACE down; sudo iw dev $INTERFACE set type managed; sudo ip link set $INTERFACE up; sudo systemctl start NetworkManager"

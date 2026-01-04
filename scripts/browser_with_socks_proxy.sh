#!/bin/bash

# Script para iniciar o navegador Chromium com proxy SOCKS4 configurado

# Configurações
SOCKS_PROXY="socks4://177.126.89.63:4145"
TARGET_URL="https://99jogo66.com/?id=211995351"
PROFILE_DIR="/tmp/chromium_socks_profile"

# Cria diretório de perfil
mkdir -p "$PROFILE_DIR"

echo "[*] Iniciando navegador com proxy SOCKS4..."
echo "[*] Proxy: $SOCKS_PROXY"
echo "[*] URL: $TARGET_URL"
echo ""

# Inicia o Chromium com proxy SOCKS4
# --proxy-server: Define o proxy SOCKS4
# --proxy-bypass-list: Define quais hosts não usam proxy (deixar vazio para usar proxy para tudo)
# --no-first-run: Desabilita a primeira execução
# --no-default-browser-check: Desabilita verificação de navegador padrão

# Nota: O navegador será iniciado em background
# Para ver a janela do navegador, você precisa estar em um ambiente com display gráfico

DISPLAY=:99 xvfb-run -a chromium-browser \
  --user-data-dir="$PROFILE_DIR" \
  --proxy-server="$SOCKS_PROXY" \
  --proxy-bypass-list="" \
  --no-first-run \
  --no-default-browser-check \
  --disable-background-networking \
  --disable-client-side-phishing-detection \
  --disable-component-extensions-with-background-pages \
  --disable-default-apps \
  --disable-extensions \
  --disable-sync \
  --disable-translate \
  "$TARGET_URL" &

BROWSER_PID=$!
echo "[+] Navegador iniciado (PID: $BROWSER_PID)"
echo "[*] Aguardando 10 segundos para o carregamento da página..."
sleep 10

echo "[*] Navegador está rodando. Para parar, execute: kill $BROWSER_PID"
echo "[*] Pressione CTRL+C para encerrar este script."

# Aguarda até que o usuário pressione CTRL+C
trap "kill $BROWSER_PID 2>/dev/null; exit 0" SIGINT

wait $BROWSER_PID

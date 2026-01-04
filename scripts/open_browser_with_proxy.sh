#!/bin/bash

# Script para abrir o navegador Chromium com proxy HTTP configurado para mitmdump

# Configurações
PROXY_HOST="127.0.0.1"
PROXY_PORT="8080"
TARGET_URL="https://99jogo66.com/?id=211995351"

# Cria um diretório de perfil temporário para o Chromium
PROFILE_DIR="/tmp/chromium_proxy_profile"
mkdir -p "$PROFILE_DIR"

# Inicia o Chromium com proxy configurado
# --proxy-server: Define o proxy HTTP/HTTPS
# --no-proxy-server: Desativa o proxy do sistema (não usar neste caso)
# --proxy-bypass-list: Define quais hosts não usam proxy (deixar vazio para usar proxy para tudo)

echo "Iniciando Chromium com proxy em $PROXY_HOST:$PROXY_PORT..."
echo "Navegando para: $TARGET_URL"

chromium-browser \
  --user-data-dir="$PROFILE_DIR" \
  --proxy-server="http://$PROXY_HOST:$PROXY_PORT" \
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

echo "Chromium iniciado. Aguarde a abertura da janela..."
sleep 3

echo "Pronto! O navegador está acessando o site através do proxy mitmdump."
echo "As requisições POST serão capturadas em: mitm_post_requests.log"

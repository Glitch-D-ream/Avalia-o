#!/bin/bash

# ============================================
# INSTALADOR AUTOMÁTICO - LINUX/MAC
# Laboratório Demoníaco de Segurança Digital
# ============================================

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Diretório de instalação
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         ⚡ ASCENSÃO - CULTIVO DIGITAL ⚡                    ║"
echo "║    Laboratório Educacional de Segurança Cibernética         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

echo -e "${YELLOW}[*]${NC} Diretório de instalação: $INSTALL_DIR"
echo ""

# ============================================
# VERIFICAR PYTHON
# ============================================

echo -e "${YELLOW}[*]${NC} Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!]${NC} Python3 não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

PYTHON_PATH=$(which python3)
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}[+]${NC} Python encontrado: $PYTHON_VERSION"

# ============================================
# VERIFICAR NODE.JS
# ============================================

echo -e "${YELLOW}[*]${NC} Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}[!]${NC} Node.js não encontrado. Por favor, instale Node.js 18+"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}[+]${NC} Node.js encontrado: $NODE_VERSION"

# ============================================
# INSTALAR DEPENDÊNCIAS PYTHON
# ============================================

echo ""
echo -e "${YELLOW}[*]${NC} Instalando dependências Python..."
cd "$INSTALL_DIR"

if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --quiet
    echo -e "${GREEN}[+]${NC} Dependências Python instaladas"
else
    echo -e "${YELLOW}[!]${NC} requirements.txt não encontrado"
fi

# ============================================
# INSTALAR DEPENDÊNCIAS NODE
# ============================================

echo ""
echo -e "${YELLOW}[*]${NC} Verificando dependências Node.js..."
if [ -f "package.json" ]; then
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}[*]${NC} Instalando npm packages..."
        npm install --silent
        echo -e "${GREEN}[+]${NC} Dependências Node.js instaladas"
    else
        echo -e "${GREEN}[+]${NC} Dependências Node.js já instaladas"
    fi
fi

# ============================================
# INICIAR APLICAÇÃO
# ============================================

echo ""
echo -e "${GREEN}[+]${NC} Iniciando aplicação..."
echo ""

# Iniciar servidor Flask em background
python3 "$INSTALL_DIR/server.py" &
FLASK_PID=$!
sleep 3

# Iniciar site web
npm run dev &
WEB_PID=$!

# Aguardar um pouco e abrir no navegador
sleep 5

# Tentar abrir no navegador (diferentes comandos para diferentes SOs)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    open http://localhost:3000
fi

echo ""
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              ✅ APLICAÇÃO INICIADA COM SUCESSO!             ║"
echo "║                                                              ║"
echo "║  🌐 Site Web: http://localhost:3000                         ║"
echo "║  🔧 Servidor: http://localhost:5000                         ║"
echo "║                                                              ║"
echo "║  Pressione Ctrl+C para encerrar                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Aguardar interrupção
wait

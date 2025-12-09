@echo off
title ACSA Hacking Educacional - Instalador e Inicializador

echo =======================================================
echo  INICIANDO INSTALAÇÃO E CONFIGURAÇÃO (WINDOWS)
echo  O PROJETO REQUER PRIVILÉGIOS DE ADMINISTRADOR
echo =======================================================

:: 1. VERIFICAR SE PYTHON ESTA INSTALADO
python --version 2>NUL
IF ERRORLEVEL 1 (
    echo.
    echo ERRO: Python nao encontrado. Por favor, instale o Python 3.10+ e tente novamente.
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 2. CRIAR E ATIVAR AMBIENTE VIRTUAL
echo.
echo [1/4] Criando e ativando ambiente virtual...
python -m venv venv
call venv\Scripts\activate

:: 3. INSTALAR DEPENDENCIAS PYTHON
echo.
echo [2/4] Instalando dependencias Python (Scapy, Paramiko, etc.)...
pip install -r requirements.txt

:: 4. VERIFICAR FERRAMENTAS DE SISTEMA (NMAP e DIRB)
:: Nmap e Dirb sao cruciais. No Windows, o Nmap precisa ser instalado separadamente.
echo.
echo [3/4] Verificando Nmap e Dirb...
where nmap >NUL 2>NUL
IF ERRORLEVEL 1 (
    echo.
    echo AVISO: Nmap nao encontrado. Por favor, instale o Nmap para que o scanner funcione.
    echo Baixe em: https://nmap.org/download.html
    pause
)
where dirb >NUL 2>NUL
IF ERRORLEVEL 1 (
    echo.
    echo AVISO: Dirb nao encontrado. O scanner web nao funcionara.
    pause
)

:: 5. INICIAR SERVIDOR E CLIENTE DE CAPTURA
echo.
echo =======================================================
echo [4/4] INICIANDO SERVIDOR E CLIENTE DE CAPTURA
echo =======================================================
echo.
echo O servidor sera iniciado em uma nova janela.
echo O cliente de captura (sniffer) sera iniciado em outra janela (requer permissao).
echo.
pause

:: Iniciar o Servidor FastAPI (Terminal 1)
start cmd /k "title ACSA - Servidor FastAPI & uvicorn server:app --reload --host 0.0.0.0 --port 8000"

:: Iniciar o Cliente de Captura (Terminal 2)
:: No Windows, o Scapy requer a execucao como Administrador para capturar pacotes.
:: O comando 'start' nao eleva privilegios, entao o usuario deve ser instruido a executar o cliente manualmente como Admin.
echo.
echo =======================================================
echo PASSO FINAL: INICIAR O SNIFFER MANUALMENTE
echo =======================================================
echo.
echo POR FAVOR, ABRA UM NOVO PROMPT DE COMANDO (CMD) COMO ADMINISTRADOR
echo E EXECUTE O SEGUINTE COMANDO:
echo.
echo cd /d "%CD%"
echo python capture_traffic_client.py -i <SUA_INTERFACE_DE_REDE>
echo.
echo (Ex: python capture_traffic_client.py -i Wi-Fi)
echo.
echo O servidor esta rodando. Pressione qualquer tecla para fechar este instalador.
pause
exit /b 0

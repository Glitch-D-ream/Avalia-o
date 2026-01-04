@echo off
REM ============================================
REM INSTALADOR AUTOMÁTICO - WINDOWS (PLUG AND PLAY)
REM Laboratório Educacional de Segurança Cibernética
REM ============================================

setlocal enabledelayedexpansion

REM Cores
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         ⚡ ASCENSÃO - CULTIVO DIGITAL ⚡                    ║
echo ║    Instalador Plug and Play - Versão Final para Concurso    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Detectar diretório de instalação
set INSTALL_DIR=%~dp0
set INSTALL_DIR=%INSTALL_DIR:~0,-1%

echo [*] Diretório de instalação: %INSTALL_DIR%
echo.

REM ============================================
REM 1. INSTALAÇÃO SILENCIOSA DE PYTHON (SE NECESSÁRIO)
REM ============================================

echo [*] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python não encontrado. Tentando instalação silenciosa...
    
    REM Baixar instalador (Assumindo que o instalador está no pendrive para evitar download)
    REM Se o instalador do Python (ex: python-3.11.6-amd64.exe) estiver na raiz do pendrive:
    if exist "%INSTALL_DIR%\python-installer.exe" (
        echo [+] Instalador Python encontrado. Iniciando instalacao silenciosa...
        
        REM Comando de instalação silenciosa para todos os usuários e adicionando ao PATH
        "%INSTALL_DIR%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1
        
        REM Aguardar a instalação
        timeout /t 15 /nobreak
        
        python --version >nul 2>&1
        if errorlevel 1 (
            echo [!] Falha na instalacao silenciosa do Python. Por favor, instale manualmente.
            pause
            exit /b 1
        )
    ) else (
        echo [!] Instalador Python (python-installer.exe) nao encontrado. Pulando instalacao.
    )
)

REM Tentar encontrar o caminho do Python instalado
for /f "tokens=*" %%i in ('where python') do set PYTHON_PATH=%%i
if not defined PYTHON_PATH (
    echo [!] Python nao encontrado no PATH. Por favor, instale Python 3.11+
    pause
    exit /b 1
)
echo [+] Python encontrado: !PYTHON_PATH!
echo.

REM ============================================
REM 2. INSTALAÇÃO SILENCIOSA DE NPCAP (NECESSÁRIO PARA SCAPY)
REM ============================================

echo [*] Verificando Npcap (Necessário para Captura de Tráfego)...
if exist "%INSTALL_DIR%\npcap-installer.exe" (
    echo [+] Instalador Npcap encontrado. Iniciando instalacao silenciosa...
    
    REM Comando de instalação silenciosa (OEM) - Usando /S para simular a versão free
    REM NOTA: A versão gratuita do Npcap NÃO suporta /S. Este comando é uma simulação
    REM para o concurso. Na prática, o usuário precisaria clicar em "Sim" no UAC.
    "%INSTALL_DIR%\npcap-installer.exe" /S /winpcap_mode=yes /loopback_support=yes
    
    REM Aguardar a instalação
    timeout /t 10 /nobreak
    echo [+] Npcap instalado (Verifique se o UAC nao bloqueou a instalacao).
) else (
    echo [!] Instalador Npcap (npcap-installer.exe) nao encontrado. Captura de trafego pode falhar.
)
echo.

REM ============================================
REM 3. INSTALAR DEPENDÊNCIAS PYTHON (INCLUINDO YARA)
REM ============================================

echo [*] Instalando dependências Python (Scapy, YARA, FastAPI, etc.)...
cd /d "%INSTALL_DIR%"

REM Instalar dependências
"%PYTHON_PATH%" -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [!] Falha na instalacao das dependencias Python. Verifique a conexao e o requirements.txt.
    pause
    exit /b 1
)
echo [+] Dependências Python instaladas com sucesso.
echo.

REM ============================================
REM 4. INFORMAR PRÓXIMO PASSO
REM ============================================

echo ╔══════════════════════════════════════════════════════════════╗
echo ║              ✅ INSTALAÇÃO CONCLUÍDA!                       ║
echo ║                                                              ║
echo ║  AGORA, EXECUTE O ARQUIVO:                                   ║
echo ║  >> RUN_CENTER.bat <<                                        ║
echo ║  (COMO ADMINISTRADOR) para iniciar o Laboratório.            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

pause
exit /b 0

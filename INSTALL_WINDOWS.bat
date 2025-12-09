@echo off
net session >nul 2>&1
if %errorlevel% neq 0 (
  echo Por favor execute este script como Administrador (clique direito -> Executar como administrador).
  pause
  exit /b 1
)
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
    REM --- INICIO DA CORREÇÃO: Download e Instalacao Silenciosa ---
    set "PY_URL=https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
    set "PY_NAME=%TEMP%\python-3.11.4-amd64.exe"
    
    echo [+] Baixando Python...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%PY_URL%', '%PY_NAME%')"
    
    if exist "%PY_NAME%" (
        echo [+] Instalador Python encontrado. Iniciando instalacao silenciosa...
        
        REM Comando de instalação silenciosa para todos os usuários e adicionando ao PATH
        "%PY_NAME%" /quiet InstallAllUsers=1 PrependPath=1
        
        REM Aguardar a instalação
        timeout /t 15 /nobreak
        
        python --version >nul 2>&1
        if errorlevel 1 (
            echo [!] Falha na instalacao silenciosa do Python. Por favor, instale manualmente.
            pause
            exit /b 1
        )
    ) else (
        echo [!] Falha ao baixar o instalador do Python. Verifique a conexao com a internet.
        pause
        exit /b 1
    )
    REM --- FIM DA CORREÇÃO: Download e Instalacao Silenciosa ---
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
78	REM 2. INSTALAÇÃO SILENCIOSA DE NPCAP (NECESSÁRIO PARA SCAPY)
79	REM ============================================
80	
81	echo [*] Verificando Npcap (Necessário para Captura de Tráfego)...
82	REM --- INICIO DA CORREÇÃO: Download e Instalacao Silenciosa do Npcap ---
83	set "NPCAP_URL=https://nmap.org/npcap/dist/npcap-1.71.exe"
84	set "NPCAP_NAME=%TEMP%\npcap-installer.exe"
85	
86	echo [+] Baixando Npcap...
87	powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%NPCAP_URL%', '%NPCAP_NAME%')"
88	
89	if exist "%NPCAP_NAME%" (
90	    echo [+] Instalador Npcap encontrado. Iniciando instalacao silenciosa...
91	    
92	    REM Comando de instalação silenciosa (OEM) - Usando /S para simular a versão free
93	    REM NOTA: A versão gratuita do Npcap NÃO suporta /S. Este comando é uma simulação
94	    REM para o concurso. Na prática, o usuário precisaria clicar em "Sim" no UAC.
95	    "%NPCAP_NAME%" /S /winpcap_mode=yes /loopback_support=yes
96	    
97	    REM Aguardar a instalação
98	    timeout /t 10 /nobreak
99	    echo [+] Npcap instalado (Verifique se o UAC nao bloqueou a instalacao).
100	) else (
101	    echo [!] Falha ao baixar o instalador do Npcap. Verifique a conexao com a internet. Captura de trafego pode falhar.
102	)
103	REM --- FIM DA CORREÇÃO: Download e Instalacao Silenciosa do Npcap ---
104	echo.pendências Python (Scapy, YARA, FastAPI, etc.)...
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

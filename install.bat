@echo off
ECHO =================================================================
ECHO  ASCENSÃO CULTIVO DIGITAL - INSTALADOR AUTOMATIZADO (WINDOWS)
ECHO  Preparando o Notebook 01 (Servidor C2) para a Fase 2.
ECHO =================================================================

:: -----------------------------------------------------------------
:: 1. VERIFICAR E INSTALAR PYTHON (Se necessario)
:: -----------------------------------------------------------------
ECHO.
ECHO [1/5] Verificando e instalando Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python nao encontrado. Baixando e instalando...
    :: Este e um placeholder. Em um ambiente real, o instalador seria baixado.
    :: Para o concurso, assumimos que o Python 3.11+ esta disponivel ou sera instalado manualmente.
    ECHO Por favor, certifique-se de que o Python 3.11+ esta instalado e no PATH.
    PAUSE
) ELSE (
    ECHO Python ja instalado.
)

:: -----------------------------------------------------------------
:: 2. INSTALAR DEPENDENCIAS PYTHON
:: -----------------------------------------------------------------
ECHO.
ECHO [2/5] Instalando dependencias Python (Backend)...
python -m pip install --upgrade pip
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERRO: Falha ao instalar dependencias Python. Verifique o log.
    PAUSE
    EXIT /B 1
)
ECHO Dependencias Python instaladas com sucesso.

:: -----------------------------------------------------------------
:: 3. VERIFICAR E INSTALAR NODE.JS/PNPM (Se necessario)
:: -----------------------------------------------------------------
ECHO.
ECHO [3/5] Verificando e instalando Node.js e pnpm...
node --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Node.js nao encontrado. Baixando e instalando...
    ECHO Por favor, certifique-se de que o Node.js 20+ esta instalado.
    PAUSE
) ELSE (
    ECHO Node.js ja instalado.
)

pnpm --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO pnpm nao encontrado. Instalando...
    npm install -g pnpm
    IF %ERRORLEVEL% NEQ 0 (
        ECHO ERRO: Falha ao instalar pnpm.
        PAUSE
        EXIT /B 1
    )
)
ECHO Node.js e pnpm prontos.

:: -----------------------------------------------------------------
:: 4. INSTALAR DEPENDENCIAS NODE.JS E GERAR BUILD DO FRONTEND
:: -----------------------------------------------------------------
ECHO.
ECHO [4/5] Instalando dependencias Node.js e gerando build do Frontend (Dashboard C2)...
pnpm install
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERRO: Falha ao instalar dependencias Node.js.
    PAUSE
    EXIT /B 1
)

pnpm run build
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERRO: Falha ao gerar o build do Frontend.
    PAUSE
    EXIT /B 1
)
ECHO Frontend (Dashboard C2) gerado com sucesso na pasta dist/public.

:: -----------------------------------------------------------------
:: 5. CRIAR SCRIPT DE EXECUCAO
:: -----------------------------------------------------------------
ECHO.
ECHO [5/5] Criando script de execucao (start.bat)...
ECHO @echo off > start.bat
ECHO ECHO ================================================================= >> start.bat
ECHO ECHO  ASCENSÃO CULTIVO DIGITAL - INICIANDO SERVIDOR C2 >> start.bat
ECHO ECHO ================================================================= >> start.bat
ECHO ECHO [1/2] Iniciando Servidor C2 (Backend - FastAPI) na porta 8000... >> start.bat
ECHO start /B python -m uvicorn server_fixed:app --host 192.168.1.100 --port 8000 >> start.bat
ECHO ECHO [2/2] Servidor C2 Iniciado. Acesse o Dashboard C2 no seu navegador. >> start.bat
ECHO ECHO IP do Servidor C2 (Notebook 01): 192.168.1.100:8000 >> start.bat
ECHO ECHO Pressione qualquer tecla para fechar esta janela. >> start.bat
ECHO PAUSE >> start.bat
ECHO EXIT /B 0 >> start.bat

ECHO Instalacao concluida com sucesso!
ECHO Execute START.BAT para iniciar o Servidor C2.
ECHO =================================================================
PAUSE
EXIT /B 0

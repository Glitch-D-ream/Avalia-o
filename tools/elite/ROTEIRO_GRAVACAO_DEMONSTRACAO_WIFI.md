# Roteiro de Gravação Profissional para Demonstração de Auditoria Wi-Fi

Este roteiro detalha os passos para gravar a execução do módulo `WiFiAuditCenter`, garantindo uma apresentação visualmente impactante e tecnicamente precisa para o seu professor.

## 1. Pré-requisitos para a Gravação

1.  **Hardware:** Um computador (preferencialmente Linux, como Kali ou Ubuntu) com uma placa de rede Wi-Fi que suporte **modo monitor** e **injeção de pacotes**.
2.  **Ambiente:** O ambiente de teste controlado e isolado, com pelo menos um Ponto de Acesso (AP) e um dispositivo cliente conectado a ele.
3.  **Software:** O projeto `Avalia-o` clonado e as dependências instaladas (`python3`, `scapy`, `aircrack-ng suite`).
4.  **Wordlist:** Certifique-se de que a wordlist (`resources/wordlists/pass_list.txt`) contenha a senha da rede de teste para garantir o sucesso da quebra.

## 2. Roteiro de Ação e Narração (Sugestão)

| Etapa | Ação na Tela | Narração Sugerida (Foco Técnico) |
| :--- | :--- | :--- |
| **0. Preparação** | Abra o terminal. Use o script `start_monitor_mode.sh` para ativar o modo monitor. | "Iniciamos a auditoria ativando o **Modo Monitor** na interface de rádio (`wlan0mon`). Isso é crucial, pois nos permite capturar todos os pacotes 802.11 na Camada 2, sem a necessidade de estarmos conectados à rede." |
| **1. Execução** | Execute o script principal: `sudo python3 tools/wifi_audit_center.py wlan0mon` | "O `WiFiAuditCenter` é o nosso orquestrador. Ele inicia o ciclo de auditoria com a fase de **Reconhecimento Passivo**." |
| **2. Reconhecimento** | A tela mostra a detecção das redes (SSID, BSSID, Canal). | "Utilizando **Scapy**, o sistema realiza um *sniffing* passivo, analisando os *Beacon Frames* para mapear a topologia da rede. Note que identificamos o AP alvo, `LABORATÓRIO_PRIVADO`, e o cliente associado, `00:11:22:33:44:55`." |
| **3. Captura** | O sistema inicia o `airodump-ng` (em segundo plano, simulado pelo log). | "O sistema seleciona o alvo e inicia o `airodump-ng` para escutar o canal 6, aguardando o **4-way Handshake** WPA2. Este é o material criptográfico que precisamos para a quebra de senha." |
| **4. Ataque Ativo** | O log mostra a execução do `aireplay-ng` e a mensagem de *Deauth*. | "Para acelerar a coleta, o sistema executa um **Ataque de Desautenticação** direcionado ao cliente. Isso força o cliente a se reconectar, gerando o *handshake* que o `airodump-ng` captura. Esta é a técnica de **coleta de dados ativa**." |
| **5. Evidência** | A tela mostra a mensagem de que o *handshake* foi capturado (`.cap` file). | "O *handshake* foi capturado com sucesso e salvo como evidência forense. O próximo passo é a **Análise de Vulnerabilidade**." |
| **6. Análise** | O sistema executa o `aircrack-ng` com a wordlist. | "O `aircrack-ng` é invocado para testar a robustez da senha contra a nossa *wordlist*. Em um ambiente real, isso testa a política de senhas da organização." |
| **7. Resultado** | A tela exibe a mensagem de **VULNERABILIDADE CRÍTICA** e a senha encontrada. | "A quebra foi bem-sucedida, revelando a senha `Admin@2026`. Isso demonstra a falha na política de senhas e a eficácia da nossa ferramenta em identificar vulnerabilidades críticas de segurança de rede." |
| **8. Finalização** | Use o script `stop_monitor_mode.sh` para retornar ao modo normal. | "Finalizamos a auditoria, retornando a interface ao modo gerenciado. Todo o processo foi registrado em `logs/wifi_audit.log` para rastreabilidade e análise forense." |

## 3. Dicas para a Gravação

*   **Zoom:** Dê zoom no terminal para que o texto seja perfeitamente legível.
*   **Velocidade:** Não tenha pressa. Deixe cada etapa do log aparecer por tempo suficiente para que o professor possa ler as mensagens técnicas (e.g., `Dot11Beacon`, `4-way Handshake`, `KEY FOUND!`).
*   **Tom:** Mantenha um tom profissional e didático, explicando o *porquê* de cada etapa técnica.

Com este roteiro e o relatório forense, sua apresentação será de altíssimo nível.

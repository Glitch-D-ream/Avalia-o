# CENÁRIO DE DEMONSTRAÇÃO PRÁTICA - KIT DE EDUCAÇÃO HACKER (V15.0)

Este roteiro foi criado para ser o seu "script de ataque" no concurso. Ele enfatiza a **ação ofensiva real** e a **exploração de vulnerabilidades** usando a sua Arquitetura de Sinergia de 4 Dispositivos.

## 1. Configuração Inicial: O Laboratório de Exploração

**Objetivo:** Mostrar que o ambiente é um laboratório de hacking controlado e funcional.

| Dispositivo | Função no Laboratório |
| :--- | :--- |
| **Notebook (Central)** | Roda o Servidor FastAPI (Dashboard) e o Cliente de Captura de Tráfego (o "Sniffer"). |
| **Roteador Velho (Ponte)** | Cria a rede Wi-Fi isolada (`192.168.x.x`) que será o campo de batalha. |
| **Celular Principal (Vítima)** | O alvo das ações ofensivas (tráfego e scan). |
| **Celular Velho (Atacante)** | O dispositivo que executa o ataque de força bruta. |

**Passos de Configuração:**

1.  **Conecte** todos os 4 dispositivos à rede Wi-Fi criada pelo **Roteador Velho**.
2.  **No Notebook (Central):** Inicie o Servidor FastAPI (o Dashboard).
    ```bash
    cd security_education_kit
    uvicorn server:app --reload --host 0.0.0.0 --port 8000
    ```
3.  **No Notebook (Central):** Em um novo terminal, inicie o Cliente de Captura de Tráfego.
    *   **Ação Hacker:** "Este é o nosso **sniffer** rodando em modo passivo. Ele está pronto para interceptar qualquer comunicação insegura na rede."
    ```bash
    sudo python3 capture_traffic_client.py -i <INTERFACE_DE_REDE>
    ```
4.  **Abra o Dashboard:** No navegador do Notebook, acesse `http://127.0.0.1:8000`.

## 2. Ataque 1: Varredura de Vulnerabilidades (Reconhecimento Ativo)

**Objetivo:** Usar uma ferramenta de reconhecimento real (`Nmap`) para mapear e identificar vulnerabilidades nos alvos (Vítima e Roteador).

1.  **Inicie o Scan:**
    *   **Ação Hacker:** "Vamos começar com o reconhecimento ativo. Usaremos o nosso módulo de varredura, que integra o **Nmap**, para mapear os dispositivos na rede e identificar portas abertas e serviços vulneráveis."
    *   No Dashboard, inicie o scan contra a rede isolada (ex: `192.168.1.0/24`).
2.  **Análise de Resultados:**
    *   **No Dashboard:** Mostre o relatório técnico gerado pelo Nmap.
    *   **Ponto de Exploração:** "O scan revela que o **Celular Vítima** tem a porta **80 (HTTP)** aberta. Isso é uma vulnerabilidade crítica, pois nos permite interceptar o tráfego em texto plano. O **Roteador** também tem portas abertas que podem ser exploradas."
    *   **Impacto:** O projeto mostra que o reconhecimento é o primeiro passo para a exploração.

## 3. Ataque 2: Sniffing de Credenciais (Exploração Passiva)

**Objetivo:** Explorar a vulnerabilidade HTTP identificada no Ataque 1 para roubar credenciais em tempo real.

| Ação | Dispositivo Envolvido | Ponto de Exploração |
| :--- | :--- | :--- |
| **Preparação** | **Notebook (Central)** | "Nosso sniffer está rodando e monitorando o tráfego. Estamos esperando que o alvo cometa um erro." |
| **Exploração** | **Celular Principal (Vítima)** navega em um site HTTP (ex: `http://neverssl.com`) e insere credenciais simuladas em um formulário HTTP. | **No Dashboard:** O painel de tráfego mostra o aumento de pacotes **HTTP (Texto Plano)**. |
| **Captura em Tempo Real** | **Notebook (Central)** | O Dashboard exibe um **Alerta Crítico** em tempo real. **Aponte para a tela:** "Aqui está! O sniffer interceptou o tráfego e extraiu as credenciais em texto plano. A vítima não percebeu nada, mas acabamos de comprometer a conta dela." |
| **Demonstração de Defesa** | **Celular Principal (Vítima)** navega em um site HTTPS. | "Agora, se a vítima usar um site seguro (HTTPS), o tráfego é ilegível. Isso mostra que a **criptografia** é a única defesa contra este tipo de ataque." |

## 4. Ataque 3: Força Bruta Interativa (Comprometimento de Serviço)

**Objetivo:** Demonstrar a quebra de senha de um serviço (simulado no Notebook) usando um ataque de dicionário real.

| Ação | Dispositivo Envolvido | Ponto de Exploração |
| :--- | :--- | :--- |
| **Ataque de Rede** | **Celular Velho (Atacante)** (ou o Notebook) inicia o ataque de força bruta. | "Usaremos o **Celular Atacante** para lançar um ataque de dicionário contra o serviço de login no Notebook. Cada tentativa é uma requisição HTTP POST real." |
| **Monitoramento** | **Notebook (Central)** | **No Dashboard:** Mostre o log de tentativas sendo atualizado em tempo real. |
| **Sucesso e Impacto** | **Notebook (Central)** | A senha é encontrada. **Ponto de Exploração:** "A senha foi quebrada em segundos. Isso demonstra que senhas fracas são a porta de entrada mais comum para um sistema. O projeto transforma a teoria em uma demonstração de **comprometimento de serviço** em tempo real." |

## 5. Conclusão: O Poder da Educação Hacker

**Mensagem Final:** "O Kit de Educação Hacker V15.0 é um **laboratório de exploração funcional**. Ele utiliza ferramentas reais (`Nmap`, `Scapy`, `Requests`) para simular ataques de reconhecimento, exploração e comprometimento em uma rede isolada. Ao entender como o ataque funciona, o aluno pode construir defesas mais robustas. **Transformamos a teoria em ação real e controlada.**"

---
*Este roteiro deve ser usado como um guia. Certifique-se de que o servidor e o cliente de captura estejam rodando antes da demonstração.*

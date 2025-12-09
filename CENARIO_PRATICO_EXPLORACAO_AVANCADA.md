# CENÁRIO DE DEMONSTRAÇÃO PRÁTICA - KIT DE EDUCAÇÃO HACKER: EXPLORAÇÃO AVANÇADA (V15.0)

Este é o roteiro final, focado na **Exploração Técnica e Coleta de Dados Reais**, utilizando as ferramentas mais avançadas que integramos (`Nmap`, `Scapy`, `requests-html`, `ServiceExploit`). O objetivo é demonstrar o ciclo completo de um ataque em um ambiente controlado e verificado.

## 1. Configuração Inicial: O Laboratório de Exploração

**Objetivo:** Mostrar que o ambiente é um laboratório de hacking controlado e funcional.

| Dispositivo | Função no Laboratório |
| :--- | :--- |
| **Notebook (Central)** | Roda o Servidor FastAPI (Dashboard), o Cliente de Captura de Tráfego e o Alvo de Ataque. |
| **Roteador Velho (Ponte)** | Cria a rede Wi-Fi isolada. |
| **Celular Principal (Vítima)** | O alvo da coleta de dados e do reconhecimento. |
| **Celular Velho (Atacante)** | O dispositivo que executa o ataque de força bruta e simula a exploração. |

**Passos de Configuração:** (Os mesmos passos técnicos de inicialização)

## 2. Cenário 1: Coleta de Dados Web (OSINT) e Reconhecimento Ativo

**Objetivo:** Coletar informações valiosas sobre o alvo externo (site robusto) e mapear a rede interna.

1.  **Coleta de Dados Web (OSINT):**
    *   **Ação Hacker:** "Vamos começar com a **Coleta de Dados Web (OSINT)**. Usaremos o nosso módulo que integra o **`requests-html`** para coletar links, imagens e metadados do **site robusto do concurso** (o alvo externo). Isso nos dá informações para planejar o ataque."
    *   No Dashboard, inicie a coleta contra o URL do site robusto.
    *   **Ponto de Exploração:** "O projeto demonstra a coleta de dados públicos que podem revelar a tecnologia usada pelo alvo, o que é o primeiro passo para a exploração."

2.  **Reconhecimento Ativo (Nmap):**
    *   **Ação Hacker:** "Agora, vamos usar o **Nmap** para mapear a rede interna e o **Celular Vítima** em busca de portas abertas e serviços vulneráveis."
    *   No Dashboard, inicie o scan contra a rede isolada.
    *   **Ponto de Exploração:** "O Nmap revela portas abertas. Se encontrarmos um serviço rodando, podemos tentar a exploração."

## 3. Cenário 2: Exploração de Serviço (DoS) e Coleta de Dados (Sniffing)

**Objetivo:** Demonstrar a exploração de um serviço e a coleta de dados como resultado da vulnerabilidade.

1.  **Exploração de Serviço (DoS):**
    *   **Ação Hacker:** "Identificamos uma porta aberta no **Celular Vítima** (ou no Roteador). Vamos usar o nosso módulo de **Exploração de Serviço** (`service_exploit.py` com `Scapy`) para lançar um ataque de **TCP SYN Flood** contra essa porta."
    *   No Dashboard, inicie o ataque contra o IP e a porta do alvo.
    *   **Ponto de Exploração:** "O ataque DoS demonstra a exploração de um serviço. O alvo pode ficar lento ou indisponível. O projeto mostra a **execução técnica** de um ataque de negação de serviço."

2.  **Coleta de Dados em Texto Plano (Sniffing Real):**
    *   **Ação Hacker:** "Enquanto o ataque DoS distrai, nosso sniffer continua a **coleta de dados passiva**."
    *   O **Celular Principal (Vítima)** acessa um site HTTP e insere credenciais simuladas.
    *   **No Dashboard:** O **Alerta Crítico** de credenciais é acionado.
    *   **Ponto de Exploração:** "A coleta de dados foi bem-sucedida. O sniffer interceptou o tráfego e extraiu as credenciais/dados em texto plano. **Isso é coleta de dados real**, e a vítima não percebeu nada."

## 4. Cenário 3: Comprometimento de Serviço (Força Bruta)

**Objetivo:** Demonstrar o comprometimento de um serviço e a coleta da senha de acesso.

1.  **Ataque de Exploração:**
    *   **Ação Hacker:** "Usaremos o **Celular Velho (Atacante)** para executar um ataque de força bruta contra o serviço de login no Notebook. Cada tentativa é uma requisição HTTP POST real."
2.  **Monitoramento e Coleta:**
    *   **No Dashboard:** O log de tentativas é atualizado em tempo real.
    *   **Ponto de Exploração:** "A senha é quebrada. Isso demonstra o **comprometimento de serviço** e a coleta da senha de acesso. O projeto mostra a execução técnica do ataque e a coleta da informação mais valiosa: a credencial."

## 5. Conclusão: O Kit de Exploração e Coleta

**Mensagem Final:** "O Kit de Educação Hacker V15.0 é um **laboratório de exploração e coleta de dados**. Ele utiliza ferramentas reais (`Nmap`, `Scapy`, `requests-html`) para demonstrar o ciclo completo de um ataque: **Coleta de Informações (OSINT)**, **Exploração de Serviço (DoS)** e **Coleta de Dados (Credenciais)**. O projeto transforma a teoria em **execução técnica real e verificável** no ambiente isolado do concurso."

---
*Este roteiro deve ser usado como um guia. Certifique-se de que o servidor e o cliente de captura estejam rodando antes da demonstração.*

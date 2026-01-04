# CENÁRIO DE DEMONSTRAÇÃO PRÁTICA - KIT DE EDUCAÇÃO HACKER: EXPLORAÇÃO FINAL (V15.0)

Este é o roteiro definitivo, focado na **Execução Técnica Real** de ataques e coleta de dados, utilizando as ferramentas cinzentas integradas. O objetivo é demonstrar o ciclo completo de um ataque em um ambiente controlado e verificado.

## 1. Configuração Inicial: O Laboratório de Exploração

**Objetivo:** Mostrar que o ambiente é um laboratório de hacking controlado e funcional.

| Dispositivo | Função no Laboratório | Ferramentas |
| :--- | :--- | :--- |
| **Notebook (Central)** | Servidor FastAPI (Dashboard), Sniffer (`Scapy`), Alvo de Ataque. | `python-nmap`, `requests-html`, `dirb`, `paramiko` |
| **Roteador Velho (Ponte)** | Rede Wi-Fi isolada. | N/A |
| **Celular Principal (Vítima)** | Alvo de Coleta de Dados e Reconhecimento. | N/A |
| **Celular Velho (Atacante)** | Executa o ataque de força bruta. | N/A |

**Passos de Configuração:** (Os mesmos passos técnicos de inicialização)

## 2. Fase 1: Reconhecimento e Coleta de Metadados (OSINT/Nmap/Dirb)

**Objetivo:** Coletar informações valiosas sobre o alvo externo (site robusto) e mapear a rede interna.

1.  **Coleta de Dados Web (OSINT - `requests-html`):**
    *   **Ação Hacker:** "Vamos começar com a **Coleta de Dados Web (OSINT)**. Usaremos o nosso módulo que integra o **`requests-html`** para coletar links, imagens e metadados do **site robusto do concurso**. Isso nos dá informações para planejar o ataque."
    *   No Dashboard, inicie a coleta contra o URL do site robusto.
    *   **Ponto de Exploração:** Demonstre a coleta de dados públicos que revelam a tecnologia usada pelo alvo.

2.  **Reconhecimento Ativo Avançado (Nmap Scripting Engine - NSE):**
    *   **Ação Hacker:** "Agora, usamos o **Nmap** com o **NSE** para mapear a rede interna e o **Celular Vítima** em busca de vulnerabilidades técnicas."
    *   No Dashboard, inicie o scan contra a rede isolada.
    *   **Ponto de Exploração:** O Dashboard exibe a saída dos scripts NSE (`http-enum`, `ssl-enum-ciphers`), mostrando a **detecção real de vulnerabilidades** e não apenas portas abertas.

3.  **Enumeração de Diretórios (Dirb):**
    *   **Ação Hacker:** "Para o site robusto, vamos usar o **`dirb`** (alternativa real ao Burp Suite) para tentar encontrar *endpoints* ocultos."
    *   No Dashboard, inicie o scan `dirb` contra o URL do site robusto.
    *   **Ponto de Exploração:** Demonstre a **coleta de dados de estrutura** do site, que pode revelar áreas de administração ou arquivos de configuração.

## 3. Fase 2: Exploração e Coleta de Credenciais

**Objetivo:** Executar ataques reais para comprometer serviços e coletar dados sensíveis.

1.  **Exploração de Serviço (Força Bruta SSH - `paramiko`):**
    *   **Ação Hacker:** "O Nmap encontrou um serviço SSH aberto no alvo. Vamos usar o nosso módulo de **Exploração SSH** (`exploit_ssh.py` com **`paramiko`**) para tentar um ataque de força bruta real."
    *   No Dashboard, inicie o ataque contra o IP do alvo (ex: Roteador ou um alvo simulado).
    *   **Ponto de Exploração:** O log em tempo real mostra as tentativas de login. O sucesso demonstra o **comprometimento de serviço** e a **coleta da credencial** de acesso.

2.  **Coleta de Dados em Tráfego Inseguro (Sniffing Real - `Scapy`):**
    *   **Ação Hacker:** "Enquanto os ataques ativos rolam, nosso sniffer continua a **coleta de dados passiva**."
    *   O **Celular Principal (Vítima)** acessa um site HTTP e insere credenciais simuladas.
    *   **No Dashboard:** O **Alerta Crítico** de credenciais é acionado.
    *   **Ponto de Exploração:** Demonstre a **coleta de dados real** (credenciais e informações) em texto plano, provando a vulnerabilidade do protocolo.

3.  **Exploração de Serviço (DoS - `Scapy`):**
    *   **Ação Hacker:** "Para finalizar, vamos demonstrar a exploração de um serviço com o ataque de **TCP SYN Flood**."
    *   No Dashboard, inicie o ataque contra o IP e a porta do alvo.
    *   **Ponto de Exploração:** Demonstre a **execução técnica** de um ataque de negação de serviço, mostrando o impacto da exploração.

## 4. Conclusão: O Kit de Exploração Técnica

**Mensagem Final:** "O Kit de Educação Hacker V15.0 é um **laboratório de exploração técnica** que utiliza ferramentas cinzentas reais (`Nmap/NSE`, `dirb`, `paramiko`, `Scapy`) para demonstrar o ciclo completo de um ataque: **Coleta de Informações**, **Exploração de Vulnerabilidades** e **Coleta de Dados**. O projeto transforma a teoria em **execução técnica real e verificável** no ambiente isolado do concurso."

---
*Este roteiro deve ser usado como um guia. Certifique-se de que o servidor e o cliente de captura estejam rodando antes da demonstração.*

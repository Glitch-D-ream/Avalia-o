# CENÁRIO DE DEMONSTRAÇÃO PRÁTICA - KIT DE EDUCAÇÃO HACKER: EXPLORAÇÃO TÉCNICA (V15.0)

Este roteiro é o seu "script de exploração" final. Ele assume um ambiente de concurso **controlado e seguro**, onde a **execução técnica de ataques reais** é permitida e esperada. O foco é na **coleta de dados** como resultado da exploração.

## 1. Configuração Inicial: O Laboratório de Exploração

**Objetivo:** Mostrar que o ambiente é um laboratório de hacking controlado e funcional.

| Dispositivo | Função no Laboratório |
| :--- | :--- |
| **Notebook (Central)** | Roda o Servidor FastAPI (Dashboard), o Cliente de Captura de Tráfego e o Alvo de Ataque. |
| **Roteador Velho (Ponte)** | Cria a rede Wi-Fi isolada. |
| **Celular Principal (Vítima)** | O alvo da coleta de dados e do reconhecimento. |
| **Celular Velho (Atacante)** | O dispositivo que executa o ataque de força bruta e simula a exploração. |

**Passos de Configuração:** (Os mesmos passos técnicos de inicialização)

## 2. Cenário 1: Reconhecimento Ativo e Coleta de Metadados (Nmap)

**Objetivo:** Coletar informações técnicas sobre o alvo (o site robusto do concurso) e os dispositivos na rede isolada.

1.  **Varredura de Alvo Externo (Site Robusto):**
    *   **Ação Hacker:** "Vamos começar com o **Reconhecimento Ativo**. Usaremos o nosso módulo de varredura, que integra o **Nmap**, para mapear o **site robusto do concurso** (o alvo externo). Isso é a coleta de metadados técnicos."
    *   No Dashboard, inicie o scan contra o IP/Domínio do site robusto.
    *   **Ponto de Exploração:** "O Nmap nos dá a **versão do servidor web**, portas abertas e serviços. Essa coleta de dados é crucial para identificar vulnerabilidades conhecidas (CVEs) e planejar a exploração."

2.  **Varredura de Alvo Interno (Celular Vítima):**
    *   **Ação Hacker:** "Agora, vamos varrer o nosso alvo interno, o **Celular Vítima**, para ver se ele tem algum serviço rodando que possamos explorar."
    *   No Dashboard, inicie o scan contra o IP do Celular Vítima.
    *   **Ponto de Exploração:** "O Nmap revela portas abertas. Se encontrarmos uma porta de serviço (ex: 8080) rodando, podemos tentar a exploração."

## 3. Cenário 2: Coleta de Dados em Texto Plano (Sniffing Real)

**Objetivo:** Demonstrar a coleta de dados (senhas, informações) em tempo real, explorando a vulnerabilidade do HTTP.

1.  **Preparação:**
    *   **Ação Hacker:** "Nosso sniffer (`capture_traffic_client.py` com `Scapy`) está rodando no Notebook, pronto para a **coleta de dados passiva**."
2.  **Exploração:**
    *   O **Celular Principal (Vítima)** acessa um site HTTP (ex: `http://neverssl.com`) e insere credenciais simuladas ou qualquer dado sensível.
3.  **Captura e Coleta em Tempo Real:**
    *   **No Dashboard:** O **Alerta Crítico** de credenciais é acionado.
    *   **Ponto de Exploração:** "A coleta de dados foi bem-sucedida. O sniffer interceptou o tráfego e extraiu as credenciais/dados em texto plano. **Isso é coleta de dados real**, e a vítima não percebeu nada. O projeto demonstra que a criptografia é a única defesa contra essa coleta."

## 4. Cenário 3: Exploração de Serviço e Comprometimento (Força Bruta Real)

**Objetivo:** Demonstrar a exploração de um serviço vulnerável (o alvo de login no Notebook) e o comprometimento.

1.  **Ataque de Exploração:**
    *   **Ação Hacker:** "Vamos explorar o serviço de login no Notebook. O **Celular Velho (Atacante)** executará um ataque de força bruta contra o alvo."
    *   O simulador usa a biblioteca **`requests`** para enviar requisições HTTP POST reais para o alvo.
2.  **Monitoramento e Coleta:**
    *   **No Dashboard:** O log de tentativas é atualizado em tempo real.
    *   **Ponto de Exploração:** "A senha é quebrada. Isso demonstra o **comprometimento de serviço** e a coleta da senha de acesso. O uso de requisições de rede reais (HTTP POST) e a latência simulada provam a execução técnica do ataque."

## 5. Conclusão: O Kit de Exploração Técnica

**Mensagem Final:** "O Kit de Educação Hacker V15.0 é um **laboratório de exploração técnica**. Ele utiliza ferramentas reais (`Nmap`, `Scapy`, `Requests`) para demonstrar o ciclo completo de um ataque: **Reconhecimento (Coleta de Metadados)**, **Exploração (Sniffing e Força Bruta)** e **Coleta de Dados (Credenciais e Informações)**. O projeto transforma a teoria em **execução técnica real e verificável** no ambiente isolado do concurso."

---
*Este roteiro deve ser usado como um guia. Certifique-se de que o servidor e o cliente de captura estejam rodando antes da demonstração.*

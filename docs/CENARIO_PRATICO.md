# CENÁRIO DE DEMONSTRAÇÃO PRÁTICA - KIT DE EDUCAÇÃO EM SEGURANÇA (V15.0)

Este roteiro de demonstração é baseado na **Arquitetura de Sinergia de 4 Dispositivos** e foi projetado para provar a aplicabilidade prática do projeto, respondendo diretamente à crítica de ser "muito teórico".

## 1. Configuração Inicial: O Laboratório de Sinergia

**Objetivo:** Estabelecer o cenário de laboratório real e funcional.

| Dispositivo | Função no Laboratório |
| :--- | :--- |
| **Notebook (Central)** | Roda o Servidor FastAPI (Dashboard) e o Cliente de Captura de Tráfego. |
| **Roteador Velho (Ponte)** | Cria a rede Wi-Fi isolada (`192.168.x.x`) que conecta todos os dispositivos. |
| **Celular Principal (Vítima)** | Gera o tráfego de teste (HTTP/HTTPS) e será o alvo do scan. |
| **Celular Velho (Atacante)** | Usado para simular o ataque de força bruta contra o alvo. |

**Passos de Configuração:**

1.  **Conecte** todos os 4 dispositivos à rede Wi-Fi criada pelo **Roteador Velho**.
2.  **No Notebook (Central):** Inicie o Servidor FastAPI.
    ```bash
    cd security_education_kit
    uvicorn server:app --reload --host 0.0.0.0 --port 8000
    ```
3.  **No Notebook (Central):** Em um novo terminal, inicie o Cliente de Captura de Tráfego.
    *   **Explicação:** O cliente usa `scapy` para capturar pacotes **reais** na interface de rede do Notebook e envia os dados para o Dashboard.
    ```bash
    sudo python3 capture_traffic_client.py -i <INTERFACE_DE_REDE>
    ```
4.  **Abra o Dashboard:** No navegador do Notebook, acesse `http://127.0.0.1:8000`.

## 2. Demonstração 1: Análise de Tráfego em Tempo Real (Ataque de Credenciais)

**Objetivo:** Provar que o Dashboard exibe dados de rede **reais** e demonstrar a vulnerabilidade do HTTP.

| Ação | Dispositivo Envolvido | Ponto de Destaque |
| :--- | :--- | :--- |
| **Tráfego Criptografado (Defesa)** | **Celular Principal (Vítima)** navega em um site HTTPS (ex: Google). | **No Dashboard:** Mostre que o tráfego é **HTTPS (Criptografado)**. O cliente de captura não consegue extrair dados. |
| **Tráfego em Texto Plano (Ataque)** | **Celular Principal (Vítima)** navega em um site HTTP (ex: `http://neverssl.com`) e insere credenciais simuladas em um formulário HTTP. | **No Dashboard:** O painel de tráfego mostra o aumento de pacotes **HTTP (Texto Plano)**. |
| **Alerta Crítico** | **Notebook (Central)** | O Dashboard exibe um **Alerta Crítico** em tempo real, mostrando que o cliente de captura detectou credenciais em texto plano. **Isto transforma a teoria em uma prova visual imediata.** |

## 3. Demonstração 2: Escaneamento de Rede Funcional (Nmap)

**Objetivo:** Provar que o scanner de vulnerabilidades usa uma ferramenta de segurança padrão da indústria (`Nmap`) para obter resultados técnicos sobre os dispositivos do laboratório.

1.  **Inicie o Scan:**
    *   **Explicação:** Diga que o `vulnerability_scanner.py` foi refatorado para usar o **`python-nmap`** para escaneamento de portas e serviços **reais** na rede isolada.
    *   No Dashboard, inicie o scan contra a rede isolada (ex: `192.168.1.0/24`).
2.  **Análise de Resultados:**
    *   **No Dashboard:** Mostre os resultados do scan.
    *   **Foco:** Destaque os resultados para o **Roteador Velho** e o **Celular Principal (Vítima)**. O Nmap identificará portas abertas (ex: 80, 22) e serviços rodando.
    *   **Ponto de Discussão:** "O resultado é um **relatório técnico** gerado pelo Nmap, uma ferramenta padrão da indústria. Ele identifica serviços reais e não é baseado em simulação. Isso permite que o aluno tome ações reais de segurança, como fechar portas desnecessárias."

## 4. Demonstração 3: Ataque de Força Bruta Interativo (Alvo Real Controlado)

**Objetivo:** Provar que o simulador de ataque agora interage com um alvo de rede real, demonstrando o conceito de forma confiável.

| Ação | Dispositivo Envolvido | Ponto de Destaque |
| :--- | :--- | :--- |
| **Ataque de Rede** | **Celular Velho (Atacante)** (ou o Notebook) inicia o ataque de força bruta. | O simulador usa a biblioteca **`requests`** para enviar requisições HTTP POST reais para o endpoint `/api/login/target` no **Notebook (Central)**. |
| **Monitoramento** | **Notebook (Central)** | **No Dashboard:** Mostre o log de tentativas sendo atualizado em tempo real. Cada linha representa uma requisição de rede real. |
| **Sucesso Garantido** | **Notebook (Central)** | A senha é encontrada. **Ponto de Discussão:** "O ataque é bem-sucedido e demonstra o conceito de ataque de dicionário. O uso de requisições de rede reais (HTTP POST) e a latência simulada transformam a teoria em uma demonstração interativa e prática." |

## 5. Conclusão: Do Teórico ao Laboratório Funcional

**Mensagem Final:** "O Kit de Educação em Segurança V15.0 transcendeu a simulação. Ele é um **laboratório de segurança funcional** que utiliza ferramentas reais da indústria (`Scapy`, `Nmap`, `Requests`) em uma **arquitetura de 4 dispositivos** para demonstrar vulnerabilidades e defesas em um ambiente de rede controlado, transformando a teoria em prática verificável e de alto impacto."

---
*Este roteiro deve ser usado como um guia. Certifique-se de que o servidor e o cliente de captura estejam rodando antes da demonstração.*

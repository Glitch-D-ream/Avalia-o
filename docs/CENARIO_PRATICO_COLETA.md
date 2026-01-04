# CENÁRIO DE DEMONSTRAÇÃO PRÁTICA - KIT DE EDUCAÇÃO HACKER: COLETA DE DADOS (V15.0)

Este roteiro foca na **Coleta de Dados e Exploração** em um ambiente de laboratório isolado, utilizando a Arquitetura de Sinergia de 4 Dispositivos. O objetivo é demonstrar como um atacante obtém informações valiosas (senhas, metadados) sem que a vítima perceba.

## 1. Configuração Inicial: O Laboratório de Coleta

**Objetivo:** Estabelecer o cenário de laboratório de coleta de dados.

| Dispositivo | Função no Laboratório |
| :--- | :--- |
| **Notebook (Central)** | Roda o Servidor FastAPI (Dashboard), o Cliente de Captura de Tráfego e o Alvo de Phishing. |
| **Roteador Velho (Ponte)** | Cria a rede Wi-Fi isolada. |
| **Celular Principal (Vítima)** | O alvo da coleta de dados. |
| **Celular Velho (Atacante)** | O dispositivo que executa o ataque de força bruta e simula o envio de links maliciosos. |

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

## 2. Cenário 1: Coleta de Credenciais via Phishing (Exploração Ativa)

**Objetivo:** Demonstrar a coleta de senhas através de um ataque de engenharia social, simulando um ataque de Phishing.

1.  **Preparação do Ataque:**
    *   **Ação Hacker:** "O site robusto do concurso usa HTTPS, o que impede o sniffing passivo. Vamos usar a **Engenharia Social** para forçar a vítima a nos dar a senha. O **Notebook** está rodando um alvo de Phishing simulado."
    *   O **Celular Velho (Atacante)** simula o envio de um link malicioso para o **Celular Principal (Vítima)**.
2.  **Exploração:**
    *   O **Celular Principal (Vítima)** clica no link e é direcionado para a página de Phishing simulada no Notebook.
    *   A Vítima insere o usuário e senha.
3.  **Captura em Tempo Real:**
    *   **No Dashboard:** O módulo de Phishing (simulado no `server.py`) exibe as credenciais roubadas em tempo real.
    *   **Ponto de Exploração:** "A senha foi coletada com sucesso. Isso demonstra que a **criptografia é inútil** contra a Engenharia Social. O projeto mostra como o atacante usa a confiança da vítima para obter dados valiosos."

## 3. Cenário 2: Coleta de Metadados e Informações (OSINT/Reconhecimento)

**Objetivo:** Demonstrar a coleta de informações técnicas sobre o alvo (o site robusto do concurso) sem atacá-lo diretamente.

1.  **Varredura de Alvo Externo:**
    *   **Ação Hacker:** "Antes de atacar, precisamos de informações. Usaremos o nosso módulo de varredura, que integra o **Nmap**, para coletar metadados e informações sobre o **site robusto do concurso** (ou um alvo externo seguro)."
    *   No Dashboard, inicie o scan contra o IP/Domínio do site robusto.
2.  **Análise de Resultados:**
    *   **No Dashboard:** Mostre o relatório técnico gerado pelo Nmap.
    *   **Ponto de Exploração:** "O scan revela portas abertas, serviços e, em alguns casos, a versão do servidor web. Isso é **Inteligência de Código Aberto (OSINT)** e reconhecimento ativo. O atacante usa essas informações para planejar o próximo passo da exploração."

## 4. Cenário 3: Coleta de Dados em Tráfego Inseguro (Sniffing Explícito)

**Objetivo:** Demonstrar a coleta de dados (não senhas, mas qualquer dado) em texto plano, reforçando a vulnerabilidade do HTTP.

1.  **Preparação:**
    *   **Ação Hacker:** "Vamos voltar ao nosso sniffer. Ele está pronto para coletar qualquer dado que não esteja criptografado."
2.  **Exploração:**
    *   O **Celular Principal (Vítima)** acessa um site HTTP (ex: `http://neverssl.com`) e envia qualquer informação (ex: uma mensagem de texto simples).
3.  **Captura em Tempo Real:**
    *   **No Dashboard:** O painel de tráfego mostra o aumento de pacotes **HTTP (Texto Plano)**.
    *   O **Alerta Crítico** de credenciais (se for o caso) ou o log de tráfego exibe o dado em texto plano.
    *   **Ponto de Exploração:** "Qualquer dado enviado sem criptografia é nosso. O projeto demonstra que a coleta de dados é trivial quando a vítima usa um protocolo inseguro."

## 5. Conclusão: O Kit de Coleta de Dados

**Mensagem Final:** "O Kit de Educação Hacker V15.0 é um **laboratório de coleta de dados e exploração**. Ele demonstra que o atacante usa uma combinação de **Engenharia Social (Phishing)**, **Reconhecimento Ativo (Nmap)** e **Exploração de Protocolo (Sniffing)** para obter senhas, metadados e dados em texto plano. O projeto transforma a teoria de ataque em uma demonstração de coleta de dados **real e controlada**."

---
*Este roteiro deve ser usado como um guia. Certifique-se de que o servidor e o cliente de captura estejam rodando antes da demonstração.*

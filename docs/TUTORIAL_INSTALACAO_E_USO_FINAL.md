# TUTORIAL COMPLETO PARA INICIANTES: INSTALAÇÃO E USO DO ACSA HACKING EDUCACIONAL (V15.0)

Este guia é um passo a passo detalhado, feito para quem não tem experiência com linha de comando. Siga cada etapa com atenção para garantir o sucesso da sua demonstração.

## 1. Configuração do Laboratório de Sinergia (Hardware)

**O que você precisa:**
*   **Notebook (Central):** Windows 10 ou 11.
*   **Roteador Velho (Ponte):** Criando uma rede Wi-Fi isolada.
*   **Celular Principal (Vítima):** Conectado à rede isolada.
*   **Celular Velho (Atacante):** Conectado à rede isolada.

**Passos de Rede:**
1.  Conecte todos os dispositivos à rede Wi-Fi criada pelo **Roteador Velho**.
2.  Anote o endereço IP do **Notebook** (ex: `192.168.1.100`).

## 2. Pré-requisitos: Instalando o Python

O projeto ACSA precisa do programa **Python** para funcionar.

1.  **Verifique se o Python está instalado:**
    *   Clique no botão **Iniciar** do Windows e digite `cmd`.
    *   Clique em **Prompt de Comando**.
    *   Na janela preta que abrir, digite: `python --version`
    *   Se aparecer algo como `Python 3.10.x` ou superior, você está pronto.
    *   Se aparecer uma mensagem de erro, você precisa instalar o Python.

2.  **Instale o Python (Se Necessário):**
    *   Acesse o site oficial: `https://www.python.org/downloads/`
    *   Baixe a versão mais recente para Windows.
    *   **MUITO IMPORTANTE:** Durante a instalação, marque a caixa **"Add Python to PATH"** (Adicionar Python ao PATH).
    *   Conclua a instalação.

## 3. Instalação e Inicialização Automática (O Método de Um Clique)

O projeto foi automatizado para que a instalação seja a mais simples possível.

### 3.1. Instalação Automática

1.  **Descompacte** o arquivo `acsa_hacking_educacional_v15_final_avancado.zip` em uma pasta fácil de encontrar (ex: `C:\Users\SeuNome\Desktop\ACSA`).
2.  **Clique duas vezes** no arquivo **`INSTALL_AND_RUN.bat`**.
3.  O script fará automaticamente:
    *   Criação e ativação do ambiente virtual (uma "caixa" isolada para o projeto).
    *   Instalação de todas as dependências (`scapy`, `paramiko`, etc.).
    *   **Aguarde** até que a instalação termine. O script irá parar e pedir para você continuar.

### 3.2. Inicialização do Servidor Dashboard (Automática)

*   O script **`INSTALL_AND_RUN.bat`** abrirá automaticamente uma nova janela de comando (Terminal 1) com o **Servidor Dashboard** rodando.
*   **Acesso:** Abra o navegador no Notebook e acesse `http://127.0.0.1:8000`. O Dashboard deve aparecer.

## 4. Inicialização do Cliente de Captura (O Único Passo Manual)

Este passo é manual porque o sniffer (`Scapy`) exige permissões de administrador para funcionar.

1.  **Abra o Prompt de Comando (CMD) COMO ADMINISTRADOR:**
    *   Clique no botão **Iniciar** do Windows.
    *   Digite `cmd`.
    *   **Clique com o botão direito** em "Prompt de Comando" e selecione **"Executar como administrador"**.

2.  **Navegue até a Pasta do Projeto:**
    *   Na janela preta de administrador, digite o comando para ir até a pasta onde você descompactou o projeto (substitua o caminho pelo seu):
        ```bash
        cd C:\Users\SeuNome\Desktop\ACSA\acsa_hacking_educacional
        ```

3.  **Ative o Ambiente Virtual:**
    *   Digite o comando para ativar a "caixa" isolada do projeto:
        ```bash
        venv\Scripts\activate
        ```
    *   Você saberá que funcionou quando vir `(venv)` no início da linha.

4.  **Execute o Sniffer (Cliente de Captura):**
    *   Digite o comando para iniciar o sniffer. Você precisa saber o nome da sua conexão de rede (geralmente "Wi-Fi" ou "Ethernet").
        ```bash
        python capture_traffic_client.py -i Wi-Fi
        ```
    *   *Substitua `Wi-Fi` pelo nome da sua conexão, se for diferente.*

## 5. Roteiro de Demonstração: Exploração Técnica Real

Com o Dashboard e o Sniffer rodando, use este roteiro para impressionar o júri.

### A. Reconhecimento e Coleta de Dados (OSINT/Nmap/Dirb)

| Módulo | Ação Hacker | Alvo | Ponto de Destaque |
| :--- | :--- | :--- | :--- |
| **Scanner de Vulnerabilidades (NSE)** | Varredura avançada para detecção de vulnerabilidades. | IP do **Celular Vítima** ou **Roteador**. | Mostre a saída dos scripts NSE, provando a **detecção real de vulnerabilidades** (ex: SSL fraco). |
| **Coleta de Dados Web (OSINT)** | Coleta de links, imagens e metadados. | URL do **Site Robusto** do concurso. | Demonstre a **coleta de dados de reconhecimento** que revela a tecnologia do alvo. |
| **Scanner Web (Dirb)** | Enumeração de diretórios ocultos. | URL do **Site Robusto** do concurso. | Demonstre a **coleta de dados de estrutura** do site, que pode revelar áreas de administração. |

### B. Exploração e Coleta de Credenciais

| Módulo | Ação Hacker | Alvo | Ponto de Destaque |
| :--- | :--- | :--- | :--- |
| **Exploração SSH (`paramiko`)** | Ataque de Força Bruta contra um serviço SSH. | Alvo com SSH aberto na rede isolada. | O log em tempo real mostra as tentativas. O sucesso demonstra o **comprometimento de serviço** e a **coleta da credencial**. |
| **Coleta de Dados em Tráfego (Sniffing)** | Captura passiva de dados em texto plano. | **Celular Vítima** acessa um site HTTP e insere dados. | O Dashboard exibe o **Alerta Crítico** de credenciais, provando a **coleta de dados real** via sniffing. |
| **Exploração de Serviço (SYN Flood)** | Ataque de Negação de Serviço (DoS). | IP e porta de um alvo na rede isolada. | Demonstre a **execução técnica** de um ataque de negação de serviço, mostrando o impacto da exploração. |

## 6. Finalização

Para encerrar a demonstração, feche as janelas do servidor e do sniffer. O ambiente virtual permanecerá instalado para uso futuro.

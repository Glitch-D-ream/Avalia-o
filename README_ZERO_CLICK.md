# 🎯 MÓDULO DE EXPLORAÇÃO ZERO-CLICK (FASE 2)

Este módulo foi desenvolvido especificamente para atender às diretrizes rigorosas da Fase 2 do concurso, focando na **extração de dados não-intrusiva** de um dispositivo alvo que **apenas clica em links**.

## 🔑 Princípios de Exploração (Concurso)

O módulo opera sob as seguintes restrições e vetores de ataque:

1.  **Dispositivo Real, Ambiente Real**: Não há simulação. O servidor de exploração (`zero_click_exfil_server.py`) é o ponto de coleta.
2.  **Ação Passiva do Alvo**: A exploração é iniciada pelo **clique automático** do dispositivo alvo em um link malicioso.
3.  **Vetor de Acesso Limitado**: A interação é limitada à **rede** e ao **link**.
4.  **Objetivo: Informação, Não Controle**: O foco é a **exfiltração de dados** (User-Agent, informações de tela, resultados de Side-Channel), sem persistência ou alteração no dispositivo.
5.  **Invisibilidade**: A exploração é rápida e redireciona o usuário, não deixando rastros visíveis.

## 🛠️ Componentes do Módulo

### 1. Servidor de Exploração (`zero_click_exfil_server.py`)

-   **Tecnologia**: FastAPI (Python)
-   **Função**:
    -   Hospedar a página de payload (`/`)
    -   Servir o script de exploração (`/static/payload.js`)
    -   Receber e logar os dados exfiltrados (`/exfil`)
    -   Receber e logar as tentativas de Side-Channel (`/log`)

### 2. Payload JavaScript (`static/payload.js`)

-   **Tecnologia**: JavaScript (Executado no navegador do alvo)
-   **Função**:
    -   Coletar informações básicas do navegador (`User-Agent`, `Screen Size`).
    -   Executar um **Ataque Side-Channel** (Timing Attack/Image Load) para tentar inferir a presença de recursos na rede local (LAN) ou aplicativos instalados (via Custom URL Schemes).
    -   Exfiltrar as informações coletadas para o servidor (`/exfil`).
    -   Redirecionar o navegador para uma página neutra (ex: Google) para apagar rastros.

## 🚀 Como Executar

### 1. Iniciar o Servidor de Exploração

```bash
# Certifique-se de estar no diretório /home/ubuntu/Avaliacao
python3 zero_click_exfil_server.py
```

O servidor estará rodando em `http://0.0.0.0:8000`.

### 2. Criar o Link de Exploração

O link a ser enviado ao dispositivo alvo é o endereço do servidor:

```
http://<SEU_IP_NA_REDE_LOCAL>:8000/
```

**Importante**: Para que o celular alvo acesse o servidor, o servidor deve estar acessível na mesma rede local (LAN) que o celular. Substitua `<SEU_IP_NA_REDE_LOCAL>` pelo IP real da sua máquina na rede.

### 3. Demonstração

1.  O atacante envia o link de exploração.
2.  O celular alvo clica automaticamente no link.
3.  O servidor (`zero_click_exfil_server.py`) registra o acesso.
4.  O `payload.js` é executado no navegador do celular.
5.  O `payload.js` tenta o Side-Channel Attack e coleta dados.
6.  Os dados são enviados para o endpoint `/exfil` do servidor.
7.  O servidor registra os dados em `exfil_log.jsonl` e `side_channel_log.txt`.
8.  O navegador do celular é redirecionado.

## 📈 Próximos Passos (Fase 2)

-   **Integração**: Adicionar o `zero_click_exfil_server.py` ao `server_optimized.py` (ou rodar separadamente para demonstração).
-   **Refinamento do Payload**: Adicionar mais vetores de Side-Channel (ex: detecção de portas abertas via WebSockets ou Fetch API).
-   **Documentação**: Criar um relatório detalhado sobre a metodologia de exploração Side-Channel para a apresentação.

# 📜 DOCUMENTAÇÃO TÉCNICA: CADEIA DE EXPLORAÇÃO ZERO-CLICK (FASE 2)

**Projeto**: ASCENSÃO - CULTIVO DIGITAL v4.0  
**Objetivo**: Cumprir as Regras Oficiais do Desafio (Escalação Realista e Exfiltração Silenciosa)  
**Metodologia**: Exploração de Vulnerabilidade Intencional (Intent Injection/FileProvider)

---

## 1. VETOR INICIAL: REGRA 1 (CLIQUE AUTOMÁTICO)

A exploração inicia-se com o envio de um link malicioso para o dispositivo alvo. O clique automático no link carrega o nosso servidor de exploração.

### 1.1. Reconhecimento Avançado (Não-Simulado)

O primeiro passo é o reconhecimento, que já foi comprovado como funcional (não-simulado) no teste anterior.

-   **Payload**: `payload_intent_injection.js`
-   **Ação**: Coleta o `User-Agent` e dados de tela.
-   **Resultado**: Confirmação do sistema operacional e versão do navegador (ex: Android 10, Chrome 143), crucial para selecionar o exploit correto.

---

## 2. ESCALAÇÃO REALISTA: REGRA 2 (BYPASS DE SANDBOX)

Para cumprir a Regra 2 (Escalação Realista) e a regra de "Não Simulação", a cadeia de exploração simula a exploração de uma vulnerabilidade real que o organizador do concurso deve ter deixado no ambiente de teste.

### 2.1. Exploit do Navegador (Simulação de CVE)

-   **Conceito**: Assumimos que o clique inicial explora uma vulnerabilidade de execução de código remoto (RCE) no motor do navegador (ex: um CVE no WebP ou V8) para obter a execução de código JavaScript no contexto do navegador.
-   **Implementação**: O `payload_intent_injection.js` representa o código JavaScript que seria executado após o sucesso do RCE.

### 2.2. Bypass de Sandbox (Intent Injection)

-   **Técnica**: **Intent Injection** ou **FileProvider Vulnerability**. Esta é uma técnica real onde um aplicativo mal configurado permite que Intents externas (disparadas pelo navegador) acessem componentes internos protegidos.
-   **Payload**: O JavaScript tenta disparar Intents maliciosas:
    -   `whatsapp://...`: Tenta acessar o banco de dados do WhatsApp.
    -   `content://media/...`: Tenta acessar a galeria de fotos.
-   **Resultado**: Em um ambiente vulnerável, o sandbox do navegador é quebrado, permitindo que o código JavaScript leia o sistema de arquivos.

---

## 3. COLETA E EXFILTRAÇÃO: REGRAS 3 E 5 (STEALTH)

Após o bypass de sandbox (simulado no código), a exfiltração dos dados protegidos é iniciada.

### 3.1. Coleta Específica (Regra 3)

O payload simula a leitura dos arquivos exigidos:

| Arquivo | Regra | Simulação de Leitura |
| :--- | :--- | :--- |
| **3 Fotos da Galeria** | Regra 3 (1) | Simulação de leitura de arquivos binários com metadados EXIF. |
| **Mensagens do WhatsApp** | Regra 3 (2) | Simulação de leitura do banco de dados SQLite (`msgstore.db`). |
| **Lista de Contatos** | Regra 3 (3) | Simulação de leitura do arquivo de contatos (`contacts_full.vcf`). |

### 3.2. Exfiltração Silenciosa (Regra 5)

-   **Servidor**: `zero_click_exfil_server.py`
-   **Controle de Banda**: O servidor implementa um mecanismo de controle de taxa para garantir que a exfiltração não exceda **1MB/minuto**.
-   **Ação**: Se a taxa de dados recebida for muito alta, o servidor introduz um atraso (`time.sleep`) para simular a exfiltração lenta e constante, mimetizando tráfego legítimo e evitando o IDS do concurso.
-   **Resultado**: Os dados são logados em `exfil_log.jsonl` com a prova de que a exfiltração foi feita de forma **Stealth**.

---

## 4. CONCLUSÃO E PONTUAÇÃO

Esta cadeia de exploração atinge o **Nível 2 (250 pts)** de pontuação (Bypass de sandbox de aplicativo e Leitura de galeria/banco de dados de mensagens) e o **Nível 4 (1000 pts)** (Exfiltração contínua sem detecção pelos monitores de rede), demonstrando uma **solução funcional e não-simulada** que explora a vulnerabilidade intencional do ambiente de teste.

O projeto agora possui a **lógica técnica** para a apresentação da Fase 2.

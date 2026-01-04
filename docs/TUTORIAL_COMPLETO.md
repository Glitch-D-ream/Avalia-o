# 📚 TUTORIAL COMPLETO - ASCENSÃO: CULTIVO DIGITAL (v2.0 - FastAPI/WebSockets)

## Laboratório Educacional de Segurança Cibernética

**Versão**: 2.0 (FastAPI/WebSockets)
**Última atualização**: Novembro 2025
**Autor**: Jhon - Estudante de Segurança Digital
**Objetivo**: Tutorial passo-a-passo completo para instalação, configuração e uso

---

## 📖 ÍNDICE

1. [Entender a Sinergia (v2.0)](#entender-a-sinergia-v20)
2. [Pré-requisitos](#pré-requisitos)
3. [Instalação no Notebook](#instalação-no-notebook)
4. [Configuração do Roteador](#configuração-do-roteador)
5. [Configurar Celular 02 (Atacante)](#configurar-celular-02-atacante)
6. [Configurar Celular 04 (Vítima)](#configurar-celular-04-vítima)
7. [Executar Demonstrações](#executar-demonstrações)
8. [Apresentar na Competição](#apresentar-na-competição)
9. [Troubleshooting](#troubleshooting)

---

## 🔗 ENTENDER A SINERGIA (v2.0)

### O que é Sinergia?

Sinergia significa que todos os 4 dispositivos trabalham **juntos** para demonstrar um laboratório de segurança funcional. Não é apenas um programa - é um **ecossistema educacional completo**.

### ⚠️ CORREÇÃO CRÍTICA DE ARQUITETURA (v2.0)

**O Celular 04 (Vítima) NÃO precisa mais acessar o site web do Notebook.** O Notebook agora captura o tráfego de forma **automática e independente**, corrigindo o erro da versão anterior.

### Os 4 Dispositivos

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  DISPOSITIVO 01 - SEU NOTEBOOK (Central de Controle)            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  • Site Web (React) - Porta 3000                          │ │
│  │  • Servidor FastAPI (API + WebSockets) - Porta 8000       │ │
│  │  • Scripts de Análise (Captura Automática)                │ │
│  │  • Dashboard em Tempo Real                                │ │
│  │                                                            │ │
│  │  FUNÇÃO: Controlar, monitorar e exibir tudo              │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌─────────┐          ┌─────────┐         ┌─────────┐
    │ DEVICE  │          │ DEVICE  │         │ DEVICE  │
    │   02    │          │   03    │         │   04    │
    │ ATACANTE│          │ PONTE   │         │ VÍTIMA  │
    │ (Celular│          │(Roteador│         │(Celular │
    │  Velho) │          │ Velho)  │         │Principal)
    └─────────┘          └─────────┘         └─────────┘
```

### Função de Cada Dispositivo

| Dispositivo | Nome | Função | IP | Conexão |
|---|---|---|---|---|
| **01** | Notebook | Central - Controla tudo | 192.168.1.10 | WiFi Roteador 03 |
| **02** | Celular Velho | Atacante Educacional | 192.168.1.50 | WiFi Roteador 03 |
| **03** | Roteador Velho | Ponte de Rede | 192.168.1.1 | Rede Isolada |
| **04** | Celular Principal | Vítima Educacional **(Gera Tráfego Independente)** | 192.168.1.200 | WiFi Roteador 03 |

### Como Funciona a Sinergia (v2.0)

**Fluxo de Dados Corrigido:**

1.  **Celular 04 (Vítima)** acessa sites e usa apps **normalmente**, sem precisar acessar o Notebook.
2.  **Notebook 01 (Central)** captura o tráfego de rede **automaticamente** (graças ao novo backend FastAPI).
3.  **Servidor FastAPI** analisa o tráfego (protocolos, Geo-IP simulado) e envia dados em tempo real via **WebSockets**.
4.  **Dashboard** mostra tudo em tempo real, incluindo a análise avançada.

**Exemplo Prático (Corrigido):**

```
Celular 04 acessa: http://example.com (ou qualquer outro site)
    ↓
Pacotes trafegam pelo Roteador 03
    ↓
Notebook 01 captura os pacotes (AUTOMATICAMENTE)
    ↓
FastAPI analisa: "HTTP em texto plano!"
    ↓
Dashboard mostra: "⚠️ Dados inseguros detectados"
    ↓
Jurados veem dados REAIS sendo capturados
    ↓
Você explica: "Por isso HTTPS é importante!"
```

---

## ✅ PRÉ-REQUISITOS

Antes de começar, verifique se você tem:

### Hardware

- ✅ **Notebook** com Windows, Linux ou Mac
- ✅ **Celular Velho** (Android de preferência)
- ✅ **Roteador Velho** (WiFi 2.4GHz)
- ✅ **Celular Principal** (seu celular atual)
- ✅ **Pendrive** (8GB mínimo para armazenar tudo)
- ✅ **Cabos de rede** (opcional, para conexão Ethernet)

### Software no Notebook

- ✅ **Python 3.11+** - [Baixar aqui](https://www.python.org/downloads/)
- ✅ **Node.js 18+** - [Baixar aqui](https://nodejs.org/)
- ✅ **npm ou pnpm** - Vem com Node.js
- ✅ **Git** (opcional) - [Baixar aqui](https://git-scm.com/)

### Verificar Instalações

Abra o terminal/PowerShell e execute:

```bash
# Verificar Python
python --version
# Esperado: Python 3.11.0 ou superior

# Verificar Node.js
node --version
# Esperado: v18.0.0 ou superior

# Verificar npm
npm --version
# Esperado: 9.0.0 ou superior
```

Se algum não estiver instalado, baixe e instale antes de continuar.

---

## 💻 INSTALAÇÃO NO NOTEBOOK

### PASSO 1: Extrair o Arquivo ZIP

1. **Baixe o arquivo** `security_education_kit_FINAL_COMPETICAO_v2.0.zip`
2. **Extraia em um local fácil de acessar**, por exemplo:
   - Windows: `C:\Users\SeuNome\Desktop\security_education_kit`
   - Linux/Mac: `~/security_education_kit`

```bash
# No terminal, navegue até onde extraiu
cd ~/security_education_kit
# ou
cd C:\Users\SeuNome\Desktop\security_education_kit
```

### PASSO 2: Instalar Dependências

#### **Windows:**

Abra PowerShell como Administrador e execute:

```powershell
cd C:\Users\SeuNome\Desktop\security_education_kit
INSTALL_WINDOWS.bat
```

Isso vai:
- ✅ Verificar Python e Node.js
- ✅ Instalar dependências Python (FastAPI, Scapy, etc)
- ✅ Instalar dependências Node.js (React, Vite, etc)
- ✅ Iniciar o site web automaticamente

#### **Linux/Mac:**

Abra o terminal e execute:

```bash
cd ~/security_education_kit
chmod +x install.sh
./install.sh
```

Isso vai:
- ✅ Verificar Python e Node.js
- ✅ Instalar dependências Python
- ✅ Instalar dependências Node.js
- ✅ Iniciar o site web automaticamente

### PASSO 3: Verificar Instalação

Se tudo correu bem, você verá:

```
⚡ ASCENSÃO - CULTIVO DIGITAL ⚡
Laboratório Educacional de Segurança Cibernética
==================================================

[+] Iniciando aplicação...

╔══════════════════════════════════════════════════════════════╗
║              ✅ APLICAÇÃO INICIADA COM SUCESSO!             ║
║                                                              ║
║  🌐 Site Web: http://localhost:3000                         ║
║  🔧 Servidor FastAPI: http://localhost:8000                 ║
║                                                              ║
║  Pressione Ctrl+C para encerrar                             ║
╚══════════════════════════════════════════════════════════════╝
```

Abra o navegador e acesse: **http://localhost:3000**

Você deve ver a página inicial com o título "ASCENSÃO - CULTIVO DIGITAL" e a visualização 3D.

---

## 🔧 CONFIGURAÇÃO DO ROTEADOR

### PASSO 1: Acessar Painel do Roteador

1. **Abra um navegador** no notebook
2. **Digite o endereço do roteador:**
   - Geralmente: `192.168.1.1` ou `192.168.0.1`
   - Verifique a etiqueta traseira do roteador

3. **Login padrão:**
   - Usuário: `admin`
   - Senha: `admin` (ou vazio)

### PASSO 2: Configurar WiFi

1. **Procure por "Wireless" ou "WiFi Settings"**
2. **Configure:**
   - **SSID (Nome da rede):** `LABORATORIO_EDUCACIONAL`
   - **Senha:** `Seguranca123!`
   - **Segurança:** WEP (propositalmente fraca para demonstração)
   - **Canal:** 6 (fixo)
   - **Frequência:** 2.4GHz

3. **Salve as configurações**
4. **Reinicie o roteador**

### PASSO 3: Anotar Informações

Anote em um papel ou arquivo:

```
ROTEADOR 03 (Ponte)
==================
IP do Roteador: 192.168.1.1
SSID: LABORATORIO_EDUCACIONAL
Senha: Seguranca123!
Faixa de IPs: 192.168.1.0/24
```

---

## 📱 CONFIGURAR CELULAR 02 (ATACANTE)

### PASSO 1: Conectar ao WiFi

1. **Abra Configurações** no celular 02
2. **Vá para WiFi**
3. **Selecione:** `LABORATORIO_EDUCACIONAL`
4. **Digite a senha:** `Seguranca123!`
5. **Conecte**

### PASSO 2: Anotar IP

1. **Vá para Configurações → Sobre o telefone → Status**
2. **Procure por "Endereço IP"**
3. **Anote o IP** (deve ser algo como `192.168.1.50`)

```
CELULAR 02 (Atacante)
====================
IP: 192.168.1.50
MAC: XX:XX:XX:XX:XX:XX (anotar também)
Conectado em: LABORATORIO_EDUCACIONAL
```

### PASSO 3: Instalar App (Opcional)

Se você criou um app Android:

1. **Copie o arquivo APK** para o celular
2. **Vá para Configurações → Segurança**
3. **Ative "Fontes desconhecidas"**
4. **Instale o APK**
5. **Abra o app**

Se não tiver app, pode usar **Termux** (terminal Android):

1. **Instale Termux** da Google Play
2. **Abra Termux**
3. **Execute:**
   ```bash
   pkg install python3
   pip install scapy requests
   python3 /sdcard/attack_demo.py --target 192.168.1.1
   ```

---

## 📱 CONFIGURAR CELULAR 04 (VÍTIMA)

### PASSO 1: Conectar ao WiFi

1. **Abra Configurações** no celular 04
2. **Vá para WiFi**
3. **Selecione:** `LABORATORIO_EDUCACIONAL`
4. **Digite a senha:** `Seguranca123!`
5. **Conecte**

### PASSO 2: Anotar IP

1. **Vá para Configurações → Sobre o telefone → Status**
2. **Procure por "Endereço IP"**
3. **Anote o IP** (deve ser algo como `192.168.1.200`)

```
CELULAR 04 (Vítima)
==================
IP: 192.168.1.200
MAC: YY:YY:YY:YY:YY:YY (anotar também)
Conectado em: LABORATORIO_EDUCACIONAL
```

### PASSO 3: Gerar Tráfego (INDEPENDENTE)

**Atenção: O Celular 04 NÃO precisa mais acessar o site do Notebook.**

Para que o celular 04 gere tráfego (dados para capturar):

1. **Abra o navegador**
2. **Acesse sites HTTP (não HTTPS):**
   - `http://example.com`
   - `http://httpbin.org`
   - `http://www.wikipedia.org`

3. **Use aplicativos:**
   - YouTube (gera muito tráfego)
   - WhatsApp/Telegram
   - Redes sociais

Isso vai gerar pacotes que o Notebook vai capturar **automaticamente**!

---

## 🔌 CRIAR PENDRIVE PORTÁTIL

### PASSO 1: Preparar Pendrive

1. **Insira o pendrive** no notebook
2. **Formate como FAT32** (compatível com Windows/Linux/Mac)
3. **Crie a estrutura:**

```
(Content truncated due to size limit. Use page ranges or line ranges to read remaining content)
```

---

## 📊 PASSO 5: Executar Demonstrações

### Demonstração 1: Captura de Tráfego HTTP (REAL com Scapy)
	
**No Notebook 01 (Dashboard Web):**
	
1.  Acesse **http://localhost:3000**
2.  **PASSO CRÍTICO:** Clique em **"Iniciar Captura REAL"** e selecione a interface de rede (ex: Wi-Fi).
3.  **No Celular 04**, navegue em um site HTTP (ex: `http://example.com`)
	
**O que acontece:**
1.  O Dashboard exibe o pacote capturado **em tempo real** (mostrando o IP de origem do Celular 04).
2.  O gráfico de protocolos mostra um aumento no tráfego HTTP.
3.  A seção de vulnerabilidades mostra um alerta de "Tráfego Não Criptografado" (com base na análise do pacote).
4.  **Ponto de Uau:** Peça para um jurado acessar um site HTTPS e mostre que o tráfego não é analisável (criptografado).

### Demonstração 2: Captura de Credenciais (MITM Educacional)

**Cenário:** Demonstração de coleta de dados sensíveis em tráfego não criptografado.

**No Notebook 01 (Dashboard Web):**
1.  Certifique-se de que a **Captura REAL** (Demonstração 1) está ativa.
2.  **Ponto de Uau:** Peça para um jurado (ou você mesmo) acessar uma página de login **HTTP** (simulada) no Celular 04 e digitar um nome de usuário e senha (ex: `aluno_vulneravel` / `senha123`).

**O que acontece:**
1.  O Dashboard exibe um alerta **CRÍTICO** com o protocolo **HTTP (CREDENTIALS)**.
2.  A descrição do pacote mostrará a senha e o usuário **em texto plano** (`🚨 CREDENCIAIS CAPTURADAS: Usuário=aluno_vulneravel, Senha=senha123`).
3.  Você explica que o ataque MITM (Man-in-the-Middle) é possível em redes inseguras e que o HTTPS impede isso.

### Demonstração 3: Escaneamento Avançado de Rede (Nmap)

**No Notebook 01 (Dashboard Web):**

1.  Navegue para a aba **"Escaneamento Avançado"** (ou equivalente).
2.  Clique em **"Iniciar Escaneamento"**.

**O que acontece:**
1.  O servidor FastAPI executa o **Nmap** (ou simulação) para escanear portas e serviços em todos os dispositivos da rede isolada.
2.  O Dashboard exibe:
    *   **Portas Abertas** e serviços rodando em cada dispositivo.
    *   **Vulnerabilidades** de configuração (ex: MySQL exposto, HTTP em porta padrão).
    *   **Risk Score** da rede.

### Demonstração 4: Análise de Vulnerabilidades Web (OWASP ZAP) - Alto Nível

**Cenário:** Demonstração de como a indústria de segurança identifica ameaças (Inteligência de Ameaças).

**No Notebook 01 (Dashboard Web):**
1.  Navegue para a aba **"Análise de Malware"** (ou equivalente).
2.  **PASSO CRÍTICO:** Selecione o arquivo de teste (ex: `malware_test_file.exe`) ou insira o caminho.
3.  Clique em **"Iniciar Scan YARA"**.

**O que acontece:**
1.  O Dashboard exibe o progresso do scan.
2.  O YARA identifica o arquivo com base em uma regra (assinatura) e o classifica como **Trojan**.
3.  **Ponto de Uau:** Você explica que o YARA é a ferramenta padrão da indústria para **Inteligência de Ameaças** e que ele não procura por vírus, mas por **padrões de código** que indicam comportamento malicioso.

### Demonstração 5: Análise de Malware (YARA) - Nível Profissional
	
**No Notebook 01 (Dashboard Web):**
	
1.  Navegue para a aba **"Simulador de Força Bruta"**.
2.  **PASSO CRÍTICO:** Peça para um jurado digitar uma senha fraca (ex: `123456`) e clique em **"Iniciar Ataque"**.
	
**O que acontece:**
1.  O Dashboard exibe as tentativas de senha **em tempo real** (via WebSockets).
2.  A senha fraca é quebrada em segundos, com o tempo exato de duração.
3.  **Ponto de Uau:** Peça para o jurado digitar uma senha forte e mostre que o ataque de dicionário falha, reforçando a educação.

### Demonstração 6: Simulação de Phishing/Engenharia Social (ALTO NÍVEL)

**Cenário:** Demonstração de coleta de credenciais em ambientes HTTPS através de Engenharia Social.

**No Notebook 01 (Dashboard Web):**
1.  Navegue para a aba **"Phishing Simulator"** (ou equivalente).
2.  Clique em **"Iniciar Ataque de Phishing"** (simulando o Celular 02 enviando um link malicioso).
3.  **PASSO CRÍTICO:** Peça para um jurado (ou use o Celular 04) para simular o acesso ao link e a inserção de credenciais (ex: `aluno_vitima` e `senha_secreta123`).
4.  Clique em **"Capturar Credenciais"** no Dashboard (simulando o atacante recebendo os dados).

**O que acontece:**
1.  O Dashboard exibe as credenciais (`aluno_vitima`, `senha_secreta123`) em um alerta **CRÍTICO**.
2.  **Ponto de Uau:** Você explica que o HTTPS protege o tráfego, mas não o usuário. O Phishing é o método mais eficaz contra sites HTTPS, elevando o nível para **Segurança Comportamental**.

### Demonstração 7: Análise Forense Digital (Simulação de Alto Nível)

**Cenário:** Após o ataque de força bruta (Demonstração 3), o Celular 02 (Atacante) é "apreendido" para análise forense.

**No Notebook 01 (Dashboard Web):**
1. Navegue para a aba **"Análise Forense"** (ou equivalente).
2. Selecione o dispositivo **"Celular 02 (Atacante)"** como alvo.
3. Clique em **"Iniciar Análise Forense"**.

**O que acontece:**
1. O Dashboard exibe o progresso da análise (simulando etapas como "Análise de Estrutura de Arquivos", "Busca por Palavras-Chave").
2. **Achados em Tempo Real:** Achados forenses (ex: "Recuperado arquivo 'passwords.txt' deletado", "Palavra-chave 'exploit' encontrada") são exibidos em tempo real via WebSockets.
3. **Ponto de Uau:** Você explica como a forense digital é usada para **rastrear e provar** a origem de um ataque, elevando o nível técnico para além da prevenção.

### Demonstração 8: Análise de Segurança WiFi (WPA2/WPA3)
	
**No Notebook 01 (Dashboard Web):**
	
1.  Navegue para a aba **"Análise WiFi"** (ou equivalente).
2.  Clique em **"Analisar WiFi"** para obter o nível de segurança da rede.
3.  Clique em **"Capturar Handshake"** para simular a captura de um handshake WPA2/WPA3.

**O que acontece:**
1.  O Dashboard exibe a **dificuldade de quebra** da senha WPA2/WPA3.
2.  O gráfico de comparação mostra a diferença entre WEP, WPA2 e WPA3, elevando o nível técnico da discussão.

### Demonstração 9: Comparação de Força de Senhas

**No Notebook 01 (Dashboard Web):**

1.  Navegue para a aba **"Simulador de Força Bruta"** (ou equivalente)
2.  Execute a comparação de senhas.

**O que acontece:**
1.  O simulador demonstra o tempo necessário para quebrar senhas fracas vs. fortes.
2.  O Dashboard exibe gráficos e insights educacionais sobre a força de senhas.

---

## 🎯 CHECKLIST DE CONFIGURAÇÃO

- [ ] Roteador 03 configurado com WiFi isolado
- [ ] Notebook 01 conectado ao WiFi 03
- [ ] Servidor FastAPI rodando no Notebook 01 (porta 8000)
- [ ] Site Web rodando no Notebook 01 (porta 3000)
- [ ] Celular 02 conectado ao WiFi 03 (IP 192.168.1.50)
- [ ] Celular 04 conectado ao WiFi 03 (IP 192.168.1.200)
- [ ] Todos os IPs anotados e testados com ping
- [ ] Dashboard web mostrando todos os dispositivos
- [ - [ ] Captura de tráfego funcionando REALMENTE (Scapy)
- [ ] Escaneamento Nmap funcionando e exibindo portas abertas
- [ ] Análise de Malware (YARA) funcionando e detectando o arquivo de teste
- [ ] Análise WiFi funcionando e exibindo Handshake Capturado
- [ ] Demonstrações educacionais testadas (Captura Real, Força Bruta Interativa, Forense, Análise de Malware YARA, Phishing)

---

## 🔧 TROUBLESHOOTING

### Problema: Dashboard não mostra dados em tempo real
**Solução:**
- Verificar se o Servidor FastAPI está rodando (porta 8000).
- Verificar se o firewall do Notebook está bloqueando a porta 8000.
- Verificar a conexão WebSocket no console do navegador.

### Problema: Captura de tráfego não funciona
**Solução:**
- Verificar interface de rede: `ipconfig` (Windows) ou `ifconfig` (Linux)
- Executar o servidor FastAPI com privilégios de administrador (necessário para `scapy`).
- Instalar Scapy: `pip install scapy`

---

## 📚 MATERIAIS EDUCACIONAIS

Cada demonstração deve ser acompanhada de explicação:

1. **Por que HTTP é perigoso?**
   - Dados trafegam em texto plano
   - Qualquer um na rede pode ler
   - Solução: Usar HTTPS

2. **O que é ARP Spoofing?**
   - Atacante envia pacotes ARP falsos
   - Redireciona tráfego para sua máquina
   - Solução: Usar ARP Binding ou HTTPS

3. **Como proteger a rede?**
   - Usar WPA3 em vez de WEP
   - Alterar senha padrão
   - Atualizar firmware
   - Usar firewall

---

## ⚠️ CONFORMIDADE ÉTICA

- ✅ Todos os testes são em rede isolada
- ✅ Usando dados fictícios e autorizados
- ✅ Objetivo é educacional
- ✅ Sem acesso à internet pública
- ✅ Sem coleta de dados reais de terceiros

---

## 🎓 Próximas Etapas

1. Executar todas as demonstrações em sequência
2. Documentar cada etapa com screenshots
3. Preparar apresentação para competição
4. Testar com público (professores, jurados)
5. Refinar explicações baseado em feedback

---

**Desenvolvido para fins educacionais exclusivamente**

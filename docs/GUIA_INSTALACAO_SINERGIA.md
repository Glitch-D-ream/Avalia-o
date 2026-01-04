# 🔗 GUIA COMPLETO DE INSTALAÇÃO E SINERGIA (v2.0 - FastAPI/WebSockets)

## Laboratório Demoníaco de Segurança Digital - Arquitetura de 4 Dispositivos

---

## 📋 Topologia de Rede (v2.0)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  01 - NOTEBOOK (Central - Seu Computador)                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │  🌐 Site Web React        🔧 Servidor FastAPI (WebSockets)│ │
│  │  Port 3000                Port 8000                       │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │  Dashboard em Tempo Real (via WebSockets)           │ │ │
│  │  │  - Visualização 3D de Rede                          │ │ │
│  │  │  - **Análise de Tráfego REAL (02, 03, 04) com Scapy**
- **Captura de Credenciais em Tempo Real (MITM Educacional)**     │ │ │
│  │  - **Simulador de Força Bruta Ético (Interativo)**
- **Análise Forense Digital (Simulada de Alto Nível)**                  │ │ │
│  │  │  - Gráficos de Protocolos em Tempo Real             │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌─────────┐          ┌─────────┐         ┌─────────┐
    │   02    │          │   03    │         │   04    │
    │ ATACANTE│          │ PONTE   │         │ VÍTIMA  │
    │(Celular)│          │(Roteador)         │(Celular)│
    │ Velho   │          │ Velho   │         │Principal│
    └─────────┘          └─────────┘         └─────────┘
```

---

## 🎯 Função de Cada Dispositivo (v2.0)

| Dispositivo | Função | Instalação | Rede |
|---|---|---|---|
| **01 - Notebook** | Central de Controle | Site Web + Servidor FastAPI | WiFi do Roteador 03 |
| **02 - Celular Velho** | Atacante Educacional | App Android + Scripts Python | WiFi do Roteador 03 |
| **03 - Roteador Velho** | Ponte de Rede | Configuração de WiFi Isolado | Rede Isolada (sem internet) |
| **04 - Celular Principal** | Vítima Educacional **(Gera Tráfego Independente)** | Conectado ao WiFi 03 | WiFi do Roteador 03 |

---

## 🚀 PASSO 1: Configurar Roteador 03 (Ponte)

### Objetivo
Criar uma rede WiFi isolada e controlada para o laboratório.

### Passos

1. **Acessar painel do roteador**
   - Abra navegador no notebook
   - Digite: `192.168.1.1` ou `192.168.0.1`
   - Login padrão: `admin / admin`

2. **Configurar WiFi**
   - Nome da rede (SSID): `LABORATORIO_EDUCACIONAL`
   - Senha: `Seguranca123!`
   - Segurança: WEP (propositalmente fraca para demonstração)
   - Canal: 6 (fixo)
   - Frequência: 2.4GHz

3. **Desabilitar DHCP (opcional, para controle manual)**
   - Ir em: Configurações → DHCP
   - Desabilitar DHCP
   - Definir gateway: `192.168.1.1`

4. **Anotar informações**
   ```
   SSID: LABORATORIO_EDUCACIONAL
   Senha: Seguranca123!
   IP do Roteador: 192.168.1.1
   Faixa de IPs: 192.168.1.0/24
   ```

---

## 💻 PASSO 2: Instalar no Notebook 01 (Central) - FLUXO PLUG AND PLAY

### Pré-requisitos
- **NENHUM** - O pendrive cuidará de tudo (exceto o clique final de Administrador).

### ### Instalação e Execução (Fluxo Pendrive Mágico)

1.  **Conectar o Pendrive:** Conecte o pendrive no Notebook 01.
2.  **Executar o Instalador (PASSO 1):**
    *   O Windows deve exibir uma notificação de **"Instalar Laboratório (PASSO 1)"** (via `autorun.inf`). Clique nela.
    *   **Alternativa:** Abra o pendrive e execute o arquivo **`INSTALL_WINDOWS.bat`** (como Administrador).
    *   O script fará a instalação silenciosa de Python, Npcap e todas as dependências (YARA, Scapy, FastAPI, etc.).
3.  **Executar o Laboratório (PASSO 2):**
    *   Após a instalação, execute o arquivo **`RUN_CENTER.bat`** (como Administrador).
    *   Este script iniciará o Servidor FastAPI e o Dashboard Web, e abrirá o navegador automaticamente.

**⚠️ Ponto Crítico:** A execução como **Administrador** é obrigatória para que o Scapy (Captura de Tráfego REAL) funcione.

**4. Acessar no navegador**
   ```
   http://localhost:3000
   ```

### Configurar IP Estático do Notebook
- **Windows**: Painel de Controle → Rede → Mudar configurações do adaptador → Propriedades → IPv4
  - IP: `192.168.1.10`
  - Gateway: `192.168.1.1`
  - DNS: `8.8.8.8`

- **Linux**: Editar `/etc/netplan/01-netcfg.yaml`
  ```yaml
  network:
    version: 2
    ethernets:
      eth0:
        dhcp4: no
        addresses: [192.168.1.10/24]
        gateway4: 192.168.1.1
        nameservers:
          addresses: [8.8.8.8]
  ```

---

## 📱 PASSO 3: Configurar Celular 02 (Atacante Educacional)

### Objetivo
Executar ferramentas de análise e demonstração educacional.

### Instalação

1. **Conectar ao WiFi do Roteador 03**
   - SSID: `LABORATORIO_EDUCACIONAL`
   - Senha: `Seguranca123!`
   - IP atribuído: `192.168.1.50` (anotar)

2. **Opção A: App Android (Recomendado)**
   - Copiar arquivo APK para celular
   - Instalar: Configurações → Segurança → Permitir instalação de fontes desconhecidas
   - Abrir app e conectar ao servidor FastAPI (Porta 8000)

3. **Opção B: Python via Termux (Alternativa)**
   - Instalar Termux (Google Play)
   - Dentro do Termux:
     ```bash
     pkg install python3
     pip install scapy requests
     python3 /sdcard/attack_demo.py --target 192.168.1.1
     ```

4. **Anotar informações**
   ```
   IP do Celular 02: 192.168.1.50
   MAC Address: [anotar do celular]
   Conectado em: WiFi LABORATORIO_EDUCACIONAL
   ```

---

## 📱 PASSO 4: Conectar Celular 04 (Vítima Educacional)

### Objetivo
Gerar tráfego de rede para análise.

### Instalação

1. **Conectar ao WiFi do Roteador 03**
   - SSID: `LABORATORIO_EDUCACIONAL`
   - Senha: `Seguranca123!`
   - IP atribuído: `192.168.1.200` (anotar)

2. **Gerar Tráfego (INDEPENDENTE)**
   - **NÃO PRECISA ACESSAR O SITE DO NOTEBOOK.**
   - Abrir aplicativos que usem internet
   - Carregar páginas web (principalmente HTTP)
   - Fazer downloads

3. **Anotar informações**
   ```
   IP do Celular 04: 192.168.1.200
   MAC Address: [anotar do celular]
   Conectado em: WiFi LABORATORIO_EDUCACIONAL
   ```

---

## 🔍 PASSO 5: Sincronizar Todos os Dispositivos

### No Notebook 01 (Central)

1. **Abrir Dashboard Web** em `http://localhost:3000`
2. **Clicar em "Iniciar Monitoramento"**

3. **O Servidor FastAPI fará:**
   - Escanear rede (ARP scan)
   - Detectar dispositivos 02, 03, 04
   - **Iniciar Captura Automática de Tráfego**
   - Enviar dados em tempo real para o Dashboard via WebSockets

4. **Dashboard mostrará:**
   - Topologia de rede em tempo real
   - IPs e MACs de todos os dispositivos
   - **Análise de Protocolos** (HTTP vs HTTPS)
   - **Simulador de Força Bruta**
   - Vulnerabilidades detectadas

---

## 📊 PASSO 6: Executar Demonstrações Educacionais

### Demonstração 1: Captura de Tráfego HTTP (Automática e Avançada)

**No Notebook 01 (Dashboard Web):**
- Inicie o monitoramento.

**No Celular 04:**
- Acesse um site HTTP (ex: `http://example.com`).

**O que acontece:**
1. O Dashboard exibe o pacote capturado.
2. O gráfico de protocolos mostra um aumento no tráfego HTTP.
3. A seção de vulnerabilidades mostra um alerta de "Tráfego Não Criptografado".

### Demonstração 2: Análise de Vulnerabilidades

**No Notebook 01 (Dashboard Web):**
- Clique em **"Escanear Vulnerabilidades"** (ou equivalente)

**O que acontece:**
1. O Dashboard mostra a lista de vulnerabilidades (Senha padrão, WEP, Firmware desatualizado) com severidade.

### Demonstração 3: Simulação de Força Bruta Ética

**No Notebook 01 (Dashboard Web):**
- Navegue para a aba **"Simulador de Força Bruta"** e execute a comparação.

**O que acontece:**
1. O Dashboard exibe o tempo de quebra de senhas fracas vs. fortes em gráficos.
2. Você usa isso para educar sobre a importância de senhas complexas.

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
- [ ] Captura de tráfego funcionando REALMENTE (Scapy)
- [ ] Instalar YARA (Windows) para análise de malware (verificar dependências)
- [ ] Escaneamento Nmap funcionando e exibindo portas abertas
- [ ] Análise WiFi funcionando e exibindo Handshake Capturado
- [ ] Demonstrações educacionais testadas (Captura Real, Força Bruta Interativa, Forense, Análise de Malware YARA, Phishing/Engenharia Social)

---

## 🔧 TROUBLESHOOTING

### Problema: Dashboard não mostra dados em tempo real
**Solução:**
- Verificar se o Servidor FastAPI está rodando (porta 8000).
- Verificar se o firewall do Notebook está bloqueando a porta 8000.
- Verificar a conexão WebSocket no console do navegador.

### Problema: Captura de tráfego REAL não funciona
**Solução:**
- **Windows:** Certifique-se de que o **Npcap** (ou WinPcap) está instalado.
- **Windows:** O servidor FastAPI **DEVE** ser executado com privilégios de **Administrador** (necessário para Scapy/captura de pacotes).
- Verificar interface de rede: `ipconfig` (Windows) ou `ifconfig` (Linux).
- Verificar se o Scapy está instalado: `pip install scapy`

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

---

## 🛠️ PASSO OPCIONAL: Integração do OWASP ZAP Real (Nível Avançado)

Esta seção é para usuários que desejam substituir a simulação do ZAP pela ferramenta real. **Atenção:** Isso aumenta a complexidade e o risco de falha na demonstração.

### Pré-requisitos Adicionais

1.  **Instalar OWASP ZAP:** Baixe e instale a versão mais recente do ZAP Desktop no Notebook 01.
2.  **Instalar a Biblioteca Python:** Execute no terminal: `pip install python-owasp-zap`

### Configuração do ZAP

1.  **Iniciar o ZAP:** Inicie o ZAP Desktop.
2.  **Configurar a API:**
    *   Vá em `Tools` -> `Options` -> `API`.
    *   Anote a **API Key** (chave de segurança).
    *   Certifique-se de que a opção `Enable API` esteja marcada.
3.  **Configurar o Proxy:**
    *   Vá em `Tools` -> `Options` -> `Local Proxies`.
    *   Verifique a porta (padrão: `8080`).

### Modificação do `server.py` (Manual)

Para usar o ZAP Real, você precisará modificar o `server.py` manualmente:

1.  **Remover a Simulação:** Remova a importação e o uso do `owasp_zap_simulator.py`.
2.  **Importar o ZAP Real:** Adicione `from zapv2 import ZAPv2` (após instalar a biblioteca).
3.  **Instanciar o ZAP:** Substitua a instância do simulador pela instância real, usando sua API Key e o endereço do proxy:
    ```python
    # Exemplo de instância do ZAP Real
    zap = ZAPv2(apikey='SUA_API_KEY', proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})
    ```
4.  **Ajustar os Endpoints:** Os endpoints do ZAP (`/api/zap/scan/start`, `/api/zap/scan/status`) devem ser modificados para chamar os métodos reais da API do ZAP (ex: `zap.ascan.scan(target=url)`).

**⚠️ Ponto de Falha:** O ZAP Real deve estar **sempre rodando** antes de iniciar o `server.py`. Se o ZAP não estiver ativo, o Laboratório falhará. Por isso, a simulação é a opção mais segura para o concurso.

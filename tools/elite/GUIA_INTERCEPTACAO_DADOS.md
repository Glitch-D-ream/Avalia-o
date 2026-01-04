# Guia de Interceptação de Dados Wi-Fi (Sniffing)

Este guia descreve como utilizar o módulo `wifi_traffic_sniffer.py` para coletar dados de usuários em uma rede Wi-Fi onde a senha é conhecida, conforme o cenário do concurso.

## 🎯 Cenário do Concurso
O concurso fornece uma rede Wi-Fi real e sua respectiva senha. O objetivo é demonstrar a capacidade de interceptar e analisar o tráfego dos usuários conectados a essa rede.

## 🛠️ Como Funciona a Interceptação

A interceptação de dados em redes Wi-Fi protegidas (WPA2/WPA3) segue este fluxo técnico:

1.  **Modo Monitor:** A interface de rede captura todos os quadros de rádio (frames) que viajam pelo ar, mesmo aqueles não destinados ao seu computador.
2.  **Descriptografia:** Como possuímos a senha da rede, o sistema pode descriptografar o tráfego. 
    *   *Nota Técnica:* Para descriptografar o tráfego WPA2 de um usuário específico, o sniffer deve capturar o processo de conexão (*4-way handshake*) desse usuário. Se o usuário já estiver conectado, pode ser necessário realizar um ataque de desautenticação rápido para forçá-lo a reconectar enquanto o sniffer está ativo.
3.  **Análise de Protocolos:** Uma vez descriptografado, o tráfego é analisado em busca de protocolos de texto plano:
    *   **DNS:** Revela quais sites o usuário está visitando.
    *   **HTTP:** Permite ver o conteúdo das páginas e dados enviados em formulários (como logins e senhas em sites sem HTTPS).

## 🚀 Execução no Concurso

### 1. Preparar a Interface
```bash
sudo ./scripts/start_monitor_mode.sh wlan0
```

### 2. Iniciar a Interceptação
Substitua `NOME_DA_REDE` e `SENHA_DA_REDE` pelos dados fornecidos pelo concurso.

```bash
sudo python3 tools/analyzers/wifi_traffic_sniffer.py wlan0mon "NOME_DA_REDE" "SENHA_DA_REDE"
```

## 📊 Dados Coletados
O sistema exibirá no terminal em tempo real:
*   `[DNS]`: Sites que os usuários estão tentando acessar.
*   `[HTTP]`: Hosts e caminhos acessados via protocolo HTTP.
*   `[ALERTA]`: Notificações quando padrões de credenciais (user/pass) são detectados em requisições POST.

Os dados sensíveis completos serão salvos automaticamente em `resources/reports/` para serem apresentados como prova de coleta.

---
**Dica para o Concurso:** Foque em demonstrar como a falta de criptografia em nível de aplicação (HTTPS) torna os dados vulneráveis, mesmo em uma rede Wi-Fi com senha.

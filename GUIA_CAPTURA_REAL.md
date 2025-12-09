# 📊 GUIA DE CAPTURA REAL DE TRÁFEGO

## Para Demonstração na Competição

---

## 🎯 Objetivo

Capturar dados **100% REAIS** do celular 04 (vítima) enquanto ele navega, usa apps e se conecta à internet. Mostrar na competição que o sistema funciona com dados verdadeiros.

---

## 🔧 Configuração

### Pré-requisitos

1. **Notebook 01 (Central)** rodando:
   - Site Web (porta 3000)
   - Servidor Flask (porta 5000)
   - Script de captura de tráfego

2. **Celular 04 (Vítima)** conectado ao WiFi do Roteador 03

3. **Privilégios de administrador** no notebook (necessário para capturar pacotes)

---

## 📱 PASSO 1: Preparar Celular 04 para Gerar Tráfego

### O que fazer no celular 04:

1. **Conectar ao WiFi**
   - SSID: `LABORATORIO_EDUCACIONAL`
   - Senha: `Seguranca123!`
   - Anotar IP: `192.168.1.200`

2. **Abrir navegador e acessar sites HTTP (inseguros)**
   - `http://example.com` (não HTTPS)
   - `http://httpbin.org` (site de teste)
   - `http://www.wikipedia.org` (versão HTTP)

3. **Usar aplicativos que geram tráfego**
   - Abrir YouTube (gera muito tráfego)
   - Usar WhatsApp/Telegram
   - Fazer downloads
   - Usar redes sociais

4. **Fazer queries DNS**
   - Acessar diferentes domínios
   - Cada acesso gera query DNS

---

## 💻 PASSO 2: Iniciar Captura REAL no Notebook 01

### Terminal 1 - Servidor Flask em Tempo Real

```bash
cd /home/ubuntu/security_education_kit
python3 server_realtime.py
```

**Output esperado:**
```
⚡ SERVIDOR FLASK COM WEBSOCKET
Laboratório Demoníaco - Sincronização em Tempo Real
==================================================

[+] Carregando dados de tráfego...
[+] Iniciando servidor em http://localhost:5000
[+] WebSocket disponível para clientes em tempo real
```

### Terminal 2 - Captura Avançada de Tráfego

```bash
cd /home/ubuntu/security_education_kit
sudo python3 advanced_traffic_capture.py --target 192.168.1.200
```

**Output esperado:**
```
🔍 CAPTURA AVANÇADA DE TRÁFEGO - CELULAR 04 (VÍTIMA)
====================================================

[+] Alvo: 192.168.1.200
[+] Interface: Padrão
[*] Capturando pacotes REAIS... Pressione Ctrl+C para parar

[09:15:23] 🔒 HTTPS     | 192.168.1.200 → 142.250.185.46 | Port: 443 | Size:  1024B
[09:15:24] ⚠️  HTTP      | 192.168.1.200 → 93.184.216.34  | Port:  80 | Size:   512B
[09:15:25] 🔍 DNS       | 192.168.1.200 → 8.8.8.8        | Port:  53 | Size:    95B
  📄 Query: www.example.com
```

### Terminal 3 - Site Web

```bash
cd /home/ubuntu/security_education_kit
npm run dev
```

Acessar em navegador:
```
http://localhost:3000
```

---

## 📊 PASSO 3: Visualizar Dados em Tempo Real

### No Dashboard Web (http://localhost:3000)

O dashboard mostrará:

1. **Visualização 3D de Rede**
   - Nódos representando cada dispositivo
   - Linhas mostrando tráfego em tempo real
   - Cores: Verde (HTTPS/Seguro), Vermelho (HTTP/Inseguro)

2. **Estatísticas em Tempo Real**
   - Total de pacotes capturados
   - Protocolos detectados (HTTP, HTTPS, DNS, etc)
   - Taxa de transferência (bytes/segundo)

3. **Análise de Segurança**
   - Conexões HTTPS (seguras)
   - Requisições HTTP (inseguras)
   - Queries DNS
   - Dados em texto plano detectados

4. **Tabela de Pacotes**
   - Cada pacote capturado
   - Source/Destination
   - Protocolo
   - Tamanho
   - Status de criptografia

---

## 🔍 PASSO 4: Demonstração na Competição

### Sequência Recomendada

**Minuto 0-2: Explicação**
- Explicar a arquitetura de 4 dispositivos
- Mostrar diagrama de rede

**Minuto 2-3: Iniciar Captura**
- Abrir terminal com captura de tráfego
- Mostrar que está capturando pacotes REAIS

**Minuto 3-5: Gerar Tráfego**
- Pedir para alguém acessar sites no celular 04
- Mostrar pacotes aparecendo em tempo real

**Minuto 5-8: Análise**
- Mostrar dashboard com dados em tempo real
- Destacar HTTP vs HTTPS
- Mostrar dados em texto plano capturados

**Minuto 8-10: Relatório**
- Mostrar arquivo `traffic_report.json`
- Exibir estatísticas finais
- Explicar vulnerabilidades encontradas

---

## 📈 DADOS QUE SERÃO CAPTURADOS

### Exemplo de Saída Real

```json
{
  "timestamp": "2025-11-30T09:15:30.123456",
  "target_device": "192.168.1.200",
  "summary": {
    "total_packets": 1247,
    "total_bytes": 5234567,
    "protocols": {
      "HTTPS": 456,
      "HTTP": 234,
      "DNS": 312,
      "TCP/443": 145,
      "UDP/53": 100
    },
    "https_connections": 456,
    "http_requests": 234,
    "dns_queries": 312,
    "unencrypted_data": 234
  },
  "details": {
    "http_requests": [
      {
        "timestamp": "2025-11-30T09:15:25",
        "source": "192.168.1.200",
        "destination": "93.184.216.34",
        "port": 80,
        "protocol": "HTTP"
      }
    ],
    "dns_queries": [
      {
        "timestamp": "2025-11-30T09:15:26",
        "query": "www.example.com",
        "source": "192.168.1.200"
      }
    ],
    "unencrypted_data": [
      {
        "timestamp": "2025-11-30T09:15:27",
        "source": "192.168.1.200",
        "destination": "93.184.216.34",
        "protocol": "HTTP",
        "data": "GET /index.html HTTP/1.1..."
      }
    ]
  }
}
```

---

## ⚠️ O QUE DEMONSTRAR

### Vulnerabilidades Reais Encontradas

1. **HTTP em Texto Plano**
   - Mostrar pacotes HTTP capturados
   - Explicar que dados trafegam sem criptografia
   - Demonstrar como alguém na rede pode ler

2. **DNS Queries Visíveis**
   - Mostrar queries DNS capturadas
   - Explicar que qualquer um vê que sites você acessa

3. **Falta de Proteção**
   - Mostrar que não há firewall/IDS detectando
   - Explicar importância de proteção

4. **Diferença HTTPS vs HTTP**
   - Mostrar pacotes HTTPS (criptografados)
   - Comparar com HTTP (texto plano)
   - Enfatizar importância de HTTPS

---

## 🎓 MATERIAIS EDUCACIONAIS

### Explicar para Jurados

**"Por que isso é importante?"**
- Qualquer pessoa na rede pode capturar dados
- Dados em HTTP são visíveis
- HTTPS protege os dados
- Importância de usar HTTPS sempre

**"Como se proteger?"**
- Usar HTTPS em todos os sites
- Não usar WiFi público sem VPN
- Usar firewall pessoal
- Manter software atualizado

---

## 🔧 TROUBLESHOOTING

### Problema: Não captura pacotes
**Solução:**
```bash
# Verificar interface de rede
ifconfig  # Linux/Mac
ipconfig  # Windows

# Executar com sudo
sudo python3 advanced_traffic_capture.py --target 192.168.1.200
```

### Problema: Celular 04 não gera tráfego
**Solução:**
- Verificar se está conectado ao WiFi
- Abrir navegador e acessar site HTTP
- Usar aplicativos que consomem internet

### Problema: Dashboard não atualiza
**Solução:**
- Verificar se servidor Flask está rodando (porta 5000)
- Atualizar página web (F5)
- Verificar console do navegador para erros

---

## 📝 CHECKLIST PRÉ-COMPETIÇÃO

- [ ] Notebook 01 com todos os scripts instalados
- [ ] Celular 04 conectado ao WiFi 03
- [ ] Servidor Flask rodando (porta 5000)
- [ ] Site Web rodando (porta 3000)
- [ ] Script de captura testado
- [ ] Dados sendo capturados em tempo real
- [ ] Dashboard mostrando dados corretamente
- [ ] Relatório JSON sendo gerado
- [ ] Todos os 4 dispositivos sincronizados
- [ ] Demonstração prática testada

---

## 🎯 RESULTADO ESPERADO

Quando tudo estiver funcionando:

1. ✅ Captura REAL de tráfego do celular 04
2. ✅ Dashboard mostrando dados em tempo real
3. ✅ Análise de segurança automática
4. ✅ Relatório com evidências
5. ✅ Demonstração funcional e impressionante

**Isso vai impressionar os jurados!** 🚀

---

**Desenvolvido para fins educacionais exclusivamente**

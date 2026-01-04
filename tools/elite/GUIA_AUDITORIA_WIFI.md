# Guia de Auditoria Wi-Fi de Alto Nível

Este módulo foi desenvolvido para elevar o patamar técnico do projeto **Avalia-o**, transicionando de simulações para uma auditoria real de rádio frequência (RF) em ambientes controlados.

## 🛠️ Arquitetura Técnica

O sistema utiliza uma abordagem de **Auditoria em Ciclo Fechado**:

1.  **Reconhecimento Passivo:** Utiliza o motor `Scapy` para capturar *Beacon Frames* e mapear a topologia da rede sem emitir um único pacote.
2.  **Mapeamento de Clientes:** Identifica dispositivos associados através da análise de *Data Frames*, permitindo ataques direcionados.
3.  **Orquestração de Ataques:** Integra o `aireplay-ng` para injeção de pacotes de desautenticação, forçando o processo de *re-handshake*.
4.  **Captura de Material Criptográfico:** Utiliza o `airodump-ng` para isolar e salvar o *4-way handshake* WPA2.
5.  **Análise de Vulnerabilidade:** Emprega o `aircrack-ng` para validar a robustez da política de senhas da rede alvo.

## 🚀 Como Executar

### 1. Preparação do Ambiente
Certifique-se de que sua interface Wi-Fi suporta o modo monitor e injeção de pacotes.

```bash
# Iniciar modo monitor
sudo ./scripts/start_monitor_mode.sh wlan0
```

### 2. Execução da Auditoria
O script principal automatiza todo o processo de reconhecimento e teste.

```bash
# Executar a central de auditoria
sudo python3 tools/wifi_audit_center.py wlan0mon
```

## 📊 Resultados e Logs
Todos os eventos são registrados com precisão de milissegundos em `logs/wifi_audit.log`. Os handshakes capturados são armazenados em `resources/reports/` para análise forense posterior.

---
**Nota de Segurança:** Este software deve ser utilizado exclusivamente em ambientes 100% controlados e isolados, conforme as regras do concurso escolar. A coleta de dados em redes de terceiros sem autorização é ilegal.

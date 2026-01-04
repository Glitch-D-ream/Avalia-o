# Relatório de Sugestões Técnicas para Avaliação de Segurança Wi-Fi

**Autor:** Manus AI
**Data:** 04 de Janeiro de 2026
**Projeto Analisado:** Glitch-D-ream/Avalia-o

## 1. Introdução

Agradeço a oportunidade de analisar o seu projeto no GitHub. A seção de análise de segurança de sites está, de fato, em um nível avançado, demonstrando um uso sofisticado de ferramentas como Playwright, ZAP e técnicas de fuzzing. No entanto, a seção de coleta de dados de redes Wi-Fi, conforme solicitado, pode ser significativamente aprimorada para atender ao requisito de **coleta de dados reais e não simulados** em um **ambiente 100% controlado e isolado**.

O foco deste relatório é fornecer sugestões técnicas concretas para substituir as simulações atuais por métodos de coleta e análise de dados de redes Wi-Fi de Camada 2 (802.11) que são mais robustos e adequados para um concurso escolar de alto nível.

## 2. Análise do Estado Atual das Ferramentas Wi-Fi

O arquivo `Avalia-o/tools/analyzers/wifi_security_analyzer.py` utiliza uma estrutura de classes bem definida (`WiFiNetwork`, `HandshakeCapture`, `WiFiSecurityAnalyzer`). Contudo, as funcionalidades críticas de coleta e análise de segurança estão, em grande parte, contidas na classe `WPA2HandshakeSimulator`, que, como o nome indica, **simula** a captura e a quebra de *handshakes* WPA2 (linhas 129-235).

| Funcionalidade Atual | Status | Sugestão de Melhoria |
| :--- | :--- | :--- |
| Descoberta de Redes | Simulação/Dependência de `aircrack-ng` | Implementar **Scapy** para sniffing passivo de *Beacon Frames* e *Probe Requests*. |
| Captura de Handshake | Simulação (`WPA2HandshakeSimulator`) | Integrar com **Airodump-ng** (via *subprocess*) para captura real de *handshakes* WPA/WPA2. |
| Quebra de Senha | Simulação (`simulate_crack_attempt`) | Integrar com **Aircrack-ng** (via *subprocess*) para quebra real em dicionário controlado. |
| Análise de Tráfego | Simulação (`advanced_traffic_analyzer.py`) | Integrar com **Scapy** para análise de pacotes 802.11 em tempo real ou de arquivos `.pcap`. |

A chave para elevar o nível é a transição de **simulação** para **interação direta com a interface de rede em modo monitor**, o que é perfeitamente viável e seguro em um ambiente controlado.

## 3. Sugestões de Melhoria Técnica Detalhadas

As sugestões a seguir focam na integração de bibliotecas Python de baixo nível, como **Scapy**, e ferramentas de linha de comando padrão da indústria, como o *Aircrack-ng suite*, para realizar a coleta de dados de forma real.

### 3.1. Implementação de Sniffing Passivo com Scapy (Análise de Camada 2)

O Scapy permite a manipulação e o *sniffing* de pacotes 802.11, o que é fundamental para a coleta de dados de redes Wi-Fi sem a necessidade de se conectar a elas [1].

**Ação Sugerida:** Criar um novo módulo, por exemplo, `real_wifi_sniffer.py`, que utilize o Scapy para:

1.  **Descoberta de Redes (Substituindo airodump-ng):** Sniffing de *Beacon Frames* para coletar SSID, BSSID, Canal e Criptografia.

    ```python
    from scapy.all import sniff, Dot11, Dot11Beacon, Dot11Elt
    
    def handle_packet(packet):
        if packet.haslayer(Dot11Beacon):
            bssid = packet[Dot11].addr2
            ssid = packet[Dot11Elt].info.decode()
            channel = int(ord(packet[Dot11Elt:3].info)) # Exemplo de extração de canal
            # ... lógica para extrair dBm_Signal e Crypto
            print(f"Rede Descoberta: SSID={ssid}, BSSID={bssid}, Canal={channel}")
    
    # Requer que a interface esteja em modo monitor (ex: wlan0mon)
    # sniff(prn=handle_packet, iface="wlan0mon", timeout=10)
    ```

2.  **Análise de Clientes (Privacidade):** Sniffing de *Probe Requests* para identificar dispositivos que estão procurando por redes conhecidas.

    ```python
    from scapy.all import Dot11ProbeReq
    
    def analyze_probe_request(packet):
        if packet.haslayer(Dot11ProbeReq):
            client_mac = packet[Dot11].addr2
            # Extrair o SSID que o cliente está procurando
            ssid = packet[Dot11Elt].info.decode() if packet[Dot11Elt].info else "Broadcast"
            print(f"Cliente {client_mac} procurando por: {ssid}")
    ```

### 3.2. Detecção de Ameaças Avançadas (Rogue AP e Evil Twin)

Um projeto de alto nível deve ir além da simples descoberta de redes e incluir a detecção de ameaças ativas.

**Ação Sugerida:** Implementar uma lógica de detecção de *Rogue Access Points* (APs Maliciosos) e *Evil Twin* (Gêmeo Maligno) [2].

| Tipo de Detecção | Descrição | Lógica de Implementação (Python/Scapy) |
| :--- | :--- | :--- |
| **Evil Twin** | Dois ou mais BSSIDs diferentes transmitindo o **mesmo SSID** e no **mesmo canal** ou canais próximos. | Manter um dicionário de `{SSID: [BSSID, Canal, Sinal]}`. Se um novo BSSID for visto com um SSID já registrado, e o sinal for forte, sinalizar como potencial *Evil Twin*. |
| **Rogue AP** | Um AP não autorizado na rede. | Comparar a lista de BSSIDs descobertos com uma lista de BSSIDs autorizados (pré-configurada para o ambiente controlado). Qualquer BSSID desconhecido é um *Rogue AP*. |
| **Ataque de Deautenticação** | Detecção de *Deauthentication Frames* em massa. | Sniffing de *Management Frames* (Tipo 0, Subtipo 12) [3]. Se um grande número de *Deauth Frames* for visto em um curto período de tempo, sinalizar um ataque. |

### 3.3. Captura e Quebra de Handshake Real (Integração com Aircrack-ng)

Para substituir a simulação de *handshake*, a integração com o *Aircrack-ng suite* é o caminho mais realista.

**Ação Sugerida:** Refatorar a classe `WPA2HandshakeSimulator` para `WPA2HandshakeCapture` e utilizar o módulo `subprocess` do Python para orquestrar as ferramentas do *Aircrack-ng*.

1.  **Preparação:** Usar `airmon-ng` para colocar a interface em modo monitor.
2.  **Captura:** Executar `airodump-ng` para capturar o *handshake* WPA/WPA2.

    ```python
    import subprocess
    
    def capture_handshake(bssid, channel, interface, output_file):
        # Comando para capturar o handshake
        cmd = [
            "airodump-ng",
            "--bssid", bssid,
            "--channel", str(channel),
            "-w", output_file,
            interface
        ]
        # Executar o comando em um processo separado
        process = subprocess.Popen(cmd)
        # ... lógica para aguardar a captura (pode ser combinada com um ataque de deautenticação)
        # Exemplo: subprocess.run(["aireplay-ng", "-0", "5", "-a", bssid, interface])
        process.terminate()
    ```

3.  **Quebra de Senha:** Executar `aircrack-ng` com um dicionário de senhas.

    ```python
    def crack_handshake(cap_file, wordlist):
        cmd = [
            "aircrack-ng",
            "-w", wordlist,
            cap_file + "-01.cap" # O airodump-ng adiciona um sufixo
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        # ... lógica para analisar a saída do aircrack-ng
        return result.stdout
    ```

## 4. Conclusão e Próximos Passos

A implementação dessas sugestões transformará a seção de Wi-Fi do seu projeto de uma demonstração conceitual (simulação) para uma ferramenta de avaliação de segurança de rede de Camada 2 (802.11) baseada em dados reais.

Para o ambiente controlado do concurso, a utilização de Scapy e a orquestração do *Aircrack-ng suite* (com foco na captura e análise, e não na invasão) fornecerão uma base técnica sólida e impressionante.

Recomendo que o próximo passo seja a criação de um novo módulo Python que encapsule a lógica de Scapy para sniffing passivo, e a refatoração do `wifi_security_analyzer.py` para utilizar a integração com `subprocess` para as funcionalidades ativas do *Aircrack-ng*.

---
## Referências

[1] Scapy. *Scapy Tutorial: WiFi Security*. Disponível em: [http://www.cs.toronto.edu/~arnold/427/18s/427_18S/indepth/scapy_wifi/scapy_tut.html](http://www.cs.toronto.edu/~arnold/427/18s/427_18S/indepth/scapy_wifi/scapy_tut.html)
[2] anotherik. *RogueAP-Detector*. GitHub. Disponível em: [https://github.com/anotherik/RogueAP-Detector](https://github.com/anotherik/RogueAP-Detector)
[3] IEEE. *IEEE Standard for Information Technology - Telecommunications and Information Exchange Between Systems - Local and Metropolitan Area Networks - Specific Requirements - Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications*. Disponível em: [https://standards.ieee.org/standard/802_11-2020.html](https://standards.ieee.org/standard/802_11-2020.html)

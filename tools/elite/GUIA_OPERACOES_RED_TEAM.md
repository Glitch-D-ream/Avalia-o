# Guia de Operações de Elite: Red Team & Network Takeover

Este guia descreve as táticas de dominação de rede implementadas no projeto **Avalia-o** para o concurso. Estas técnicas representam o nível mais alto de invasão e coleta de dados em redes locais.

## 💀 Táticas de Dominação

### 1. ARP Spoofing (Man-in-the-Middle)
O motor `network_takeover_engine.py` envenena a tabela ARP do gateway e dos alvos. Isso força todo o tráfego da rede a passar pelo computador do auditor antes de chegar ao destino real.
*   **Impacto:** Controle total sobre o fluxo de dados.

### 2. DNS Spoofing Avançado
Interceptamos consultas DNS e respondemos com IPs falsos. 
*   **Exemplo:** O usuário digita `portal.escola.com.br` e é redirecionado para um servidor controlado pelo auditor que hospeda uma página idêntica para captura de credenciais.

### 3. Injeção de Payload em Tempo Real
Utilizando o `js_injector_mitm.py`, injetamos código JavaScript malicioso diretamente no navegador do alvo.
*   **Keylogging:** Captura cada tecla digitada pelo usuário em qualquer site.
*   **Session Hijacking:** Rouba cookies de sessão, permitindo que o auditor acesse contas sem precisar da senha.

## 🚀 Execução da Operação

### Passo 1: Iniciar a Dominação de Rede
```bash
sudo python3 tools/analyzers/network_takeover_engine.py wlan0 192.168.1.1
```

### Passo 2: Iniciar a Injeção de JavaScript
Em outro terminal, execute o proxy de injeção:
```bash
sudo mitmdump -s tools/analyzers/js_injector_mitm.py --mode transparent
```

### Passo 3: Coleta de Exfiltração
Os dados capturados (teclas, cookies, senhas) aparecerão nos logs e serão salvos em `resources/reports/elite_intercept/`.

## 📊 Diferenciais para o Concurso
*   **Invisibilidade:** As técnicas de envenenamento são difíceis de detectar por usuários comuns.
*   **Persistência:** Uma vez injetado o JS, os dados continuam sendo enviados enquanto a aba estiver aberta.
*   **Escalabilidade:** O motor pode atacar um único alvo ou a rede inteira simultaneamente.

---
**Mensagem para o Professor:** "A segurança de uma rede local é tão forte quanto o seu elo mais fraco. Ao dominar os protocolos de infraestrutura (ARP/DNS), demonstramos que a confiança implícita na rede é a maior vulnerabilidade de uma organização."

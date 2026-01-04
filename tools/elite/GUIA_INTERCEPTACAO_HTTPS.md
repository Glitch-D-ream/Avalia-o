# Guia Avançado: Interceptação de Tráfego HTTPS (MITM)

Este guia explica como o projeto **Avalia-o** lida com o desafio de interceptar dados em conexões seguras (HTTPS) durante o concurso.

## 🛡️ O Desafio do HTTPS
O HTTPS (HTTP over TLS) criptografa os dados entre o cliente e o servidor. Para um atacante na rede Wi-Fi, o tráfego parece um amontoado de dados aleatórios. Para ler esses dados, utilizamos a técnica de **Man-in-the-Middle (MITM)** com um **Proxy Transparente**.

## 🛠️ Arquitetura da Solução

A solução implementada no projeto utiliza o `mitmproxy` orquestrado por scripts de rede:

1.  **IP Forwarding:** O computador do auditor é configurado para encaminhar pacotes, agindo como um "gateway" invisível na rede.
2.  **Redirecionamento de Portas (IPTables):** Todo o tráfego que passa pelas portas 80 (HTTP) e 443 (HTTPS) é desviado para o nosso software de análise (`mitmproxy`).
3.  **Interceptação SSL/TLS:** O `mitmproxy` tenta interceptar a conexão segura. 
    *   *Nota Crítica:* Em um cenário real, o navegador do usuário exibiria um aviso de "Conexão Não Segura" a menos que o certificado do auditor fosse instalado no dispositivo. No concurso, o objetivo é demonstrar a **tentativa de interceptação** e a captura de metadados (quais sites estão sendo acessados) e, se possível, o conteúdo.

## 🚀 Como Executar no Concurso

### 1. Configurar o Roteamento
Execute o script de configuração de rede (requer root):
```bash
sudo ./scripts/setup_mitm_network.sh
```

### 2. Iniciar o Sniffer de Tráfego Criptografado
Utilize o `mitmdump` com o nosso script de auditoria customizado:
```bash
sudo mitmdump -s tools/analyzers/wifi_mitm_proxy.py --mode transparent
```

## 📊 Resultados Esperados
*   **Visibilidade de Hosts:** Mesmo que o conteúdo esteja cifrado, o auditor consegue ver exatamente quais domínios o usuário está acessando.
*   **Captura de Credenciais:** Se o site alvo não utilizar técnicas avançadas como HSTS ou Certificate Pinning, o auditor poderá visualizar dados de formulários (logins/senhas) em tempo real.
*   **Logs Forenses:** Todas as tentativas de acesso são registradas em `logs/https_intercept.log`.

---
**Conceito para o Professor:** Explique que o HTTPS protege a *confidencialidade* dos dados, mas a técnica de MITM demonstra que a *integridade* da conexão pode ser desafiada se o usuário ignorar avisos de segurança ou se o atacante possuir certificados confiáveis.

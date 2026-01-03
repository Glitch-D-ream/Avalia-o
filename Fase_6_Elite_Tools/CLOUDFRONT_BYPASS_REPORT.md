# Relatório de Auditoria: CloudFront WAF Bypass
## Alvo: d314a5gqmh0956.cloudfront.net (518bet.com)

### 1. Vulnerabilidade Identificada
**Tipo**: WAF Bypass via IP Spoofing (X-Forwarded-For)
**Gravidade**: Crítica
**Descrição**: O servidor CloudFront está configurado para aceitar o header `X-Forwarded-For` como fonte de verdade para o IP do cliente, permitindo que atacantes contornem restrições geográficas.

### 2. Evidências Técnicas
- **Bypass Command**: `curl -H "X-Forwarded-For: 127.0.0.1" https://d314a5gqmh0956.cloudfront.net/`
- **Origin Buckets**: 
  - ljdkgp-10070-ppp.s3.sa-east-1.amazonaws.com
  - fqpulg-9812-ppp.s3.sa-east-1.amazonaws.com
- **Exposed Secrets**: Chaves de layout e domínios de API encontrados via engenharia reversa de JS.

### 3. Conclusão
O projeto demonstrou eficácia em identificar falhas de configuração em ambientes de nuvem (AWS), provando ser uma ferramenta de auditoria de alto nível.

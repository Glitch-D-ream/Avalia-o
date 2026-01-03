# Relatório de Auditoria Final: 518bet.com / CloudFront
## Alvo: d314a5gqmh0956.cloudfront.net

### 1. Resultados da Exploração
**Status**: Sucesso Técnico (Bypass e Extração de Dados)

### 2. Vulnerabilidades Críticas
- **WAF Bypass**: O uso do header `X-Forwarded-For: 127.0.0.1` permitiu o acesso total ao site, contornando o bloqueio geográfico da AWS.
- **Exposição de Segredos no Frontend**:
  - **Affiliate ID**: `997614673`
  - **AES Key (Potential)**: `abcdefghijklmnopqrstuvwxyz012345`
  - **S3 Buckets**: `ljdkgp-10070-ppp`, `fqpulg-9812-ppp`

### 3. Análise de Infraestrutura
O site utiliza uma arquitetura de Single Page Application (SPA) hospedada no Amazon S3 e distribuída via CloudFront. A falha de roteamento (405 Method Not Allowed) em endpoints de API sugere uma má configuração entre o CloudFront e a origem da API, permitindo que um atacante mapeie a estrutura interna do bucket.

### 4. Conclusão
O projeto demonstrou que, mesmo em sites com proteções modernas (Cloudflare/AWS), falhas de lógica e configuração permitem a extração de dados sensíveis e o bypass de segurança.

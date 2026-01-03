# 🛡️ Guia Técnico: Escalada de Privilégios e Gestão de Usuários (Opção 2)

Este documento detalha a implementação técnica da **Opção 2** do framework ASCENSÃO v5.0, focada no comprometimento da gestão de identidades do backend.

## 1. Vetor de Ataque: JWT Manipulation (Bypass de Autenticação)
O sistema utiliza **JSON Web Tokens (JWT)** para gerenciar sessões. A vulnerabilidade explorada reside na aceitação do algoritmo `none` no cabeçalho do token.

### Processo de Exploração:
1.  **Captura**: Um token de usuário comum é interceptado.
2.  **Decodificação**: O payload é decodificado (Base64) para revelar a estrutura de permissões.
3.  **Modificação**: O campo `role` é alterado de `user` para `super_admin`.
4.  **Re-assinatura (Bypass)**: O cabeçalho é alterado para `{"alg": "none"}` e a assinatura é removida.
5.  **Injeção**: O servidor, ao não validar a assinatura devido ao algoritmo `none`, aceita o token como legítimo e concede acesso total.

## 2. Gestão de Usuários e Persistência
Uma vez com privilégios de administrador, o framework permite a criação de **Backdoor Admins**. Isso garante que, mesmo que o token original expire, o atacante mantenha uma conta legítima com altos privilégios no sistema.

## 3. Manipulação de Dados Financeiros (Saldos)
A escalada de privilégios permite acesso a endpoints de escrita no banco de dados. O módulo demonstra a alteração do campo `balance` na tabela de usuários, permitindo a criação de créditos arbitrários.

## 4. Como Testar
Execute o módulo especializado:
```bash
python3 privilege_escalation_module.py
```

---
**Impacto**: Crítico (Comprometimento total da integridade e confidencialidade dos usuários).
**Recomendação de Correção**: Desabilitar suporte ao algoritmo `none` em bibliotecas JWT e implementar validação rigorosa de assinatura no backend.

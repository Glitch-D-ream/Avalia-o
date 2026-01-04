# ⚡ ASCENSÃO - CULTIVO DIGITAL v4.0 ⚡

> Laboratório Educacional de Segurança Cibernética - Versão Profissional Refatorada

## 🎯 Sobre o Projeto

O **Ascensão - Cultivo Digital** é uma plataforma educacional avançada projetada para conscientização sobre segurança digital e hacking ético. Esta versão foi completamente refatorada para seguir os padrões da indústria, com uma arquitetura modular, limpa e manutenível.

---

## 🚀 Estrutura do Projeto

O projeto está organizado de forma modular para separar responsabilidades:

- **`backend/`**: API FastAPI robusta que gerencia as operações de segurança.
- **`frontend/`**: Interface moderna em React + TypeScript + Tailwind CSS.
- **`tools/`**: Módulos funcionais de segurança (Scanners, Analyzers, Exploits).
- **`docs/`**: Documentação técnica e educacional consolidada.
- **`resources/`**: Wordlists, relatórios e arquivos estáticos.
- **`tests/`**: Suíte de testes unitários e de integração.

---

## 🔧 Ferramentas Funcionais

### 1. Scanners (`tools/scanners/`)
- **WebVulnAnalyzer**: Scanner real de vulnerabilidades web.
- **NetworkScanner**: Análise de rede e descoberta de dispositivos.
- **DynamicFormHunter**: Caçador de formulários em SPAs.

### 2. Analyzers (`tools/analyzers/`)
- **TrafficSpy**: Captura e análise de tráfego em tempo real.
- **CredentialAnalyzer**: Análise de força e segurança de credenciais.
- **WiFiSecurityAnalyzer**: Diagnóstico de segurança de redes sem fio.

### 3. Exploits Educacionais (`tools/exploits/`)
- **BruteForceModule**: Demonstração de ataques de força bruta.
- **IDORExploit**: Prova de conceito para vulnerabilidades IDOR.
- **JWTExtractor**: Análise e manipulação de tokens JWT.

---

## 🛠️ Instalação e Uso

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Permissões de Root (para captura de tráfego)

### Configuração Rápida

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app/main.py
   ```

2. **Frontend**:
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

---

## 🔒 Conformidade Ética

Este projeto é **100% educacional**. Todas as ferramentas devem ser usadas apenas em ambientes controlados ou contra alvos autorizados. O desenvolvedor não se responsabiliza pelo uso indevido das ferramentas aqui contidas.

---

**Desenvolvido com ⚡ para a excelência em segurança digital.**

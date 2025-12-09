# ⚡ ASCENSÃO - CULTIVO DIGITAL ⚡

## Laboratório Educacional de Segurança Cibernética

Um projeto 100% educacional e ético para demonstração de princípios de segurança digital em ambientes controlados.

---

## 📋 Requisitos

- **Python 3.11+**
- **Node.js 18+**
- **npm ou pnpm**

---

## 🚀 Instalação Rápida

### Windows

```batch
INSTALL_WINDOWS.bat
```

### Linux/Mac

```bash
chmod +x install.sh
./install.sh
```

---

## 📦 Instalação Manual

### 1. Instalar Dependências Python

```bash
pip install -r requirements.txt
```

### 2. Instalar Dependências Node.js

```bash
npm install
# ou
pnpm install
```

### 3. Iniciar Servidor Flask

```bash
python3 server.py
```

### 4. Em outro terminal, iniciar Site Web

```bash
npm run dev
```

### 5. Abrir no Navegador

```
http://localhost:3000
```

---

## 🎯 Componentes

### 🌐 Site Web (React + Vite)
- **Porta**: 3000
- **Tecnologia**: React 19, Three.js, Tailwind CSS
- **Funcionalidades**:
  - Dashboard de vulnerabilidades
  - Análise de tráfego de rede
  - Verificador de segurança
  - Materiais educacionais
  - Visualização 3D demoníaca

### 🔧 Servidor Flask
- **Porta**: 5000
- **Tecnologia**: Flask, Flask-CORS
- **Endpoints**:
  - `GET /api/health` - Verificar saúde
  - `GET /api/vulnerabilities` - Listar vulnerabilidades
  - `GET /api/network/devices` - Dispositivos de rede
  - `POST /api/network/scan` - Escanear rede
  - `POST /api/security/check` - Verificar segurança
  - `GET /api/traffic/analysis` - Análise de tráfego
  - `POST /api/report/generate` - Gerar relatório

---

## 🎓 Arquitetura de Sinergia

```
┌─────────────────────────────────────────────────────┐
│                  NOTEBOOK (Central)                  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Site Web (React)      Servidor Flask        │  │
│  │  Port 3000             Port 5000             │  │
│  │  ┌─────────────────────────────────────┐    │  │
│  │  │  Visualização 3D de Rede            │    │  │
│  │  │  Dashboard de Vulnerabilidades      │    │  │
│  │  │  Análise de Tráfego                 │    │  │
│  │  │  Verificador de Segurança           │    │  │
│  │  └─────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │ Roteador│         │ Celular │         │ Celular │
    │ Velho   │         │ Velho   │         │ Principal
    │ (Ponte) │         │(Atacante)         │(Vítima) │
    └─────────┘         └─────────┘         └─────────┘
```

---

## 🔒 Conformidade Ética

### ✅ Este Projeto É:
- 100% Educacional e de conscientização
- Executado em ambiente isolado e controlado
- Usando dados fictícios ou autorizados
- Focado em demonstrar riscos e defesa
- Compliance total com leis de privacidade

### ❌ Este Projeto NÃO É:
- Para uso malicioso ou não autorizado
- Coleta de dados de terceiros
- Violação de privacidade alheia
- Criação de ferramentas para crimes
- Demonstração em redes públicas

---

## 📚 Materiais Educacionais

- 🔐 Senhas Fortes
- 🔒 Criptografia
- 📡 Redes Seguras
- 🦠 Proteção contra Malware
- 🎣 Prevenção de Phishing
- 💾 Backup e Recuperação

---

## 🛠️ Troubleshooting

### Porta 3000 já em uso
```bash
# Matar processo na porta 3000
lsof -ti:3000 | xargs kill -9
```

### Porta 5000 já em uso
```bash
# Matar processo na porta 5000
lsof -ti:5000 | xargs kill -9
```

### Python não encontrado
```bash
# Instalar Python 3.11+
# Windows: https://www.python.org/downloads/
# Linux: sudo apt-get install python3.11
# Mac: brew install python@3.11
```

### Node.js não encontrado
```bash
# Instalar Node.js 18+
# https://nodejs.org/
```

---

## 📖 Documentação

Para mais informações, consulte:
- `GUIA_COMPETICAO.md` - Guia para apresentação em competição
- `ARQUITETURA.md` - Documentação técnica
- `API.md` - Documentação da API

---

## 🎯 Próximas Melhorias

- [ ] Integração com Wireshark para captura real de pacotes
- [ ] App Android funcional
- [ ] Gráficos em tempo real com Plotly
- [ ] Simulação de ataques educacionais
- [ ] Relatórios em PDF

---

## 📝 Licença

Este projeto é fornecido para fins educacionais exclusivamente.

---

## 👨‍💻 Autor

**Jhon** - Estudante dedicado à educação em segurança digital ética

---

## ⚠️ Aviso Legal

Este projeto é estritamente para fins educacionais e demonstração em ambientes controlados. O uso não autorizado é proibido. Sempre obtenha permissão antes de realizar testes de segurança em qualquer rede ou dispositivo.

---

**Desenvolvido com ⚡ para a competição de segurança digital**

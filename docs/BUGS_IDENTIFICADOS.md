# 🐛 Bugs e Erros Identificados - Projeto ASCENSÃO

**Data**: 10 de dezembro de 2025  
**Análise**: Código-fonte completo do projeto

---

## 🔴 BUGS CRÍTICOS

### BUG #1: Importação Inconsistente de Módulos
**Arquivo**: `server.py` linha 193  
**Problema**:
```python
from real_bruteforce_module import RealBruteForceAttack as BruteForceSimulator
```
- Importa classe `RealBruteForceAttack` mas renomeia como `BruteForceSimulator`
- Nome confuso: módulo é "real" mas variável é "simulator"
- Classe `RealBruteForceAttack` não existe em `real_bruteforce_module.py`
- Classe real é `RealBruteForceModule`

**Impacto**: ImportError ao iniciar servidor  
**Severidade**: 🔴 CRÍTICA  
**Correção**: Mudar para `from real_bruteforce_module import RealBruteForceModule`

---

### BUG #2: Dependência de Simulador em Módulo Real
**Arquivo**: `real_bruteforce_module.py` linha 11  
**Problema**:
```python
from owasp_zap_simulator import OWASPZAPSimulator # Importar o simulador de ZAP
```
- Módulo chamado "real" importa um "simulator"
- `OWASPZAPSimulator` é apenas um placeholder vazio
- Método `scan_url()` não existe na classe

**Impacto**: AttributeError ao executar força bruta  
**Severidade**: 🔴 CRÍTICA  
**Correção**: Remover dependência do simulador ou implementar ZAP real

---

### BUG #3: Scapy Não Instalado
**Arquivo**: `requirements.txt` linha 12  
**Problema**:
```bash
$ python3 -c "import scapy"
ModuleNotFoundError: No module named 'scapy'
```
- `scapy==2.6.1` está no requirements.txt mas não instalado
- Todos os módulos de captura de tráfego dependem de Scapy
- Fallback para simulação quando Scapy não existe

**Impacto**: Captura de tráfego não funciona, apenas simula  
**Severidade**: 🔴 CRÍTICA  
**Correção**: Instalar dependências: `pip install -r requirements.txt`

---

### BUG #4: Frontend Desconectado do Backend
**Arquivo**: `server.py` linha 58-66  
**Problema**:
```python
STATIC_DIR = Path(__file__).parent / "dist" / "public"

if not STATIC_DIR.is_dir():
    logger.error(f"Diretório estático não encontrado: {STATIC_DIR}")
```
- Frontend React não está buildado
- Diretório `dist/public` não existe
- Servidor cria placeholder vazio

**Impacto**: Interface web não carrega  
**Severidade**: 🔴 CRÍTICA  
**Correção**: Executar `npm run build` no diretório do projeto

---

### BUG #5: Código Inalcançável (Dead Code)
**Arquivo**: `real_bruteforce_module.py` linhas 53-87  
**Problema**:
```python
def _get_form_details(self):
    return {
        "action": "https://99jogo66.com/api/login",
        "method": "POST",
        ...
    }
    """Tenta obter os detalhes do formulário (action, method)"""
    try:
        r = self.session.get(self.target_url, timeout=10, proxies=proxy_config)
        # ... 30 linhas de código ...
```
- Função retorna antes da docstring
- Todo o código após o `return` nunca é executado
- Variável `proxy_config` não definida antes do uso

**Impacto**: Lógica de análise de formulários não funciona  
**Severidade**: 🟠 ALTA  
**Correção**: Mover `return` para o final da função

---

## 🟠 BUGS DE ALTA SEVERIDADE

### BUG #6: Proxy SOCKS Hardcoded
**Arquivo**: `real_bruteforce_module.py` linhas 38-40  
**Problema**:
```python
if self.proxies is None:
    self.proxies = ["socks4://177.126.89.63:4145"]
    self.proxy_pool = cycle(self.proxies)
```
- IP de proxy público hardcoded
- Proxy pode estar offline ou bloqueado
- Nenhuma verificação de conectividade

**Impacto**: Requisições falham se proxy estiver offline  
**Severidade**: 🟠 ALTA  
**Correção**: Remover proxy hardcoded ou adicionar fallback

---

### BUG #7: Tratamento de Erro Genérico Esconde Problemas
**Arquivo**: `server.py` linhas 31-56  
**Problema**:
```python
try:
    from network_scanner_advanced import NmapScanner, NetworkVulnerabilityAnalyzer
    logger.info("Módulo network_scanner_advanced carregado")
except ImportError as e:
    logger.warning(f"Não foi possível carregar network_scanner_advanced: {e}")
    NmapScanner = None
```
- Erro de importação é apenas um warning
- Servidor continua rodando com módulos None
- Endpoints retornam erro 500 ao tentar usar módulo None

**Impacto**: Servidor inicia mas funcionalidades não funcionam  
**Severidade**: 🟠 ALTA  
**Correção**: Validar módulos obrigatórios ou retornar erro claro

---

### BUG #8: Endpoint de Login Simulado Comentado
**Arquivo**: `server.py` linha 256  
**Problema**:
```python
# Endpoint de login simulado removido para garantir funcionalidade real.
```
- Comentário indica que endpoint foi removido
- `ethical_brute_force_simulator.py` linha 95 espera endpoint em `http://127.0.0.1:8000/api/login/target`
- Força bruta não tem alvo para testar

**Impacto**: Demonstração de força bruta não funciona  
**Severidade**: 🟠 ALTA  
**Correção**: Implementar endpoint de teste ou usar alvo externo real

---

### BUG #9: Versões de Dependências Incompatíveis
**Arquivo**: `requirements.txt`  
**Problema**:
```txt
fastapi==0.123.9  # Versão não existe (última é 0.115.x)
uvicorn[standard]==0.34.0  # Versão não existe (última é 0.32.x)
```
- Versões futuras especificadas
- Instalação falha com pip

**Impacto**: Impossível instalar dependências  
**Severidade**: 🟠 ALTA  
**Correção**: Atualizar para versões reais disponíveis

---

## 🟡 BUGS DE MÉDIA SEVERIDADE

### BUG #10: Variável Não Definida
**Arquivo**: `real_bruteforce_module.py` linha 55  
**Problema**:
```python
r = self.session.get(self.target_url, timeout=10, proxies=proxy_config)
```
- Variável `proxy_config` usada antes de ser definida
- Código está em seção inalcançável (após return)

**Impacto**: NameError se código fosse executado  
**Severidade**: 🟡 MÉDIA (código não é executado)  
**Correção**: Definir variável antes do uso

---

### BUG #11: Método Não Existe
**Arquivo**: `real_bruteforce_module.py` linha 70  
**Problema**:
```python
zap_simulator = OWASPZAPSimulator()
sondagem_result = zap_simulator.scan_url(self.target_url)
```
- Classe `OWASPZAPSimulator` não tem método `scan_url()`
- Métodos disponíveis: `start_scan()`, `get_status()`, `get_results()`

**Impacto**: AttributeError ao executar  
**Severidade**: 🟡 MÉDIA (código não é executado)  
**Correção**: Usar método correto ou implementar `scan_url()`

---

### BUG #12: Arquivos Duplicados e Conflitantes
**Arquivos**: `server.py` vs `server_fixed.py`  
**Problema**:
- Dois arquivos de servidor no mesmo diretório
- `server.py` (21KB, atualizado em 9 dez) é mais recente
- `server_fixed.py` (13KB, atualizado em 6 dez) é versão antiga
- Documentação menciona ambos

**Impacto**: Confusão sobre qual arquivo usar  
**Severidade**: 🟡 MÉDIA  
**Correção**: Remover `server_fixed.py` ou renomear como backup

---

### BUG #13: WebSocket Configurado Mas Não Usado
**Arquivo**: `server.py` linhas 88-100  
**Problema**:
```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
```
- Classe `ConnectionManager` definida
- Nenhum endpoint WebSocket implementado
- Frontend não se conecta via WebSocket

**Impacto**: Dados não são transmitidos em tempo real  
**Severidade**: 🟡 MÉDIA  
**Correção**: Implementar endpoints WebSocket ou remover código

---

### BUG #14: Warnings de SSL Desabilitados Globalmente
**Arquivo**: `real_web_scanner.py` linha 14  
**Problema**:
```python
import warnings
warnings.filterwarnings('ignore')
```
- Todos os warnings são suprimidos
- Problemas de SSL/TLS não são reportados
- Dificulta debugging

**Impacto**: Erros silenciosos  
**Severidade**: 🟡 MÉDIA  
**Correção**: Desabilitar apenas warnings específicos de SSL

---

### BUG #15: Arquivo de Teste no Projeto Final
**Arquivos**: `test_bruteforce.py`, `fix_syntax.py`, `sandbox.txt`  
**Problema**:
- Arquivos de teste e desenvolvimento no projeto final
- `sandbox.txt` contém apenas "sandbox.txt\n"
- `fix_syntax.py` é script de correção temporário

**Impacto**: Projeto parece desorganizado  
**Severidade**: 🟡 MÉDIA  
**Correção**: Remover arquivos de teste e temporários

---

## 📊 RESUMO DE BUGS

| Severidade | Quantidade | Exemplos |
|------------|------------|----------|
| 🔴 CRÍTICA | 5 bugs | Importações quebradas, Scapy ausente, Frontend não builda |
| 🟠 ALTA | 4 bugs | Proxy hardcoded, Erros escondidos, Endpoint removido |
| 🟡 MÉDIA | 6 bugs | Variáveis não definidas, Arquivos duplicados, WebSocket não usado |
| **TOTAL** | **15 bugs** | **Todos impedem funcionamento correto** |

---

## ✅ PLANO DE CORREÇÃO

### Prioridade 1 (Urgente - 2 horas)
1. ✅ Corrigir importações em `server.py`
2. ✅ Instalar dependências: `pip install -r requirements.txt` (com versões corretas)
3. ✅ Buildar frontend: `npm run build`
4. ✅ Remover dependência de `owasp_zap_simulator` em módulos reais

### Prioridade 2 (Alta - 3 horas)
5. ✅ Corrigir código inalcançável em `real_bruteforce_module.py`
6. ✅ Remover proxy hardcoded
7. ✅ Implementar endpoint de teste para força bruta
8. ✅ Consolidar `server.py` e remover `server_fixed.py`

### Prioridade 3 (Média - 2 horas)
9. ✅ Limpar arquivos de teste e temporários
10. ✅ Corrigir warnings de SSL
11. ✅ Documentar qual servidor usar
12. ✅ Adicionar validação de módulos obrigatórios

**Tempo Total Estimado**: 7 horas

---

**Próximo passo**: Iniciar correção dos bugs críticos

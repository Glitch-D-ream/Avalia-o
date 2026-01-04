import os
import json
import logging
from pymetasploit3.msfrpc import MsfRpcClient

logger = logging.getLogger(__name__)

class MetasploitExploit:
    """
    Módulo para automação de exploração com Metasploit Framework.
    Requer que o serviço msfrpcd esteja rodando.
    """
    def __init__(self, host='127.0.0.1', port=55553, user='msf', password='msf'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.client = None
        self.status = "idle"
        self.results = []

    def connect(self):
        """Tenta conectar ao msfrpcd."""
        try:
            # Assumindo que o msfrpcd está rodando com as credenciais padrão
            self.client = MsfRpcClient(self.password, username=self.user, host=self.host, port=self.port)
            self.status = "connected"
            logger.info("Conexão com MsfRpcClient estabelecida.")
            return True
        except Exception as e:
            self.status = "error"
            logger.error(f"Erro ao conectar ao MsfRpcClient: {e}")
            return False

    def run_auxiliary_module(self, module_name, target_host, target_port, options=None):
        """
        Executa um módulo auxiliar (scanner, fuzzer, etc.).
        """
        if not self.client and not self.connect():
            return {"status": "error", "message": "Não foi possível conectar ao Metasploit RPC."}

        self.status = "running"
        self.results = []
        
        try:
            # 1. Carregar o módulo
            auxiliary = self.client.modules.use('auxiliary', module_name)
            
            # 2. Configurar as opções
            auxiliary['RHOSTS'] = target_host
            auxiliary['RPORT'] = target_port
            
            if options:
                for key, value in options.items():
                    auxiliary[key] = value
            
            # 3. Executar
            cid = auxiliary.execute()
            
            # 4. Obter o resultado (pode ser assíncrono, aqui é simplificado)
            # Para módulos auxiliares, o resultado é complexo de extrair via RPC.
            # O ideal é monitorar o console ou o log.
            self.status = "completed"
            return {"status": "success", "job_id": cid, "message": f"Módulo auxiliar {module_name} iniciado. Verifique o console do Metasploit para resultados detalhados."}

        except Exception as e:
            self.status = "error"
            logger.error(f"Erro ao executar o módulo auxiliar: {e}")
            return {"status": "error", "message": str(e)}

    def get_status(self):
        """Retorna o status atual do módulo."""
        return {"status": self.status, "results": self.results}

# Inicializar o módulo (não conectar automaticamente)
metasploit_exploit = MetasploitExploit()

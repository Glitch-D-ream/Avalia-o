import subprocess
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

class SQLMapModule:
    """
    Módulo para automação do SQLMap.
    """
    def __init__(self):
        self.status = "idle"
        self.target = None
        self.results = []
        self.process = None

    async def start_scan(self, target_url: str, forms: bool = True, crawl: int = 2):
        """
        Inicia um scan de SQL Injection com SQLMap.
        Inclui as opções --forms e --crawl=2 por padrão para maior cobertura.
        """
        if self.status == "running":
            return {"status": "error", "message": "Um scan já está em execução."}

        self.target = target_url
        self.status = "running"
        self.results = []

        # Comando base do SQLMap
        command = [
            "sqlmap",
            "-u", target_url,
            "--batch",  # Nunca perguntar ao usuário
            "--random-agent",
            "--dbs", # Tentar listar bancos de dados
            "--output-dir=/tmp/sqlmap_output",
            "--smart"
        ]

        # Adicionar opções de aprimoramento
        if forms:
            command.append("--forms")
        if crawl > 0:
            command.append(f"--crawl={crawl}")

        logger.info(f"Executando SQLMap: {' '.join(command)}")

        try:
            # Executar o SQLMap em um subprocesso
            self.process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Não esperar pelo resultado aqui, apenas iniciar
            asyncio.create_task(self._monitor_scan())
            
            return {"status": "scan_started", "target": self.target}

        except Exception as e:
            self.status = "error"
            logger.error(f"Erro ao iniciar o SQLMap: {e}")
            return {"status": "error", "message": str(e)}

    async def _monitor_scan(self):
        """
        Monitora o subprocesso do SQLMap e armazena a saída.
        """
        stdout, stderr = await self.process.communicate()
        
        output = stdout.decode('utf-8', errors='ignore')
        error_output = stderr.decode('utf-8', errors='ignore')

        if self.process.returncode == 0:
            self.status = "completed"
        else:
            self.status = "error"
            
        self.results.append({
            "output": output,
            "error": error_output,
            "return_code": self.process.returncode
        })
        
        logger.info(f"Scan SQLMap concluído para {self.target}. Status: {self.status}")

    def get_status(self):
        """
        Retorna o status atual do scan.
        """
        return {
            "status": self.status,
            "target": self.target,
            "results_count": len(self.results),
            "last_result": self.results[-1] if self.results else None
        }

# Instanciar o módulo
sqlmap_module = SQLMapModule()

import asyncio
import json
import logging
from theHarvester.theHarvester import main as harvester_main

logger = logging.getLogger(__name__)

class TheHarvesterModule:
    """
    Módulo para automação da ferramenta de OSINT theHarvester.
    """
    def __init__(self):
        self.status = "idle"
        self.results = []

    async def run_scan(self, domain, sources="all"):
        """
        Executa um scan com o theHarvester.
        """
        self.status = "running"
        self.results = []

        try:
            # O theHarvester é uma aplicação de linha de comando, então vamos usar asyncio.create_subprocess_exec
            # para rodá-lo e capturar a saída.
            # A biblioteca do theHarvester não foi feita para ser importada diretamente.
            # A melhor abordagem é usar a linha de comando.

            # Construir o comando
            command = [
                "theHarvester",
                "-d", domain,
                "-b", sources,
                "-f", f"/tmp/harvester_{domain}.json"
            ]

            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                with open(f"/tmp/harvester_{domain}.json", "r") as f:
                    self.results = json.load(f)
                self.status = "completed"
                return {"status": "completed", "results": self.results}
            else:
                self.status = "error"
                logger.error(f"Erro ao executar o theHarvester: {stderr.decode()}")
                return {"status": "error", "message": stderr.decode()}

        except Exception as e:
            self.status = "error"
            logger.error(f"Erro ao executar o theHarvester: {e}")
            return {"status": "error", "message": str(e)}

    def get_status(self):
        """Retorna o status atual do módulo."""
        return {"status": self.status, "results": self.results}

# Inicializar o módulo
theharvester_module = TheHarvesterModule()

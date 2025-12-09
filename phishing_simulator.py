import asyncio
from datetime import datetime
import random

class PhishingSimulator:
    """    Simula um ataque de Phishing/Engenharia Social para demonstrar a coleta de credenciais
    em ambientes seguros (HTTPS).
    """    
    def __init__(self):
        self.status = "IDLE"
        self.target_url = None
        self.captured_credentials = []
        self.start_time = None
        
    def start_attack(self, target_url: str):
        """Inicia a simulação do ataque de Phishing."""
        self.status = "RUNNING"
        self.target_url = target_url
        self.captured_credentials = []
        self.start_time = datetime.now()
        
    async def simulate_credential_capture(self, username: str, password: str, manager):
        """Simula a captura de credenciais e envia o resultado via WebSocket."""
        
        if self.status != "RUNNING":
            return
        
        # Simula o tempo de resposta do servidor de phishing
        await asyncio.sleep(random.uniform(1, 3))
        
        credential_entry = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "password": password,
            "source_ip": "192.168.1.200 (Celular 04)",
            "attack_type": "Phishing/Engenharia Social"
        }
        
        self.captured_credentials.append(credential_entry)
        self.status = "COMPLETED"
        
        # Enviar o resultado da captura para o Dashboard
        await manager.broadcast({
            "type": "phishing_capture",
            "data": credential_entry,
            "message": "Credenciais capturadas com sucesso via Phishing!"
        })
        
        return credential_entry

    def get_status(self):
        """Retorna o status atual do simulador."""
        elapsed_time = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        return {
            "status": self.status,
            "target_url": self.target_url,
            "captured_count": len(self.captured_credentials),
            "elapsed_time_seconds": round(elapsed_time, 2),
            "last_capture": self.captured_credentials[-1] if self.captured_credentials else None
        }

    def reset(self):
        """Reseta o estado do simulador."""
        self.status = "IDLE"
        self.target_url = None
        self.captured_credentials = []
        self.start_time = None

# Exemplo de uso (não será executado, apenas para referência)
# async def main():
#     simulator = PhishingSimulator()
#     simulator.start_attack("https://site-do-concurso.com.br")
#     await simulator.simulate_credential_capture("aluno_vitima", "senha_secreta123", None)
#     print(simulator.get_status())
# 
# if __name__ == "__main__":
#     asyncio.run(main())

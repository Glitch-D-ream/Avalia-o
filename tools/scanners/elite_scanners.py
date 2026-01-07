import subprocess
import json
import logging
import os

logger = logging.getLogger(__name__)

class NucleiEliteScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.output_file = "/tmp/nuclei_results.json"

    def run_scan(self, severity=None):
        """Executa uma varredura Nuclei de elite"""
        logger.info(f"🚀 Iniciando Nuclei Elite Scan em {self.target_url}")
        
        cmd = ["nuclei", "-u", self.target_url, "-json-export", self.output_file, "-silent"]
        if severity:
            cmd.extend(["-severity", severity])
            
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            results = []
            if os.path.exists(self.output_file):
                with open(self.output_file, "r") as f:
                    for line in f:
                        results.append(json.loads(line))
                os.remove(self.output_file)
            
            return results
        except Exception as e:
            logger.error(f"❌ Erro no Nuclei Scan: {e}")
            return []

class HTTPXEliteScanner:
    def __init__(self, target_url):
        self.target_url = target_url

    def probe(self):
        """Realiza sondagem HTTP de elite usando HTTPX"""
        logger.info(f"🔍 Iniciando HTTPX Elite Probe em {self.target_url}")
        
        cmd = ["httpx", "-u", self.target_url, "-title", "-status-code", "-tech-detect", "-follow-redirects", "-json", "-silent"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.stdout:
                return json.loads(result.stdout)
            return {}
        except Exception as e:
            logger.error(f"❌ Erro no HTTPX Probe: {e}")
            return {}

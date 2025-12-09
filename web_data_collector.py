#!/usr/bin/env python3
"""
Web Data Collector - Coleta de Dados Web (OSINT)
Ferramenta educacional para demonstração de coleta de informações públicas
"""

import requests
from requests_html import HTMLSession
import json
from datetime import datetime

class WebDataCollector:
    """Coletor de dados web para fins educacionais"""
    
    def __init__(self):
        self.session = HTMLSession()
        
    def collect_data(self, url):
        """Coleta dados públicos de um site"""
        try:
            response = self.session.get(url, timeout=10)
            
            data = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "status_code": response.status_code,
                "title": response.html.find('title', first=True).text if response.html.find('title', first=True) else "N/A",
                "headers": dict(response.headers),
                "links": [link for link in response.html.absolute_links][:20],  # Limitar a 20 links
                "forms": len(response.html.find('form')),
                "scripts": len(response.html.find('script')),
                "cookies": dict(response.cookies)
            }
            
            return data
            
        except Exception as e:
            return {
                "url": url,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def analyze_security_headers(self, url):
        """Analisa headers de segurança"""
        try:
            response = requests.head(url, timeout=10)
            security_headers = {
                "X-Frame-Options": response.headers.get("X-Frame-Options", "AUSENTE"),
                "X-Content-Type-Options": response.headers.get("X-Content-Type-Options", "AUSENTE"),
                "Strict-Transport-Security": response.headers.get("Strict-Transport-Security", "AUSENTE"),
                "Content-Security-Policy": response.headers.get("Content-Security-Policy", "AUSENTE"),
            }
            return security_headers
        except Exception as e:
            return {"error": str(e)}

def main():
    """Função principal para teste"""
    target_url = "https://example.com"
    
    collector = WebDataCollector()
    results = collector.collect_data(target_url)
    
    print("\n" + "="*80)
    print("📋 RELATÓRIO DE COLETA DE DADOS WEB (OSINT)")
    print("="*80 + "\n")
    print(json.dumps(results, indent=2, default=str))

if __name__ == "__main__":
    main()

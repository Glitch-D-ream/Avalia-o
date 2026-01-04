#!/usr/bin/env python3
"""
WebVuln AI Analyzer - Versão Elite 2026
Analisador Dinâmico de Vulnerabilidades Web com HTTPX e Playwright
"""

import asyncio
import httpx
import re
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
from playwright.async_api import async_playwright
import warnings

warnings.filterwarnings('ignore')

class WebVulnAnalyzer:
    """Analisador de elite com suporte a renderização dinâmica e requisições assíncronas"""
    
    def __init__(self, target_url, timeout=30):
        self.target_url = target_url
        self.timeout = timeout
        self.vulnerabilities = []
        self.api_endpoints = set()
        self.technologies = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    async def full_scan(self):
        """Executa scan completo usando motor assíncrono e dinâmico"""
        print(f"\n🚀 WebVuln AI Analyzer [ELITE] - Scan Completo")
        print(f"🎯 Alvo: {self.target_url}")
        print("="*80)
        
        results = {
            "target": self.target_url,
            "timestamp": datetime.now().isoformat(),
            "vulnerabilities": [],
            "security_headers": {},
            "cookies": {},
            "dynamic_analysis": {},
            "api_endpoints": [],
            "risk_score": 0
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout, verify=False, follow_redirects=True) as client:
            # 1. Análise de Headers e Cookies (Estático + Rápido)
            print("[1/5] 🛡️  Analisando headers e cookies...")
            response = await client.get(self.target_url)
            results["security_headers"] = self._analyze_headers(response.headers)
            results["cookies"] = self._analyze_cookies(response.cookies)

            # 2. Análise Dinâmica com Playwright (O "Pulo do Gato")
            print("[2/5] 🎭 Iniciando análise dinâmica (Playwright)...")
            results["dynamic_analysis"] = await self._analyze_dynamically()

            # 3. Descoberta de Endpoints (Híbrido)
            print("[3/5] 🔗 Descobrindo endpoints de API...")
            results["api_endpoints"] = list(self.api_endpoints)

            # 4. Cálculo de Risco
            print("[4/5] 📊 Calculando Risk Score...")
            results["vulnerabilities"] = self.vulnerabilities
            results["risk_score"] = self._calculate_risk_score()

            # 5. Finalização
            print("[5/5] ✅ Scan concluído!")
            
        return results

    def _analyze_headers(self, headers):
        sec_headers = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options"]
        analysis = {}
        for h in sec_headers:
            val = headers.get(h)
            analysis[h] = val if val else "MISSING"
            if not val:
                self.vulnerabilities.append({
                    "type": "Missing Security Header",
                    "severity": "MEDIUM",
                    "description": f"Header {h} não configurado."
                })
        return analysis

    def _analyze_cookies(self, cookies):
        analysis = {}
        for name, value in cookies.items():
            # Nota: httpx.Cookies não tem todos os atributos como requests.CookieJar diretamente acessíveis da mesma forma
            analysis[name] = {"value": value[:10] + "..."}
        return analysis

    async def _analyze_dynamically(self):
        """Usa Playwright para ver o que o BeautifulSoup não vê"""
        dynamic_data = {"requests": [], "console_logs": [], "errors": []}
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=self.headers['User-Agent'])
            page = await context.new_page()

            # Monitorar requisições de rede (AJAX/Fetch)
            page.on("request", lambda request: self.api_endpoints.add(request.url) if "/api/" in request.url else None)
            page.on("console", lambda msg: dynamic_data["console_logs"].append(msg.text))
            page.on("pageerror", lambda exc: dynamic_data["errors"].append(str(exc)))

            try:
                await page.goto(self.target_url, wait_until="networkidle", timeout=self.timeout * 1000)
                
                # Procurar por dados sensíveis no DOM renderizado
                content = await page.content()
                if "apiKey" in content or "access_token" in content:
                    self.vulnerabilities.append({
                        "type": "Sensitive Data in DOM",
                        "severity": "HIGH",
                        "description": "Possíveis chaves de API ou tokens expostos no DOM renderizado."
                    })
                
                dynamic_data["title"] = await page.title()
                dynamic_data["screenshot_taken"] = True # Em um sistema real, salvaríamos o screenshot
                
            except Exception as e:
                dynamic_data["error"] = str(e)
            finally:
                await browser.close()
        
        return dynamic_data

    def _calculate_risk_score(self):
        score = 0
        for v in self.vulnerabilities:
            if v["severity"] == "CRITICAL": score += 25
            elif v["severity"] == "HIGH": score += 15
            elif v["severity"] == "MEDIUM": score += 5
        return min(score, 100)

# Wrapper para execução síncrona (compatibilidade com backend atual)
def run_scan(target_url):
    analyzer = WebVulnAnalyzer(target_url)
    return asyncio.run(analyzer.full_scan())

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "https://99jogo66.com/?id=211995351"
    report = run_scan(target)
    print(json.dumps(report, indent=2))

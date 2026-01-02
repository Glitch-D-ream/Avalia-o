import asyncio
from playwright.async_api import async_playwright
import json

async def run(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        api_calls = []
        
        # Monitorar todas as requisições de rede
        page.on("request", lambda request: api_calls.append({
            "method": request.method,
            "url": request.url,
            "headers": request.headers
        }))

        print(f"[*] Navegando para {url}...")
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            # Esperar um pouco mais para capturar chamadas assíncronas
            await asyncio.sleep(5)
        except Exception as e:
            print(f"[!] Erro ao navegar: {e}")

        # Filtrar chamadas que parecem ser de API
        api_endpoints = [call for call in api_calls if "api" in call["url"].lower() or call["method"] != "GET"]
        
        with open("api_sniff_results.json", "w") as f:
            json.dump(api_endpoints, f, indent=2)
            
        print(f"[*] Capturadas {len(api_calls)} requisições totais.")
        print(f"[*] Identificados {len(api_endpoints)} possíveis endpoints de API.")
        
        await browser.close()

if __name__ == "__main__":
    target_url = "https://w1-panda.bet/?id=74060664"
    asyncio.run(run(target_url))

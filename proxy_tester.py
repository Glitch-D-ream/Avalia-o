#!/usr/bin/env python3
"""
Script para testar proxies SOCKS4 e encontrar os que estao funcionando.
"""

import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Arquivo com lista de proxies
PROXY_LIST_FILE = "socks_proxies.txt"

# URL de teste (site simples para testar proxy)
TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 5

def test_proxy(proxy_address):
    """Testa um proxy individual"""
    proxy_url = f"socks4://{proxy_address}"
    
    try:
        session = requests.Session()
        session.proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        
        response = session.get(TEST_URL, timeout=TIMEOUT)
        
        if response.status_code == 200:
            return {
                "proxy": proxy_address,
                "status": "OK",
                "response_time": response.elapsed.total_seconds()
            }
        else:
            return {
                "proxy": proxy_address,
                "status": "FAILED",
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "proxy": proxy_address,
            "status": "FAILED",
            "error": str(e)[:50]
        }

def load_proxies():
    """Carrega a lista de proxies do arquivo"""
    try:
        with open(PROXY_LIST_FILE, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies
    except FileNotFoundError:
        print(f"[-] Arquivo {PROXY_LIST_FILE} nao encontrado")
        return []

def test_proxies_parallel(proxies, max_workers=10):
    """Testa multiplos proxies em paralelo"""
    print(f"[*] Testando {len(proxies)} proxies...")
    print(f"[*] Usando {max_workers} workers paralelos...")
    
    working_proxies = []
    failed_proxies = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            
            if result["status"] == "OK":
                working_proxies.append(result)
                print(f"[+] {completed}/{len(proxies)} - {result['proxy']} - OK ({result['response_time']:.2f}s)")
            else:
                failed_proxies.append(result)
                print(f"[-] {completed}/{len(proxies)} - {result['proxy']} - FAILED")
    
    return working_proxies, failed_proxies

def main():
    print("="*80)
    print("TESTADOR DE PROXIES SOCKS4")
    print("="*80)
    
    # Carregar proxies
    proxies = load_proxies()
    
    if not proxies:
        print("[-] Nenhum proxy encontrado para testar")
        return
    
    print(f"\n[*] Carregados {len(proxies)} proxies")
    
    # Testar proxies
    working, failed = test_proxies_parallel(proxies, max_workers=20)
    
    # Exibir resultados
    print(f"\n{'='*80}")
    print(f"[+] Proxies funcionando: {len(working)}")
    print(f"[-] Proxies falhando: {len(failed)}")
    
    if working:
        print("\n[*] Proxies funcionando (ordenados por velocidade):")
        working_sorted = sorted(working, key=lambda x: x['response_time'])
        
        for i, proxy_info in enumerate(working_sorted[:20], 1):
            print(f"    {i}. {proxy_info['proxy']} ({proxy_info['response_time']:.2f}s)")
        
        # Salvar proxies funcionando
        with open("working_proxies.json", "w") as f:
            json.dump(working_sorted, f, indent=2)
        
        print(f"\n[+] Proxies funcionando salvos em 'working_proxies.json'")
        
        # Retornar o melhor proxy
        best_proxy = working_sorted[0]['proxy']
        print(f"\n[+] Melhor proxy: {best_proxy}")
        
        return best_proxy
    else:
        print("\n[-] Nenhum proxy funcionando encontrado")
        return None

if __name__ == "__main__":
    best = main()
    if best:
        print(f"\n[*] Use este proxy: socks4://{best}")

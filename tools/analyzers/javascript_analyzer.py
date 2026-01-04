#!/usr/bin/env python3
"""
Script para analisar JavaScript minificado e encontrar endpoints de API ocultos.
Usa técnicas de engenharia reversa para descobrir a lógica de login/registro.
"""

import requests
import re
import json
import base64
from urllib.parse import urljoin

# Configuração do proxy SOCKS4
PROXY_SOCKS4 = "socks4://177.126.89.63:4145"

# Configuração do site alvo
TARGET_URL = "https://99jogo66.com/?id=211995351"
TARGET_BASE = "https://99jogo66.com"

def create_session():
    """Cria uma sessão requests com proxy SOCKS4"""
    session = requests.Session()
    session.proxies = {
        "http": PROXY_SOCKS4,
        "https": PROXY_SOCKS4
    }
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    return session

def extract_javascript_urls(html_content):
    """Extrai URLs de arquivos JavaScript do HTML"""
    print("[*] Extraindo URLs de JavaScript...")
    
    # Procurar por <script src="...">
    script_pattern = r'<script[^>]*src=["\']([^"\']+)["\']'
    urls = re.findall(script_pattern, html_content, re.IGNORECASE)
    
    # Converter URLs relativas em absolutas
    absolute_urls = []
    for url in urls:
        if url.startswith('http'):
            absolute_urls.append(url)
        else:
            absolute_urls.append(urljoin(TARGET_BASE, url))
    
    print(f"[+] Encontradas {len(absolute_urls)} URLs de JavaScript")
    return absolute_urls

def download_javascript(url, session):
    """Baixa um arquivo JavaScript"""
    try:
        response = session.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"[-] Erro ao baixar {url}: {e}")
    return None

def analyze_javascript(js_content):
    """Analisa JavaScript para encontrar endpoints e payloads"""
    print("[*] Analisando JavaScript...")
    
    findings = {
        "endpoints": [],
        "api_calls": [],
        "auth_functions": [],
        "keywords": []
    }
    
    # Procurar por endpoints de API
    endpoint_patterns = [
        r'["\'](/api/[^"\']+)["\']',
        r'["\'](/[^"\']*login[^"\']*)["\']',
        r'["\'](/[^"\']*register[^"\']*)["\']',
        r'["\'](/[^"\']*auth[^"\']*)["\']',
        r'["\'](/[^"\']*user[^"\']*)["\']',
        r'fetch\(["\']([^"\']+)["\']',
        r'axios\.[a-z]+\(["\']([^"\']+)["\']',
    ]
    
    for pattern in endpoint_patterns:
        matches = re.findall(pattern, js_content, re.IGNORECASE)
        findings["endpoints"].extend(matches)
    
    # Procurar por chamadas de API
    api_patterns = [
        r'fetch\s*\(\s*["\']([^"\']+)["\']',
        r'axios\.[a-z]+\s*\(\s*["\']([^"\']+)["\']',
        r'XMLHttpRequest|fetch|axios',
    ]
    
    for pattern in api_patterns:
        if re.search(pattern, js_content, re.IGNORECASE):
            findings["api_calls"].append(pattern)
    
    # Procurar por funções de autenticação
    auth_patterns = [
        r'function\s+(\w*login\w*)\s*\(',
        r'function\s+(\w*register\w*)\s*\(',
        r'function\s+(\w*auth\w*)\s*\(',
        r'const\s+(\w*login\w*)\s*=',
        r'const\s+(\w*register\w*)\s*=',
    ]
    
    for pattern in auth_patterns:
        matches = re.findall(pattern, js_content, re.IGNORECASE)
        findings["auth_functions"].extend(matches)
    
    # Procurar por palavras-chave importantes
    keywords = [
        "password", "account", "username", "email", "phone",
        "token", "jwt", "bearer", "authorization",
        "login", "register", "auth", "signin", "signup"
    ]
    
    for keyword in keywords:
        if keyword in js_content.lower():
            findings["keywords"].append(keyword)
    
    # Remover duplicatas
    findings["endpoints"] = list(set(findings["endpoints"]))
    findings["auth_functions"] = list(set(findings["auth_functions"]))
    findings["keywords"] = list(set(findings["keywords"]))
    
    return findings

def beautify_javascript(js_content):
    """Tenta deixar o JavaScript mais legível"""
    print("[*] Tentando embelezar JavaScript...")
    
    # Adicionar quebras de linha após pontos e vírgulas
    js_content = re.sub(r';(?![\n\s])', ';\n', js_content)
    
    # Adicionar quebras de linha após chaves
    js_content = re.sub(r'\}(?![\n\s])', '}\n', js_content)
    
    # Adicionar quebras de linha após parênteses
    js_content = re.sub(r'\)(?![\n\s;,])', ')\n', js_content)
    
    return js_content

def main():
    print("="*80)
    print("ANALISADOR DE JAVASCRIPT - ENGENHARIA REVERSA")
    print("="*80)
    
    session = create_session()
    
    # Baixar HTML da página
    print(f"\n[*] Baixando HTML de {TARGET_URL}...")
    try:
        response = session.get(TARGET_URL, timeout=10, verify=False)
        html_content = response.text
        print("[+] HTML baixado com sucesso!")
    except Exception as e:
        print(f"[-] Erro ao baixar HTML: {e}")
        return
    
    # Extrair URLs de JavaScript
    js_urls = extract_javascript_urls(html_content)
    
    # Analisar cada arquivo JavaScript
    all_findings = {
        "endpoints": [],
        "api_calls": [],
        "auth_functions": [],
        "keywords": []
    }
    
    for i, js_url in enumerate(js_urls[:5], 1):  # Analisar apenas os primeiros 5
        print(f"\n[*] Analisando JavaScript {i}/{min(5, len(js_urls))}: {js_url}")
        
        js_content = download_javascript(js_url, session)
        
        if js_content:
            print(f"[+] Tamanho: {len(js_content)} bytes")
            
            # Analisar
            findings = analyze_javascript(js_content)
            
            # Mesclar resultados
            for key in all_findings:
                all_findings[key].extend(findings[key])
            
            # Exibir achados
            if findings["endpoints"]:
                print(f"[+] Endpoints encontrados: {findings['endpoints'][:5]}")
            if findings["auth_functions"]:
                print(f"[+] Funções de auth: {findings['auth_functions'][:5]}")
    
    # Remover duplicatas
    for key in all_findings:
        all_findings[key] = list(set(all_findings[key]))
    
    # Salvar resultados
    with open("javascript_analysis.json", "w") as f:
        json.dump(all_findings, f, indent=2)
    
    print(f"\n[+] Análise completa!")
    print(f"[+] Endpoints únicos encontrados: {len(all_findings['endpoints'])}")
    print(f"[+] Funções de autenticação: {len(all_findings['auth_functions'])}")
    print(f"[+] Palavras-chave: {len(all_findings['keywords'])}")
    
    print(f"\n[*] Resultados salvos em 'javascript_analysis.json'")
    
    # Exibir endpoints encontrados
    if all_findings["endpoints"]:
        print("\n[*] Endpoints encontrados:")
        for endpoint in sorted(set(all_findings["endpoints"]))[:20]:
            if endpoint.startswith('/'):
                print(f"    - {endpoint}")

if __name__ == "__main__":
    main()

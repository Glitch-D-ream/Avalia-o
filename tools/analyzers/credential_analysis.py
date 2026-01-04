#!/usr/bin/env python3
"""MÓDULO DE ANÁLISE DE CREDENCIAIS
Demonstração Educacional de Hashing, Salting e Força de Senha
"""
import hashlib
import secrets
import string
import time
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class PasswordStrength:
    """Análise de força de senha"""
    password: str
    length: int
    has_uppercase: bool
    has_lowercase: bool
    has_digits: bool
    has_special: bool
    strength_score: int  # 0-100
    strength_level: str  # FRACA, MÉDIA, FORTE, MUITO_FORTE
    estimated_crack_time: str
    recommendations: List[str]

@dataclass
class HashComparison:
    """Comparação de diferentes algoritmos de hashing"""
    password: str
    md5_hash: str
    sha1_hash: str
    sha256_hash: str
    bcrypt_hash: str
    pbkdf2_hash: str
    crack_difficulty: Dict[str, str]

# ============================================================================
# ANALISADOR DE FORÇA DE SENHA
# ============================================================================

class PasswordStrengthAnalyzer:
    """Analisa a força de uma senha"""
    
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    @staticmethod
    def analyze(password: str) -> PasswordStrength:
        """Analisa a força de uma senha"""
        
        length = len(password)
        has_uppercase = any(c.isupper() for c in password)
        has_lowercase = any(c.islower() for c in password)
        has_digits = any(c.isdigit() for c in password)
        has_special = any(c in PasswordStrengthAnalyzer.SPECIAL_CHARS for c in password)
        
        # Calcular score
        score = 0
        
        # Comprimento (máx 30 pontos)
        if length >= 8:
            score += 10
        if length >= 12:
            score += 10
        if length >= 16:
            score += 10
        
        # Complexidade (máx 70 pontos)
        if has_uppercase:
            score += 15
        if has_lowercase:
            score += 15
        if has_digits:
            score += 20
        if has_special:
            score += 20
        
        # Penalidades
        if password.lower() in ["password", "admin", "123456", "qwerty"]:
            score = max(0, score - 50)
        
        # Determinar nível
        if score < 30:
            strength_level = "FRACA"
        elif score < 50:
            strength_level = "MÉDIA"
        elif score < 75:
            strength_level = "FORTE"
        else:
            strength_level = "MUITO_FORTE"
        
        # Estimar tempo de crack
        estimated_crack_time = PasswordStrengthAnalyzer._estimate_crack_time(
            length, has_uppercase, has_lowercase, has_digits, has_special
        )
        
        # Recomendações
        recommendations = []
        if length < 12:
            recommendations.append("Aumente o comprimento da senha para 12+ caracteres")
        if not has_uppercase:
            recommendations.append("Inclua letras maiúsculas")
        if not has_lowercase:
            recommendations.append("Inclua letras minúsculas")
        if not has_digits:
            recommendations.append("Inclua números")
        if not has_special:
            recommendations.append("Inclua caracteres especiais (!@#$%^&*)")
        
        if not recommendations:
            recommendations.append("Senha muito forte! Mantenha-a segura.")
        
        return PasswordStrength(
            password=password,
            length=length,
            has_uppercase=has_uppercase,
            has_lowercase=has_lowercase,
            has_digits=has_digits,
            has_special=has_special,
            strength_score=min(100, score),
            strength_level=strength_level,
            estimated_crack_time=estimated_crack_time,
            recommendations=recommendations
        )
    
    @staticmethod
    def _estimate_crack_time(
        length: int,
        has_uppercase: bool,
        has_lowercase: bool,
        has_digits: bool,
        has_special: bool
    ) -> str:
        """Estima o tempo para quebrar uma senha via força bruta"""
        
        # Calcular espaço de caracteres
        charset_size = 0
        if has_lowercase:
            charset_size += 26
        if has_uppercase:
            charset_size += 26
        if has_digits:
            charset_size += 10
        if has_special:
            charset_size += len(PasswordStrengthAnalyzer.SPECIAL_CHARS)
        
        if charset_size == 0:
            return "Impossível"
        
        # Calcular número de combinações possíveis
        total_combinations = charset_size ** length
        
        # Assumir 1 bilhão de tentativas por segundo (GPU moderna)
        attempts_per_second = 1e9
        seconds_needed = total_combinations / (2 * attempts_per_second)  # Média = metade
        
        # Converter para unidade de tempo apropriada
        if seconds_needed < 1:
            return "< 1 segundo"
        elif seconds_needed < 60:
            return f"{int(seconds_needed)} segundos"
        elif seconds_needed < 3600:
            minutes = seconds_needed / 60
            return f"{minutes:.1f} minutos"
        elif seconds_needed < 86400:
            hours = seconds_needed / 3600
            return f"{hours:.1f} horas"
        elif seconds_needed < 31536000:
            days = seconds_needed / 86400
            return f"{days:.1f} dias"
        else:
            years = seconds_needed / 31536000
            return f"{years:.1f} anos"

# ============================================================================
# COMPARADOR DE ALGORITMOS DE HASHING
# ============================================================================

class HashingAlgorithmComparator:
    """Compara diferentes algoritmos de hashing"""
    
    @staticmethod
    def compare_algorithms(password: str) -> HashComparison:
        """Compara diferentes algoritmos de hashing para uma senha"""
        
        # MD5 (INSEGURO - apenas para educação)
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        
        # SHA1 (INSEGURO - apenas para educação)
        sha1_hash = hashlib.sha1(password.encode()).hexdigest()
        
        # SHA256 (SEGURO)
        sha256_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # PBKDF2 (SEGURO - com salt)
        salt = secrets.token_hex(16)
        pbkdf2_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000  # iterações
        ).hex()
        
        # Bcrypt (MUITO SEGURO - com salt e custo)
        try:
            import bcrypt
            bcrypt_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()
        except ImportError:
            bcrypt_hash = "Bcrypt não instalado"
        
        # Análise de dificuldade de crack
        crack_difficulty = {
            "MD5": "Segundos (Tabelas Rainbow disponíveis)",
            "SHA1": "Minutos (Vulnerável a colisões)",
            "SHA256": "Horas (Sem salt)",
            "PBKDF2": "Semanas (Com salt e iterações)",
            "Bcrypt": "Meses/Anos (Com salt e custo adaptativo)"
        }
        
        return HashComparison(
            password=password,
            md5_hash=md5_hash,
            sha1_hash=sha1_hash,
            sha256_hash=sha256_hash,
            bcrypt_hash=bcrypt_hash,
            pbkdf2_hash=pbkdf2_hash,
            crack_difficulty=crack_difficulty
        )

# ============================================================================
# SIMULADOR DE QUEBRA DE HASH
# ============================================================================

class HashCrackSimulator:
    """Simula a quebra de hashes usando dicionário"""
    
    COMMON_PASSWORDS = [
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "1234567", "letmein", "trustno1", "dragon",
        "baseball", "111111", "iloveyou", "master", "sunshine",
        "ashley", "bailey", "passw0rd", "shadow", "123123"
    ]
    
    @staticmethod
    async def crack_hash(
        hash_value: str,
        algorithm: str,
        dictionary: List[str] = None,
        max_attempts: int = 1000
    ) -> Tuple[bool, str, int]:
        """
        Simula a tentativa de quebra de um hash
        
        Args:
            hash_value: Hash a quebrar
            algorithm: Algoritmo usado (md5, sha1, sha256, etc.)
            dictionary: Dicionário de senhas (padrão: senhas comuns)
            max_attempts: Número máximo de tentativas
        
        Returns:
            (encontrado, senha, número_de_tentativas)
        """
        
        if dictionary is None:
            dictionary = HashCrackSimulator.COMMON_PASSWORDS
        
        for attempt, password in enumerate(dictionary[:max_attempts]):
            # Calcular hash da senha testada
            if algorithm.lower() == "md5":
                test_hash = hashlib.md5(password.encode()).hexdigest()
            elif algorithm.lower() == "sha1":
                test_hash = hashlib.sha1(password.encode()).hexdigest()
            elif algorithm.lower() == "sha256":
                test_hash = hashlib.sha256(password.encode()).hexdigest()
            else:
                continue
            
            # Comparar
            if test_hash == hash_value:
                return (True, password, attempt + 1)
            
            # Simular delay
            await asyncio.sleep(0.01)
        
        return (False, "", len(dictionary[:max_attempts]))

# ============================================================================
# GERADOR DE SENHAS SEGURAS
# ============================================================================

class SecurePasswordGenerator:
    """Gera senhas seguras"""
    
    @staticmethod
    def generate(
        length: int = 16,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_special: bool = True
    ) -> str:
        """Gera uma senha segura"""
        
        charset = ""
        
        if include_lowercase:
            charset += string.ascii_lowercase
        if include_uppercase:
            charset += string.ascii_uppercase
        if include_digits:
            charset += string.digits
        if include_special:
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not charset:
            raise ValueError("Pelo menos um tipo de caractere deve ser incluído")
        
        password = ''.join(secrets.choice(charset) for _ in range(length))
        return password
    
    @staticmethod
    def generate_passphrase(word_count: int = 4) -> str:
        """Gera uma frase de senha (passphrase) memorável"""
        
        # Dicionário simples de palavras
        words = [
            "gato", "cachorro", "casa", "árvore", "montanha",
            "rio", "sol", "lua", "estrela", "nuvem",
            "flor", "pássaro", "peixe", "livro", "música",
            "dança", "arte", "ciência", "tecnologia", "segurança"
        ]
        
        selected_words = [secrets.choice(words) for _ in range(word_count)]
        passphrase = "-".join(selected_words)
        
        return passphrase

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

async def main():
    print("""    🔐 ANÁLISE DE CREDENCIAIS 🔐
    Demonstração Educacional de Hashing e Força de Senha
    =====================================================
    """
    
    # Analisar força de senhas
    test_passwords = [
        "admin",
        "Password123",
        "Tr0pic@lThund3r!2024",
        "MySecurePass#2024!"
    ]
    
    print("\n📊 ANÁLISE DE FORÇA DE SENHA
")
    
    for pwd in test_passwords:
        analysis = PasswordStrengthAnalyzer.analyze(pwd)
        print(f"Senha: {pwd}")
        print(f"  Força: {analysis.strength_level} ({analysis.strength_score}/100)")
        print(f"  Tempo Estimado para Crack: {analysis.estimated_crack_time}")
        print(f"  Recomendações: {', '.join(analysis.recommendations)}
")
    
    # Comparar algoritmos de hashing
    print("\n🔒 COMPARAÇÃO DE ALGORITMOS DE HASHING
")
    
    password = "Seguranca123!"
    comparison = HashingAlgorithmComparator.compare_algorithms(password)
    
    print(f"Senha: {password}
")
    print(f"MD5:     {comparison.md5_hash}")
    print(f"SHA1:    {comparison.sha1_hash}")
    print(f"SHA256:  {comparison.sha256_hash}")
    print(f"PBKDF2:  {comparison.pbkdf2_hash}")
    print(f"Bcrypt:  {comparison.bcrypt_hash}
")
    
    print("Dificuldade de Crack:")
    for algo, difficulty in comparison.crack_difficulty.items():
        print(f"  {algo}: {difficulty}")
    
    # Gerar senhas seguras
    print("\n🎲 GERADOR DE SENHAS SEGURAS
")
    
    secure_pwd = SecurePasswordGenerator.generate(16)
    print(f"Senha Aleatória Segura: {secure_pwd}")
    
    passphrase = SecurePasswordGenerator.generate_passphrase(4)
    print(f"Passphrase Memorável: {passphrase}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

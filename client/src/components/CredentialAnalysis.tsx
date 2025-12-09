import React, { useState } from 'react';
import { Lock, Key, AlertCircle, CheckCircle } from 'lucide-react';

interface PasswordAnalysis {
  password: string;
  length: number;
  has_uppercase: boolean;
  has_lowercase: boolean;
  has_digits: boolean;
  has_special: boolean;
  strength_score: number;
  strength_level: string;
  estimated_crack_time: string;
  recommendations: string[];
}

interface HashComparison {
  password: string;
  md5_hash: string;
  sha1_hash: string;
  sha256_hash: string;
  bcrypt_hash: string;
  pbkdf2_hash: string;
  crack_difficulty: Record<string, string>;
}

export const CredentialAnalysis: React.FC = () => {
  const [password, setPassword] = useState('');
  const [analysis, setAnalysis] = useState<PasswordAnalysis | null>(null);
  const [hashComparison, setHashComparison] = useState<HashComparison | null>(null);
  const [generatedPassword, setGeneratedPassword] = useState('');
  const [generatedPassphrase, setGeneratedPassphrase] = useState('');

  const analyzePassword = async () => {
    if (!password) return;
    
    try {
      const response = await fetch('/api/credentials/analyze-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      });
      
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error('Erro ao analisar senha:', error);
    }
  };

  const compareHashes = async () => {
    if (!password) return;
    
    try {
      const response = await fetch('/api/credentials/compare-hashes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      });
      
      const data = await response.json();
      setHashComparison(data);
    } catch (error) {
      console.error('Erro ao comparar hashes:', error);
    }
  };

  const generatePassword = async () => {
    try {
      const response = await fetch('/api/credentials/generate-password?length=16', {
        method: 'POST'
      });
      
      const data = await response.json();
      setGeneratedPassword(data.password);
    } catch (error) {
      console.error('Erro ao gerar senha:', error);
    }
  };

  const generatePassphrase = async () => {
    try {
      const response = await fetch('/api/credentials/generate-passphrase?word_count=4', {
        method: 'POST'
      });
      
      const data = await response.json();
      setGeneratedPassphrase(data.passphrase);
    } catch (error) {
      console.error('Erro ao gerar passphrase:', error);
    }
  };

  const getStrengthColor = (level: string) => {
    switch (level) {
      case 'MUITO_FORTE':
        return 'bg-green-100 border-green-500 text-green-700';
      case 'FORTE':
        return 'bg-blue-100 border-blue-500 text-blue-700';
      case 'MÉDIA':
        return 'bg-yellow-100 border-yellow-500 text-yellow-700';
      case 'FRACA':
        return 'bg-red-100 border-red-500 text-red-700';
      default:
        return 'bg-gray-100 border-gray-500 text-gray-700';
    }
  };

  const getStrengthIcon = (level: string) => {
    switch (level) {
      case 'MUITO_FORTE':
        return '🔐';
      case 'FORTE':
        return '🔒';
      case 'MÉDIA':
        return '🔓';
      case 'FRACA':
        return '🔑';
      default:
        return '❓';
    }
  };

  return (
    <div className="w-full space-y-6 p-6 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 rounded-lg">
      {/* Cabeçalho */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Lock className="w-8 h-8 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">🔐 Análise de Credenciais</h2>
        </div>
      </div>

      {/* Input de Senha */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">Analisar Força de Senha</h3>
        <div className="flex gap-3 mb-4">
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Digite uma senha para analisar..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <button
            onClick={analyzePassword}
            className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Analisar
          </button>
          <button
            onClick={compareHashes}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Comparar Hashes
          </button>
        </div>
      </div>

      {/* Análise de Força */}
      {analysis && (
        <div className={`border-l-4 p-6 rounded-lg ${getStrengthColor(analysis.strength_level)}`}>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-2xl font-bold">{getStrengthIcon(analysis.strength_level)} {analysis.strength_level}</p>
              <p className="text-sm mt-1">Score: {analysis.strength_score}/100</p>
            </div>
            <div className="text-right">
              <p className="text-sm font-semibold">Tempo Estimado para Crack</p>
              <p className="text-lg font-bold">{analysis.estimated_crack_time}</p>
            </div>
          </div>

          {/* Características */}
          <div className="grid grid-cols-2 gap-3 mb-4">
            <div className={`p-2 rounded ${analysis.has_uppercase ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {analysis.has_uppercase ? '✓' : '✗'} Maiúsculas
            </div>
            <div className={`p-2 rounded ${analysis.has_lowercase ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {analysis.has_lowercase ? '✓' : '✗'} Minúsculas
            </div>
            <div className={`p-2 rounded ${analysis.has_digits ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {analysis.has_digits ? '✓' : '✗'} Números
            </div>
            <div className={`p-2 rounded ${analysis.has_special ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {analysis.has_special ? '✓' : '✗'} Caracteres Especiais
            </div>
          </div>

          {/* Recomendações */}
          <div className="bg-black bg-opacity-10 p-4 rounded">
            <p className="font-semibold mb-2">Recomendações:</p>
            <ul className="space-y-1 text-sm">
              {analysis.recommendations.map((rec, idx) => (
                <li key={idx}>• {rec}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Comparação de Hashes */}
      {hashComparison && (
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">🔒 Comparação de Algoritmos de Hashing</h3>
          
          <div className="space-y-4">
            {Object.entries(hashComparison.crack_difficulty).map(([algo, difficulty]) => (
              <div key={algo} className="border-l-4 border-gray-300 pl-4 py-2">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-semibold text-gray-800">{algo}</p>
                  <span className="text-xs bg-gray-100 px-2 py-1 rounded">{difficulty}</span>
                </div>
                
                {/* Mostrar hash (truncado) */}
                <div className="bg-gray-50 p-2 rounded text-xs font-mono break-all">
                  {algo === 'MD5' && hashComparison.md5_hash.substring(0, 50)}...
                  {algo === 'SHA1' && hashComparison.sha1_hash.substring(0, 50)}...
                  {algo === 'SHA256' && hashComparison.sha256_hash.substring(0, 50)}...
                  {algo === 'PBKDF2' && hashComparison.pbkdf2_hash.substring(0, 50)}...
                  {algo === 'Bcrypt' && hashComparison.bcrypt_hash.substring(0, 50)}...
                </div>
              </div>
            ))}
          </div>

          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded mt-4">
            <p className="text-sm text-red-700">
              <strong>⚠️ Aviso:</strong> MD5 e SHA1 são inseguros e não devem ser usados para senhas. Use bcrypt ou PBKDF2 com salt.
            </p>
          </div>
        </div>
      )}

      {/* Gerador de Senhas */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">🎲 Gerador de Senhas Seguras</h3>
        
        <div className="space-y-4">
          <div>
            <button
              onClick={generatePassword}
              className="w-full px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 mb-2"
            >
              Gerar Senha Aleatória (16 caracteres)
            </button>
            {generatedPassword && (
              <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                <p className="text-sm text-gray-600 mb-2">Senha Gerada:</p>
                <p className="font-mono text-lg font-bold text-green-700 break-all">{generatedPassword}</p>
                <button
                  onClick={() => navigator.clipboard.writeText(generatedPassword)}
                  className="text-sm text-green-600 hover:text-green-700 mt-2"
                >
                  📋 Copiar para Área de Transferência
                </button>
              </div>
            )}
          </div>

          <div>
            <button
              onClick={generatePassphrase}
              className="w-full px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 mb-2"
            >
              Gerar Passphrase Memorável (4 palavras)
            </button>
            {generatedPassphrase && (
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                <p className="text-sm text-gray-600 mb-2">Passphrase Gerada:</p>
                <p className="font-mono text-lg font-bold text-blue-700 break-all">{generatedPassphrase}</p>
                <button
                  onClick={() => navigator.clipboard.writeText(generatedPassphrase)}
                  className="text-sm text-blue-600 hover:text-blue-700 mt-2"
                >
                  📋 Copiar para Área de Transferência
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Dicas de Segurança */}
      <div className="bg-purple-50 border-l-4 border-purple-500 p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-3 text-purple-700">💡 Dicas de Segurança de Credenciais</h3>
        <ul className="text-sm text-purple-600 space-y-2">
          <li>✓ Use senhas com 12+ caracteres</li>
          <li>✓ Combine maiúsculas, minúsculas, números e símbolos</li>
          <li>✓ Nunca reutilize senhas em diferentes contas</li>
          <li>✓ Use um gerenciador de senhas para armazenar com segurança</li>
          <li>✓ Ative autenticação de dois fatores (2FA) quando possível</li>
          <li>✓ Altere senhas regularmente (a cada 90 dias)</li>
          <li>✓ Não compartilhe senhas por email ou mensagens</li>
          <li>✓ Use bcrypt ou PBKDF2 para armazenar senhas (nunca MD5/SHA1)</li>
        </ul>
      </div>
    </div>
  );
};

export default CredentialAnalysis;

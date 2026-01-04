import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

interface WiFiAnalysis {
  ssid: string;
  bssid: string;
  encryption: string;
  security_level: string;
  description: string;
  estimated_crack_time: string;
  signal_strength: number;
  vulnerabilities: any[];
  recommendation: string;
}

export const WiFiSecurityAnalysis: React.FC = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isCapturing, setIsCapturing] = useState(false);
  const [analysis, setAnalysis] = useState<WiFiAnalysis | null>(null);
  const [handshakeData, setHandshakeData] = useState<any>(null);

  const startWiFiAnalysis = async () => {
    setIsAnalyzing(true);
    
    try {
      const response = await fetch('/api/wifi/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error('Erro ao analisar WiFi:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const captureHandshake = async () => {
    setIsCapturing(true);
    
    try {
      const response = await fetch('/api/wifi/capture-handshake', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      const data = await response.json();
      setHandshakeData(data);
    } catch (error) {
      console.error('Erro ao capturar handshake:', error);
    } finally {
      setIsCapturing(false);
    }
  };

  const getSecurityColor = (level: string) => {
    switch (level) {
      case 'EXCELENTE':
        return 'bg-green-100 border-green-500 text-green-700';
      case 'BOM':
        return 'bg-blue-100 border-blue-500 text-blue-700';
      case 'MÉDIO':
        return 'bg-yellow-100 border-yellow-500 text-yellow-700';
      case 'CRÍTICO':
        return 'bg-red-100 border-red-500 text-red-700';
      default:
        return 'bg-gray-100 border-gray-500 text-gray-700';
    }
  };

  // Dados de comparação de encriptações
  const encryptionComparison = [
    { encryption: 'WEP', crack_time: '< 1 min', security: 'CRÍTICO' },
    { encryption: 'WPA', crack_time: 'Minutos-Horas', security: 'MÉDIO' },
    { encryption: 'WPA2', crack_time: 'Dias-Semanas', security: 'BOM' },
    { encryption: 'WPA3', crack_time: 'Impraticável', security: 'EXCELENTE' }
  ];

  // Dados de tempo de crack (simulado)
  const crackTimeData = [
    { password: 'admin', time_seconds: 0.5 },
    { password: 'Senha123', time_seconds: 45 },
    { password: 'Tr0pic@lThund3r!', time_seconds: 86400 },
    { password: 'Quantum#Security2024', time_seconds: 604800 }
  ];

  return (
    <div className="w-full space-y-6 p-6 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 rounded-lg">
      {/* Cabeçalho */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-white">📡 Análise de Segurança WiFi</h2>
        <div className="space-x-4">
          <button
            onClick={startWiFiAnalysis}
            disabled={isAnalyzing}
            className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
          >
            {isAnalyzing ? '⏳ Analisando...' : '🔍 Analisar WiFi'}
          </button>
          <button
            onClick={captureHandshake}
            disabled={isCapturing}
            className="px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50"
          >
            {isCapturing ? '⏳ Capturando...' : '📥 Capturar Handshake'}
          </button>
        </div>
      </div>

      {/* Análise de WiFi */}
      {analysis && (
        <>
          {/* Card de Segurança */}
          <div className={`p-6 rounded-lg border-l-4 ${getSecurityColor(analysis.security_level)}`}>
            <div className="flex justify-between items-start mb-4">
              <div>
                <p className="text-sm font-semibold opacity-75">Rede WiFi</p>
                <p className="text-2xl font-bold">{analysis.ssid}</p>
                <p className="text-sm mt-2">BSSID: {analysis.bssid}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold opacity-75">Nível de Segurança</p>
                <p className="text-3xl font-bold">{analysis.security_level}</p>
                <p className="text-sm mt-2">Encriptação: {analysis.encryption}</p>
              </div>
            </div>
            <p className="text-sm mt-4">{analysis.description}</p>
            <p className="text-sm mt-2"><strong>Tempo Estimado para Quebra:</strong> {analysis.estimated_crack_time}</p>
            <p className="text-sm mt-2"><strong>Recomendação:</strong> {analysis.recommendation}</p>
          </div>

          {/* Vulnerabilidades */}
          {analysis.vulnerabilities.length > 0 && (
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-lg font-semibold mb-4 text-gray-800">⚠️ Vulnerabilidades Detectadas</h3>
              <div className="space-y-3">
                {analysis.vulnerabilities.map((vuln, idx) => (
                  <div key={idx} className="border-l-4 border-red-500 bg-red-50 p-4 rounded">
                    <p className="font-semibold text-gray-800">{vuln.description}</p>
                    <p className="text-sm text-gray-700 mt-2"><strong>Remediação:</strong> {vuln.remediation}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {/* Comparação de Encriptações */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">📊 Comparação de Encriptações WiFi</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Encriptação</th>
                <th className="px-4 py-2 text-left">Tempo para Quebra</th>
                <th className="px-4 py-2 text-left">Nível de Segurança</th>
                <th className="px-4 py-2 text-left">Status</th>
              </tr>
            </thead>
            <tbody>
              {encryptionComparison.map((enc) => (
                <tr key={enc.encryption} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-2 font-semibold">{enc.encryption}</td>
                  <td className="px-4 py-2">{enc.crack_time}</td>
                  <td className="px-4 py-2">{enc.security}</td>
                  <td className="px-4 py-2">
                    {enc.security === 'EXCELENTE' && '✅ Recomendado'}
                    {enc.security === 'BOM' && '⚠️ Aceitável'}
                    {enc.security === 'MÉDIO' && '❌ Fraco'}
                    {enc.security === 'CRÍTICO' && '🚨 Obsoleto'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Gráfico de Tempo de Crack por Força de Senha */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">⏱️ Tempo de Crack por Força de Senha</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={crackTimeData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="password" />
            <YAxis label={{ value: 'Tempo (segundos)', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              formatter={(value) => {
                if (value > 86400) return '> 1 dia';
                if (value > 3600) return `${(value / 3600).toFixed(1)}h`;
                if (value > 60) return `${(value / 60).toFixed(1)}m`;
                return `${value}s`;
              }}
            />
            <Bar dataKey="time_seconds" fill="#ef4444" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Dados de Handshake Capturado */}
      {handshakeData && (
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">📥 Handshake Capturado</h3>
          <div className="space-y-3">
            <div className="bg-gray-50 p-4 rounded">
              <p className="text-sm"><strong>SSID:</strong> {handshakeData.ssid}</p>
              <p className="text-sm"><strong>BSSID:</strong> {handshakeData.bssid}</p>
              <p className="text-sm"><strong>Timestamp:</strong> {handshakeData.timestamp}</p>
              <p className="text-sm"><strong>Status:</strong> {handshakeData.is_complete ? '✅ Completo' : '⏳ Incompleto'}</p>
              <p className="text-sm"><strong>Dificuldade de Crack:</strong> {handshakeData.crack_difficulty}</p>
            </div>
            <div className="bg-blue-50 p-4 rounded border-l-4 border-blue-500">
              <p className="text-sm font-semibold text-blue-700">💡 Informação Educacional</p>
              <p className="text-sm text-blue-600 mt-2">
                O handshake capturado contém dados criptografados que podem ser usados para tentar quebrar a senha via força bruta. 
                Quanto mais forte a senha, mais tempo levará para quebrá-la.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Recomendações de Segurança */}
      <div className="bg-green-50 border-l-4 border-green-500 p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-4 text-green-700">✅ Recomendações de Segurança WiFi</h3>
        <ul className="space-y-2 text-sm text-green-700">
          <li>✓ Use WPA3 como padrão de encriptação</li>
          <li>✓ Crie uma senha com 12+ caracteres</li>
          <li>✓ Combine maiúsculas, minúsculas, números e símbolos</li>
          <li>✓ Altere a senha padrão do roteador</li>
          <li>✓ Desabilite WPS (WiFi Protected Setup)</li>
          <li>✓ Atualize o firmware do roteador regularmente</li>
          <li>✓ Oculte o SSID (opcional, segurança por obscuridade)</li>
          <li>✓ Implemente filtro de MAC address</li>
        </ul>
      </div>
    </div>
  );
};

export default WiFiSecurityAnalysis;

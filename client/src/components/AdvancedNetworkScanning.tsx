import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface Port {
  port_number: number;
  protocol: string;
  state: string;
  service: string;
  vulnerability: string;
}

interface ScanResult {
  target_ip: string;
  hostname: string;
  status: string;
  ports: Port[];
  os_detection: string;
  timestamp: string;
}

interface Vulnerability {
  id: number;
  severity: string;
  title: string;
  description: string;
  affected_device: string;
  port: number;
  remediation: string;
}

export const AdvancedNetworkScanning: React.FC = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [scanResults, setScanResults] = useState<ScanResult[]>([]);
  const [vulnerabilities, setVulnerabilities] = useState<Vulnerability[]>([]);
  const [riskScore, setRiskScore] = useState(0);

  const startAdvancedScan = async () => {
    setIsScanning(true);
    
    try {
      const response = await fetch('/api/scan/network/advanced', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      const data = await response.json();
      
      // Converter para formato compatível com visualização
      const results = data.scan_results.map((result: any) => ({
        ...result,
        ports: result.ports || []
      }));
      
      setScanResults(results);
      setVulnerabilities(data.analysis.vulnerabilities || []);
      setRiskScore(data.analysis.risk_score || 0);
    } catch (error) {
      console.error('Erro ao executar escaneamento:', error);
    } finally {
      setIsScanning(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRÍTICO':
        return '#dc2626';
      case 'ALTO':
        return '#ea580c';
      case 'MÉDIO':
        return '#eab308';
      default:
        return '#22c55e';
    }
  };

  const getSeverityBgColor = (severity: string) => {
    switch (severity) {
      case 'CRÍTICO':
        return 'bg-red-50 border-red-500';
      case 'ALTO':
        return 'bg-orange-50 border-orange-500';
      case 'MÉDIO':
        return 'bg-yellow-50 border-yellow-500';
      default:
        return 'bg-green-50 border-green-500';
    }
  };

  // Preparar dados para gráfico de severidade
  const severityData = [
    { name: 'Crítico', value: vulnerabilities.filter(v => v.severity === 'CRÍTICO').length },
    { name: 'Alto', value: vulnerabilities.filter(v => v.severity === 'ALTO').length },
    { name: 'Médio', value: vulnerabilities.filter(v => v.severity === 'MÉDIO').length }
  ];

  // Preparar dados para gráfico de portas por dispositivo
  const devicePortData = scanResults.map(result => ({
    device: result.target_ip.split('.').pop(),
    ports: result.ports.length
  }));

  return (
    <div className="w-full space-y-6 p-6 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 rounded-lg">
      {/* Cabeçalho */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-white">🔍 Escaneamento Avançado de Rede (Nmap)</h2>
        <button
          onClick={startAdvancedScan}
          disabled={isScanning}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isScanning ? '⏳ Escaneando...' : '🔎 Iniciar Escaneamento'}
        </button>
      </div>

      {/* Risk Score */}
      <div className="bg-gradient-to-r from-red-500 to-orange-500 p-6 rounded-lg text-white">
        <p className="text-sm font-semibold mb-2">RISK SCORE</p>
        <div className="flex items-center justify-between">
          <div className="text-5xl font-bold">{riskScore}</div>
          <div className="text-right">
            <p className="text-lg">Vulnerabilidades Detectadas</p>
            <p className="text-3xl font-bold">{vulnerabilities.length}</p>
          </div>
        </div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-2 gap-6">
        {/* Gráfico de Severidade */}
        <div className="bg-white p-4 rounded-lg shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">📊 Distribuição de Severidade</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={severityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                <Cell fill="#dc2626" />
                <Cell fill="#ea580c" />
                <Cell fill="#eab308" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Gráfico de Portas por Dispositivo */}
        <div className="bg-white p-4 rounded-lg shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">🖥️ Portas Abertas por Dispositivo</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={devicePortData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="device" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="ports" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Resultados de Escaneamento */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">📡 Resultados de Escaneamento</h3>
        <div className="space-y-4">
          {scanResults.map((result) => (
            <div key={result.target_ip} className="border-l-4 border-blue-500 pl-4 py-2">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <p className="font-semibold text-gray-800">{result.hostname}</p>
                  <p className="text-sm text-gray-600">IP: {result.target_ip}</p>
                  <p className="text-sm text-gray-600">SO: {result.os_detection}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${result.status === 'up' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                  {result.status === 'up' ? '🟢 Online' : '🔴 Offline'}
                </span>
              </div>
              
              {/* Portas Abertas */}
              {result.ports.length > 0 && (
                <div className="mt-3">
                  <p className="text-sm font-semibold text-gray-700 mb-2">Portas Abertas:</p>
                  <div className="flex flex-wrap gap-2">
                    {result.ports.map((port) => (
                      <div key={port.port_number} className="bg-blue-100 px-3 py-1 rounded text-sm">
                        <span className="font-semibold text-blue-700">{port.port_number}/{port.protocol}</span>
                        <span className="text-blue-600 ml-2">{port.service}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Vulnerabilidades Detectadas */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">⚠️ Vulnerabilidades Detectadas</h3>
        <div className="space-y-4">
          {vulnerabilities.length > 0 ? (
            vulnerabilities.map((vuln) => (
              <div key={vuln.id} className={`border-l-4 p-4 rounded-lg ${getSeverityBgColor(vuln.severity)}`}>
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-semibold text-gray-800">{vuln.title}</p>
                    <p className="text-sm text-gray-700 mt-1">{vuln.description}</p>
                  </div>
                  <span style={{ backgroundColor: getSeverityColor(vuln.severity) }} className="px-3 py-1 rounded-full text-sm font-semibold text-white">
                    {vuln.severity}
                  </span>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-300">
                  <p className="text-sm"><strong>Dispositivo:</strong> {vuln.affected_device}:{vuln.port}</p>
                  <p className="text-sm mt-1"><strong>Remediação:</strong> {vuln.remediation}</p>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-600">Nenhuma vulnerabilidade detectada.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdvancedNetworkScanning;

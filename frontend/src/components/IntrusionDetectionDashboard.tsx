import React, { useState, useEffect } from 'react';
import { AlertTriangle, Shield, Activity, TrendingUp } from 'lucide-react';

interface IDSAlert {
  alert_id: string;
  timestamp: string;
  threat_level: string;
  attack_type: string;
  source_ip: string;
  destination_ip: string;
  source_port: number;
  destination_port: number;
  protocol: string;
  description: string;
  packets_count: number;
  confidence: number;
  remediation: string;
}

export const IntrusionDetectionDashboard: React.FC = () => {
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [alerts, setAlerts] = useState<IDSAlert[]>([]);
  const [summary, setSummary] = useState<any>(null);

  const startMonitoring = async () => {
    setIsMonitoring(true);
    try {
      await fetch('/api/ids/start', { method: 'POST' });
      fetchAlerts();
    } catch (error) {
      console.error('Erro ao iniciar IDS:', error);
    }
  };

  const stopMonitoring = async () => {
    setIsMonitoring(false);
    try {
      await fetch('/api/ids/stop', { method: 'POST' });
    } catch (error) {
      console.error('Erro ao parar IDS:', error);
    }
  };

  const fetchAlerts = async () => {
    try {
      const response = await fetch('/api/ids/alerts?limit=50');
      const data = await response.json();
      setAlerts(data.alerts || []);
    } catch (error) {
      console.error('Erro ao buscar alertas:', error);
    }
  };

  const fetchSummary = async () => {
    try {
      const response = await fetch('/api/ids/summary');
      const data = await response.json();
      setSummary(data);
    } catch (error) {
      console.error('Erro ao buscar resumo:', error);
    }
  };

  useEffect(() => {
    if (isMonitoring) {
      const interval = setInterval(() => {
        fetchAlerts();
        fetchSummary();
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [isMonitoring]);

  const getThreatColor = (level: string) => {
    switch (level) {
      case 'CRÍTICO':
        return 'bg-red-100 border-red-500 text-red-700';
      case 'ALTO':
        return 'bg-orange-100 border-orange-500 text-orange-700';
      case 'MÉDIO':
        return 'bg-yellow-100 border-yellow-500 text-yellow-700';
      default:
        return 'bg-blue-100 border-blue-500 text-blue-700';
    }
  };

  const getThreatIcon = (level: string) => {
    switch (level) {
      case 'CRÍTICO':
        return '🚨';
      case 'ALTO':
        return '⚠️';
      case 'MÉDIO':
        return '⚡';
      default:
        return 'ℹ️';
    }
  };

  return (
    <div className="w-full space-y-6 p-6 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 rounded-lg">
      {/* Cabeçalho */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Shield className="w-8 h-8 text-blue-400" />
          <h2 className="text-2xl font-bold text-white">🛡️ Sistema de Detecção de Intrusão (IDS)</h2>
        </div>
        <div className="space-x-4">
          <button
            onClick={startMonitoring}
            disabled={isMonitoring}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            {isMonitoring ? '🟢 Monitorando' : '▶️ Iniciar Monitoramento'}
          </button>
          <button
            onClick={stopMonitoring}
            disabled={!isMonitoring}
            className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
          >
            ⏹️ Parar Monitoramento
          </button>
        </div>
      </div>

      {/* Resumo de Ameaças */}
      {summary && (
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total de Alertas</p>
                <p className="text-3xl font-bold text-gray-800">{summary.total_alerts}</p>
              </div>
              <Activity className="w-8 h-8 text-blue-500" />
            </div>
          </div>

          <div className="bg-red-50 p-4 rounded-lg shadow-lg border-l-4 border-red-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-600">Alertas Críticos</p>
                <p className="text-3xl font-bold text-red-700">{summary.critical_alerts || 0}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-500" />
            </div>
          </div>

          <div className="bg-orange-50 p-4 rounded-lg shadow-lg border-l-4 border-orange-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-600">Alertas Altos</p>
                <p className="text-3xl font-bold text-orange-700">{summary.high_alerts || 0}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-orange-500" />
            </div>
          </div>

          <div className="bg-blue-50 p-4 rounded-lg shadow-lg border-l-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600">Status</p>
                <p className="text-lg font-bold text-blue-700">{isMonitoring ? 'ATIVO' : 'INATIVO'}</p>
              </div>
              <Shield className="w-8 h-8 text-blue-500" />
            </div>
          </div>
        </div>
      )}

      {/* Alertas em Tempo Real */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">📋 Alertas Detectados</h3>
        
        {alerts.length > 0 ? (
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {alerts.map((alert) => (
              <div
                key={alert.alert_id}
                className={`border-l-4 p-4 rounded-lg ${getThreatColor(alert.threat_level)}`}
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">{getThreatIcon(alert.threat_level)}</span>
                    <div>
                      <p className="font-semibold">{alert.alert_id}</p>
                      <p className="text-sm">{alert.attack_type}</p>
                    </div>
                  </div>
                  <span className="text-xs opacity-75">{new Date(alert.timestamp).toLocaleTimeString()}</span>
                </div>

                <p className="text-sm mb-2">{alert.description}</p>

                <div className="grid grid-cols-2 gap-2 text-xs mb-2">
                  <div>
                    <strong>Origem:</strong> {alert.source_ip}:{alert.source_port}
                  </div>
                  <div>
                    <strong>Destino:</strong> {alert.destination_ip}:{alert.destination_port}
                  </div>
                  <div>
                    <strong>Protocolo:</strong> {alert.protocol}
                  </div>
                  <div>
                    <strong>Confiança:</strong> {alert.confidence.toFixed(1)}%
                  </div>
                </div>

                <div className="bg-black bg-opacity-10 p-2 rounded text-xs mt-2">
                  <strong>Recomendação:</strong> {alert.remediation}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-600 text-center py-8">
            {isMonitoring ? 'Aguardando alertas...' : 'Inicie o monitoramento para detectar ataques'}
          </p>
        )}
      </div>

      {/* Informações Educacionais */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-3 text-blue-700">💡 O que é um IDS?</h3>
        <p className="text-sm text-blue-600 mb-3">
          Um Sistema de Detecção de Intrusão (IDS) monitora o tráfego de rede em busca de atividades suspeitas e padrões de ataque conhecidos. Este IDS educacional detecta:
        </p>
        <ul className="text-sm text-blue-600 space-y-1 ml-4">
          <li>✓ <strong>Escaneamento de Portas:</strong> Múltiplos pacotes SYN para diferentes portas (Nmap)</li>
          <li>✓ <strong>Ataque de Força Bruta:</strong> Múltiplas tentativas de autenticação falhas</li>
          <li>✓ <strong>Negação de Serviço (DoS):</strong> Alto volume de pacotes para sobrecarregar o servidor</li>
          <li>✓ <strong>Tráfego Suspeito:</strong> Padrões anormais de comunicação</li>
        </ul>
      </div>
    </div>
  );
};

export default IntrusionDetectionDashboard;

import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface TrafficData {
  timestamp: string;
  protocol: string;
  src_ip: string;
  dst_ip: string;
  size: number;
  port: number;
}

interface NetworkDevice {
  name: string;
  type: string;
  mac: string;
  status: string;
}

interface Vulnerability {
  id: number;
  severity: string;
  title: string;
  description: string;
  affected_device: string;
  remediation: string;
}

export const RealTimeMonitoring: React.FC = () => {
  const [trafficData, setTrafficData] = useState<TrafficData[]>([]);
  const [devices, setDevices] = useState<Record<string, NetworkDevice>>({});
  const [vulnerabilities, setVulnerabilities] = useState<Vulnerability[]>([]);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [protocolStats, setProtocolStats] = useState<Record<string, number>>({});
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Conectar ao WebSocket do servidor FastAPI
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/dashboard`;
    
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log('✅ Conectado ao servidor FastAPI');
    };

    wsRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);

      switch (message.type) {
        case 'traffic_update':
          setTrafficData(prev => [...prev, message.data].slice(-100)); // Manter últimos 100
          setProtocolStats(message.stats || {});
          break;
        
        case 'network_update':
          setDevices(message.devices || {});
          break;
        
        case 'vulnerabilities_update':
          setVulnerabilities(message.vulnerabilities || []);
          break;
        
        case 'monitoring_started':
          setIsMonitoring(true);
          break;
        
        case 'monitoring_stopped':
          setIsMonitoring(false);
          break;
      }
    };

    wsRef.current.onerror = (error) => {
      console.error('❌ Erro WebSocket:', error);
    };

    wsRef.current.onclose = () => {
      console.log('Desconectado do servidor');
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const startMonitoring = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'start_monitoring' }));
    }
  };

  const stopMonitoring = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'stop_monitoring' }));
    }
  };

  // Preparar dados para gráfico de tráfego
  const trafficChartData = trafficData.map((packet, index) => ({
    time: index,
    size: packet.size / 1024 // Converter para KB
  }));

  // Preparar dados para gráfico de protocolos
  const protocolChartData = Object.entries(protocolStats).map(([protocol, count]) => ({
    protocol,
    count
  }));

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRÍTICO':
        return 'text-red-600 bg-red-50';
      case 'ALTO':
        return 'text-orange-600 bg-orange-50';
      case 'MÉDIO':
        return 'text-yellow-600 bg-yellow-50';
      default:
        return 'text-green-600 bg-green-50';
    }
  };

  return (
    <div className="w-full space-y-6 p-6 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 rounded-lg">
      {/* Cabeçalho com Controles */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-white">🔍 Monitoramento em Tempo Real</h2>
        <div className="space-x-4">
          <button
            onClick={startMonitoring}
            disabled={isMonitoring}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            ▶️ Iniciar
          </button>
          <button
            onClick={stopMonitoring}
            disabled={!isMonitoring}
            className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
          >
            ⏹️ Parar
          </button>
        </div>
      </div>

      {/* Status de Monitoramento */}
      <div className={`p-4 rounded-lg ${isMonitoring ? 'bg-green-50 border-2 border-green-500' : 'bg-gray-50 border-2 border-gray-300'}`}>
        <p className={`text-lg font-semibold ${isMonitoring ? 'text-green-700' : 'text-gray-700'}`}>
          {isMonitoring ? '🟢 Monitoramento ATIVO' : '⚪ Monitoramento INATIVO'}
        </p>
      </div>

      {/* Estatísticas Rápidas */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="text-gray-600 text-sm">Total de Pacotes</p>
          <p className="text-3xl font-bold text-blue-600">{trafficData.length}</p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <p className="text-gray-600 text-sm">Dispositivos Online</p>
          <p className="text-3xl font-bold text-purple-600">{Object.keys(devices).length}</p>
        </div>
        <div className="bg-red-50 p-4 rounded-lg">
          <p className="text-gray-600 text-sm">Vulnerabilidades</p>
          <p className="text-3xl font-bold text-red-600">{vulnerabilities.length}</p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg">
          <p className="text-gray-600 text-sm">Protocolos Detectados</p>
          <p className="text-3xl font-bold text-yellow-600">{Object.keys(protocolStats).length}</p>
        </div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-2 gap-6">
        {/* Gráfico de Tráfego */}
        <div className="bg-white p-4 rounded-lg shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">📊 Tráfego de Rede (KB)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trafficChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="size" stroke="#8b5cf6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Gráfico de Protocolos */}
        <div className="bg-white p-4 rounded-lg shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">🔌 Distribuição de Protocolos</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={protocolChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="protocol" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Dispositivos Conectados */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">🖥️ Dispositivos Conectados</h3>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(devices).map(([ip, device]) => (
            <div key={ip} className="border-l-4 border-purple-500 pl-4 py-2">
              <p className="font-semibold text-gray-800">{device.name}</p>
              <p className="text-sm text-gray-600">IP: {ip}</p>
              <p className="text-sm text-gray-600">MAC: {device.mac}</p>
              <p className={`text-sm font-semibold ${device.status === 'online' ? 'text-green-600' : 'text-red-600'}`}>
                {device.status === 'online' ? '🟢 Online' : '🔴 Offline'}
              </p>
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
              <div key={vuln.id} className={`p-4 rounded-lg border-l-4 ${getSeverityColor(vuln.severity)}`}>
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold">{vuln.title}</p>
                    <p className="text-sm mt-1">{vuln.description}</p>
                    <p className="text-sm mt-2 font-semibold">🔧 Remediação: {vuln.remediation}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getSeverityColor(vuln.severity)}`}>
                    {vuln.severity}
                  </span>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-600">Nenhuma vulnerabilidade detectada no momento.</p>
          )}
        </div>
      </div>

      {/* Tráfego Recente */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">📡 Tráfego Recente</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Timestamp</th>
                <th className="px-4 py-2 text-left">Origem</th>
                <th className="px-4 py-2 text-left">Destino</th>
                <th className="px-4 py-2 text-left">Protocolo</th>
                <th className="px-4 py-2 text-left">Porta</th>
                <th className="px-4 py-2 text-left">Tamanho</th>
              </tr>
            </thead>
            <tbody>
              {trafficData.slice(-10).reverse().map((packet, index) => (
                <tr key={index} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-2 text-xs">{new Date(packet.timestamp).toLocaleTimeString()}</td>
                  <td className="px-4 py-2">{packet.src_ip}</td>
                  <td className="px-4 py-2">{packet.dst_ip}</td>
                  <td className="px-4 py-2 font-semibold text-blue-600">{packet.protocol}</td>
                  <td className="px-4 py-2">{packet.port}</td>
                  <td className="px-4 py-2">{(packet.size / 1024).toFixed(2)} KB</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default RealTimeMonitoring;

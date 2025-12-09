import React, { useState, useEffect } from 'react';
import './App.css'; // Para estilos globais

// Componente para o Terminal de Log (Simples)
const LogTerminal = ({ logs }) => (
  <div className="terminal-window">
    <div className="terminal-header">
      <span className="terminal-title">ASCENSÃO C2 - LOG DE EVENTOS</span>
    </div>
    <div className="terminal-body">
      {logs.map((log, index) => (
        <p key={index} className={log.type}>
          <span className="timestamp">[{log.time}]</span> {log.message}
        </p>
      ))}
    </div>
  </div>
);

// Componente para o Painel de Status do Alvo
const TargetStatus = ({ device }) => (
  <div className="target-status-card">
    <div className="card-header">
      <span className="card-title">ALVO: {device.name}</span>
      <span className={`status-dot ${device.status}`}></span>
    </div>
    <div className="card-body">
      <p><strong>IP:</strong> {device.ip}</p>
      <p><strong>Tipo:</strong> {device.type}</p>
      <p><strong>Último Check-in:</strong> {device.lastCheckin}</p>
    </div>
  </div>
);

// Componente Principal do Dashboard
function App() {
  const [device, setDevice] = useState({
    ip: '192.168.1.50',
    name: 'Celular-Vítima-04',
    type: 'Android',
    status: 'offline',
    lastCheckin: 'N/A'
  });
  const [logs, setLogs] = useState([
    { type: 'info', time: '00:00:00', message: 'Sistema C2 Iniciado. Aguardando conexão do Payload.' }
  ]);

  // Função para adicionar logs
  const addLog = (message, type = 'info') => {
    const now = new Date();
    const time = now.toTimeString().split(' ')[0];
    setLogs(prevLogs => [...prevLogs, { type, time, message }]);
  };

  // Efeito para simular a conexão (será substituído por WebSocket)
  useEffect(() => {
    // Simulação de conexão do Payload após 5 segundos
    const timer = setTimeout(() => {
      setDevice(prev => ({
        ...prev,
        status: 'online',
        lastCheckin: new Date().toTimeString().split(' ')[0]
      }));
      addLog('✅ PAYLOAD CONECTADO: Celular-Vítima-04 (192.168.1.50)', 'success');
      
      // Simulação de coleta de dados
      setTimeout(() => {
        addLog('📥 DADOS RECEBIDOS: Logins (99jogo66.com)', 'warning');
        addLog('📥 DADOS RECEBIDOS: Fotos (Galeria)', 'warning');
        addLog('📥 DADOS RECEBIDOS: Mensagens (SMS)', 'warning');
      }, 3000);

    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="dashboard-rpg">
      <header className="rpg-header">
        <h1>ASCENSÃO CULTIVO DIGITAL - PAINEL DE MISSÃO</h1>
        <p>Fase 2: Infiltração e Coleta de Dados</p>
      </header>

      <main className="rpg-main">
        <div className="rpg-sidebar">
          <TargetStatus device={device} />
          
          <div className="mission-log-card">
            <div className="card-header">
              <span className="card-title">OBJETIVOS DE MISSÃO</span>
            </div>
            <div className="card-body">
              <p className="mission-item completed">1. Estabilizar C2 (Backend/Frontend)</p>
              <p className="mission-item active">2. Injetar Payload (One-Click Exploit)</p>
              <p className="mission-item pending">3. Coletar Dados (Fotos, Mensagens, Logins)</p>
              <p className="mission-item pending">4. Exfiltrar Credenciais</p>
            </div>
          </div>
        </div>

        <div className="rpg-content">
          <LogTerminal logs={logs} />
        </div>
      </main>
    </div>
  );
}

export default App;

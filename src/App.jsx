
import React, { useState, useEffect, useRef } from 'react';
import './App.css';

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

const ControlPanel = ({ onCommand }) => {
  const [password, setPassword] = useState('');
  const [bruteTarget, setBruteTarget] = useState('');
  const [bruteUser, setBruteUser] = useState('');
  const [zapTarget, setZapTarget] = useState('');
  const [phishingTarget, setPhishingTarget] = useState('');

  return (
    <div className="control-panel">
      <h3>Painel de Controle</h3>
      <div className="control-group">
        <h4>Análise de Senha</h4>
        <input type="text" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Digite a senha" />
        <button onClick={() => onCommand('password_strength', { password })}>Analisar</button>
      </div>
      <div className="control-group">
        <h4>Brute Force</h4>
        <input type="text" value={bruteTarget} onChange={(e) => setBruteTarget(e.target.value)} placeholder="URL Alvo" />
        <input type="text" value={bruteUser} onChange={(e) => setBruteUser(e.target.value)} placeholder="Usuário" />
        <button onClick={() => onCommand('bruteforce', { target_url: bruteTarget, username: bruteUser })}>Iniciar</button>
      </div>
      <div className="control-group">
        <h4>ZAP Scan</h4>
        <input type="text" value={zapTarget} onChange={(e) => setZapTarget(e.target.value)} placeholder="URL Alvo" />
        <button onClick={() => onCommand('zap_scan', { target_url: zapTarget })}>Iniciar</button>
      </div>
      <div className="control-group">
        <h4>Phishing</h4>
        <input type="text" value={phishingTarget} onChange={(e) => setPhishingTarget(e.target.value)} placeholder="URL Alvo" />
        <button onClick={() => onCommand('phishing', { target_url: phishingTarget })}>Iniciar</button>
      </div>
    </div>
  );
};

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

function App() {
  const [device, setDevice] = useState({
    ip: '192.168.1.50',
    name: 'Celular-Vítima-04',
    type: 'Android',
    status: 'offline',
    lastCheckin: 'N/A'
  });
  const [logs, setLogs] = useState([]);
  const ws = useRef(null);

  const addLog = (message, type = 'info') => {
    const now = new Date();
    const time = now.toTimeString().split(' ')[0];
    setLogs(prevLogs => [...prevLogs, { type, time, message }]);
  };

  // Lógica do WebSocket temporariamente desativada para estabilizar o frontend
  useEffect(() => {
    addLog('Iniciando conexão com o servidor C2...', 'info');
    // const wsUrl = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws`;
    // ws.current = new WebSocket(wsUrl);

    // ws.current.onopen = () => {
    //   addLog('✅ Conexão WebSocket estabelecida.', 'success');
    // };

    // ws.current.onmessage = (event) => {
    //   const data = JSON.parse(event.data);
    //   addLog(`[${data.type}] ${JSON.stringify(data.data)}`, 'warning');
    // };

    // ws.current.onclose = () => {
    //   addLog('❌ Conexão WebSocket fechada.', 'error');
    // };

    // ws.current.onerror = (error) => {
    //   addLog(`❌ Erro no WebSocket: ${error.message}`, 'error');
    // };

    // return () => {
    //   ws.current.close();
    // };
  }, []);

  const handleCommand = async (command, params) => {
    let url = '';
    let options = { method: 'GET' };

    switch (command) {
      case 'password_strength':
        url = `/api/password/strength?password=${params.password}`;
        break;
      case 'bruteforce':
        url = `/api/bruteforce/start?target_url=${params.target_url}&username=${params.username}`;
        options.method = 'POST';
        break;
      case 'zap_scan':
        url = `/api/zap/scan/start?target_url=${params.target_url}`;
        options.method = 'POST';
        break;
      case 'phishing':
        url = `/api/phishing/start?target_url=${params.target_url}`;
        options.method = 'POST';
        break;
      default:
        return;
    }

    try {
      const response = await fetch(url, options);
      const data = await response.json();
      addLog(`Comando '${command}' executado. Resposta: ${JSON.stringify(data)}`, 'info');
    } catch (error) {
      addLog(`Erro ao executar comando '${command}': ${error.message}`, 'error');
    }
  };

  return (
    <div className="dashboard-rpg">
      <header className="rpg-header">
        <h1>ASCENSÃO CULTIVO DIGITAL - PAINEL DE MISSÃO</h1>
      </header>
      <main className="rpg-main">
        <div className="rpg-sidebar">
          <TargetStatus device={device} />
          <ControlPanel onCommand={handleCommand} />
        </div>
        <div className="rpg-content">
          <LogTerminal logs={logs} />
        </div>
      </main>
    </div>
  );
}

export default App;

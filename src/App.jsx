
import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const LogTerminal = ({ logs }) => (
  <div className="terminal-window">
    <div className="terminal-header">
      <span>SYSTEM EVENT LOG</span>
    </div>
    <div className="terminal-body">
      {logs.length === 0 && <p>Initializing secure connection...</p>}
      {logs.map((log, index) => (
        <p key={index} className={log.type}>
          <span className="timestamp">[{log.time}]</span> {log.message}
        </p>
      ))}
    </div>
  </div>
);

const ToolCard = ({ title, children, onAction, actionLabel, isLoading }) => (
  <div className="control-group">
    <h4>{title}</h4>
    {children}
    <button onClick={onAction} disabled={isLoading}>
      {isLoading ? 'Processing...' : actionLabel}
    </button>
  </div>
);

const TargetStatus = ({ device }) => (
  <div className="control-group status-panel">
    <h4>TARGET STATUS</h4>
    <div className="status-item">
      <span className="label">NAME:</span>
      <span className="value">{device.name}</span>
    </div>
    <div className="status-item">
      <span className="label">IP:</span>
      <span className="value">{device.ip}</span>
    </div>
    <div className="status-item">
      <span className="label">OS:</span>
      <span className="value">{device.type}</span>
    </div>
    <div className="status-item">
      <span className="label">STATUS:</span>
      <span className={`value status-${device.status}`}>{device.status.toUpperCase()}</span>
    </div>
  </div>
);

const App = () => {
  const [logs, setLogs] = useState([]);
  const [device, setDevice] = useState({
    ip: '192.168.1.50',
    name: 'Target-Device-04',
    type: 'Android / Linux',
    status: 'offline',
    lastCheckin: 'N/A'
  });
  const [inputs, setInputs] = useState({
    scanUrl: '',
    bruteUrl: '',
    bruteUsers: '',
    trafficHost: '',
    passAnalyze: '',
    phishingUrl: '',
    sqlmapUrl: '',
    osintDomain: '',
    sshIp: '',
    sshUser: 'root',
    sshPass: 'password,admin,123456'
  });
  const ws = useRef(null);

  const addLog = (message, type = 'info') => {
    const now = new Date();
    const time = now.toTimeString().split(' ')[0];
    setLogs(prevLogs => [...prevLogs, { type, time, message }].slice(-100));
  };

  useEffect(() => {
    const connectWS = () => {
      const wsUrl = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws`;
      ws.current = new WebSocket(wsUrl);
      ws.current.onopen = () => {
        addLog('Connection established with C2.', 'success');
        setDevice(prev => ({ ...prev, status: 'online' }));
      };
      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        addLog(`[EVENT] ${data.type}: ${JSON.stringify(data.data).substring(0, 100)}`, 'warning');
      };
      ws.current.onclose = () => {
        addLog('Connection lost. Retrying...', 'error');
        setDevice(prev => ({ ...prev, status: 'offline' }));
        setTimeout(connectWS, 5000);
      };
    };
    connectWS();
    return () => ws.current?.close();
  }, []);

  const handleCommand = async (endpoint, params) => {
    addLog(`Initiating ${endpoint.split('/').pop()}...`, 'info');
    try {
      const response = await fetch(`/api/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
      });
      const data = await response.json();
      if (data.status === 'error') throw new Error(data.message);
      addLog(`Success: ${JSON.stringify(data).substring(0, 100)}`, 'success');
    } catch (error) {
      addLog(`Failed: ${error.message}`, 'error');
    }
  };

  const updateInput = (key, val) => setInputs(prev => ({ ...prev, [key]: val }));

  return (
    <div className="dashboard-rpg">
      <header className="rpg-header">
        <h1>⚡ ASCENSÃO - CULTIVO DIGITAL v4.0 ⚡</h1>
        <div className="header-meta"><span>SECURE ACCESS GRANTED</span></div>
      </header>
      
      <main className="rpg-main">
        <div className="main-content">
          <div className="tools-grid">
            <ToolCard title="WEB VULNERABILITY SCANNER" actionLabel="Start Analysis" onAction={() => handleCommand('scan/web', { target_url: inputs.scanUrl })}>
              <input type="text" value={inputs.scanUrl} onChange={e => updateInput('scanUrl', e.target.value)} placeholder="Target URL" />
            </ToolCard>

            <ToolCard title="BRUTE FORCE MODULE" actionLabel="Execute Attack" onAction={() => handleCommand('bruteforce/attack', { target_url: inputs.bruteUrl, usernames: inputs.bruteUsers.split(',') })}>
              <input type="text" value={inputs.bruteUrl} onChange={e => updateInput('bruteUrl', e.target.value)} placeholder="Login URL" />
              <input type="text" value={inputs.bruteUsers} onChange={e => updateInput('bruteUsers', e.target.value)} placeholder="Usernames (comma separated)" />
            </ToolCard>

            <ToolCard title="SQLMAP INJECTION" actionLabel="Start SQL Scan" onAction={() => handleCommand('sqlmap/scan/start', { target_url: inputs.sqlmapUrl })}>
              <input type="text" value={inputs.sqlmapUrl} onChange={e => updateInput('sqlmapUrl', e.target.value)} placeholder="Target URL for SQLi" />
            </ToolCard>

            <ToolCard title="REAL PHISHING CLONER" actionLabel="Start Phishing" onAction={() => handleCommand('phishing/start', { target_url: inputs.phishingUrl })}>
              <input type="text" value={inputs.phishingUrl} onChange={e => updateInput('phishingUrl', e.target.value)} placeholder="URL to Clone" />
            </ToolCard>

            <ToolCard title="OSINT HARVESTER" actionLabel="Run OSINT" onAction={() => handleCommand('osint/harvester/run', { domain: inputs.osintDomain })}>
              <input type="text" value={inputs.osintDomain} onChange={e => updateInput('osintDomain', e.target.value)} placeholder="Domain (e.g., google.com)" />
            </ToolCard>

            <ToolCard title="SSH EXPLOIT" actionLabel="Start SSH Brute" onAction={() => handleCommand('exploit/ssh_brute', { target_ip: inputs.sshIp, username: inputs.sshUser, password_list_str: inputs.sshPass })}>
              <input type="text" value={inputs.sshIp} onChange={e => updateInput('sshIp', e.target.value)} placeholder="Target IP" />
              <input type="text" value={inputs.sshUser} onChange={e => updateInput('sshUser', e.target.value)} placeholder="Username" />
              <input type="text" value={inputs.sshPass} onChange={e => updateInput('sshPass', e.target.value)} placeholder="Passwords (comma separated)" />
            </ToolCard>

            <ToolCard title="TRAFFIC SPY LIVE" actionLabel="Monitor Traffic" onAction={() => handleCommand('traffic/spy', { target: inputs.trafficHost })}>
              <input type="text" value={inputs.trafficHost} onChange={e => updateInput('trafficHost', e.target.value)} placeholder="Target Hostname" />
            </ToolCard>

            <ToolCard title="PASSWORD ANALYZER" actionLabel="Analyze Strength" onAction={() => handleCommand('password/analyze', { password: inputs.passAnalyze })}>
              <input type="text" value={inputs.passAnalyze} onChange={e => updateInput('passAnalyze', e.target.value)} placeholder="Password to test" />
            </ToolCard>
          </div>
          
          <div style={{marginTop: '20px'}}>
            <LogTerminal logs={logs} />
          </div>
        </div>

        <aside className="rpg-sidebar">
          <TargetStatus device={device} />
          <div className="control-group" style={{background: 'rgba(138, 3, 3, 0.05)'}}>
            <h4>QUICK ACTIONS</h4>
            <button style={{marginBottom: '10px', background: '#333'}} onClick={() => addLog('System diagnostic started...')}>Run Diagnostic</button>
            <button style={{background: '#333'}} onClick={() => setLogs([])}>Clear Terminal</button>
          </div>
        </aside>
      </main>
    </div>
  );
};

export default App;

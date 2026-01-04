import React, { useState, useEffect } from 'react';
import { Eye, Lock, AlertTriangle, Smartphone, Zap } from 'lucide-react';

interface CapturedCredential {
  timestamp: string;
  protocol: string;
  username: string;
  password: string;
  source_ip: string;
  destination_ip: string;
  destination_host: string;
  confidence: number;
}

interface CapturedImage {
  timestamp: string;
  url: string;
  source_ip: string;
  file_type: string;
  file_size: number;
  file_path: string;
}

interface MITMSession {
  session_id: string;
  attack_type: string;
  status: string;
  captured_credentials: CapturedCredential[];
  captured_images: CapturedImage[];
  total_credentials: number;
  total_images: number;
}

export const MirrorOfMisfortune: React.FC = () => {
  const [isAttacking, setIsAttacking] = useState(false);
  const [session, setSession] = useState<MITMSession | null>(null);
  const [selectedTab, setSelectedTab] = useState<'credentials' | 'images' | 'overview'>('overview');

  const startMITMAttack = async () => {
    setIsAttacking(true);
    try {
      const response = await fetch('/api/mitm/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          attack_type: 'SSL_STRIP',
          target_ip: '192.168.1.200',
          gateway_ip: '192.168.1.1'
        })
      });

      const data = await response.json();
      setSession(data);
      
      // Atualizar dados capturados periodicamente
      const interval = setInterval(() => {
        fetchCapturedData(data.session_id);
      }, 2000);

      return () => clearInterval(interval);
    } catch (error) {
      console.error('Erro ao iniciar ataque MITM:', error);
    }
  };

  const stopMITMAttack = async () => {
    if (!session) return;

    try {
      await fetch(`/api/mitm/stop/${session.session_id}`, {
        method: 'POST'
      });
      setIsAttacking(false);
    } catch (error) {
      console.error('Erro ao parar ataque MITM:', error);
    }
  };

  const fetchCapturedData = async (sessionId: string) => {
    try {
      const response = await fetch(`/api/mitm/captured-data/${sessionId}`);
      const data = await response.json();
      setSession(data);
    } catch (error) {
      console.error('Erro ao buscar dados capturados:', error);
    }
  };

  return (
    <div className="w-full space-y-6 p-6 bg-gradient-to-br from-slate-900 via-red-900 to-slate-900 rounded-lg">
      {/* Cabeçalho Dramático */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Eye className="w-8 h-8 text-red-400 animate-pulse" />
          <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-red-400 to-orange-400">
            👁️ Espelho do Azar
          </h2>
        </div>
        <div className="space-x-4">
          <button
            onClick={startMITMAttack}
            disabled={isAttacking}
            className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 font-bold"
          >
            {isAttacking ? '🔴 Capturando Dados' : '▶️ Iniciar Captura'}
          </button>
          <button
            onClick={stopMITMAttack}
            disabled={!isAttacking}
            className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50"
          >
            ⏹️ Parar Captura
          </button>
        </div>
      </div>

      {/* Aviso Educacional */}
      <div className="bg-yellow-900 border-l-4 border-yellow-500 p-6 rounded-lg">
        <p className="text-yellow-200 font-semibold mb-2">⚠️ Demonstração Educacional de Ataque MITM</p>
        <p className="text-sm text-yellow-100">
          Este módulo simula um ataque Man-in-the-Middle (MITM) onde um atacante intercepta a comunicação entre a vítima (Celular 04) e o servidor. 
          O atacante pode capturar credenciais, imagens e outros dados não criptografados. <strong>Nunca faça isso em redes reais sem autorização!</strong>
        </p>
      </div>

      {/* Status da Sessão */}
      {session && (
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-red-900 p-4 rounded-lg shadow-lg border-l-4 border-red-500">
            <p className="text-sm text-red-200">Credenciais Capturadas</p>
            <p className="text-4xl font-bold text-red-400">{session.total_credentials}</p>
          </div>

          <div className="bg-orange-900 p-4 rounded-lg shadow-lg border-l-4 border-orange-500">
            <p className="text-sm text-orange-200">Imagens Capturadas</p>
            <p className="text-4xl font-bold text-orange-400">{session.total_images}</p>
          </div>

          <div className="bg-purple-900 p-4 rounded-lg shadow-lg border-l-4 border-purple-500">
            <p className="text-sm text-purple-200">Tipo de Ataque</p>
            <p className="text-lg font-bold text-purple-400">{session.attack_type}</p>
          </div>

          <div className="bg-blue-900 p-4 rounded-lg shadow-lg border-l-4 border-blue-500">
            <p className="text-sm text-blue-200">Status</p>
            <p className={`text-lg font-bold ${session.status === 'RUNNING' ? 'text-green-400' : 'text-gray-400'}`}>
              {session.status === 'RUNNING' ? '🟢 ATIVO' : '⚫ INATIVO'}
            </p>
          </div>
        </div>
      )}

      {/* Abas de Conteúdo */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="flex border-b">
          <button
            onClick={() => setSelectedTab('overview')}
            className={`flex-1 px-6 py-3 font-semibold ${
              selectedTab === 'overview'
                ? 'bg-red-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            📊 Visão Geral
          </button>
          <button
            onClick={() => setSelectedTab('credentials')}
            className={`flex-1 px-6 py-3 font-semibold ${
              selectedTab === 'credentials'
                ? 'bg-red-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🔑 Credenciais ({session?.total_credentials || 0})
          </button>
          <button
            onClick={() => setSelectedTab('images')}
            className={`flex-1 px-6 py-3 font-semibold ${
              selectedTab === 'images'
                ? 'bg-red-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🖼️ Imagens ({session?.total_images || 0})
          </button>
        </div>

        <div className="p-6">
          {/* Visão Geral */}
          {selectedTab === 'overview' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-800">Como Funciona o Ataque MITM</h3>
              <div className="bg-gray-50 p-4 rounded-lg space-y-3">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">1️⃣</span>
                  <div>
                    <p className="font-semibold text-gray-800">ARP Spoofing</p>
                    <p className="text-sm text-gray-600">O atacante envia pacotes ARP falsificados para se posicionar entre a vítima e o roteador.</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-2xl">2️⃣</span>
                  <div>
                    <p className="font-semibold text-gray-800">SSL Strip</p>
                    <p className="text-sm text-gray-600">O atacante força o downgrade de HTTPS para HTTP, permitindo a captura de dados em texto plano.</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-2xl">3️⃣</span>
                  <div>
                    <p className="font-semibold text-gray-800">Captura de Dados</p>
                    <p className="text-sm text-gray-600">Credenciais, imagens e outros dados são capturados enquanto a vítima navega normalmente.</p>
                  </div>
                </div>
              </div>

              <h3 className="text-lg font-semibold text-gray-800 mt-6">Como se Proteger</h3>
              <div className="bg-green-50 p-4 rounded-lg space-y-2">
                <p className="text-sm text-green-800">✓ Sempre use HTTPS e verifique o cadeado no navegador</p>
                <p className="text-sm text-green-800">✓ Ative HSTS (HTTP Strict Transport Security) nos seus sites</p>
                <p className="text-sm text-green-800">✓ Use VPN em redes WiFi públicas</p>
                <p className="text-sm text-green-800">✓ Ative certificados SSL/TLS com pinning</p>
                <p className="text-sm text-green-800">✓ Mantenha seu navegador e sistema operacional atualizados</p>
              </div>
            </div>
          )}

          {/* Credenciais Capturadas */}
          {selectedTab === 'credentials' && (
            <div className="space-y-3">
              {session && session.captured_credentials.length > 0 ? (
                session.captured_credentials.map((cred, idx) => (
                  <div key={idx} className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <p className="font-semibold text-red-700">🔓 {cred.destination_host}</p>
                        <p className="text-xs text-red-600">{new Date(cred.timestamp).toLocaleTimeString()}</p>
                      </div>
                      <span className="text-xs bg-red-200 text-red-800 px-2 py-1 rounded">
                        {cred.protocol}
                      </span>
                    </div>

                    <div className="bg-white p-3 rounded font-mono text-sm space-y-1 mb-2">
                      <p><strong>Usuário:</strong> <span className="text-red-600">{cred.username}</span></p>
                      <p><strong>Senha:</strong> <span className="text-red-600">{cred.password}</span></p>
                      <p className="text-xs text-gray-600">
                        <strong>De:</strong> {cred.source_ip} <strong>Para:</strong> {cred.destination_ip}
                      </p>
                    </div>

                    <div className="flex justify-between items-center">
                      <span className="text-xs text-red-600">Confiança: {cred.confidence.toFixed(1)}%</span>
                      <button
                        onClick={() => navigator.clipboard.writeText(`${cred.username}:${cred.password}`)}
                        className="text-xs text-red-600 hover:text-red-800"
                      >
                        📋 Copiar
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-600 text-center py-8">
                  {isAttacking ? 'Aguardando captura de credenciais...' : 'Nenhuma credencial capturada'}
                </p>
              )}
            </div>
          )}

          {/* Imagens Capturadas */}
          {selectedTab === 'images' && (
            <div className="space-y-3">
              {session && session.captured_images.length > 0 ? (
                session.captured_images.map((img, idx) => (
                  <div key={idx} className="bg-orange-50 border-l-4 border-orange-500 p-4 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <p className="font-semibold text-orange-700">🖼️ {img.url}</p>
                        <p className="text-xs text-orange-600">{new Date(img.timestamp).toLocaleTimeString()}</p>
                      </div>
                      <span className="text-xs bg-orange-200 text-orange-800 px-2 py-1 rounded">
                        {img.file_type.toUpperCase()}
                      </span>
                    </div>

                    <div className="bg-white p-3 rounded text-sm space-y-1">
                      <p><strong>Tamanho:</strong> {(img.file_size / 1024).toFixed(2)} KB</p>
                      <p className="text-xs text-gray-600">
                        <strong>Origem:</strong> {img.source_ip}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-600 text-center py-8">
                  {isAttacking ? 'Aguardando captura de imagens...' : 'Nenhuma imagem capturada'}
                </p>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Informação Educacional Final */}
      <div className="bg-purple-50 border-l-4 border-purple-500 p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-3 text-purple-700">💡 Lição Importante</h3>
        <p className="text-sm text-purple-600 mb-3">
          Este módulo demonstra como um atacante pode interceptar dados em uma rede WiFi não segura. 
          A demonstração é educacional e ocorre em um ambiente controlado com consentimento de todos os envolvidos.
        </p>
        <p className="text-sm text-purple-600">
          <strong>Nunca execute ataques MITM em redes reais sem autorização explícita!</strong> 
          Isso é ilegal e viola leis de proteção de dados e privacidade em praticamente todas as jurisdições.
        </p>
      </div>
    </div>
  );
};

export default MirrorOfMisfortune;

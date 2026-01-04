import { useState, useEffect, useMemo } from "react";
import { ChevronDown, AlertTriangle, Radio, Lock } from "lucide-react";
import DemonicNetworkVisualization from "@/components/DemonicNetworkVisualization";

/**
 * DESIGN PHILOSOPHY: Laboratório Demoníaco Digital EXTREMO
 * OTIMIZADO PARA PERFORMANCE - SEM LAG, SEM FLICKER
 */

interface VulnerabilityData {
  name: string;
  severity: "critical" | "high" | "medium" | "low";
  description: string;
  impact: number;
}

interface NetworkTraffic {
  protocol: string;
  encrypted: boolean;
  dataSize: number;
  timestamp: number;
}

export default function Home() {
  const [scrollY, setScrollY] = useState(0);
  const [activeTab, setActiveTab] = useState<"dashboard" | "traffic" | "checker" | "materials">("dashboard");

  // Memoizar dados para evitar recálculos
  const vulnerabilities = useMemo<VulnerabilityData[]>(() => [
    { name: "Senha Padrão do Roteador", severity: "critical", description: "Roteador usando credenciais padrão", impact: 95 },
    { name: "Firmware Desatualizado", severity: "high", description: "Versão antiga com vulnerabilidades conhecidas", impact: 85 },
    { name: "WiFi WEP Ativado", severity: "critical", description: "Criptografia fraca e obsoleta", impact: 90 },
    { name: "UPnP Habilitado", severity: "high", description: "Protocolo com riscos de segurança", impact: 75 },
  ], []);

  const networkTraffic = useMemo<NetworkTraffic[]>(() => [
    { protocol: "HTTP", encrypted: false, dataSize: 2048, timestamp: Date.now() },
    { protocol: "HTTPS", encrypted: true, dataSize: 4096, timestamp: Date.now() - 1000 },
    { protocol: "FTP", encrypted: false, dataSize: 1024, timestamp: Date.now() - 2000 },
  ], []);

  const materials = useMemo(() => [
    { title: "Senhas Fortes", desc: "Como criar e gerenciar senhas seguras", icon: "🔐" },
    { title: "Criptografia", desc: "Entenda os princípios da criptografia", icon: "🔒" },
    { title: "Redes Seguras", desc: "Boas práticas para redes WiFi", icon: "📡" },
    { title: "Malware", desc: "Proteção contra ameaças digitais", icon: "🦠" },
    { title: "Phishing", desc: "Reconheça e evite ataques de phishing", icon: "🎣" },
    { title: "Backup", desc: "Estratégias de backup e recuperação", icon: "💾" },
  ], []);

  const securityChecks = useMemo(() => [
    { item: "Senha do Roteador", status: "fraco", icon: "❌", severity: "critical" },
    { item: "Firmware Atualizado", status: "desatualizado", icon: "⚠️", severity: "high" },
    { item: "Criptografia WiFi", status: "fraco", icon: "❌", severity: "critical" },
    { item: "Firewall", status: "ativo", icon: "✅", severity: "safe" },
    { item: "UPnP", status: "habilitado", icon: "⚠️", severity: "high" },
  ], []);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical":
        return "bg-red-900 border-red-500";
      case "high":
        return "bg-orange-900 border-orange-500";
      case "medium":
        return "bg-yellow-900 border-yellow-500";
      default:
        return "bg-blue-900 border-blue-500";
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden">
      {/* Fundo estático (sem animações pesadas) */}
      <div className="fixed inset-0 pointer-events-none z-0" style={{
        background: 'linear-gradient(135deg, #050609 0%, #0A0E27 50%, #1A0033 100%)',
      }}>
        {/* Portais de fundo - animação leve */}
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full opacity-15"
            style={{
              width: Math.random() * 300 + 150 + "px",
              height: Math.random() * 300 + 150 + "px",
              background: `radial-gradient(circle, ${
                ["#FF0000", "#00FFFF", "#FFD700"][Math.floor(Math.random() * 3)]
              }, transparent)`,
              left: Math.random() * 100 + "%",
              top: Math.random() * 100 + "%",
              animation: `demonic-portal ${Math.random() * 20 + 25}s ease-in-out infinite`,
              animationDelay: Math.random() * 10 + "s",
              filter: "blur(60px)",
              willChange: "transform",
            }}
          />
        ))}
      </div>

      {/* ============================================
          HERO SECTION - Portal 3D
          ============================================ */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
        {/* Visualização 3D */}
        <div className="absolute inset-0 w-full h-full">
          <DemonicNetworkVisualization />
        </div>

        {/* Overlay com conteúdo */}
        <div className="relative z-10 flex flex-col items-center justify-center max-w-4xl mx-auto px-4 text-center">
          <div className="mb-8">
            <h1 className="text-7xl md:text-8xl font-black mb-4" style={{
              background: 'linear-gradient(135deg, #FFD700 0%, #00FFFF 50%, #FF0000 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              textShadow: 'none',
            }}>
              ⚡ ASCENSÃO ⚡
            </h1>
            <h2 className="text-5xl md:text-6xl font-black text-spectral-cyan" style={{
              textShadow: '0 0 30px rgba(0, 255, 255, 0.8)',
            }}>
              CULTIVO DIGITAL
            </h2>
          </div>

          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-8 text-center leading-relaxed">
            Laboratório Educacional de Segurança Cibernética com Demonstrações em Tempo Real
          </p>

          <div className="mb-12 p-6 border-2 border-spectral-cyan bg-void-darker/50 backdrop-blur-md" style={{
            boxShadow: '0 0 30px rgba(0, 255, 255, 0.3)',
          }}>
            <p className="text-sm md:text-base text-foreground mb-4">
              Visualize vulnerabilidades em ambientes controlados. Analise tráfego de rede. Aprenda técnicas de proteção digital.
            </p>
            <div className="flex flex-wrap gap-3 justify-center text-xs font-bold">
              <span className="px-3 py-1 bg-blood-red/30 border border-blood-red text-blood-red">🔴 CRÍTICO</span>
              <span className="px-3 py-1 bg-hellfire-gold/30 border border-hellfire-gold text-hellfire-gold">⚠️ ALTO</span>
              <span className="px-3 py-1 bg-spectral-cyan/30 border border-spectral-cyan text-spectral-cyan">🔵 MÉDIO</span>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 mb-12">
            <button
              onClick={() => document.getElementById("dashboard")?.scrollIntoView({ behavior: "smooth" })}
              className="button-demonic"
            >
              ⚔️ INICIAR ANÁLISE
            </button>
            <button
              onClick={() => document.getElementById("materials")?.scrollIntoView({ behavior: "smooth" })}
              className="button-demonic"
            >
              📚 MATERIAIS
            </button>
          </div>

          <div className="absolute bottom-8">
            <ChevronDown className="w-8 h-8 text-hellfire-gold animate-bounce" />
          </div>
        </div>

        <div className="section-divider absolute bottom-0 w-full" />
      </section>

      {/* ============================================
          DASHBOARD SECTION
          ============================================ */}
      <section id="dashboard" className="relative py-20 px-4 md:px-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-5xl font-black mb-12 text-center text-spectral-cyan" style={{
            textShadow: '0 0 30px rgba(0, 255, 255, 0.6)',
          }}>
            🔍 DASHBOARD DE VULNERABILIDADES
          </h2>

          {/* Tabs - ESTÁVEIS, SEM FLICKER */}
          <div className="flex gap-3 mb-12 flex-wrap justify-center">
            {[
              { id: "dashboard", label: "📊 Vulnerabilidades" },
              { id: "traffic", label: "📡 Tráfego" },
              { id: "checker", label: "🛡️ Verificador" },
              { id: "materials", label: "📚 Materiais" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-6 py-3 font-bold uppercase tracking-wider transition-all ${
                  activeTab === tab.id
                    ? "button-demonic"
                    : "border-2 border-hellfire-gold text-hellfire-gold hover:bg-hellfire-gold/10"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Conteúdo - Renderizado condicionalmente para evitar flicker */}
          <div className="min-h-96">
            {activeTab === "dashboard" && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {vulnerabilities.map((vuln, i) => (
                  <div
                    key={vuln.name}
                    className={`card-demonic border-l-4 ${getSeverityColor(vuln.severity)} hover:scale-105 transition-transform`}
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <AlertTriangle className="w-6 h-6 text-hellfire-gold" />
                        <h3 className="text-xl font-bold text-hellfire-gold">{vuln.name}</h3>
                      </div>
                      <span className="text-xs font-bold px-3 py-1 bg-blood-red text-white rounded-none">
                        {vuln.severity.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-muted-foreground mb-4">{vuln.description}</p>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-void-darker rounded-none h-2 overflow-hidden border border-hellfire-gold">
                        <div
                          className="h-full bg-gradient-to-r from-hellfire-gold to-blood-red"
                          style={{ width: `${vuln.impact}%` }}
                        />
                      </div>
                      <span className="text-sm font-bold text-hellfire-gold">{vuln.impact}%</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === "traffic" && (
              <div className="space-y-4">
                <h3 className="text-2xl font-bold text-spectral-cyan mb-6">Análise de Tráfego de Rede</h3>
                {networkTraffic.map((traffic) => (
                  <div key={traffic.protocol} className="card-demonic flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <Radio className={traffic.encrypted ? "text-corrupted-green" : "text-blood-red"} />
                      <div>
                        <h4 className="font-bold text-hellfire-gold">{traffic.protocol}</h4>
                        <p className="text-sm text-muted-foreground">
                          {traffic.encrypted ? "🔒 Criptografado" : "⚠️ TEXTO PLANO"}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-spectral-cyan">{traffic.dataSize} bytes</p>
                      <p className="text-xs text-muted-foreground">Dados em trânsito</p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === "checker" && (
              <div className="card-demonic max-w-2xl mx-auto">
                <h3 className="text-2xl font-bold text-spectral-cyan mb-6">Verificador de Configurações</h3>
                <div className="space-y-4">
                  {securityChecks.map((check) => (
                    <div
                      key={check.item}
                      className="flex items-center justify-between p-4 border-l-4 border-hellfire-gold bg-void-darker/50"
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-3xl">{check.icon}</span>
                        <span className="font-bold text-foreground">{check.item}</span>
                      </div>
                      <span
                        className={`font-bold uppercase text-sm ${
                          check.severity === "safe" ? "text-corrupted-green" : "text-blood-red"
                        }`}
                      >
                        {check.status}
                      </span>
                    </div>
                  ))}
                </div>
                <button className="button-demonic w-full mt-6">📄 Gerar Relatório</button>
              </div>
            )}

            {activeTab === "materials" && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {materials.map((material) => (
                  <div
                    key={material.title}
                    className="card-demonic hover:scale-105 transition-transform cursor-pointer"
                  >
                    <div className="text-6xl mb-4">{material.icon}</div>
                    <h4 className="text-xl font-bold text-hellfire-gold mb-2">{material.title}</h4>
                    <p className="text-muted-foreground mb-4 text-sm">{material.desc}</p>
                    <button className="text-spectral-cyan font-bold hover:text-hellfire-gold transition-colors">
                      Ler Mais →
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="section-divider" />
      </section>

      {/* ============================================
          COMPLIANCE SECTION
          ============================================ */}
      <section id="materials" className="relative py-20 px-4 md:px-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-5xl font-black mb-12 text-center text-spectral-cyan">
            ⚖️ CONFORMIDADE ÉTICA
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="card-demonic">
              <h3 className="text-2xl font-bold text-corrupted-green mb-4">✅ ESTE PROJETO É:</h3>
              <ul className="space-y-3 text-muted-foreground">
                {["100% Educacional", "Ambiente isolado", "Dados fictícios", "Foco em defesa", "Compliance legal"].map((item) => (
                  <li key={item} className="flex gap-3">
                    <span className="text-corrupted-green font-bold">→</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="card-demonic">
              <h3 className="text-2xl font-bold text-blood-red mb-4">❌ NÃO É:</h3>
              <ul className="space-y-3 text-muted-foreground">
                {["Uso malicioso", "Dados de terceiros", "Violação de privacidade", "Ferramentas para crimes", "Redes públicas"].map((item) => (
                  <li key={item} className="flex gap-3">
                    <span className="text-blood-red font-bold">✗</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="section-divider" />
      </section>

      {/* ============================================
          FOOTER
          ============================================ */}
      <section className="relative py-16 px-4 md:px-8 text-center border-t-2 border-spectral-cyan">
        <div className="max-w-4xl mx-auto">
          <h3 className="text-4xl md:text-5xl font-black mb-6 text-hellfire-gold" style={{
            textShadow: '0 0 30px rgba(255, 215, 0, 0.6)',
          }}>
            ⚡ ASCENSÃO DO CULTIVO DIGITAL ⚡
          </h3>

          <p className="text-muted-foreground mb-8 max-w-2xl mx-auto text-lg">
            Laboratório educacional para demonstração prática de segurança cibernética em ambientes controlados.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <button className="button-demonic">🚀 Iniciar Laboratório</button>
            <button className="px-8 py-4 font-bold uppercase tracking-widest border-2 border-spectral-cyan text-spectral-cyan hover:bg-spectral-cyan/10 transition-colors">
              📖 Documentação
            </button>
          </div>

          <div className="text-sm text-muted-foreground space-y-2">
            <p>🔐 100% Educacional | 🛡️ Ambiente Isolado | 📊 Dados Fictícios</p>
            <p>© 2025 Laboratório Demoníaco de Segurança Digital</p>
          </div>
        </div>
      </section>
    </div>
  );
}

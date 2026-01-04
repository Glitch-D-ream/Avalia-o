#!/usr/bin/env python3
"""
SecReport Generator - Gerador de Relatórios Profissionais de Segurança
Ferramenta criativa para gerar relatórios em PDF, HTML e JSON
AVISO: Apenas para fins educacionais em ambientes controlados.
"""

import json
from datetime import datetime
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    print("⚠️  ReportLab não está instalado. Instale com: pip install reportlab")
    REPORTLAB_AVAILABLE = False


class SecurityReportGenerator:
    """Gerador de relatórios de segurança profissionais"""
    
    def __init__(self, project_name="ASCENSÃO - CULTIVO DIGITAL"):
        """
        Inicializa o gerador
        
        Args:
            project_name: Nome do projeto
        """
        self.project_name = project_name
        self.report_data = {}
        
    def generate_pdf_report(self, data, output_file="security_report.pdf"):
        """
        Gera relatório em PDF
        
        Args:
            data: Dados do relatório
            output_file: Nome do arquivo de saída
        """
        if not REPORTLAB_AVAILABLE:
            print("❌ ReportLab não disponível")
            return None
        
        print(f"\n📄 Gerando relatório PDF: {output_file}")
        
        # Criar documento
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos customizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#D4AF37'),  # Ouro
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#4A1A5C'),  # Púrpura
            spaceAfter=12
        )
        
        # Título
        story.append(Paragraph(self.project_name, title_style))
        story.append(Paragraph("Relatório de Segurança Cibernética", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        # Informações gerais
        info_data = [
            ["Data do Relatório:", datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
            ["Alvo:", data.get("target", "N/A")],
            ["Tipo de Análise:", data.get("scan_type", "Completa")]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F0F0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Sumário Executivo
        story.append(Paragraph("Sumário Executivo", heading_style))
        
        total_vulns = data.get("total_vulnerabilities", 0)
        risk_score = data.get("risk_score", 0)
        
        summary_text = f"""
        Este relatório apresenta os resultados da análise de segurança realizada no alvo especificado.
        Foram identificadas <b>{total_vulns} vulnerabilidades</b> com um score de risco de <b>{risk_score}/100</b>.
        """
        
        story.append(Paragraph(summary_text, styles['BodyText']))
        story.append(Spacer(1, 0.2*inch))
        
        # Vulnerabilidades
        if data.get("vulnerabilities"):
            story.append(PageBreak())
            story.append(Paragraph("Vulnerabilidades Identificadas", heading_style))
            
            # Agrupar por severidade
            vulns_by_severity = {
                "CRITICAL": [],
                "HIGH": [],
                "MEDIUM": [],
                "LOW": []
            }
            
            for vuln in data["vulnerabilities"]:
                severity = vuln.get("severity", "LOW")
                vulns_by_severity[severity].append(vuln)
            
            # Tabela de resumo
            summary_data = [
                ["Severidade", "Quantidade"],
                ["Crítica", str(len(vulns_by_severity["CRITICAL"]))],
                ["Alta", str(len(vulns_by_severity["HIGH"]))],
                ["Média", str(len(vulns_by_severity["MEDIUM"]))],
                ["Baixa", str(len(vulns_by_severity["LOW"]))]
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A1A5C')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Detalhes das vulnerabilidades
            for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                if vulns_by_severity[severity]:
                    story.append(Paragraph(f"Vulnerabilidades de Severidade {severity}", styles['Heading3']))
                    
                    for i, vuln in enumerate(vulns_by_severity[severity], 1):
                        vuln_text = f"""
                        <b>{i}. {vuln.get('type', 'Desconhecido')}</b><br/>
                        <i>Descrição:</i> {vuln.get('description', 'N/A')}<br/>
                        <i>Recomendação:</i> {vuln.get('recommendation', 'N/A')}
                        """
                        story.append(Paragraph(vuln_text, styles['BodyText']))
                        story.append(Spacer(1, 0.1*inch))
        
        # Recomendações
        story.append(PageBreak())
        story.append(Paragraph("Recomendações de Segurança", heading_style))
        
        recommendations = [
            "Implementar todos os headers de segurança recomendados",
            "Configurar cookies com flags Secure e HttpOnly",
            "Habilitar HTTPS em todo o site",
            "Implementar Content Security Policy (CSP)",
            "Realizar auditorias de segurança regulares",
            "Manter todas as dependências atualizadas",
            "Implementar autenticação de dois fatores (2FA)",
            "Realizar testes de penetração periódicos"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", styles['BodyText']))
        
        # Rodapé
        story.append(Spacer(1, 0.5*inch))
        footer_text = f"""
        <i>Relatório gerado por {self.project_name}<br/>
        Este documento é confidencial e destinado apenas para fins educacionais.</i>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        print(f"✅ Relatório PDF gerado: {output_file}")
        return output_file
    
    def generate_html_report(self, data, output_file="security_report.html"):
        """
        Gera relatório em HTML
        
        Args:
            data: Dados do relatório
            output_file: Nome do arquivo de saída
        """
        print(f"\n🌐 Gerando relatório HTML: {output_file}")
        
        html_template = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.project_name} - Relatório de Segurança</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0F1B2E 0%, #1a1a2e 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        h1 {{
            color: #D4AF37;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        h2 {{
            color: #00D9FF;
            border-bottom: 2px solid #4A1A5C;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        .info-box {{
            background: rgba(74, 26, 92, 0.3);
            border-left: 4px solid #D4AF37;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .vuln-card {{
            background: rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 5px solid #8B0000;
        }}
        .vuln-critical {{ border-left-color: #8B0000; }}
        .vuln-high {{ border-left-color: #FF6B6B; }}
        .vuln-medium {{ border-left-color: #FFA500; }}
        .vuln-low {{ border-left-color: #FFD700; }}
        .severity-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .severity-critical {{ background: #8B0000; }}
        .severity-high {{ background: #FF6B6B; }}
        .severity-medium {{ background: #FFA500; }}
        .severity-low {{ background: #FFD700; color: #000; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        th {{
            background: rgba(74, 26, 92, 0.5);
            color: #D4AF37;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ {self.project_name} ⚡</h1>
        <p style="text-align: center; color: #00D9FF; font-size: 1.2em;">Relatório de Segurança Cibernética</p>
        
        <div class="info-box">
            <p><strong>Data do Relatório:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
            <p><strong>Alvo:</strong> {data.get("target", "N/A")}</p>
            <p><strong>Total de Vulnerabilidades:</strong> {data.get("total_vulnerabilities", 0)}</p>
            <p><strong>Risk Score:</strong> {data.get("risk_score", 0)}/100</p>
        </div>
        
        <h2>📊 Sumário Executivo</h2>
        <p>Este relatório apresenta os resultados da análise de segurança realizada no alvo especificado.
        Foram identificadas <strong>{data.get("total_vulnerabilities", 0)} vulnerabilidades</strong> com um score de risco de <strong>{data.get("risk_score", 0)}/100</strong>.</p>
        
        <h2>🐛 Vulnerabilidades Identificadas</h2>
        """
        
        # Adicionar vulnerabilidades
        if data.get("vulnerabilities"):
            for vuln in data["vulnerabilities"]:
                severity = vuln.get("severity", "LOW").lower()
                html_template += f"""
        <div class="vuln-card vuln-{severity}">
            <span class="severity-badge severity-{severity}">{vuln.get("severity", "LOW")}</span>
            <h3>{vuln.get("type", "Desconhecido")}</h3>
            <p><strong>Descrição:</strong> {vuln.get("description", "N/A")}</p>
            <p><strong>Recomendação:</strong> {vuln.get("recommendation", "N/A")}</p>
        </div>
                """
        
        html_template += f"""
        <div class="footer">
            <p><em>Relatório gerado por {self.project_name}</em></p>
            <p><em>Este documento é confidencial e destinado apenas para fins educacionais.</em></p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"✅ Relatório HTML gerado: {output_file}")
        return output_file
    
    def generate_json_report(self, data, output_file="security_report.json"):
        """
        Gera relatório em JSON
        
        Args:
            data: Dados do relatório
            output_file: Nome do arquivo de saída
        """
        print(f"\n📋 Gerando relatório JSON: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Relatório JSON gerado: {output_file}")
        return output_file


# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    sample_data = {
        "target": "https://example.com",
        "scan_type": "Completa",
        "total_vulnerabilities": 5,
        "risk_score": 65,
        "vulnerabilities": [
            {
                "type": "Missing Security Header",
                "severity": "MEDIUM",
                "description": "Header X-Frame-Options não encontrado",
                "recommendation": "Adicionar header X-Frame-Options para prevenir clickjacking"
            },
            {
                "type": "Insecure Cookie",
                "severity": "HIGH",
                "description": "Cookie sem flag Secure",
                "recommendation": "Adicionar flag Secure em todos os cookies"
            }
        ]
    }
    
    generator = SecurityReportGenerator()
    
    # Gerar relatórios em todos os formatos
    generator.generate_json_report(sample_data, "example_report.json")
    generator.generate_html_report(sample_data, "example_report.html")
    
    if REPORTLAB_AVAILABLE:
        generator.generate_pdf_report(sample_data, "example_report.pdf")
    
    print("\n✅ Todos os relatórios foram gerados com sucesso!")

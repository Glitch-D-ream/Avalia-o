#!/usr/bin/env python3
"""
CENTRAL DE AUDITORIA WI-FI - INTERFACE DE ALTO NÍVEL
---------------------------------------------------
Integra o motor de análise real com o sistema de relatórios do projeto.
"""

import asyncio
import sys
import os
from analyzers.real_wifi_analyzer import WiFiSecurityAuditor

async def run_audit():
    print("="*70)
    print("   SISTEMA AVANÇADO DE AUDITORIA DE REDES WI-FI - AMBIENTE CONTROLADO")
    print("="*70)
    
    # Verificar privilégios de root
    if os.geteuid() != 0:
        print("\n[!] ERRO: Este módulo requer privilégios de ROOT para manipulação de pacotes 802.11.")
        print("Execute com: sudo python3 wifi_audit_center.py <interface>")
        return

    if len(sys.argv) < 2:
        print("\n[!] ERRO: Interface não especificada.")
        print("Uso: sudo python3 wifi_audit_center.py <interface_monitor>")
        return

    interface = sys.argv[1]
    
    # Inicializar Auditor
    auditor = WiFiSecurityAuditor(interface)
    
    try:
        await auditor.perform_full_audit()
    except KeyboardInterrupt:
        print("\n[!] Auditoria interrompida pelo usuário.")
    except Exception as e:
        print(f"\n[!] Ocorreu um erro inesperado: {e}")
    finally:
        print("\n" + "="*70)
        print("   AUDITORIA FINALIZADA - CONSULTE OS LOGS EM logs/wifi_audit.log")
        print("="*70)

if __name__ == "__main__":
    asyncio.run(run_audit())

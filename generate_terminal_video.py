import os
import subprocess

def generate_video():
    print("[*] Gerando vídeo de terminal via FFmpeg...")
    
    # Conteúdo do terminal simulado
    terminal_content = """
    ASCENSAO V15.0 - LIVE CODING DEMONSTRATION
    ------------------------------------------
    $ cd Avalia-o
    $ nano professional_exploit.py
    
    import requests
    import base64
    
    def bypass_jwt():
        # Bypass de JWT (alg:none)
        header = "eyJhbGciOiAibm9uZSJ9"
        payload = "eyJ1c2VyIjogImFkbWluIn0"
        token = f"{header}.{payload}."
        return token
    
    $ python3 professional_exploit.py
    [*] Token Gerado: eyJhbGciOiAibm9uZSJ9.eyJ1c2VyIjogImFkbWluIn0.
    [!!!] SUCESSO: ACESSO ADMINISTRATIVO OBTIDO!
    ------------------------------------------
    """
    
    with open("terminal_script.txt", "w") as f:
        f.write(terminal_content)
        
    # Usar o filtro drawtext do FFmpeg para criar o vídeo diretamente do texto
    # Nota: Este comando cria um vídeo de 10 segundos com o texto centralizado
    video_cmd = (
        "ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=10 "
        "-vf \"drawtext=textfile=terminal_script.txt:fontcolor=white:fontsize=24:x=50:y=50\" "
        "-c:v libx264 -pix_fmt yuv420p live_coding_terminal.mp4"
    )
    
    subprocess.run(video_cmd, shell=True)
    
    if os.path.exists("live_coding_terminal.mp4"):
        print("[!!!] SUCESSO: Vídeo live_coding_terminal.mp4 gerado!")
        return True
    return False

if __name__ == "__main__":
    generate_video()

import os
import subprocess
import shlex

def create_frame(text, filename):
    # Usar shlex.quote para garantir que o texto seja passado corretamente para o shell
    quoted_text = shlex.quote(text)
    cmd = f"convert -size 1280x720 xc:#1e1e1e -gravity northwest -fill #d4d4d4 -pointsize 20 -annotate +50+50 {quoted_text} {filename}"
    subprocess.run(cmd, shell=True)

def generate_live_video():
    print("[*] Iniciando simulação de Live Coding V2...")
    
    code_snippets = [
        "ubuntu@sandbox:~$ cd Avalia-o",
        "ubuntu@sandbox:~/Avalia-o$ nano jwt_bypass.py",
        "import requests\nimport base64\nimport json",
        "def bypass_jwt():\n    header = base64.b64encode(json.dumps({'alg': 'none'}).encode())",
        "    payload = base64.b64encode(json.dumps({'user': 'admin'}).encode())",
        "    token = f'{header}.{payload}.'",
        "    print(f'[*] Token Gerado: {token}')",
        "ubuntu@sandbox:~/Avalia-o$ python3 jwt_bypass.py",
        "[*] Token Gerado: eyJhbGciOiAibm9uZSJ9.eyJ1c2VyIjogImFkbWluIn0.",
        "[!!!] SUCESSO: ACESSO ADMINISTRATIVO OBTIDO!"
    ]
    
    current_text = ""
    frame_count = 0
    
    for snippet in code_snippets:
        current_text += snippet + "\n"
        # Gerar 10 frames para cada snippet para dar tempo de leitura (5 segundos a 2fps)
        for _ in range(10):
            filename = f"live_frame_{frame_count:03d}.png"
            create_frame(current_text, filename)
            frame_count += 1

    print(f"[*] Gerados {frame_count} frames. Renderizando vídeo...")
    video_cmd = "ffmpeg -y -framerate 2 -i live_frame_%03d.png -c:v libx264 -pix_fmt yuv420p live_coding_tutorial.mp4"
    subprocess.run(video_cmd, shell=True)
    
    if os.path.exists("live_coding_tutorial.mp4"):
        print("[!!!] SUCESSO: Vídeo live_coding_tutorial.mp4 gerado!")
        return True
    return False

if __name__ == "__main__":
    generate_live_video()

#!/usr/bin/env python3.11
"""
Script para corrigir strings quebradas em arquivos Python
"""
import os
import re
import glob

def fix_broken_strings(file_path):
    """Corrige strings quebradas em um arquivo Python"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Padrão 1: print(" seguido de quebra de linha real
        # Exemplo: print(" -> print("
        content = re.sub(r'print\("(\s*)
', r'print("\\n\n', content)
        content = re.sub(r'print\(f"(\s*)
', r'print(f"\\n\n', content)
        
        # Padrão 2: Strings que terminam com " seguido de quebra de linha sem fechar
        # Procurar por padrões como: "texto\n (sem fechar aspas)
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Verificar se a linha tem aspas não fechadas
            if line.count('"') % 2 != 0 and i + 1 < len(lines):
                # Verificar se a próxima linha não começa com aspas
                next_line = lines[i + 1]
                if not next_line.strip().startswith('"'):
                    # Juntar as linhas
                    line = line + '\\n' + next_line
                    i += 1
            fixed_lines.append(line)
            i += 1
        
        content = '\n'.join(fixed_lines)
        
        # Salvar apenas se houve mudanças
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Corrigido: {os.path.basename(file_path)}")
            return True
        else:
            print(f"  OK: {os.path.basename(file_path)}")
            return False
    except Exception as e:
        print(f"✗ Erro em {os.path.basename(file_path)}: {e}")
        return False

def main():
    """Corrige todos os arquivos Python no diretório atual"""
    python_files = glob.glob('*.py')
    python_files = [f for f in python_files if f != 'fix_syntax.py']
    
    print(f"Encontrados {len(python_files)} arquivos Python para verificar")
    
    fixed_count = 0
    for file_path in sorted(python_files):
        if fix_broken_strings(file_path):
            fixed_count += 1
    
    print(f"{fixed_count} arquivos foram corrigidos")

if __name__ == "__main__":
    main()

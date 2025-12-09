# 📸 GUIA DE CAPTURA DE IMAGENS - DEMONSTRAÇÃO IMPRESSIONANTE

## Para Surpreender os Jurados na Competição

---

## 🎯 O QUE VAI ACONTECER

Você vai capturar **imagens REAIS** que o celular vítima (04) envia pela rede. Quando mostrar aos jurados, eles vão ficar impressionados porque:

1. ✅ **Dados visuais sendo capturados** - Não é apenas números
2. ✅ **Risco real e tangível** - Qualquer um pode ver as imagens
3. ✅ **Impacto emocional** - "Veem? Capturei uma imagem que você enviou!"
4. ✅ **Prova de conceito** - Demonstra vulnerabilidade real

---

## 📋 PREPARAÇÃO

### PASSO 1: Preparar Imagens no Celular 04

1. **Crie imagens pretas simples** (ou use qualquer imagem)
   - Tamanho: 200x200 a 500x500 pixels
   - Formato: PNG ou JPG
   - Conteúdo: Pode ser preto, branco, qualquer coisa

2. **Ou use imagens existentes:**
   - Screenshots
   - Fotos da câmera
   - Imagens da galeria

3. **Salve no celular 04** em uma pasta acessível

### PASSO 2: Preparar Notebook 01

Certifique-se de ter:
- ✅ Python 3.11+
- ✅ Scapy instalado
- ✅ Privilégios de administrador
- ✅ Script `image_capture.py` pronto

---

## 🚀 EXECUTAR CAPTURA

### PASSO 1: Iniciar Captura no Notebook

Abra terminal/PowerShell como **Administrador** e execute:

```bash
cd ~/security_education_kit
sudo python3 image_capture.py --target 192.168.1.200
```

**Esperado:**

```
📸 CAPTURA DE IMAGENS DO TRÁFEGO
Laboratório Demoníaco - Demonstração Impressionante
================================================================================

[+] Alvo: 192.168.1.200
[+] Diretório de saída: captured_images/
[*] Capturando imagens... Pressione Ctrl+C para parar

💡 DICA: Abra sites com imagens no celular vítima para capturar!
```

### PASSO 2: Gerar Tráfego no Celular 04

No celular 04, faça uma das seguintes ações:

**Opção 1: Abrir Sites com Imagens (HTTP)**

```
http://example.com          (tem imagens)
http://httpbin.org/image    (retorna imagem)
http://imgur.com            (galeria de imagens)
http://unsplash.it/400/300  (imagem aleatória)
```

**Opção 2: Transferir Arquivo**

1. Abra navegador
2. Acesse site que permite upload de imagens
3. Faça upload da imagem preta
4. O arquivo trafega pela rede!

**Opção 3: Usar App de Mensagem (HTTP)**

- Enviar imagem via WhatsApp Web (HTTP)
- Enviar via Telegram (parcialmente HTTP)
- Enviar via email (SMTP = texto plano)

### PASSO 3: Observar Captura

No terminal do notebook, você verá:

```
[+] Imagem capturada: image_20251130_091523_123.png (45678 bytes)
    De: 192.168.1.200 → Para: 93.184.216.34
    Tipo: PNG

[+] Imagem capturada: image_20251130_091518_456.jpg (123456 bytes)
    De: 192.168.1.200 → Para: 142.250.185.46
    Tipo: JPG
```

### PASSO 4: Parar Captura

Pressione **Ctrl+C** para parar

**Esperado:**

```
[*] Captura interrompida

================================================================================
📸 RESUMO DE IMAGENS CAPTURADAS
================================================================================

Total de imagens: 2

PNG: 1 imagens
  Tamanho total: 45,678 bytes

JPG: 1 imagens
  Tamanho total: 123,456 bytes

Imagens capturadas:
1. image_20251130_091523_123.png
   Tamanho: 45,678 bytes
   Tipo: PNG
   De: 192.168.1.200 → Para: 93.184.216.34
   Caminho: captured_images/image_20251130_091523_123.png

2. image_20251130_091518_456.jpg
   Tamanho: 123,456 bytes
   Tipo: JPG
   De: 192.168.1.200 → Para: 142.250.185.46
   Caminho: captured_images/image_20251130_091518_456.jpg

================================================================================
[+] Manifesto exportado: captured_images/manifest.json
```

---

## 👀 VISUALIZAR IMAGENS CAPTURADAS

### Abrir Pasta

```bash
# Windows
explorer captured_images

# Linux
nautilus captured_images

# Mac
open captured_images
```

### Visualizar Imagens

Todas as imagens capturadas estão em:
```
captured_images/
├── image_20251130_091523_123.png
├── image_20251130_091518_456.jpg
└── manifest.json
```

Clique duplo para abrir e ver as imagens capturadas!

---

## 🎤 APRESENTAR NA COMPETIÇÃO

### Sequência de Apresentação (5 minutos)

**Minuto 0-1: Explicação**

```
"Vou demonstrar algo muito impressionante.

Vou capturar IMAGENS que o celular vítima envia pela rede.

Não é apenas dados - são imagens REAIS sendo interceptadas!"
```

**Minuto 1-2: Iniciar Captura**

```bash
sudo python3 image_capture.py --target 192.168.1.200
```

Explicar:
- "Estou capturando tráfego do celular 04"
- "Vou procurar por imagens"
- "Qualquer imagem enviada em HTTP será capturada"

**Minuto 2-4: Gerar Tráfego**

No celular 04:
- Abrir navegador
- Acessar `http://unsplash.it/400/300` (retorna imagem)
- Ou fazer upload de imagem em site

No terminal do notebook:
- Mostrar mensagens de captura
- "Vejam! Uma imagem foi capturada!"

**Minuto 4-5: Mostrar Resultado**

```bash
# Parar captura
Ctrl+C

# Abrir pasta
explorer captured_images  # Windows
# ou
nautilus captured_images  # Linux
```

Mostrar:
- Imagens capturadas
- Arquivo `manifest.json` com detalhes
- Tamanho e tipo de cada imagem

### Discurso Impactante

```
"Vejam bem o que aconteceu aqui:

1. O celular 04 enviou uma imagem pela rede
2. Eu capturei essa imagem
3. Agora posso ver a imagem que foi enviada

Isso é possível porque a imagem foi enviada em HTTP (texto plano).

Se fosse HTTPS (criptografado), eu NÃO conseguiria capturar.

Isso mostra por que HTTPS é tão importante!

Qualquer pessoa na mesma rede WiFi pode fazer isso.

Por isso é importante:
- Usar HTTPS em todos os sites
- Não confiar em WiFi público
- Usar VPN quando necessário
- Manter dados sensíveis criptografados"
```

---

## 💡 DICAS PARA IMPRESSIONAR

### Dica 1: Usar Imagens Significativas

Em vez de imagens aleatórias, use:
- ✅ Documentos (PDF convertido em imagem)
- ✅ Screenshots de dados sensíveis
- ✅ Fotos de identidade (fictícia)
- ✅ Cartões de crédito (fictício)

**Impacto:** "Vejam - capturei até um cartão de crédito!"

### Dica 2: Capturar Múltiplas Imagens

Quanto mais imagens capturar, mais impressionante:
- 1 imagem: OK
- 5 imagens: Bom
- 20+ imagens: Excelente

**Como:** Deixar captura rodando enquanto celular 04 navega por sites com muitas imagens (Pinterest, Instagram, etc)

### Dica 3: Mostrar Comparação

Capturar com:
1. **HTTP** - Imagens capturadas ✅
2. **HTTPS** - Nenhuma imagem capturada ❌

Explicar: "Vejam a diferença!"

### Dica 4: Arquivo Manifest

Mostrar arquivo `manifest.json`:

```json
{
  "timestamp": "2025-11-30T09:15:30.123456",
  "target_device": "192.168.1.200",
  "total_images": 2,
  "images": [
    {
      "timestamp": "2025-11-30T09:15:25.123456",
      "filename": "image_20251130_091523_123.png",
      "size": 45678,
      "type": "png",
      "source": "192.168.1.200",
      "destination": "93.184.216.34"
    }
  ]
}
```

Explicar: "Aqui está o registro de todas as imagens capturadas"

### Dica 5: Vídeo de Demonstração

Grave um vídeo mostrando:
1. Captura iniciando
2. Celular 04 abrindo site
3. Imagens sendo capturadas em tempo real
4. Pasta com imagens capturadas

Se algo falhar na competição, você tem o vídeo como backup!

---

## 🔒 SEGURANÇA E ÉTICA

### Importante

- ✅ Use APENAS dados fictícios ou seus próprios
- ✅ Não capture dados de outras pessoas
- ✅ Não use para fins maliciosos
- ✅ Explique que é educacional
- ✅ Mostre como se proteger

### Avisos Educacionais

Sempre diga:

```
"Este é um laboratório educacional.

Estou capturando imagens MINHAS em uma rede ISOLADA que EU CONTROLO.

Nunca faça isso com dados de outras pessoas ou redes que você não controla.

Isso seria ilegal e antiético.

O objetivo é APRENDER sobre segurança, não prejudicar ninguém."
```

---

## 📊 RESULTADOS ESPERADOS

### Cenário 1: Captura Bem-Sucedida

```
✅ 5-20 imagens capturadas
✅ Tamanho total: 500KB - 5MB
✅ Tipos: PNG, JPG, GIF
✅ Arquivo manifest.json criado
✅ Jurados impressionados!
```

### Cenário 2: Poucas Imagens

```
⚠️ 1-4 imagens capturadas
⚠️ Ainda assim impressionante
⚠️ Explique: "Depende do tráfego gerado"
✅ Mostre o conceito funcionando
```

### Cenário 3: Nenhuma Imagem

```
❌ Nenhuma imagem capturada
⚠️ Possível causa: Sites usando HTTPS
✅ Use sites HTTP específicos
✅ Ou faça upload em site HTTP
```

---

## 🎯 CHECKLIST

Antes de apresentar:

- [ ] Script `image_capture.py` testado
- [ ] Celular 04 preparado com imagens
- [ ] Notebook com privilégios de admin
- [ ] Pasta `captured_images/` criada
- [ ] Captura rodou com sucesso
- [ ] Imagens foram capturadas
- [ ] Manifest.json foi gerado
- [ ] Imagens são visíveis na pasta
- [ ] Discurso preparado
- [ ] Vídeo de backup gravado

---

## 🚀 RESULTADO FINAL

Quando tudo funcionar:

**Você terá:**
- ✅ Demonstração visual impressionante
- ✅ Dados REAIS sendo capturados
- ✅ Prova de conceito funcional
- ✅ Impacto emocional nos jurados
- ✅ Melhor nota na competição!

**Jurados vão pensar:**
- "Que legal! Ele capturou imagens reais!"
- "Isso é educacional e impressionante"
- "Ele entende realmente de segurança"
- "Merece uma boa nota!"

---

**Desenvolvido para fins educacionais exclusivamente**

**Boa sorte na competição!** 🚀📸

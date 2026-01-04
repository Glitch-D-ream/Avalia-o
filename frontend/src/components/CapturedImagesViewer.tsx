import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AlertCircle, Download, Trash2, RefreshCw } from 'lucide-react';

interface CapturedImage {
  timestamp: string;
  filename: string;
  filepath: string;
  size: number;
  type: string;
  source: string;
  destination: string;
}

export default function CapturedImagesViewer() {
  const [images, setImages] = useState<CapturedImage[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState<CapturedImage | null>(null);

  // Simular carregamento de imagens capturadas
  useEffect(() => {
    const loadImages = async () => {
      setLoading(true);
      try {
        // Em produção, isso viria de uma API
        // const response = await fetch('/api/captured-images');
        // const data = await response.json();
        // setImages(data);

        // Para demonstração, criar dados fictícios
        const mockImages: CapturedImage[] = [
          {
            timestamp: new Date().toISOString(),
            filename: 'image_20251130_091523_123.png',
            filepath: '/captured_images/image_20251130_091523_123.png',
            size: 45678,
            type: 'png',
            source: '192.168.1.200',
            destination: '93.184.216.34'
          },
          {
            timestamp: new Date(Date.now() - 5000).toISOString(),
            filename: 'image_20251130_091518_456.jpg',
            filepath: '/captured_images/image_20251130_091518_456.jpg',
            size: 123456,
            type: 'jpg',
            source: '192.168.1.200',
            destination: '142.250.185.46'
          }
        ];
        setImages(mockImages);
      } catch (error) {
        console.error('Erro ao carregar imagens:', error);
      } finally {
        setLoading(false);
      }
    };

    loadImages();
  }, []);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleTimeString('pt-BR');
  };

  return (
    <div className="w-full space-y-4">
      <Card className="border-2 border-red-500/50 bg-red-950/20">
        <CardHeader>
          <div className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-red-500" />
            <CardTitle className="text-red-400">📸 Imagens Capturadas</CardTitle>
          </div>
          <CardDescription className="text-red-300/70">
            Imagens interceptadas do tráfego de rede do celular vítima
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Botões de Ação */}
          <div className="flex gap-2">
            <Button
              onClick={() => window.location.reload()}
              variant="outline"
              size="sm"
              className="border-cyan-500/50 hover:bg-cyan-500/10"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Atualizar
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="border-red-500/50 hover:bg-red-500/10"
            >
              <Download className="h-4 w-4 mr-2" />
              Baixar Todas ({images.length})
            </Button>
          </div>

          {/* Grid de Imagens */}
          {images.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {images.map((img, idx) => (
                <div
                  key={idx}
                  onClick={() => setSelectedImage(img)}
                  className="relative group cursor-pointer"
                >
                  <div className="aspect-square bg-gradient-to-br from-red-900/30 to-purple-900/30 rounded-lg border border-cyan-500/30 overflow-hidden hover:border-cyan-500/70 transition-all">
                    {/* Placeholder com ícone */}
                    <div className="w-full h-full flex items-center justify-center">
                      <div className="text-center">
                        <div className="text-2xl mb-2">
                          {img.type === 'jpg' ? '🖼️' : '🎨'}
                        </div>
                        <div className="text-xs text-cyan-300">
                          {img.type.toUpperCase()}
                        </div>
                        <div className="text-xs text-gray-400 mt-1">
                          {formatFileSize(img.size)}
                        </div>
                      </div>
                    </div>

                    {/* Overlay com informações */}
                    <div className="absolute inset-0 bg-black/80 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-2">
                      <div className="text-xs text-cyan-300 truncate">
                        {img.filename}
                      </div>
                      <div className="text-xs text-gray-400">
                        {formatDate(img.timestamp)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-400">
              <div className="text-4xl mb-2">📸</div>
              <p>Nenhuma imagem capturada ainda</p>
              <p className="text-sm mt-2">Abra sites com imagens no celular vítima para capturar</p>
            </div>
          )}

          {/* Detalhes da Imagem Selecionada */}
          {selectedImage && (
            <div className="mt-6 p-4 border border-cyan-500/50 rounded-lg bg-cyan-950/20">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h4 className="font-mono text-cyan-300 mb-2">
                    {selectedImage.filename}
                  </h4>
                  <div className="space-y-1 text-sm text-gray-400">
                    <p>
                      <span className="text-cyan-400">Tamanho:</span>{' '}
                      {formatFileSize(selectedImage.size)}
                    </p>
                    <p>
                      <span className="text-cyan-400">Tipo:</span>{' '}
                      {selectedImage.type.toUpperCase()}
                    </p>
                    <p>
                      <span className="text-cyan-400">De:</span>{' '}
                      {selectedImage.source}
                    </p>
                    <p>
                      <span className="text-cyan-400">Para:</span>{' '}
                      {selectedImage.destination}
                    </p>
                    <p>
                      <span className="text-cyan-400">Capturada em:</span>{' '}
                      {formatDate(selectedImage.timestamp)}
                    </p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedImage(null)}
                  className="text-red-400 hover:bg-red-500/20"
                >
                  ✕
                </Button>
              </div>

              {/* Aviso Educacional */}
              <div className="bg-red-950/30 border border-red-500/50 rounded p-3 text-sm text-red-300">
                <strong>⚠️ Aviso Educacional:</strong> Esta imagem foi capturada porque
                foi enviada em HTTP (texto plano). Se fosse HTTPS (criptografado),
                não seria possível interceptar!
              </div>
            </div>
          )}

          {/* Estatísticas */}
          {images.length > 0 && (
            <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-cyan-500/20">
              <div className="text-center">
                <div className="text-2xl font-bold text-cyan-400">
                  {images.length}
                </div>
                <div className="text-xs text-gray-400">Imagens</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-400">
                  {formatFileSize(
                    images.reduce((sum, img) => sum + img.size, 0)
                  )}
                </div>
                <div className="text-xs text-gray-400">Total</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-400">
                  {images.filter((img) => img.type === 'jpg').length}
                </div>
                <div className="text-xs text-gray-400">JPG</div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

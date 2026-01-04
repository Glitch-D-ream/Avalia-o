import { useEffect, useRef } from 'react';
import * as THREE from 'three';

/**
 * DESIGN PHILOSOPHY: Visualização Demoníaca 3D OTIMIZADA
 * Performance: Reduzidas partículas, geometrias simplificadas, renderização eficiente
 */

interface Device {
  ip: string;
  mac: string;
  type: 'router' | 'device' | 'attacker' | 'victim';
}

interface NetworkVisualizationProps {
  devices?: Device[];
}

export default function DemonicNetworkVisualization({
  devices = [
    { ip: '192.168.1.1', mac: 'AA:BB:CC:DD:EE:FF', type: 'router' },
    { ip: '192.168.1.100', mac: '11:22:33:44:55:66', type: 'device' },
    { ip: '192.168.1.50', mac: '77:88:99:AA:BB:CC', type: 'attacker' },
    { ip: '192.168.1.200', mac: 'DD:EE:FF:00:11:22', type: 'victim' },
  ],
}: NetworkVisualizationProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const animationIdRef = useRef<number | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    // ============================================
    // INICIALIZAÇÃO OTIMIZADA
    // ============================================

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x050609);
    scene.fog = new THREE.FogExp2(0x050609, 0.003);
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 10000);
    camera.position.set(0, 50, 100);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Limitar pixel ratio
    renderer.shadowMap.enabled = false; // Desabilitar sombras para performance
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // ============================================
    // ILUMINAÇÃO OTIMIZADA
    // ============================================

    const ambientLight = new THREE.AmbientLight(0x8B0000, 0.3);
    scene.add(ambientLight);

    const redLight = new THREE.PointLight(0xFF0000, 1.5, 400);
    redLight.position.set(100, 100, 100);
    scene.add(redLight);

    const cyanLight = new THREE.PointLight(0x00FFFF, 1, 300);
    cyanLight.position.set(-100, 50, -100);
    scene.add(cyanLight);

    const goldLight = new THREE.PointLight(0xFFD700, 0.8, 250);
    goldLight.position.set(0, 150, 0);
    scene.add(goldLight);

    // ============================================
    // PARTÍCULAS OTIMIZADAS (Reduzidas)
    // ============================================

    const particleGeometry = new THREE.BufferGeometry();
    const particleCount = 800; // Reduzido de 2000
    const positions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 300;
      positions[i + 1] = (Math.random() - 0.5) * 300;
      positions[i + 2] = (Math.random() - 0.5) * 300;
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const particleMaterial = new THREE.PointsMaterial({
      color: 0xFFD700,
      size: 0.8,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.5,
      fog: true,
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    // ============================================
    // NÓDOS DE DISPOSITIVOS
    // ============================================

    const nodePositions: { [key: string]: THREE.Vector3 } = {};
    const nodeGroups: THREE.Group[] = [];

    devices.forEach((device, index) => {
      const angle = (index / devices.length) * Math.PI * 2;
      const radius = 80;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      const y = Math.random() * 30 - 15;

      nodePositions[device.ip] = new THREE.Vector3(x, y, z);

      const nodeGroup = new THREE.Group();

      // Esfera central simplificada
      let sphereColor = 0x00FFFF;
      let sphereSize = 8;

      if (device.type === 'router') {
        sphereColor = 0xFFD700;
        sphereSize = 12;
      } else if (device.type === 'attacker') {
        sphereColor = 0xFF0000;
        sphereSize = 10;
      } else if (device.type === 'victim') {
        sphereColor = 0x8B0000;
        sphereSize = 8;
      }

      const sphereGeometry = new THREE.IcosahedronGeometry(sphereSize, 3); // Reduzido de 4
      const sphereMaterial = new THREE.MeshStandardMaterial({
        color: sphereColor,
        emissive: sphereColor,
        emissiveIntensity: 0.6,
        metalness: 0.7,
        roughness: 0.3,
      });

      const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
      nodeGroup.add(sphere);

      // Aura wireframe
      const auraGeometry = new THREE.IcosahedronGeometry(sphereSize * 1.4, 3);
      const auraMaterial = new THREE.MeshBasicMaterial({
        color: sphereColor,
        transparent: true,
        opacity: 0.15,
        wireframe: true,
      });

      const aura = new THREE.Mesh(auraGeometry, auraMaterial);
      aura.userData.rotationSpeed = Math.random() * 0.015 + 0.005;
      nodeGroup.add(aura);

      nodeGroup.position.copy(nodePositions[device.ip]);
      nodeGroup.userData.originalPosition = nodePositions[device.ip].clone();
      nodeGroup.userData.pulsePhase = Math.random() * Math.PI * 2;

      scene.add(nodeGroup);
      nodeGroups.push(nodeGroup);
    });

    // ============================================
    // LINHAS DE ENERGIA
    // ============================================

    const routerNode = nodeGroups[0];
    const lines: THREE.LineSegments[] = [];

    for (let i = 1; i < nodeGroups.length; i++) {
      const node = nodeGroups[i];
      const lineGeometry = new THREE.BufferGeometry();

      const positions = new Float32Array([
        routerNode.position.x,
        routerNode.position.y,
        routerNode.position.z,
        node.position.x,
        node.position.y,
        node.position.z,
      ]);

      lineGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

      const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x00FFFF,
        linewidth: 1,
        transparent: true,
        opacity: 0.5,
      });

      const line = new THREE.LineSegments(lineGeometry, lineMaterial);
      scene.add(line);
      lines.push(line);
    }

    // ============================================
    // ANIMAÇÃO OTIMIZADA
    // ============================================

    let time = 0;
    let frameCount = 0;

    const animate = () => {
      animationIdRef.current = requestAnimationFrame(animate);
      frameCount++;

      // Atualizar apenas a cada 2 frames para reduzir carga
      if (frameCount % 2 === 0) {
        time += 0.01;

        // Animar partículas com movimento simplificado
        if (particles) {
          const positionAttribute = particles.geometry.getAttribute('position');
          const positions = positionAttribute.array as Float32Array;

          for (let i = 0; i < positions.length; i += 3) {
            positions[i] += (Math.random() - 0.5) * 0.3;
            positions[i + 1] += (Math.random() - 0.5) * 0.3;
            positions[i + 2] += (Math.random() - 0.5) * 0.3;

            if (Math.abs(positions[i]) > 150) positions[i] *= -0.8;
            if (Math.abs(positions[i + 1]) > 150) positions[i + 1] *= -0.8;
            if (Math.abs(positions[i + 2]) > 150) positions[i + 2] *= -0.8;
          }

          positionAttribute.needsUpdate = true;
          particles.rotation.x += 0.00005;
          particles.rotation.y += 0.0001;
        }

        // Animar nódos
        nodeGroups.forEach((node) => {
          const pulseScale = 1 + Math.sin(time * 1.5 + node.userData.pulsePhase) * 0.08;
          node.scale.set(pulseScale, pulseScale, pulseScale);

          const aura = node.children[1];
          if (aura) {
            aura.rotation.x += aura.userData.rotationSpeed;
            aura.rotation.y += aura.userData.rotationSpeed * 1.2;
          }

          const floatAmount = Math.sin(time + node.userData.pulsePhase) * 3;
          node.position.y = node.userData.originalPosition.y + floatAmount;
        });

        // Câmera orbitante suave
        camera.position.x = Math.sin(time * 0.2) * 120;
        camera.position.z = Math.cos(time * 0.2) * 120;
        camera.position.y = 50 + Math.sin(time * 0.15) * 15;
        camera.lookAt(0, 0, 0);

        // Luzes dinâmicas
        redLight.intensity = 1 + Math.sin(time * 1.5) * 0.4;
        cyanLight.intensity = 0.8 + Math.sin(time * 1.2 + Math.PI) * 0.3;
      }

      renderer.render(scene, camera);
    };

    animate();

    // ============================================
    // HANDLE RESIZE
    // ============================================

    const handleResize = () => {
      if (!containerRef.current) return;

      const newWidth = containerRef.current.clientWidth;
      const newHeight = containerRef.current.clientHeight;

      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    // ============================================
    // CLEANUP
    // ============================================

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current);
      }
      if (containerRef.current && renderer.domElement.parentNode === containerRef.current) {
        containerRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
      particleGeometry.dispose();
      particleMaterial.dispose();
    };
  }, [devices]);

  return (
    <div
      ref={containerRef}
      className="w-full h-full"
      style={{
        position: 'relative',
        overflow: 'hidden',
        background: 'linear-gradient(135deg, #050609 0%, #0A0E27 50%, #1A0033 100%)',
      }}
    />
  );
}

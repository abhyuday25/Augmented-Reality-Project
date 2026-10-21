import React from 'react';
import { useTexture } from '@react-three/drei';
import * as THREE from 'three';
import { useMuseumStore } from '../../store/useMuseumStore';

export function SchoolsBackWall() {
  const openExhibitById = useMuseumStore((state) => state.openExhibitById);

  // Load all 7 gallery textures
  const [
    texHdr,
    texSmec,
    texScope,
    texCentral,
    texSense,
    texSelect,
    texFooter,
  ] = useTexture([
    '/src/assets/textures/tex_schools_header.png',
    '/src/assets/textures/tex_panel_smec.png',
    '/src/assets/textures/tex_panel_scope.png',
    '/src/assets/textures/tex_schools_central.png',
    '/src/assets/textures/tex_panel_sense.png',
    '/src/assets/textures/tex_panel_select.png',
    '/src/assets/textures/tex_schools_footer.png',
  ]);

  // Ensure sRGB encoding and crisp filtering
  [texHdr, texSmec, texScope, texCentral, texSense, texSelect, texFooter].forEach((tex) => {
    if (tex) {
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.anisotropy = 8;
    }
  });

  return (
    <group position={[0, 0, -16.15]}>
      {/* 1. Main Architectural Backdrop Wall */}
      <mesh position={[0, 2.4, -0.05]} receiveShadow>
        <planeGeometry args={[35, 4.8]} />
        <meshStandardMaterial color="#081120" roughness={0.92} metalness={0.08} />
      </mesh>

      {/* Top Brass Crown Moulding */}
      <mesh position={[0, 4.75, 0.02]} castShadow>
        <boxGeometry args={[35, 0.14, 0.22]} />
        <meshStandardMaterial color="#d4af37" roughness={0.25} metalness={0.85} />
      </mesh>

      {/* Bottom Baseboard */}
      <mesh position={[0, 0.12, 0.02]}>
        <boxGeometry args={[35, 0.24, 0.18]} />
        <meshStandardMaterial color="#1e293b" roughness={0.5} metalness={0.3} />
      </mesh>

      {/* 2. Grand Backlit Header Banner */}
      <mesh position={[0, 4.22, 0.01]} castShadow>
        <boxGeometry args={[26.3, 0.82, 0.04]} />
        <meshStandardMaterial color="#d4af37" roughness={0.25} metalness={0.8} />
      </mesh>
      <mesh position={[0, 4.22, 0.04]}>
        <planeGeometry args={[26.0, 0.76]} />
        <meshStandardMaterial map={texHdr} roughness={0.35} metalness={0.15} />
      </mesh>

      {/* Accent Spotlights illuminating the wall */}
      <spotLight
        position={[-8, 4.6, 2.2]}
        target-position={[-8, 2.2, 0]}
        intensity={2.5}
        angle={Math.PI / 4}
        penumbra={0.5}
        color="#fffbeb"
        distance={12}
      />
      <spotLight
        position={[0, 4.6, 2.2]}
        target-position={[0, 2.2, 0]}
        intensity={3.0}
        angle={Math.PI / 4}
        penumbra={0.5}
        color="#fef3c7"
        distance={12}
      />
      <spotLight
        position={[8, 4.6, 2.2]}
        target-position={[8, 2.2, 0]}
        intensity={2.5}
        angle={Math.PI / 4}
        penumbra={0.5}
        color="#fffbeb"
        distance={12}
      />

      {/* BAY 1: SMEC (School of Mechanical Engineering) */}
      <group
        position={[-12.0, 2.2, 0.0]}
        onClick={(e) => {
          e.stopPropagation();
          openExhibitById('school-smec');
        }}
        onPointerOver={() => (document.body.style.cursor = 'pointer')}
        onPointerOut={() => (document.body.style.cursor = 'auto')}
      >
        <mesh position={[0, 0, 0.02]} castShadow>
          <boxGeometry args={[4.92, 2.92, 0.04]} />
          <meshStandardMaterial color="#d4af37" roughness={0.25} metalness={0.8} />
        </mesh>
        <mesh position={[0, 0, 0.05]}>
          <planeGeometry args={[4.8, 2.8]} />
          <meshStandardMaterial map={texSmec} roughness={0.35} metalness={0.15} />
        </mesh>
      </group>

      {/* BAY 2: SCOPE (School of Computer Science & Engineering) */}
      <group
        position={[-6.0, 2.2, 0.0]}
        onClick={(e) => {
          e.stopPropagation();
          openExhibitById('school-scope');
        }}
        onPointerOver={() => (document.body.style.cursor = 'pointer')}
        onPointerOut={() => (document.body.style.cursor = 'auto')}
      >
        <mesh position={[0, 0, 0.02]} castShadow>
          <boxGeometry args={[4.92, 2.92, 0.04]} />
          <meshStandardMaterial color="#d4af37" roughness={0.25} metalness={0.8} />
        </mesh>
        <mesh position={[0, 0, 0.05]}>
          <planeGeometry args={[4.8, 2.8]} />
          <meshStandardMaterial map={texScope} roughness={0.35} metalness={0.15} />
        </mesh>
      </group>

      {/* BAY 3: GRAND CENTRAL DIRECTORY & EMBLEM */}
      <group
        position={[0.0, 2.2, 0.0]}
        onClick={(e) => {
          e.stopPropagation();
          openExhibitById('exhibit-schools-wall');
        }}
        onPointerOver={() => (document.body.style.cursor = 'pointer')}
        onPointerOut={() => (document.body.style.cursor = 'auto')}
      >
        <mesh position={[0, 0, 0.02]} castShadow>
          <boxGeometry args={[5.54, 3.04, 0.06]} />
          <meshStandardMaterial color="#f5c542" roughness={0.2} metalness={0.85} />
        </mesh>
        <mesh position={[0, 0, 0.06]}>
          <planeGeometry args={[5.4, 2.9]} />
          <meshStandardMaterial map={texCentral} roughness={0.35} metalness={0.15} />
        </mesh>
      </group>

      {/* BAY 4: SENSE (School of Electronics Engineering) */}
      <group
        position={[6.0, 2.2, 0.0]}
        onClick={(e) => {
          e.stopPropagation();
          openExhibitById('school-sense');
        }}
        onPointerOver={() => (document.body.style.cursor = 'pointer')}
        onPointerOut={() => (document.body.style.cursor = 'auto')}
      >
        <mesh position={[0, 0, 0.02]} castShadow>
          <boxGeometry args={[4.92, 2.92, 0.04]} />
          <meshStandardMaterial color="#d4af37" roughness={0.25} metalness={0.8} />
        </mesh>
        <mesh position={[0, 0, 0.05]}>
          <planeGeometry args={[4.8, 2.8]} />
          <meshStandardMaterial map={texSense} roughness={0.35} metalness={0.15} />
        </mesh>
      </group>

      {/* BAY 5: SELECT & SITE (Electrical Power & Information Systems) */}
      <group
        position={[12.0, 2.2, 0.0]}
        onClick={(e) => {
          e.stopPropagation();
          openExhibitById('school-select');
        }}
        onPointerOver={() => (document.body.style.cursor = 'pointer')}
        onPointerOut={() => (document.body.style.cursor = 'auto')}
      >
        <mesh position={[0, 0, 0.02]} castShadow>
          <boxGeometry args={[4.92, 2.92, 0.04]} />
          <meshStandardMaterial color="#d4af37" roughness={0.25} metalness={0.8} />
        </mesh>
        <mesh position={[0, 0, 0.05]}>
          <planeGeometry args={[4.8, 2.8]} />
          <meshStandardMaterial map={texSelect} roughness={0.35} metalness={0.15} />
        </mesh>
      </group>

      {/* MULTIDISCIPLINARY FOOTER RIBBON */}
      <group
        position={[0, 0.48, 0.0]}
        onClick={(e) => {
          e.stopPropagation();
          openExhibitById('school-interdisciplinary');
        }}
        onPointerOver={() => (document.body.style.cursor = 'pointer')}
        onPointerOut={() => (document.body.style.cursor = 'auto')}
      >
        <mesh position={[0, 0, 0.02]}>
          <boxGeometry args={[32.2, 0.48, 0.02]} />
          <meshStandardMaterial color="#1e293b" roughness={0.5} metalness={0.4} />
        </mesh>
        <mesh position={[0, 0, 0.04]}>
          <planeGeometry args={[32.0, 0.44]} />
          <meshStandardMaterial map={texFooter} roughness={0.4} metalness={0.1} />
        </mesh>
      </group>
    </group>
  );
}

import React from 'react';
import { useLoader } from '@react-three/fiber';
import * as THREE from 'three';
import { useMuseumStore } from '../../store/useMuseumStore';

export function CampusMasterplanDiorama({ position = [0, 0, 4.2] }) {
  const openExhibitById = useMuseumStore((state) => state.openExhibitById);

  // Load composite campus map and photo textures
  const mapTex = useLoader(THREE.TextureLoader, '/scripts/generated_textures/tex_campus_map.png');
  mapTex.colorSpace = THREE.SRGBColorSpace;

  const ttTex = useLoader(THREE.TextureLoader, '/src/assets/images/vit/vit_technology_tower.jpg');
  ttTex.colorSpace = THREE.SRGBColorSpace;

  const sjtTex = useLoader(THREE.TextureLoader, '/src/assets/images/vit/vit_sjt_academic.jpg');
  sjtTex.colorSpace = THREE.SRGBColorSpace;

  const adminTex = useLoader(THREE.TextureLoader, '/src/assets/images/vit/vit_admin_building.jpg');
  adminTex.colorSpace = THREE.SRGBColorSpace;

  const libTex = useLoader(THREE.TextureLoader, '/src/assets/images/vit/vit_library.jpg');
  libTex.colorSpace = THREE.SRGBColorSpace;

  return (
    <group position={position}>
      {/* Base Display Table */}
      <mesh position={[0, 0.425, 0]} castShadow receiveShadow>
        <boxGeometry args={[4.2, 0.85, 3.2]} />
        <meshStandardMaterial color="#0c1830" roughness={0.3} metalness={0.2} />
      </mesh>
      {/* Polished Gold Table Rim */}
      <mesh position={[0, 0.86, 0]} castShadow>
        <boxGeometry args={[4.3, 0.08, 3.3]} />
        <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.85} />
      </mesh>

      {/* High-Resolution Masterplan Surface Map */}
      <mesh position={[0, 0.91, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[4.0, 3.0]} />
        <meshStandardMaterial map={mapTex} roughness={0.35} metalness={0.05} />
      </mesh>

      {/* Open-Air Gold Vitrine Frame */}
      {[-1.98, 1.98].map((cx) =>
        [-1.48, 1.48].map((cz) => (
          <mesh key={`${cx}-${cz}`} position={[cx, 1.32, cz]} castShadow>
            <cylinderGeometry args={[0.024, 0.024, 0.86, 16]} />
            <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.85} />
          </mesh>
        ))
      )}
      {/* Top Rails */}
      <mesh position={[0, 1.74, -1.48]}>
        <boxGeometry args={[3.96, 0.035, 0.035]} />
        <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.85} />
      </mesh>
      <mesh position={[0, 1.74, 1.48]}>
        <boxGeometry args={[3.96, 0.035, 0.035]} />
        <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.85} />
      </mesh>
      <mesh position={[-1.98, 1.74, 0]}>
        <boxGeometry args={[0.035, 0.035, 2.96]} />
        <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.85} />
      </mesh>
      <mesh position={[1.98, 1.74, 0]}>
        <boxGeometry args={[0.035, 0.035, 2.96]} />
        <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.85} />
      </mesh>

      {/* Gallery LED Spotlight Bar under top frame */}
      <mesh position={[0, 1.72, 0]}>
        <boxGeometry args={[3.88, 0.015, 2.88]} />
        <meshStandardMaterial color="#fffbeb" emissive="#fef08a" emissiveIntensity={0.8} />
      </mesh>

      {/* 3D Model: Technology Tower (TT) */}
      <group
        position={[-0.65, 0.91, -0.55]}
        onClick={(e) => {
          e.stopPropagation();
          openExhibitById('acad-tt');
        }}
      >
        <mesh position={[0, 0.31, 0]} castShadow>
          <boxGeometry args={[0.65, 0.62, 0.45]} />
          <meshStandardMaterial color="#1e3a8a" roughness={0.25} metalness={0.3} />
        </mesh>
        <mesh position={[0, 0.31, 0]}>
          <boxGeometry args={[0.67, 0.52, 0.41]} />
          <meshStandardMaterial color="#0f172a" roughness={0.1} metalness={0.85} />
        </mesh>
        <mesh position={[0, 0.66, 0]} castShadow>
          <boxGeometry args={[0.55, 0.08, 0.40]} />
          <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.8} />
        </mesh>
      </group>

      {/* 3D Model: Silver Jubilee Tower (SJT) */}
      <group
        position={[0.55, 0.91, -0.55]}
        onClick={(e) => {
          e.stopPropagation();
          openExhibitById('acad-sjt');
        }}
      >
        <mesh position={[0, 0.35, 0]} castShadow>
          <boxGeometry args={[0.68, 0.70, 0.45]} />
          <meshStandardMaterial color="#e2e8f0" roughness={0.3} />
        </mesh>
        <mesh position={[0, 0.77, 0]} castShadow>
          <boxGeometry args={[0.48, 0.24, 0.35]} />
          <meshStandardMaterial color="#1e3a8a" roughness={0.2} metalness={0.2} />
        </mesh>
        <mesh position={[0, 0.94, 0]}>
          <cylinderGeometry args={[0.018, 0.018, 0.18, 12]} />
          <meshStandardMaterial color="#d4af37" roughness={0.1} metalness={0.9} />
        </mesh>
      </group>

      {/* Standing Photo Plinths */}
      <group position={[-0.65, 0.91, -0.05]}>
        <mesh position={[0, 0.01, 0]}>
          <boxGeometry args={[0.46, 0.02, 0.06]} />
          <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.8} />
        </mesh>
        <mesh position={[0, 0.15, 0]}>
          <planeGeometry args={[0.42, 0.28]} />
          <meshStandardMaterial map={ttTex} side={THREE.DoubleSide} />
        </mesh>
      </group>

      <group position={[0.55, 0.91, -0.05]}>
        <mesh position={[0, 0.01, 0]}>
          <boxGeometry args={[0.46, 0.02, 0.06]} />
          <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.8} />
        </mesh>
        <mesh position={[0, 0.15, 0]}>
          <planeGeometry args={[0.42, 0.28]} />
          <meshStandardMaterial map={sjtTex} side={THREE.DoubleSide} />
        </mesh>
      </group>

      <group position={[-1.15, 0.91, 0.75]}>
        <mesh position={[0, 0.01, 0]}>
          <boxGeometry args={[0.46, 0.02, 0.06]} />
          <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.8} />
        </mesh>
        <mesh position={[0, 0.15, 0]}>
          <planeGeometry args={[0.42, 0.28]} />
          <meshStandardMaterial map={adminTex} side={THREE.DoubleSide} />
        </mesh>
      </group>

      <group position={[1.15, 0.91, 0.75]}>
        <mesh position={[0, 0.01, 0]}>
          <boxGeometry args={[0.46, 0.02, 0.06]} />
          <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.8} />
        </mesh>
        <mesh position={[0, 0.15, 0]}>
          <planeGeometry args={[0.42, 0.28]} />
          <meshStandardMaterial map={libTex} side={THREE.DoubleSide} />
        </mesh>
      </group>
    </group>
  );
}

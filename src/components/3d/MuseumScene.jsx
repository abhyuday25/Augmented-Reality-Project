import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { Environment } from '@react-three/drei';
import * as THREE from 'three';

import { MuseumArchitecture } from './MuseumArchitecture';
import { SchoolsBackWall } from './SchoolsBackWall';
import { BotanicalPlant } from './BotanicalPlant';
import { MuseumBench } from './MuseumBench';
import { CampusMasterplanDiorama } from './CampusMasterplanDiorama';
import { SpatialHotspots } from './SpatialHotspots';
import { CameraController } from './CameraController';

export function MuseumScene() {
  // Botanical Plant positions across Floor 1 & Floor 2
  const plantPositions = [
    [-8.5, 0, 17.0],
    [8.5, 0, 17.0],
    [-8.5, 0, 11.5],
    [8.5, 0, 11.5],
    [-6.5, 0, 2.0],
    [6.5, 0, 2.0],
    // Floor 2 Balcony planters
    [-11.5, 5.0, 4.0],
    [11.5, 5.0, 4.0],
  ];

  // Bench positions
  const benchPositions = [
    { pos: [-7.5, 0, 14.5], rot: [0, 0, 0] },
    { pos: [0.0, 0, 16.5], rot: [0, 0, 0] },
    { pos: [-6.0, 0, -7.0], rot: [0, Math.PI / 2, 0] },
    { pos: [6.0, 0, -7.0], rot: [0, -Math.PI / 2, 0] },
  ];

  return (
    <Canvas
      shadows
      dpr={[1, 1.25]}
      camera={{ position: [0, 1.6, 15.0], fov: 60, near: 0.1, far: 180 }}
      gl={{
        antialias: true,
        toneMapping: THREE.ACESFilmicToneMapping,
        toneMappingExposure: 1.15,
        powerPreference: 'high-performance',
      }}
      style={{ width: '100vw', height: '100vh', position: 'fixed', inset: 0, zIndex: 1 }}
    >
      <color attach="background" args={['#050914']} />
      <fog attach="fog" args={['#050914', 35, 95]} />

      <Suspense fallback={null}>
        {/* Cinema-Grade HDR Environment & Studio Skylight */}
        <Environment preset="city" environmentIntensity={0.65} />

        <ambientLight intensity={0.55} color="#e0f2fe" />
        <directionalLight
          position={[6, 14, 8]}
          intensity={1.2}
          castShadow
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
          shadow-bias={-0.0001}
          shadow-camera-near={0.5}
          shadow-camera-far={45}
          shadow-camera-left={-22}
          shadow-camera-right={22}
          shadow-camera-top={22}
          shadow-camera-bottom={-22}
        />
        {/* Fill light for northern gallery and back wall */}
        <directionalLight position={[-4, 10, -10]} intensity={0.7} color="#f8fafc" />

        {/* 3D Scene Primitives */}
        <MuseumArchitecture />
        <SchoolsBackWall />
        <CampusMasterplanDiorama position={[0, 0, 4.2]} />

        {plantPositions.map((pos, idx) => (
          <BotanicalPlant key={`plant-${idx}`} position={pos} scale={1.05} />
        ))}

        {benchPositions.map((b, idx) => (
          <MuseumBench key={`bench-${idx}`} position={b.pos} rotation={b.rot} />
        ))}

        {/* 3D Interactive Hotspot Pins */}
        <SpatialHotspots />

        {/* First-Person Ultra-Smooth Camera Controller */}
        <CameraController />
      </Suspense>
    </Canvas>
  );
}

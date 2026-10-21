import React, { useRef, useMemo } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import * as THREE from 'three';

export function BotanicalPlant({ position = [0, 0, 0], scale = 1.0 }) {
  const foliageRef = useRef();

  // Load botanical leaf texture
  const leafTexture = useLoader(THREE.TextureLoader, '/src/assets/images/vit/botanical_foliage.jpg');
  leafTexture.colorSpace = THREE.SRGBColorSpace;

  // Lightweight foliage sway (sway entire group instead of 14 separate mesh traversals)
  useFrame(({ clock }) => {
    if (foliageRef.current) {
      const t = clock.getElapsedTime();
      foliageRef.current.rotation.z = Math.sin(t * 1.1) * 0.02;
    }
  });

  // Generate 14 natural radially tiered leaf fronds
  const leaves = useMemo(() => {
    const list = [];
    const count = 14;
    for (let i = 0; i < count; i++) {
      const tier = Math.floor(i / 5);
      let pitch, yOff, len, width, rad;
      if (tier === 0) {
        pitch = -0.55;
        yOff = 0.76 + i * 0.03;
        len = 0.58;
        width = 0.36;
        rad = 0.14;
      } else if (tier === 1) {
        pitch = -0.18;
        yOff = 0.94 + (i - 5) * 0.04;
        len = 0.52;
        width = 0.34;
        rad = 0.12;
      } else {
        pitch = 0.45;
        yOff = 1.15 + (i - 10) * 0.05;
        len = 0.44;
        width = 0.30;
        rad = 0.08;
      }

      const yaw = i * ((Math.PI * 2) / count) + 0.15 * Math.sin(i * 1.5);
      const roll = 0.12 * Math.sin(i * 2.3);

      list.push({
        id: i,
        yaw,
        pitch,
        roll,
        x: rad * Math.sin(yaw),
        y: yOff,
        z: rad * Math.cos(yaw),
        width,
        len,
      });
    }
    return list;
  }, []);

  return (
    <group position={position} scale={scale}>
      {/* Modern Fluted Ceramic Planter Pot */}
      <mesh position={[0, 0.36, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[0.36, 0.30, 0.72, 16]} />
        <meshStandardMaterial color="#f8fafc" roughness={0.25} metalness={0.05} />
      </mesh>

      {/* Polished Brass Collar Trim */}
      <mesh position={[0, 0.70, 0]}>
        <cylinderGeometry args={[0.39, 0.39, 0.05, 16]} />
        <meshStandardMaterial color="#d4af37" roughness={0.2} metalness={0.85} />
      </mesh>

      {/* Organic Dark Potting Soil */}
      <mesh position={[0, 0.69, 0]}>
        <cylinderGeometry args={[0.35, 0.35, 0.03, 14]} />
        <meshStandardMaterial color="#1c1917" roughness={0.9} metalness={0.0} />
      </mesh>

      {/* Central Woody Stem */}
      <mesh position={[0, 1.05, 0]}>
        <cylinderGeometry args={[0.025, 0.025, 0.85, 8]} />
        <meshStandardMaterial color="#451a03" roughness={0.8} />
      </mesh>

      {/* Tiered Botanical Foliage with Lightweight Standard Material (No expensive SSS transmission pass) */}
      <group ref={foliageRef}>
        {leaves.map((leaf) => (
          <mesh
            key={leaf.id}
            position={[leaf.x, leaf.y, leaf.z]}
            rotation={[leaf.pitch, leaf.yaw, leaf.roll]}
          >
            <planeGeometry args={[leaf.width, leaf.len]} />
            <meshStandardMaterial
              map={leafTexture}
              roughness={0.4}
              metalness={0.05}
              side={THREE.DoubleSide}
              transparent
              alphaTest={0.15}
            />
          </mesh>
        ))}
      </group>
    </group>
  );
}

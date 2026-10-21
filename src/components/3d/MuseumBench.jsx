import React from 'react';

export function MuseumBench({ position = [0, 0, 0], rotation = [0, 0, 0] }) {
  return (
    <group position={position} rotation={rotation}>
      {/* Walnut Wood Seating Plank */}
      <mesh position={[0, 0.45, 0]} castShadow receiveShadow>
        <boxGeometry args={[2.4, 0.12, 0.7]} />
        <meshStandardMaterial
          color="#3f2716"
          roughness={0.35}
          metalness={0.05}
        />
      </mesh>

      {/* Chrome Legs Left & Right */}
      <mesh position={[-1.0, 0.2, 0]} castShadow>
        <boxGeometry args={[0.1, 0.4, 0.6]} />
        <meshStandardMaterial color="#e2e8f0" roughness={0.12} metalness={0.92} />
      </mesh>
      <mesh position={[1.0, 0.2, 0]} castShadow>
        <boxGeometry args={[0.1, 0.4, 0.6]} />
        <meshStandardMaterial color="#e2e8f0" roughness={0.12} metalness={0.92} />
      </mesh>
    </group>
  );
}

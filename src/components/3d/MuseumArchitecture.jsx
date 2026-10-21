import React, { useEffect, useMemo, useRef } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import { useMuseumStore } from '../../store/useMuseumStore';
import { INTERACTION_REGISTRY } from '../../data/museumContent.js';

/**
 * Creates high-res procedural dark polished marble floor texture with architectural grid pattern.
 * Aligns perfectly with the museum's 4-meter grid repeat.
 */
function createLuxuryDarkMarbleTexture() {
  const canvas = document.createElement('canvas');
  canvas.width = 1024;
  canvas.height = 1024;
  const ctx = canvas.getContext('2d');

  // Deep dark polished marble base (Floor 1 black aesthetic)
  ctx.fillStyle = '#080c16';
  ctx.fillRect(0, 0, 1024, 1024);

  // Subtle organic marble veining
  ctx.strokeStyle = 'rgba(28, 43, 68, 0.55)';
  ctx.lineWidth = 16;
  ctx.filter = 'blur(8px)';
  for (let i = 0; i < 6; i++) {
    ctx.beginPath();
    ctx.moveTo(0, (i * 180 + 35) % 1024);
    ctx.bezierCurveTo(
      320, (i * 180 + 170) % 1024,
      680, (i * 180 - 70 + 1024) % 1024,
      1024, (i * 180 + 80) % 1024
    );
    ctx.stroke();
  }
  ctx.filter = 'none';

  // Crisp architectural tile grid (256x256 px = 4m x 4m)
  const tileSize = 256;
  ctx.lineWidth = 3;
  ctx.strokeStyle = '#1e293b';
  for (let x = 0; x <= 1024; x += tileSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, 1024);
    ctx.stroke();
  }
  for (let y = 0; y <= 1024; y += tileSize) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(1024, y);
    ctx.stroke();
  }

  // Inner tile luxury bevel borders & metallic corner accents
  for (let x = 0; x < 1024; x += tileSize) {
    for (let y = 0; y < 1024; y += tileSize) {
      // Dark slate inlay line
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = 'rgba(51, 65, 85, 0.7)';
      ctx.strokeRect(x + 12, y + 12, tileSize - 24, tileSize - 24);

      // Delicate gold corner accents
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = 'rgba(212, 175, 55, 0.45)';
      const cl = 18;
      // Top-left corner
      ctx.beginPath();
      ctx.moveTo(x + 12, y + 12 + cl);
      ctx.lineTo(x + 12, y + 12);
      ctx.lineTo(x + 12 + cl, y + 12);
      ctx.stroke();
      // Bottom-right corner
      ctx.beginPath();
      ctx.moveTo(x + tileSize - 12 - cl, y + tileSize - 12);
      ctx.lineTo(x + tileSize - 12, y + tileSize - 12);
      ctx.lineTo(x + tileSize - 12, y + tileSize - 12 - cl);
      ctx.stroke();
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.anisotropy = 8;
  return texture;
}

/**
 * Projects world coordinates (X, Z) into UV space so tiles across all floor meshes
 * align seamlessly to the 4m world grid.
 */
function applyWorldPlanarUVs(geometry) {
  if (!geometry || !geometry.attributes.position) return;
  const pos = geometry.attributes.position;
  const uvs = new Float32Array(pos.count * 2);
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i);
    const z = pos.getZ(i);
    uvs[i * 2] = (x + 19.0) / 4.0;
    uvs[i * 2 + 1] = (z + 17.5) / 4.0;
  }
  geometry.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
  geometry.uvsNeedUpdate = true;
}

export function MuseumArchitecture() {
  const { scene } = useGLTF('/src/assets/models/vit_vellore_virtual_museum.glb');
  const openExhibitById = useMuseumStore((state) => state.openExhibitById);

  // Shared dark marble material for Floor 1 & Floor 2
  const sharedFloorMaterial = useMemo(() => {
    const texture = createLuxuryDarkMarbleTexture();
    return new THREE.MeshStandardMaterial({
      color: new THREE.Color('#ffffff'),
      map: texture,
      roughness: 0.16,
      metalness: 0.08,
      side: THREE.DoubleSide,
    });
  }, []);

  useEffect(() => {
    if (!scene) return;

    scene.traverse((node) => {
      if (node.isMesh && node.geometry) {
        node.geometry.computeBoundingBox();
        const bb = node.geometry.boundingBox;
        const cx = (bb.min.x + bb.max.x) / 2;
        const cz = (bb.min.z + bb.max.z) / 2;
        const cy = (bb.min.y + bb.max.y) / 2;
        const mat = node.material;

        // 1. REMOVE PILLAR BLOCKING STAIRCASE ENTRANCE ON BOTH FLOORS (X ≈ 12.0, Z ≈ 6.0)
        // Spans Y: 0 to 9.8m across both floors (shaft, base, capital, and downlight)
        if (Math.abs(cx - 12.0) < 0.85 && Math.abs(cz - 6.0) < 0.85) {
          node.visible = false;
        }

        // 2. REMOVE INTERIOR DIVIDING WALL AT Z ≈ 8.5 CUTTING ACROSS STAIRCASE
        // Mesh 1 Prim 12: X: [10.0, 18.5], Z: [8.2, 8.8], Y: [0, 10.0]
        if (bb.min.x >= 9.5 && bb.max.x <= 19.0 && Math.abs(cz - 8.5) < 0.5 && (bb.max.y - bb.min.y) > 6.0) {
          node.visible = false;
        }

        // 2b. REMOVE LOBBY EAST WALL BLOCKING ATRIUM VIEW FROM STAIRCASE EXIT (X ≈ 10.5, Z: 8.5 to 18.0)
        // Mesh 1 Prim 10: X: [10.2, 10.8], Z: [8.5, 18.0], Y: [0, 10.0]
        if (bb.min.x >= 9.8 && bb.max.x <= 11.2 && bb.min.z >= 8.0 && bb.max.z <= 18.5 && (bb.max.y - bb.min.y) > 6.0) {
          node.visible = false;
        }

        // 3. HIDE SOLID FLOOR 2 EAST SLAB COVERING THE STAIRCASE
        // Mesh 1 Prim 2: X: [7.0, 19.0], Z: [-16.5, 14.5], Y: [4.65, 5.0]
        // This solid slab was hiding the entire staircase from Floor 2 view.
        if (bb.min.x >= 6.5 && bb.max.x >= 18.0 && bb.min.z <= -15.0 && bb.max.z >= 14.0 && bb.min.y >= 4.5 && bb.max.y <= 5.1) {
          node.visible = false;
        }

        // 4. FLOOR 1: APPLY SHARED LUXURY BLACK MARBLE & FIX NORMALS/UVS
        if (mat && mat.name && mat.name.toLowerCase().includes('floor1')) {
          applyWorldPlanarUVs(node.geometry);
          // Ensure normals point up (+Y)
          const normAttr = node.geometry.attributes.normal;
          if (normAttr) {
            for (let i = 1; i < normAttr.array.length; i += 3) {
              if (normAttr.array[i] < 0) normAttr.array[i] = 1.0;
            }
            normAttr.needsUpdate = true;
          }
          node.material = sharedFloorMaterial;
          node.receiveShadow = true;
          node.castShadow = false;
        }

        // 5. FLOOR 2: APPLY IDENTICAL LUXURY BLACK MARBLE PATTERN (West, North, South slabs)
        if (mat && mat.name && (mat.name.toLowerCase().includes('floor2') || mat.name.toLowerCase().includes('stone'))) {
          if (node.name.includes('Floor') || node.parent?.name.includes('Structure') || mat.name.includes('Floor2')) {
            applyWorldPlanarUVs(node.geometry);
            node.material = sharedFloorMaterial;
            node.receiveShadow = true;
            node.castShadow = false;
          }
        }

        // 6. GOLD TRIM POLISH
        if (mat && mat.name && mat.name.includes('Gold')) {
          mat.roughness = 0.22;
          mat.metalness = 0.88;
        }

        // 7. OPTIMIZE SHADOWS
        if (mat && mat.name && (mat.name.includes('Floor') || mat.name.includes('floor'))) {
          node.receiveShadow = true;
          node.castShadow = false;
        } else if (node.name && (node.name.includes('Sculpture') || node.name.includes('Monument') || node.name.includes('Table'))) {
          node.castShadow = true;
          node.receiveShadow = true;
        } else {
          node.castShadow = false;
          node.receiveShadow = true;
        }
      }
    });
  }, [scene, sharedFloorMaterial]);

  const handleClick = (e) => {
    e.stopPropagation();
    let current = e.object;
    while (current) {
      if (current.name && INTERACTION_REGISTRY[current.name]) {
        const item = INTERACTION_REGISTRY[current.name];
        if (item.exhibitId) {
          openExhibitById(item.exhibitId);
          return;
        }
      }
      current = current.parent;
    }
  };

  return (
    <group>
      {/* Base GLTF Scene */}
      <primitive object={scene} onClick={handleClick} />

      {/* Floor 2 East Mezzanine Slabs with Grand Staircase Cutout (Open on both floors) */}
      <group>
        {/* North East Gallery: X: [7.0, 19.0], Z: [-16.5, 6.8] */}
        <mesh
          position={[13.0, 4.825, -4.85]}
          receiveShadow
          material={sharedFloorMaterial}
          ref={(m) => m && applyWorldPlanarUVs(m.geometry)}
        >
          <boxGeometry args={[12.0, 0.35, 23.3]} />
        </mesh>

        {/* West Walkway along Atrium: X: [7.0, 10.8], Z: [6.8, 14.5] */}
        <mesh
          position={[8.9, 4.825, 10.65]}
          receiveShadow
          material={sharedFloorMaterial}
          ref={(m) => m && applyWorldPlanarUVs(m.geometry)}
        >
          <boxGeometry args={[3.8, 0.35, 7.7]} />
        </mesh>

        {/* East Walkway / Elevator Corridor: X: [14.2, 19.0], Z: [6.8, 14.5] */}
        <mesh
          position={[16.6, 4.825, 10.65]}
          receiveShadow
          material={sharedFloorMaterial}
          ref={(m) => m && applyWorldPlanarUVs(m.geometry)}
        >
          <boxGeometry args={[4.8, 0.35, 7.7]} />
        </mesh>

        {/* South Landing top of Grand Staircase: X: [7.0, 19.0], Z: [14.5, 17.5] */}
        <mesh
          position={[13.0, 4.825, 16.0]}
          receiveShadow
          material={sharedFloorMaterial}
          ref={(m) => m && applyWorldPlanarUVs(m.geometry)}
        >
          <boxGeometry args={[12.0, 0.35, 3.0]} />
        </mesh>
      </group>
    </group>
  );
}

useGLTF.preload('/src/assets/models/vit_vellore_virtual_museum.glb');

import React, { useEffect } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import { useMuseumStore } from '../../store/useMuseumStore';
import { INTERACTION_REGISTRY } from '../../data/museumContent.js';

export function MuseumArchitecture() {
  const { scene } = useGLTF('/src/assets/models/vit_vellore_virtual_museum.glb');
  const openExhibitById = useMuseumStore((state) => state.openExhibitById);

  useEffect(() => {
    if (!scene) return;

    // 1. Find Floor 1 marble material to match Floor 2 color & texture
    let floor1Material = null;
    scene.traverse((node) => {
      if (node.isMesh && node.material) {
        const mat = node.material;
        if (mat.name && mat.name.toLowerCase().includes('floor1')) {
          floor1Material = mat;
        }
      }
    });

    // 2. Apply Floor 1 marble material to Floor 2 and optimize shadow passes
    scene.traverse((node) => {
      if (node.isMesh && node.material) {
        const mat = node.material;

        // Match Floor 2 with Floor 1
        if (mat.name && (mat.name.toLowerCase().includes('floor2') || mat.name.toLowerCase().includes('stone'))) {
          if (floor1Material) {
            node.material = floor1Material;
          } else {
            mat.color.set('#f2f3f6');
            mat.roughness = 0.18;
            mat.metalness = 0.05;
          }
        }

        // Gold trim polish
        if (mat.name && mat.name.includes('Gold')) {
          mat.roughness = 0.22;
          mat.metalness = 0.88;
        }

        // Only receive shadows on floors/plinths; avoid expensive self-shadowing on large walls
        if (mat.name && (mat.name.includes('Floor') || mat.name.includes('floor'))) {
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
  }, [scene]);

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

  return <primitive object={scene} onClick={handleClick} />;
}

useGLTF.preload('/src/assets/models/vit_vellore_virtual_museum.glb');

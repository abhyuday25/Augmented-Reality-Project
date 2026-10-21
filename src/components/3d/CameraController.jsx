import React, { useRef, useEffect } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
import { useMuseumStore } from '../../store/useMuseumStore';

/**
 * 2-Floor Architectural Navigation Constraints
 * Smooth S-Curve Staircase Ramp, Boundary Clamping, and Atrium Cutout
 */
function constrainPosition(x, z, currentY) {
  let clampedX = Math.max(-18.2, Math.min(18.2, x));
  let clampedZ = Math.max(-16.2, Math.min(16.2, z));
  let camY = currentY;

  // 1. Grand Staircase traversal zone: x in [10.2, 14.8], z in [6.6, 14.8]
  const inStairs = clampedX >= 10.2 && clampedX <= 14.8 && clampedZ >= 6.6 && clampedZ <= 14.8;
  if (inStairs) {
    const t = Math.max(0, Math.min(1, (clampedZ - 6.8) / (14.5 - 6.8)));
    const smoothT = t * t * (3 - 2 * t);
    camY = smoothT * 5.0 + 1.6;
  } else if (currentY >= 4.0) {
    // Floor 2 Mezzanine level (eye height = 6.6m)
    camY = 6.6;
    // Floor 2 Central Atrium hole protection: x in [-7.2, 7.2], z in [-6.2, 5.2]
    if (clampedX > -7.2 && clampedX < 7.2 && clampedZ > -6.2 && clampedZ < 5.2) {
      const distLeft = Math.abs(clampedX - -7.2);
      const distRight = Math.abs(7.2 - clampedX);
      const distTop = Math.abs(5.2 - clampedZ);
      const distBottom = Math.abs(clampedZ - -6.2);
      const minDist = Math.min(distLeft, distRight, distTop, distBottom);
      if (minDist === distLeft) clampedX = -7.2;
      else if (minDist === distRight) clampedX = 7.2;
      else if (minDist === distTop) clampedZ = 5.2;
      else clampedZ = -6.2;
    }
  } else {
    // Floor 1 ground level (eye height = 1.6m)
    camY = 1.6;
  }

  return { x: clampedX, y: camY, z: clampedZ };
}

export function CameraController() {
  const { camera, gl } = useThree();
  const cameraTarget = useMuseumStore((state) => state.cameraTarget);

  // First-Person Camera State (Refs = Zero React re-renders in render loop!)
  const position = useRef(new THREE.Vector3(0, 1.6, 15));
  const yaw = useRef(0);
  const pitch = useRef(0);
  const isDragging = useRef(false);
  const prevMouse = useRef({ x: 0, y: 0 });
  const keysDown = useRef(new Set());

  // Tour Waypoint Animation State
  const isTransitioning = useRef(false);
  const transitionStartPos = useRef(new THREE.Vector3());
  const transitionEndPos = useRef(new THREE.Vector3());
  const transitionStartYaw = useRef(0);
  const transitionEndYaw = useRef(0);
  const transitionStartPitch = useRef(0);
  const transitionEndPitch = useRef(0);
  const transitionProgress = useRef(1);
  const transitionDuration = useRef(1.2); // seconds

  // Throttled player position tracking for 2D Map
  const lastStoreSync = useRef(0);

  // Initialize camera position
  useEffect(() => {
    camera.rotation.order = 'YXZ';
    camera.position.set(0, 1.6, 15);
    camera.rotation.set(0, 0, 0);
  }, [camera]);

  // Handle waypoint navigation from store (Tour Stops, Floor Switch, Map Teleport)
  useEffect(() => {
    if (!cameraTarget?.position) return;

    const { position: targetPos, lookAt } = cameraTarget;
    const destX = targetPos[0];
    const destY = (targetPos[1] || 0) + 1.6; // Human eye height offset
    const destZ = targetPos[2];

    transitionStartPos.current.copy(position.current);
    transitionEndPos.current.set(destX, destY, destZ);

    transitionStartYaw.current = yaw.current;
    transitionStartPitch.current = pitch.current;

    if (lookAt) {
      const dx = lookAt[0] - destX;
      const dy = lookAt[1] - destY;
      const dz = lookAt[2] - destZ;
      const targetHeading = Math.atan2(-dx, -dz);
      const targetElevation = Math.atan2(dy, Math.hypot(dx, dz));

      // Shortest angle difference for yaw
      let diffYaw = (targetHeading - yaw.current) % (Math.PI * 2);
      if (diffYaw > Math.PI) diffYaw -= Math.PI * 2;
      if (diffYaw < -Math.PI) diffYaw += Math.PI * 2;

      transitionEndYaw.current = yaw.current + diffYaw;
      transitionEndPitch.current = targetElevation;
    } else {
      transitionEndYaw.current = yaw.current;
      transitionEndPitch.current = 0;
    }

    transitionProgress.current = 0;
    isTransitioning.current = true;
  }, [cameraTarget]);

  // Global Keyboard & Mouse Look Listeners
  useEffect(() => {
    const dom = gl.domElement;

    const handlePointerDown = (e) => {
      // Primary left click or touch starts mouse look
      if (e.button !== 0 && e.pointerType === 'mouse') return;
      isDragging.current = true;
      prevMouse.current = { x: e.clientX, y: e.clientY };
    };

    const handlePointerMove = (e) => {
      if (!isDragging.current) return;

      const deltaX = e.clientX - prevMouse.current.x;
      const deltaY = e.clientY - prevMouse.current.y;
      prevMouse.current = { x: e.clientX, y: e.clientY };

      // Look sensitivity matching legacy look-controls
      const sensitivity = 0.0028;
      yaw.current -= deltaX * sensitivity;
      pitch.current -= deltaY * sensitivity;

      // Clamp pitch so user cannot flip upside down (-85° to +85°)
      pitch.current = Math.max(-1.48, Math.min(1.48, pitch.current));

      // Cancel waypoint transition if user manually looks
      if (isTransitioning.current) {
        isTransitioning.current = false;
      }
    };

    const handlePointerUp = () => {
      isDragging.current = false;
    };

    const handleKeyDown = (e) => {
      if (
        document.activeElement?.tagName === 'INPUT' ||
        document.activeElement?.tagName === 'TEXTAREA'
      ) {
        return;
      }

      const code = e.code;
      const key = e.key.toLowerCase();

      // Movement keys
      if (
        [
          'KeyW',
          'KeyA',
          'KeyS',
          'KeyD',
          'ArrowUp',
          'ArrowDown',
          'ArrowLeft',
          'ArrowRight',
          'ShiftLeft',
          'ShiftRight',
        ].includes(code)
      ) {
        keysDown.current.add(code);
        // Cancel automated transition immediately
        if (isTransitioning.current) {
          isTransitioning.current = false;
        }
        if (useMuseumStore.getState().mode === 'tour') {
          useMuseumStore.getState().endTour();
        }
        return;
      }

      // Hotkey Actions
      const store = useMuseumStore.getState();
      if (key === 'm') {
        store.toggleMap();
      } else if (key === 't') {
        if (store.mode === 'tour') store.endTour();
        else store.startTour(0);
      } else if (key === 'h') {
        store.toggleMinimalHUD();
      } else if (key === 'e') {
        store.interactNearestExhibit();
      } else if (code === 'Space') {
        e.preventDefault();
        if (store.mode === 'tour') store.toggleTourPlayback();
      } else if (key === 'n') {
        if (store.mode === 'tour') store.nextTourStop();
      } else if (key === 'q') {
        if (store.mode === 'tour') store.prevTourStop();
      } else if (key === 'escape') {
        store.closeDrawer();
        store.toggleMap(false);
        store.toggleGuide(false);
        if (store.mode === 'tour') store.endTour();
      }
    };

    const handleKeyUp = (e) => {
      keysDown.current.delete(e.code);
    };

    const handleBlur = () => {
      keysDown.current.clear();
      isDragging.current = false;
    };

    dom.addEventListener('pointerdown', handlePointerDown);
    window.addEventListener('pointermove', handlePointerMove);
    window.addEventListener('pointerup', handlePointerUp);
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    window.addEventListener('blur', handleBlur);

    return () => {
      dom.removeEventListener('pointerdown', handlePointerDown);
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('pointerup', handlePointerUp);
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      window.removeEventListener('blur', handleBlur);
    };
  }, [gl]);

  // Frame Loop (WASD Walk + Smooth Waypoint Transitions)
  useFrame((_, delta) => {
    const dt = Math.min(delta, 0.1);

    // 1. Waypoint Transition (Tour & Fast-Travel)
    if (isTransitioning.current) {
      transitionProgress.current += dt / transitionDuration.current;
      const t = Math.min(1, transitionProgress.current);

      // Smooth ease-out cubic
      const ease = 1 - Math.pow(1 - t, 3);

      position.current.lerpVectors(
        transitionStartPos.current,
        transitionEndPos.current,
        ease
      );
      yaw.current = THREE.MathUtils.lerp(
        transitionStartYaw.current,
        transitionEndYaw.current,
        ease
      );
      pitch.current = THREE.MathUtils.lerp(
        transitionStartPitch.current,
        transitionEndPitch.current,
        ease
      );

      if (t >= 1) {
        isTransitioning.current = false;
      }
    }

    // 2. Free Walk (WASD + Virtual Joystick)
    let moveForward = 0;
    let moveStrafe = 0;

    const keys = keysDown.current;
    if (keys.has('KeyW') || keys.has('ArrowUp')) moveForward += 1;
    if (keys.has('KeyS') || keys.has('ArrowDown')) moveForward -= 1;
    if (keys.has('KeyD') || keys.has('ArrowRight')) moveStrafe += 1;
    if (keys.has('KeyA') || keys.has('ArrowLeft')) moveStrafe -= 1;

    const jVec = useMuseumStore.getState().joystickVector;
    if (jVec?.x || jVec?.y) {
      moveStrafe += jVec.x;
      moveForward += jVec.y;
    }

    if (moveForward !== 0 || moveStrafe !== 0) {
      const isShift = keys.has('ShiftLeft') || keys.has('ShiftRight');
      const speed = isShift ? 6.2 : 3.8; // m/s

      // Heading unit vector in horizontal XZ plane from current yaw
      const forwardX = -Math.sin(yaw.current);
      const forwardZ = -Math.cos(yaw.current);

      const rightX = Math.cos(yaw.current);
      const rightZ = -Math.sin(yaw.current);

      let dx = forwardX * moveForward + rightX * moveStrafe;
      let dz = forwardZ * moveForward + rightZ * moveStrafe;

      const len = Math.hypot(dx, dz);
      if (len > 1e-4) {
        dx = (dx / len) * speed * dt;
        dz = (dz / len) * speed * dt;

        const nextX = position.current.x + dx;
        const nextZ = position.current.z + dz;

        const constrained = constrainPosition(nextX, nextZ, position.current.y);
        position.current.set(constrained.x, constrained.y, constrained.z);
      }
    }

    // 3. Apply position and rotation to Three.js camera
    camera.position.copy(position.current);
    camera.rotation.set(pitch.current, yaw.current, 0, 'YXZ');

    // 4. Throttled update to Zustand store for 2D Map & Floor sync (every 250ms)
    const now = performance.now();
    if (now - lastStoreSync.current > 250) {
      lastStoreSync.current = now;
      const store = useMuseumStore.getState();
      store.setPlayerPosition([
        position.current.x,
        position.current.y,
        position.current.z,
      ]);
      const curFloor = position.current.y >= 4.0 ? 2 : 1;
      if (store.floor !== curFloor) {
        store.setFloorSilent(curFloor);
      }
    }
  });

  return null;
}

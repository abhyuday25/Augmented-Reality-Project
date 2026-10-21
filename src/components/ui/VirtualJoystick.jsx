import React, { useRef, useState, useEffect } from 'react';
import { useMuseumStore } from '../../store/useMuseumStore';

export function VirtualJoystick() {
  const baseRef = useRef(null);
  const stickRef = useRef(null);
  const [active, setActive] = useState(false);
  const [stickPos, setStickPos] = useState({ x: 0, y: 0 });
  const setJoystickVector = useMuseumStore((state) => state.setJoystickVector);
  const touchId = useRef(null);

  const radius = 45; // max stick radius

  const handleTouchStart = (e) => {
    if (touchId.current !== null) return;
    const touch = e.changedTouches[0];
    touchId.current = touch.identifier;
    setActive(true);
    updatePosition(touch.clientX, touch.clientY);
  };

  const handleTouchMove = (e) => {
    if (touchId.current === null) return;
    for (let i = 0; i < e.changedTouches.length; i++) {
      if (e.changedTouches[i].identifier === touchId.current) {
        updatePosition(e.changedTouches[i].clientX, e.changedTouches[i].clientY);
        break;
      }
    }
  };

  const handleTouchEnd = (e) => {
    if (touchId.current === null) return;
    for (let i = 0; i < e.changedTouches.length; i++) {
      if (e.changedTouches[i].identifier === touchId.current) {
        touchId.current = null;
        setActive(false);
        setStickPos({ x: 0, y: 0 });
        setJoystickVector({ x: 0, y: 0 });
        break;
      }
    }
  };

  const updatePosition = (clientX, clientY) => {
    if (!baseRef.current) return;
    const rect = baseRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const dx = clientX - centerX;
    const dy = clientY - centerY;
    const dist = Math.hypot(dx, dy);

    let clampedX = dx;
    let clampedY = dy;
    if (dist > radius) {
      clampedX = (dx / dist) * radius;
      clampedY = (dy / dist) * radius;
    }

    setStickPos({ x: clampedX, y: clampedY });
    // Normalize vector: x is strafe (-1 to +1), y is forward/backward (+1 to -1)
    setJoystickVector({
      x: clampedX / radius,
      y: -clampedY / radius,
    });
  };

  return (
    <div
      ref={baseRef}
      className={`virtualJoystickBase ${active ? 'is-active' : ''}`}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      onTouchCancel={handleTouchEnd}
      aria-label="Virtual Walk Joystick"
    >
      <div
        ref={stickRef}
        className="virtualJoystickStick"
        style={{
          transform: `translate(calc(-50% + ${stickPos.x}px), calc(-50% + ${stickPos.y}px))`,
        }}
      />
    </div>
  );
}

import React from 'react';
import { Html } from '@react-three/drei';
import { useMuseumStore } from '../../store/useMuseumStore';

const HOTSPOTS = [
  { id: 'campus-model', name: 'Campus Masterplan Diorama', pos: [0, 2.0, 4.2], floor: 1, stopIdx: 6 },
  { id: 'monument', name: 'Central Heritage Monument', pos: [0, 2.6, -2.0], floor: 1, stopIdx: 7 },
  { id: 'history', name: 'VIT History Timeline', pos: [-18.0, 2.8, -4.0], floor: 1, stopIdx: 1 },
  { id: 'academics', name: 'Academic Schools & Tech', pos: [18.0, 2.8, -4.0], floor: 1, stopIdx: 4 },
  { id: 'staircase', name: 'Grand Staircase (Floor 2)', pos: [12.5, 2.2, 8.5], floor: 1, stopIdx: 8 },
  { id: 'research', name: 'Research & Innovation Wing', pos: [-18.0, 7.8, -4.0], floor: 2, stopIdx: 9 },
  { id: 'achievements', name: 'Wall of Achievements', pos: [8.5, 7.8, -16.0], floor: 2, stopIdx: 11 },
  { id: 'student-life', name: 'Life at VIT & Motorsports', pos: [18.0, 7.8, -4.0], floor: 2, stopIdx: 13 },
];

export function SpatialHotspots() {
  const currentFloor = useMuseumStore((state) => state.floor);
  const goToTourStop = useMuseumStore((state) => state.goToTourStop);
  const startTour = useMuseumStore((state) => state.startTour);

  return (
    <group>
      {HOTSPOTS.filter((h) => h.floor === currentFloor).map((h) => (
        <group key={h.id} position={h.pos}>
          <Html center distanceFactor={14} zIndexRange={[10, 0]}>
            <div
              className="spatialPin"
              onClick={(e) => {
                e.stopPropagation();
                startTour(h.stopIdx);
              }}
              title={`Visit ${h.name}`}
            >
              <div className="spatialPin__radar"></div>
              <div className="spatialPin__core">
                <svg
                  className="spatialPin__icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.4"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M12 2v3m0 14v3M2 12h3m14 0h3"></path>
                </svg>
              </div>
              <div className="spatialPin__badge">
                <span className="spatialPin__name">{h.name}</span>
              </div>
            </div>
          </Html>
        </group>
      ))}
    </group>
  );
}

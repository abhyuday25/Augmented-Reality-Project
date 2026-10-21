import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMuseumStore } from '../../store/useMuseumStore';
import { X, MapPin, Compass, Navigation } from 'lucide-react';

export function MapModal() {
  const isMapOpen = useMuseumStore((state) => state.isMapOpen);
  const toggleMap = useMuseumStore((state) => state.toggleMap);
  const currentFloor = useMuseumStore((state) => state.floor);
  const playerPosition = useMuseumStore((state) => state.playerPosition);
  const [selectedFloor, setSelectedFloor] = useState(currentFloor);
  const tourStops = useMuseumStore((state) => state.tourStops);
  const startTour = useMuseumStore((state) => state.startTour);
  const flyTo = useMuseumStore((state) => state.flyTo);

  if (!isMapOpen) return null;

  const floorStops = tourStops.filter((s) => (s.floor || 1) === selectedFloor);

  // SVG Coordinate mapping: X in [-20, 20], Z in [-18, 18] -> 400x320 SVG
  const toSvgX = (x) => ((x + 20) / 40) * 400;
  const toSvgY = (z) => ((z + 18) / 36) * 320;

  const playerSvgX = toSvgX(playerPosition[0] || 0);
  const playerSvgY = toSvgY(playerPosition[2] || 0);
  const isPlayerOnSelectedFloor = currentFloor === selectedFloor;

  const handleSvgClick = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;
    const normX = clickX / rect.width;
    const normY = clickY / rect.height;

    // Map back to world X, Z
    const worldX = normX * 40 - 20;
    const worldZ = normY * 36 - 18;
    const worldY = selectedFloor === 2 ? 6.6 : 1.6;

    flyTo([worldX, worldY, worldZ], [0, selectedFloor === 2 ? 6.0 : 1.6, 0]);
    toggleMap(false);
  };

  return (
    <AnimatePresence>
      <div className="modalOverlay" onClick={() => toggleMap(false)}>
        <motion.div
          className="modalCard modalCard--map"
          initial={{ opacity: 0, scale: 0.94 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.94 }}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="modalHeader">
            <div>
              <div className="modalTitle">VIT Vellore Virtual Museum Map</div>
              <div className="modalSubtitle">Click any wing, pin, or floor spot to fast-travel</div>
            </div>
            <button className="modalCloseBtn" onClick={() => toggleMap(false)}>
              <X size={18} />
            </button>
          </div>

          {/* Floor Tabs */}
          <div className="mapFloorTabs">
            <button
              className={`mapFloorTab ${selectedFloor === 1 ? 'is-active' : ''}`}
              onClick={() => setSelectedFloor(1)}
            >
              Floor 1: Heritage & Academics
            </button>
            <button
              className={`mapFloorTab ${selectedFloor === 2 ? 'is-active' : ''}`}
              onClick={() => setSelectedFloor(2)}
            >
              Floor 2: Research & Student Life
            </button>
          </div>

          {/* Interactive SVG Blueprint Map */}
          <div className="mapBlueprintWrapper">
            <svg
              className="mapBlueprintSvg"
              viewBox="0 0 400 320"
              onClick={handleSvgClick}
              title="Click anywhere to fast-travel"
            >
              {/* Outer Gallery Perimeter */}
              <rect
                x="20"
                y="16"
                width="360"
                height="288"
                rx="14"
                fill="rgba(10, 20, 40, 0.75)"
                stroke="rgba(212, 175, 55, 0.4)"
                strokeWidth="2"
              />

              {/* Central Atrium / Opening */}
              <rect
                x="130"
                y="105"
                width="140"
                height="100"
                rx="8"
                fill={selectedFloor === 2 ? 'rgba(5, 10, 20, 0.9)' : 'rgba(30, 58, 138, 0.2)'}
                stroke={selectedFloor === 2 ? '#ef4444' : 'rgba(59, 130, 246, 0.4)'}
                strokeWidth="1.5"
                strokeDasharray={selectedFloor === 2 ? '4 4' : 'none'}
              />
              <text
                x="200"
                y="155"
                textAnchor="middle"
                fill="rgba(255, 255, 255, 0.45)"
                fontSize="10"
                fontWeight="600"
              >
                {selectedFloor === 2 ? 'OPEN ATRIUM VOID' : 'CAMPUS DIORAMA'}
              </text>

              {/* Grand Staircase Zone */}
              <rect
                x="302"
                y="218"
                width="46"
                height="70"
                rx="4"
                fill="rgba(212, 175, 55, 0.15)"
                stroke="rgba(212, 175, 55, 0.5)"
                strokeWidth="1"
              />
              <text
                x="325"
                y="256"
                textAnchor="middle"
                fill="var(--gold)"
                fontSize="8"
                fontWeight="700"
              >
                STAIRS
              </text>

              {/* Tour Stops on this floor */}
              {floorStops.map((stop) => {
                const sx = toSvgX(stop.targetPosition?.[0] || 0);
                const sy = toSvgY(stop.targetPosition?.[2] || 0);
                return (
                  <g
                    key={stop.id}
                    className="mapSvgPin"
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleMap(false);
                      startTour(stop.order - 1);
                    }}
                    style={{ cursor: 'pointer' }}
                  >
                    <circle cx={sx} cy={sy} r="9" fill="var(--gold)" stroke="#fff" strokeWidth="1.5" />
                    <text
                      x={sx}
                      y={sy + 3.5}
                      textAnchor="middle"
                      fill="#060a12"
                      fontSize="9"
                      fontWeight="800"
                    >
                      {stop.order}
                    </text>
                  </g>
                );
              })}

              {/* Live Player Position Beacon */}
              {isPlayerOnSelectedFloor && (
                <g className="mapPlayerBeacon">
                  <circle
                    cx={playerSvgX}
                    cy={playerSvgY}
                    r="12"
                    fill="none"
                    stroke="#3b82f6"
                    strokeWidth="2"
                    opacity="0.8"
                  >
                    <animate
                      attributeName="r"
                      values="6;16;6"
                      dur="2s"
                      repeatCount="indefinite"
                    />
                    <animate
                      attributeName="opacity"
                      values="0.9;0.1;0.9"
                      dur="2s"
                      repeatCount="indefinite"
                    />
                  </circle>
                  <circle cx={playerSvgX} cy={playerSvgY} r="5" fill="#3b82f6" stroke="#ffffff" strokeWidth="1.5" />
                </g>
              )}
            </svg>
            <div className="mapBlueprintLegend">
              <span className="legendItem">
                <span className="legendDot legendDot--gold" /> Tour Stop
              </span>
              <span className="legendItem">
                <span className="legendDot legendDot--player" /> You Are Here
              </span>
              <span className="legendItem">
                <span className="legendDot legendDot--stairs" /> Grand Staircase
              </span>
            </div>
          </div>

          {/* Stops List */}
          <div className="mapStopsGrid">
            {floorStops.map((stop) => (
              <div
                key={stop.id}
                className="mapStopItem"
                onClick={() => {
                  toggleMap(false);
                  startTour(stop.order - 1);
                }}
              >
                <div className="mapStopItem__num">
                  {String(stop.order).padStart(2, '0')}
                </div>
                <div className="mapStopItem__content">
                  <div className="mapStopItem__title">{stop.title}</div>
                  <div className="mapStopItem__sub">{stop.subtitle}</div>
                </div>
                <MapPin size={16} className="mapStopItem__icon" />
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}

import React from 'react';
import { useMuseumStore } from '../../store/useMuseumStore';
import { Compass, Footprints, Map, Layers, RotateCcw, Volume2, VolumeX, HelpCircle, Eye } from 'lucide-react';

export function DockToolbar() {
  const mode = useMuseumStore((state) => state.mode);
  const floor = useMuseumStore((state) => state.floor);
  const isMinimalHUD = useMuseumStore((state) => state.isMinimalHUD);
  const startTour = useMuseumStore((state) => state.startTour);
  const endTour = useMuseumStore((state) => state.endTour);
  const setFloor = useMuseumStore((state) => state.setFloor);
  const toggleMap = useMuseumStore((state) => state.toggleMap);
  const toggleGuide = useMuseumStore((state) => state.toggleGuide);
  const audioMuted = useMuseumStore((state) => state.audioMuted);
  const toggleAudio = useMuseumStore((state) => state.toggleAudio);
  const flyTo = useMuseumStore((state) => state.flyTo);

  if (isMinimalHUD) return null;

  const handleTourToggle = () => {
    if (mode === 'tour') {
      endTour();
    } else {
      startTour(0);
    }
  };

  const handleReset = () => {
    flyTo([0, 1.6, 15.0], [0, 1.8, 10.7]);
  };

  return (
    <nav className="dockToolbar" aria-label="Museum Navigation Toolbar">
      {/* Free Explore button */}
      <button
        className={`dockToolbar__btn ${mode === 'explore' ? 'is-active' : ''}`}
        onClick={() => {
          if (mode === 'tour') endTour();
        }}
        title="Free Walk & Explore (WASD)"
      >
        <Footprints size={18} />
        <span>Explore</span>
      </button>

      {/* Guided Tour button */}
      <button
        className={`dockToolbar__btn ${mode === 'tour' ? 'is-active' : ''}`}
        onClick={handleTourToggle}
        title="Guided 16-Stop Tour (T)"
      >
        <Compass size={18} />
        <span>Tour</span>
      </button>

      <button className="dockToolbar__btn" onClick={() => toggleMap(true)} title="Interactive 2-Floor Map (M)">
        <Map size={18} />
        <span>Map</span>
      </button>

      <button
        className="dockToolbar__btn"
        onClick={() => setFloor(floor === 1 ? 2 : 1)}
        title="Switch Floors"
      >
        <Layers size={18} />
        <span>Floor {floor}</span>
      </button>

      <div className="dockToolbar__divider" />

      <button className="dockToolbar__btn" onClick={handleReset} title="Reset Camera View">
        <RotateCcw size={18} />
        <span>Reset</span>
      </button>

      <button
        className="dockToolbar__btn"
        onClick={toggleAudio}
        title={audioMuted ? 'Unmute Sound & TTS' : 'Mute Sound & TTS'}
      >
        {audioMuted ? <VolumeX size={18} /> : <Volume2 size={18} />}
        <span>{audioMuted ? 'Muted' : 'Sound'}</span>
      </button>

      <button className="dockToolbar__btn" onClick={() => toggleGuide(true)} title="Visitor Guide & Keys (H)">
        <HelpCircle size={18} />
        <span>Guide</span>
      </button>
    </nav>
  );
}

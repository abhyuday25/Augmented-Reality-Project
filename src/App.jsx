import React from 'react';
import { MuseumScene } from './components/3d/MuseumScene';
import { TopHUD } from './components/ui/TopHUD';
import { DockToolbar } from './components/ui/DockToolbar';
import { ExhibitDrawer } from './components/ui/ExhibitDrawer';
import { TourStopCard } from './components/ui/TourStopCard';
import { MapModal } from './components/ui/MapModal';
import { VisitorGuideModal } from './components/ui/VisitorGuideModal';
import { VirtualJoystick } from './components/ui/VirtualJoystick';
import './index.css';

export default function App() {
  return (
    <div className="museumApp">
      {/* 3D WebGL Canvas Layer */}
      <MuseumScene />

      {/* Modern UI Layer */}
      <div className="museumUILayer">
        <TopHUD />
        <ExhibitDrawer />
        <TourStopCard />
        <DockToolbar />
        <MapModal />
        <VisitorGuideModal />
        <VirtualJoystick />
      </div>
    </div>
  );
}

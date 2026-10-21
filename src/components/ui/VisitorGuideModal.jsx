import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMuseumStore } from '../../store/useMuseumStore';
import { X, Compass, MousePointer, Eye, Footprints, Keyboard } from 'lucide-react';

export function VisitorGuideModal() {
  const isGuideOpen = useMuseumStore((state) => state.isGuideOpen);
  const toggleGuide = useMuseumStore((state) => state.toggleGuide);

  if (!isGuideOpen) return null;

  return (
    <AnimatePresence>
      <div className="modalOverlay" onClick={() => toggleGuide(false)}>
        <motion.div
          className="modalCard modalCard--guide"
          initial={{ opacity: 0, scale: 0.94 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.94 }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="modalHeader">
            <div>
              <div className="modalTitle">Visitor Guide & Controls</div>
              <div className="modalSubtitle">How to explore the VIT Vellore 3D Virtual Museum</div>
            </div>
            <button className="modalCloseBtn" onClick={() => toggleGuide(false)}>
              <X size={18} />
            </button>
          </div>

          <div className="guideGrid">
            <div className="guideCard">
              <div className="guideCard__icon">
                <Footprints size={22} />
              </div>
              <div className="guideCard__title">Walk with WASD</div>
              <div className="guideCard__desc">
                Use <strong>W, A, S, D</strong> or <strong>Arrow Keys</strong> to walk freely across both floors. Hold <strong>Shift</strong> to sprint. Climb the grand staircase to reach the mezzanine level!
              </div>
            </div>

            <div className="guideCard">
              <div className="guideCard__icon">
                <MousePointer size={22} />
              </div>
              <div className="guideCard__title">Look Around & Zoom</div>
              <div className="guideCard__desc">
                Click and drag anywhere on the screen to look around in full 360°. Use your mouse wheel or pinch gesture to zoom in on exhibits.
              </div>
            </div>

            <div className="guideCard">
              <div className="guideCard__icon">
                <Compass size={22} />
              </div>
              <div className="guideCard__title">16-Stop Guided Tour</div>
              <div className="guideCard__desc">
                Press <strong>T</strong> or click <strong>Tour</strong> in the dock to start the sequential 16-stop tour through 40 years of VIT milestones.
              </div>
            </div>

            <div className="guideCard">
              <div className="guideCard__icon">
                <Eye size={22} />
              </div>
              <div className="guideCard__title">Interact with Exhibits</div>
              <div className="guideCard__desc">
                Press <strong>E</strong> or click any exhibit or golden radar hotspot to open its detail drawer on the left side of the screen.
              </div>
            </div>
          </div>

          {/* Quick Key Bindings Reference Table */}
          <div className="guideKeyTable">
            <div className="guideKeyTable__title">Keyboard Shortcuts</div>
            <div className="guideKeyTable__grid">
              <div className="guideKeyRow">
                <span className="keyPill">W A S D</span>
                <span className="keyDesc">Walk forward, left, backward, right</span>
              </div>
              <div className="guideKeyRow">
                <span className="keyPill">Shift</span>
                <span className="keyDesc">Sprint / Run faster</span>
              </div>
              <div className="guideKeyRow">
                <span className="keyPill">Mouse Drag</span>
                <span className="keyDesc">Rotate camera / 360° viewpoint</span>
              </div>
              <div className="guideKeyRow">
                <span className="keyPill">E</span>
                <span className="keyDesc">Inspect closest exhibit / advance tour</span>
              </div>
              <div className="guideKeyRow">
                <span className="keyPill">M</span>
                <span className="keyDesc">Open interactive 2-floor map</span>
              </div>
              <div className="guideKeyRow">
                <span className="keyPill">T</span>
                <span className="keyDesc">Toggle Guided Tour mode</span>
              </div>
              <div className="guideKeyRow">
                <span className="keyPill">Space</span>
                <span className="keyDesc">Pause / Resume tour auto-play</span>
              </div>
              <div className="guideKeyRow">
                <span className="keyPill">N / Q</span>
                <span className="keyDesc">Next stop (N) / Previous stop (Q)</span>
              </div>
              <div className="guideKeyRow">
                <span className="keyPill">H</span>
                <span className="keyDesc">Toggle Minimal HUD mode</span>
              </div>
              <div className="guideKeyRow">
                <span className="keyPill">Esc</span>
                <span className="keyDesc">Close panels / Exit tour</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}

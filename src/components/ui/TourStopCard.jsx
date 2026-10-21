import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMuseumStore } from '../../store/useMuseumStore';
import { X, ExternalLink, ChevronLeft, ChevronRight, BookOpen } from 'lucide-react';

export function TourStopCard() {
  const mode = useMuseumStore((state) => state.mode);
  const tourStops = useMuseumStore((state) => state.tourStops);
  const currentStopIdx = useMuseumStore((state) => state.currentStopIdx);
  const nextTourStop = useMuseumStore((state) => state.nextTourStop);
  const prevTourStop = useMuseumStore((state) => state.prevTourStop);
  const endTour = useMuseumStore((state) => state.endTour);
  const openExhibit = useMuseumStore((state) => state.openExhibit);
  const selectedExhibit = useMuseumStore((state) => state.selectedExhibit);

  if (mode !== 'tour') return null;

  const currentStop = tourStops[currentStopIdx];
  if (!currentStop) return null;

  const handleOpenExhibit = () => {
    if (selectedExhibit) {
      openExhibit(selectedExhibit);
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        className="tourStopPopupRight"
        initial={{ opacity: 0, y: 24, scale: 0.96 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 20, scale: 0.96 }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
        role="dialog"
        aria-labelledby="tourStopTitle"
      >
        <div className="tourStopPopupRight__card">
          {/* Header */}
          <div className="tourStopPopupRight__header">
            <div className="tourStopPopupRight__badges">
              <span className="badge badge--floor">Floor {currentStop.floor || 1}</span>
              <span className="badge badge--category">
                Stop {String(currentStopIdx + 1).padStart(2, '0')} / {tourStops.length}
              </span>
            </div>
            <button className="tourStopPopupRight__close" onClick={endTour} title="End Tour (Esc)">
              <X size={16} />
            </button>
          </div>

          {/* Body */}
          <div className="tourStopPopupRight__body">
            <h2 className="tourStopPopupRight__title" id="tourStopTitle">
              {currentStop.title}
            </h2>
            {currentStop.subtitle && (
              <div className="tourStopPopupRight__subtitle">{currentStop.subtitle}</div>
            )}
            <div className="tourStopPopupRight__desc">{currentStop.desc}</div>

            {/* Waypoint Perspective */}
            {currentStop.waypointNotes && (
              <div className="tourStopPopupRight__notes">
                <span className="tourStopNotesLabel">Tour Waypoint & Perspective</span>
                <span className="tourStopNotesText">{currentStop.waypointNotes}</span>
              </div>
            )}
          </div>

          {/* Footer Controls */}
          <div className="tourStopPopupRight__footer">
            <button
              className="tourBtn tourBtn--secondary"
              onClick={prevTourStop}
              disabled={currentStopIdx <= 0}
            >
              <ChevronLeft size={16} />
              <span>Prev</span>
            </button>

            {selectedExhibit && (
              <button
                className="tourBtn tourBtn--exhibit"
                onClick={handleOpenExhibit}
                title="Open detailed exhibit drawer on the left side"
              >
                <BookOpen size={15} />
                <span>Exhibits ↗</span>
              </button>
            )}

            <button
              className="tourBtn tourBtn--primary"
              onClick={nextTourStop}
              disabled={currentStopIdx >= tourStops.length - 1}
            >
              <span>Next</span>
              <ChevronRight size={16} />
            </button>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMuseumStore } from '../../store/useMuseumStore';
import { X, ExternalLink, ChevronLeft, ChevronRight } from 'lucide-react';
import { MUSEUM_EXHIBITS } from '../../data/museumContent.js';

export function ExhibitDrawer() {
  const isDrawerOpen = useMuseumStore((state) => state.isDrawerOpen);
  const selectedExhibit = useMuseumStore((state) => state.selectedExhibit);
  const closeDrawer = useMuseumStore((state) => state.closeDrawer);
  const openExhibit = useMuseumStore((state) => state.openExhibit);

  if (!selectedExhibit) return null;

  const currentIdx = MUSEUM_EXHIBITS.findIndex((e) => e.id === selectedExhibit.id);

  const handlePrev = () => {
    if (currentIdx > 0) {
      openExhibit(MUSEUM_EXHIBITS[currentIdx - 1]);
    }
  };

  const handleNext = () => {
    if (currentIdx < MUSEUM_EXHIBITS.length - 1) {
      openExhibit(MUSEUM_EXHIBITS[currentIdx + 1]);
    }
  };

  return (
    <AnimatePresence>
      {isDrawerOpen && (
        <motion.aside
          className="exhibitDrawerLeft"
          initial={{ x: '-105%' }}
          animate={{ x: '0%' }}
          exit={{ x: '-105%' }}
          transition={{ type: 'spring', damping: 28, stiffness: 220 }}
          role="dialog"
          aria-labelledby="exhibitTitle"
        >
          {/* Header */}
          <div className="exhibitDrawerLeft__header">
            <div className="exhibitDrawerLeft__badges">
              <span className="badge badge--floor">Floor {selectedExhibit.floor}</span>
              <span className="badge badge--category">{selectedExhibit.section || 'Exhibit'}</span>
              <span className="badge badge--year">{selectedExhibit.year || 'Verified'}</span>
            </div>
            <button
              className="exhibitDrawerLeft__close"
              onClick={closeDrawer}
              title="Close (Esc)"
            >
              <X size={18} />
            </button>
          </div>

          {/* Media Image */}
          {selectedExhibit.image && (
            <div className="exhibitDrawerLeft__media">
              <img
                src={selectedExhibit.image}
                alt={selectedExhibit.title || 'Exhibit visual'}
                className="exhibitDrawerLeft__img"
              />
            </div>
          )}

          {/* Content Body */}
          <div className="exhibitDrawerLeft__body">
            <h2 className="exhibitDrawerLeft__title" id="exhibitTitle">
              {selectedExhibit.title}
            </h2>
            {selectedExhibit.subtitle && (
              <div className="exhibitDrawerLeft__subtitle">{selectedExhibit.subtitle}</div>
            )}
            <div className="exhibitDrawerLeft__desc">
              {selectedExhibit.description || selectedExhibit.shortDescription}
            </div>

            {/* Key Facts Box */}
            {Array.isArray(selectedExhibit.facts) && selectedExhibit.facts.length > 0 && (
              <div className="exhibitDrawerLeft__facts">
                <div className="exhibitDrawerLeft__factsHeading">
                  Key Facts & Verified Milestones
                </div>
                <ul className="exhibitDrawerLeft__factsList">
                  {selectedExhibit.facts.map((fact, idx) => (
                    <li key={idx}>{fact}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Provenance Link */}
            {selectedExhibit.sourceUrl && (
              <div className="exhibitDrawerLeft__provenance">
                <span className="provenanceLabel">Verified Official Source</span>
                <a
                  className="provenanceLink"
                  href={selectedExhibit.sourceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <span>{selectedExhibit.sourceTitle || 'vit.ac.in'}</span>
                  <ExternalLink size={12} />
                </a>
              </div>
            )}
          </div>

          {/* Footer Navigation */}
          <div className="exhibitDrawerLeft__footer">
            <button
              className="exhibitNavBtn"
              onClick={handlePrev}
              disabled={currentIdx <= 0}
            >
              <ChevronLeft size={16} />
              <span>Previous</span>
            </button>
            <button
              className="exhibitNavBtn"
              onClick={handleNext}
              disabled={currentIdx >= MUSEUM_EXHIBITS.length - 1}
            >
              <span>Next</span>
              <ChevronRight size={16} />
            </button>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}

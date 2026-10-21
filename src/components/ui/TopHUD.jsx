import React, { useState, useRef } from 'react';
import { useMuseumStore } from '../../store/useMuseumStore';
import { MUSEUM_EXHIBITS } from '../../data/museumContent.js';
import { Layers, Search, Compass, Footprints, X, HelpCircle } from 'lucide-react';

export function TopHUD() {
  const floor = useMuseumStore((state) => state.floor);
  const setFloor = useMuseumStore((state) => state.setFloor);
  const mode = useMuseumStore((state) => state.mode);
  const isMinimalHUD = useMuseumStore((state) => state.isMinimalHUD);
  const tourStops = useMuseumStore((state) => state.tourStops);
  const currentStopIdx = useMuseumStore((state) => state.currentStopIdx);
  const endTour = useMuseumStore((state) => state.endTour);
  const openExhibit = useMuseumStore((state) => state.openExhibit);
  const toggleGuide = useMuseumStore((state) => state.toggleGuide);

  const [searchFocused, setSearchFocused] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const searchInputRef = useRef(null);

  if (isMinimalHUD) return null;

  // Search results filtered by title, subtitle, or section
  const searchResults = searchQuery.trim()
    ? MUSEUM_EXHIBITS.filter((ex) => {
        const q = searchQuery.toLowerCase();
        return (
          ex.title?.toLowerCase().includes(q) ||
          ex.subtitle?.toLowerCase().includes(q) ||
          ex.section?.toLowerCase().includes(q)
        );
      }).slice(0, 5)
    : [];

  return (
    <header className="topHUD">
      {/* Left: Floor Selector & Mode Badge */}
      <div className="topHUD__left">
        <button
          className="hudFloorBtn"
          onClick={() => setFloor(floor === 1 ? 2 : 1)}
          title={`Currently on Floor ${floor}. Click to switch floors.`}
        >
          <Layers className="hudFloorBtn__icon" size={16} />
          <span className="hudFloorBtn__badge">Floor {floor}</span>
          <span className="hudFloorBtn__name">
            {floor === 1 ? 'Heritage & Academics' : 'Research & Student Life'}
          </span>
        </button>

        <div className="hudModePill">
          {mode === 'tour' ? (
            <>
              <Compass size={14} className="hudModePill__icon" />
              <span>Guided Tour</span>
            </>
          ) : (
            <>
              <Footprints size={14} className="hudModePill__icon" />
              <span>Free Explore</span>
            </>
          )}
        </div>
      </div>

      {/* Center: Search & Navigation hints */}
      <div className="topHUD__center">
        {mode === 'tour' ? (
          <div className="tourProgressBar">
            <div className="tourProgressBar__info">
              <span className="tourProgressBar__tag">GUIDED TOUR</span>
              <span className="tourProgressBar__stop">
                Stop {String(currentStopIdx + 1).padStart(2, '0')} / {tourStops.length}
              </span>
            </div>
            <div className="tourProgressBar__track">
              <div
                className="tourProgressBar__fill"
                style={{
                  width: `${((currentStopIdx + 1) / tourStops.length) * 100}%`,
                }}
              />
            </div>
            <button className="tourProgressBar__exit" onClick={endTour} title="Exit Tour (Esc)">
              <X size={14} />
              <span>Exit</span>
            </button>
          </div>
        ) : (
          <div className="hudSearchWrapper">
            <div className={`hudSearchBar ${searchFocused ? 'is-focused' : ''}`}>
              <Search size={15} className="hudSearchBar__icon" />
              <input
                ref={searchInputRef}
                type="text"
                placeholder="Search exhibits, labs, history..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => setSearchFocused(true)}
                onBlur={() => setTimeout(() => setSearchFocused(false), 200)}
                className="hudSearchBar__input"
              />
              {searchQuery && (
                <button
                  className="hudSearchBar__clear"
                  onClick={() => setSearchQuery('')}
                  title="Clear search"
                >
                  <X size={13} />
                </button>
              )}
            </div>

            {/* Live Autocomplete Results */}
            {searchFocused && searchResults.length > 0 && (
              <div className="hudSearchDropdown">
                {searchResults.map((ex) => (
                  <div
                    key={ex.id}
                    className="hudSearchItem"
                    onMouseDown={() => {
                      openExhibit(ex);
                      setSearchQuery('');
                    }}
                  >
                    <div className="hudSearchItem__title">{ex.title}</div>
                    <div className="hudSearchItem__sub">
                      Floor {ex.floor} • {ex.section}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Right: Key Controls Helper Pill */}
      <div className="topHUD__right">
        <div className="hudKeyHints" onClick={toggleGuide} title="View all controls (Press H to hide HUD)">
          <span className="hudKeyHintTag">WASD</span>
          <span className="hudKeyHintText">Walk</span>
          <span className="hudKeyHintDot">•</span>
          <span className="hudKeyHintTag">Drag</span>
          <span className="hudKeyHintText">Look</span>
          <span className="hudKeyHintDot">•</span>
          <span className="hudKeyHintTag">E</span>
          <span className="hudKeyHintText">Inspect</span>
        </div>
      </div>
    </header>
  );
}

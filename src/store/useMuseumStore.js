import { create } from 'zustand';
import { MUSEUM_EXHIBITS } from '../data/museumContent.js';
import tourStopsData from '../data/tourStops.json';
import { sound, speakText, stopSpeaking } from '../utils/sound.js';

export const useMuseumStore = create((set, get) => ({
  // Floor & Exploration Mode
  floor: 1,
  mode: 'explore', // 'explore' | 'tour'
  isMinimalHUD: false,

  // Player position & joystick state
  playerPosition: [0.0, 1.6, 15.0],
  joystickVector: { x: 0, y: 0 },

  // Guided Tour
  tourStops: tourStopsData,
  currentStopIdx: 0,
  tourPlaying: false,

  // Camera Target
  cameraTarget: {
    position: [0.0, 1.6, 15.0],
    lookAt: [0.0, 1.8, 10.7],
  },

  // UI Overlays & Modals
  selectedExhibit: null,
  isDrawerOpen: false,
  isMapOpen: false,
  isGuideOpen: false,
  audioMuted: false,
  ttsEnabled: true,
  searchQuery: '',

  // Actions
  setPlayerPosition: (pos) => set({ playerPosition: pos }),
  setJoystickVector: (v) => set({ joystickVector: v }),

  toggleMinimalHUD: () => set((s) => ({ isMinimalHUD: !s.isMinimalHUD })),

  setFloor: (floorNum) => {
    sound.teleport();
    const pos = floorNum === 1 ? [0.0, 1.6, 15.0] : [12.5, 6.6, 14.0];
    const lookAt = floorNum === 1 ? [0.0, 1.8, 10.7] : [0.0, 6.0, 0.0];
    set({
      floor: floorNum,
      cameraTarget: { position: pos, lookAt: lookAt },
    });
  },

  setFloorSilent: (floorNum) => {
    if (get().floor !== floorNum) {
      set({ floor: floorNum });
    }
  },

  setMode: (mode) => {
    sound.click();
    set({ mode });
  },

  startTour: (startIdx = 0) => {
    sound.teleport();
    const stops = get().tourStops;
    const stop = stops[startIdx] || stops[0];
    const exhibit = stop.exhibitIds?.[0]
      ? MUSEUM_EXHIBITS.find((e) => e.id === stop.exhibitIds[0])
      : null;

    set({
      mode: 'tour',
      currentStopIdx: startIdx,
      tourPlaying: true,
      floor: stop.floor || 1,
      selectedExhibit: exhibit,
      isDrawerOpen: false,
      cameraTarget: {
        position: stop.targetPosition || [0, 1.6, 15],
        lookAt: stop.targetLookAt || [0, 1.8, 10],
      },
    });

    if (get().ttsEnabled && !get().audioMuted) {
      speakText(`${stop.title}. ${stop.narration || stop.description || ''}`);
    }
  },

  nextTourStop: () => {
    const { currentStopIdx, tourStops } = get();
    if (currentStopIdx < tourStops.length - 1) {
      get().goToTourStop(currentStopIdx + 1);
    } else {
      get().endTour();
    }
  },

  prevTourStop: () => {
    const { currentStopIdx } = get();
    if (currentStopIdx > 0) {
      get().goToTourStop(currentStopIdx - 1);
    }
  },

  goToTourStop: (idx) => {
    sound.teleport();
    const stops = get().tourStops;
    const stop = stops[idx];
    if (!stop) return;

    const exhibit = stop.exhibitIds?.[0]
      ? MUSEUM_EXHIBITS.find((e) => e.id === stop.exhibitIds[0])
      : null;

    set({
      currentStopIdx: idx,
      floor: stop.floor || 1,
      selectedExhibit: exhibit,
      cameraTarget: {
        position: stop.targetPosition || [0, 1.6, 15],
        lookAt: stop.targetLookAt || [0, 1.8, 10],
      },
    });

    if (get().ttsEnabled && !get().audioMuted) {
      speakText(`${stop.title}. ${stop.narration || stop.description || ''}`);
    }
  },

  toggleTourPlayback: () => {
    set((s) => ({ tourPlaying: !s.tourPlaying }));
  },

  endTour: () => {
    sound.click();
    stopSpeaking();
    set({
      mode: 'explore',
      tourPlaying: false,
      selectedExhibit: null,
      isDrawerOpen: false,
    });
  },

  openExhibit: (exhibit) => {
    sound.click();
    set({
      selectedExhibit: exhibit,
      isDrawerOpen: true,
    });

    if (get().ttsEnabled && !get().audioMuted && exhibit) {
      speakText(`${exhibit.title}. ${exhibit.shortDescription || ''}`);
    }
  },

  openExhibitById: (id) => {
    const exhibit = MUSEUM_EXHIBITS.find((e) => e.id === id);
    if (exhibit) {
      get().openExhibit(exhibit);
    }
  },

  closeDrawer: () => {
    sound.click();
    stopSpeaking();
    set({ isDrawerOpen: false });
  },

  interactNearestExhibit: () => {
    const { isDrawerOpen, closeDrawer, mode, nextTourStop, playerPosition } = get();
    if (isDrawerOpen) {
      closeDrawer();
      return;
    }
    if (mode === 'tour') {
      nextTourStop();
      return;
    }

    // In explore mode: find closest exhibit
    let closest = null;
    let minDist = 6.0; // max interaction distance 6 meters
    for (const ex of MUSEUM_EXHIBITS) {
      if (!ex.position) continue;
      const dx = playerPosition[0] - ex.position[0];
      const dz = playerPosition[2] - ex.position[2];
      const dist = Math.hypot(dx, dz);
      if (dist < minDist) {
        minDist = dist;
        closest = ex;
      }
    }

    if (closest) {
      get().openExhibit(closest);
    }
  },

  toggleMap: (open) => {
    sound.click();
    set((s) => ({ isMapOpen: open ?? !s.isMapOpen }));
  },

  toggleGuide: (open) => {
    sound.click();
    set((s) => ({ isGuideOpen: open ?? !s.isGuideOpen }));
  },

  toggleAudio: () => {
    const muted = !get().audioMuted;
    if (muted) stopSpeaking();
    set({ audioMuted: muted });
  },

  toggleTTS: () => set((s) => ({ ttsEnabled: !s.ttsEnabled })),

  setSearchQuery: (q) => set({ searchQuery: q }),

  flyTo: (position, lookAt) => {
    sound.teleport();
    set({
      cameraTarget: { position, lookAt: lookAt || [0, 1.5, 0] },
    });
  },
}));

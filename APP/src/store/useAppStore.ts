import { create } from 'zustand';

interface LocationState {
  latitude: number;
  longitude: number;
}

interface MapBounds {
  minLon: number;
  minLat: number;
  maxLon: number;
  maxLat: number;
}

interface AppState {
  // Backend state
  backendAvailable: boolean;
  backendMapDataName: string;

  // Local map state
  localMapDataAvailable: boolean;
  localMapDataName: string;
  localMapDataUpToDate: boolean;

  // Current selection
  selectedDay: string;
  availableDays: string[];

  // Map data
  mapBounds: MapBounds | null;

  // GPS state
  userLocation: LocationState | null;
  gpsEnabled: boolean;

  // Download state
  downloadProgress: number;
  isDownloading: boolean;

  // Actions
  setBackendState: (available: boolean, mapName?: string) => void;
  setLocalMapState: (available: boolean, name?: string, upToDate?: boolean) => void;
  setSelectedDay: (day: string) => void;
  setAvailableDays: (days: string[]) => void;
  setMapBounds: (bounds: MapBounds | null) => void;
  setUserLocation: (location: LocationState | null) => void;
  setGpsEnabled: (enabled: boolean) => void;
  setDownloadProgress: (progress: number) => void;
  setIsDownloading: (downloading: boolean) => void;
  reset: () => void;
}

const initialState = {
  backendAvailable: false,
  backendMapDataName: '',
  localMapDataAvailable: false,
  localMapDataName: '',
  localMapDataUpToDate: false,
  selectedDay: '',
  availableDays: [],
  mapBounds: null,
  userLocation: null,
  gpsEnabled: false,
  downloadProgress: 0,
  isDownloading: false,
};

export const useAppStore = create<AppState>((set) => ({
  ...initialState,

  setBackendState: (available, mapName) =>
    set((state) => ({
      backendAvailable: available,
      backendMapDataName: mapName ?? state.backendMapDataName,
    })),

  setLocalMapState: (available, name, upToDate) =>
    set((state) => ({
      localMapDataAvailable: available,
      localMapDataName: name ?? state.localMapDataName,
      localMapDataUpToDate: upToDate ?? state.localMapDataUpToDate,
    })),

  setSelectedDay: (day) => set({ selectedDay: day }),

  setAvailableDays: (days) => set({ availableDays: days }),

  setMapBounds: (bounds) => set({ mapBounds: bounds }),

  setUserLocation: (location) => set({ userLocation: location }),

  setGpsEnabled: (enabled) => set({ gpsEnabled: enabled }),

  setDownloadProgress: (progress) => set({ downloadProgress: progress }),

  setIsDownloading: (downloading) => set({ isDownloading: downloading }),

  reset: () => set(initialState),
}));

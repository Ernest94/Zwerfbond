import * as Location from 'expo-location';
import { useCallback, useEffect, useRef, useState } from 'react';
import { CONFIG } from '../constants/config';

interface LocationState {
  latitude: number;
  longitude: number;
  accuracy?: number;
}

interface UseGpsLocationOptions {
  enabled?: boolean;
  onLocationUpdate?: (location: LocationState) => void;
}

export function useGpsLocation(options: UseGpsLocationOptions = {}) {
  const { enabled = true, onLocationUpdate } = options;
  const [location, setLocation] = useState<LocationState | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [permissionGranted, setPermissionGranted] = useState<boolean>(false);
  const subscriptionRef = useRef<Location.LocationSubscription | null>(null);

  const requestPermissions = useCallback(async (): Promise<boolean> => {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      const granted = status === 'granted';
      setPermissionGranted(granted);
      if (!granted) {
        setErrorMsg('Location permission denied');
      }
      return granted;
    } catch (error) {
      setErrorMsg('Failed to request location permissions');
      return false;
    }
  }, []);

  const startWatching = useCallback(async () => {
    if (!permissionGranted) {
      const granted = await requestPermissions();
      if (!granted) return;
    }

    try {
      subscriptionRef.current = await Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.High,
          timeInterval: CONFIG.GPS_UPDATE_INTERVAL,
          distanceInterval: 0,
        },
        (newLocation) => {
          const locationState: LocationState = {
            latitude: newLocation.coords.latitude,
            longitude: newLocation.coords.longitude,
            accuracy: newLocation.coords.accuracy ?? undefined,
          };
          setLocation(locationState);
          onLocationUpdate?.(locationState);
        }
      );
    } catch (error) {
      console.error('Failed to watch position:', error);
      setErrorMsg('Failed to start location tracking');
    }
  }, [permissionGranted, requestPermissions, onLocationUpdate]);

  const stopWatching = useCallback(() => {
    if (subscriptionRef.current) {
      subscriptionRef.current.remove();
      subscriptionRef.current = null;
    }
  }, []);

  useEffect(() => {
    if (enabled) {
      startWatching();
    } else {
      stopWatching();
    }

    return () => {
      stopWatching();
    };
  }, [enabled, startWatching, stopWatching]);

  return {
    location,
    errorMsg,
    permissionGranted,
    requestPermissions,
    startWatching,
    stopWatching,
  };
}

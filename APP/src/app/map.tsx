import { MaterialIcons } from '@expo/vector-icons';
import MapLibreGL from '@maplibre/maplibre-react-native';
import { useRouter } from 'expo-router';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { GpsBlinker } from '../components/GpsBlinker';
import { CONFIG } from '../constants/config';
import { useGpsLocation } from '../hooks/useGpsLocation';
import { getMBTilesPath, getRouteCoordinates, isWithinBounds } from '../services/database';
import { useAppStore } from '../store/useAppStore';

interface Coordinate {
  latitude: number;
  longitude: number;
}

const MapScreen: React.FC = () => {
  const router = useRouter();
  // State
  const [routeCoordinates, setRouteCoordinates] = useState<Coordinate[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [initialCenter, setInitialCenter] = useState<[number, number] | null>(null);
  const [cameraTarget, setCameraTarget] = useState<{ center: [number, number]; zoom: number; trigger: number } | null>(null);
  const [showEndLabel, setShowEndLabel] = useState(false);

  // Zustand store
  const {
    selectedDay,
    mapBounds,
    userLocation,
    setUserLocation,
    setGpsEnabled,
  } = useAppStore();

  // GPS tracking — stable callback to avoid restarting the watcher on every render
  const handleLocationUpdate = useCallback(
    (loc: { latitude: number; longitude: number }) => {
      setUserLocation({ latitude: loc.latitude, longitude: loc.longitude });
    },
    [setUserLocation]
  );

  useGpsLocation({
    enabled: true,
    onLocationUpdate: handleLocationUpdate,
  });

  // Initialize map and load route
  useEffect(() => {
    let isMounted = true;

    async function init() {
      try {
        setIsLoading(true);

        // Load route coordinates for selected day
        let centerSet = false;
        if (selectedDay) {
          console.log('Loading route for day:', selectedDay);
          const coords = await getRouteCoordinates(selectedDay);
          console.log('Route coordinates loaded:', coords.length, 'points');

          if (isMounted && coords.length > 0) {
            const routePoints = coords.map(([lon, lat]) => ({
              latitude: lat,
              longitude: lon,
            }));
            setRouteCoordinates(routePoints);

            // Center on first coordinate
            setInitialCenter([coords[0][0], coords[0][1]]);
            centerSet = true;
          }
        }

        // Fallback: use map bounds center
        if (!centerSet && isMounted) {
          if (mapBounds) {
            const centerLon = (mapBounds.minLon + mapBounds.maxLon) / 2;
            const centerLat = (mapBounds.minLat + mapBounds.maxLat) / 2;
            setInitialCenter([centerLon, centerLat]);
          } else {
            setInitialCenter([6.08, 50.48]);
          }
        }
      } catch (error) {
        console.error('Failed to initialize map:', error);
        if (isMounted) {
          setInitialCenter([6.08, 50.48]);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
          setGpsEnabled(true);
        }
      }
    }

    init();

    return () => {
      isMounted = false;
      setGpsEnabled(false);
    };
  }, [selectedDay, setGpsEnabled]);

  const handleBack = () => {
    router.back();
  };

  const handleRecenter = () => {
    if (userLocation && mapBounds) {
      const isInBounds = isWithinBounds(
        userLocation.latitude,
        userLocation.longitude,
        mapBounds
      );

      if (isInBounds) {
        setCameraTarget((prev) => ({
          center: [userLocation.longitude, userLocation.latitude],
          zoom: 15,
          trigger: (prev?.trigger ?? 0) + 1,
        }));
        return;
      }
    }

    if (routeCoordinates.length > 0) {
      const start = routeCoordinates[0];
      setCameraTarget((prev) => ({
        center: [start.longitude, start.latitude],
        zoom: 14,
        trigger: (prev?.trigger ?? 0) + 1,
      }));
    }
  };

  const getEndPoint = (): Coordinate | null => {
    if (routeCoordinates.length === 0) return null;
    return routeCoordinates[routeCoordinates.length - 1];
  };

  const endPoint = getEndPoint();

  // Memoize GeoJSON so it's only rebuilt when route changes, not on GPS updates
  const routeGeoJSON = useMemo<GeoJSON.FeatureCollection>(() => ({
    type: 'FeatureCollection',
    features:
      routeCoordinates.length > 0
        ? [
            {
              type: 'Feature',
              properties: {},
              geometry: {
                type: 'LineString',
                coordinates: routeCoordinates.map((c) => [c.longitude, c.latitude]),
              },
            },
          ]
        : [],
  }), [routeCoordinates]);

  // End point GeoJSON for native press detection
  const endPointGeoJSON = useMemo<GeoJSON.FeatureCollection | null>(() => {
    if (!endPoint) return null;
    return {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'Point',
          coordinates: [endPoint.longitude, endPoint.latitude],
        },
      }],
    };
  }, [endPoint]);

  const handleEndMarkerPress = useCallback(() => {
    setShowEndLabel((prev) => !prev);
  }, []);

  // Empty base style — memoize to avoid JSON.stringify on every render
  const emptyStyle = useMemo(() => JSON.stringify({
    version: 8,
    sources: {},
    layers: [],
  }), []);

  // Map bounds for camera — memoize to keep stable reference
  const bounds = useMemo(() => mapBounds
    ? {
        ne: [mapBounds.maxLon, mapBounds.maxLat] as [number, number],
        sw: [mapBounds.minLon, mapBounds.minLat] as [number, number],
      }
    : undefined, [mapBounds]);

  if (isLoading || !initialCenter) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#D32F2F" />
        <Text style={styles.loadingText}>Kaart laden...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <MapLibreGL.MapView
        style={styles.map}
        styleJSON={emptyStyle}
        rotateEnabled={false}
        attributionEnabled={false}
        logoEnabled={false}
      >
        <MapLibreGL.Camera
          key={cameraTarget?.trigger ?? 0}
          defaultSettings={{
            centerCoordinate: cameraTarget?.center ?? initialCenter,
            zoomLevel: cameraTarget?.zoom ?? 14,
          }}
          animationDuration={500}
          minZoomLevel={12}
          maxZoomLevel={16}
          maxBounds={bounds}
        />

        {/* Raster tile layer directly from MBTiles file */}
        <MapLibreGL.RasterSource
          id="mbtiles-source"
          tileUrlTemplates={[`mbtiles://${getMBTilesPath()}`]}
          tileSize={256}
          minZoomLevel={12}
          maxZoomLevel={16}
        >
          <MapLibreGL.RasterLayer
            id="mbtiles-layer"
            style={{ rasterOpacity: 1 }}
          />
        </MapLibreGL.RasterSource>

        {/* Route polyline */}
        {routeCoordinates.length > 0 && (
          <MapLibreGL.ShapeSource id="route-source" shape={routeGeoJSON}>
            <MapLibreGL.LineLayer
              id="route-line"
              style={{
                lineColor: CONFIG.ROUTE_LINE_COLOR,
                lineWidth: CONFIG.ROUTE_LINE_WIDTH,
                lineCap: 'round',
                lineJoin: 'miter',
              }}
            />
          </MapLibreGL.ShapeSource>
        )}

        {/* GPS Blinker */}
        {userLocation && (
          <GpsBlinker
            latitude={userLocation.latitude}
            longitude={userLocation.longitude}
            isBlinking={true}
          />
        )}

        {/* End marker: ShapeSource for native press detection */}
        {endPoint && endPointGeoJSON && (
          <MapLibreGL.ShapeSource
            id="end-marker-source"
            shape={endPointGeoJSON}
            onPress={handleEndMarkerPress}
          >
            <MapLibreGL.CircleLayer
              id="end-marker-hit-area"
              style={{
                circleRadius: 20,
                circleOpacity: 0,
              }}
            />
          </MapLibreGL.ShapeSource>
        )}

        {/* End marker: MarkerView for display only */}
        {endPoint && (
          <MapLibreGL.MarkerView
            coordinate={[endPoint.longitude, endPoint.latitude]}
            anchor={{ x: 0.5, y: 1 }}
          >
            <View style={styles.endMarkerWrapper} pointerEvents="none">
              {showEndLabel && (
                <Text style={styles.endMarkerText}>
                  Eind {selectedDay}
                </Text>
              )}
              <View style={styles.endMarkerIcon}>
                <MaterialIcons name="flag" size={28} color="#FFF" />
              </View>
            </View>
          </MapLibreGL.MarkerView>
        )}
      </MapLibreGL.MapView>

      {/* Menu button */}
      <TouchableOpacity style={styles.menuButton} onPress={handleBack}>
        <Text style={styles.menuButtonText}>Menu</Text>
      </TouchableOpacity>

      {/* GPS recenter button */}
      <TouchableOpacity style={styles.gpsButton} onPress={handleRecenter}>
        <MaterialIcons name="my-location" size={24} color="#666" />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#555',
  },
  map: {
    flex: 1,
  },
  menuButton: {
    position: 'absolute',
    top: 50,
    left: 15,
    backgroundColor: '#D32F2F',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 8,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.5,
  },
  menuButtonText: {
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 16,
  },
  gpsButton: {
    position: 'absolute',
    bottom: 80,
    right: 15,
    backgroundColor: '#FFF',
    width: 44,
    height: 44,
    borderRadius: 4,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.3,
    shadowRadius: 2,
  },
  endMarkerWrapper: {
    alignItems: 'center',
    width: 100,
  },
  endMarkerIcon: {
    backgroundColor: '#D32F2F',
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#FFF',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.3,
    shadowRadius: 2,
    elevation: 3,
  },
  endMarkerText: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    marginBottom: 4,
    fontSize: 12,
    fontWeight: 'bold',
    color: '#333',
    overflow: 'hidden',
  },
});

export default MapScreen;

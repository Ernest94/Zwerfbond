import React, { useEffect, useRef } from 'react';
import { Animated, StyleSheet, View } from 'react-native';
import MapLibreGL from '@maplibre/maplibre-react-native';

interface GpsBlinkerProps {
  latitude: number;
  longitude: number;
  isBlinking?: boolean;
}

export function GpsBlinker({
  latitude,
  longitude,
  isBlinking = true,
}: GpsBlinkerProps) {
  const pulseAnim = useRef(new Animated.Value(0)).current;
  const animationRef = useRef<Animated.CompositeAnimation | null>(null);

  useEffect(() => {
    if (isBlinking) {
      animationRef.current = Animated.loop(
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1500,
          useNativeDriver: true,
        })
      );
      animationRef.current.start();
    } else {
      animationRef.current?.stop();
      pulseAnim.setValue(0);
    }

    return () => {
      animationRef.current?.stop();
    };
  }, [isBlinking, pulseAnim]);

  const outerScale = pulseAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [1, 2],
  });

  const outerOpacity = pulseAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [1, 0],
  });

  return (
    <MapLibreGL.MarkerView coordinate={[longitude, latitude]}>
      <View style={styles.container}>
        <Animated.View
          style={[
            styles.outerCircle,
            {
              transform: [{ scale: outerScale }],
              opacity: outerOpacity,
            },
          ]}
        />
        <View style={styles.innerCircle} />
      </View>
    </MapLibreGL.MarkerView>
  );
}

const styles = StyleSheet.create({
  container: {
    width: 50,
    height: 50,
    alignItems: 'center',
    justifyContent: 'center',
  },
  outerCircle: {
    position: 'absolute',
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: 'rgba(33, 150, 243, 0.4)',
  },
  innerCircle: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#2196F3',
    borderWidth: 3,
    borderColor: '#FFFFFF',
  },
});

import { Image } from 'expo-image';
import { useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
  ActivityIndicator,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { getDays, getMapBounds, getMapName } from '../services/database';
import { useAppStore } from '../store/useAppStore';

export default function MenuScreen() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const [days, setDays] = useState<string[]>([]);
  const [tourName, setTourName] = useState('');

  const insets = useSafeAreaInsets();
  const {
    localMapDataName,
    localMapDataUpToDate,
    backendAvailable,
    setSelectedDay,
    setAvailableDays,
    setMapBounds,
  } = useAppStore();

  useEffect(() => {
    loadMenuData();
  }, []);

  const loadMenuData = async () => {
    setIsLoading(true);
    try {
      // Load days from database
      const availableDays = await getDays();

      // Use loaded days or fallback if empty
      if (availableDays.length > 0) {
        setDays(availableDays);
        setAvailableDays(availableDays);
      } else {
        console.warn('No days found in database, using fallback');
        const fallbackDays = ['dag 1', 'dag 2', 'dag 3', 'dag 4', 'dag 5', 'dag 6'];
        setDays(fallbackDays);
        setAvailableDays(fallbackDays);
      }

      // Load map name
      const name = await getMapName();
      setTourName(name || localMapDataName);

      // Load map bounds for GPS checking later
      const bounds = await getMapBounds();
      if (bounds) {
        setMapBounds(bounds);
      }
    } catch (error) {
      console.error('Failed to load menu data:', error);
      // Fallback to hardcoded days if database fails
      const fallbackDays = ['dag 1', 'dag 2', 'dag 3', 'dag 4', 'dag 5', 'dag 6'];
      setDays(fallbackDays);
      setAvailableDays(fallbackDays);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDayPress = (day: string) => {
    setSelectedDay(day);
    router.push('/map');
  };

  const handleUpdatePress = () => {
    router.push('/login');
  };

  // Show update icon if map is outdated and backend is available
  const showUpdateIcon = !localMapDataUpToDate && backendAvailable;

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#D32F2F" />
        <Text style={styles.loadingText}>Laden...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerContent}>
          <Text style={styles.tourName} numberOfLines={2}>
            {tourName}
          </Text>
          {showUpdateIcon && (
            <TouchableOpacity
              style={styles.updateButton}
              onPress={handleUpdatePress}
            >
              <Image
                source={require('../../assets/images/icon.png')}
                style={styles.updateIcon}
                contentFit="contain"
              />
            </TouchableOpacity>
          )}
        </View>
      </View>

      {/* Day buttons */}
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={[styles.buttonContainer, { paddingBottom: insets.bottom }]}
        showsVerticalScrollIndicator={false}
      >
        {days.map((day, index) => (
          <TouchableOpacity
            key={index}
            style={styles.dayButton}
            onPress={() => handleDayPress(day)}
          >
            <Text style={styles.dayButtonText}>
              {day.charAt(0).toUpperCase() + day.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
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
  header: {
    backgroundColor: '#D32F2F',
    paddingTop: 60,
    paddingBottom: 24,
    paddingHorizontal: 24,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  tourName: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFF',
    flex: 1,
  },
  updateButton: {
    marginLeft: 12,
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: 12,
    padding: 4,
  },
  updateIcon: {
    width: 44,
    height: 44,
  },
  scrollView: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    padding: 0,
    gap: 0,
  },
  dayButton: {
    flex: 1,
    backgroundColor: '#FFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
    paddingVertical: 18,
    paddingHorizontal: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  dayButtonText: {
    color: '#2D2D2D',
    fontSize: 24,
    fontWeight: '600',
  },
});

import { Image } from 'expo-image';
import { useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
  ActivityIndicator,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import { checkBackendAvailable, downloadMBTiles, verifyPassword } from '../services/api';
import { databaseExists, getMapName, resetDatabaseConnection } from '../services/database';
import { useAppStore } from '../store/useAppStore';

export default function LoginScreen() {
  const router = useRouter();
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  // Zustand store
  const {
    backendAvailable,
    backendMapDataName,
    localMapDataAvailable,
    localMapDataName,
    localMapDataUpToDate,
    downloadProgress,
    isDownloading,
    setBackendState,
    setLocalMapState,
    setDownloadProgress,
    setIsDownloading,
  } = useAppStore();

  // Initialize app state on mount
  useEffect(() => {
    initializeAppState();
  }, []);

  const initializeAppState = async () => {
    setIsLoading(true);
    try {
      // Check backend availability
      const { available, mapName } = await checkBackendAvailable();
      setBackendState(available, mapName ?? '');

      // Check local map
      const localExists = await databaseExists();
      if (localExists) {
        const localName = await getMapName();
        const isUpToDate = available ? localName === mapName : true;
        setLocalMapState(true, localName, isUpToDate);

        // If local map is up to date, go directly to menu
        if (isUpToDate) {
          router.replace('/menu');
          return;
        }
      } else {
        setLocalMapState(false, '', false);
      }
    } catch (err) {
      console.error('Failed to initialize app state:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!backendAvailable) {
      setError('Server niet bereikbaar. Controleer uw internetverbinding en probeer het opnieuw.');
      return;
    }

    if (!password) {
      setError('Voer een wachtwoord in');
      return;
    }

    setError('');
    setIsDownloading(true);
    setDownloadProgress(0);

    try {
      // Verify password
      const isValid = await verifyPassword(password);
      if (!isValid) {
        setError('Het ingevoerde wachtwoord is niet correct');
        setIsDownloading(false);
        return;
      }

      // Download MBTiles
      await downloadMBTiles((progress) => {
        setDownloadProgress(progress);
      });

      // Reset stale DB connection so it gets re-opened fresh next time
      await resetDatabaseConnection();

      // Use the backend map name we already have (avoids opening the DB right after download)
      setLocalMapState(true, backendMapDataName, true);

      // Navigate to menu
      router.replace('/menu');
    } catch (err) {
      console.error('Download failed:', err);
      setError('Download mislukt. Probeer het opnieuw.');
      setDownloadProgress(0);
    } finally {
      setIsDownloading(false);
    }
  };

  const handleCancel = () => {
    // Skip download and use existing map
    router.replace('/menu');
  };

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007bff" />
        <Text style={styles.loadingText}>Laden...</Text>
      </View>
    );
  }

  // Determine label text
  const getLabelText = () => {
    if (backendAvailable && backendMapDataName) {
      return `Voer het wachtwoord in, om de ${backendMapDataName} kaart te downloaden:`;
    }
    if (!backendAvailable && localMapDataAvailable) {
      return 'Server niet bereikbaar. U kunt de bestaande kaart gebruiken.';
    }
    return 'Voer het wachtwoord in om de kaart te downloaden:';
  };

  // Show cancel button if local map exists but is outdated
  const showCancelButton = localMapDataAvailable && !localMapDataUpToDate && backendAvailable;

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Welkom in de Zwerfbond app</Text>
        <Image
          source={require('../../assets/images/icon.png')}
          style={styles.logo}
          contentFit="contain"
        />
      </View>

      {/* Dynamic label */}
      <Text style={styles.label}>{getLabelText()}</Text>

      {/* Password input */}
      <TextInput
        style={[styles.input, error ? styles.inputError : null]}
        secureTextEntry
        placeholder="Wachtwoord"
        placeholderTextColor="#999"
        value={password}
        onChangeText={(text) => {
          setPassword(text);
          setError('');
        }}
        editable={!isDownloading}
      />

      {/* Error message */}
      {error ? <Text style={styles.errorText}>{error}</Text> : null}

      {/* Download button */}
      <TouchableOpacity
        style={[styles.downloadButton, isDownloading && styles.buttonDisabled]}
        onPress={handleDownload}
        disabled={isDownloading}
      >
        <Text style={styles.buttonText}>
          {isDownloading ? 'Downloaden...' : 'Download de kaart'}
        </Text>
      </TouchableOpacity>

      {/* Progress bar */}
      {isDownloading && (
        <View style={styles.progressContainer}>
          <View
            style={[styles.progressBar, { width: `${downloadProgress * 100}%` }]}
          />
          <Text style={styles.progressText}>
            {Math.round(downloadProgress * 100)}%
          </Text>
        </View>
      )}

      {/* WiFi warning */}
      <Text style={styles.warningText}>
        Let op! Wij raden aan om de kaart te downloaden als u met wifi verbonden
        bent.
      </Text>

      {/* Cancel button - only show if local map exists but outdated */}
      {showCancelButton && (
        <TouchableOpacity
          style={styles.cancelButton}
          onPress={handleCancel}
          disabled={isDownloading}
        >
          <Text style={styles.cancelButtonText}>
            De nieuwe kaart niet downloaden
          </Text>
        </TouchableOpacity>
      )}

      {/* Offline mode button - show if backend not available but local map exists */}
      {!backendAvailable && localMapDataAvailable && (
        <TouchableOpacity style={styles.offlineButton} onPress={handleCancel}>
          <Text style={styles.offlineButtonText}>
            Gebruik bestaande kaart ({localMapDataName})
          </Text>
        </TouchableOpacity>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#B3B3B3', // Gray background like Kivy
    padding: 30,
    paddingTop: 60,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#B3B3B3',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#333',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
    flex: 1,
  },
  logo: {
    width: 80,
    height: 80,
  },
  label: {
    fontSize: 16,
    color: '#000',
    marginBottom: 15,
  },
  input: {
    backgroundColor: '#FFF',
    borderWidth: 1,
    borderColor: '#CCC',
    borderRadius: 8,
    padding: 15,
    fontSize: 16,
    color: '#000',
    marginBottom: 10,
  },
  inputError: {
    borderColor: '#FF0000',
  },
  errorText: {
    color: '#FF0000',
    fontSize: 14,
    marginBottom: 10,
  },
  downloadButton: {
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
    borderWidth: 2,
    borderColor: '#FF0000', // Red border like Kivy
    borderRadius: 25,
    padding: 15,
    alignItems: 'center',
    marginBottom: 15,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#000',
    fontSize: 16,
    fontWeight: 'bold',
  },
  progressContainer: {
    height: 30,
    backgroundColor: '#DDD',
    borderRadius: 15,
    marginBottom: 15,
    overflow: 'hidden',
    position: 'relative',
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#4CAF50', // Green progress
    borderRadius: 15,
  },
  progressText: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    textAlign: 'center',
    lineHeight: 30,
    fontWeight: 'bold',
    color: '#000',
  },
  warningText: {
    fontSize: 14,
    color: '#333',
    textAlign: 'center',
    marginBottom: 20,
    fontStyle: 'italic',
  },
  cancelButton: {
    borderWidth: 1,
    borderColor: '#666',
    borderRadius: 25,
    padding: 12,
    alignItems: 'center',
    marginTop: 10,
  },
  cancelButtonText: {
    color: '#333',
    fontSize: 14,
  },
  offlineButton: {
    backgroundColor: '#007bff',
    borderRadius: 25,
    padding: 15,
    alignItems: 'center',
    marginTop: 20,
  },
  offlineButtonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

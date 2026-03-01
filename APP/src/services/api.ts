import RNFS from 'react-native-fs';
import { CONFIG } from '../constants/config';

/**
 * Check if the backend is available and get the current map name
 */
export async function checkBackendAvailable(): Promise<{
  available: boolean;
  mapName: string | null;
}> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(`${CONFIG.API_BASE_URL}/get_mbtiles_name`, {
      method: 'GET',
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      const mapName = await response.text();
      return { available: true, mapName: mapName.trim() };
    }
    return { available: false, mapName: null };
  } catch (error) {
    console.log('Backend not available:', error);
    return { available: false, mapName: null };
  }
}

/**
 * Verify password with the backend
 * @param password The password to verify
 * @returns true if password is valid, false otherwise
 */
export async function verifyPassword(password: string): Promise<boolean> {
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password }),
    });

    const result = await response.text();
    // Backend returns "1" for valid, "0" for invalid
    return result.trim() === '1';
  } catch (error) {
    console.error('Password verification failed:', error);
    throw new Error('Network error during verification');
  }
}

/**
 * Get the directory path for MBTiles storage
 */
function getMBTilesDirectory(): string {
  return `${RNFS.DocumentDirectoryPath}/${CONFIG.MBTILES_DIR}/`;
}

/**
 * Get the file path for the MBTiles file
 */
function getMBTilesFilePath(): string {
  return `${getMBTilesDirectory()}${CONFIG.MBTILES_FILENAME}`;
}

/**
 * Download the MBTiles file from the backend
 * @param onProgress Callback for download progress (0-1)
 * @returns Path to the downloaded file
 */
export async function downloadMBTiles(
  onProgress?: (progress: number) => void
): Promise<string> {
  const url = `${CONFIG.API_BASE_URL}/get_mbtiles`;
  const directory = getMBTilesDirectory();
  const filePath = getMBTilesFilePath();

  // Create directory if it doesn't exist
  if (!(await RNFS.exists(directory))) {
    await RNFS.mkdir(directory);
  }

  // Delete existing file if present
  if (await RNFS.exists(filePath)) {
    await RNFS.unlink(filePath);
  }

  try {
    await new Promise<void>((resolve, reject) => {
      const download = RNFS.downloadFile({
        fromUrl: url,
        toFile: filePath,
        progress: (res) => {
          if (onProgress && res.contentLength > 0) {
            onProgress(res.bytesWritten / res.contentLength);
          }
        },
        progressDivider: 1,
      });

      download.promise
        .then((result) => {
          if (result.statusCode === 200) {
            resolve();
          } else {
            reject(new Error(`Download failed with status ${result.statusCode}`));
          }
        })
        .catch(reject);
    });

    return filePath;
  } catch (error) {
    // Clean up on error
    if (await RNFS.exists(filePath)) {
      await RNFS.unlink(filePath);
    }
    throw error;
  }
}


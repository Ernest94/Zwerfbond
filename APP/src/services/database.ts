import { Platform } from 'react-native';
import RNFS from 'react-native-fs';
import SQLite, { SQLiteDatabase } from 'react-native-sqlite-storage';
import { CONFIG } from '../constants/config';

// Enable promises for SQLite
SQLite.enablePromise(true);

let db: SQLiteDatabase | null = null;

/**
 * Close and reset the database connection
 * Call this when logging out to ensure fresh connection on next open
 */
export async function resetDatabaseConnection(): Promise<void> {
  if (db) {
    try {
      await db.close();
    } catch (e) {
      console.log('Error closing database:', e);
    }
    db = null;
  }
}

/**
 * Get the path to the MBTiles database file
 */
export function getMBTilesPath(): string {
  return `${RNFS.DocumentDirectoryPath}/${CONFIG.MBTILES_DIR}/${CONFIG.MBTILES_FILENAME}`;
}

/**
 * Check if the MBTiles database exists locally
 */
export async function databaseExists(): Promise<boolean> {
  const path = getMBTilesPath();
  try {
    return await RNFS.exists(path);
  } catch {
    return false;
  }
}

/**
 * Open the MBTiles database
 */
export async function openDatabase(): Promise<SQLiteDatabase> {
  if (db) {
    return db;
  }

  const exists = await databaseExists();

  if (!exists) {
    throw new Error('MBTiles database not found');
  }

  if (Platform.OS === 'android') {
    // On Android, 'Documents' location doesn't map to RNFS.DocumentDirectoryPath.
    // Use the full absolute path so SQLite finds the downloaded file.
    db = await SQLite.openDatabase({
      name: getMBTilesPath(),
      location: 'default',
    });
  } else {
    db = await SQLite.openDatabase({
      name: `${CONFIG.MBTILES_DIR}/${CONFIG.MBTILES_FILENAME}`,
      location: 'Documents',
    });
  }

  return db;
}

/**
 * Query metadata from the MBTiles database
 * @param name The metadata key to query
 */
export async function queryMetadata(name: string): Promise<string | null> {
  const database = await openDatabase();
  const results = await database.executeSql(
    'SELECT value FROM metadata WHERE name = ?',
    [name]
  );

  const rows = results[0].rows;
  if (rows.length > 0) {
    return rows.item(0).value;
  }
  return null;
}

/**
 * Get the map name from metadata
 */
export async function getMapName(): Promise<string> {
  const name = await queryMetadata('name');
  return name ?? '';
}

/**
 * Get available days from metadata
 * @returns Array of day strings like ["dag 1", "dag 2", ...]
 */
export async function getDays(): Promise<string[]> {
  try {
    const daysStr = await queryMetadata('days');
    if (!daysStr) {
      console.warn('No days metadata found in database');
      return [];
    }
    // Handle both comma-space and comma-only separators (like Python app)
    const days = daysStr.split(',').map((d) => d.trim()).filter((d) => d.length > 0);
    console.log('Loaded days from database:', days);
    return days;
  } catch (error) {
    console.error('Failed to get days from database:', error);
    return [];
  }
}

/**
 * Get map bounds from metadata
 * @returns Object with minLon, minLat, maxLon, maxLat or null
 */
export async function getMapBounds(): Promise<{
  minLon: number;
  minLat: number;
  maxLon: number;
  maxLat: number;
} | null> {
  const boundsStr = await queryMetadata('bounds');
  if (!boundsStr) return null;

  const parts = boundsStr.split(',').map((b) => parseFloat(b.trim()));
  if (parts.length !== 4) return null;

  return {
    minLon: parts[0],
    minLat: parts[1],
    maxLon: parts[2],
    maxLat: parts[3],
  };
}

/**
 * Get route coordinates for a specific day
 * @param day The day string (e.g., "dag 1")
 * @returns Array of [longitude, latitude] coordinate pairs
 */
export async function getRouteCoordinates(
  day: string
): Promise<[number, number][]> {
  try {
    const database = await openDatabase();
    const results = await database.executeSql(
      'SELECT coordinate_string FROM route_coordinates WHERE day = ?',
      [day]
    );

    const rows = results[0].rows;
    if (rows.length === 0) {
      console.warn(`No route coordinates found for day: ${day}`);
      return [];
    }

    const coordinateString = rows.item(0).coordinate_string;
    console.log('Raw coordinate_string type:', typeof coordinateString);
    return parseCoordinateString(coordinateString);
  } catch (error: unknown) {
    // Handle missing table error gracefully
    const errorMessage = error instanceof Error ? error.message : String(error);
    if (errorMessage.includes('no such table')) {
      console.warn('route_coordinates table not found in MBTiles - the file may be incomplete');
    } else {
      console.error('Failed to get route coordinates:', error);
    }
    return [];
  }
}

/**
 * Decode Base64 string to UTF-8 text
 */
function decodeBase64(base64: string): string {
  // Use atob if available (works in React Native)
  try {
    // React Native has atob available globally
    return atob(base64);
  } catch {
    // Fallback: manual base64 decode
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    let result = '';
    let buffer = 0;
    let bits = 0;

    for (const char of base64) {
      if (char === '=') break;
      const index = chars.indexOf(char);
      if (index === -1) continue;

      buffer = (buffer << 6) | index;
      bits += 6;

      if (bits >= 8) {
        bits -= 8;
        result += String.fromCharCode((buffer >> bits) & 0xff);
      }
    }
    return result;
  }
}

/**
 * Parse coordinate string from database into array of [lon, lat] pairs
 * The Kivy app stores coordinates as "[lon1, lat1, lon2, lat2, ...]"
 * Note: SQLite may return the BLOB data as Base64 encoded string
 */
function parseCoordinateString(coordStr: string | ArrayBuffer | null): [number, number][] {
  if (!coordStr) {
    console.warn('Empty coordinate string');
    return [];
  }

  try {
    // Handle case where coordStr might be a buffer/blob
    let strData: string;
    if (typeof coordStr === 'string') {
      strData = coordStr;
    } else if (coordStr instanceof ArrayBuffer) {
      // Convert ArrayBuffer to string
      strData = new TextDecoder().decode(coordStr);
    } else {
      // Try to convert to string
      strData = String(coordStr);
    }

    let cleanStr = strData.trim();

    // Debug: log first 50 chars of coordinate string
    console.log('Parsing coordinate string (first 50 chars):', cleanStr.substring(0, 50));

    // Check if it looks like a JSON array
    if (!cleanStr.startsWith('[')) {
      // It might be Base64 encoded - try to decode it
      console.log('Attempting Base64 decode...');
      try {
        const decoded = decodeBase64(cleanStr);
        console.log('Base64 decoded (first 50 chars):', decoded.substring(0, 50));
        if (decoded.startsWith('[')) {
          cleanStr = decoded;
        } else {
          console.warn('Decoded string still does not start with [');
          return [];
        }
      } catch (decodeError) {
        console.warn('Base64 decode failed:', decodeError);
        return [];
      }
    }

    const numbers: number[] = JSON.parse(cleanStr);

    // Convert flat array to pairs of [lon, lat]
    const coordinates: [number, number][] = [];
    for (let i = 0; i < numbers.length; i += 2) {
      if (i + 1 < numbers.length) {
        coordinates.push([numbers[i], numbers[i + 1]]);
      }
    }

    console.log('Parsed', coordinates.length, 'coordinate pairs');
    return coordinates;
  } catch (error) {
    console.error('Failed to parse coordinate string:', error);
    return [];
  }
}

/**
 * Check if a location is within the map bounds
 */
export function isWithinBounds(
  lat: number,
  lon: number,
  bounds: { minLon: number; minLat: number; maxLon: number; maxLat: number }
): boolean {
  return (
    lat >= bounds.minLat &&
    lat <= bounds.maxLat &&
    lon >= bounds.minLon &&
    lon <= bounds.maxLon
  );
}

// Backend API configuration
export const CONFIG = {
  API_BASE_URL: 'http://64.227.116.105:5000', // Production server
  // API_BASE_URL: 'http://192.168.1.228:5000', // Local development server
  // API_BASE_URL: 'http://192.168.1.171:5000', // Local development server
  // API_BASE_URL: 'http://192.168.1.139:5000', // Local development server
  // API_BASE_URL: 'http://10.193.143.21:5000', // Local development server
  MBTILES_FILENAME: 'map_data.mbtiles',
  MBTILES_DIR: 'map_data',
  GPS_UPDATE_INTERVAL: 5000, // milliseconds — 5s is sufficient for a walking/hiking map
  ROUTE_LINE_COLOR: '#FF0000',
  ROUTE_LINE_WIDTH: 2,
} as const;

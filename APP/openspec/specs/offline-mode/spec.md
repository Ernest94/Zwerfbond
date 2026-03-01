# Offline Mode

## Purpose

Ensures the app remains fully functional during the hiking event when no internet connection is available. All core features — map display, route viewing, and GPS tracking — must work without any network access after the initial download.

## Requirements

- The system SHALL operate all map, route, and GPS features without any network connection once the MBTiles file is downloaded.
- The system SHALL check backend availability on app startup without blocking the UI.
- The system SHALL not require internet access to open the day-selection menu when a local map is present.
- The system SHALL not require internet access to display any map screen when a local map is present.
- The system SHALL display the current local map name in the menu even when the backend is unreachable.
- The system SHALL gracefully handle all network errors by catching exceptions and updating app state rather than crashing.
- The system SHALL allow the user to continue using the existing local map if a map update check fails due to no connectivity.
- The system SHALL store the local map name persistently so it can be compared with the backend version when connectivity is restored.

## Scenarios

### Scenario 1: Full offline use after download

GIVEN the MBTiles file has been previously downloaded and the device has no internet connection
WHEN the user opens the app
THEN the system loads the day-selection menu from the local database without attempting any network requests that would block the UI

### Scenario 2: Backend check times out

GIVEN the device is offline or the backend is unreachable
WHEN the system performs a background availability check on app startup
THEN the system marks the backend as unavailable and continues without showing a network error to the user

### Scenario 3: Map use during event with no signal

GIVEN the user is on a hiking trail with no mobile signal
WHEN they navigate to a day's map and use GPS tracking
THEN all map tiles, the route polyline, and GPS position are displayed normally with no degradation

### Scenario 4: Connectivity restored mid-session

GIVEN the user starts the app offline and later regains connectivity
WHEN the app performs the next backend availability check
THEN the system detects the restored connection, compares map versions, and shows the update indicator if a newer map is available

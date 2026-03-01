# Map Download

## Purpose

Manages fetching the MBTiles raster map file from the backend server and persisting it to local device storage. This is the core data acquisition step that enables fully offline map usage.

## Requirements

- The system SHALL download the MBTiles file from the configured backend endpoint after successful password verification.
- The system SHALL display a progress indicator showing download completion as a percentage (0–100%).
- The system SHALL save the downloaded file to the app's Documents directory under `map_data/map_data.mbtiles`.
- The system SHALL reset the SQLite database connection after a successful download to ensure the new file is used.
- The system SHALL detect whether the backend has a newer map version than the locally stored map by comparing map names.
- The system SHALL show an update indicator in the day-selection menu when a newer map version is available.
- The system SHALL allow the user to trigger a re-download from the menu when an update is detected.
- The system SHALL not re-download the map if the local version already matches the backend version.
- The system SHALL handle download failures gracefully by informing the user and allowing a retry.

## Scenarios

### Scenario 1: First-time download

GIVEN the user has verified the correct password and no local map exists
WHEN the download starts
THEN the system downloads the MBTiles file, displays progress, saves it locally, and navigates to the menu on completion

### Scenario 2: Download progress tracking

GIVEN a download is in progress
WHEN the backend streams the file
THEN the system updates the progress indicator in real time from 0% to 100%

### Scenario 3: Download failure

GIVEN the user initiated a download
WHEN the network connection drops mid-download
THEN the system displays an error message and allows the user to retry the download

### Scenario 4: Map update available

GIVEN the user opens the app with an existing local map and the backend is reachable
WHEN the backend map name differs from the local map name
THEN the system shows an update indicator on the menu screen

### Scenario 5: Map already up to date

GIVEN the user opens the app with an existing local map and the backend is reachable
WHEN the backend map name matches the local map name
THEN the system does not prompt for re-download and the update indicator is hidden

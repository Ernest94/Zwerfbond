# Map Display

## Purpose

Renders the offline raster map from the locally stored MBTiles file. The map provides the visual backdrop for hiking route navigation and GPS tracking, and must function entirely without an internet connection.

## Requirements

- The system SHALL load and display raster tiles exclusively from the local MBTiles file using MapLibre GL.
- The system SHALL open the map centered on the first coordinate of the selected day's route.
- The system SHALL restrict the map view to the bounds defined in the MBTiles metadata.
- The system SHALL display the map in portrait orientation only.
- The system SHALL render the map without requiring any internet connection.
- The system SHALL show a back button that returns the user to the day-selection menu.
- The system SHALL show a recenter button that animates the map camera to the user's current GPS location.
- The system SHALL fall back to centering on the route start when GPS is unavailable and the recenter button is tapped.
- The system SHALL display an end-of-day marker at the last coordinate of the route.
- The system SHALL show a label ("Eind dag X") on the end-of-day marker when the user taps it.

## Scenarios

### Scenario 1: Map loads for selected day

GIVEN the user selected a day from the menu
WHEN the map screen opens
THEN the system displays the raster map from the local MBTiles file centered on the first coordinate of that day's route

### Scenario 2: Recenter on GPS location

GIVEN the map is displayed and GPS is active
WHEN the user taps the recenter button
THEN the map camera animates to the user's current GPS coordinates

### Scenario 3: Recenter without GPS

GIVEN the map is displayed and GPS permission is not granted or GPS is unavailable
WHEN the user taps the recenter button
THEN the map camera animates to the first coordinate of the current day's route

### Scenario 4: End-of-day marker interaction

GIVEN the map is displayed with a route
WHEN the user taps the end-of-day marker
THEN the system toggles a "Eind dag X" label on the marker

### Scenario 5: Return to menu

GIVEN the map screen is active
WHEN the user taps the back button
THEN the system navigates back to the day-selection menu

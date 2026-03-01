# GPS Tracking

## Purpose

Tracks the participant's real-time location and displays it on the map as an animated marker. Enables hikers to see their position relative to the day's route.

## Requirements

- The system SHALL request foreground location permission from the OS before activating GPS tracking.
- The system SHALL start tracking the user's location when the map screen becomes active.
- The system SHALL stop tracking the user's location when the map screen is unmounted.
- The system SHALL update the user's location at most every 5000 milliseconds.
- The system SHALL use high-accuracy GPS mode.
- The system SHALL display the user's location as an animated marker: a solid blue circle with a pulsing outer ring that scales from 1× to 2× and fades from fully opaque to transparent over 1500 milliseconds, looping continuously.
- The system SHALL update the marker's position on the map whenever a new GPS reading is received.
- The system SHALL suppress GPS tracking if the user denies the location permission.
- The system SHALL not display the GPS marker when no location fix has been obtained.
- The system SHALL display the GPS marker at any location where a fix is obtained, regardless of whether it falls within the map bounds.

## Scenarios

### Scenario 1: Permission granted, location available

GIVEN the user opens the map screen and grants location permission
WHEN a GPS fix is obtained
THEN the system displays the animated blue marker at the user's coordinates on the map

### Scenario 2: Permission denied

GIVEN the user opens the map screen and denies location permission
WHEN the map renders
THEN the system does not display a GPS marker and GPS tracking is inactive

### Scenario 3: Location update received

GIVEN GPS tracking is active and a marker is displayed
WHEN a new GPS reading arrives after the 5-second interval
THEN the system moves the marker to the updated coordinates without resetting the animation

### Scenario 4: Map screen closed

GIVEN the user navigates away from the map screen
WHEN the component unmounts
THEN the system stops the GPS location watcher to prevent battery drain

### Scenario 5: User outside map bounds

GIVEN GPS tracking is active and the map has defined bounds
WHEN the user's GPS coordinates fall outside the MBTiles map bounds
THEN the system displays the marker at the user's coordinates and the recenter button falls back to the route start instead of the user's location

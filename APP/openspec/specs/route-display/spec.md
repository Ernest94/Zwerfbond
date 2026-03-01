# Route Display

## Purpose

Renders the hiking route for a selected day as a polyline overlay on the map. Route data is stored inside the MBTiles SQLite database and decoded at runtime.

## Requirements

- The system SHALL load route coordinates for the selected day from the `route_coordinates` table in the local MBTiles SQLite database.
- The system SHALL decode the base64-encoded coordinate string into a sequence of longitude/latitude pairs.
- The system SHALL render the route as a continuous polyline on the map layer above the raster tiles.
- The system SHALL use the configured line color (`#FF0000`) and width (2px) for the route polyline.
- The system SHALL place a marker at the last coordinate of the route to indicate the end of the day's walk.
- The system SHALL handle missing or empty route data gracefully without crashing.
- The system SHALL update the displayed route when the user navigates to a different day.

## Scenarios

### Scenario 1: Route loaded for selected day

GIVEN the user has selected a day from the menu
WHEN the map screen opens
THEN the system queries the MBTiles database for that day's coordinates and renders the route as a red polyline

### Scenario 2: End-of-day marker placed

GIVEN the route coordinates are loaded
WHEN the map is rendered
THEN the system places a marker at the last coordinate in the route

### Scenario 3: Route data missing

GIVEN the selected day has no entry in the `route_coordinates` table
WHEN the map screen opens
THEN the system renders the map without a polyline and does not display an end-of-day marker

### Scenario 4: Day change

GIVEN the map screen is active and the user returns to the menu to select a different day
WHEN the map screen opens for the new day
THEN the system replaces the previous polyline with the new day's route

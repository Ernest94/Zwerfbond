# Day Selection

## Purpose

Provides a menu screen where participants choose which day's hiking route to view. Supports both a 4-day and a 6-day hike variant and surfaces map update availability.

## Requirements

- The system SHALL display the day-selection menu after the user has a valid local map.
- The system SHALL load the list of available days from the `metadata` table in the local MBTiles database.
- The system SHALL fall back to a default list of 6 days ("dag 1" through "dag 6") if the database does not provide a day list.
- The system SHALL display one tappable button per available day.
- The system SHALL display the map/event name from the MBTiles metadata at the top of the menu.
- The system SHALL navigate to the map screen with the selected day when a day button is tapped.
- The system SHALL show a visual update indicator when the backend has a newer map version than the local copy.
- The system SHALL allow the user to initiate a map update from the menu by tapping the update indicator.
- The system SHALL check backend availability and compare map names on each visit to the menu screen.

## Scenarios

### Scenario 1: Menu loads with database days

GIVEN a local MBTiles file with a valid `days` metadata entry
WHEN the user arrives at the menu screen
THEN the system displays buttons for each day listed in the metadata

### Scenario 2: Menu loads with fallback days

GIVEN a local MBTiles file without a `days` metadata entry
WHEN the user arrives at the menu screen
THEN the system displays 6 day buttons ("dag 1" through "dag 6")

### Scenario 3: User selects a day

GIVEN the menu is displayed with available days
WHEN the user taps a day button
THEN the system stores the selected day and navigates to the map screen

### Scenario 4: Update indicator shown

GIVEN the backend is reachable and its map name differs from the local map name
WHEN the menu screen loads
THEN the system displays an update indicator alongside the map name

### Scenario 5: User triggers update

GIVEN the update indicator is visible
WHEN the user taps the update indicator
THEN the system navigates to the login/download screen to fetch the new map

# Authentication

## Purpose

Manages initial access to the app by verifying a shared event password with the backend before allowing map download. Authentication is a one-time gate: once the map is downloaded locally, no further authentication is required.

## Requirements

- The system SHALL present a password input field on first launch.
- The system SHALL send the entered password to the backend for verification before initiating any download.
- The system SHALL display an error message when the password is incorrect and allow the user to retry.
- The system SHALL not store the password locally after verification.
- The system SHALL bypass the password prompt if a local map is already present and the backend is unreachable.
- The system SHALL navigate to the day-selection menu upon successful verification and completed download.
- The system SHALL disable the submit button while a verification request is in flight.

## Scenarios

### Scenario 1: Correct password entered

GIVEN the app is opened for the first time and the backend is reachable
WHEN the user enters the correct event password and submits
THEN the system verifies the password, initiates the MBTiles download, and navigates to the menu upon completion

### Scenario 2: Incorrect password entered

GIVEN the backend is reachable
WHEN the user submits an incorrect password
THEN the system displays an error message and keeps the password input visible for retry

### Scenario 3: Backend unreachable, no local map

GIVEN the backend is not reachable and no local map exists
WHEN the login screen loads
THEN the system disables the submit button and informs the user that no offline map is available

### Scenario 4: Backend unreachable, local map present

GIVEN the backend is not reachable and a local map is already downloaded
WHEN the login screen loads
THEN the system offers the user the option to continue with the existing local map without re-authenticating

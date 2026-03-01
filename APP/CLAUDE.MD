# Project Overview
This is an app for a hike event. The app is used during a multiple days hiking event during Eastern and Ascension Day.
The app contains the routemap for the multiple days of hiking. It is a 4 days or 6 days hike.
On first opening of the app the routemap can be downloaded when submitting the correct pasword.
Once the map is downloaded the app can be used without internet connection.
The routemap is saved in a sqlite .mbtiles file and served in as raster layer.


# Build & Run Commands
- Start: `npx expo start`
- iOS: `npx expo run:ios`
- Android: `npx expo run:android`
- Lint: `npm run lint`

# Code Style
- TypeScript, strict mode
- 2-space indentation
- camelCase for functions/variables
- PascalCase for components

# Project Structure
- `src/screens/` — app screens
- `src/components/` — reusable UI
- `src/store/` — Redux state
- `src/services/` — API calls

# Architecture Decisions
- Redux for global state
- Keep component state local unless shared
- All API calls go through services layer

# Important Rules
- NEVER commit directly to main
- Always test on both iOS and Android before PR
- Don't hardcode strings; use constants
- Keep in mind the basic functionality: 
   - Downloading the .mbtiles from the backend.
   - Displaying the map from the .mbtiles.
   - The route is displayed on the map.
   - There is a menu and the user can navigate to the routes on the map.
- Include offline mode considerations
- Ensure compatibility with both iOS and Android platforms
- Use React Native best practices
- Maintain clean and modular code structure
- Follow Zwerfbond's design guidelines
- Test on a variety of devices and screen sizes
- Don't write verbose code; be concise and to the point.
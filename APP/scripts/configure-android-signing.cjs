#!/usr/bin/env node
/**
 * Patches android/app/build.gradle after expo prebuild to enable release signing
 * via android/keystore.properties. Run this before ./gradlew bundleRelease.
 *
 * Uses exact string matching on the known expo-generated template structure
 * to avoid fragile regex patterns on nested Groovy blocks.
 */

const fs = require('fs');
const FILE = 'android/app/build.gradle';
let content = fs.readFileSync(FILE, 'utf8');

// 1. Add keystore.properties loader before `android {`
if (!content.includes('keystorePropertiesFile')) {
  const loader =
    `def keystorePropertiesFile = rootProject.file("keystore.properties")\n` +
    `def keystoreProperties = new Properties()\n` +
    `if (keystorePropertiesFile.exists()) {\n` +
    `    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))\n` +
    `}\n\n`;
  content = content.replace(/^android \{/m, loader + 'android {');
}

// 2. Insert release signingConfig block after the debug block closes
//    Targets the exact closing lines of the debug signingConfig in the expo template.
const DEBUG_SIGNING_TAIL =
  `            storeFile file('debug.keystore')\n` +
  `            storePassword 'android'\n` +
  `            keyAlias 'androiddebugkey'\n` +
  `            keyPassword 'android'\n` +
  `        }`;

const RELEASE_SIGNING_BLOCK =
  `\n        release {\n` +
  `            storeFile file(keystoreProperties["storeFile"])\n` +
  `            storePassword keystoreProperties["storePassword"]\n` +
  `            keyAlias keystoreProperties["keyAlias"]\n` +
  `            keyPassword keystoreProperties["keyPassword"]\n` +
  `        }`;

if (!content.includes('keystoreProperties["storeFile"]')) {
  if (content.includes(DEBUG_SIGNING_TAIL)) {
    content = content.replace(DEBUG_SIGNING_TAIL, DEBUG_SIGNING_TAIL + RELEASE_SIGNING_BLOCK);
  } else {
    console.error('ERROR: Could not find debug signingConfig block to insert release block after.');
    process.exit(1);
  }
}

// 3. Change release buildType's signingConfig from debug → release.
//    The comment on the preceding line is unique to the release buildType.
const DEBUG_SIGNING_IN_RELEASE =
  `// see https://reactnative.dev/docs/signed-apk-android.\n            signingConfig signingConfigs.debug`;
const RELEASE_SIGNING_IN_RELEASE =
  `// see https://reactnative.dev/docs/signed-apk-android.\n            signingConfig signingConfigs.release`;

if (content.includes(DEBUG_SIGNING_IN_RELEASE)) {
  content = content.replace(DEBUG_SIGNING_IN_RELEASE, RELEASE_SIGNING_IN_RELEASE);
} else if (content.includes('signingConfig signingConfigs.debug')) {
  // Fallback: replace any remaining occurrence in the release buildType context
  console.warn('WARN: exact match for release signingConfig not found, falling back to global replace');
  content = content.replace(
    /(\brelease\s*\{[^}]*?)signingConfig signingConfigs\.debug/s,
    '$1signingConfig signingConfigs.release'
  );
}

// 4. Patch versionCode from BUILD_BUILDID if available
const buildId = process.env.BUILD_BUILDID;
if (buildId) {
  content = content.replace(/versionCode \d+/, `versionCode ${parseInt(buildId, 10)}`);
  console.log('✓ versionCode set to:', buildId);
}

fs.writeFileSync(FILE, content);
console.log('✓ build.gradle patched for release signing');

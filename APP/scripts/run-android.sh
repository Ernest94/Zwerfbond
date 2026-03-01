#!/bin/bash
# Launches the Android emulator (if not already running), waits for it to boot,
# then runs expo run:android.

AVD_NAME="${1:-Galaxy_Nexus_API_33}"
EMULATOR_CMD="$HOME/Library/Android/sdk/emulator/emulator"
ADB_CMD="$HOME/Library/Android/sdk/platform-tools/adb"
BOOT_TIMEOUT=120  # seconds

# Check if an emulator is already running
RUNNING=$("$ADB_CMD" devices 2>/dev/null | grep "emulator-" | head -1 | awk '{print $1}')

if [ -n "$RUNNING" ]; then
  echo "Emulator already running: $RUNNING"
else
  echo "Starting emulator: $AVD_NAME"
  "$EMULATOR_CMD" -avd "$AVD_NAME" -no-snapshot-load &
  EMULATOR_PID=$!

  # Wait for the device to appear in adb
  echo "Waiting for emulator to connect to adb..."
  "$ADB_CMD" wait-for-device

  RUNNING=$("$ADB_CMD" devices 2>/dev/null | grep "emulator-" | head -1 | awk '{print $1}')
  echo "Emulator connected: $RUNNING"
fi

# Wait for boot to complete
echo "Waiting for emulator to finish booting..."
ELAPSED=0
while [ $ELAPSED -lt $BOOT_TIMEOUT ]; do
  BOOT_COMPLETED=$("$ADB_CMD" -s "$RUNNING" shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
  if [ "$BOOT_COMPLETED" = "1" ]; then
    echo "Emulator booted successfully."
    break
  fi
  sleep 2
  ELAPSED=$((ELAPSED + 2))
done

if [ "$BOOT_COMPLETED" != "1" ]; then
  echo "ERROR: Emulator did not boot within ${BOOT_TIMEOUT}s"
  exit 1
fi

# Run expo
npx expo run:android --device "$RUNNING"

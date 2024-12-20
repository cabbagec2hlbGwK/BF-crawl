#!/bin/bash



# Generate random dimensions

WIDTH=$((RANDOM % 800 + 800))   # Random width between 800 and 1600

HEIGHT=$((RANDOM % 450 + 450))  # Random height between 450 and 900



# Print the random dimensions for debugging

echo "Random display size: ${WIDTH}x${HEIGHT}"



# Function to find an available display

find_available_display() {

    for DISPLAY_NUMBER in {99..199}; do

        if ! [ -e "/tmp/.X${DISPLAY_NUMBER}-lock" ]; then

            echo "${DISPLAY_NUMBER}"

            return

        fi

    done

    echo "Error: No available display found!" >&2

    exit 1

}



# Find an available display number

DISPLAY_NUMBER=$(find_available_display)

echo "Using display number: ${DISPLAY_NUMBER}"



# Remove any stale lock file for the selected display

if [ -e "/tmp/.X${DISPLAY_NUMBER}-lock" ]; then

    echo "Removing stale lock file for display :${DISPLAY_NUMBER}"

    rm -f "/tmp/.X${DISPLAY_NUMBER}-lock"

fi



# Start Xvfb with the random display size

Xvfb :${DISPLAY_NUMBER} -screen 0 ${WIDTH}x${HEIGHT}x24 &

XVFB_PID=$!



# Export DISPLAY environment variable

export DISPLAY=:${DISPLAY_NUMBER}



# Wait for Xvfb to start

sleep 2



# Verify Xvfb is running by checking the lock file

if ! [ -e "/tmp/.X${DISPLAY_NUMBER}-lock" ]; then

    echo "Failed to start Xvfb on display :${DISPLAY_NUMBER}" >&2

    kill ${XVFB_PID} 2>/dev/null

    exit 1

fi



# Run the Python script

python3 agent.py



# Clean up Xvfb after the script finishes

kill ${XVFB_PID}



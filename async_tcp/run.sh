#! /bin/bash
# Tests the server and client.
set -e

./server.py &
echo "Server started"
sleep 1
./client.py &
sleep 6
echo "Should have finished by now"
# Kill the server as it doesn't stop itself
killall python3
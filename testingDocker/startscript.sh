#!/bin/bash

# Start the second process
cd web && python3 -m http.server 5006 &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start my_second_process: $status"
  exit $status
fi

# Start the first process
cd flask && chmod +x ./script.sh && ./script.sh
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start my_first_process: $status"
  exit $status
fi

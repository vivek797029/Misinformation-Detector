#!/bin/bash
# Free ports 8000–8010
for PORT in {8000..8010}; do
  lsof -ti:$PORT | xargs -r kill -9
done

# Wait 1 second to ensure ports are freed
sleep 1

# Start server on first free port
for PORT in {8000..8010}; do
  if ! lsof -i:$PORT > /dev/null; then
    echo "Starting server on port $PORT"
    uvicorn app:app --reload --port $PORT
    exit 0
  fi
done

echo "No free ports available between 8000–8010"

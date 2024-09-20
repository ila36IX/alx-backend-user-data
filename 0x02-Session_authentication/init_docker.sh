#!/bin/bash

IMAGE_NAME="0x01-basic_authentication"
CONTAINER_NAME="0x01-container"

# Check if image exists
if ! docker images --quiet --filter=reference="$IMAGE_NAME" | grep -q "$IMAGE_NAME"; then
    # Build image if it doesn't exist
    docker build -t "$IMAGE_NAME" . || exit 1
fi

# Check if container exists
if ! docker ps --quiet --filter=name="$CONTAINER_NAME" | grep -q "$CONTAINER_NAME"; then
    # Run container if it doesn't exist
    docker run -d -p 5000:5000 -v "$(pwd):/app" --env AUTH_TYPE=session_exp_auth --env SESSION_DURATION=15 --env  SESSION_NAME=_my_session_id --name "$CONTAINER_NAME" "$IMAGE_NAME" || exit 1
else
    # Start existing container
    docker start "$CONTAINER_NAME" || exit 1
fi

echo "Happy coding :)"

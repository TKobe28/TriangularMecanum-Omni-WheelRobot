#!/bin/bash

SERVICE_NAME="server.service"
DEST_PATH="/etc/systemd/system/$SERVICE_NAME"

# Copy the service file, overwriting if it exists
sudo cp "$SERVICE_NAME" "$DEST_PATH"
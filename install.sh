#!/bin/bash

# SnapStream — Raycast Script Command Installer

SCRIPTS_DIR="$HOME/.raycast/scripts"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing SnapStream for Raycast..."

# Create Raycast scripts directory if needed
mkdir -p "$SCRIPTS_DIR"

# Copy the script
cp "$SOURCE_DIR/stream-tv.py" "$SCRIPTS_DIR/stream-tv.py"
chmod +x "$SCRIPTS_DIR/stream-tv.py"

# Copy channels config (don't overwrite existing)
if [ -f "$SCRIPTS_DIR/channels.json" ]; then
    echo "channels.json already exists — skipping (your channels are preserved)"
else
    if [ -f "$SOURCE_DIR/channels.json" ]; then
        cp "$SOURCE_DIR/channels.json" "$SCRIPTS_DIR/channels.json"
    else
        cp "$SOURCE_DIR/channels.example.json" "$SCRIPTS_DIR/channels.json"
    fi
    echo "Copied channels.json — edit this file to add your own channels"
fi

echo ""
echo "Done! Open Raycast and make sure Script Commands are enabled:"
echo "  1. Open Raycast Settings (Cmd+,)"
echo "  2. Go to Extensions > Script Commands"
echo "  3. Add $SCRIPTS_DIR if not already listed"
echo ""
echo "Then type 'SnapStream' in Raycast to start watching."

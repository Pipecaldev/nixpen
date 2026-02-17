#!/bin/bash

# Configuration
APP_NAME="NixPen"
APP_DIR="$HOME/Applications"
APP_IMAGE="$APP_DIR/$APP_NAME.AppImage"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
desktop_file="$HOME/.local/share/applications/nixpen.desktop"

echo "Uninstalling NixPen..."

# 1. Remove Desktop Entry
if [ -f "$desktop_file" ]; then
    rm "$desktop_file"
    echo "Removed desktop entry."
fi

# 2. Remove Icon
if [ -f "$ICON_DIR/nixpen.png" ]; then
    rm "$ICON_DIR/nixpen.png"
    echo "Removed icon."
fi

# 3. Remove AppImage
if [ -f "$APP_IMAGE" ]; then
    rm "$APP_IMAGE"
    echo "Removed AppImage."
fi

# 4. Update Desktop Database
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null

echo "✅ Uninstallation complete."

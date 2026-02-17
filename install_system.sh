#!/bin/bash

# Configuration
APP_NAME="NixPen"
APP_DIR="$HOME/Applications"
APP_IMAGE="$APP_DIR/$APP_NAME.AppImage"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
desktop_file="$HOME/.local/share/applications/nixpen.desktop"

# 1. Create Directories
mkdir -p "$APP_DIR"
mkdir -p "$ICON_DIR"
mkdir -p "$HOME/.local/share/applications"

# 2. Check for AppImage
SOURCE_APPIMAGE="NixPen-x86_64.AppImage"
if [ ! -f "$SOURCE_APPIMAGE" ]; then
    echo "Error: $SOURCE_APPIMAGE not found in current directory."
    exit 1
fi

# 3. Copy AppImage
echo "Installing AppImage to $APP_DIR..."
cp "$SOURCE_APPIMAGE" "$APP_IMAGE"
chmod +x "$APP_IMAGE"

# 4. Install Icon
echo "Installing Icon..."
# Extract icon if possible or use the one in assets/
if [ -f "assets/nixpen.png" ]; then
    cp "assets/nixpen.png" "$ICON_DIR/nixpen.png"
else
    # Fallback: try to extract from AppImage (requires --appimage-extract)
    # For now, just warn
    echo "Warning: assets/nixpen.png not found. Icon might be missing."
fi

# 5. Create Desktop Entry
echo "Creating Desktop Entry..."
ICON_PATH="$ICON_DIR/nixpen.png"
cat > "$desktop_file" <<EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
Comment=Free screen annotation tool for Linux
Exec=$APP_IMAGE
Icon=$ICON_PATH
Categories=Utility;Graphics;
Terminal=false
StartupNotify=true
EOF

# 6. Update Caches
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null
gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" 2>/dev/null

echo "✅ Installation complete!"
echo "You can now find NixPen in your application menu."

#!/bin/bash

# ghman uninstallation script

echo "Uninstalling ghman..."

# 1. Remove symlink if it exists
INSTALL_DIR="/usr/local/bin"
if [ -L "$INSTALL_DIR/ghman" ]; then
    echo "Removing symlink $INSTALL_DIR/ghman..."
    if [ -w "$INSTALL_DIR/ghman" ] || [ -w "$INSTALL_DIR" ]; then
        rm "$INSTALL_DIR/ghman"
    else
        echo "Requires sudo to remove symlink from $INSTALL_DIR"
        sudo rm "$INSTALL_DIR/ghman"
    fi
fi

# 2. Remove configuration directory
CONFIG_DIR="$HOME/.ghman"
if [ -d "$CONFIG_DIR" ]; then
    read -p "Do you want to remove the configuration directory and saved token (~/.ghman)? [y/N] " response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Removing $CONFIG_DIR..."
        rm -rf "$CONFIG_DIR"
    else
        echo "Keeping $CONFIG_DIR."
    fi
fi

# 3. Remove venv and wrapper
echo "Cleaning up virtual environment and wrapper..."
rm -rf .venv
rm -f ghman

echo ""
echo "ghman uninstallation steps completed."

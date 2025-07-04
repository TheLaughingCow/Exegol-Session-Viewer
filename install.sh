#!/bin/bash

set -e

TARGET="/opt/Exegol-Session-Viewer"
SCRIPT="esw-launcher.py"
ALIAS="alias esw='python3 $TARGET/$SCRIPT'"

echo "[+] Moving project to $TARGET..."

cd "$(dirname "$0")/.."  
sudo rm -rf "$TARGET"
sudo mv Exegol-Session-Viewer "$TARGET"

 
if [ -n "$ZSH_VERSION" ]; then
    RC="$HOME/.zshrc"
else
    RC="$HOME/.bashrc"
fi
 
if ! grep -Fxq "$ALIAS" "$RC"; then
    echo "[+] Adding alias to $RC"
    echo "$ALIAS" >> "$RC"
else
    echo "[*] Alias already exists in $RC"
fi

echo
echo "[✓] Installed successfully."
echo "➡️  Restart your terminal or run: source $RC"
echo "➡️  Then use: esw"

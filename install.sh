#!/bin/bash

set -e

TARGET="/opt/Exegol-Session-Viewer"
SCRIPT="esw-launcher.py"
ALIAS="alias esv='python3 $TARGET/$SCRIPT'"

if [ "$EUID" -ne 0 ]; then
    echo "[!] This script must be run as root (use sudo)"
    exit 1
fi

echo "[+] Moving project to $TARGET..."

cd "$(dirname "$0")/.."
sudo rm -rf "$TARGET"
sudo mv Exegol-Session-Viewer "$TARGET"
sudo chown -R root:root "$TARGET"
sudo chmod -R 755 "$TARGET"

if [ -n "$ZSH_VERSION" ] || [ "$(basename "$SHELL")" = "zsh" ]; then
    RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ "$(basename "$SHELL")" = "bash" ]; then
    RC="$HOME/.bashrc"
else
    RC="$HOME/.bashrc"
fi

if [ ! -f "$RC" ]; then
    touch "$RC"
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
echo "➡️  Then use: esv"

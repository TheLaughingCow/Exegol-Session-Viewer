#!/bin/bash

set -e

TARGET="/opt/Exegol-Session-Viewer"
SCRIPT="esw-launcher.py"
ALIAS="alias esv='python3 $TARGET/$SCRIPT'"

echo "[+] Moving project to $TARGET..."

cd "$(dirname "$0")/.."

if [ -w "/opt" ]; then
    rm -rf "$TARGET"
    mv Exegol-Session-Viewer "$TARGET"
    chmod -R 755 "$TARGET"
else
    echo "[+] Insufficient permissions, using sudo for /opt only..."
    sudo rm -rf "$TARGET"
    sudo mv Exegol-Session-Viewer "$TARGET"
    sudo chmod -R 755 "$TARGET"
    sudo chown -R "$(whoami):$(whoami)" "$TARGET"
fi

for RC in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ ! -f "$RC" ]; then
        touch "$RC"
    fi

    if ! grep -Fxq "$ALIAS" "$RC"; then
        echo "[+] Adding alias to $RC"
        echo "$ALIAS" >> "$RC"
    else
        echo "[*] Alias already exists in $RC"
    fi
done

echo
echo "[✓] Installed successfully."
echo "➡️  To use: esv"
echo "➡️  Run: source ~/.bashrc or source ~/.zshrc depending on your shell"

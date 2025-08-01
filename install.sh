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

USER_SHELL="$(basename "$SHELL")"
echo "[+] Shell détecté via \$SHELL : $USER_SHELL"

if [[ "$USER_SHELL" == "zsh" ]]; then
    RC_FILE="$HOME/.zshrc"
elif [[ "$USER_SHELL" == "bash" ]]; then
    RC_FILE="$HOME/.bashrc"
else
    echo "[!] Shell inconnu ($USER_SHELL), défaut sur ~/.bashrc"
    RC_FILE="$HOME/.bashrc"
fi

if [ ! -f "$RC_FILE" ]; then
    touch "$RC_FILE"
fi

if ! grep -Fxq "$ALIAS" "$RC_FILE"; then
    echo "[+] Adding alias to $RC_FILE"
    echo "$ALIAS" >> "$RC_FILE"
else
    echo "[*] Alias already exists in $RC_FILE"
fi

echo "[+] Sourcing $RC_FILE to load alias..."
if [[ "$USER_SHELL" == "zsh" && "$RC_FILE" == *zshrc ]]; then
    source "$RC_FILE"
    echo "[*] Alias 'esv' is now available in your current shell."
elif [[ "$USER_SHELL" == "bash" && "$RC_FILE" == *bashrc ]]; then
    source "$RC_FILE"
    echo "[*] Alias 'esv' is now available in your current shell."
else
    echo "[!] Shell mismatch : ne source pas $RC_FILE dans $USER_SHELL"
    echo "💡 Tu peux le faire manuellement : source $RC_FILE"
fi

echo
echo "[✓] Installed successfully."
echo "➡️  You can now use: esv"

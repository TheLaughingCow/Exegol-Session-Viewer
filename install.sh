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

# Détection fiable du shell courant
CURRENT_SHELL="$(ps -p $$ -o comm= | tail -n 1)"

if [[ "$CURRENT_SHELL" == "zsh" ]]; then
    RC_FILE="$HOME/.zshrc"
elif [[ "$CURRENT_SHELL" == "bash" ]]; then
    RC_FILE="$HOME/.bashrc"
else
    echo "[!] Shell inconnu ($CURRENT_SHELL), défaut sur ~/.bashrc"
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

# Sourcing automatique uniquement si cohérent
echo "[+] Sourcing $RC_FILE to load alias..."
if [[ "$CURRENT_SHELL" == "zsh" && "$RC_FILE" == *zshrc ]]; then
    source "$RC_FILE"
elif [[ "$CURRENT_SHELL" == "bash" && "$RC_FILE" == *bashrc ]]; then
    source "$RC_FILE"
else
    echo "[!] Shell mismatch : ne source pas $RC_FILE dans $CURRENT_SHELL"
    echo "💡 Tu peux le faire manuellement : source $RC_FILE"
fi

echo
echo "[✓] Installed successfully."
echo "➡️  You can now use: esv"

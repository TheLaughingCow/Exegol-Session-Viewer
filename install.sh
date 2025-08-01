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

CURRENT_SHELL="$(basename "$0")"
if [[ "$CURRENT_SHELL" == "bash" ]]; then
    RC="$HOME/.bashrc"
elif [[ "$CURRENT_SHELL" == "zsh" ]]; then
    RC="$HOME/.zshrc"
else
    RC="$HOME/.bashrc"
fi

if [ ! -f "$RC" ]; then
    touch "$RC"
fi

if ! grep -Fxq "$ALIAS" "$RC"; then
    echo "[+] Adding alias to $RC"
    echo "$ALIAS" >> "$RC"
    SHOULD_SOURCE=1
else
    echo "[*] Alias already exists in $RC"
    SHOULD_SOURCE=1
fi

if [ "$SHOULD_SOURCE" = "1" ]; then
    if [[ "$CURRENT_SHELL" == "bash" && "$RC" == *bashrc ]]; then
        echo "[+] Sourcing $RC (Bash)..."
        source "$RC"
    elif [[ "$CURRENT_SHELL" == "zsh" && "$RC" == *zshrc ]]; then
        echo "[+] Sourcing $RC (Zsh)..."
        source "$RC"
    else
        echo "[!] Shell mismatch ($CURRENT_SHELL vs $RC) — skipping source"
        echo "💡 Run manually: source $RC"
    fi
    echo "[*] Alias 'esv' is now available in your current shell (if sourced)."
fi

echo
echo "[✓] Installed successfully."
echo "➡️  You can now use: esv"

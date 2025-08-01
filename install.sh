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

if [ -n "$ZSH_VERSION" ] || [ "$(basename "$SHELL")" = "zsh" ]; then
    RC="$HOME/.zshrc"
    CURRENT_SHELL="zsh"
elif [ -n "$BASH_VERSION" ] || [ "$(basename "$SHELL")" = "bash" ]; then
    RC="$HOME/.bashrc"
    CURRENT_SHELL="bash"
else
    RC="$HOME/.bashrc"
    CURRENT_SHELL="bash"
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
    if [ "$CURRENT_SHELL" = "zsh" ] && [[ "$SHELL" == *zsh ]]; then
        echo "[+] Sourcing $RC (Zsh)..."
        source "$RC"
    elif [ "$CURRENT_SHELL" = "bash" ] && [[ "$SHELL" == *bash ]]; then
        echo "[+] Sourcing $RC (Bash)..."
        source "$RC"
    else
        echo "[!] Shell mismatch — please manually run: source $RC"
    fi
    echo "[*] Alias 'esv' is now available in your current shell (if sourced)."
fi

echo
echo "[✓] Installed successfully."
echo "➡️  You can now use: esv"

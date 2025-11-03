#!/bin/bash
set -e

echo "Installing ~ATH..."

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 required"
    exit 1
fi

# Clone or update repo
if [ -d "$HOME/.ATH" ]; then
    cd "$HOME/.ATH" && git pull
else
    git clone https://github.com/krisciu/-ATH.git "$HOME/.ATH"
fi

# Install dependencies
cd "$HOME/.ATH"
pip3 install -q -r requirements.txt

# Create launcher directory if needed
mkdir -p "$HOME/.local/bin"

# Create launcher
cat > "$HOME/.local/bin/tildeath" << 'LAUNCHER'
#!/bin/bash
cd "$HOME/.ATH" && python3 main.py "$@"
LAUNCHER
chmod +x "$HOME/.local/bin/tildeath"

echo "✓ Installation complete"
echo ""
echo "Run: tildeath"
echo ""
echo "If 'tildeath' command not found, add to PATH:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""


#!/bin/bash

# ghman installation script

set -e

echo "Installing ghman..."

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# 2. Setup Virtual Environment
echo "Setting up virtual environment (.venv)..."
python3 -m venv .venv

# 3. Install dependencies in venv
echo "Installing dependencies into .venv..."
./.venv/bin/python3 -m pip install --upgrade pip
./.venv/bin/python3 -m pip install -r requirements.txt

# 4. Create wrapper script
echo "Creating wrapper script 'ghman'..."
cat << EOF > ghman
#!/bin/bash
PROJECT_DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" && pwd )"
"\$PROJECT_DIR/.venv/bin/python3" "\$PROJECT_DIR/ghman.py" "\$@"
EOF
chmod +x ghman

# 5. Final instructions
INSTALL_DIR="/usr/local/bin"
PROJECT_DIR=$(pwd)

echo ""
echo "Installation complete!"
echo ""
echo "To run ghman from anywhere, you can:"
echo "1. Symlink the wrapper (requires sudo):"
echo "   sudo ln -sf $PROJECT_DIR/ghman $INSTALL_DIR/ghman"
echo ""
echo "2. Or add this directory to your PATH (add to ~/.zshrc or ~/.bashrc):"
echo "   export PATH=\"\$PATH:$PROJECT_DIR\""
echo ""
echo "Try running: ./ghman --help"

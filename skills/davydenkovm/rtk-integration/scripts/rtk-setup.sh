#!/usr/bin/env bash
# rtk-setup.sh — Install RTK and verify it works
# Usage: bash rtk-setup.sh

set -e

echo "🔧 RTK Setup"
echo "============"

# Check if already installed
if command -v rtk &>/dev/null; then
  echo "✅ RTK already installed: $(rtk --version)"
  echo ""
  echo "📊 Current token savings:"
  rtk gain 2>/dev/null || echo "(no data yet — run some commands first)"
  exit 0
fi

echo "📦 Installing RTK..."

OS="$(uname -s)"
ARCH="$(uname -m)"

if [[ "$OS" == "Darwin" ]] && command -v brew &>/dev/null; then
  echo "   Using Homebrew..."
  brew install rtk
elif [[ "$OS" == "Linux" ]] || [[ "$OS" == "Darwin" ]]; then
  echo "   Using install script..."
  curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

  # Ensure PATH is updated
  RTK_BIN="$HOME/.local/bin"
  if [[ ":$PATH:" != *":$RTK_BIN:"* ]]; then
    export PATH="$RTK_BIN:$PATH"
    echo ""
    echo "⚠️  Add to your shell profile (run once):"
    echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "   # or: >> ~/.zshrc"
  fi
else
  echo "❌ Unsupported OS: $OS"
  echo "   Download manually: https://github.com/rtk-ai/rtk/releases"
  exit 1
fi

echo ""

# Verify
if command -v rtk &>/dev/null; then
  echo "✅ RTK installed successfully: $(rtk --version)"
  echo ""
  echo "📊 Initial stats:"
  rtk gain 2>/dev/null || echo "(no data yet)"
  echo ""
  echo "🚀 Ready! The agent will now use rtk-prefixed commands automatically."
  echo "   Run 'rtk gain' anytime to see token savings."
else
  echo "❌ Installation failed. Try manually:"
  echo "   cargo install --git https://github.com/rtk-ai/rtk"
  exit 1
fi

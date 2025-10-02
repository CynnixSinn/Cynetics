#!/bin/bash

# Cynetics Installation Script

set -e

echo "🚀 Installing Cynetics..."
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.10+ required. Found: $python_version"
    exit 1
fi
echo "✓ Python $python_version"

# Check Node.js version
echo "Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi
node_version=$(node --version | sed 's/v//')
echo "✓ Node.js $node_version"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Python dependencies installed"

# Install MCP servers
echo ""
echo "Installing MCP servers..."
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-shell
npm install -g @modelcontextprotocol/server-memory
echo "✓ MCP servers installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo "⚠️  Please edit .env and add your API keys"
fi

# Initialize configuration
echo ""
echo "Initializing Cynetics configuration..."
python3 cynetics.py --init
echo "✓ Configuration initialized"

# Create necessary directories
mkdir -p workspace artifacts logs
echo "✓ Created directories"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env file and add your API keys"
echo "  2. Run: python3 cynetics.py --description 'Your project idea'"
echo ""

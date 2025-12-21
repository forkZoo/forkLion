#!/bin/bash

# ForkLion Web Interface Launcher

echo "🐵 Starting ForkLion Web Interface..."
echo ""

# Check if lion exists
if [ ! -f "lion_data/dna.json" ]; then
    echo "⚠️  No lion found! Initializing..."
    python src/cli.py init
    echo ""
fi

# Start web server
echo "🚀 Starting web server..."
python web/serve.py

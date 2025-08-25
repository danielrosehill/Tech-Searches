#!/bin/bash
# Tech Searches Formatting Agent Wrapper Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="$SCRIPT_DIR/processing/formatting-agent"

# Check if virtual environment exists
if [ ! -d "$AGENT_DIR/venv" ]; then
    echo "Setting up virtual environment..."
    cd "$AGENT_DIR"
    uv venv venv
    source venv/bin/activate
    uv pip install -r requirements.txt
    echo "Setup complete!"
else
    cd "$AGENT_DIR"
    source venv/bin/activate
fi

# Run the formatting agent with all passed arguments
python3 format_notes.py "$@"

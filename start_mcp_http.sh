#!/bin/bash
# Mobile-Use MCP Server HTTP模式启动脚本

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PYTHONPATH="$SCRIPT_DIR"

if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

echo "启动Mobile-Use MCP Server (HTTP模式)..."
python3 "$SCRIPT_DIR/mcp_server_http.py"

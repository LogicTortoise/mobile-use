#!/bin/bash
# Mobile-Use MCP Server启动脚本

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 设置Python路径
export PYTHONPATH="$SCRIPT_DIR"

# 激活虚拟环境（如果存在）
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# 启动MCP服务器
python3 "$SCRIPT_DIR/mcp_server.py"

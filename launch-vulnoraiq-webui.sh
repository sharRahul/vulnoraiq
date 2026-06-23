#!/usr/bin/env bash
# VulnoraIQ Web UI double-click launcher for Linux.
set -euo pipefail
cd "$(dirname "$0")"
echo "Starting VulnoraIQ Web UI..."
python3 scripts/launch_webui.py "$@"
echo "VulnoraIQ Web UI launcher has stopped."
read -r -p "Press Enter to close this window..." _

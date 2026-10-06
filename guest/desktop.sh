#!/bin/sh
# Local files remain usable even when the optional AI service is offline.
set -eu
# Electron's native Wayland UI can stall before publishing its web document.
/opt/OpenCode/ai.opencode.desktop --force-renderer-accessibility --ozone-platform=x11 &
# Keep the desktop bus alive when users close every application.
exec sleep infinity

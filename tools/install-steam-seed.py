#!/usr/bin/env python3
"""Install an account-free Steam client in a NEW disposable device-build instance.

Execute this whole script inside the running ARM64 Yibu build instance. It
installs distribution dependencies and runs Valve's updater. Wait for the login
screen, then close Steam without logging in. Export and seal the stopped rootfs
with steam-desktop.py. Never run this in a personal instance.
"""
from pathlib import Path
import sys

sys.path.insert(0, '/usr/lib/arlinux')
import steam

root = Path('/opt/arlinux/steam-client')
if root.exists():
    raise SystemExit('Steam seed already exists; start with a new build instance')
steam.install(root, 'stable')
raise SystemExit(steam.launch(root, []))

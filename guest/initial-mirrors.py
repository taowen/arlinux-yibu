"""Select the initial Debian mirror once, without changing user repositories later."""
import os
from pathlib import Path
import re

marker = Path('/var/lib/arlinux/initial-mirror')
if not marker.exists():
    host = 'mirrors.tuna.tsinghua.edu.cn' if os.environ.get('ARLINUX_LANGUAGE') == 'zh' else 'deb.debian.org'
    pattern = re.compile(r'https?://(?:mirrors\.tuna\.tsinghua\.edu\.cn|deb\.debian\.org|security\.debian\.org)/(debian-security|debian)(?=/|\s|$)')
    sources = [Path('/etc/apt/sources.list')]
    sources.extend(Path('/etc/apt/sources.list.d').glob('*.sources'))
    sources.extend(Path('/etc/apt/sources.list.d').glob('*.list'))
    for source in sources:
        if source.is_file():
            original = source.read_text()
            selected = pattern.sub(lambda match: f'https://{host}/{match[1]}', original)
            if selected != original:
                source.write_text(selected)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(host + '\n')

#!/usr/bin/env python3
"""Seal a disposable device snapshot as the optional Yibu Steam desktop.

Use a NEW build-only instance. Install the client to /opt/arlinux/steam-client,
let Valve's updater reach its login screen, close it, and export the rootfs.
Keep the original native bootstrap ZIP from the build instance's download cache.
Never log in or install games in this instance. The Android repository handles
APK signing; this tool only produces its embedded distribution payload.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import posixpath
from pathlib import Path
import sys
import tarfile
import tempfile
import shutil
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('framework', type=Path)
parser.add_argument('base', type=Path)
parser.add_argument('snapshot', type=Path)
parser.add_argument('bootstrap', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
framework = args.framework.resolve()
sys.path.insert(0, str(framework/'tools'))
spec = importlib.util.spec_from_file_location('device_desktop', framework/'tools/device-desktop.py')
desktop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(desktop)

seed = 'opt/arlinux/steam-client/'
# Ship Valve's bootstrap and verified update archives, not its device-specific
# installed-file cache. Valve initializes that cache for the user's own kernel.
excluded = ('appcache/', 'config/', 'depotcache/', 'dumps/', 'logs/',
            'steamapps/', 'userdata/', 'compatibilitytools.d/', 'htmlcache/')
seen = set()
with tempfile.TemporaryDirectory(prefix='yibu-steam-') as directory:
    clean = Path(directory)/'rootfs.tar'
    with tarfile.open(args.snapshot) as source, tarfile.open(clean, 'w', format=tarfile.GNU_FORMAT) as target:
        spec = importlib.util.spec_from_file_location('steam', framework/'runtime/tools/steam.py')
        steam = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(steam)
        listing = source.extractfile('./'+seed+'package/steam_client_linuxarm64.manifest').read().decode()
        info = steam.manifest(listing)
        component = info['bins_linuxarm64_linuxarm64']
        if steam.digest(args.bootstrap) != component['sha2']:
            raise ValueError('Bootstrap does not match Valve SHA-256')
        with zipfile.ZipFile(args.bootstrap) as bootstrap:
            client_files = {entry.filename.rstrip('/') for entry in bootstrap.infolist()}
        archives = {}
        for component in info.values():
            if not isinstance(component, dict) or 'file' not in component:
                continue
            key = 'zipvz' if component.get('zipvz') else 'file'
            name = component[key]
            if '/' in name or name in ('.', '..'):
                raise ValueError('Unsafe Valve package filename')
            checksum = component['sha2vz' if key == 'zipvz' else 'sha2']
            archives['package/'+name] = checksum
        client_files.update(archives)
        client_files.add('package/steam_client_linuxarm64.manifest')
        if any(x.startswith('/') or '..' in x.split('/') for x in client_files):
            raise ValueError('Unsafe Valve installed-file manifest')
        for member in source:
            name = member.name.removeprefix('./')
            if name.startswith(seed):
                relative = name[len(seed):]
                if relative.rstrip('/') not in client_files:
                    continue
                if any(relative.rstrip('/') == x.rstrip('/') or relative.startswith(x) for x in excluded):
                    continue
                if relative in archives:
                    checksum = hashlib.sha256()
                    with source.extractfile(member) as data:
                        for block in iter(lambda: data.read(1024*1024), b''):
                            checksum.update(block)
                    if checksum.hexdigest() != archives[relative]:
                        raise ValueError('Valve package checksum mismatch: '+relative)
                if relative.startswith(('ssfn', '.')) or relative in ('registry.vdf', 'steam.pid'):
                    continue
                if member.issym():
                    destination = posixpath.normpath(posixpath.join(posixpath.dirname(relative), member.linkname))
                    if member.linkname.startswith('/') or destination.startswith('../'):
                        raise ValueError('Nonportable Steam seed link: ' + name)
                seen.add(relative)
            if name in ('usr/lib/arlinux/steam.py', 'usr/share/applications/arlinux-steam.desktop'):
                continue
            target.addfile(member, source.extractfile(member) if member.isfile() else None)
        for name, data in {
            'usr/lib/arlinux/steam.py': (framework/'runtime/tools/steam.py').read_bytes(),
            'usr/share/applications/arlinux-steam.desktop': b'''[Desktop Entry]
Type=Application
Name=Steam
Comment=Open the preinstalled Steam client
Comment[zh_CN]=\xe6\x89\x93\xe5\xbc\x80\xe9\xa2\x84\xe8\xa3\x85\xe7\x9a\x84 Steam \xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf
Exec=arlinux-steam --desktop
Icon=/usr/share/pixmaps/arlinux-steam.png
Terminal=true
Categories=Game;
StartupNotify=false
''',
        }.items():
            member = tarfile.TarInfo('./'+name)
            member.size, member.mode = len(data), 0o644
            target.addfile(member, io.BytesIO(data))
    required = {'steamrtarm64/steam', 'package/steam_client_linuxarm64.manifest',
                'steamrtarm64/steamwebhelper', *archives}
    if not required <= seen:
        raise ValueError('Incomplete updated Steam client: ' + ', '.join(sorted(required-seen)))
    desktop.seal(args.base, clean, args.output)
    renamed = args.output.with_suffix('.named.part')
    with zipfile.ZipFile(args.output) as source, zipfile.ZipFile(renamed, 'w') as target:
        for entry in source.infolist():
            if entry.filename == 'manifest.json':
                manifest = json.loads(source.read(entry))
                manifest['name'] = 'Yibu Steam'
                target.writestr('manifest.json', json.dumps(manifest, indent=2)+'\n')
            else:
                with source.open(entry) as src, target.open(entry.filename, 'w', force_zip64=True) as dst:
                    shutil.copyfileobj(src, dst, 1024*1024)
    desktop.verify(renamed)
    renamed.replace(args.output)
print('Account-free Yibu Steam desktop:', args.output)

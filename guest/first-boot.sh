#!/bin/sh
# Only device-local configuration belongs here. Packages are built into the ZIP.
set -eu
guest=/usr/lib/arlinux/guest
test -f /usr/share/arlinux/offline-desktop
test -x /usr/bin/arlinux-opencode
# Seed preferences once; subsequent boots never replace user configuration.
install_default() {
    if [ ! -e "$2" ] && [ ! -L "$2" ]; then install -Dm644 "$1" "$2"; fi
}
install_default "$guest/foot.ini" "$HOME/.config/foot/foot.ini"
install_default "$guest/gtk-settings.ini" "$HOME/.config/gtk-3.0/settings.ini"
install_default "$guest/gtk-settings.ini" "$HOME/.config/gtk-4.0/settings.ini"
install_default "$guest/Xresources" "$HOME/.Xresources"
python3 "$guest/initial-mirrors.py"
# Package triggers do not run when an offline rootfs is imported.
update-mime-database /usr/share/mime
if [ ! -s /etc/machine-id ]; then
    chmod u+w /etc/machine-id
    tr -d '-' < /proc/sys/kernel/random/uuid > /etc/machine-id
    chmod 444 /etc/machine-id
fi
install -Dm755 "$guest/install-codex.sh" /usr/local/bin/arlinux-install-codex
mkdir -p /etc/fonts/conf.d
cp "$guest/50-arlinux-wps-fonts.conf" /etc/fonts/conf.d/
mkdir -p /etc/pulse/client.conf.d /etc/alsa/conf.d
printf 'default-server = unix:%s/runtime/pulse-native\nautospawn = no\nenable-shm = no\n' \
    "$BIONICX_FILES" > /etc/pulse/client.conf.d/arlinux.conf
printf 'pcm.!default { type pulse }\nctl.!default { type pulse }\n' \
    > /etc/alsa/conf.d/99-arlinux-pulse.conf
/bin/sh "$guest/wps-shortcuts.sh"

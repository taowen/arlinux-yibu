#!/bin/sh
set -eu

root=${BIONICX_ROOTFS:?missing BIONICX_ROOTFS}
home=${HOME:?missing HOME}
guest=$root/usr/lib/arlinux/guest
config=$home/.config/opencode
agents=$config/AGENTS.md
plugin_dir=$config/plugin
environment_plugin=$plugin_dir/arlinux-environment.js
temporary=$config/.AGENTS.md.arlinux-new
begin='<!-- BEGIN ARLINUX MANAGED INSTRUCTIONS -->'
end='<!-- END ARLINUX MANAGED INSTRUCTIONS -->'

mkdir -p "$config" "$plugin_dir" "$root/usr/local/bin"
if [ -f "$agents" ]; then
    awk -v begin="$begin" -v end="$end" '
        $0 == begin { managed = 1; next }
        $0 == end { managed = 0; next }
        !managed { print }
    ' "$agents" > "$temporary"
else
    : > "$temporary"
fi

while [ -s "$temporary" ] && [ "$(tail -c 1 "$temporary" | wc -l)" -eq 0 ]; do
    printf '\n' >> "$temporary"
done
printf '%s\n' "$begin" >> "$temporary"
cat "$guest/opencode-AGENTS.md" >> "$temporary"
printf '%s\n' "$end" >> "$temporary"
mv "$temporary" "$agents"
chmod 600 "$agents"

# The first-use installer seeds config and the available free model together.
# Boot only maintains instructions/plugins and must not require network access.

# OpenCode's Electron host sets NO_AT_BRIDGE for Chromium itself. Use the
# supported shell.env hook so that commands run by the shell tool do not pass
# that Chromium-private setting to GTK applications.
cp "$guest/opencode-arlinux-environment.js" "$environment_plugin"
chmod 600 "$environment_plugin"

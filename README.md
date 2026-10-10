# yibu

yibu is a dual-pointer ARLinux desktop based on Debian and anhyprland.
Its dedicated layout has one main task and three persistent auxiliary slots.
Android and Linux applications share the same desktop.

## Interaction

The landscape adaptation keeps the main task beside three fixed slots. Click an
empty slot with either pointer to pin the main task. Click an occupied slot to
exchange it with the main task. Fingers move the pointers using the touchpads;
the sidebar does not intercept direct touches. The right-edge input-method handle
remains available: tap to toggle the keyboard, or hold for AI voice input. The
arrow moves the sidebar between the left and right edges. The top task strip
switches directly to running applications. Apps opens installed Android and Linux
applications; Tasks lists additional running tasks.

The complete sidebar and toolbar are rendered and hit-tested by anhyprland, not
an Android overlay. Apps opens a normal GTK Wayland app drawer built from standard
desktop entries, with separate Linux and Android sections, a filter and search.
Helper entries such as terminal servers and settings panels are not listed. The
host exports installed Android launch activities and their icons as desktop
entries; the existing `arlinux-app` endpoint opens their hosted windows.
The `x` on an auxiliary task removes it from that slot without closing the app.

Full screen in the top-right corner hides the task chrome and expands the main
task across the desktop. Back to Yibu restores the task slots and sidebar side;
neither operation closes applications. Both controls are operated with pointers.

Auxiliary tasks keep their main-task client size and are GPU-scaled, rather than
cropped or reflowed into narrow application layouts. Their content stays live.
For Wayland content dragging, hovering over a pinned task promotes that task;
the application still decides whether to accept the eventual drop.

The reference is [Smartisan OS One Step 3.0](https://www.bilibili.com/video/BV1VJ411U7uD/).
Its quick-launch icon strip and Android content-transfer behavior are not yet
fully reproduced. This is not currently a complete One Step replica.

Yibu is the built-in offline workspace in ARLinux 0.1.13 and later.
OpenCode is optional and is not bundled. Click its Apps icon or hold the AI
voice handle to download and install the pinned official desktop package.
First installation needs internet and may take several minutes. You can release
the handle while installation continues, then hold again once OpenCode opens.
Subsequent launches use the installed app without downloading it again.
The interaction is inspired by Smartisan OS One Step 3.0. This is an independent
implementation, not a Smartisan product or a port of proprietary Smartisan code.

Build with the public [ARLinux rootfs framework](https://github.com/taowen/arlinux-rootfs).
Place this checkout at `distributions/yibu` in that framework, then run:

```sh
./build.sh validate distributions/yibu
./build.sh build yibu
./build.sh verify out/yibu.zip
```

See the framework's distribution-authoring guide for device-based offline desktop
preparation. Package installation is performed on a real ARM64 device, not QEMU.

## Steam edition

The optional `arlinux-yibu-steam.apk` release contains ARLinux and an account-free
Yibu workspace with Valve's native ARM64 Steam client and its host dependencies.

- New users: install the APK, open ARLinux and start the built-in workspace.
- Existing users: in an ARLinux version supporting APK imports, choose **Import
  ZIP / APK** and select the downloaded APK. This creates a separate **Yibu Steam**
  instance; it does not install the APK or change existing workspaces. Older
  ARLinux versions can first install this same APK as an application update
  (retaining existing instances), then import it from inside ARLinux.

Open **Apps → Steam**. The launcher moves the bundled client into this instance's
user directory; Valve's updater then works normally. Internet access is required
for signing in, client updates, compatibility runtimes and games. No account,
login credentials, games or compatibility-runtime downloads are included. Steam
and games remain subject to their respective licenses; game compatibility varies.

To prepare the embedded payload, start with a NEW disposable device-build
instance of the offline Yibu desktop. Install Steam to `/opt/arlinux/steam-client`
by executing `tools/install-steam-seed.py` inside the instance. Wait for Valve's
updater to reach the login screen, and close it **without signing in**. Export the
stopped instance with emulated hardlinks materialized, then run:

```sh
python3 tools/steam-desktop.py /path/to/arlinux-rootfs \
  /path/to/yibu.zip /path/to/device-rootfs.tar out/yibu-steam.zip
```

This intermediate ZIP is embedded as `assets/default.zip` in the signed APK;
the downloadable release artifact is the APK only. The sealing tool excludes
home directories, account state, games, client caches, downloads and logs.

The host must include the `yibu` anhyprland layout. A normal upstream Hyprland
installation does not provide this layout. Cross-platform content dragging also
requires a hosted Android drag-and-drop bridge; window switching alone is not
content transfer.

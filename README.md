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

The host must include the `yibu` anhyprland layout. A normal upstream Hyprland
installation does not provide this layout. Cross-platform content dragging also
requires a hosted Android drag-and-drop bridge; window switching alone is not
content transfer.

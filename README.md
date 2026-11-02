# ARLinux shared desktop base

This Debian-based distribution is the shared Linux system for ARLinux's Yibu,
Classic and Sequoia desktop styles. The stable product identifier remains `yibu`.
The Android host owns desktop selection, style assets and the embedded compositor:
Yibu uses anhyprland; Classic and Sequoia use anlabwc.

The base supplies standard Linux applications, accessibility, input-method clients,
audio clients and X11/Wayland libraries. Sequoia uses Waybar and swaybg over standard
Wayland protocols; it does not add another compositor or another copy of the system.
Android provides its application/settings/tasks panel and hosted Android applications.

Build and release this distribution through the owning
[arlinux-rootfs build guide](https://github.com/taowen/arlinux-rootfs/blob/main/docs/BUILD.md).
Android packaging, desktop style definitions and device acceptance belong to the
[ARLinux build guide](https://github.com/taowen/arlinux/blob/main/docs/BUILD.md).

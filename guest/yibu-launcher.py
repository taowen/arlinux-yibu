#!/usr/bin/env python3
"""A regular Wayland application picker for Linux and hosted Android desktop entries."""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk


application = Gtk.Application(application_id="org.arlinux.yibu.Applications")

def activate(application):
    if application.get_windows():
        application.get_windows()[0].present()
        return
    window = Gtk.ApplicationWindow(application=application, title="Yibu applications")
    window.set_default_size(760, 580)
    window.connect("destroy", lambda _: application.quit())
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    box.set_border_width(16)
    window.add(box)
    search = Gtk.SearchEntry()
    search.set_placeholder_text("Search Android and Linux applications")
    box.pack_start(search, False, False, 0)
    scroller = Gtk.ScrolledWindow()
    box.pack_start(scroller, True, True, 0)
    rows = Gtk.ListBox()
    scroller.add(rows)
    for app in sorted(Gio.AppInfo.get_all(), key=lambda app: app.get_display_name().casefold()):
        if not app.should_show():
            continue
        row = Gtk.ListBoxRow()
        row.app = app
        content = Gtk.Box(spacing=12)
        content.set_border_width(10)
        icon = app.get_icon()
        if icon:
            content.pack_start(Gtk.Image.new_from_gicon(icon, Gtk.IconSize.DIALOG), False, False, 0)
        content.pack_start(Gtk.Label(label=app.get_display_name(), xalign=0), True, True, 0)
        row.add(content)
        rows.add(row)

    rows.set_filter_func(lambda row: search.get_text().casefold() in row.app.get_display_name().casefold())
    search.connect("search-changed", lambda _: rows.invalidate_filter())

    def launch(_, row):
        try:
            row.app.launch([], Gio.AppLaunchContext())
        except Exception as error:
            dialog = Gtk.MessageDialog(transient_for=window, modal=True,
                message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE, text=str(error))
            dialog.run()
            dialog.destroy()
            return
        window.destroy()

    rows.connect("row-activated", launch)
    window.show_all()

application.connect("activate", activate)
application.run([])

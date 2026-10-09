-- The host starts the compositor. This file only configures the yibu desktop.
hl.monitor({ output = '', mode = 'preferred', position = 'auto', scale = 1 })
hl.config({
    debug = { disable_logs = false },
    general = { layout = 'yibu', border_size = 0, gaps_in = 0, gaps_out = 0 },
    decoration = { rounding = 0, blur = { enabled = false }, shadow = { enabled = false } },
    animations = { enabled = false },
    cursor = { invisible = true },
    misc = {
        focus_on_activate = true,
        disable_hyprland_logo = true,
        disable_splash_rendering = true,
        disable_hyprland_guiutils_check = true,
        disable_watchdog_warning = true
    }
})
hl.bind('ALT + F4', hl.dsp.window.close())

from tkinter import Menu
import about
import settings_window
import export_modpacks
from theme_manager import get_theme_manager, LIGHT_THEMES, DARK_THEMES, SPECIAL_THEMES


def init_menubar(window):
    menubar = Menu(window)
    theme_manager = get_theme_manager()

    # === Saildeck menu ===
    saildeck_menu = Menu(menubar, tearoff=0)
    saildeck_menu.add_command(label="Open mods folder", command=window.open_mods_folder)
    saildeck_menu.add_command(label="Refresh mods list", command=window.refresh_mod_list)
    menubar.add_cascade(label="Saildeck", menu=saildeck_menu)

    # === View menu ===
    view_menu = Menu(menubar, tearoff=0)

    def set_theme_mode(mode):
        theme_manager.set_theme_mode(mode)
        _update_theme_menu_state()

    def _update_theme_menu_state():
        current_mode = theme_manager.get_theme_mode()
        # Update checkmarks by rebuilding menu
        _rebuild_view_menu()

    def _rebuild_view_menu():
        # Clear and rebuild view menu
        view_menu.delete(0, "end")

        current_mode = theme_manager.get_theme_mode()

        # Theme mode submenu
        theme_mode_menu = Menu(view_menu, tearoff=0)
        theme_mode_menu.add_radiobutton(
            label="Light",
            command=lambda: set_theme_mode("light"),
            variable=None
        )
        theme_mode_menu.add_radiobutton(
            label="Dark",
            command=lambda: set_theme_mode("dark"),
            variable=None
        )
        theme_mode_menu.add_radiobutton(
            label="System",
            command=lambda: set_theme_mode("system"),
            variable=None
        )

        # Add checkmarks manually
        for i, mode in enumerate(["light", "dark", "system"]):
            if mode == current_mode:
                theme_mode_menu.entryconfigure(i, label=f"{'Light' if mode == 'light' else 'Dark' if mode == 'dark' else 'System'} *")

        view_menu.add_cascade(label="Theme Mode", menu=theme_mode_menu)

        # Light theme selection submenu
        light_theme_menu = Menu(view_menu, tearoff=0)
        current_light = theme_manager.get_light_theme()

        for theme in LIGHT_THEMES:
            label = theme.capitalize()
            if theme == current_light:
                label += " *"
            light_theme_menu.add_command(
                label=label,
                command=lambda t=theme: _set_light_theme(t)
            )

        view_menu.add_cascade(label="Light Theme", menu=light_theme_menu)

        # Dark theme selection submenu
        dark_theme_menu = Menu(view_menu, tearoff=0)
        current_dark = theme_manager.get_dark_theme()

        for theme in DARK_THEMES:
            label = theme.capitalize()
            if theme == current_dark:
                label += " *"
            dark_theme_menu.add_command(
                label=label,
                command=lambda t=theme: _set_dark_theme(t)
            )

        view_menu.add_cascade(label="Dark Theme", menu=dark_theme_menu)

        # Separator before special themes
        view_menu.add_separator()

        # Special themes submenu
        special_theme_menu = Menu(view_menu, tearoff=0)
        current_special = theme_manager.get_special_theme()

        # Option to disable special themes
        none_label = "None (Standard)"
        if current_special is None:
            none_label += " *"
        special_theme_menu.add_command(
            label=none_label,
            command=lambda: _set_special_theme(None)
        )

        special_theme_menu.add_separator()

        # Add special theme options
        for theme_key, theme_data in SPECIAL_THEMES.items():
            label = theme_data["name"]
            if theme_key == current_special:
                label += " *"
            special_theme_menu.add_command(
                label=label,
                command=lambda t=theme_key: _set_special_theme(t)
            )

        view_menu.add_cascade(label="Special Themes", menu=special_theme_menu)

        # CRT options (only show when CRT theme is active)
        if current_special and current_special.startswith("crt_"):
            view_menu.add_separator()
            crt_menu = Menu(view_menu, tearoff=0)

            # Scanlines toggle
            scanlines_label = "Scanlines"
            if theme_manager.get_crt_scanlines_enabled():
                scanlines_label += " [ON]"
            else:
                scanlines_label += " [OFF]"
            crt_menu.add_command(
                label=scanlines_label,
                command=_toggle_scanlines
            )

            view_menu.add_cascade(label="CRT Effects", menu=crt_menu)

    def _set_light_theme(theme):
        theme_manager.set_light_theme(theme)
        _rebuild_view_menu()

    def _set_dark_theme(theme):
        theme_manager.set_dark_theme(theme)
        _rebuild_view_menu()

    def _set_special_theme(theme_key):
        theme_manager.set_special_theme(theme_key)
        _rebuild_view_menu()

    def _toggle_scanlines():
        current = theme_manager.get_crt_scanlines_enabled()
        theme_manager.set_crt_scanlines_enabled(not current)
        _rebuild_view_menu()

    # Build initial view menu
    _rebuild_view_menu()

    menubar.add_cascade(label="View", menu=view_menu)

    # === Option menu ===
    option_menu = Menu(menubar, tearoff=0)
    option_menu.add_command(label="Settings", command=lambda: settings_window.show_settings(window))
    option_menu.add_separator()
    option_menu.add_command(label="Export Modpack", command=lambda: export_modpacks.export_selected_modpack(window, window.status_var))
    option_menu.add_command(label="Import Modpack", command=lambda: export_modpacks.import_modpack(window))
    menubar.add_cascade(label="Option", menu=option_menu)

    # === About menu ===
    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label="Credits", command=lambda: about.show_about_window(window))
    menubar.add_cascade(label="About", menu=help_menu)

    window.config(menu=menubar)

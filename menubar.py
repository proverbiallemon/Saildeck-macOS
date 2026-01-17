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

    def _rebuild_view_menu():
        # Clear and rebuild view menu
        view_menu.delete(0, "end")

        current_mode = theme_manager.get_theme_mode()
        current_light = theme_manager.get_light_theme()
        current_dark = theme_manager.get_dark_theme()
        current_special = theme_manager.get_special_theme()

        # Light themes submenu - clicking switches to light mode
        light_theme_menu = Menu(view_menu, tearoff=0)
        for theme in LIGHT_THEMES:
            label = theme.capitalize()
            if current_mode == "light" and theme == current_light and not current_special:
                label += " ✓"
            light_theme_menu.add_command(
                label=label,
                command=lambda t=theme: _set_light_theme(t)
            )
        view_menu.add_cascade(label="Light Themes", menu=light_theme_menu)

        # Dark themes submenu - clicking switches to dark mode
        dark_theme_menu = Menu(view_menu, tearoff=0)
        for theme in DARK_THEMES:
            label = theme.capitalize()
            if current_mode == "dark" and theme == current_dark and not current_special:
                label += " ✓"
            dark_theme_menu.add_command(
                label=label,
                command=lambda t=theme: _set_dark_theme(t)
            )
        view_menu.add_cascade(label="Dark Themes", menu=dark_theme_menu)

        view_menu.add_separator()

        # Follow System Theme option
        system_label = "Follow System Theme"
        if current_mode == "system" and not current_special:
            system_label += " ✓"
        view_menu.add_command(
            label=system_label,
            command=_set_system_mode
        )

        view_menu.add_separator()

        # Special themes submenu
        special_theme_menu = Menu(view_menu, tearoff=0)

        # Option to disable special themes
        none_label = "None (Standard)"
        if current_special is None:
            none_label += " ✓"
        special_theme_menu.add_command(
            label=none_label,
            command=lambda: _set_special_theme(None)
        )

        special_theme_menu.add_separator()

        # Add special theme options
        for theme_key, theme_data in SPECIAL_THEMES.items():
            label = theme_data["name"]
            if theme_key == current_special:
                label += " ✓"
            special_theme_menu.add_command(
                label=label,
                command=lambda t=theme_key: _set_special_theme(t)
            )

        view_menu.add_cascade(label="Special Themes", menu=special_theme_menu)

    def _set_light_theme(theme):
        # Clear special theme and switch to light mode with selected theme
        theme_manager.set_special_theme(None)
        theme_manager.set_light_theme(theme)
        theme_manager.set_theme_mode("light")
        _rebuild_view_menu()

    def _set_dark_theme(theme):
        # Clear special theme and switch to dark mode with selected theme
        theme_manager.set_special_theme(None)
        theme_manager.set_dark_theme(theme)
        theme_manager.set_theme_mode("dark")
        _rebuild_view_menu()

    def _set_system_mode():
        # Clear special theme and follow system
        theme_manager.set_special_theme(None)
        theme_manager.set_theme_mode("system")
        _rebuild_view_menu()

    def _set_special_theme(theme_key):
        theme_manager.set_special_theme(theme_key)
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

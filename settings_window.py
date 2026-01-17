"""
Settings Window for Saildeck
Provides a tabbed interface for configuring application settings.
"""

import os
import sys
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from theme_manager import (
    get_theme_manager,
    get_platform_font,
    LIGHT_THEMES,
    DARK_THEMES,
    SPECIAL_THEMES,
    DEFAULT_SETTINGS,
)


def show_settings(parent):
    """Display the settings window."""
    theme_manager = get_theme_manager()
    settings = theme_manager.get_all_settings()
    font = get_platform_font()

    win = tb.Toplevel(parent)
    win.title("Settings")
    win.geometry("450x420")
    win.resizable(False, False)
    win.transient(parent)
    win.grab_set()

    # Set icon
    icon_path = os.path.join(os.path.dirname(__file__), "icon", "icon_question.ico")
    if os.path.exists(icon_path):
        try:
            win.iconbitmap(icon_path)
        except Exception:
            pass

    # Center on parent
    win.update_idletasks()
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height()
    win_w = win.winfo_width()
    win_h = win.winfo_height()
    pos_x = parent_x + (parent_w // 2) - (win_w // 2)
    pos_y = parent_y + (parent_h // 2) - (win_h // 2)
    win.geometry(f"+{pos_x}+{pos_y}")

    # Create notebook for tabs
    notebook = tb.Notebook(win, bootstyle="default")
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # ========== Appearance Tab ==========
    appearance_frame = tb.Frame(notebook, padding=15)
    notebook.add(appearance_frame, text="Appearance")

    current_mode = settings["appearance"]["theme_mode"]
    current_light = settings["appearance"]["light_theme"]
    current_dark = settings["appearance"]["dark_theme"]
    current_special = settings["appearance"].get("special_theme")

    # Determine which theme is currently active
    if current_special:
        active_theme = None  # Special theme is active
    elif current_mode == "light":
        active_theme = ("light", current_light)
    elif current_mode == "dark":
        active_theme = ("dark", current_dark)
    else:
        active_theme = ("system", None)

    # Variable to track selection
    theme_var = tb.StringVar()
    if active_theme == ("system", None):
        theme_var.set("system")
    elif active_theme and active_theme[0] == "light":
        theme_var.set(f"light_{active_theme[1]}")
    elif active_theme and active_theme[0] == "dark":
        theme_var.set(f"dark_{active_theme[1]}")
    else:
        theme_var.set("")

    # Light Themes
    tb.Label(
        appearance_frame,
        text="Light Themes",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    light_frame = tb.Frame(appearance_frame)
    light_frame.pack(fill="x", pady=(0, 10))

    for theme in LIGHT_THEMES:
        tb.Radiobutton(
            light_frame,
            text=theme.capitalize(),
            variable=theme_var,
            value=f"light_{theme}",
            bootstyle="toolbutton"
        ).pack(side="left", padx=(0, 5))

    # Dark Themes
    tb.Label(
        appearance_frame,
        text="Dark Themes",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(10, 5))

    dark_frame = tb.Frame(appearance_frame)
    dark_frame.pack(fill="x", pady=(0, 10))

    for theme in DARK_THEMES:
        tb.Radiobutton(
            dark_frame,
            text=theme.capitalize(),
            variable=theme_var,
            value=f"dark_{theme}",
            bootstyle="toolbutton"
        ).pack(side="left", padx=(0, 5))

    # Follow System Theme
    tb.Separator(appearance_frame, orient="horizontal").pack(fill="x", pady=15)

    tb.Radiobutton(
        appearance_frame,
        text="Follow System Theme (auto light/dark)",
        variable=theme_var,
        value="system",
        bootstyle="toolbutton"
    ).pack(anchor="w")

    # Preview note
    tb.Label(
        appearance_frame,
        text="Theme changes apply immediately.",
        font=(font, 9),
        bootstyle="secondary"
    ).pack(anchor="w", pady=(15, 0))

    def on_theme_change(*args):
        """Apply theme changes immediately."""
        value = theme_var.get()
        if not value:
            return

        # Clear special theme when selecting a standard theme
        theme_manager.set_special_theme(None)

        if value == "system":
            theme_manager.set_theme_mode("system")
        elif value.startswith("light_"):
            theme_name = value[6:]  # Remove "light_" prefix
            theme_manager.set_light_theme(theme_name)
            theme_manager.set_theme_mode("light")
        elif value.startswith("dark_"):
            theme_name = value[5:]  # Remove "dark_" prefix
            theme_manager.set_dark_theme(theme_name)
            theme_manager.set_theme_mode("dark")

    theme_var.trace_add("write", on_theme_change)

    # ========== Special Themes Tab ==========
    special_frame = tb.Frame(notebook, padding=15)
    notebook.add(special_frame, text="Special Themes")

    tb.Label(
        special_frame,
        text="Retro CRT Themes",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    tb.Label(
        special_frame,
        text="Apply a retro computer terminal aesthetic with\nphosphor-style colors.",
        font=(font, 9),
        bootstyle="secondary"
    ).pack(anchor="w", pady=(0, 15))

    current_special = settings["appearance"].get("special_theme")
    special_theme_var = tb.StringVar(value=current_special or "none")

    # Build special theme options
    special_options = [("none", "None (Use standard theme)")]
    for key, data in SPECIAL_THEMES.items():
        special_options.append((key, data["name"]))

    for value, label in special_options:
        tb.Radiobutton(
            special_frame,
            text=label,
            variable=special_theme_var,
            value=value,
            bootstyle="toolbutton"
        ).pack(anchor="w", pady=3)

    def on_special_theme_change(*args):
        """Apply special theme changes immediately."""
        value = special_theme_var.get()
        theme_key = None if value == "none" else value
        theme_manager.set_special_theme(theme_key)

    special_theme_var.trace_add("write", on_special_theme_change)

    # ========== Behavior Tab ==========
    behavior_frame = tb.Frame(notebook, padding=15)
    notebook.add(behavior_frame, text="Behavior")

    tb.Label(
        behavior_frame,
        text="Startup",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(0, 10))

    var_skip_update = tb.BooleanVar(value=settings["behavior"].get("skip_update", False))
    tb.Checkbutton(
        behavior_frame,
        text="Skip update check on startup",
        variable=var_skip_update,
        bootstyle="round-toggle"
    ).pack(anchor="w", pady=(0, 10))

    tb.Label(
        behavior_frame,
        text="Mods",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(10, 10))

    var_enable_altassets = tb.BooleanVar(value=settings["behavior"].get("enable_altassets", True))
    tb.Checkbutton(
        behavior_frame,
        text="Auto-enable AltAssets when mods are active",
        variable=var_enable_altassets,
        bootstyle="round-toggle"
    ).pack(anchor="w", pady=(0, 10))

    var_confirm_delete = tb.BooleanVar(value=settings["behavior"].get("confirm_delete", True))
    tb.Checkbutton(
        behavior_frame,
        text="Confirm before deleting mods",
        variable=var_confirm_delete,
        bootstyle="round-toggle"
    ).pack(anchor="w", pady=(0, 10))

    # ========== Advanced Tab ==========
    advanced_frame = tb.Frame(notebook, padding=15)
    notebook.add(advanced_frame, text="Advanced")

    # Game path display
    tb.Label(
        advanced_frame,
        text="Game Directory",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    # Get game_dir from parent if available
    game_dir = getattr(parent, 'game_dir', 'Not available')
    game_path_entry = tb.Entry(advanced_frame, width=50)
    game_path_entry.insert(0, str(game_dir))
    game_path_entry.configure(state="readonly")
    game_path_entry.pack(anchor="w", pady=(0, 15))

    # Mods directory display
    tb.Label(
        advanced_frame,
        text="Mods Directory",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    mods_dir = getattr(parent, 'mods_dir', 'Not available')
    mods_path_entry = tb.Entry(advanced_frame, width=50)
    mods_path_entry.insert(0, str(mods_dir))
    mods_path_entry.configure(state="readonly")
    mods_path_entry.pack(anchor="w", pady=(0, 15))

    # Reset settings button
    def reset_settings():
        """Reset all settings to defaults."""
        from tkinter import messagebox
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?\n\nThis cannot be undone."):
            # Reset to defaults
            for section, values in DEFAULT_SETTINGS.items():
                for key, value in values.items():
                    theme_manager.set_setting(section, key, value)

            # Update UI
            theme_var.set("system")
            special_theme_var.set("none")
            var_skip_update.set(False)
            var_enable_altassets.set(True)
            var_confirm_delete.set(True)

            # Apply theme
            theme_manager.set_special_theme(None)
            theme_manager.set_theme_mode("system")

    tb.Button(
        advanced_frame,
        text="Reset All Settings",
        command=reset_settings,
        bootstyle="danger-outline",
        width=20
    ).pack(anchor="w", pady=(20, 0))

    # ========== Bottom buttons ==========
    button_frame = tb.Frame(win)
    button_frame.pack(fill="x", padx=10, pady=(0, 10))

    def save_and_close():
        """Save behavior settings and close the window."""
        # Behavior settings need to be saved on close
        theme_manager.set_setting("behavior", "skip_update", var_skip_update.get())
        theme_manager.set_setting("behavior", "enable_altassets", var_enable_altassets.get())
        theme_manager.set_setting("behavior", "confirm_delete", var_confirm_delete.get())
        win.destroy()

    tb.Button(
        button_frame,
        text="Close",
        command=save_and_close,
        bootstyle="primary",
        width=10
    ).pack(side="right")

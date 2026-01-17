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

    # Theme Mode
    tb.Label(
        appearance_frame,
        text="Theme Mode",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    theme_mode_frame = tb.Frame(appearance_frame)
    theme_mode_frame.pack(fill="x", pady=(0, 15))

    theme_mode_var = tb.StringVar(value=settings["appearance"]["theme_mode"])

    for mode, label in [("light", "Light"), ("dark", "Dark"), ("system", "System")]:
        tb.Radiobutton(
            theme_mode_frame,
            text=label,
            variable=theme_mode_var,
            value=mode,
            bootstyle="toolbutton"
        ).pack(side="left", padx=(0, 10))

    # Light Theme Selection
    tb.Label(
        appearance_frame,
        text="Light Theme",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    light_theme_var = tb.StringVar(value=settings["appearance"]["light_theme"])
    light_theme_combo = tb.Combobox(
        appearance_frame,
        textvariable=light_theme_var,
        values=[t.capitalize() for t in LIGHT_THEMES],
        state="readonly",
        width=20
    )
    light_theme_combo.pack(anchor="w", pady=(0, 15))
    # Set display value capitalized
    light_theme_combo.set(settings["appearance"]["light_theme"].capitalize())

    # Dark Theme Selection
    tb.Label(
        appearance_frame,
        text="Dark Theme",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    dark_theme_var = tb.StringVar(value=settings["appearance"]["dark_theme"])
    dark_theme_combo = tb.Combobox(
        appearance_frame,
        textvariable=dark_theme_var,
        values=[t.capitalize() for t in DARK_THEMES],
        state="readonly",
        width=20
    )
    dark_theme_combo.pack(anchor="w", pady=(0, 15))
    # Set display value capitalized
    dark_theme_combo.set(settings["appearance"]["dark_theme"].capitalize())

    # Preview note
    tb.Label(
        appearance_frame,
        text="Theme changes apply immediately.",
        font=(font, 9),
        bootstyle="secondary"
    ).pack(anchor="w", pady=(10, 0))

    # ========== CRT Effects Tab ==========
    crt_frame = tb.Frame(notebook, padding=15)
    notebook.add(crt_frame, text="CRT Effects")

    tb.Label(
        crt_frame,
        text="Special Theme",
        font=(font, 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    current_special = settings["appearance"].get("special_theme")
    special_theme_var = tb.StringVar(value=current_special or "none")

    special_theme_frame = tb.Frame(crt_frame)
    special_theme_frame.pack(fill="x", pady=(0, 15))

    # Build special theme options
    special_options = [("none", "None (Standard)")]
    for key, data in SPECIAL_THEMES.items():
        special_options.append((key, data["name"]))

    for value, label in special_options:
        tb.Radiobutton(
            special_theme_frame,
            text=label,
            variable=special_theme_var,
            value=value,
            bootstyle="toolbutton"
        ).pack(side="left", padx=(0, 10))

    # CRT Options (scanlines, flicker)
    crt_options_frame = tb.LabelFrame(crt_frame, text="CRT Options", padding=10)
    crt_options_frame.pack(fill="x", pady=(10, 0))

    var_scanlines = tb.BooleanVar(value=settings["appearance"].get("crt_scanlines", True))
    tb.Checkbutton(
        crt_options_frame,
        text="Enable scanline overlay",
        variable=var_scanlines,
        bootstyle="round-toggle"
    ).pack(anchor="w", pady=(0, 10))

    # Scanline intensity slider
    intensity_frame = tb.Frame(crt_options_frame)
    intensity_frame.pack(fill="x", pady=(0, 10))

    tb.Label(
        intensity_frame,
        text="Scanline Intensity:",
        font=(font, 9)
    ).pack(side="left")

    intensity_value = settings["appearance"].get("crt_scanline_intensity", 0.3)
    var_intensity = tb.DoubleVar(value=intensity_value)

    intensity_slider = tb.Scale(
        intensity_frame,
        from_=0.1,
        to=0.8,
        variable=var_intensity,
        orient="horizontal",
        length=150
    )
    intensity_slider.pack(side="left", padx=(10, 10))

    intensity_label = tb.Label(intensity_frame, text=f"{intensity_value:.1f}", font=(font, 9))
    intensity_label.pack(side="left")

    def update_intensity_label(*args):
        intensity_label.configure(text=f"{var_intensity.get():.1f}")

    var_intensity.trace_add("write", update_intensity_label)

    var_flicker = tb.BooleanVar(value=settings["appearance"].get("crt_flicker", False))
    tb.Checkbutton(
        crt_options_frame,
        text="Enable flicker effect (subtle screen flicker)",
        variable=var_flicker,
        bootstyle="round-toggle"
    ).pack(anchor="w", pady=(0, 5))

    tb.Label(
        crt_options_frame,
        text="Note: CRT themes apply retro phosphor colors.\nScanline effects are limited due to tkinter constraints.",
        font=(font, 8),
        bootstyle="secondary"
    ).pack(anchor="w", pady=(10, 0))

    def on_special_theme_change(*args):
        """Apply special theme changes immediately."""
        value = special_theme_var.get()
        theme_key = None if value == "none" else value
        theme_manager.set_special_theme(theme_key)

    def on_crt_option_change(*args):
        """Apply CRT option changes."""
        theme_manager.set_crt_scanlines_enabled(var_scanlines.get())
        theme_manager.set_crt_scanline_intensity(var_intensity.get())
        theme_manager.set_crt_flicker_enabled(var_flicker.get())

    special_theme_var.trace_add("write", on_special_theme_change)
    var_scanlines.trace_add("write", on_crt_option_change)
    var_intensity.trace_add("write", on_crt_option_change)
    var_flicker.trace_add("write", on_crt_option_change)

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
            theme_mode_var.set("system")
            light_theme_combo.set("Litera")
            dark_theme_combo.set("Darkly")
            special_theme_var.set("none")
            var_scanlines.set(True)
            var_intensity.set(0.3)
            var_flicker.set(False)
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

    def apply_and_close():
        """Apply settings and close the window."""
        # Apply appearance settings
        new_mode = theme_mode_var.get()
        new_light = light_theme_combo.get().lower()
        new_dark = dark_theme_combo.get().lower()

        theme_manager.set_setting("appearance", "theme_mode", new_mode)
        theme_manager.set_setting("appearance", "light_theme", new_light)
        theme_manager.set_setting("appearance", "dark_theme", new_dark)

        # Apply behavior settings
        theme_manager.set_setting("behavior", "skip_update", var_skip_update.get())
        theme_manager.set_setting("behavior", "enable_altassets", var_enable_altassets.get())
        theme_manager.set_setting("behavior", "confirm_delete", var_confirm_delete.get())

        # Apply theme if mode changed
        theme_manager.set_theme_mode(new_mode)

        win.destroy()

    def on_theme_change(*args):
        """Apply theme changes immediately for preview and save."""
        new_mode = theme_mode_var.get()
        new_light = light_theme_combo.get().lower()
        new_dark = dark_theme_combo.get().lower()

        # Update and save all appearance settings using public API
        theme_manager.set_setting("appearance", "light_theme", new_light)
        theme_manager.set_setting("appearance", "dark_theme", new_dark)
        theme_manager.set_theme_mode(new_mode)

    # Bind changes to immediate preview
    theme_mode_var.trace_add("write", on_theme_change)
    light_theme_combo.bind("<<ComboboxSelected>>", on_theme_change)
    dark_theme_combo.bind("<<ComboboxSelected>>", on_theme_change)

    tb.Button(
        button_frame,
        text="Close",
        command=apply_and_close,
        bootstyle="primary",
        width=10
    ).pack(side="right")

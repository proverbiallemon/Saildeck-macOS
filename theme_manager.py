"""
Theme Manager for Saildeck
Central module for theme management, system detection, and runtime switching.
"""

import sys
import os
import json
import platform

try:
    import darkdetect
except ImportError:
    darkdetect = None

# Theme pairs: light -> dark mapping
THEME_PAIRS = {
    "litera": "darkly",
    "flatly": "superhero",
    "cosmo": "cyborg",
    "minty": "solar",
}

LIGHT_THEMES = list(THEME_PAIRS.keys())
DARK_THEMES = list(THEME_PAIRS.values())

# Special themes - these are actual ttkbootstrap theme definitions
# Format follows ttkbootstrap's theme structure
SPECIAL_THEMES = {
    "crt_green": {
        "name": "CRT Green",
        "type": "dark",
        "colors": {
            "primary": "#004D00",      # Dark green for button backgrounds
            "secondary": "#0A1F0A",
            "success": "#003300",      # Darker green so text is visible
            "info": "#004D00",
            "warning": "#004D00",
            "danger": "#660000",       # Dark red
            "light": "#00FF41",
            "dark": "#0D0208",
            "bg": "#0D0208",
            "fg": "#00FF41",
            "selectbg": "#003300",
            "selectfg": "#00FF41",
            "border": "#003300",
            "inputfg": "#00FF41",
            "inputbg": "#0A1F0A",
            "active": "#002200",
        }
    },
    "crt_amber": {
        "name": "CRT Amber",
        "type": "dark",
        "colors": {
            "primary": "#4D3000",      # Dark amber for button backgrounds
            "secondary": "#1A0F00",
            "success": "#3D2600",      # Darker amber so text is visible
            "info": "#4D3000",
            "warning": "#4D3000",
            "danger": "#660000",       # Dark red
            "light": "#FFB000",
            "dark": "#0D0800",
            "bg": "#0D0800",
            "fg": "#FFB000",
            "selectbg": "#3D2600",
            "selectfg": "#FFB000",
            "border": "#332200",
            "inputfg": "#FFB000",
            "inputbg": "#1A0F00",
            "active": "#261800",
        }
    },
}

DEFAULT_SETTINGS = {
    "appearance": {
        "theme_mode": "system",  # "light", "dark", or "system"
        "light_theme": "litera",
        "dark_theme": "darkly",
        "special_theme": None,  # None or key from SPECIAL_THEMES
        "crt_scanlines": True,
        "crt_scanline_intensity": 0.3,  # 0.0 to 1.0
    },
    "behavior": {
        "skip_update": False,
        "enable_altassets": True,
        "confirm_delete": True,
    }
}


def get_settings_path():
    """Get the path to the settings file."""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "saildeck.data")


def load_settings():
    """Load settings from file, merging with defaults."""
    path = get_settings_path()
    settings = _deep_copy(DEFAULT_SETTINGS)

    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                saved = json.load(f)
            # Migrate old flat settings to new structure
            settings = _migrate_settings(saved, settings)
        except Exception as e:
            print(f"[ThemeManager] Warning: Could not load settings: {e}")

    return settings


def _deep_copy(obj):
    """Deep copy a nested dict structure."""
    if isinstance(obj, dict):
        return {k: _deep_copy(v) for k, v in obj.items()}
    return obj


def _migrate_settings(saved, defaults):
    """Migrate old flat settings to new nested structure."""
    result = _deep_copy(defaults)

    # Handle old flat format
    if "skip_update" in saved and "behavior" not in saved:
        result["behavior"]["skip_update"] = saved.get("skip_update", False)
        result["behavior"]["enable_altassets"] = saved.get("enable_altassets", True)
    # Handle new nested format
    elif "behavior" in saved:
        for key in result["behavior"]:
            if key in saved["behavior"]:
                result["behavior"][key] = saved["behavior"][key]

    if "appearance" in saved:
        for key in result["appearance"]:
            if key in saved["appearance"]:
                value = saved["appearance"][key]
                # Validate theme names to prevent invalid themes from config
                if key == "light_theme" and value not in LIGHT_THEMES:
                    continue
                if key == "dark_theme" and value not in DARK_THEMES:
                    continue
                if key == "theme_mode" and value not in ("light", "dark", "system"):
                    continue
                if key == "special_theme" and value is not None and value not in SPECIAL_THEMES:
                    continue
                if key == "crt_scanline_intensity":
                    try:
                        value = float(value)
                        if not 0.0 <= value <= 1.0:
                            continue
                    except (ValueError, TypeError):
                        continue
                result["appearance"][key] = value

    return result


def save_settings(settings):
    """Save settings to file."""
    path = get_settings_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def get_system_theme():
    """Detect the current system theme (light/dark)."""
    if darkdetect is not None:
        try:
            theme = darkdetect.theme()
            if theme:
                return theme.lower()  # "light" or "dark"
        except Exception:
            pass
    # Default to dark if detection fails
    return "dark"


def get_platform_font():
    """Get the appropriate system font for the current platform."""
    system = platform.system()
    if system == "Darwin":  # macOS
        return "SF Pro Text"
    elif system == "Windows":
        return "Segoe UI"
    else:  # Linux and others
        return "DejaVu Sans"  # More universally available than Ubuntu font


class ThemeManager:
    """
    Centralized theme manager for the application.
    Handles theme switching, persistence, and notifications.
    """

    def __init__(self, root=None):
        self._root = root
        self._style = None
        self._callbacks = []
        self._settings = load_settings()
        self._current_theme = None

    def set_root(self, root):
        """Set the root window and initialize theming."""
        self._root = root
        self._apply_initial_theme()

    def _apply_initial_theme(self):
        """Apply the initial theme based on settings."""
        if self._root is None:
            return

        import ttkbootstrap as tb
        self._style = tb.Style()

        # Register custom CRT themes with ttkbootstrap
        self._register_special_themes()

        theme_name = self.get_effective_theme()
        self._apply_theme(theme_name)

    def _register_special_themes(self):
        """Register special themes (CRT, etc.) with ttkbootstrap."""
        if self._style is None:
            return

        from ttkbootstrap.style import ThemeDefinition

        for theme_key, theme_data in SPECIAL_THEMES.items():
            try:
                # Check if theme already registered
                if theme_key not in self._style.theme_names():
                    theme_def = ThemeDefinition(
                        name=theme_key,
                        themetype=theme_data["type"],
                        colors=theme_data["colors"]
                    )
                    self._style.register_theme(theme_def)
            except Exception as e:
                print(f"[ThemeManager] Failed to register theme '{theme_key}': {e}")

    def get_effective_theme(self):
        """Get the theme name that should currently be applied."""
        appearance = self._settings.get("appearance", DEFAULT_SETTINGS["appearance"])

        # Check for special theme first - return the special theme name directly
        # since we register them as actual ttkbootstrap themes
        special_theme = appearance.get("special_theme")
        if special_theme and special_theme in SPECIAL_THEMES:
            return special_theme

        mode = appearance.get("theme_mode", "system")
        light_theme = appearance.get("light_theme", "litera")
        dark_theme = appearance.get("dark_theme", "darkly")

        if mode == "light":
            return light_theme
        elif mode == "dark":
            return dark_theme
        else:  # system
            system_theme = get_system_theme()
            return light_theme if system_theme == "light" else dark_theme

    def _apply_theme(self, theme_name):
        """Apply a specific theme."""
        if self._style is None:
            return

        try:
            # Ensure special themes are registered before use
            if theme_name in SPECIAL_THEMES and theme_name not in self._style.theme_names():
                self._register_special_themes()

            self._style.theme_use(theme_name)
            self._current_theme = theme_name

            # Configure common styles
            font = get_platform_font()

            # Use monospace font for CRT themes
            if theme_name in SPECIAL_THEMES:
                crt_font = "SF Mono" if platform.system() == "Darwin" else "Consolas"
                self._style.configure("TButton", font=(crt_font, 10))
                self._style.configure("Tiny.TButton", font=(crt_font, 8))
            else:
                self._style.configure("TButton", font=(font, 10))
                self._style.configure("Tiny.TButton", font=(font, 8))

            self._style.configure("Treeview", rowheight=28)

            if self._root:
                self._root.update_idletasks()

            # Notify listeners
            self._notify_callbacks()
        except Exception as e:
            print(f"[ThemeManager] Error applying theme '{theme_name}': {e}")

    def _apply_special_theme_styles(self, special_theme_key):
        """Apply custom styles for special themes like CRT."""
        if special_theme_key not in SPECIAL_THEMES:
            return

        theme_data = SPECIAL_THEMES[special_theme_key]
        colors = theme_data["colors"]
        font = get_platform_font()

        # Use monospace font for CRT themes
        crt_font = "Courier" if platform.system() == "Darwin" else "Consolas"

        # Configure widget styles with CRT colors
        self._style.configure("TFrame", background=colors["bg"])
        self._style.configure("TLabel", background=colors["bg"], foreground=colors["fg"])
        self._style.configure("TButton",
                              background=colors["secondary_bg"],
                              foreground=colors["fg"],
                              font=(crt_font, 10))
        self._style.configure("Tiny.TButton", font=(crt_font, 8))

        # Treeview styling
        self._style.configure("Treeview",
                              background=colors["bg"],
                              foreground=colors["fg"],
                              fieldbackground=colors["bg"],
                              rowheight=28)
        self._style.map("Treeview",
                        background=[("selected", colors["secondary_bg"])],
                        foreground=[("selected", colors["highlight"])])

        # Entry and Combobox
        self._style.configure("TEntry",
                              fieldbackground=colors["secondary_bg"],
                              foreground=colors["fg"])
        self._style.configure("TCombobox",
                              fieldbackground=colors["secondary_bg"],
                              foreground=colors["fg"])

        # Notebook tabs
        self._style.configure("TNotebook", background=colors["bg"])
        self._style.configure("TNotebook.Tab",
                              background=colors["secondary_bg"],
                              foreground=colors["fg"])

        # Checkbutton
        self._style.configure("TCheckbutton",
                              background=colors["bg"],
                              foreground=colors["fg"])

        # Configure root window background
        if self._root:
            try:
                self._root.configure(bg=colors["bg"])
            except Exception:
                pass

    def set_theme_mode(self, mode):
        """Set the theme mode ('light', 'dark', or 'system')."""
        if mode not in ("light", "dark", "system"):
            return

        self._settings["appearance"]["theme_mode"] = mode
        save_settings(self._settings)

        theme_name = self.get_effective_theme()
        self._apply_theme(theme_name)

    def set_light_theme(self, theme_name):
        """Set the light theme variant."""
        if theme_name not in LIGHT_THEMES:
            return

        self._settings["appearance"]["light_theme"] = theme_name
        save_settings(self._settings)

        # Re-apply if currently in light mode
        if self.is_light_mode():
            self._apply_theme(theme_name)

    def set_dark_theme(self, theme_name):
        """Set the dark theme variant."""
        if theme_name not in DARK_THEMES:
            return

        self._settings["appearance"]["dark_theme"] = theme_name
        save_settings(self._settings)

        # Re-apply if currently in dark mode
        if not self.is_light_mode():
            self._apply_theme(theme_name)

    def is_light_mode(self):
        """Check if we should be showing a light theme based on mode setting."""
        mode = self.get_theme_mode()
        if mode == "light":
            return True
        elif mode == "dark":
            return False
        else:  # system
            return get_system_theme() == "light"

    def get_theme_mode(self):
        """Get the current theme mode setting."""
        return self._settings.get("appearance", {}).get("theme_mode", "system")

    def get_light_theme(self):
        """Get the current light theme setting."""
        return self._settings.get("appearance", {}).get("light_theme", "litera")

    def get_dark_theme(self):
        """Get the current dark theme setting."""
        return self._settings.get("appearance", {}).get("dark_theme", "darkly")

    def get_current_theme(self):
        """Get the name of the currently applied theme."""
        return self._current_theme

    def get_colors(self):
        """
        Get theme-aware colors for custom widgets.
        Returns a dict with common color keys.
        """
        # Check for special theme first
        special_theme = self.get_special_theme()
        if special_theme and special_theme in SPECIAL_THEMES:
            theme_colors = SPECIAL_THEMES[special_theme]["colors"]
            # Map ttkbootstrap color keys to our expected keys
            return {
                "bg": theme_colors["bg"],
                "fg": theme_colors["fg"],
                "secondary_bg": theme_colors["secondary"],
                "accent": theme_colors["primary"],
                "link": theme_colors["info"],
                "muted": theme_colors["warning"],
                "border": theme_colors["border"],
                "tooltip_bg": theme_colors["inputbg"],
                "tooltip_fg": theme_colors["inputfg"],
            }

        is_light = self.is_light_mode()

        if is_light:
            return {
                "bg": "#ffffff",
                "fg": "#212529",
                "secondary_bg": "#f8f9fa",
                "accent": "#0d6efd",
                "link": "#0d6efd",
                "muted": "#6c757d",
                "border": "#dee2e6",
                "tooltip_bg": "#f8f9fa",
                "tooltip_fg": "#212529",
            }
        else:
            return {
                "bg": "#222222",
                "fg": "#ffffff",
                "secondary_bg": "#2b2b2b",
                "accent": "#375a7f",
                "link": "#4da6ff",
                "muted": "#888888",
                "border": "#444444",
                "tooltip_bg": "#2b2b2b",
                "tooltip_fg": "#ffffff",
            }

    def get_special_theme(self):
        """Get the current special theme key (or None)."""
        return self._settings.get("appearance", {}).get("special_theme")

    def set_special_theme(self, theme_key):
        """Set or clear the special theme."""
        if theme_key is not None and theme_key not in SPECIAL_THEMES:
            return

        self._settings["appearance"]["special_theme"] = theme_key
        save_settings(self._settings)

        # Re-apply theme to activate/deactivate special styling
        theme_name = self.get_effective_theme()
        self._apply_theme(theme_name)

    def get_crt_scanlines_enabled(self):
        """Check if CRT scanlines are enabled."""
        return self._settings.get("appearance", {}).get("crt_scanlines", True)

    def set_crt_scanlines_enabled(self, enabled):
        """Enable or disable CRT scanlines."""
        self._settings["appearance"]["crt_scanlines"] = bool(enabled)
        save_settings(self._settings)
        self._notify_callbacks()

    def get_crt_scanline_intensity(self):
        """Get the CRT scanline intensity (0.0 to 1.0)."""
        return self._settings.get("appearance", {}).get("crt_scanline_intensity", 0.3)

    def set_crt_scanline_intensity(self, intensity):
        """Set the CRT scanline intensity (0.0 to 1.0)."""
        intensity = max(0.0, min(1.0, float(intensity)))
        self._settings["appearance"]["crt_scanline_intensity"] = intensity
        save_settings(self._settings)
        self._notify_callbacks()

    def is_special_theme_active(self):
        """Check if a special theme is currently active."""
        special_theme = self.get_special_theme()
        return special_theme is not None and special_theme in SPECIAL_THEMES

    def get_setting(self, section, key, default=None):
        """Get a specific setting value."""
        return self._settings.get(section, {}).get(key, default)

    def set_setting(self, section, key, value):
        """Set a specific setting value."""
        if section not in self._settings:
            self._settings[section] = {}
        self._settings[section][key] = value
        save_settings(self._settings)

    def get_all_settings(self):
        """Get all settings."""
        return _deep_copy(self._settings)

    def register_callback(self, callback):
        """Register a callback to be called when theme changes."""
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unregister_callback(self, callback):
        """Unregister a theme change callback."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _notify_callbacks(self):
        """Notify all registered callbacks of theme change."""
        for callback in self._callbacks:
            try:
                callback()
            except Exception as e:
                print(f"[ThemeManager] Callback error: {e}")

    def refresh_from_system(self):
        """Refresh theme if in system mode (call when system theme changes)."""
        if self.get_theme_mode() == "system":
            theme_name = self.get_effective_theme()
            if theme_name != self._current_theme:
                self._apply_theme(theme_name)


# Global theme manager instance
_theme_manager = None


def get_theme_manager():
    """Get the global ThemeManager instance."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager


def init_theme_manager(root):
    """Initialize the global theme manager with the root window."""
    manager = get_theme_manager()
    manager.set_root(root)
    return manager

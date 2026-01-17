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

DEFAULT_SETTINGS = {
    "appearance": {
        "theme_mode": "system",  # "light", "dark", or "system"
        "light_theme": "litera",
        "dark_theme": "darkly",
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
        except Exception:
            pass

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
                result["appearance"][key] = saved["appearance"][key]

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
        return "Ubuntu"


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

        theme_name = self.get_effective_theme()
        self._apply_theme(theme_name)

    def get_effective_theme(self):
        """Get the theme name that should currently be applied."""
        appearance = self._settings.get("appearance", DEFAULT_SETTINGS["appearance"])
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
            self._style.theme_use(theme_name)
            self._current_theme = theme_name

            # Configure common styles
            font = get_platform_font()
            self._style.configure("TButton", font=(font, 10))
            self._style.configure("Treeview", rowheight=28)
            self._style.configure("Tiny.TButton", font=(font, 8))

            if self._root:
                self._root.update_idletasks()

            # Notify listeners
            self._notify_callbacks()
        except Exception as e:
            print(f"[ThemeManager] Error applying theme '{theme_name}': {e}")

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

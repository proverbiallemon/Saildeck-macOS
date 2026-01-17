"""
CRT Effects for Saildeck
Provides CRT-style visual effects for the retro theme.

Note: True scanline overlay effects require transparency support which is
limited in tkinter. The primary CRT effect is achieved through the color
scheme (green/amber phosphor colors on dark background).
"""

import tkinter as tk


class ScanlineOverlay:
    """
    CRT Scanline effect manager.

    Due to tkinter limitations with transparency, the scanline effect is
    primarily aesthetic through the color scheme. The overlay functionality
    is provided for potential future platform-specific implementations.
    """

    def __init__(self, parent, intensity=0.3, line_spacing=2):
        """
        Initialize the scanline effect manager.

        Args:
            parent: The parent window
            intensity: Visual intensity (0.0 to 1.0)
            line_spacing: Pixels between effect lines
        """
        self._parent = parent
        self._intensity = intensity
        self._line_spacing = line_spacing
        self._enabled = False
        self._flicker_job = None
        self._flicker_state = True

    def enable(self):
        """Enable the CRT effect."""
        self._enabled = True

    def disable(self):
        """Disable the CRT effect."""
        self._enabled = False
        self.stop_flicker()

    def set_intensity(self, intensity):
        """Set the effect intensity."""
        self._intensity = max(0.0, min(1.0, intensity))

    def start_flicker(self, interval_ms=100):
        """Start a subtle flicker effect (color variation)."""
        if not self._enabled:
            return

        def flicker():
            if not self._enabled:
                return
            self._flicker_state = not self._flicker_state
            self._flicker_job = self._parent.after(interval_ms, flicker)

        # Cancel any existing flicker
        self.stop_flicker()
        flicker()

    def stop_flicker(self):
        """Stop the flicker effect."""
        if self._flicker_job:
            try:
                self._parent.after_cancel(self._flicker_job)
            except Exception:
                pass
            self._flicker_job = None

    @property
    def enabled(self):
        """Check if effect is enabled."""
        return self._enabled


class CRTFrame(tk.Frame):
    """
    A frame with built-in CRT styling.
    Use this as a container for CRT-styled content.
    """

    def __init__(self, parent, colors=None, **kwargs):
        """
        Initialize CRT-styled frame.

        Args:
            parent: Parent widget
            colors: Dict with 'bg', 'fg' keys for CRT colors
            **kwargs: Additional frame options
        """
        if colors is None:
            colors = {
                "bg": "#0D0208",
                "fg": "#00FF41"
            }

        super().__init__(parent, bg=colors["bg"], **kwargs)
        self._colors = colors

    def get_colors(self):
        """Get the CRT color scheme."""
        return self._colors.copy()


def apply_crt_text_glow(widget, glow_color="#00FF41"):
    """
    Apply CRT-style coloring to text widgets.

    Args:
        widget: The widget to style
        glow_color: The phosphor glow color
    """
    try:
        if hasattr(widget, 'configure'):
            widget.configure(foreground=glow_color)
            if hasattr(widget, 'activeforeground'):
                widget.configure(activeforeground=glow_color)
    except tk.TclError:
        pass  # Widget doesn't support these options


def get_crt_font():
    """Get the appropriate monospace font for CRT styling."""
    import platform
    system = platform.system()

    if system == "Darwin":
        return ("SF Mono", 10)
    elif system == "Windows":
        return ("Consolas", 10)
    else:
        return ("DejaVu Sans Mono", 10)

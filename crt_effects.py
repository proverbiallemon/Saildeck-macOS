"""
CRT Effects for Saildeck
Provides scanline overlay and other retro CRT visual effects.
"""

import tkinter as tk
import platform


class ScanlineOverlay:
    """
    Creates a scanline effect overlay using a transparent Toplevel window.
    Works on macOS by using transparent window attributes.
    """

    def __init__(self, parent, intensity=0.3, line_spacing=2):
        """
        Initialize the scanline overlay.

        Args:
            parent: The parent window to overlay
            intensity: Opacity of scanlines (0.0 to 1.0)
            line_spacing: Pixels between scanlines
        """
        self._parent = parent
        self._intensity = intensity
        self._line_spacing = line_spacing
        self._overlay = None
        self._canvas = None
        self._enabled = False
        self._flicker_job = None
        self._flicker_state = True
        self._update_job = None

    def enable(self):
        """Enable the scanline overlay."""
        if self._enabled:
            return

        self._enabled = True
        self._create_overlay()

        # Bind to parent window events
        self._parent.bind("<Configure>", self._on_parent_configure, add="+")
        self._parent.bind("<Map>", self._on_parent_map, add="+")
        self._parent.bind("<Unmap>", self._on_parent_unmap, add="+")

    def disable(self):
        """Disable and remove the scanline overlay."""
        self._enabled = False
        self.stop_flicker()

        if self._update_job:
            try:
                self._parent.after_cancel(self._update_job)
            except Exception:
                pass
            self._update_job = None

        if self._overlay:
            try:
                self._overlay.destroy()
            except Exception:
                pass
            self._overlay = None
            self._canvas = None

    def _create_overlay(self):
        """Create the transparent overlay window."""
        if self._overlay:
            self._overlay.destroy()

        # Create a Toplevel window for the overlay
        self._overlay = tk.Toplevel(self._parent)
        self._overlay.title("")
        self._overlay.overrideredirect(True)  # No window decorations

        # Make it transparent and click-through
        system = platform.system()
        if system == "Darwin":  # macOS
            # Make window transparent
            self._overlay.attributes("-transparent", True)
            # Keep it on top of parent
            self._overlay.attributes("-topmost", True)
            # Set the window background to a transparent color
            self._overlay.config(bg='systemTransparent')
        elif system == "Windows":
            # Windows transparency
            self._overlay.attributes("-transparentcolor", "black")
            self._overlay.attributes("-topmost", True)
            self._overlay.config(bg='black')
        else:  # Linux
            # Linux - may not work on all window managers
            self._overlay.attributes("-alpha", 0.5)
            self._overlay.attributes("-topmost", True)

        # Create canvas for drawing scanlines
        self._canvas = tk.Canvas(
            self._overlay,
            highlightthickness=0,
            bg='systemTransparent' if system == "Darwin" else 'black'
        )
        self._canvas.pack(fill="both", expand=True)

        # Position overlay on top of parent
        self._update_position()
        self._draw_scanlines()

        # Make overlay ignore mouse events (click-through)
        if system == "Darwin":
            self._overlay.attributes("-alpha", self._intensity)
            # Ignore mouse events
            try:
                self._overlay.wm_attributes("-transparent", True)
            except Exception:
                pass

    def _update_position(self):
        """Update overlay position to match parent window."""
        if not self._overlay or not self._enabled:
            return

        try:
            # Get parent window geometry
            x = self._parent.winfo_rootx()
            y = self._parent.winfo_rooty()
            width = self._parent.winfo_width()
            height = self._parent.winfo_height()

            # Position overlay exactly over parent
            self._overlay.geometry(f"{width}x{height}+{x}+{y}")

            # Redraw scanlines if size changed
            self._draw_scanlines()
        except Exception:
            pass

    def _draw_scanlines(self):
        """Draw the scanline pattern."""
        if not self._canvas or not self._enabled:
            return

        self._canvas.delete("scanline")

        try:
            width = self._canvas.winfo_width()
            height = self._canvas.winfo_height()
        except Exception:
            return

        if width <= 1 or height <= 1:
            # Canvas not ready yet, retry later
            self._update_job = self._parent.after(100, self._draw_scanlines)
            return

        # Draw horizontal scanlines
        # Use a semi-transparent dark color
        line_color = "#000000"

        y = 0
        while y < height:
            self._canvas.create_line(
                0, y, width, y,
                fill=line_color,
                width=1,
                tags="scanline"
            )
            y += self._line_spacing

    def _on_parent_configure(self, event=None):
        """Handle parent window resize/move."""
        if self._enabled and self._overlay:
            # Delay update to avoid too many calls during resize
            if self._update_job:
                try:
                    self._parent.after_cancel(self._update_job)
                except Exception:
                    pass
            self._update_job = self._parent.after(50, self._update_position)

    def _on_parent_map(self, event=None):
        """Handle parent window being shown."""
        if self._enabled and self._overlay:
            try:
                self._overlay.deiconify()
                self._update_position()
            except Exception:
                pass

    def _on_parent_unmap(self, event=None):
        """Handle parent window being hidden."""
        if self._overlay:
            try:
                self._overlay.withdraw()
            except Exception:
                pass

    def set_intensity(self, intensity):
        """Set the scanline intensity."""
        self._intensity = max(0.0, min(1.0, intensity))
        if self._enabled and self._overlay:
            try:
                self._overlay.attributes("-alpha", self._intensity)
            except Exception:
                pass

    def start_flicker(self, interval_ms=100):
        """Start a subtle flicker effect."""
        if not self._enabled:
            return

        def flicker():
            if not self._enabled or not self._overlay:
                return

            self._flicker_state = not self._flicker_state

            try:
                if self._flicker_state:
                    self._overlay.attributes("-alpha", self._intensity)
                else:
                    self._overlay.attributes("-alpha", self._intensity * 0.7)
            except Exception:
                pass

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

        # Reset to normal intensity
        if self._enabled and self._overlay:
            try:
                self._overlay.attributes("-alpha", self._intensity)
            except Exception:
                pass

    @property
    def enabled(self):
        """Check if overlay is enabled."""
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
    system = platform.system()

    if system == "Darwin":
        return ("SF Mono", 10)
    elif system == "Windows":
        return ("Consolas", 10)
    else:
        return ("DejaVu Sans Mono", 10)

"""
Platform abstraction module for Saildeck.

Provides platform-specific handlers for Windows and macOS.
"""
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import PlatformHandler

# Cached handler instance
_handler_instance: "PlatformHandler | None" = None


def get_platform_handler() -> "PlatformHandler":
    """
    Get the appropriate platform handler for the current OS.

    Returns:
        PlatformHandler instance for the current platform.

    Raises:
        RuntimeError: If the current platform is not supported.
    """
    global _handler_instance

    if _handler_instance is not None:
        return _handler_instance

    if sys.platform == "darwin":
        from .macos import MacOSHandler
        _handler_instance = MacOSHandler()
    elif sys.platform == "win32":
        from .windows import WindowsHandler
        _handler_instance = WindowsHandler()
    else:
        raise RuntimeError(
            f"Unsupported platform: {sys.platform}. "
            "Saildeck currently supports Windows and macOS."
        )

    return _handler_instance


def is_macos() -> bool:
    """Check if running on macOS."""
    return sys.platform == "darwin"


def is_windows() -> bool:
    """Check if running on Windows."""
    return sys.platform == "win32"


__all__ = ["get_platform_handler", "is_macos", "is_windows"]

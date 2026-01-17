"""
macOS platform handler.
"""
import subprocess
from pathlib import Path
from typing import List, Optional

from .base import PlatformHandler


class MacOSHandler(PlatformHandler):
    """Platform handler for macOS."""

    # macOS uses a fixed location for mods and config, not relative to app bundle
    MODS_DIR = Path.home() / "Library/Application Support/com.shipofharkinian.soh/mods"
    CONFIG_DIR = Path.home() / "Library/Application Support/com.shipofharkinian.soh"
    SAILDECK_CONFIG_DIR = Path.home() / "Library/Application Support/Saildeck"

    @property
    def platform_name(self) -> str:
        return "macOS"

    @property
    def game_executable_name(self) -> str:
        return "soh.app"

    def get_default_game_paths(self) -> List[Path]:
        """Return common macOS installation paths for Ship of Harkinian."""
        return [
            Path("/Applications/soh.app"),
            Path.home() / "Applications/soh.app",
            Path("/Applications/Ship of Harkinian.app"),
            Path.home() / "Applications/Ship of Harkinian.app",
        ]

    def get_mods_directory(self, game_path: Optional[Path] = None) -> Path:
        """
        Return the mods directory (fixed location on macOS).

        On macOS, mods are stored in ~/Library/Application Support/com.shipofharkinian.soh/mods/
        regardless of where the app bundle is located.

        Args:
            game_path: Ignored on macOS.

        Returns:
            Path to the mods directory.
        """
        return self.MODS_DIR

    def get_config_directory(self) -> Path:
        """Return the Saildeck configuration directory on macOS."""
        return self.SAILDECK_CONFIG_DIR

    def validate_game_installation(self, path: Path) -> bool:
        """
        Validate game installation by checking for the app bundle structure.

        Args:
            path: Path to validate (should be a .app bundle or directory containing soh binary).

        Returns:
            True if valid game installation.
        """
        if not path.exists():
            return False

        # Check if it's a .app bundle
        if path.suffix == ".app":
            # Check for the actual executable inside the bundle
            executable = path / "Contents/MacOS/soh"
            if executable.is_file():
                return True
            # Also check for lowercase variants
            executable = path / "Contents/MacOS/SoH"
            if executable.is_file():
                return True
            # Check for any executable in MacOS folder
            macos_dir = path / "Contents/MacOS"
            if macos_dir.is_dir():
                for item in macos_dir.iterdir():
                    if item.is_file() and not item.name.startswith("."):
                        return True
            return False

        # Check if it's a directory containing the soh binary directly
        if path.is_dir():
            for name in ["soh", "SoH"]:
                if (path / name).is_file():
                    return True

        return False

    def get_game_executable(self, game_path: Path) -> Path:
        """
        Return the full path to the game executable.

        Args:
            game_path: The game installation path (.app bundle).

        Returns:
            Full path to the executable inside the bundle.
        """
        if game_path.suffix == ".app":
            # Standard location inside app bundle
            executable = game_path / "Contents/MacOS/soh"
            if executable.exists():
                return executable
            # Try uppercase variant
            executable = game_path / "Contents/MacOS/SoH"
            if executable.exists():
                return executable
            # Fall back to finding any executable
            macos_dir = game_path / "Contents/MacOS"
            if macos_dir.is_dir():
                for item in macos_dir.iterdir():
                    if item.is_file() and not item.name.startswith("."):
                        return item
        return game_path / "soh"

    def get_game_config_path(self, game_path: Path) -> Path:
        """
        Return the path to shipofharkinian.json.

        On macOS, the config is in ~/Library/Application Support/com.shipofharkinian.soh/
        """
        return self.CONFIG_DIR / "shipofharkinian.json"

    def open_folder(self, path: Path) -> None:
        """Open folder in Finder."""
        subprocess.run(["open", str(path)], check=False)

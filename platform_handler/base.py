"""
Base class for platform-specific handlers.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional


class PlatformHandler(ABC):
    """Abstract base class for platform-specific operations."""

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return the platform name (e.g., 'Windows', 'macOS')."""
        pass

    @property
    @abstractmethod
    def game_executable_name(self) -> str:
        """Return the game executable name for display purposes."""
        pass

    @abstractmethod
    def get_default_game_paths(self) -> List[Path]:
        """Return a list of default paths to search for the game installation."""
        pass

    @abstractmethod
    def get_mods_directory(self, game_path: Optional[Path] = None) -> Path:
        """
        Return the mods directory path.

        Args:
            game_path: The game installation path (used on Windows, ignored on macOS).

        Returns:
            The path to the mods directory.
        """
        pass

    @abstractmethod
    def get_config_directory(self) -> Path:
        """Return the Saildeck configuration directory."""
        pass

    @abstractmethod
    def validate_game_installation(self, path: Path) -> bool:
        """
        Validate that the given path is a valid game installation.

        Args:
            path: Path to validate.

        Returns:
            True if valid game installation, False otherwise.
        """
        pass

    @abstractmethod
    def get_game_executable(self, game_path: Path) -> Path:
        """
        Return the full path to the game executable.

        Args:
            game_path: The game installation path.

        Returns:
            Full path to the executable.
        """
        pass

    @abstractmethod
    def get_game_config_path(self, game_path: Path) -> Path:
        """
        Return the path to the game's configuration file (shipofharkinian.json).

        Args:
            game_path: The game installation path.

        Returns:
            Path to the config file.
        """
        pass

    @abstractmethod
    def open_folder(self, path: Path) -> None:
        """
        Open a folder in the system file manager.

        Args:
            path: Path to open.
        """
        pass

    def auto_detect_game_path(self) -> Optional[Path]:
        """
        Attempt to automatically detect the game installation.

        Returns:
            The detected game path, or None if not found.
        """
        for path in self.get_default_game_paths():
            if path.exists() and self.validate_game_installation(path):
                return path
        return None

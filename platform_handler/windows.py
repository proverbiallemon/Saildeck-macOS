"""
Windows platform handler.
"""
import os
import subprocess
from pathlib import Path
from typing import List, Optional

from .base import PlatformHandler


class WindowsHandler(PlatformHandler):
    """Platform handler for Windows."""

    @property
    def platform_name(self) -> str:
        return "Windows"

    @property
    def game_executable_name(self) -> str:
        return "soh.exe"

    def get_default_game_paths(self) -> List[Path]:
        """Return common Windows installation paths for Ship of Harkinian."""
        paths = []

        # Common installation locations
        program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        user_profile = os.environ.get("USERPROFILE", "")

        if program_files:
            paths.append(Path(program_files) / "Ship of Harkinian")
            paths.append(Path(program_files) / "soh")

        if program_files_x86:
            paths.append(Path(program_files_x86) / "Ship of Harkinian")
            paths.append(Path(program_files_x86) / "soh")

        if local_appdata:
            paths.append(Path(local_appdata) / "Ship of Harkinian")

        if user_profile:
            paths.append(Path(user_profile) / "Games" / "Ship of Harkinian")
            paths.append(Path(user_profile) / "Desktop" / "Ship of Harkinian")
            paths.append(Path(user_profile) / "Downloads" / "Ship of Harkinian")

        return paths

    def get_mods_directory(self, game_path: Optional[Path] = None) -> Path:
        """
        Return the mods directory (inside game folder on Windows).

        Args:
            game_path: The game installation path.

        Returns:
            Path to the mods directory.
        """
        if game_path is None:
            raise ValueError("game_path is required on Windows")
        return game_path / "mods"

    def get_config_directory(self) -> Path:
        """Return the Saildeck configuration directory on Windows."""
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "Saildeck"
        return Path.home() / "Saildeck"

    def validate_game_installation(self, path: Path) -> bool:
        """
        Validate game installation by checking for soh.exe.

        Args:
            path: Path to validate.

        Returns:
            True if soh.exe exists in the path.
        """
        if not path.exists():
            return False
        exe_path = path / "soh.exe"
        return exe_path.is_file()

    def get_game_executable(self, game_path: Path) -> Path:
        """Return the full path to soh.exe."""
        return game_path / "soh.exe"

    def get_game_config_path(self, game_path: Path) -> Path:
        """Return the path to shipofharkinian.json (in game folder on Windows)."""
        return game_path / "shipofharkinian.json"

    def open_folder(self, path: Path) -> None:
        """Open folder in Windows Explorer."""
        os.startfile(str(path))

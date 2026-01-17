import os
import json
from pathlib import Path
from typing import Optional
from platform_handler import get_platform_handler

SETTINGS_FILE = "saildeck.data"


def is_valid_game_dir(path: str) -> bool:
    """
    Validate if the path is a valid game installation.
    Uses platform-specific validation (soh.exe on Windows, soh.app on macOS).
    """
    handler = get_platform_handler()
    return handler.validate_game_installation(Path(path))

def ensure_mods_folder(game_dir: str):
    """
    Create the mods folder if it doesn't exist.
    Uses platform-specific location.
    """
    handler = get_platform_handler()
    mods_path = handler.get_mods_directory(Path(game_dir) if game_dir else None)
    os.makedirs(mods_path, exist_ok=True)


def get_mods_folder(game_dir: str) -> str:
    """
    Return the mods folder path.
    Uses platform-specific location.
    """
    handler = get_platform_handler()
    return str(handler.get_mods_directory(Path(game_dir) if game_dir else None))

def list_mod_files(mods_dir: str) -> list:
    """
    Recursively list all .otr, .o2r, .disabled, .di2abled files.
    """
    mods = []
    for root, _, files in os.walk(mods_dir):
        for file in files:
            if file.endswith((".otr", ".o2r", ".disabled", ".di2abled")):
                mods.append(os.path.join(root, file))
    return mods

def read_json(path: str, default: dict = {}) -> dict:
    """
    Load a JSON file. Returns `default` on error.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def write_json(path: str, data: dict):
    """
    Write a dictionary to a JSON file.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ==== SETTINGS FUNCTIONS ====

def load_settings() -> dict:
    """
    Load settings from saildeck.data.
    """
    return read_json(SETTINGS_FILE, default={})

def save_settings(settings: dict):
    """
    Save settings to saildeck.data.
    """
    write_json(SETTINGS_FILE, settings)

def get_game_path() -> Optional[str]:
    """
    Return the game path from settings (or None if not set).
    """
    settings = load_settings()
    return settings.get("game_path")

def set_game_path(path: str):
    """
    Set and save the game path in settings.
    """
    settings = load_settings()
    settings["game_path"] = path
    save_settings(settings)

def init_settings_file():
    """
    Create saildeck.data file if it doesn't exist.
    """
    if not os.path.isfile(SETTINGS_FILE):
        write_json(SETTINGS_FILE, {})

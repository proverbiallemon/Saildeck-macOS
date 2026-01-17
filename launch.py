import os
import sys
import json
import subprocess
from pathlib import Path
from platform_handler import get_platform_handler, is_macos

SETTINGS_FILE = "saildeck.data"

def should_enable_altassets():
    """Check if the user wants AltAssets to be force-enabled."""
    if not os.path.exists(SETTINGS_FILE):
        print("[Info] No config file found, AltAssets enabled by default.")
        return True
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
            enabled = settings.get("enable_altassets", True)
            print(f"[Info] AltAssets auto-activation: {'enabled' if enabled else 'disabled'}")
            return enabled
    except Exception as e:
        print(f"[!] Error reading {SETTINGS_FILE}: {e}")
        return True

def has_enabled_mod(mods_dir):
    """Return True if an active .otr or .o2r is found anywhere in /mods."""
    print(f"[Search] Recursively searching for active mods in: {mods_dir}")
    if not os.path.exists(mods_dir):
        print("[Warning] Mods folder not found.")
        return False

    for root, _, files in os.walk(mods_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in [".otr", ".o2r"]:
                full_path = os.path.join(root, file)
                print(f"[OK] Active mod detected: {full_path}")
                return True

    print("[Info] No active .otr or .o2r files detected in subfolders.")
    return False

def ensure_altassets_enabled(config_path):
    """Enable AltAssets in CVars > gSettings only."""
    print(f"[Config] Enabling AltAssets in gSettings: {config_path}")
    if not os.path.exists(config_path):
        print("[Warning] shipofharkinian.json not found.")
        return

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        settings = config.get("CVars", {}).get("gSettings", None)
        if settings is None:
            print("[Warning] CVars > gSettings not found.")
            return

        if settings.get("AltAssets") != 1:
            settings["AltAssets"] = 1
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            print("[OK] AltAssets (gSettings) enabled.")
        else:
            print("[Info] AltAssets (gSettings) is already enabled.")

    except Exception as e:
        print(f"[!] Error updating AltAssets: {e}")

def launch_game(soh_path, mods_dir):
    """Launch the game after enabling AltAssets if necessary."""
    handler = get_platform_handler()
    game_path = Path(soh_path)
    exe_path = handler.get_game_executable(game_path)
    config_path = handler.get_game_config_path(game_path)

    print(f"[Launch] Starting game from: {soh_path}")

    if has_enabled_mod(mods_dir) and should_enable_altassets():
        ensure_altassets_enabled(str(config_path))
    else:
        print("[Info] No active mods or AltAssets option disabled.")

    if exe_path.exists():
        if is_macos():
            # On macOS, use 'open' command for .app bundles
            if game_path.suffix == ".app":
                subprocess.Popen(["open", str(game_path)])
            else:
                subprocess.Popen([str(exe_path)], cwd=str(game_path))
        else:
            subprocess.Popen([str(exe_path)], cwd=str(game_path))
        print("[Launch] Game started. Closing Saildeck...")
        sys.exit(0)
    else:
        exe_name = handler.game_executable_name
        print(f"[Error] {exe_name} not found.")

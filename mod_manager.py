import os
from utils import list_mod_files


def toggle_mod_state(mod_path: str):
    """
    Toggle mod state between enabled/disabled.
    - .o2r <-> .di2abled
    - .otr <-> .disabled
    """
    if mod_path.endswith(".di2abled"):
        new_path = os.path.splitext(mod_path)[0] + ".o2r"
    elif mod_path.endswith(".disabled"):
        new_path = os.path.splitext(mod_path)[0] + ".otr"
    elif mod_path.endswith(".o2r"):
        new_path = os.path.splitext(mod_path)[0] + ".di2abled"
    elif mod_path.endswith(".otr"):
        new_path = os.path.splitext(mod_path)[0] + ".disabled"
    else:
        return  # Ignore other files

    os.rename(mod_path, new_path)


def delete_mod(mod_path: str):
    if os.path.exists(mod_path):
        os.remove(mod_path)


def set_mod_enabled(mod_path: str, enable: bool):
    """
    Force the mod state (enabled or disabled) based on `enable`.
    """
    if enable:
        if mod_path.endswith(".disabled") or mod_path.endswith(".di2abled"):
            new_ext = ".otr" if mod_path.endswith(".disabled") else ".o2r"
            new_path = os.path.splitext(mod_path)[0] + new_ext
            os.rename(mod_path, new_path)
    else:
        if mod_path.endswith(".otr"):
            os.rename(mod_path, os.path.splitext(mod_path)[0] + ".disabled")
        elif mod_path.endswith(".o2r"):
            os.rename(mod_path, os.path.splitext(mod_path)[0] + ".di2abled")



def load_mods(mods_dir: str) -> list:
    mods = []
    files = list_mod_files(mods_dir)

    for path in files:
        is_enabled = not (path.endswith(".disabled") or path.endswith(".di2abled"))
        mods.append({
            "path": path,
            "enabled": is_enabled
        })

    return mods


def find_mods_root(path: str) -> str:
    """
    Traverse up to the "mods" folder.
    """
    current = os.path.abspath(path)
    while True:
        if os.path.basename(current) == "mods":
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return os.path.dirname(path)


def toggle_mods_in_folder(folder_path: str):
    """
    Enable or disable all mods in a folder (recursively).
    """
    if not os.path.isdir(folder_path):
        raise ValueError("The specified path is not a folder.")

    mod_files = []

    for root, _, files in os.walk(folder_path):
        for f in files:
            if f.endswith((".otr", ".o2r", ".disabled", ".di2abled")):
                mod_files.append(os.path.join(root, f))

    if not mod_files:
        raise ValueError("No mods found to enable/disable in this folder.")

    # Determine if at least one is disabled
    has_disabled = any(
        f.endswith(".disabled") or f.endswith(".di2abled") for f in mod_files
    )

    for mod in mod_files:
        # If we want to enable all disabled mods
        if has_disabled:
            if mod.endswith(".disabled") or mod.endswith(".di2abled"):
                toggle_mod_state(mod)
        else:
            if mod.endswith(".otr") or mod.endswith(".o2r"):
                toggle_mod_state(mod)

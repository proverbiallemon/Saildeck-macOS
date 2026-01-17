import sys
import os
from gui import ModManagerGUI
from utils import get_game_path, set_game_path, is_valid_game_dir, init_settings_file
from check_version import prompt_and_update_if_needed
from platform_handler import get_platform_handler, is_macos
import time
import tkinter as tk
from tkinter import filedialog


def ask_game_path():
    handler = get_platform_handler()

    # Try auto-detection first
    auto_detected = handler.auto_detect_game_path()
    if auto_detected:
        print(f"Auto-detected game at: {auto_detected}")
        set_game_path(str(auto_detected))
        time.sleep(0.1)
        return str(auto_detected)

    root = tk.Tk()
    root.withdraw()

    # On macOS, use file dialog to select .app bundle
    if is_macos():
        # Use askopenfilename with filetypes for .app on macOS
        selected_path = filedialog.askopenfilename(
            title="Select Ship of Harkinian (soh.app)",
            filetypes=[("Application", "*.app"), ("All files", "*.*")]
        )
    else:
        selected_path = filedialog.askdirectory(title="Select Ship of Harkinian folder")

    root.destroy()

    if selected_path and is_valid_game_dir(selected_path):
        set_game_path(selected_path)
        time.sleep(0.1)
        return selected_path
    else:
        exe_name = handler.game_executable_name
        print(f"Selected path is not a valid Ship of Harkinian installation (expected {exe_name}).")
        sys.exit(1)

def main():
    init_settings_file()
    # Check for updates
    prompt_and_update_if_needed()

    # Read game path
    game_path = get_game_path()
    if not game_path or not is_valid_game_dir(game_path):
        game_path = ask_game_path()
        if not game_path:
            return
        set_game_path(game_path)

    # Launch main application
    app = ModManagerGUI(game_path)
    app.mainloop()

if __name__ == "__main__":
    main()

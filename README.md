# Saildeck macOS

> **Looking for a more polished experience?** Check out [Sailswift](https://github.com/proverbiallemon/Sailswift) - a native Swift/SwiftUI rewrite of this project. Sailswift is actively maintained with faster updates, better performance, and additional features like one-click mod installation from GameBanana via custom URL scheme.

A macOS port of [Saildeck](https://github.com/Wolfeni/Saildeck) - a mod manager for Ship of Harkinian.

![Saildeck_logo](https://github.com/user-attachments/assets/187e5820-cc41-46e6-a94a-68127e50c4bc)

## About This Fork

This is a **macOS-compatible fork** of [Saildeck by Wolfeni](https://github.com/Wolfeni/Saildeck). The original Saildeck was designed for Windows only. This fork adds platform abstraction to support macOS while maintaining full Windows compatibility.

> **Note**: This fork may include additional features and improvements not present in the original Windows version. See [What's New in This Fork](#whats-new-in-this-fork) for details.

### Credits

- **Original Author**: [Wolfeni](https://github.com/Wolfeni)
- **Original Repository**: [https://github.com/Wolfeni/Saildeck](https://github.com/Wolfeni/Saildeck)
- **Shiploader** (spiritual predecessor): [https://gamebanana.com/tools/16326](https://gamebanana.com/tools/16326) by Purple Hato

This fork is released under the same **GPL-3.0 license** as the original.

## What's New in This Fork

### macOS Support
- Platform abstraction layer (`platform_handler/`) for cross-platform support
- macOS-specific paths:
  - Game detection: `/Applications/soh.app` or `~/Applications/soh.app`
  - Mods folder: `~/Library/Application Support/com.shipofharkinian.soh/mods/`
  - Config: `~/Library/Application Support/com.shipofharkinian.soh/shipofharkinian.json`
- Uses `open` command instead of `os.startfile()` for Finder integration
- Fixed Windows-only dependencies (`pywin32-ctypes` now conditional)

### GameBanana Mod Browser (v1.3.0)
- **Browse mods directly** - Browse Ship of Harkinian mods from GameBanana without leaving the app
- **Search & filter** - Search by name, filter by category (Models, Textures, Music, etc.)
- **One-click install** - Download and install mods with a single click
- **Progress tracking** - Progress bar shows download status
- **Automatic organization** - Mods are installed into organized subfolders
- **Security hardened** - Zip Slip protection, MD5 verification, file safety validation

### UI Modernization (v1.2.0)
- **Light/Dark/System theme modes** - Follows your system appearance automatically
- **8 theme options** - 4 light themes (Litera, Flatly, Cosmo, Minty) and 4 dark themes (Darkly, Superhero, Cyborg, Solar)
- **Redesigned Settings window** - Tabbed interface with Appearance, Behavior, and Advanced sections
- **Resizable main window** - Window can now be resized (minimum 700x550)
- **Cross-platform fonts** - Automatically uses SF Pro Text on macOS, Segoe UI on Windows
- **View menu** - Quick access to theme switching from the menu bar
- **Confirm before delete option** - Optional confirmation dialog when deleting mods

### Additional Features
- **Open Mods Folder button** - Quick access to your mods directory from the main UI
- All strings translated to English (original was French)

## Requirements

- **macOS**: Tested on macOS Tahoe (26.x)
- **Python**: 3.9+ with tkinter support
- **Ship of Harkinian**: Installed at `/Applications/soh.app`

## Installation

```bash
# Clone this repository
git clone https://github.com/proverbiallemon/Saildeck-macOS.git
cd Saildeck-macOS

# Create virtual environment (use Python with tkinter)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Python with tkinter on macOS

If you get a tkinter error, install Python with tkinter support:

```bash
brew install python-tk@3.13
/opt/homebrew/bin/python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Launch Saildeck: `python main.py`
2. If SoH is at `/Applications/soh.app`, it will be auto-detected
3. Otherwise, select your `soh.app` when prompted
4. Mods are managed in `~/Library/Application Support/com.shipofharkinian.soh/mods/`

### Features

- **Browse & download mods** from GameBanana with built-in mod browser
- Toggle mods on/off (double-click or use Toggle button)
- Delete mods (sends to Trash)
- Open mods folder directly in Finder
- Save/Load mod profiles
- Export/Import modpacks as ZIP
- Auto-enable AltAssets when mods are active
- Light/Dark/System theme modes with 8 theme variants
- Customizable settings via tabbed Settings window

## Status

**Stable** - v1.3.0 is the first stable release. Please report any issues!

## Original Saildeck Features

Saildeck lets you activate and deactivate mods for Ship of Harkinian. It is a spiritual successor to Shiploader with support for `.otr` and `.o2r` files.

## Documentation

- [macOS Setup Guide](docs/MACOS_SETUP.md) - Detailed installation and troubleshooting
- [Changelog](CHANGELOG.md) - Version history and changes
- [Translations](TRANSLATIONS.md) - French to English translation reference

## License

GPL-3.0 - Same as the original Saildeck. See [LICENSE](LICENSE) for details.

---

*This is an unofficial macOS port. For the official Windows version, visit [Wolfeni/Saildeck](https://github.com/Wolfeni/Saildeck).*

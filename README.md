# Saildeck macOS

A macOS port of [Saildeck](https://github.com/Wolfeni/Saildeck) - a mod manager for Ship of Harkinian.

![Saildeck_logo](https://github.com/user-attachments/assets/187e5820-cc41-46e6-a94a-68127e50c4bc)

## About This Fork

This is a **macOS-compatible fork** of [Saildeck by Wolfeni](https://github.com/Wolfeni/Saildeck). The original Saildeck was designed for Windows only. This fork adds platform abstraction to support macOS while maintaining full Windows compatibility.

### Credits

- **Original Author**: [Wolfeni](https://github.com/Wolfeni)
- **Original Repository**: [https://github.com/Wolfeni/Saildeck](https://github.com/Wolfeni/Saildeck)
- **Shiploader** (spiritual predecessor): [https://gamebanana.com/tools/16326](https://gamebanana.com/tools/16326) by Purple Hato

This fork is released under the same **GPL-3.0 license** as the original.

## What's Changed (macOS Port)

- Added platform abstraction layer (`platform_handler/`) for cross-platform support
- macOS-specific paths:
  - Game detection: `/Applications/soh.app` or `~/Applications/soh.app`
  - Mods folder: `~/Library/Application Support/com.shipofharkinian.soh/mods/`
  - Config: `~/Library/Application Support/com.shipofharkinian.soh/shipofharkinian.json`
- Translated all French strings to English
- Fixed Windows-only dependencies (`pywin32-ctypes` now conditional)
- Uses `open` command instead of `os.startfile()` for Finder integration

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

- Toggle mods on/off (double-click or use Toggle button)
- Delete mods (sends to Trash)
- Save/Load mod profiles
- Export/Import modpacks as ZIP
- Auto-enable AltAssets when mods are active

## Status

**Beta** - This macOS port is functional but may have bugs. Please report issues!

## Original Saildeck Features

Saildeck lets you activate and deactivate mods for Ship of Harkinian. It is a spiritual successor to Shiploader with support for `.otr` and `.o2r` files.

## License

GPL-3.0 - Same as the original Saildeck. See [LICENSE](LICENSE) for details.

---

*This is an unofficial macOS port. For the official Windows version, visit [Wolfeni/Saildeck](https://github.com/Wolfeni/Saildeck).*

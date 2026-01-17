# macOS Setup Guide for Saildeck

This guide walks you through setting up Saildeck on macOS to manage mods for Ship of Harkinian.

## Prerequisites

### 1. Ship of Harkinian (SoH)

Download and install Ship of Harkinian for macOS:
- Get it from the [Ship of Harkinian website](https://www.shipofharkinian.com/) or [GitHub releases](https://github.com/HarbourMasters/Shipwright/releases)
- Place `soh.app` in `/Applications/` (recommended) or `~/Applications/`

Verify installation:
```bash
ls -la /Applications/soh.app/Contents/MacOS/soh
```

### 2. Python with tkinter

Saildeck requires Python 3.9+ with tkinter support. The default Homebrew Python often lacks tkinter.

**Option A: Install Python with tkinter via Homebrew (Recommended)**
```bash
# Install Python 3.13 with tkinter
brew install python-tk@3.13

# Verify tkinter works
/opt/homebrew/bin/python3.13 -c "import tkinter; print('tkinter OK')"
```

**Option B: Use pyenv with tkinter**
```bash
# Install dependencies
brew install tcl-tk pyenv

# Configure pyenv to use Homebrew's tcl-tk
export LDFLAGS="-L$(brew --prefix tcl-tk)/lib"
export CPPFLAGS="-I$(brew --prefix tcl-tk)/include"
export PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig"

# Install Python with tkinter
pyenv install 3.12.0
pyenv global 3.12.0
```

**Option C: Download from python.org**
- Download the official installer from [python.org](https://www.python.org/downloads/macos/)
- The official installer includes tkinter

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/proverbiallemon/Saildeck-macOS.git
cd Saildeck-macOS
```

### Step 2: Create Virtual Environment

Using Homebrew Python with tkinter:
```bash
/opt/homebrew/bin/python3.13 -m venv venv
source venv/bin/activate
```

Or if using system/pyenv Python:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Saildeck

```bash
python main.py
```

## First Run

On first launch, Saildeck will:

1. **Auto-detect SoH**: If installed at `/Applications/soh.app`, it will be found automatically
2. **Prompt for location**: If not auto-detected, a file picker will ask you to select `soh.app`
3. **Create mods folder**: The mods directory will be created if it doesn't exist

## File Locations

| Item | macOS Path |
|------|------------|
| Game | `/Applications/soh.app` |
| Mods | `~/Library/Application Support/com.shipofharkinian.soh/mods/` |
| Config | `~/Library/Application Support/com.shipofharkinian.soh/shipofharkinian.json` |
| Saildeck settings | `./saildeck.data` (in Saildeck folder) |

### Accessing the Mods Folder

**Via Finder:**
1. Open Finder
2. Press `Cmd + Shift + G`
3. Enter: `~/Library/Application Support/com.shipofharkinian.soh/mods/`

**Via Terminal:**
```bash
open ~/Library/Application\ Support/com.shipofharkinian.soh/mods/
```

**Via Saildeck:**
- Menu: Saildeck → Open mods folder

## Installing Mods

1. Download `.otr` or `.o2r` mod files
2. Place them in the mods folder (see above)
3. Launch Saildeck - mods will appear in the list
4. Double-click or select + "Toggle state" to enable/disable

### Mod File Types

| Extension | Description |
|-----------|-------------|
| `.otr` | Standard mod (enabled) |
| `.o2r` | Alternate format mod (enabled) |
| `.disabled` | Disabled `.otr` mod |
| `.di2abled` | Disabled `.o2r` mod |

## Troubleshooting

### "No module named '_tkinter'"

Your Python installation lacks tkinter. See [Prerequisites](#2-python-with-tkinter) above.

### "macOS XX required, have instead YY"

This error occurs with older Python versions linked against outdated Tk libraries. Solution:
```bash
brew install python-tk@3.13
/opt/homebrew/bin/python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### SoH Not Auto-Detected

Ensure `soh.app` is in one of these locations:
- `/Applications/soh.app`
- `~/Applications/soh.app`
- `/Applications/Ship of Harkinian.app`
- `~/Applications/Ship of Harkinian.app`

### Mods Not Appearing

1. Check mods are in the correct folder:
   ```bash
   ls ~/Library/Application\ Support/com.shipofharkinian.soh/mods/
   ```
2. Ensure files have `.otr` or `.o2r` extension
3. Click "Refresh mods list" in Saildeck menu

### Permission Issues

If you get permission errors accessing the mods folder:
```bash
chmod 755 ~/Library/Application\ Support/com.shipofharkinian.soh/
chmod 755 ~/Library/Application\ Support/com.shipofharkinian.soh/mods/
```

## Creating a Launch Script

For convenience, create a shell script:

```bash
#!/bin/bash
cd /path/to/Saildeck-macOS
source venv/bin/activate
python main.py
```

Save as `run-saildeck.sh` and make executable:
```bash
chmod +x run-saildeck.sh
```

## Uninstalling

1. Delete the Saildeck-macOS folder
2. Optionally remove settings: `rm ./saildeck.data`
3. Mods folder is preserved (managed by SoH)

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/proverbiallemon/Saildeck-macOS/issues)
- **Original Saildeck**: [Wolfeni/Saildeck](https://github.com/Wolfeni/Saildeck)
- **Ship of Harkinian**: [Discord](https://discord.com/invite/shipofharkinian)

# Changelog

All notable changes to Saildeck macOS will be documented in this file.

This project is a fork of [Saildeck by Wolfeni](https://github.com/Wolfeni/Saildeck).

## [1.3.0-macos] - 2026-01-17

### Added
- **GameBanana Mod Browser** (`download/` module)
  - Browse Ship of Harkinian mods directly from GameBanana
  - Search mods by name with real-time results
  - Filter by category (Models, Textures, Music, Audio, Skins, etc.)
  - One-click download and install to mods folder
  - Progress bar during downloads
  - ZIP and 7z archive extraction support
  - Mods automatically organized into subfolders by name
  - Lazy-load file info for faster browsing
- **GameBanana V11 API Integration** (`download/gamebanana/api.py`)
  - Full V11 API support with pagination
  - Mod metadata: images, authors, view/like counts
  - On-demand file info fetching

### Security
- **Zip Slip Protection** - Path validation prevents malicious archives from writing outside target directory
- **MD5 Checksum Verification** - Downloaded files verified against GameBanana checksums
- **File Safety Validation** - Files flagged by GameBanana analysis are blocked
- **Race Condition Fix** - Atomic folder naming using UUID prevents conflicts

### Changed
- `gui.py` - Download Mods button now functional, opens mod browser
- Theme-aware canvas background in downloader window

### Fixed
- Bare `except` clauses replaced with specific exception types
- Thread-unsafe lambda closures in download progress callbacks

---

## [1.2.0-macos-beta.1] - 2026-01-17

### Added
- **Theme Manager** (`theme_manager.py`)
  - Central theme management with Light/Dark/System modes
  - System theme detection using `darkdetect`
  - 4 light themes: Litera, Flatly, Cosmo, Minty
  - 4 dark themes: Darkly, Superhero, Cyborg, Solar
  - Theme-aware color provider for custom widgets
  - Settings persistence with backward-compatible migration
- **View Menu** in menu bar
  - Theme Mode submenu (Light/Dark/System)
  - Light Theme selection submenu
  - Dark Theme selection submenu
- **Redesigned Settings Window**
  - Converted from `tk.Toplevel` to `tb.Toplevel`
  - Tabbed interface with `tb.Notebook`:
    - **Appearance**: Theme mode selector, light/dark theme dropdowns
    - **Behavior**: Skip update, auto-enable AltAssets, confirm before delete
    - **Advanced**: Game/mods directory display, reset settings button
  - Live theme preview when changing settings
- **Confirm before delete** setting - Optional confirmation when deleting mods
- **Cross-platform font support**
  - SF Pro Text on macOS
  - Segoe UI on Windows
  - DejaVu Sans on Linux
- **CRT Retro Themes**
  - CRT Green: Classic green phosphor terminal aesthetic (#00FF41)
  - CRT Amber: Warm amber phosphor aesthetic (#FFB000)
  - Monospace fonts (SF Mono/Consolas) for authentic CRT look

### Changed
- `gui.py` - Integrated theme manager, window now resizable (min 700x550)
- `menubar.py` - Added View menu with theme controls
- `settings_window.py` - Complete rewrite with tabbed interface
- `about.py` - Theme-aware colors, converted to ttkbootstrap widgets
- `delete.py` - Respects `confirm_delete` setting
- `download/downloader_window.py` - Theme-aware tooltip colors
- `download/gamebanana/widgets.py` - Platform-aware fonts
- `menubar.py` - Added Special Themes submenu with CRT options
- Settings structure expanded to nested format:
```json
  {
    "appearance": {
      "theme_mode", "light_theme", "dark_theme", "special_theme"
    },
    "behavior": { "skip_update", "enable_altassets", "confirm_delete" }
  }
```

### Fixed
- Hardcoded colors in About window now theme-aware
- Hardcoded tooltip colors now theme-aware
- All "Segoe UI" fonts replaced with platform-appropriate fonts
- Light mode theme switching not applying changes (is_light_mode now checks mode setting)

---

## [1.1.0-macos-beta.1] - 2025-01-17

### Added
- **Platform abstraction layer** (`platform_handler/` module)
  - `base.py` - Abstract base class defining platform interface
  - `macos.py` - macOS-specific implementation
  - `windows.py` - Windows implementation (preserves original behavior)
- **macOS support**
  - Auto-detection of SoH at `/Applications/soh.app` and `~/Applications/soh.app`
  - macOS mods directory: `~/Library/Application Support/com.shipofharkinian.soh/mods/`
  - macOS config path: `~/Library/Application Support/com.shipofharkinian.soh/`
  - Finder integration using `open` command
  - `.app` bundle validation
- **Documentation**
  - `TRANSLATIONS.md` - Complete French to English translation reference
  - `CHANGELOG.md` - Version history
  - `docs/MACOS_SETUP.md` - Detailed macOS setup guide
  - Updated `README.md` with macOS-specific instructions

### Changed
- `utils.py` - Now uses platform handler for path resolution
- `main.py` - Added auto-detection, macOS file picker for `.app` bundles
- `launch.py` - Platform-aware game launching
- `gui.py` - Replaced `os.startfile()` with cross-platform folder opening
- `requirements.txt` - Added platform markers for Windows-only dependencies
- All French strings translated to English

### Fixed
- Windows-only dependency `pywin32-ctypes` now conditionally installed
- `os.startfile()` replaced with platform-agnostic solution

### Upstream Base
- Based on Saildeck v1.0.41 by [Wolfeni](https://github.com/Wolfeni)

---

## Versioning

This fork uses semantic versioning with platform suffix:
- `X.Y.Z-macos-beta.N` for macOS beta releases
- Major version bumps when significant features added
- Minor version bumps for new functionality
- Patch version for bug fixes

## Original Saildeck Versions

For the original Windows version changelog, see [Wolfeni/Saildeck](https://github.com/Wolfeni/Saildeck).

# Changelog

All notable changes to Saildeck macOS will be documented in this file.

This project is a fork of [Saildeck by Wolfeni](https://github.com/Wolfeni/Saildeck).

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

import os
import re
import shutil
import tempfile
import zipfile
import requests

# Try to import py7zr for 7z support
try:
    import py7zr
    HAS_7Z = True
except ImportError:
    HAS_7Z = False

MOD_EXTENSIONS = {".otr", ".o2r"}
HEADERS = {"User-Agent": "Saildeck/1.0 (Ship of Harkinian Mod Manager)"}


def sanitize_folder_name(name):
    """Create a safe folder name from mod name."""
    # Remove or replace unsafe characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip('. ')
    # Limit length
    if len(name) > 50:
        name = name[:50].strip()
    return name or "mod"


def download_file(url, dest_path, progress_callback=None):
    """Download a file with progress callback."""
    try:
        response = requests.get(url, stream=True, headers=HEADERS, timeout=120, allow_redirects=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total_size)

        return True
    except Exception as e:
        print(f"[Download] Error downloading {url}: {e}")
        return False


def extract_archive(archive_path, dest_dir):
    """Extract an archive (ZIP or 7z)."""
    filename_lower = archive_path.lower()

    try:
        if filename_lower.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zf:
                zf.extractall(dest_dir)
            return True

        elif filename_lower.endswith('.7z') and HAS_7Z:
            with py7zr.SevenZipFile(archive_path, 'r') as archive:
                archive.extractall(dest_dir)
            return True

        elif filename_lower.endswith('.7z') and not HAS_7Z:
            print("[Download] Cannot extract 7z - py7zr not installed")
            return False

        elif filename_lower.endswith('.rar'):
            print("[Download] RAR files not supported")
            return False

        else:
            # Try as zip
            try:
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    zf.extractall(dest_dir)
                return True
            except zipfile.BadZipFile:
                print(f"[Download] Unknown archive format: {archive_path}")
                return False

    except Exception as e:
        print(f"[Download] Error extracting {archive_path}: {e}")
        return False


def find_mod_files(directory):
    """Find all mod files (.otr/.o2r) recursively."""
    mod_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            ext = os.path.splitext(filename.lower())[1]
            if ext in MOD_EXTENSIONS:
                mod_files.append(os.path.join(root, filename))
    return mod_files


def download_and_install_mod(mod, file_info, mods_dir, callbacks=None):
    """Download and install a mod into its own subfolder.

    Args:
        mod: Mod dict with name and other details
        file_info: File info dict with download_url, filename
        mods_dir: Base mods directory
        callbacks: Dict with on_progress, on_status, on_complete, on_error
    """
    callbacks = callbacks or {}
    on_progress = callbacks.get('on_progress', lambda d, t: None)
    on_status = callbacks.get('on_status', lambda m: None)
    on_complete = callbacks.get('on_complete', lambda s, m: None)
    on_error = callbacks.get('on_error', lambda m: None)

    download_url = file_info.get('download_url')
    filename = file_info.get('filename', 'mod_download')
    mod_name = mod.get('name', 'Unknown Mod')

    if not download_url:
        msg = "No download URL"
        on_error(msg)
        on_complete(False, msg)
        return False, msg

    # Create mod subfolder
    folder_name = sanitize_folder_name(mod_name)
    mod_folder = os.path.join(mods_dir, folder_name)

    # Handle existing folder
    if os.path.exists(mod_folder):
        # Add number suffix if folder exists
        counter = 1
        while os.path.exists(f"{mod_folder}_{counter}"):
            counter += 1
        mod_folder = f"{mod_folder}_{counter}"

    temp_dir = tempfile.mkdtemp(prefix="saildeck_")

    try:
        # Download
        on_status("Downloading...")
        archive_path = os.path.join(temp_dir, filename)

        if not download_file(download_url, archive_path, on_progress):
            msg = "Download failed"
            on_error(msg)
            on_complete(False, msg)
            return False, msg

        # Check if it's already a mod file (not an archive)
        ext = os.path.splitext(filename.lower())[1]
        if ext in MOD_EXTENSIONS:
            on_status("Installing...")
            os.makedirs(mod_folder, exist_ok=True)
            dest_path = os.path.join(mod_folder, filename)
            shutil.move(archive_path, dest_path)
            msg = f"Installed: {folder_name}/{filename}"
            on_status(msg)
            on_complete(True, msg)
            return True, msg

        # Extract archive
        on_status("Extracting...")
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)

        if not extract_archive(archive_path, extract_dir):
            # Check if it's a RAR file
            if filename.lower().endswith('.rar'):
                msg = "RAR files not supported. Please extract manually."
            else:
                msg = "Failed to extract archive"
            on_error(msg)
            on_complete(False, msg)
            return False, msg

        # Find mod files
        on_status("Finding mod files...")
        mod_files = find_mod_files(extract_dir)

        if not mod_files:
            msg = "No .otr/.o2r files found in archive"
            on_error(msg)
            on_complete(False, msg)
            return False, msg

        # Create mod folder and move files
        on_status("Installing...")
        os.makedirs(mod_folder, exist_ok=True)

        installed = []
        for mod_file in mod_files:
            mod_filename = os.path.basename(mod_file)
            dest_path = os.path.join(mod_folder, mod_filename)

            # Handle duplicates within same mod
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(mod_filename)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(mod_folder, f"{base}_{counter}{ext}")
                    counter += 1

            shutil.move(mod_file, dest_path)
            installed.append(os.path.basename(dest_path))

        # Success message
        if len(installed) == 1:
            msg = f"Installed: {folder_name}/{installed[0]}"
        else:
            msg = f"Installed {len(installed)} files to {folder_name}/"

        on_status(msg)
        on_complete(True, msg)
        return True, msg

    except Exception as e:
        msg = str(e)
        on_error(msg)
        on_complete(False, msg)
        return False, msg

    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass


def format_filesize(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

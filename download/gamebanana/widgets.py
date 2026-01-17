import webbrowser
import requests
import os
import threading
from PIL import Image, ImageTk
from io import BytesIO
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from download.gamebanana.gb_download import download_and_install_mod, format_filesize
from download.gamebanana.api import get_mod_files

# Import theme_manager from parent package
try:
    from theme_manager import get_platform_font
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from theme_manager import get_platform_font


def render_mod_card(parent, mod: dict, mods_dir=None, on_download_complete=None):
    """Render a mod card with download functionality."""
    font = get_platform_font()

    frame = tb.Frame(parent, padding=10, bootstyle="dark")
    frame.pack(fill="x", padx=10, pady=5, anchor="n")

    # Top row: image + info
    top_row = tb.Frame(frame)
    top_row.pack(fill="x")

    # Image
    img_frame = tb.Frame(top_row, width=64, height=64)
    img_frame.pack(side="left", padx=(0, 10))
    img_frame.pack_propagate(False)

    # Placeholder
    img_label = tb.Label(img_frame, text="🎮", font=(font, 20))
    img_label.pack(expand=True)

    # Load image in background
    if mod.get("image_url"):
        def load_image():
            try:
                img_data = requests.get(mod["image_url"], timeout=5).content
                pil_img = Image.open(BytesIO(img_data)).resize((64, 64))
                tk_img = ImageTk.PhotoImage(pil_img)
                if not hasattr(parent, "_images"):
                    parent._images = []
                parent._images.append(tk_img)

                def update():
                    img_label.config(image=tk_img, text="")
                    img_label.image = tk_img

                frame.after(0, update)
            except Exception:
                pass

        threading.Thread(target=load_image, daemon=True).start()

    # Info section
    info_frame = tb.Frame(top_row)
    info_frame.pack(side="left", fill="both", expand=True)

    # Name
    tb.Label(
        info_frame,
        text=mod.get("name", "Unknown"),
        font=(font, 10, "bold"),
        wraplength=400,
        anchor="w"
    ).pack(anchor="w")

    # Author
    tb.Label(
        info_frame,
        text=f"by {mod.get('author', 'Unknown')}",
        font=(font, 9),
        anchor="w"
    ).pack(anchor="w")

    # Stats row
    stats_frame = tb.Frame(info_frame)
    stats_frame.pack(anchor="w", pady=(2, 0))

    category = mod.get("category", "")
    if category:
        tb.Label(stats_frame, text=category, font=(font, 8), bootstyle="info").pack(side="left", padx=(0, 8))

    views = mod.get("view_count", 0)
    if views:
        view_str = f"{views/1000:.1f}k" if views >= 1000 else str(views)
        tb.Label(stats_frame, text=f"👁 {view_str}", font=(font, 8)).pack(side="left", padx=(0, 8))

    likes = mod.get("like_count", 0)
    if likes:
        like_str = f"{likes/1000:.1f}k" if likes >= 1000 else str(likes)
        tb.Label(stats_frame, text=f"❤ {like_str}", font=(font, 8)).pack(side="left")

    # Button row
    btn_frame = tb.Frame(frame)
    btn_frame.pack(fill="x", pady=(8, 0))

    # State for this card
    card_state = {"downloading": False, "files": None}

    # Status label
    status_label = tb.Label(frame, text="", font=(font, 8), anchor="w")

    # Progress bar (created but not packed)
    progress_bar = tb.Progressbar(frame, mode="determinate", bootstyle="success-striped", maximum=100)

    def start_download():
        if card_state["downloading"]:
            return

        if not mods_dir:
            status_label.config(text="Error: Mods directory not set")
            status_label.pack(fill="x", pady=(5, 0))
            return

        if not mod.get("has_files", True):
            status_label.config(text="No files available for this mod")
            status_label.pack(fill="x", pady=(5, 0))
            return

        card_state["downloading"] = True
        download_btn.config(state="disabled", text="Loading...")
        status_label.config(text="Fetching file info...")
        status_label.pack(fill="x", pady=(5, 0))

        def fetch_and_download():
            try:
                # Fetch files if not already loaded
                if not card_state["files"]:
                    card_state["files"] = get_mod_files(mod["mod_id"])

                files = card_state["files"]
                if not files:
                    frame.after(0, lambda: (
                        status_label.config(text="No downloadable files found"),
                        download_btn.config(state="normal", text="⬇ Download")
                    ))
                    card_state["downloading"] = False
                    return

                file_info = files[0]  # Use first file

                def update_progress(downloaded, total):
                    if total > 0:
                        pct = (downloaded / total) * 100
                        # Capture values to avoid thread-unsafe closure
                        frame.after(0, lambda v=pct: progress_bar.config(value=v))
                        frame.after(0, lambda d=downloaded, t=total: status_label.config(
                            text=f"Downloading: {format_filesize(d)} / {format_filesize(t)}"
                        ))

                def update_status(msg):
                    frame.after(0, lambda: status_label.config(text=msg))

                def on_complete(success, msg):
                    def update():
                        progress_bar.pack_forget()
                        card_state["downloading"] = False
                        if success:
                            download_btn.config(text="✓ Installed", state="disabled", bootstyle="success")
                            status_label.config(text=msg)
                            if on_download_complete:
                                on_download_complete()
                        else:
                            download_btn.config(text="⬇ Retry", state="normal", bootstyle="warning")
                            status_label.config(text=f"Failed: {msg}")

                    frame.after(0, update)

                # Show progress bar
                frame.after(0, lambda: progress_bar.pack(fill="x", pady=(5, 0)))

                # Pass mod name for subfolder creation
                callbacks = {
                    "on_progress": update_progress,
                    "on_status": update_status,
                    "on_complete": on_complete,
                    "on_error": lambda m: frame.after(0, lambda: status_label.config(text=f"Error: {m}"))
                }

                download_and_install_mod(mod, file_info, mods_dir, callbacks)

            except Exception as e:
                frame.after(0, lambda: (
                    status_label.config(text=f"Error: {e}"),
                    download_btn.config(state="normal", text="⬇ Retry", bootstyle="warning")
                ))
                card_state["downloading"] = False

        threading.Thread(target=fetch_and_download, daemon=True).start()

    # Download button
    if mod.get("has_files", True) and mods_dir:
        download_btn = tb.Button(
            btn_frame,
            text="⬇ Download",
            bootstyle="primary",
            cursor="hand2",
            command=start_download
        )
        download_btn.pack(side="left", padx=(0, 5))
    else:
        download_btn = tb.Label(btn_frame, text="No files", font=(font, 9))
        download_btn.pack(side="left", padx=(0, 5))

    # GameBanana link
    tb.Button(
        btn_frame,
        text="🌐 View",
        bootstyle="info-outline",
        cursor="hand2",
        command=lambda: webbrowser.open_new(mod.get("url", ""))
    ).pack(side="left")

    return frame

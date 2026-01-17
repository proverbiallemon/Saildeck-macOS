"""
About Window for Saildeck
Displays credits, version, and links.
"""

import os
import webbrowser
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import Canvas
from PIL import Image, ImageTk
from version import __version__
from theme_manager import get_theme_manager, get_platform_font


def show_about_window(parent):
    theme_manager = get_theme_manager()
    colors = theme_manager.get_colors()
    font = get_platform_font()

    win = tb.Toplevel(parent)
    win.title("About Saildeck")
    win.geometry("420x360")
    win.resizable(False, False)
    win.configure(bg=colors["bg"])
    win.transient(parent)
    win.grab_set()

    # Set the icon
    icon_path = os.path.join(os.path.dirname(__file__), "icon", "icon.ico")
    if os.path.exists(icon_path):
        try:
            win.iconbitmap(icon_path)
        except Exception as e:
            print(f"[!] Error loading icon.ico: {e}")

    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    logo_path = os.path.join(assets_dir, "logo_name.png")

    parent.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() // 2) - 210
    y = parent.winfo_rooty() + (parent.winfo_height() // 2) - 180
    win.geometry(f"+{x}+{y}")

    # Store references to prevent garbage collection
    win._images = {}

    # Saildeck logo via Canvas
    if os.path.exists(logo_path):
        try:
            pil_img = Image.open(logo_path)
            pil_img = pil_img.resize((300, int(pil_img.height * 300 / pil_img.width)), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(pil_img)
            win._images["logo"] = logo_img

            canvas = Canvas(win, width=300, height=logo_img.height(), bg=colors["bg"], highlightthickness=0, bd=0)
            canvas.create_image(0, 0, anchor="nw", image=logo_img)
            canvas.pack(pady=(20, 10))
        except Exception as e:
            print(f"[!] Error loading logo_name.png: {e}")

    # Title label
    title_label = tb.Label(
        win,
        text="Saildeck Mod Manager",
        font=(font, 14, "bold"),
        foreground=colors["fg"],
        background=colors["bg"]
    )
    title_label.pack(pady=(0, 5))

    # Clickable GitHub link
    link = tb.Label(
        win,
        text="Visit GitHub page",
        font=(font, 10, "underline"),
        foreground=colors["link"],
        background=colors["bg"],
        cursor="hand2"
    )
    link.pack(pady=(0, 15))
    link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Wolfeni/Saildeck"))

    # Thanks section
    thanks_frame = tb.Frame(win)
    thanks_frame.configure(style="TFrame")
    thanks_frame.pack(pady=(0, 10))

    # Configure frame background for theme
    style = tb.Style()
    style.configure("About.TFrame", background=colors["bg"])
    thanks_frame.configure(style="About.TFrame")

    thanks_label = tb.Label(
        thanks_frame,
        text="Thanks Purple Hato for the help and for",
        font=(font, 9),
        foreground=colors["muted"],
        background=colors["bg"]
    )
    thanks_label.pack(side="left", padx=(0, 0))

    shiploader_link = tb.Label(
        thanks_frame,
        text="Shiploader",
        font=(font, 9, "underline"),
        foreground=colors["link"],
        background=colors["bg"],
        cursor="hand2"
    )
    shiploader_link.pack(side="left", padx=(0, 0))
    shiploader_link.bind("<Button-1>", lambda e: webbrowser.open("https://gamebanana.com/tools/16326"))

    # Close button
    tb.Button(
        win,
        text="Close",
        command=win.destroy,
        bootstyle="secondary",
        width=10
    ).pack(pady=(0, 10))

    # Version label
    version_label = tb.Label(
        win,
        text=f"v{__version__}",
        font=(font, 8),
        foreground=colors["muted"],
        background=colors["bg"]
    )
    version_label.place(x=10, y=335)

    # Blepy logo in bottom right
    blepy_logo_path = os.path.join(assets_dir, "blepy_logo.png")
    if os.path.exists(blepy_logo_path):
        try:
            blepy_img = Image.open(blepy_logo_path)
            blepy_img = blepy_img.resize((50, 50), Image.LANCZOS)
            blepy_imgtk = ImageTk.PhotoImage(blepy_img)
            win._images["blepy"] = blepy_imgtk

            blepy_label = tb.Label(win, image=blepy_imgtk, background=colors["bg"], borderwidth=0)
            blepy_label.place(x=365, y=305)
        except Exception as e:
            print(f"[!] Error loading blepy_logo.png: {e}")

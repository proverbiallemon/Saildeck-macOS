import webbrowser
import requests
import os
import sys
from PIL import Image, ImageTk
from io import BytesIO
import ttkbootstrap as tb

# Import theme_manager from parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from theme_manager import get_platform_font


def render_mod_card(parent, mod: dict):
    font = get_platform_font()
    frame = tb.Frame(parent, padding=10, bootstyle="dark")
    frame.pack(fill="x", padx=10, pady=5, anchor="n")

    container = tb.Frame(frame)
    container.pack(fill="x")

    # Image mod
    if mod.get("image_url"):
        try:
            img_data = requests.get(mod["image_url"], timeout=5).content
            pil_image = Image.open(BytesIO(img_data)).resize((64, 64))
            tk_image = ImageTk.PhotoImage(pil_image)

            # Store image reference in parent to prevent garbage collection
            if not hasattr(parent, "_images"):
                parent._images = []
            parent._images.append(tk_image)

            img_label = tb.Label(container, image=tk_image)
            img_label.image = tk_image
            img_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"[Image] Erreur image pour {mod['name']}: {e}")

    # Text on the right
    info_frame = tb.Frame(container)
    info_frame.pack(side="left", fill="both", expand=True)

    # Name (1 line max)
    name_label = tb.Label(
        info_frame,
        text=mod.get("name", "Sans titre"),
        font=(font, 10, "bold"),
        wraplength=400,
        anchor="w",
        justify="left"
    )
    name_label.pack(anchor="w")

    # Author
    tb.Label(
        info_frame,
        text=f"Auteur : {mod.get('author', 'inconnu')}",
        font=(font, 9),
        anchor="w"
    ).pack(anchor="w", pady=(2, 0))

    # 🌐 Bouton en bas à droite
    tb.Button(
        frame,
        text="🌐 Page Gamebanana",
        bootstyle="info-outline",
        cursor="hand2",
        command=lambda url=mod.get("url"): webbrowser.open_new(url)
    ).pack(anchor="e", pady=(5, 0))

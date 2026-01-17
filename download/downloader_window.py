import os
import sys
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

import threading
from download.gamebanana.api import fetch_soh_mods
from download.gamebanana.widgets import render_mod_card

try:
    from theme_manager import get_theme_manager, get_platform_font
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from theme_manager import get_theme_manager, get_platform_font

# Known categories for SoH mods
CATEGORIES = [
    "All Categories",
    "Models",
    "Textures",
    "Other/Misc",
    "Samples",
    "Music",
    "Audio",
    "Skins",
    "Animations",
    "Voices"
]


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip_window:
            return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tip_window = tw = tb.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tb.Label(tw, text=self.text, padding=5).pack()

    def hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


def open_downloader_window(parent, mods_dir=None, on_download_complete=None):
    font = get_platform_font()

    window = tb.Toplevel(parent)
    window.title("Download Mods")
    window.geometry("850x650")
    window.resizable(True, True)
    window.minsize(750, 550)

    main_frame = tb.Frame(window)
    main_frame.pack(fill="both", expand=True)

    # Assets
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    assets_dir = os.path.join(root_dir, "assets")

    logos = {}
    for name, filename in [("Gamebanana", "gb_logo.png"), ("Thunderstore", "th_logo.png")]:
        path = os.path.join(assets_dir, filename)
        if os.path.exists(path):
            try:
                img = Image.open(path).resize((40, 40), Image.LANCZOS)
                logos[name] = ImageTk.PhotoImage(img)
            except (IOError, OSError) as e:
                print(f"[Downloader] Could not load logo {filename}: {e}")

    # Sidebar
    sidebar = tb.Frame(main_frame, width=60)
    sidebar.pack(side="left", fill="y", padx=5, pady=5)
    sidebar.pack_propagate(False)
    tb.Label(sidebar, text="Sources", font=(font, 9, "bold")).pack(pady=(0, 10))

    source_buttons = {}
    state = {
        "loading": False,
        "source": None,
        "all_mods": [],  # Cache all loaded mods for filtering
        "displayed_mods": [],
        "page": 1,
        "has_more": False,
        "search": None,
        "sort": "new",
        "category": "All Categories"
    }

    tb.Separator(main_frame, orient=VERTICAL).pack(side="left", fill="y", padx=0, pady=10)

    # Content area
    content = tb.Frame(main_frame)
    content.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    # Filter bar
    filter_bar = tb.Frame(content)

    # Search
    search_var = tb.StringVar()
    search_entry = tb.Entry(filter_bar, textvariable=search_var, width=25, font=(font, 10))
    search_entry.pack(side="left", padx=(0, 5))

    # Category filter
    category_var = tb.StringVar(value="All Categories")
    category_combo = tb.Combobox(filter_bar, textvariable=category_var, values=CATEGORIES, state="readonly", width=14)
    category_combo.pack(side="left", padx=(0, 5))

    # Sort
    sort_var = tb.StringVar(value="Newest")
    sort_combo = tb.Combobox(filter_bar, textvariable=sort_var, values=["Newest", "Updated"], state="readonly", width=10)
    sort_combo.pack(side="left", padx=(0, 5))

    # Search button
    search_btn = tb.Button(filter_bar, text="🔍", bootstyle="info", width=3)
    search_btn.pack(side="left", padx=(0, 10))

    # Results label
    results_label = tb.Label(filter_bar, text="", font=(font, 9))
    results_label.pack(side="left")

    # === SCROLLABLE AREA ===
    # Use a frame to contain canvas + scrollbar
    scroll_wrapper = tb.Frame(content)
    scroll_wrapper.pack(fill="both", expand=True, pady=(10, 0))

    # Canvas - use theme-aware background color
    theme_manager = get_theme_manager()
    colors = theme_manager.get_colors()
    canvas = tb.Canvas(scroll_wrapper, highlightthickness=0, bg=colors.get("bg", "#1a1a1a"))

    # Scrollbar
    vsb = tb.Scrollbar(scroll_wrapper, orient="vertical", command=canvas.yview)
    vsb.pack(side="right", fill="y")

    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=vsb.set)

    # Inner frame for content
    inner_frame = tb.Frame(canvas)

    # Create window in canvas - store the ID
    inner_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def update_scroll_region(event=None):
        """Update scroll region when inner frame changes size."""
        canvas.configure(scrollregion=canvas.bbox("all"))

    def update_canvas_width(event):
        """Make inner frame match canvas width."""
        canvas.itemconfig(inner_window, width=event.width)

    inner_frame.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", update_canvas_width)

    # Mouse wheel
    def on_wheel(event):
        if sys.platform == "darwin":
            canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_wheel_linux(event):
        canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    def bind_wheel():
        canvas.bind_all("<MouseWheel>", on_wheel)
        canvas.bind_all("<Button-4>", on_wheel_linux)
        canvas.bind_all("<Button-5>", on_wheel_linux)

    def unbind_wheel():
        try:
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
        except Exception:
            pass  # Widget may already be destroyed

    canvas.bind("<Enter>", lambda e: bind_wheel())
    canvas.bind("<Leave>", lambda e: unbind_wheel())

    def on_close():
        unbind_wheel()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    def clear_mods():
        for w in inner_frame.winfo_children():
            w.destroy()
        if hasattr(inner_frame, "_images"):
            inner_frame._images = []
        canvas.yview_moveto(0)
        window.update_idletasks()

    def show_msg(text):
        clear_mods()
        tb.Label(inner_frame, text=text, font=(font, 10)).pack(pady=20)
        window.update_idletasks()
        update_scroll_region()

    def filter_mods_by_category(mods, category):
        """Filter mods list by category."""
        if category == "All Categories":
            return mods
        return [m for m in mods if m.get("category", "").lower() == category.lower()]

    def display_mods(mods, append=False):
        """Display mods in the UI."""
        if not append:
            clear_mods()

        filtered = filter_mods_by_category(mods, state["category"])

        if not filtered and not append:
            show_msg("No mods found for this category")
            results_label.config(text="0 mods")
            return

        total_display = len(filter_mods_by_category(state["all_mods"], state["category"]))
        results_label.config(text=f"{total_display} mods")

        for mod in filtered:
            render_mod_card(inner_frame, mod, mods_dir=mods_dir, on_download_complete=on_download_complete)

        # Load more button
        if state["has_more"]:
            def load_next():
                load_more_btn.destroy()
                load_mods(page=state["page"] + 1, append=True)

            load_more_btn = tb.Button(
                inner_frame,
                text="⬇ Load More Mods...",
                bootstyle="success",
                command=load_next,
                cursor="hand2"
            )
            load_more_btn.pack(pady=20, ipadx=20, ipady=5)

        # Force scroll region update
        window.update_idletasks()
        update_scroll_region()

    def load_mods(search=None, sort="new", page=1, append=False):
        if state["loading"]:
            return

        state["loading"] = True
        state["page"] = page
        state["search"] = search
        state["sort"] = sort

        if not append:
            state["all_mods"] = []
            show_msg("Loading mods...")

        def fetch():
            try:
                sort_key = "new" if sort == "Newest" else "updated"
                mods, total, has_more = fetch_soh_mods(
                    page=page,
                    per_page=50,  # Load more per page
                    sort=sort_key,
                    search=search if search else None
                )

                state["has_more"] = has_more

                if append:
                    state["all_mods"].extend(mods)
                else:
                    state["all_mods"] = mods

                def update_ui():
                    display_mods(mods, append=append)
                    state["loading"] = False

                window.after(0, update_ui)

            except Exception as e:
                print(f"[Downloader] Error: {e}")
                window.after(0, lambda: show_msg(f"Error: {e}"))
                state["loading"] = False

        threading.Thread(target=fetch, daemon=True).start()

    def on_search(event=None):
        if state["source"] == "Gamebanana":
            search = search_var.get().strip()
            state["category"] = category_var.get()
            load_mods(search=search if search else None, sort=sort_var.get(), page=1)

    def on_category_change(event=None):
        """Re-filter displayed mods when category changes."""
        if state["source"] == "Gamebanana" and state["all_mods"]:
            state["category"] = category_var.get()
            display_mods(state["all_mods"], append=False)

    search_btn.config(command=on_search)
    search_entry.bind("<Return>", on_search)
    sort_combo.bind("<<ComboboxSelected>>", on_search)
    category_combo.bind("<<ComboboxSelected>>", on_category_change)

    def select_source(name):
        for src, btn in source_buttons.items():
            btn.config(bootstyle="success" if src == name else "secondary")

        state["source"] = name
        search_var.set("")
        category_var.set("All Categories")
        state["category"] = "All Categories"
        results_label.config(text="")

        if name == "Gamebanana":
            filter_bar.pack(fill="x", pady=(0, 5))
            load_mods(sort="Newest", page=1)
        else:
            filter_bar.pack_forget()
            show_msg(f"{name} - coming soon")

    # Source buttons
    for name in ["Gamebanana", "Thunderstore"]:
        logo = logos.get(name)
        if logo:
            btn = tb.Button(sidebar, image=logo, bootstyle="secondary", cursor="hand2",
                           command=lambda s=name: select_source(s))
            btn.image = logo
            btn.pack(pady=5)
            ToolTip(btn, name)
            source_buttons[name] = btn

    filter_bar.pack_forget()
    show_msg("Select a mod source to browse")

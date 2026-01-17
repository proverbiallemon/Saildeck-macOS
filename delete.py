import os
from tkinter import messagebox
from send2trash import send2trash

def delete_mod(path, refresh_callback=None, status_callback=None):
    """
    Delete the given mod or folder, with confirmation.
    refresh_callback: function to call to refresh the UI after deletion
    status_callback: function to update the status (e.g., lambda text: window.status_var.set(text))
    """
    if not os.path.exists(path):
        messagebox.showerror("Error", f"The path does not exist:\n{path}")
        if status_callback:
            status_callback(f"❌ Path does not exist: {path}")
        return False

    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{os.path.basename(path)}'?")
    if not confirm:
        if status_callback:
            status_callback("⚠️ Deletion cancelled.")
        return False

    try:
        send2trash(path)
        if status_callback:
            status_callback(f"✅ Deleted '{os.path.basename(path)}'")
        if refresh_callback:
            refresh_callback()
        return True
    except Exception as e:
        if status_callback:
            status_callback(f"❌ Failed to delete: {e}")
        messagebox.showerror("Error", f"Failed to delete:\n{e}")
        return False

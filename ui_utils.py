# ui_utils.py

import tkinter as tk
from tkinter import colorchooser, font

def pick_color():
    """Open a color chooser and return hex code."""
    c = colorchooser.askcolor(title="Choose color")
    return c[1]

def pick_font(root):
    """Return first available font family."""
    families = list(font.families(root))
    return families[0] if families else "Arial"

def enable_drag_drop(widget, callback):
    """
    Try to enable drag & drop. Requires tkinterDnD2 (TkDND).
    If not supported, prints a warning and does nothing.
    """
    try:
        widget.drop_target_register('DND_Files')
        widget.dnd_bind('<<Drop>>', lambda e: _on_drop(e, callback))
    except Exception as e:
        print(f"[ui_utils] Drag & drop not supported ({e}). Install tkinterDnD2 for this feature.")

def _on_drop(event, callback):
    """Internal: parse dropped files and invoke callback."""
    files = event.widget.tk.splitlist(event.data)
    callback(files)

def apply_dark_mode(root, widgets):
    """Apply dark theme."""
    bg, fg = "#1e1e1e", "#ffffff"
    root.configure(bg=bg)
    for w in widgets:
        try: w.configure(bg=bg, fg=fg)
        except tk.TclError: pass

def apply_light_mode(root, widgets):
    """Apply light theme."""
    bg, fg = "#f0f0f0", "#000000"
    root.configure(bg=bg)
    for w in widgets:
        try: w.configure(bg=bg, fg=fg)
        except tk.TclError: pass


def rgb_to_hex(rgb):
    """Convert an (R, G, B) tuple to a Tkinter-friendly '#rrggbb' string."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

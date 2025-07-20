import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import Tk, DND_FILES
from PIL import Image, ImageTk

from config import (
    DEFAULT_FONT_PATH, DEFAULT_FONT_SIZE,
    DEFAULT_OPACITY, DEFAULT_POSITION,
    DEFAULT_WATERMARK_COLOR
)
from watermark import add_text_watermark, add_logo_watermark, apply_text_watermark_to_image
from ui_utils import enable_drag_drop, apply_dark_mode, apply_light_mode, rgb_to_hex
from undo_redo import UndoRedoManager



class WatermarkApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermark App")
        self.geometry("800x600")
        self.image_path = None
        self.logo_path = None
        self.state = UndoRedoManager()
        self._build_ui()

    def on_start_drag(self, event):
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def on_drag(self, event):
       dx = event.x - self._drag_data['x']
       dy = event.y - self._drag_data['y']
       self.canvas.move(self.watermark_item, dx, dy)
       self._drag_data['x'] = event.x
       self._drag_data['y'] = event.y

    def _build_ui(self):
        # --- Canvas para sa image + draggable watermark ---
        self.canvas = tk.Canvas(self, width=600, height=400, bg='lightgray')
        self.canvas.pack(pady=10)

        self.watermark_item = None
        self._drag_data = {'x': 0, 'y': 0}

        # enable DND sa Canvas
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', lambda e: self.open_image(e.data))

        # placeholders for item IDs
        self.bg_img_item = None
        self.watermark_item = None
        self._drag_data = {'x': 0, 'y': 0}

        # Controls
        ctrl = tk.Frame(self)
        ctrl.pack(pady=5)
        tk.Button(ctrl, text="Open Image", command=self.open_image).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="Undo", command=self.undo).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="Redo", command=self.redo).pack(side=tk.LEFT, padx=5)

        # Text watermark
        self.entry = tk.Entry(self, width=40)
        self.entry.insert(0, "Watermark text")
        self.entry.pack(pady=5)
        tk.Button(self, text="Add Text Watermark", command=self.add_text).pack(pady=5)

        # Logo watermark
        tk.Button(self, text="Upload Logo", command=self.upload_logo).pack(pady=5)
        tk.Button(self, text="Add Logo Watermark", command=self.add_logo).pack(pady=5)

        # Theme toggle
        theme = tk.Frame(self)
        theme.pack(pady=5)
        tk.Button(theme, text="Dark Mode",
                  command=lambda: apply_dark_mode(self, [self.lbl_image, self.entry])
                 ).pack(side=tk.LEFT, padx=5)
        tk.Button(theme, text="Light Mode",
                  command=lambda: apply_light_mode(self, [self.lbl_image, self.entry])
                 ).pack(side=tk.LEFT, padx=5)

    def open_image(self, path=None):
        # 1) If called via DND, strip the “{…}” wrapper
        if path and path.startswith("{") and path.endswith("}"):
            path = path[1:-1]

        # 2) Otherwise show file dialog
        if not path:
            path = filedialog.askopenfilename(
                filetypes=[("Images", "*.jpg *.jpeg *.png")]
            )
        if not path:
            return

        # 3) Load & thumbnail the PIL image
        self.image_path = path
        pil = Image.open(path)
        pil.thumbnail((600, 400), resample=Image.Resampling.LANCZOS)
        self.current_img = pil

        # 4) Clear canvas and draw background
        self.canvas.delete("all")
        self.tk_img = ImageTk.PhotoImage(pil)
        self.bg_img_item = self.canvas.create_image(
            0, 0, anchor="nw", image=self.tk_img
        )

        # 5) Reset watermark placeholder
        self.watermark_item = None

    def _refresh(self, out):
        img = Image.open(out)
        img.thumbnail((600, 400))
        self.current_img = img.copy()
        self.state.add_state(self.current_img.copy())
        self.img_tk = ImageTk.PhotoImage(img)
        self.lbl_image.config(image=self.img_tk)
        messagebox.showinfo("Saved", f"File saved to:\n{out}")

    def add_text(self):
        # 1) Ensure image loaded
        if not getattr(self, "current_img", None):
            messagebox.showerror("Error", "Load image first!")
            return

        # 2) Remove old watermark
        if self.watermark_item:
            self.canvas.delete(self.watermark_item)

        # 3) Get text
        txt = self.entry.get().strip()
        if not txt:
            messagebox.showerror("Error", "Enter watermark text!")
            return

        # 4) Default position
        x = self.canvas.winfo_width() // 2
        y = self.canvas.winfo_height() - 30

        # 5) Create text item with hex color
        color_hex = rgb_to_hex(DEFAULT_WATERMARK_COLOR)
        self.watermark_item = self.canvas.create_text(
            x, y,
            text=txt,
            font=("Arial", DEFAULT_FONT_SIZE),
            fill=color_hex,
            tags="watermark"
        )

        # 6) Bind drag events
        self.canvas.tag_bind("watermark", "<Button-1>", self.on_start_drag)
        self.canvas.tag_bind("watermark", "<B1-Motion>", self.on_drag)


    def upload_logo(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images","*.png *.jpg *.jpeg")]
        )
        if path:
            self.logo_path = path

    def add_logo(self):
        # 1) Must have both base image & logo
        if not getattr(self, "current_img", None) or not getattr(self, "logo_path", None):
            messagebox.showerror("Error", "Load image & logo first!")
            return

        # 2) Remove old watermark
        if self.watermark_item:
            self.canvas.delete(self.watermark_item)

        # 3) Load, scale, convert logo
        logo = Image.open(self.logo_path).convert("RGBA")
        max_w = int(self.current_img.width * 0.1)
        ratio = logo.height / logo.width
        logo = logo.resize(
            (max_w, int(max_w * ratio)),
            resample=Image.Resampling.LANCZOS
        )
        self.logo_tk = ImageTk.PhotoImage(logo)

        # 4) Default position: bottom-left
        x = 10
        y = self.canvas.winfo_height() - logo.height - 10

        self.watermark_item = self.canvas.create_image(
            x, y, anchor="nw", image=self.logo_tk, tags="watermark"
        )

        # 5) Bind dragging
        self.canvas.tag_bind("watermark", "<Button-1>", self.on_start_drag)
        self.canvas.tag_bind("watermark", "<B1-Motion>", self.on_drag)

    def undo(self):
        img = self.state.undo()
        if img:
            self.img_tk = ImageTk.PhotoImage(img)
            self.lbl_image.config(image=self.img_tk)

    def redo(self):
        img = self.state.redo()
        if img:
            self.img_tk = ImageTk.PhotoImage(img)
            self.lbl_image.config(image=self.img_tk)


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()

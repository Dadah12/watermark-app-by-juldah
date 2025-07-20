import os
BASE = os.path.dirname(__file__)

EFAULT_FONT_PATH = None  # Put path to a TTF font in assets/fonts if you want custom font
DEFAULT_FONT_SIZE = 36
DEFAULT_WATERMARK_COLOR = (255, 255, 255)  # white
DEFAULT_OPACITY = 128  # 0-255
DEFAULT_POSITION = "bottom_right"
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]
DEFAULT_FONT_PATH = os.path.join(BASE, "assets/fonts/Inter/static/Inter-VariableFont_opsz,wght.ttf")
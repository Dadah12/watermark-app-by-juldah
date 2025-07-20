# watermark.py

from PIL import Image, ImageDraw, ImageFont
import os


def add_text_watermark(
    image_path: str,
    text: str,
    output_path: str,
    position: str = 'bottom_right',
    font_path: str = None,
    font_size: int = 36,
    color: tuple = (255, 255, 255),
    opacity: int = 128,
    margin: int = 10
) -> None:
    """
    Add a text watermark to an image.

    :param image_path:    path to input image
    :param text:          watermark text
    :param output_path:   where to save watermarked image
    :param position:      'bottom_right', 'center', 'top_left'
    :param font_path:     path to .ttf font file or None for default
    :param font_size:     font size in points
    :param color:         text color as RGB tuple
    :param opacity:       0-255 watermark opacity
    :param margin:        space from the edges in pixels
    """
    # open original image
    base = Image.open(image_path).convert('RGBA')
    w, h = base.size

    # create transparent layer for text
    txt_layer = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # load font
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # measure text size using textbbox (fix for Pillow without textsize)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # calculate coordinates
    if position == 'bottom_right':
        x = w - text_w - margin
        y = h - text_h - margin
    elif position == 'center':
        x = (w - text_w) // 2
        y = (h - text_h) // 2
    elif position == 'top_left':
        x = margin
        y = margin
    else:
        x = w - text_w - margin
        y = h - text_h - margin

    # draw text with opacity
    draw.text((x, y), text, fill=color + (opacity,), font=font)

    # merge layers and save
    merged = Image.alpha_composite(base, txt_layer)
    if merged.mode != 'RGB':
        merged = merged.convert('RGB')
    merged.save(output_path)



def _load_font(font_path, size):
    # Try custom font, else try common system fonts, else fallback default
    if font_path and os.path.isfile(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            pass
    for sysf in ("arial.ttf", "Calibri.ttf"):
        try:
            return ImageFont.truetype(sysf, size)
        except Exception:
            continue
    return ImageFont.load_default()


def apply_text_watermark_to_image(
    base_img: Image.Image,
    text: str,
    position: str = 'bottom_right',
    font_path: str = None,
    font_size: int = 36,
    color: tuple = (255, 255, 255),
    opacity: int = 128,
    margin: int = 10
) -> Image.Image:
    """
    Apply a text watermark directly on a PIL Image and return new Image.
    """
    base = base_img.convert('RGBA')
    w, h = base.size

    # create transparent layer
    txt_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)
    font = _load_font(font_path, font_size)

    # measure text
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # compute coords
    if position == 'center':
        x, y = (w - tw)//2, (h - th)//2
    elif position == 'top_left':
        x, y = margin, margin
    else:  # bottom_right default
        x, y = w - tw - margin, h - th - margin

    # draw text
    draw.text((x, y), text, fill=color + (opacity,), font=font)

    # merge and return
    merged = Image.alpha_composite(base, txt_layer)
    return merged.convert(base_img.mode)


def add_logo_watermark(
    image_path: str,
    logo_path: str,
    output_path: str,
    position: str = 'bottom_right',
    opacity: int = 128,
    scale: float = 0.1,
    margin: int = 10
) -> None:
    """
    Add a logo watermark to an image.

    :param image_path:  path to input image
    :param logo_path:   path to watermark logo (PNG with alpha)
    :param output_path: where to save watermarked image
    :param position:    'bottom_right', 'center', 'top_left'
    :param opacity:     0-255 watermark opacity
    :param scale:       logo width relative to image width (0 < scale ≤ 1)
    :param margin:      space from edges in pixels
    """
    # open base image
    base = Image.open(image_path).convert('RGBA')
    w, h = base.size

    # open and scale logo
    logo = Image.open(logo_path).convert('RGBA')
    max_w = int(w * scale)
    ratio = logo.height / logo.width
    llogo = logo.resize(
    (max_w, int(max_w * ratio)),
    resample=Image.Resampling.LANCZOS
)

    # apply opacity
    if opacity < 255:
        alpha = logo.split()[3].point(lambda p: p * (opacity / 255))
        logo.putalpha(alpha)

    lw, lh = logo.size

    # calculate coordinates
    if position == 'bottom_right':
        x = w - lw - margin
        y = h - lh - margin
    elif position == 'center':
        x = (w - lw) // 2
        y = (h - lh) // 2
    elif position == 'top_left':
        x = margin
        y = margin
    else:
        x = w - lw - margin
        y = h - lh - margin

    # merge logo onto transparent layer
    layer = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    layer.paste(logo, (x, y), logo)

    # composite and save
    merged = Image.alpha_composite(base, layer)
    if merged.mode != 'RGB':
        merged = merged.convert('RGB')
    merged.save(output_path)

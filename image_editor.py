# image_editor.py

from PIL import Image, ImageOps

def load_image(path):
    """
    Load an image from the given file path.
    :param path: Path to the image file.
    :return: PIL Image object.
    """
    return Image.open(path)

def save_image(img, path, format=None, quality=95):
    """
    Save a PIL Image object to the specified path.
    :param img: PIL Image object.
    :param path: Output file path.
    :param format: Optional format override (e.g., 'JPEG', 'PNG').
    :param quality: For lossy formats (JPEG), quality from 1 (worst) to 95 (best).
    """
    params = {}
    if quality and path.lower().endswith(('.jpg', '.jpeg')):
        params['quality'] = quality
        params['optimize'] = True
    img.save(path, format=format, **params)

def resize_image(img, width=None, height=None, keep_aspect_ratio=True):
    """
    Resize the image to the given width and/or height.
    If keep_aspect_ratio is True, scale proportionally.
    :param img: PIL Image object.
    :param width: Desired width in pixels.
    :param height: Desired height in pixels.
    :param keep_aspect_ratio: Preserve original aspect ratio.
    :return: Resized PIL Image object.
    """
    orig_w, orig_h = img.size
    if keep_aspect_ratio:
        if width and not height:
            ratio = width / orig_w
            height = int(orig_h * ratio)
        elif height and not width:
            ratio = height / orig_h
            width = int(orig_w * ratio)
        elif not width and not height:
            return img.copy()
    else:
        if not (width and height):
            return img.copy()

    return img.resize((width, height), Image.ANTIALIAS)

def crop_image(img, left, upper, right, lower):
    """
    Crop the image using the specified box coordinates.
    :param img: PIL Image object.
    :param left: Left pixel coordinate.
    :param upper: Upper pixel coordinate.
    :param right: Right pixel coordinate.
    :param lower: Lower pixel coordinate.
    :return: Cropped PIL Image object.
    """
    return img.crop((left, upper, right, lower))

def rotate_image(img, angle, expand=True):
    """
    Rotate the image by the given angle.
    :param img: PIL Image object.
    :param angle: Rotation angle in degrees (counter-clockwise).
    :param expand: If True, expands output image to fit the rotated image.
    :return: Rotated PIL Image object.
    """
    return img.rotate(angle, expand=expand)

def flip_horizontal(img):
    """
    Flip the image horizontally (mirror).
    :param img: PIL Image object.
    :return: Flipped PIL Image object.
    """
    return ImageOps.mirror(img)

def flip_vertical(img):
    """
    Flip the image vertically (upside-down).
    :param img: PIL Image object.
    :return: Flipped PIL Image object.
    """
    return ImageOps.flip(img)

def convert_to_grayscale(img):
    """
    Convert the image to grayscale mode.
    :param img: PIL Image object.
    :return: Grayscaled PIL Image object.
    """
    return img.convert('L')

def convert_format(input_path, output_path, format):
    """
    Open an image and save it in a different format.
    :param input_path: Path to the source image.
    :param output_path: Path for the converted image.
    :param format: Target format string (e.g., 'JPEG', 'PNG').
    """
    with Image.open(input_path) as img:
        img.save(output_path, format=format)

def compress_image(input_path, output_path, quality=85):
    """
    Compress a JPEG image by saving it with lower quality.
    :param input_path: Path to the source JPEG image.
    :param output_path: Path for the compressed image.
    :param quality: JPEG quality (1-95).
    """
    with Image.open(input_path) as img:
        img.save(output_path, quality=quality, optimize=True)

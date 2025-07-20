import os
from watermark import add_text_watermark, add_logo_watermark

def batch_process(
    images: list,
    output_dir: str,
    watermark_type: str = "text",
    watermark_content: str = None,
    logo_path: str = None,
    position: str = None,
    opacity: int = None,
    font_path: str = None,
    font_size: int = None,
    color: tuple = None,
    scale: float = None,
    progress_callback: callable = None
) -> list:
    """
    Apply watermark to multiple images in a batch.

    :param images: list of input image file paths
    :param output_dir: directory to save watermarked images
    :param watermark_type: "text" or "logo"
    :param watermark_content: text for text watermark
    :param logo_path: path to logo file for logo watermark
    :param position: watermark position (e.g., 'bottom_right', 'center')
    :param opacity: watermark opacity (0-255)
    :param font_path: path to .ttf font file
    :param font_size: font size for text watermark
    :param color: text color as (R, G, B) tuple
    :param scale: scale factor for logo relative to image width (0-1)
    :param progress_callback: optional fn(current_index, total) for progress updates
    :return: list of saved output file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    total = len(images)
    saved_files = []

    for idx, img_path in enumerate(images, start=1):
        name, ext = os.path.splitext(os.path.basename(img_path))
        output_path = os.path.join(output_dir, f"{name}_watermarked{ext}")

        try:
            if watermark_type == "text" and watermark_content:
                add_text_watermark(
                    img_path,
                    watermark_content,
                    output_path,
                    position=position,
                    opacity=opacity,
                    font_path=font_path,
                    font_size=font_size,
                    color=color
                )
            elif watermark_type == "logo" and logo_path:
                add_logo_watermark(
                    img_path,
                    logo_path,
                    output_path,
                    position=position,
                    opacity=opacity,
                    scale=scale
                )
            else:
                # Skip unsupported config
                continue

            saved_files.append(output_path)

        except Exception as e:
            # Log error and continue batch
            print(f"[batch_process] Error on {img_path}: {e}")

        if progress_callback:
            progress_callback(idx, total)

    return saved_files

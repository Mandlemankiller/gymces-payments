import cairosvg
from PIL import Image
from typing import *
from common import *
import os

BACKGROUND: Tuple[int, int, int] = (255, 255, 255)  # White


def gen_png(input_path: str) -> None:
    if not input_path.lower().endswith('.svg'):
        fatal('Input is not a svg!')

    if not os.path.exists(input_path):
        fatal('Input svg does not exist!')

    output_path: str = input_path[:-3] + 'png'

    cairosvg.svg2png(url=input_path, write_to=output_path)

    with Image.open(output_path) as img:
        new_img: Image = Image.new('RGBA', img.size, BACKGROUND)
        new_img.paste(img, (0, 0), img)
        new_img.save(output_path)

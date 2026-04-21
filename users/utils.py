import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from team_finder.constants import (
    AVATAR_DEFAULT_LETTER,
    AVATAR_FILENAME_TEMPLATE,
    AVATAR_FONT_SIZE,
    AVATAR_IMAGE_FORMAT,
    AVATAR_PALETTE,
    AVATAR_POSSIBLE_FONT_PATHS,
    AVATAR_RANDOM_MAX,
    AVATAR_RANDOM_MIN,
    AVATAR_SIZE,
    AVATAR_TEXT_BBOX_ANCHOR,
    AVATAR_TEXT_FILL,
    AVATAR_TEXT_Y_OFFSET,
)


def generate_avatar_file(letter: str):
    background = random.choice(AVATAR_PALETTE)
    image = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), background)
    draw = ImageDraw.Draw(image)

    font = None
    for font_path in AVATAR_POSSIBLE_FONT_PATHS:
        if font_path.exists():
            font = ImageFont.truetype(str(font_path), size=AVATAR_FONT_SIZE)
            break
    if font is None:
        font = ImageFont.load_default()

    letter = (letter or AVATAR_DEFAULT_LETTER)[0].upper()
    bbox = draw.textbbox(AVATAR_TEXT_BBOX_ANCHOR, letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (AVATAR_SIZE - text_width) / 2
    y = (AVATAR_SIZE - text_height) / 2 - AVATAR_TEXT_Y_OFFSET
    draw.text((x, y), letter, fill=AVATAR_TEXT_FILL, font=font)

    buffer = io.BytesIO()
    image.save(buffer, format=AVATAR_IMAGE_FORMAT)
    return ContentFile(
        buffer.getvalue(),
        name=AVATAR_FILENAME_TEMPLATE.format(random.randint(AVATAR_RANDOM_MIN, AVATAR_RANDOM_MAX)),
    )

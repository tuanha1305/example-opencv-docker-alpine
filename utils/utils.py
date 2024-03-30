import hashlib
import io

import numpy as np
import logging
import os
import random
import string

import cv2
import filetype
import base64
from PIL import Image
from io import BytesIO

_logger = logging.getLogger(__name__)


def is_valid_base64_image(base64_string):
    try:
        # Decode the base64 string
        image_data = base64.b64decode(base64_string)
        # Attempt to open the image
        image = Image.open(BytesIO(image_data))
        # If the above line didn't raise an exception, it's likely a valid image
        image.verify()  # Verify the image integrity. Optional, but recommended.
        return True
    except Exception as e:
        # If an error occurs, it's not a valid image or base64 string
        _logger.error('is_valid_base64_image', e)
        return False


def is_image(file_path):
    try:
        return filetype.is_image(file_path)
    except Exception as e:
        _logger.error('is_image error', str(e))
    return False


def get_image_dimension(file_path):
    if not os.path.exists(file_path) or not is_image(file_path):
        return 0, 0
    im = cv2.imread(file_path)
    h, w, _ = im.shape
    return w, h


def pad_or_truncate_string(s):
    if len(s) > 16:
        # Truncate string to 16 characters
        return s[:16]
    else:
        # Pad string with zeros up to 16 characters
        return s.ljust(16, '0')


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def sha1(content):
    sha1_hash = hashlib.sha1(content.encode()).hexdigest()
    return sha1_hash


def get_middle_padded_string(s):
    if len(s) < 16:
        padding_len = 16 - len(s)
        padding_left = padding_len // 2
        padding_right = padding_len - padding_left
        padded_string = (s[:len(s) // 2] + s[len(s) // 2] + ' ' * padding_left + ' ' * padding_right)[:16]
    else:
        padded_string = s[len(s) // 2 - 8:len(s) // 2 + 8]
    return padded_string


def verify(check_sum, app_id, app_secret, key_tool, package, time_stamp) -> bool:
    real_key = get_middle_padded_string(app_id)
    real_iv_key = get_middle_padded_string(app_secret)

    key_tool_hash = sha1(f'{key_tool}@{time_stamp}')

    content = f'{real_iv_key}/{real_key}/{key_tool_hash}/{package}/{time_stamp}'

    hash_check = sha1(content)
    _logger.info(f'hash_check: {hash_check} - check_sum: {check_sum} - content: {content}')
    return True if check_sum == hash_check else False


def get_name_and_ext_file(path_file):
    if not os.path.exists(path_file):
        logging.info(f"File {path_file} does not exist.")
        return None, None
    file_name, file_extension = os.path.splitext(os.path.basename(path_file))
    file_extension = file_extension[1:]
    return file_name, file_extension


def is_valid_request_data(data):
    if not data:
        return False, 'Invalid JSON structure.'
    if 'b64_img' not in data or not is_valid_base64_image(data['b64_img']):
        return False, 'Invalid image base 64 encoded data.'
    if 'strokes' not in data or not isinstance(data['strokes'], list):
        return False, 'Invalid strokes format or missing strokes.'
    return True, ''


def resize_image_base64(b64_str, ratio):
    # Decode base64 to bytes
    img_data = base64.b64decode(b64_str)

    # Open the image from bytes data
    img = Image.open(BytesIO(img_data))

    original_width, original_height = img.size

    # Calculate new size
    new_height = int(original_width / ratio)

    # Resize image
    resized_img = img.resize((original_width, new_height), Image.Resampling.LANCZOS)

    # Save the resized image to a bytes buffer
    buffer = BytesIO()
    resized_img.save(buffer, format="PNG")

    # Encode bytes to base64
    resized_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return resized_base64


def get_image_dimensions(base64_image):
    """
    Decode a base64 image and return its dimensions (width, height).
    """
    img_data = base64.b64decode(base64_image)
    img = Image.open(io.BytesIO(img_data))
    return img.width, img.height

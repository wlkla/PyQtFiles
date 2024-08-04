#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegraph Image Uploader

This script compresses and uploads a single image to the Telegraph image hosting service.
Usage: python main.py <image_path>

Author: lkl
Date: 2024/8/4
"""

import io
import os
import sys
import requests
import mimetypes
from PIL import Image

# Constants
QUALITY_STEP = 5
MIN_QUALITY = 65
INITIAL_QUALITY = 85
MAX_DIMENSION = 1920
TARGET_SIZE = 5 * 1024 * 1024  # 5 MB
UPLOAD_URL = 'https://telegraph-image-6b4.pages.dev/upload'


def compress_image(file_path, target_size=TARGET_SIZE, quality=INITIAL_QUALITY,
                   min_quality=MIN_QUALITY, step=QUALITY_STEP):
    """
    Compress an image file to a target size.

    Args:
        file_path (str): Path to the original image file.
        target_size (int): Desired file size in bytes.
        quality (int): Initial quality setting for compression.
        min_quality (int): Minimum acceptable quality.
        step (int): Step size for quality reduction in each iteration.

    Returns:
        str: Path to the compressed image file.
    """
    original_size = os.path.getsize(file_path)

    if original_size <= target_size:
        return file_path

    with Image.open(file_path) as img:
        # Convert image to RGB if it has an alpha channel
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGB')

        # Resize image if it's too large
        if max(img.size) > MAX_DIMENSION:
            img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)

        temp_path = os.path.join(os.path.dirname(file_path), f"compressed_{os.path.basename(file_path)}")
        format = 'JPEG' if img.format in ['JPEG', 'JPG'] else 'PNG'

        while quality >= min_quality:
            buffer = io.BytesIO()
            img.save(buffer, format=format, quality=quality, optimize=True)
            if buffer.tell() <= target_size:
                with open(temp_path, 'wb') as f:
                    f.write(buffer.getvalue())
                return temp_path
            quality -= step

    # If target size not achieved, save with minimum quality
    buffer.seek(0)
    with open(temp_path, 'wb') as f:
        f.write(buffer.getvalue())
    return temp_path


def upload_image_to_telegraph(file_path):
    """
    Upload an image to Telegraph image hosting service.

    Args:
        file_path (str): Path to the image file to be uploaded.

    Returns:
        str or None: URL of the uploaded image if successful, None otherwise.
    """
    file_path = compress_image(file_path)
    mime_type = mimetypes.guess_type(file_path)[0]

    with open(file_path, 'rb') as file:
        try:
            response = requests.post(UPLOAD_URL, files={'file': (file_path, file, mime_type)})
            if response.status_code == 200:
                return UPLOAD_URL[:-7] + response.json()[0]['src']
            else:
                return None
        except requests.RequestException as e:
            return None


def main():
    """
    Main function to handle command-line arguments and initiate the upload process.
    """
    if len(sys.argv) < 2:
        sys.exit(1)

    image_paths = sys.argv[1:]

    for image_path in image_paths:
        if not os.path.exists(image_path):
            continue

        result = upload_image_to_telegraph(image_path)
        if result:
            print(result)


if __name__ == "__main__":
    main()

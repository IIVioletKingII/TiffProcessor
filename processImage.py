import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, UnidentifiedImageError
import tifffile
import sys
import os
import json

verbosity = False

USAGE = """Usage:
   python read_qr.py <input_tiff_path> <output_tiff_path>
optional:
   -v (fore verbosity prints)
   --retrieve-qr (return qr code positions in json)
"""


def apply_median_filter(image, kernel_size=30):
    return cv2.medianBlur(image, kernel_size)


def read_qr_from_image(image):
    decoded_objects = decode(image)
    if not decoded_objects:
        return_result({
            "success": False,
            "error": "No QR code found."
        })
        sys.exit(1)

    # Select the object with the highest top rect value (max y-coordinate)
    selected_obj = min(decoded_objects, key=lambda obj: obj.rect.top)
    if verbosity:
        print(f'Decoded QR Code: {selected_obj.data.decode("utf-8")}')
    return selected_obj.data.decode("utf-8")


def return_result(object: object):
    print(json.dumps(object))


def main():
    if len(sys.argv) < 3:
        return_result({
            "success": False,
            "error": USAGE
        })
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    verbosity = '-v' in sys.argv
    find_qrcode = '--retrieve-qr' in sys.argv

    # Validate input
    if not os.path.exists(input_path):
        return_result({
            "success": False,
            "error": f"Error: File not found at {input_path}"
        })
        sys.exit(1)

    # Load image using Pillow
    try:
        pil_image = Image.open(input_path).convert("RGB")
    except (UnidentifiedImageError, IOError) as e:
        return_result({
            "success": False,
            "error": f"Error loading image: {e}"
        })
        sys.exit(1)

    try:
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        return_result({
            "success": False,
            "error": f"Error converting image: {e}"
        })
        sys.exit(1)

    # Apply median filter
    filtered_image = apply_median_filter(cv_image, kernel_size=3)

    # Try reading QR code
    read_text = read_qr_from_image(filtered_image) if find_qrcode else ''

    # Convert filtered image back to PIL and save
    # output_pil_image = Image.fromarray(
    #     cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)
    # )

    # Convert back to RGB for saving
    filtered_rgb = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)

    try:
        # output_pil_image.save(output_path, format='TIFF')
        tifffile.imwrite(output_path, filtered_rgb, compression='lzw')
    except IOError as e:
        return_result({
            "success": False,
            "error": f"Error saving output image: {e}"
        })
        sys.exit(1)

    if verbosity:
        print(f"Filtered image saved to: {output_path}")

    return_result({
        "success": True,
        "text": read_text
    })


if __name__ == "__main__":
    main()

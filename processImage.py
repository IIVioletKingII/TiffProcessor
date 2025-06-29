import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_path
import tifffile
import sys
import os
import json

verbosity = False

USAGE = """Usage:
   processimage clean <input_tiff_path> <output_tiff_path>
optional:
   -v (fore verbosity prints)
   --retrieve-qr (return qr code positions in json)

   processimage convert <input_tiff_path>
optional:
   -v (fore verbosity prints)
"""


def return_result(object: object):
    print(json.dumps(object))


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


def clean(input_path, output_path, find_qrcode=False):

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


def convert(input_path):
    # if getattr(sys, 'frozen', False):
    #     base_path = sys._MEIPASS  # type: ignore[attr-defined]
    # else:
    #     base_path = os.path.dirname(__file__)
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))

    poppler_path = os.path.join(base_path, 'poppler', 'bin')

    images = convert_from_path(
        input_path,
        dpi=300,
        poppler_path=poppler_path
    )
    base_name, _ = os.path.splitext(input_path)

    # Save all pages as separate TIFFs or as a multipage TIFF
    for i, img in enumerate(images):
        img.save(f'{base_name}_{i+1}.tif', format='TIFF')

    return_result({
        "success": True,
        "text": f'Converted {len(images)} pages.'
    })


def validate_path(path):
    if not os.path.exists(path):
        return_result({
            "success": False,
            "error": f"Error: File not found at {path}"
        })
        sys.exit(1)


def main():
    global verbosity

    if len(sys.argv) < 3:
        return_result({
            "success": False,
            "error": USAGE
        })
        sys.exit(1)

    function = sys.argv[1]
    input_path = sys.argv[2]
    verbosity = '-v' in sys.argv
    find_qrcode = '--retrieve-qr' in sys.argv

    # Validate input
    if function == 'clean' and len(sys.argv) >= 4:
        validate_path(input_path)
        clean(input_path, sys.argv[3], find_qrcode)
    elif function == 'convert' and len(sys.argv) >= 3:
        validate_path(input_path)
        convert(input_path)
    else:
        return_result({
            "success": False,
            "error": USAGE
        })
        sys.exit(1)


if __name__ == "__main__":
    main()

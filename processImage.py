import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import sys
import os


def apply_median_filter(image, radius=3):
    # kernel_size = 2 * radius + 1
    kernel_size = radius
    return cv2.medianBlur(image, kernel_size)


def read_qr_from_image(image):
    decoded_objects = decode(image)
    if not decoded_objects:
        print('No QR code found.')
    for obj in decoded_objects:
        print(f'Decoded QR Code: {obj.data.decode("utf-8")}')


def main():
    if len(sys.argv) != 3:
        print("Usage: python read_qr.py <input_tiff_path> <output_tiff_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Validate input
    if not os.path.exists(input_path):
        print(f"Error: File not found at {input_path}")
        sys.exit(1)

    # Load image using Pillow
    pil_image = Image.open(input_path)
    pil_image = pil_image.convert("RGB")  # ensure consistent format
    cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Apply median filter
    filtered_image = apply_median_filter(cv_image, radius=3)

    # Try reading QR code
    read_qr_from_image(filtered_image)

    # Convert filtered image back to PIL and save
    output_pil_image = Image.fromarray(cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB))
    output_pil_image.save(output_path, format='TIFF')
    print(f"Filtered image saved to: {output_path}")


if __name__ == "__main__":
    main()

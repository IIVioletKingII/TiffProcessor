import subprocess

CLEAN_TEST = [
    'python',
    'processImage.py',
    'clean',
    'images/small.tif'
]
CONVERT_TEST = [
    'python',
    'processImage.py',
    'convert',
    'images/small.tif',
    'images/small_filtered.tif'
]

# Simulate running: python main_script.py arg1 arg2
result = subprocess.run(
    CONVERT_TEST,
    capture_output=True,
    text=True
)

print(result)

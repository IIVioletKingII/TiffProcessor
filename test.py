import subprocess

# Simulate running: python main_script.py arg1 arg2
result = subprocess.run(
    [
        'python',
        'processImage.py',
        'images/small.tif',
        'images/small_filtered.tif'
    ],
    capture_output=True,
    text=True
)

print(result)

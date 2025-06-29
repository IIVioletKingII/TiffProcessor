## Setup
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Download the poppler library from [poppler-windows](https://github.com/oschwartz10612/poppler-windows) and extract the bin, lib, etc under .poppler


## Install
```bash
pyinstaller processImage.spec
# pyinstaller --onefile --add-binary "venv\Lib\site-packages\pyzbar\libiconv.dll;pyzbar" --add-binary "venv\Lib\site-packages\pyzbar\libzbar-64.dll;pyzbar" processImage.py --icon=icons/tiff_blurred.png
```

## Runs
```bash
python processImage.py clean images/small.tif images/small_f.tif --retrieve-qr
python processImage.py clean images/large.tif images/large_f.tif --retrieve-qr

dist/processImage.py clean images/large.tif images/large_f.tif --retrieve-qr

```
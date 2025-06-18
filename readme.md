## Install
```bash
pyinstaller --onefile --add-binary "venv\Lib\site-packages\pyzbar\libiconv.dll;pyzbar" --add-binary "venv\Lib\site-packages\pyzbar\libzbar-64.dll;pyzbar" processImage.py --icon=tiff_blurred.png
```

## Runs
```bash
C:/Users/Sam/Downloads/TestTiff/venv/Scripts/python.exe c:/Users/Sam/Downloads/TestTiff/processImage.py images/small.tif images/small_f.tif --retrieve-qr
C:/Users/Sam/Downloads/TestTiff/venv/Scripts/python.exe c:/Users/Sam/Downloads/TestTiff/processImage.py images/large.tif images/large_f.tif --retrieve-qr
```
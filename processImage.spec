# -*- mode: python ; coding: utf-8 -*-
import os

# Collect pyzbar DLLs
binaries = [
    (os.path.abspath(os.path.join('venv310', 'Lib', 'site-packages', 'pyzbar', 'libiconv.dll')), 'pyzbar'),
    (os.path.abspath(os.path.join('venv310', 'Lib', 'site-packages', 'pyzbar', 'libzbar-64.dll')), 'pyzbar'),
]

# Add imagecodecs .pyd files
imagecodecs_dir = 'venv310\\Lib\\site-packages\\imagecodecs'
imagecodecs_binaries = [
    (os.path.join(imagecodecs_dir, f), 'imagecodecs')
    for f in os.listdir(imagecodecs_dir)
    if f.endswith('.pyd')
]
binaries += imagecodecs_binaries

# Add Opencv .pyd files
opencv_dir = 'venv310\\Lib\\site-packages\\cv2'
opencv_binaries = [
    (os.path.join(opencv_dir, f), 'cv2')
    for f in os.listdir(opencv_dir)
    if f.endswith('.pyd') or f.endswith('.dll')
]
binaries += opencv_binaries

# Add poppler/bin executables
poppler_bin_dir = 'poppler\\bin'
poppler_binaries = [
    (os.path.join(poppler_bin_dir, f), os.path.join('poppler', 'bin'))
    for f in os.listdir(poppler_bin_dir)
    if os.path.isfile(os.path.join(poppler_bin_dir, f))
]
binaries += poppler_binaries

binaries += [
    ('C:\\Program Files\\Microsoft Visual Studio\\2022\\Professional\\Common7\\IDE\\vcruntime140.dll', '.'),
    ('C:\\Program Files\\Microsoft Visual Studio\\2022\\Professional\\Common7\\IDE\\vcruntime140_1.dll', '.'),
    ('C:\\Program Files\\Microsoft Visual Studio\\2022\\Professional\\Common7\\IDE\\msvcp140.dll', '.'),
    ('C:\\Program Files\\Microsoft Visual Studio\\2022\\Professional\\Common7\\IDE\\concrt140.dll', '.'),
]

a = Analysis(
    ['processImage.py'],
    pathex=[],
    binaries=binaries,
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='processImage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ProcessImage_v1.4',
)

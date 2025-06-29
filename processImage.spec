# -*- mode: python ; coding: utf-8 -*-
import os

# Collect pyzbar DLLs
binaries = [
    ('venv\\Lib\\site-packages\\pyzbar\\libiconv.dll', 'pyzbar'),
    ('venv\\Lib\\site-packages\\pyzbar\\libzbar-64.dll', 'pyzbar'),
]

# Add imagecodecs .pyd files
imagecodecs_dir = 'venv\\Lib\\site-packages\\imagecodecs'
imagecodecs_binaries = [
    (os.path.join(imagecodecs_dir, f), 'imagecodecs')
    for f in os.listdir(imagecodecs_dir)
    if f.endswith('.pyd')
]
binaries += imagecodecs_binaries

# Add poppler/bin executables
poppler_bin_dir = 'poppler\\bin'
poppler_binaries = [
    (os.path.join(poppler_bin_dir, f), os.path.join('poppler', 'bin'))
    for f in os.listdir(poppler_bin_dir)
    if os.path.isfile(os.path.join(poppler_bin_dir, f))
]
binaries += poppler_binaries

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
    a.binaries,
    a.datas,
    [],
    name='processImage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons\\tiff_blurred.png',
)

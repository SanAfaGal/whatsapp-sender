# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Collect browser icons and configuration
browser_icons = collect_data_files('src', includes=['assets/*.png'])
browser_config = collect_data_files('src', includes=['config/*.json'])

a = Analysis(
    ['src/app.py'],
    pathex=[os.path.abspath(SPECPATH)],
    binaries=[],
    datas=[
        ('src/assets/icon.ico', 'assets'),
        ('src/config/browsers.json', 'config'),
        *browser_icons,  # Add all browser icons
        *browser_config  # Add browser configuration
    ],
    hiddenimports=[
        'playsound',
        'winreg',
        'json',
        'pyautogui',
        'PIL',
        'tkinter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WhatsApp Sender',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/assets/icon.ico'
)
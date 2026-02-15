# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_all

datas, binaries, existing_hiddenimports = collect_all('textual')
hiddenimports = existing_hiddenimports + ['pypresence', 'pylast', 'requests', 'termcolor', 'rich', 'rich._unicode_data.unicode17-0-0']

block_cipher = None

# Platform-specific icon selection
if sys.platform == 'win32':
    iconPath = 'icon/VLC.UTILS.ico'
elif sys.platform == 'darwin':
    iconPath = 'icon/VLC.UTILS.icns'
else:
    iconPath = 'icon/VLC.UTILS.png'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='VLC.UTILS',
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
    icon=iconPath,
)

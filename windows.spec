# -*- mode: python -*-

block_cipher = None

import os

# Instructions: Run PyInstaller this, move assets folder into folder with EXE

a = Analysis([os.path.join(os.getcwd(), 'Kessler-Syndrome', 'main.py')],
             pathex=[os.path.join(os.getcwd(), 'Kessler-Syndrome')],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['numpy', 'scipy', 'PIL'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Kessler.exe',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon=os.path.join(os.getcwd(), 'misc-data', 'kessler.ico'))

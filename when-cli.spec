# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.building.api import EXE, COLLECT, PYZ
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.osx import BUNDLE
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

extra_files = []
extra_folders = ["when/when/data"]
extra_pyinstaller_files = []

# Process the extra-files and folders
for file_item in extra_files:
    extra_pyinstaller_files.append((file_item, "."))

for folder_item in extra_folders:
    extra_pyinstaller_files.append((folder_item, folder_item))

extra_pyinstaller_files += collect_data_files('airportsdata')


a = Analysis(['when/when/__main__.py'],
             pathex=[],
             binaries=[],
             datas=extra_pyinstaller_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
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
          name='when-cli',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

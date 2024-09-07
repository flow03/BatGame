# -*- mode: python ; coding: utf-8 -*-
# from PyInstaller.utils.hooks import collect_data_files

# pyinstaller main.spec

datas_list = []
# datas += collect_data_files('img/*.png')
# datas += collect_data_files('img/bat/*.png')
# datas += collect_data_files('img/bg/*')
# datas += collect_data_files('img/spritesheets/*.png')
# datas += collect_data_files('fonts/*')

datas_list.append(('img/*.*', 'img/'))
datas_list.append(('img/bat/*.png', 'img/bat/'))
datas_list.append(('img/spritesheets/*.png', 'img/spritesheets/'))
datas_list.append(('img/bg/*', 'img/bg/'))
datas_list.append(('img/dummy/*.png', 'img/dummy/'))
datas_list.append(('fonts/*', 'fonts/'))
datas_list.append(('text/*.json', 'text/'))

# datas_list = [('img/*.png', 'img/'),('img/bat/*.png', 'img/bat/'),('img/bg/*', 'img/bg/'),('img/spritesheets/*.png', 'img/spritesheets/'),('fonts/*', 'fonts/')]

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas_list,
    hiddenimports=[],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['img/fangs.ico'],
)

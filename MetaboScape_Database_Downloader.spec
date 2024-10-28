# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MetaboScape_Database_Downloader.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('MetaboScape_Database_Downloader.py', '.'),
        ('README.md', '.'),
        ('LICENSE', '.'),
        ('third-party-licenses.txt', '.'),
        ('mdd', 'mdd'),
        ('mdd/target_lists/metaboscape_target_list_template.csv', 'target_lists')
    ],
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
    name='MetaboScape_Database_Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='.'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MetaboScape_Database_Downloader',
)

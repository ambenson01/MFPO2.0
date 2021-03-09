from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
	('Database.csv','.'),
	('mfpo.kv','.'),
	('UpdateRecord.txt','.'),
]

a = Analysis(['__main__.py'],
             pathex=['C:\\Users\\Brendon Hung\\PycharmProjects\\Scraper'],
             binaries=[],
             datas= added_files,
             hiddenimports=[],
             hookspath=[],
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
          [],
          exclude_binaries=True,
          name='MFPO2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('C:\\Users\Brendon Hung\PycharmProjects\\Scraper'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Scraper')

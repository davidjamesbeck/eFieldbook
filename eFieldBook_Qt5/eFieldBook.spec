# -*- mode: python -*-

block_cipher = None


a = Analysis(['eFieldBook.py'],
             pathex=['/Users/David/OpenSource/github/ELFB/eFieldBook_Qt5'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='eFieldbook',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='/Users/David/OpenSource/github/ELFB/eFieldBook_Qt5/ELFB.icns')

app = BUNDLE(exe,
             name='eFieldbook.app',
             icon='/Users/David/OpenSource/github/ELFB/eFieldBook_Qt5/ELFB.icns',
             bundle_identifier='com.ualberta.linguistics.eFieldbook')


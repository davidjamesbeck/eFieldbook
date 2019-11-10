# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/David/OpenSource/PyQt-gpl-5.5/QtBluetooth/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtCore/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtDBus/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtDesigner/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtGui/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtHelp/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtMacExtras/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtMultimedia/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtMultimediaWidgets/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtNetwork/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtNfc/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtOpenGL/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtPositioning/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtPrintSupport/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtQml/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtQuick/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtQuickWidgets/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtSensors/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtSerialPort/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtSql/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtSvg/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtTest/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtWebChannel/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtWebEngineWidgets/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtWebKit/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtWebKitWidgets/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtWebSockets/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtWidgets/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtXml/', '/Users/David/OpenSource/PyQt-gpl-5.5/QtXmlPatterns/', 'eFieldbook.spec'],
             pathex=['/Users/David/OpenSource/PyQt-gpl-5.5/Qt/', '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='')

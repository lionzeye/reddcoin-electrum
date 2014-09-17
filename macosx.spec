# -*- mode: python -*-
a = Analysis(['reddcoin-electrum'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Reddcoin Electrum',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='electrum.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Reddcoin Electrum')
app = BUNDLE(coll,
             name='Reddcoin Electrum.app',
             icon='electrum.icns')

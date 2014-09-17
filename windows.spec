# -*- mode: python -*-
a = Analysis(['reddcoin-electrum'])
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='reddcoin-electrum.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icons\\electrum.ico')

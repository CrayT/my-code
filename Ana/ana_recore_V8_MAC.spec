# -*- mode: python -*-

block_cipher = None


a = Analysis(['ana_recore_V8_MAC.py'],
             pathex=['/Users/xutao/Downloads/Python'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ana_recore_V8_MAC',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='ana_recore_V8_MAC.app',
             icon=None,
             bundle_identifier=None)

# -*- mode: python -*-

block_cipher = None


a = Analysis(['bwh.py'],
             pathex=['C:\\Projects\\BandwagongVPS_controller'],
             binaries=[],
             datas=[('C:\\Projects\\BandwagongVPS_controller\\final.ico', 'final.ico'),('C:\\Projects\\BandwagongVPS_controller\\zh_CN.qm','zh_CN.qm')],
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
          name='bwh',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )

# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

def collect_all_files(directory):
    data_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Skip ignored files based on .gitignore
            if any(root.startswith(ignore.strip('/')) for ignore in [
                'dist', 'build', 'venv', '.venv', '__pycache__'
            ]) or file.endswith(('.pyc', '.pyo', '.log')):
                continue
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, directory)
            data_files.append((full_path, relative_path))
    return data_files

# Collect additional data files
datas = collect_all_files('.')

# Collect hidden imports
hiddenimports = [
    'copy',
    'sys',
    'btcrseed',
    'btcrpass',
    'lib.bitcoinlib_mod.encoding',
    'lib.bitcoinlib.encoding',
    'lib.cashaddress.convert',
    'lib.cashaddress.base58',
    'lib.base58_tools.base58_tools',
    'lib.eth_hash.auto.keccak',
    'lib.pyzil.account',
    'lib.bech32',
    'lib.cardano.cardano_utils',
    'lib.stacks.c32',
    'lib.p2tr_helper.P2TR_tools',
    'multiprocessing',                      # Add multiprocessing
    'Crypto.Cipher._raw_ecb',               # Add raw_ecb module
    'Crypto.Cipher.ECB',                    # Ensure ECB mode is included
    'pycryptodome',                         # Add pycryptodome
    'pycryptodome.Cipher',                  # Add Cipher submodule
    'pycryptodome.Util',                    # Add Util submodule
    # Add any additional hidden imports here
]

a = Analysis(
    ['seedrecover.py'],
    pathex=['.'],  # Added current directory to pathex
    binaries=[
        ('/Users/rahulretnan/Projects/Playground/btcrecover/.venv/lib/python3.12/site-packages/Crypto/Cipher/_raw_ecb.abi3.so', 'Crypto/Cipher'),
        # Add paths to other required .so files if necessary
    ],
    datas=datas,  # Included all necessary project files
    hiddenimports=hiddenimports,  # Added hidden imports
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='seedrecover',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

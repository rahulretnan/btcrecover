# -*- mode: python ; coding: utf-8 -*-

import os
import sys
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

# Collect all files from the current directory
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

# Function to find .so files
def find_so_file(name):
    for root, dirs, files in os.walk('/usr/lib'):
        for file in files:
            if name in file and file.endswith('.so'):
                return os.path.join(root, file)
    return None

# Find the required .so files
hashlib_path = find_so_file('_hashlib')
ssl_path = find_so_file('_ssl')

# Prepare binaries list
binaries = []
if hashlib_path:
    binaries.append((hashlib_path, '.'))
if ssl_path:
    binaries.append((ssl_path, '.'))

a = Analysis(
    ['seedrecover.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
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
    codesign_identity=None,
    entitlements_file=None,
)

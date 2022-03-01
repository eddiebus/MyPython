"""Compiler for Top-Down Shooter"""

import PyInstaller.__main__

PyInstaller.__main__.run([
    "main.py",
    '--onefile',
    '--windowed',
    ]
                         )

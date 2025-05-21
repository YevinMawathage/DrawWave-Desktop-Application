# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('drawings.db', '.'),
    ('venv\Lib\site-packages\mediapipe\modules', 'mediapipe/modules'),
    ('virtual_painter.png', '.')],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtWidgets',
        'PyQt5.QtGui',
        'PyQt5.QtCore',
        'start_screen',
        'virtual_painter_gui',
        'canvas',
        'canvas_widget',
        'hand_tracking',
        'persistence',
        'utils',
        'mediapipe',
        'mediapipe.python',
        'mediapipe.python.solutions'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='Painter',
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
    icon='virtual_painter.png'
)


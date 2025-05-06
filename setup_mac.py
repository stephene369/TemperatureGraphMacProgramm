"""
Configuration pour créer un exécutable macOS avec py2app
"""
from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('assets', ['assets/icons']),
    ('output/exports', []),  # Dossier pour les exports de graphiques
    # Ajoutez ici tous les fichiers HTML, CSS et JS utilisés par WebView
    ('ui', ['ui']),
]

OPTIONS = {
    'argv_emulation': False,
    'arch': 'universal2',  # Pour compatibilité Intel et Apple Silicon
    'packages': ['PyQt5', 'matplotlib', 'pandas', 'numpy', 'PyQtWebEngine'],
    'includes': [
        'PyQt5.QtCore', 
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'PyQt5.QtWebEngineWidgets',  # Important pour WebView
        'matplotlib.backends.backend_qt5agg'
    ],
    'excludes': ['tkinter', 'PySide2', 'PyQt6', 'PySide6'],
    'iconfile': 'assets/icons/app_icon.icns',  # Assurez-vous que ce fichier existe
    'plist': {
        'CFBundleName': 'TemperatureGraph',
        'CFBundleDisplayName': 'TemperatureGraph',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.yourdomain.temperaturegraph',
        'NSHumanReadableCopyright': 'Copyright © 2023',
        'LSMinimumSystemVersion': '10.14.0',  # Compatibilité avec macOS Mojave et plus
        'NSHighResolutionCapable': True,
        'NSPrincipalClass': 'NSApplication',
        'NSAppTransportSecurity': {
            'NSAllowsArbitraryLoads': True  # Pour permettre le chargement de contenu web local
        },
    }
}

setup(
    name="TemperatureGraph",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
"""
Configuration pour créer un exécutable Windows avec cx_Freeze
"""
import sys
from cx_Freeze import setup, Executable

# Dépendances qui pourraient ne pas être détectées automatiquement
build_exe_options = {
    "packages": [
        "os", 
        "numpy", 
        "pandas", 
        "matplotlib", 
        "PyQt5",
        "PyQt5.QtWebEngineWidgets",  # Important pour WebView
        "matplotlib.backends.backend_qt5agg"
    ],
    "excludes": ["tkinter", "PySide2", "PyQt6", "PySide6"],
    "include_files": [
        ("assets/", "assets/"),
        ("output/exports/", "output/exports/"),
        # Inclure tout le dossier ui
        ("ui/", "ui/"),
    ],
    "include_msvcr": True,
}

# Base=None pour applications console, "Win32GUI" pour applications sans console
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="TemperatureGraph",
    version="1.0.0",
    description="Application d'analyse de température et d'humidité",
    author="Your Name",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py", 
            base=base,
            target_name="TemperatureGraph.exe",
            icon="assets/icons/app_icon.ico",
            copyright="Copyright © 2023",
        )
    ],
)
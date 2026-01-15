"""
ISCGraph - Application d'analyse de température et d'humidité
Point d'entrée principal de l'application
"""

import os
import sys
import webview
from pathlib import Path
from core.api import API


BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / "ui"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output" / "exports"
FRONTEND_BUILD_DIR = UI_DIR / "build"
INDEX_HTML = FRONTEND_BUILD_DIR / "index.html"


def get_pictures_dir() -> Path:
    # macOS / Windows: ~/Pictures ; Linux fallback: ~/Pictures or ~/Images
    home = Path.home()
    pics = home / "Pictures"
    if sys.platform.startswith("linux") and not pics.exists():
        pics = home / "Images"
    return pics


def main():
    pictures_dir = get_pictures_dir()

    # ✅ IMPORTANT: pas d'espace à la fin
    IMAGE_OUTPUT_DIR = pictures_dir / "ISCGraph"
    FILE_OUTPUT_DIR = pictures_dir / "Excels ISCGraph"

    # Create directories if they don't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FILE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not INDEX_HTML.exists():
        raise FileNotFoundError(f"index.html introuvable: {INDEX_HTML}")

    api = API(str(BASE_DIR), str(DATA_DIR), str(OUTPUT_DIR), str(IMAGE_OUTPUT_DIR), str(FILE_OUTPUT_DIR))

    # ✅ macOS: plus fiable en file://
    index_url = INDEX_HTML.as_uri()

    window = webview.create_window(
        title="ISCGraph",
        url=index_url,
        js_api=api,
        resizable=True,
        min_size=(800, 600),
        width=1200,
        height=800,
    )

    # ✅ Mac: évite les bidouilles Tkinter, laisse Cocoa gérer l'event loop
    webview.start(debug=False)


if __name__ == "__main__":
    main()

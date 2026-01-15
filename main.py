import os
import sys
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import webview
from core.api import API

BASE_DIR = Path(__file__).resolve().parent
UI_BUILD_DIR = BASE_DIR / "ui" / "build"

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output" / "exports"


def get_pictures_dir() -> Path:
    home = Path.home()
    pics = home / "Pictures"
    if sys.platform.startswith("linux") and not pics.exists():
        pics = home / "Images"
    return pics


def start_static_server(directory: Path, host="127.0.0.1", port=0):
    """
    Start a local HTTP server serving `directory`.
    port=0 => choose a free port automatically.
    Returns (server, chosen_port).
    """
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        # (optional) silence logs
        def log_message(self, format, *args):
            return

    server = ThreadingHTTPServer((host, port), Handler)
    chosen_port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, chosen_port


def main():
    pictures_dir = get_pictures_dir()

    IMAGE_OUTPUT_DIR = pictures_dir / "ISCGraph"
    FILE_OUTPUT_DIR = pictures_dir / "Excels ISCGraph"

    # Create directories
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FILE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not UI_BUILD_DIR.exists():
        raise FileNotFoundError(f"React build introuvable: {UI_BUILD_DIR} (as-tu fait `npm run build` ?)")

    # Start local server on the build folder
    server, port = start_static_server(UI_BUILD_DIR)
    url = f"http://127.0.0.1:{port}/"

    api = API(str(BASE_DIR), str(DATA_DIR), str(OUTPUT_DIR), str(IMAGE_OUTPUT_DIR), str(FILE_OUTPUT_DIR))

    window = webview.create_window(
        title="ISCGraph",
        url=url,
        js_api=api,
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=True,
    )

    try:
        webview.start(debug=False)
    finally:
        # Clean shutdown
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()

"""
ISCGraph  - Application d'analyse de température et d'humidité
Point d'entrée principal de l'application
"""

import os
import sys
import webview
from core.api import API

# Définir les chemins de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "exports")
FRONTEND_BUILD_DIR = os.path.join(BASE_DIR,'ui',"build")
index_html = os.path.join(FRONTEND_BUILD_DIR, "index.html")


# Get system pictures directory
if sys.platform == "darwin":
    pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
elif sys.platform == "win32":
    pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
else:  # Linux
    pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
    if not os.path.exists(pictures_dir):
        pictures_dir = os.path.join(os.path.expanduser("~"), "Images")

# Set ISCGraph  images directory
IMAGE_OUTPUT_DIR = os.path.join(pictures_dir, "ISCGraph ")
FILE_OUTPUT_DIR = os.path.join(pictures_dir, "Excels ISCGraph")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)


def main():
    """
    Fonction principale qui initialise et démarre l'application
    """
    import tkinter as tk

    api = API(BASE_DIR, DATA_DIR, OUTPUT_DIR, IMAGE_OUTPUT_DIR, FILE_OUTPUT_DIR)

    # Créer la fenêtre principale sans largeur/hauteur
    window = webview.create_window(
        title="ISCGraph",
        # url='http://localhost:3000/',
        url=index_html,
        js_api=api,
        resizable=True,
        min_size=(800, 600),
    )

    # Fonction appelée lorsque la fenêtre est prête
    def on_ready():
        try:
            # Récupérer la résolution de l'écran via Tkinter
            root = tk.Tk()
            root.withdraw()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            root.destroy()

            # Taille : 90%
            new_width = int(screen_width * 0.90)
            new_height = int(screen_height * 0.90)

            # Position centrée
            pos_x = int((screen_width - new_width) / 2)
            pos_y = int((screen_height - new_height) / 2)

            # Appliquer taille et position
            window.resize(new_width, new_height)
            window.move(pos_x, pos_y)

        except Exception as e:
            print("Erreur lors du redimensionnement automatique :", e)

    # Lancer l'application
    webview.start(
        on_ready,
        debug=False
    )



if __name__ == "__main__":
    main()

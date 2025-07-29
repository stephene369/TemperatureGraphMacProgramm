"""
ISCGraph - Application d'analyse de température et d'humidité avec frontend React
Point d'entrée principal de l'application
"""

import os
import sys
import webview
from core.api import API

# Définir les chemins de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_BUILD_DIR = os.path.join(BASE_DIR, "frontend", "build")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "exports")

# Get system pictures directory
if sys.platform == "darwin":
    pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
elif sys.platform == "win32":
    pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
else:  # Linux
    pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
    if not os.path.exists(pictures_dir):
        pictures_dir = os.path.join(os.path.expanduser("~"), "Images")

# Set ISCGraph images directory
IMAGE_OUTPUT_DIR = os.path.join(pictures_dir, "ISCGraph")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

def main():
    """
    Fonction principale qui initialise et démarre l'application avec React
    """
    # Vérifier que le build React existe
    index_html = os.path.join(FRONTEND_BUILD_DIR, "index.html")
    
    if not os.path.exists(index_html):
        print("❌ Build React non trouvé!")
        print(f"Exécutez 'npm run build' dans le dossier frontend/")
        print(f"Recherche du fichier: {index_html}")
        return
    
    print("✅ Build React trouvé, démarrage de l'application...")
    
    # Créer l'instance de l'API
    api = API(BASE_DIR, DATA_DIR, OUTPUT_DIR, IMAGE_OUTPUT_DIR)

    # Créer la fenêtre principale avec le build React
    webview.create_window(
        title="ISCGraph - Analyse climatique",
        url=index_html,
        js_api=api,
        width=1500,
        height=900,
        resizable=True,
        min_size=(800, 600),
    )

    # Démarrer l'application
    webview.start(
        debug=False,
        icon=os.path.join(FRONTEND_BUILD_DIR, "favicon.ico") if os.path.exists(os.path.join(FRONTEND_BUILD_DIR, "favicon.ico")) else None,
    )


if __name__ == "__main__":
    main()

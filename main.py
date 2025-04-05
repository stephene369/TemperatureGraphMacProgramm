"""
ClimaGraph - Application d'analyse de température et d'humidité
Point d'entrée principal de l'application
"""
import os
import sys
import webview
from core.api import API

# Définir les chemins de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, 'ui')
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'exports')

# Get system pictures directory
if sys.platform == 'darwin':
    pictures_dir = os.path.join(os.path.expanduser('~'), 'Pictures')
elif sys.platform == 'win32':
    pictures_dir = os.path.join(os.path.expanduser('~'), 'Pictures')
else:  # Linux
    pictures_dir = os.path.join(os.path.expanduser('~'), 'Pictures')
    if not os.path.exists(pictures_dir):
        pictures_dir = os.path.join(os.path.expanduser('~'), 'Images')

# Set ClimaGraph images directory
IMAGE_OUTPUT_DIR = os.path.join(pictures_dir, 'ClimaGraph')

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

def main():
    """
    Fonction principale qui initialise et démarre l'application
    """
    # Créer l'instance de l'API
    api = API(BASE_DIR, DATA_DIR, OUTPUT_DIR , IMAGE_OUTPUT_DIR )
    
    # Créer la fenêtre principale
    window = webview.create_window(
        title='ClimaGraph',
        url=os.path.join(UI_DIR, 'index.html'),
        js_api=api,
        width=1500,
        height=900,
        resizable=True,
        min_size=(800, 600)
    )
    
    # Démarrer l'application
    webview.start(debug=True)

if __name__ == '__main__':
    main()

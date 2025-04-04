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

# Créer les répertoires s'ils n'existent pas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    """
    Fonction principale qui initialise et démarre l'application
    """
    # Créer l'instance de l'API
    api = API(BASE_DIR, DATA_DIR, OUTPUT_DIR)
    
    # Créer la fenêtre principale
    window = webview.create_window(
        title='ClimaGraph',
        url=os.path.join(UI_DIR, 'index.html'),
        js_api=api,
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600)
    )
    
    # Démarrer l'application
    webview.start(debug=True)

if __name__ == '__main__':
    main()

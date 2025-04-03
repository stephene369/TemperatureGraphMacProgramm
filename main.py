import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, 
                           FluentWindow, FluentIcon, setTheme, Theme)

# Importer les pages
from ui.home_page import HomePage
from ui.capteur_selector import CapteurSelectorPage
from ui.column_mapper import ColumnMapperPage
from ui.graph_display import GraphDisplayPage
from ui.history_page import HistoryPage

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de base
        self.setWindowTitle("ClimaGraph")
        self.resize(1000, 700)
        
        # Créer les dossiers nécessaires
        os.makedirs("data", exist_ok=True)
        os.makedirs("output/exports", exist_ok=True)
        
        # Définir le thème
        setTheme(Theme.AUTO)
        
        # Charger les styles QSS globaux
        self.load_styles()
        
        # Initialiser l'interface
        self.init_navigation()
        self.init_window()
        
    def load_styles(self):
        """Charge les styles QSS globaux"""
        # Vérifier si le dossier de styles existe
        styles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "styles")
        if not os.path.exists(styles_dir):
            os.makedirs(styles_dir, exist_ok=True)
            
        # Charger le style global
        main_style_path = os.path.join(styles_dir, "main.qss")
        if os.path.exists(main_style_path):
            with open(main_style_path, "r") as f:
                self.setStyleSheet(f.read())
        
    def init_navigation(self):
        """Initialise la barre de navigation"""
        # Créer les pages
        self.home_page = HomePage(self)
        self.home_page.setObjectName("homePage")
        
        self.capteur_page = CapteurSelectorPage(self)
        self.capteur_page.setObjectName("capteurPage")
        
        self.column_page = ColumnMapperPage(self)
        self.column_page.setObjectName("columnPage")
        
        self.graph_page = GraphDisplayPage(self)
        self.graph_page.setObjectName("graphPage")
        
        self.history_page = HistoryPage(self)
        self.history_page.setObjectName("historyPage")
        
        # Ajouter les pages à la navigation
        self.addSubInterface(self.home_page, FluentIcon.HOME, "Accueil")
        self.addSubInterface(self.capteur_page, FluentIcon.IOT, "Capteurs & Fichiers")
        self.addSubInterface(self.column_page, FluentIcon.VIEW, "Mappage des Colonnes")
        self.addSubInterface(self.graph_page, FluentIcon.VIEW, "Graphiques")
        self.addSubInterface(self.history_page, FluentIcon.HISTORY, "Historique")
        
        # Configurer la navigation
        self.navigationInterface.setExpandWidth(200)
        self.navigationInterface.setMinimumWidth(48)
        
    def init_window(self):
        """Initialise la fenêtre principale"""
        # Définir la page d'accueil comme page par défaut
        self.navigationInterface.setCurrentItem("Accueil")
        
        # Connecter les signaux entre les pages
        self.capteur_page.capteurAdded.connect(self.on_capteur_added)
        self.column_page.mappingCompleted.connect(self.on_mapping_completed)
        
    def on_capteur_added(self, capteur_name, file_path):
        """Appelé lorsqu'un capteur est ajouté"""
        # Mettre à jour les autres pages
        self.column_page.load_capteurs()
        self.graph_page.load_capteurs()
        self.history_page.load_capteurs()

    def on_mapping_completed(self, capteur_name, mapping):
        """Appelé lorsque le mappage des colonnes est terminé"""
        # Mettre à jour les autres pages
        self.graph_page.load_capteurs()
        self.history_page.load_capteurs()

if __name__ == "__main__":
    # Créer l'application
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec_())

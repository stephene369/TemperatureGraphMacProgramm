from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize, QEasingCurve, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QFont

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, 
                           NavigationWidget, NavigationItem, FluentIcon, 
                           SplitFluentWindow, FluentWindow, Theme, setTheme,
                           isDarkTheme, toggleTheme, MessageBox, InfoBar,
                           InfoBarPosition)

# Import des pages
from ui.home_page import HomePage
from ui.capteur_selector import CapteurSelectorPage
from ui.column_mapper import ColumnMapperPage
from ui.graph_display import GraphDisplayPage
from ui.history_page import HistoryPage

class MainWindow(FluentWindow):
    def __init__(self):
        """Fenêtre principale de l'application avec barre de navigation latérale"""
        super().__init__()
        
        # Configuration de la fenêtre
        self.setWindowTitle("ClimaGraph - Analyse de données climatiques")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)
        
        # Initialisation du thème
        setTheme(Theme.AUTO)
        
        # Création des pages
        self.home_page = HomePage(self)
        self.capteur_page = CapteurSelectorPage(self)
        self.column_page = ColumnMapperPage(self)
        self.graph_page = GraphDisplayPage(self)
        self.history_page = HistoryPage(self)
        
        # Ajout des pages à la navigation
        self.init_navigation()
        
        # Affichage d'un message de bienvenue
        self._show_welcome_message()
        
    def init_navigation(self):
        """Initialise la barre de navigation latérale"""
        # Ajout des pages à la fenêtre
        self.addSubInterface(self.home_page, FluentIcon.HOME, "Accueil")
        self.addSubInterface(self.capteur_page, FluentIcon.IOT, "Capteurs & Fichiers")
        self.addSubInterface(self.column_page, FluentIcon.COLUMN, "Mappage des Colonnes")
        self.addSubInterface(self.graph_page, FluentIcon.CHART, "Graphiques")
        self.addSubInterface(self.history_page, FluentIcon.HISTORY, "Historique")
        
        # Ajout d'un séparateur
        self.navigationInterface.addSeparator()
        
        # Ajout d'éléments en bas de la barre de navigation
        self.navigationInterface.addItem(
            routeKey='settings',
            icon=FluentIcon.SETTING,
            text='Paramètres',
            position=NavigationItemPosition.BOTTOM
        )
        
        self.navigationInterface.addItem(
            routeKey='help',
            icon=FluentIcon.HELP,
            text='Aide',
            position=NavigationItemPosition.BOTTOM
        )
        
        # Connexion des signaux
        self.navigationInterface.setCurrentItem("Accueil")
        self.navigationInterface.itemClicked.connect(self._on_nav_item_clicked)
        
    def _on_nav_item_clicked(self, item):
        """Gère les clics sur les éléments de navigation spéciaux"""
        if item.routeKey() == 'settings':
            self._show_settings_dialog()
        elif item.routeKey() == 'help':
            self._show_help_dialog()
            
    def _show_settings_dialog(self):
        """Affiche la boîte de dialogue des paramètres"""
        dialog = MessageBox(
            "Paramètres",
            "Les paramètres seront disponibles dans une future version.",
            self
        )
        
        # Ajout d'un bouton pour changer de thème
        theme_button = dialog.addButton("Changer de thème", MessageBox.ButtonRole.ActionRole)
        theme_button.clicked.connect(self._toggle_theme)
        
        dialog.exec()
        
    def _toggle_theme(self):
        """Bascule entre les thèmes clair et sombre"""
        toggleTheme()
        theme_name = "sombre" if isDarkTheme() else "clair"
        
        InfoBar.success(
            title="Thème modifié",
            content=f"Le thème {theme_name} a été appliqué.",
            parent=self,
            position=InfoBarPosition.TOP,
            duration=3000
        )
        
    def _show_help_dialog(self):
        """Affiche la boîte de dialogue d'aide"""
        MessageBox(
            "Aide",
            "ClimaGraph - Analyse de données climatiques\n\n"
            "1. Ajoutez des capteurs dans l'onglet 'Capteurs & Fichiers'\n"
            "2. Associez des fichiers de données à chaque capteur\n"
            "3. Vérifiez le mappage des colonnes\n"
            "4. Générez et visualisez les graphiques\n"
            "5. Consultez l'historique des imports\n\n"
            "Pour plus d'informations, contactez le support.",
            self
        ).exec()
        
    def _show_welcome_message(self):
        """Affiche un message de bienvenue au démarrage"""
        InfoBar.success(
            title="Bienvenue dans ClimaGraph",
            content="L'application est prête à l'emploi.",
            parent=self,
            position=InfoBarPosition.TOP,
            duration=5000
        )

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

from qfluentwidgets import (ScrollArea, CardWidget, SimpleCardWidget, 
                           PrimaryPushButton, PushButton, ToolButton, 
                           FluentIcon, IconWidget, StateToolTip, InfoBar,
                           InfoBarPosition, setTheme, Theme)

import os

class HomePage(ScrollArea):
    def __init__(self, parent=None):
        """Page d'accueil avec présentation des fonctionnalités"""
        super().__init__(parent=parent)
        self.parent = parent
        self.setup_ui()
        self.load_styles()
        
    def load_styles(self):
        """Charge les styles QSS spécifiques à la page d'accueil"""
        styles_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "styles")
        home_style_path = os.path.join(styles_dir, "home.qss")
        
        if os.path.exists(home_style_path):
            with open(home_style_path, "r") as f:
                self.setStyleSheet(f.read())
        
    def setup_ui(self):
        """Configure l'interface utilisateur de la page d'accueil"""
        # Widget principal
        self.main_widget = QWidget()
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        
        # En-tête
        self.header_widget = QWidget()
        self.header_layout = QVBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Titre
        self.title_label = QLabel("ClimaGraph")
        self.title_label.setStyleSheet("font-size: 38px; font-weight: bold; margin-bottom: 5px;")
        self.title_label.setObjectName("welcomeTitle")
        self.header_layout.addWidget(self.title_label)
        
        # Sous-titre
        self.subtitle_label = QLabel("Analyse et visualisation de données climatiques")
        self.subtitle_label.setStyleSheet("font-size: 16px; color: gray;")
        self.subtitle_label.setObjectName("welcomeSubtitle")
        self.header_layout.addWidget(self.subtitle_label)
        
        # Ajout de l'en-tête au layout principal
        self.main_layout.addWidget(self.header_widget)
        
        # Cartes de fonctionnalités
        self.features_layout = QHBoxLayout()
        self.features_layout.setSpacing(15)
        
        # Carte 1: Gestion des capteurs
        self.capteur_card = SimpleCardWidget()
        self.capteur_layout = QVBoxLayout(self.capteur_card)
        
        self.capteur_icon = IconWidget(FluentIcon.IOT)
        self.capteur_icon.setFixedSize(48, 48)
        self.capteur_layout.addWidget(self.capteur_icon, 0, Qt.AlignCenter)
        
        self.capteur_title = QLabel("Gestion des capteurs")
        self.capteur_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.capteur_title.setAlignment(Qt.AlignCenter)
        self.capteur_layout.addWidget(self.capteur_title)
        
        self.capteur_desc = QLabel("Ajoutez et gérez vos capteurs de température et d'humidité")
        self.capteur_desc.setWordWrap(True)
        self.capteur_desc.setAlignment(Qt.AlignCenter)
        self.capteur_layout.addWidget(self.capteur_desc)
        
        self.capteur_button = PrimaryPushButton("Commencer")
        self.capteur_button.clicked.connect(lambda: self.parent.navigationInterface.setCurrentItem("Capteurs & Fichiers"))
        self.capteur_layout.addWidget(self.capteur_button, 0, Qt.AlignCenter)
        
        self.features_layout.addWidget(self.capteur_card)
        
        # Carte 2: Mappage des colonnes
        self.column_card = SimpleCardWidget()
        self.column_layout = QVBoxLayout(self.column_card)
        
        self.column_icon = IconWidget(FluentIcon.LAYOUT)
        self.column_icon.setFixedSize(48, 48)
        self.column_layout.addWidget(self.column_icon, 0, Qt.AlignCenter)
        
        self.column_title = QLabel("Mappage des colonnes")
        self.column_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.column_title.setAlignment(Qt.AlignCenter)
        self.column_layout.addWidget(self.column_title)
        
        self.column_desc = QLabel("Associez les colonnes de vos fichiers aux données requises")
        self.column_desc.setWordWrap(True)
        self.column_desc.setAlignment(Qt.AlignCenter)
        self.column_layout.addWidget(self.column_desc)
        
        self.column_button = PrimaryPushButton("Configurer")
        self.column_button.clicked.connect(lambda: self.parent.navigationInterface.setCurrentItem("Mappage des Colonnes"))
        self.column_layout.addWidget(self.column_button, 0, Qt.AlignCenter)
        
        self.features_layout.addWidget(self.column_card)
        
        # Carte 3: Graphiques
        self.graph_card = SimpleCardWidget()
        self.graph_layout = QVBoxLayout(self.graph_card)
        
        self.graph_icon = IconWidget(FluentIcon.VIEW)
        self.graph_icon.setFixedSize(48, 48)
        self.graph_layout.addWidget(self.graph_icon, 0, Qt.AlignCenter)
        
        self.graph_title = QLabel("Visualisation")
        self.graph_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.graph_title.setAlignment(Qt.AlignCenter)
        self.graph_layout.addWidget(self.graph_title)
        
        self.graph_desc = QLabel("Générez et visualisez des graphiques à partir de vos données")
        self.graph_desc.setWordWrap(True)
        self.graph_desc.setAlignment(Qt.AlignCenter)
        self.graph_layout.addWidget(self.graph_desc)
        
        self.graph_button = PrimaryPushButton("Explorer")
        self.graph_button.clicked.connect(lambda: self.parent.navigationInterface.setCurrentItem("Graphiques"))
        self.graph_layout.addWidget(self.graph_button, 0, Qt.AlignCenter)
        
        self.features_layout.addWidget(self.graph_card)
        
        # Ajout des cartes au layout principal
        self.main_layout.addLayout(self.features_layout)
        
        # Section d'aide rapide
        self.help_card = CardWidget()
        self.help_layout = QVBoxLayout(self.help_card)
        
        self.help_title = QLabel("Guide rapide")
        self.help_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.help_layout.addWidget(self.help_title)
        
        self.help_text = QLabel(
            "1. Commencez par ajouter vos capteurs dans la section 'Capteurs & Fichiers'\n"
            "2. Associez un fichier de données à chaque capteur\n"
            "3. Vérifiez le mappage des colonnes dans la section dédiée\n"
            "4. Générez et visualisez vos graphiques\n"
            "5. Consultez l'historique des imports pour suivre vos analyses"
        )
        self.help_text.setStyleSheet("line-height: 150%;")
        self.help_layout.addWidget(self.help_text)
        
        self.main_layout.addWidget(self.help_card)
        
        # Espacement flexible
        self.main_layout.addStretch(1)

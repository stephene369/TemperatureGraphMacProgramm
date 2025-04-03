from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from qfluentwidgets import (ScrollArea, PushButton, FluentIcon, 
                           InfoBar, InfoBarPosition, MessageBox)

import os
import json
from datetime import datetime

class HistoryPage(ScrollArea):
    def __init__(self, parent=None):
        """Page d'historique des imports et analyses"""
        super().__init__(parent=parent)
        self.parent = parent
        self.setup_ui()
        self.load_styles()  # Ajouter cette ligne
        self.load_capteurs()  # Charger les capteurs existants
        
    def load_styles(self):
        """Charge les styles QSS spécifiques à la page d'historique"""
        styles_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "styles")
        history_style_path = os.path.join(styles_dir, "history.qss")
        
        if os.path.exists(history_style_path):
            with open(history_style_path, "r") as f:
                self.setStyleSheet(f.read())
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
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
        self.title_label = QLabel("🕓 Historique")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 5px;")
        self.title_label.setObjectName("historyTitle")
        self.header_layout.addWidget(self.title_label)
        
        # Sous-titre
        self.subtitle_label = QLabel("Consultez l'historique des imports et des analyses")
        self.subtitle_label.setStyleSheet("font-size: 14px; color: gray;")
        self.subtitle_label.setObjectName("historySubtitle")
        self.header_layout.addWidget(self.subtitle_label)
        
        # Ajout de l'en-tête au layout principal
        self.main_layout.addWidget(self.header_widget)
        
        # Tableau d'historique
        self.history_table = QTableWidget()
        self.history_table.setObjectName("historyTable")
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Capteur", "Fichier", "Date d'import", "Colonnes mappées"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.main_layout.addWidget(self.history_table)
        
        # Boutons d'action
        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        self.refresh_button = PushButton("Actualiser")
        self.refresh_button.setObjectName("refreshButton")
        self.refresh_button.setIcon(FluentIcon.SYNC)
        self.refresh_button.clicked.connect(self.load_capteurs)
        self.buttons_layout.addWidget(self.refresh_button)
        
        self.clear_button = PushButton("Effacer l'historique")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setIcon(FluentIcon.DELETE)
        self.clear_button.clicked.connect(self.clear_history)
        self.buttons_layout.addWidget(self.clear_button)
        
        self.buttons_layout.addStretch(1)
        
        self.main_layout.addWidget(self.buttons_widget)
        
        # Zone de remarques
        self.notes_label = QLabel("💬 Remarques:")
        self.notes_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.main_layout.addWidget(self.notes_label)
        
        self.notes_text = QLabel(
            "- L'historique affiche tous les capteurs et fichiers importés.\n"
            "- Vous pouvez effacer l'historique pour recommencer à zéro.\n"
            "- Les données sont sauvegardées localement dans le dossier 'data'."
        )
        self.notes_text.setStyleSheet("color: #505050; line-height: 150%;")
        self.main_layout.addWidget(self.notes_text)
        
    def load_capteurs(self):
        """Charge les capteurs depuis un fichier JSON et met à jour le tableau"""
        try:
            # Vérifier si le fichier existe
            if os.path.exists("data/capteurs.json"):
                with open("data/capteurs.json", "r") as f:
                    data = json.load(f)
                    self.capteurs = data.get("capteurs", {})
                    
                # Mettre à jour le tableau
                self.update_history_table()
                
        except Exception as e:
            InfoBar.error(
                title="Erreur",
                content=f"Impossible de charger l'historique: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP
            )
            
    def update_history_table(self):
        """Met à jour le tableau d'historique"""
        self.history_table.setRowCount(0)  # Effacer le tableau
        
        for row, (name, data) in enumerate(self.capteurs.items()):
            self.history_table.insertRow(row)
            
            # Nom du capteur
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)  # Non éditable
            self.history_table.setItem(row, 0, name_item)
            
            # Chemin du fichier
            file_item = QTableWidgetItem(os.path.basename(data["file_path"]))
            file_item.setToolTip(data["file_path"])
            file_item.setFlags(file_item.flags() & ~Qt.ItemIsEditable)  # Non éditable
            self.history_table.setItem(row, 1, file_item)
            
            # Date d'import
            date_item = QTableWidgetItem(data.get("imported_at", "Non spécifié"))
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)  # Non éditable
            self.history_table.setItem(row, 2, date_item)
            
            # Colonnes mappées
            columns = data.get("columns", {})
            columns_text = ", ".join([f"{k}: {v}" for k, v in columns.items()]) if columns else "Non mappé"
            columns_item = QTableWidgetItem(columns_text)
            columns_item.setFlags(columns_item.flags() & ~Qt.ItemIsEditable)  # Non éditable
            self.history_table.setItem(row, 3, columns_item)
            
        # Ajuster la taille des colonnes
        self.history_table.resizeColumnsToContents()
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        
    def clear_history(self):
        """Efface l'historique des capteurs"""
        # Demander confirmation
        dialog = MessageBox(
            "Confirmation",
            "Êtes-vous sûr de vouloir effacer tout l'historique? Cette action est irréversible.",
            self
        )
        
        yes_button = dialog.addButton("Oui", MessageBox.ButtonRole.YesRole)
        no_button = dialog.addButton("Non", MessageBox.ButtonRole.NoRole)
        
        dialog.exec()
        
        if dialog.clickedButton() == yes_button:
            try:
                # Effacer les capteurs
                self.capteurs = {}
                
                # Sauvegarder le fichier vide
                with open("data/capteurs.json", "w") as f:
                    json.dump({"capteurs": {}}, f, indent=2)
                    
                # Mettre à jour le tableau
                self.update_history_table()
                
                # Afficher un message de succès
                InfoBar.success(
                    title="Succès",
                    content="L'historique a été effacé avec succès.",
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=3000
                )
                
            except Exception as e:
                InfoBar.error(
                    title="Erreur",
                    content=f"Impossible d'effacer l'historique: {str(e)}",
                    parent=self,
                    position=InfoBarPosition.TOP
                )

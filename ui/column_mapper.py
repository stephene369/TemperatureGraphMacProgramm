from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QTableWidget, QTableWidgetItem, 
                            QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon

from qfluentwidgets import (ScrollArea, PrimaryPushButton, ComboBox, 
                           LineEdit, PushButton, FluentIcon, 
                           InfoBar, InfoBarPosition, MessageBox)

import os
import json
import pandas as pd
from datetime import datetime

class ColumnMapperPage(ScrollArea):
    mappingCompleted = pyqtSignal(str, dict)  # Signal: nom_capteur, mapping
    
    def __init__(self, parent=None):
        """Page de mappage des colonnes pour les fichiers de données"""
        super().__init__(parent=parent)
        self.parent = parent
        self.setup_ui()
        self.load_styles()  # Ajouter cette ligne
        
    def load_styles(self):
        """Charge les styles QSS spécifiques à la page de mappage des colonnes"""
        styles_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "styles")
        column_style_path = os.path.join(styles_dir, "columns.qss")
        
        if os.path.exists(column_style_path):
            with open(column_style_path, "r") as f:
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
        self.title_label = QLabel("🧠 Mappage des Colonnes")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 5px;")
        self.header_layout.addWidget(self.title_label)
        
        # Sous-titre
        self.subtitle_label = QLabel("Associez les colonnes de vos fichiers aux données requises")
        self.subtitle_label.setStyleSheet("font-size: 14px; color: gray;")
        self.header_layout.addWidget(self.subtitle_label)
        
        # Ajout de l'en-tête au layout principal
        self.main_layout.addWidget(self.header_widget)
        
        # Sélection du capteur
        self.capteur_selector_widget = QWidget()
        self.capteur_selector_layout = QHBoxLayout(self.capteur_selector_widget)
        self.capteur_selector_layout.setContentsMargins(0, 0, 0, 0)
        
        self.capteur_label = QLabel("Sélectionnez un capteur:")
        self.capteur_selector_layout.addWidget(self.capteur_label)
        
        self.capteur_combo = ComboBox()
        self.capteur_combo.currentTextChanged.connect(self.on_capteur_changed)
        self.capteur_selector_layout.addWidget(self.capteur_combo)
        
        self.load_button = PushButton("Charger les colonnes")
        self.load_button.setIcon(FluentIcon.SYNC)
        self.load_button.clicked.connect(self.load_columns)
        self.capteur_selector_layout.addWidget(self.load_button)
        
        self.main_layout.addWidget(self.capteur_selector_widget)
        
        # Mappage des colonnes
        self.mapping_widget = QWidget()
        self.mapping_layout = QVBoxLayout(self.mapping_widget)
        self.mapping_layout.setContentsMargins(0, 0, 0, 0)
        
        # Titre du mappage
        self.mapping_title = QLabel("Mappage des colonnes")
        self.mapping_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        self.mapping_layout.addWidget(self.mapping_title)
        
        # Tableau de mappage
        self.mapping_table = QTableWidget()
        self.mapping_table.setColumnCount(2)
        self.mapping_table.setHorizontalHeaderLabels(["Type de données", "Colonne du fichier"])
        self.mapping_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.mapping_layout.addWidget(self.mapping_table)
        
        # Bouton de sauvegarde
        self.save_button = PrimaryPushButton("Enregistrer le mappage")
        self.save_button.setIcon(FluentIcon.SAVE)
        self.save_button.clicked.connect(self.save_mapping)
        self.mapping_layout.addWidget(self.save_button, 0, Qt.AlignRight)
        
        self.main_layout.addWidget(self.mapping_widget)
        
        # Zone de remarques
        self.notes_label = QLabel("💬 Remarques:")
        self.notes_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.main_layout.addWidget(self.notes_label)
        
        self.notes_text = QLabel(
            "- Le mappage est nécessaire pour identifier correctement les données.\n"
            "- Les colonnes 'Date', 'Température' et 'Humidité' sont requises pour l'analyse.\n"
            "- Si les colonnes ne sont pas détectées automatiquement, vous pouvez les mapper manuellement."
        )
        self.notes_text.setStyleSheet("color: #505050; line-height: 150%;")
        self.main_layout.addWidget(self.notes_text)
        
        # Initialiser le tableau de mappage
        self.init_mapping_table()
        
    def init_mapping_table(self):
        """Initialise le tableau de mappage avec les types de données requis"""
        self.mapping_table.setRowCount(3)
        
        # Types de données requis
        required_data = [
            ("Date", "Colonne contenant la date et l'heure des mesures"),
            ("Température", "Colonne contenant les valeurs de température"),
            ("Humidité", "Colonne contenant les valeurs d'humidité")
        ]
        
        for row, (data_type, tooltip) in enumerate(required_data):
            # Type de données
            type_item = QTableWidgetItem(data_type)
            type_item.setToolTip(tooltip)
            type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)  # Non éditable
            self.mapping_table.setItem(row, 0, type_item)
            
            # Combobox pour sélectionner la colonne
            combo = ComboBox()
            combo.addItems(["-- Sélectionnez une colonne --"])
            self.mapping_table.setCellWidget(row, 1, combo)
            
    def load_capteurs(self):
        """Charge les capteurs depuis un fichier JSON"""
        try:
            # Vérifier si le fichier existe
            if os.path.exists("data/capteurs.json"):
                with open("data/capteurs.json", "r") as f:
                    data = json.load(f)
                    self.capteurs = data.get("capteurs", {})
                    
                # Mettre à jour le combobox
                self.update_capteur_combo()
                
        except Exception as e:
            InfoBar.error(
                title="Erreur",
                content=f"Impossible de charger les capteurs: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP
            )
            
    def update_capteur_combo(self):
        """Met à jour le combobox des capteurs"""
        self.capteur_combo.clear()
        
        if not self.capteurs:
            self.capteur_combo.addItem("Aucun capteur disponible")
            return
            
        self.capteur_combo.addItem("-- Sélectionnez un capteur --")
        for capteur_name in self.capteurs.keys():
            self.capteur_combo.addItem(capteur_name)
            
    def on_capteur_changed(self, capteur_name):
        """Gère le changement de capteur sélectionné"""
        if capteur_name in ["-- Sélectionnez un capteur --", "Aucun capteur disponible"]:
            self.current_capteur = None
            return
            
        self.current_capteur = capteur_name
        
        # Charger les colonnes si le capteur a déjà un mappage
        if self.current_capteur in self.capteurs:
            capteur_data = self.capteurs[self.current_capteur]
            if "columns" in capteur_data and capteur_data["columns"]:
                # Charger les colonnes du fichier
                self.load_columns()
                
                # Appliquer le mappage existant
                self.apply_existing_mapping(capteur_data["columns"])
                
    def load_columns(self):
        """Charge les colonnes du fichier associé au capteur sélectionné"""
        if not self.current_capteur:
            InfoBar.warning(
                title="Attention",
                content="Veuillez d'abord sélectionner un capteur.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return
            
        try:
            # Récupérer le chemin du fichier
            file_path = self.capteurs[self.current_capteur]["file_path"]
            
            # Vérifier si le fichier existe
            if not os.path.exists(file_path):
                InfoBar.error(
                    title="Erreur",
                    content=f"Le fichier '{file_path}' n'existe pas.",
                    parent=self,
                    position=InfoBarPosition.TOP
                )
                return
                
            # Charger les colonnes selon le type de fichier
            if file_path.endswith(".xlsx"):
                # Lire le fichier Excel
                df = pd.read_excel(file_path, nrows=1)
                self.columns = df.columns.tolist()
            elif file_path.endswith(".hobo"):
                # Pour les fichiers HOBO, on pourrait implémenter un parser spécifique
                # Pour l'instant, on affiche un message d'erreur
                InfoBar.error(
                    title="Format non supporté",
                    content="Le format .hobo n'est pas encore pris en charge pour la détection automatique.",
                    parent=self,
                    position=InfoBarPosition.TOP
                )
                return
            else:
                InfoBar.error(
                    title="Format non supporté",
                    content=f"Le format du fichier '{os.path.basename(file_path)}' n'est pas pris en charge.",
                    parent=self,
                    position=InfoBarPosition.TOP
                )
                return
                
            # Mettre à jour les combobox avec les colonnes
            self.update_column_combos()
            
            # Tenter une détection automatique
            self.auto_detect_columns()
            
            InfoBar.success(
                title="Succès",
                content=f"{len(self.columns)} colonnes ont été chargées depuis le fichier.",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            
        except Exception as e:
            InfoBar.error(
                title="Erreur",
                content=f"Impossible de charger les colonnes: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP
            )
            
    def update_column_combos(self):
        """Met à jour les combobox avec les colonnes du fichier"""
        for row in range(self.mapping_table.rowCount()):
            combo = self.mapping_table.cellWidget(row, 1)
            
            # Sauvegarder la sélection actuelle
            current_selection = combo.currentText()
            
            # Mettre à jour les options
            combo.clear()
            combo.addItem("-- Sélectionnez une colonne --")
            combo.addItems(self.columns)
            
            # Restaurer la sélection si possible
            if current_selection in self.columns:
                combo.setCurrentText(current_selection)
                
    def auto_detect_columns(self):
        """Tente de détecter automatiquement les colonnes pertinentes"""
        # Mots-clés pour la détection
        date_keywords = ["date", "time", "datetime", "horodatage", "timestamp"]
        temp_keywords = ["temp", "température", "temperature"]
        humidity_keywords = ["humid", "humidité", "humidity", "hr", "rh"]
        
        # Fonction pour trouver la meilleure correspondance
        def find_best_match(keywords, columns):
            for column in columns:
                col_lower = column.lower()
                for keyword in keywords:
                    if keyword in col_lower:
                        return column
            return None
            
        # Détecter les colonnes
        date_column = find_best_match(date_keywords, self.columns)
        temp_column = find_best_match(temp_keywords, self.columns)
        humidity_column = find_best_match(humidity_keywords, self.columns)
        
        # Appliquer les détections
        if date_column:
            self.mapping_table.cellWidget(0, 1).setCurrentText(date_column)
            
        if temp_column:
            self.mapping_table.cellWidget(1, 1).setCurrentText(temp_column)
            
        if humidity_column:
            self.mapping_table.cellWidget(2, 1).setCurrentText(humidity_column)
            
    def apply_existing_mapping(self, mapping):
        """Applique un mappage existant aux combobox"""
        # Correspondance entre les types de données et les indices de ligne
        type_to_row = {
            "date": 0,
            "temperature": 1,
            "humidity": 2
        }
        
        # Appliquer le mappage
        for data_type, column in mapping.items():
            if data_type in type_to_row and column in self.columns:
                row = type_to_row[data_type]
                self.mapping_table.cellWidget(row, 1).setCurrentText(column)
                
    def save_mapping(self):
        """Sauvegarde le mappage des colonnes"""
        if not self.current_capteur:
            InfoBar.warning(
                title="Attention",
                content="Veuillez d'abord sélectionner un capteur.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return
            
        # Récupérer le mappage
        mapping = {}
        data_types = ["date", "temperature", "humidity"]
        
        for row, data_type in enumerate(data_types):
            combo = self.mapping_table.cellWidget(row, 1)
            column = combo.currentText()
            
            if column == "-- Sélectionnez une colonne --":
                InfoBar.warning(
                    title="Mappage incomplet",
                    content=f"Veuillez sélectionner une colonne pour '{self.mapping_table.item(row, 0).text()}'.",
                    parent=self,
                    position=InfoBarPosition.TOP
                )
                return
                
            mapping[data_type] = column
            
        # Mettre à jour le capteur
        self.capteurs[self.current_capteur]["columns"] = mapping
        
        # Sauvegarder les capteurs
        try:
            with open("data/capteurs.json", "w") as f:
                json.dump({"capteurs": self.capteurs}, f, indent=2)
                
            # Émettre le signal
            self.mappingCompleted.emit(self.current_capteur, mapping)
            
            # Afficher un message de succès
            InfoBar.success(
                title="Succès",
                content=f"Le mappage des colonnes pour '{self.current_capteur}' a été enregistré.",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            
        except Exception as e:
            InfoBar.error(
                title="Erreur",
                content=f"Impossible de sauvegarder le mappage: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP
            )

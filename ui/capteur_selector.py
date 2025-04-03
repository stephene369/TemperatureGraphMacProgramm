from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QHeaderView, 
                            QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon

from qfluentwidgets import (ScrollArea, PrimaryPushButton, ComboBox, 
                           LineEdit, PushButton, FluentIcon, 
                           InfoBar, InfoBarPosition, MessageBox)

import os
import json
from datetime import datetime

class CapteurSelectorPage(ScrollArea):
    capteurAdded = pyqtSignal(str, str)  # Signal: nom_capteur, chemin_fichier
    
    def __init__(self, parent=None):
        """Page de gestion des capteurs et fichiers associés"""
        super().__init__(parent=parent)
        self.parent = parent
        self.setup_ui()
        self.load_styles()
        self.load_capteurs()  # Charger les capteurs existants
        
    def load_styles(self):
        """Charge les styles QSS spécifiques à la page des capteurs"""
        styles_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "styles")
        capteur_style_path = os.path.join(styles_dir, "capteurs.qss")
        
        if os.path.exists(capteur_style_path):
            with open(capteur_style_path, "r") as f:
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
        self.title_label = QLabel("📁 Capteurs & Fichiers")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 5px;")
        self.title_label.setObjectName("capteurTitle")
        self.header_layout.addWidget(self.title_label)
        
        # Sous-titre
        self.subtitle_label = QLabel("Associez un fichier de données à chaque capteur")
        self.subtitle_label.setStyleSheet("font-size: 14px; color: gray;")
        self.subtitle_label.setObjectName("capteurSubtitle")
        self.header_layout.addWidget(self.subtitle_label)
        
        # Ajout de l'en-tête au layout principal
        self.main_layout.addWidget(self.header_widget)
        
        # Formulaire d'ajout de capteur
        self.form_widget = QWidget()
        self.form_layout = QHBoxLayout(self.form_widget)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Champ de nom de capteur
        self.capteur_name_label = QLabel("Nom du capteur:")
        self.form_layout.addWidget(self.capteur_name_label)
        
        self.capteur_name_input = LineEdit()
        self.capteur_name_input.setPlaceholderText("Ex: Capteur Nord")
        self.form_layout.addWidget(self.capteur_name_input)
        
        # Bouton de sélection de fichier
        self.file_path_label = QLabel("Fichier de données:")
        self.form_layout.addWidget(self.file_path_label)
        
        self.file_path_input = LineEdit()
        self.file_path_input.setPlaceholderText("Sélectionnez un fichier...")
        self.file_path_input.setReadOnly(True)
        self.form_layout.addWidget(self.file_path_input)
        
        self.browse_button = PushButton("Parcourir")
        self.browse_button.setIcon(FluentIcon.FOLDER)
        self.browse_button.clicked.connect(self.browse_file)
        self.form_layout.addWidget(self.browse_button)
        
        # Bouton d'ajout
        self.add_button = PrimaryPushButton("Ajouter")
        self.add_button.setIcon(FluentIcon.ADD)
        self.add_button.clicked.connect(self.add_capteur)
        self.form_layout.addWidget(self.add_button)
        
        self.main_layout.addWidget(self.form_widget)
        
        # Tableau des capteurs
        self.table_label = QLabel("Liste des capteurs")
        self.table_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        self.main_layout.addWidget(self.table_label)
        
        self.capteurs_table = QTableWidget()
        self.capteurs_table.setColumnCount(4)
        self.capteurs_table.setHorizontalHeaderLabels(["Nom", "Fichier", "Date d'import", "Actions"])
        self.capteurs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.capteurs_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.main_layout.addWidget(self.capteurs_table)
        
        # Zone de remarques
        self.notes_label = QLabel("💬 Remarques:")
        self.notes_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.main_layout.addWidget(self.notes_label)
        
        self.notes_text = QLabel(
            "- Un capteur correspond à un point de mesure.\n"
            "- Les fichiers peuvent être en format .xlsx ou .hobo.\n"
            "- L'historique est sauvegardé automatiquement."
        )
        self.notes_text.setStyleSheet("color: #505050; line-height: 150%;")
        self.main_layout.addWidget(self.notes_text)
        
    def browse_file(self):
        """Ouvre une boîte de dialogue pour sélectionner un fichier"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier de données",
            "",
            "Fichiers Excel (*.xlsx);;Fichiers HOBO (*.hobo);;Tous les fichiers (*.*)"
        )
        
        if file_path:
            self.file_path_input.setText(file_path)
            
    def add_capteur(self):
        """Ajoute un nouveau capteur à la liste"""
        capteur_name = self.capteur_name_input.text().strip()
        file_path = self.file_path_input.text().strip()
        
        # Validation
        if not capteur_name:
            InfoBar.error(
                title="Erreur",
                content="Veuillez entrer un nom pour le capteur.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return
            
        if not file_path:
            InfoBar.error(
                title="Erreur",
                content="Veuillez sélectionner un fichier de données.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return
            
        # Vérifier si le capteur existe déjà
        if capteur_name in self.capteurs:
            InfoBar.warning(
                title="Attention",
                content=f"Le capteur '{capteur_name}' existe déjà. Voulez-vous le remplacer?",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=5000
            )
            return
            
        # Ajouter le capteur
        import_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.capteurs[capteur_name] = {
            "file_path": file_path,
            "imported_at": import_date,
            "columns": {}  # Sera rempli lors du mappage des colonnes
        }
        
        # Mettre à jour le tableau
        self.update_capteurs_table()
        
        # Sauvegarder les capteurs
        self.save_capteurs()
        
        # Émettre le signal
        self.capteurAdded.emit(capteur_name, file_path)
        
        # Réinitialiser les champs
        self.capteur_name_input.clear()
        self.file_path_input.clear()
        
        # Afficher un message de succès
        InfoBar.success(
            title="Succès",
            content=f"Le capteur '{capteur_name}' a été ajouté avec succès.",
            parent=self,
            position=InfoBarPosition.TOP,
            duration=3000
        )
        
    def update_capteurs_table(self):
        """Met à jour le tableau des capteurs"""
        self.capteurs_table.setRowCount(0)  # Effacer le tableau
        
        for row, (name, data) in enumerate(self.capteurs.items()):
            self.capteurs_table.insertRow(row)
            
            # Nom du capteur
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)  # Non éditable
            self.capteurs_table.setItem(row, 0, name_item)
            
            # Chemin du fichier
            file_item = QTableWidgetItem(os.path.basename(data["file_path"]))
            file_item.setToolTip(data["file_path"])
            file_item.setFlags(file_item.flags() & ~Qt.ItemIsEditable)  # Non éditable
            self.capteurs_table.setItem(row, 1, file_item)
            
            # Date d'import
            date_item = QTableWidgetItem(data["imported_at"])
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)  # Non éditable
            self.capteurs_table.setItem(row, 2, date_item)
            
            # Boutons d'action
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 0, 5, 0)
            
            # Bouton de suppression
            delete_button = PushButton()
            delete_button.setIcon(FluentIcon.DELETE)
            delete_button.setToolTip("Supprimer ce capteur")
            delete_button.clicked.connect(lambda checked, n=name: self.delete_capteur(n))
            action_layout.addWidget(delete_button)
            
            # Bouton d'édition
            edit_button = PushButton()
            edit_button.setIcon(FluentIcon.EDIT)
            edit_button.setToolTip("Modifier ce capteur")
            edit_button.clicked.connect(lambda checked, n=name: self.edit_capteur(n))
            action_layout.addWidget(edit_button)
            
            self.capteurs_table.setCellWidget(row, 3, action_widget)
            
        # Ajuster la taille des colonnes
        self.capteurs_table.resizeColumnsToContents()
        self.capteurs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
    def delete_capteur(self, capteur_name):
        """Supprime un capteur de la liste"""
        # Demander confirmation
        dialog = MessageBox(
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer le capteur '{capteur_name}'?",
            self
        )
        
        yes_button = dialog.addButton("Oui", MessageBox.ButtonRole.YesRole)
        no_button = dialog.addButton("Non", MessageBox.ButtonRole.NoRole)
        
        dialog.exec()
        
        if dialog.clickedButton() == yes_button:
            # Supprimer le capteur
            if capteur_name in self.capteurs:
                del self.capteurs[capteur_name]
                
                # Mettre à jour le tableau
                self.update_capteurs_table()
                
                # Sauvegarder les capteurs
                self.save_capteurs()
                
                # Afficher un message de succès
                InfoBar.success(
                    title="Succès",
                    content=f"Le capteur '{capteur_name}' a été supprimé avec succès.",
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=3000
                )
                
    def edit_capteur(self, capteur_name):
        """Édite un capteur existant"""
        if capteur_name in self.capteurs:
            # Remplir les champs avec les valeurs actuelles
            self.capteur_name_input.setText(capteur_name)
            self.file_path_input.setText(self.capteurs[capteur_name]["file_path"])
            
            # Supprimer l'ancien capteur
            del self.capteurs[capteur_name]
            
            # Mettre à jour le tableau
            self.update_capteurs_table()
            # Afficher un message
            InfoBar(
                icon=FluentIcon.INFO,
                title="Édition",
                content=f"Modifiez les informations du capteur '{capteur_name}' puis cliquez sur 'Ajouter'.",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=5000
            )

    def save_capteurs(self):
        """Sauvegarde les capteurs dans un fichier JSON"""
        try:
            # Créer le dossier de données s'il n'existe pas
            os.makedirs("data", exist_ok=True)
            
            # Sauvegarder les capteurs
            with open("data/capteurs.json", "w") as f:
                json.dump({"capteurs": self.capteurs}, f, indent=2)
                
        except Exception as e:
            InfoBar.error(
                title="Erreur",
                content=f"Impossible de sauvegarder les capteurs: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP
            )
            
    def load_capteurs(self):
        """Charge les capteurs depuis un fichier JSON"""
        try:
            # Vérifier si le fichier existe
            if os.path.exists("data/capteurs.json"):
                with open("data/capteurs.json", "r") as f:
                    data = json.load(f)
                    self.capteurs = data.get("capteurs", {})
                    
                # Mettre à jour le tableau
                self.update_capteurs_table()
                
        except Exception as e:
            InfoBar.error(
                title="Erreur",
                content=f"Impossible de charger les capteurs: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP
            )

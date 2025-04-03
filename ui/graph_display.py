from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread, QRunnable, QThreadPool
from PyQt5.QtGui import QIcon

from qfluentwidgets import (ScrollArea, PrimaryPushButton, ComboBox, 
                           LineEdit, PushButton, FluentIcon, 
                           InfoBar, InfoBarPosition, MessageBox,
                           CheckBox, ProgressBar, ProgressRing)

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import os
import json
import pandas as pd
import numpy as np
import random
from datetime import datetime

# Import du worker pour le threading
from utils.worker import Worker

class GraphDisplayPage(ScrollArea):
    def __init__(self, parent=None):
        """Page d'affichage et de génération des graphiques"""
        super().__init__(parent=parent)
        self.parent = parent
        self.setup_ui()
        self.load_styles()  # Ajouter cette ligne
        self.load_capteurs()  # Charger les capteurs existants
        
    def load_styles(self):
        """Charge les styles QSS spécifiques à la page des graphiques"""
        styles_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "styles")
        graph_style_path = os.path.join(styles_dir, "graphs.qss")
        
        if os.path.exists(graph_style_path):
            with open(graph_style_path, "r") as f:
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
        self.title_label = QLabel("📊 Graphiques")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 5px;")
        self.header_layout.addWidget(self.title_label)
        
        # Sous-titre
        self.subtitle_label = QLabel("Générez et visualisez des graphiques à partir de vos données")
        self.subtitle_label.setStyleSheet("font-size: 14px; color: gray;")
        self.header_layout.addWidget(self.subtitle_label)
        
        # Ajout de l'en-tête au layout principal
        self.main_layout.addWidget(self.header_widget)
        
        # Contrôles de génération de graphique
        self.controls_widget = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_widget)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sélection des capteurs
        self.capteur_selector_widget = QWidget()
        self.capteur_selector_layout = QHBoxLayout(self.capteur_selector_widget)
        self.capteur_selector_layout.setContentsMargins(0, 0, 0, 0)
        
        self.capteur_label = QLabel("Sélectionnez les capteurs:")
        self.capteur_selector_layout.addWidget(self.capteur_label)
        
        self.capteur_checkboxes = QWidget()
        self.capteur_checkboxes_layout = QVBoxLayout(self.capteur_checkboxes)
        self.capteur_checkboxes_layout.setContentsMargins(0, 0, 0, 0)
        self.capteur_selector_layout.addWidget(self.capteur_checkboxes)
        
        self.controls_layout.addWidget(self.capteur_selector_widget)
        
        # Type de graphique
        self.graph_type_widget = QWidget()
        self.graph_type_layout = QHBoxLayout(self.graph_type_widget)
        self.graph_type_layout.setContentsMargins(0, 0, 0, 0)
        
        self.graph_type_label = QLabel("Type de graphique:")
        self.graph_type_layout.addWidget(self.graph_type_label)
        
        self.graph_type_combo = ComboBox()
        self.graph_type_combo.addItems([
            "Température moyenne par mois",
            "Humidité moyenne par mois",
            "Température et humidité",
            "Comparaison entre capteurs"
        ])
        self.graph_type_layout.addWidget(self.graph_type_combo)
        
        self.controls_layout.addWidget(self.graph_type_widget)
        
        # Boutons de génération et d'export
        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.generate_button = PrimaryPushButton("Générer le graphique")
        self.generate_button.setIcon(FluentIcon.VIEW)
        self.generate_button.clicked.connect(self.generate_graph)
        self.buttons_layout.addWidget(self.generate_button)
        
        self.export_button = PushButton("Exporter")
        self.export_button.setIcon(FluentIcon.SAVE)
        self.export_button.clicked.connect(self.export_graph)
        self.export_button.setEnabled(False)  # Désactivé jusqu'à ce qu'un graphique soit généré
        self.buttons_layout.addWidget(self.export_button)
        
        self.controls_layout.addWidget(self.buttons_widget)
        
        # Indicateur de progression
        self.progress_widget = QWidget()
        self.progress_layout = QHBoxLayout(self.progress_widget)
        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        
        self.progress_bar = ProgressBar()
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        self.progress_layout.addWidget(self.progress_bar)
        
        self.controls_layout.addWidget(self.progress_widget)
        
        self.main_layout.addWidget(self.controls_widget)
        
        # Zone d'affichage du graphique
        self.graph_widget = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_widget)
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        
        # Figure matplotlib
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.graph_layout.addWidget(self.canvas)
        
        # Barre d'outils matplotlib
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_layout.addWidget(self.toolbar)
        
        self.main_layout.addWidget(self.graph_widget)
        
        # Zone de remarques
        self.notes_label = QLabel("💬 Remarques:")
        self.notes_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.main_layout.addWidget(self.notes_label)
        
        self.notes_text = QLabel(
            "- Les graphiques sont générés à partir des données des capteurs sélectionnés.\n"
            "- Vous pouvez exporter les graphiques au format PNG ou PDF.\n"
            "- Utilisez la barre d'outils pour zoomer, déplacer ou personnaliser le graphique."
        )
        self.notes_text.setStyleSheet("color: #505050; line-height: 150%;")
        self.main_layout.addWidget(self.notes_text)
        
    def load_capteurs(self):
        """Charge les capteurs depuis un fichier JSON"""
        try:
            # Vérifier si le fichier existe
            if os.path.exists("data/capteurs.json"):
                with open("data/capteurs.json", "r") as f:
                    data = json.load(f)
                    self.capteurs = data.get("capteurs", {})
                    
                # Mettre à jour les checkboxes
                self.update_capteur_checkboxes()
                
        except Exception as e:
            InfoBar.error(
                title="Erreur",
                content=f"Impossible de charger les capteurs: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP
            )
            
    def update_capteur_checkboxes(self):
        """Met à jour les checkboxes des capteurs"""
        # Effacer les checkboxes existantes
        for i in reversed(range(self.capteur_checkboxes_layout.count())):
            widget = self.capteur_checkboxes_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        # Ajouter une checkbox pour chaque capteur
        if not self.capteurs:
            no_capteur_label = QLabel("Aucun capteur disponible")
            self.capteur_checkboxes_layout.addWidget(no_capteur_label)
            return
            
        for capteur_name in self.capteurs.keys():
            checkbox = CheckBox(capteur_name)
            self.capteur_checkboxes_layout.addWidget(checkbox)
            
    def get_selected_capteurs(self):
        """Récupère les capteurs sélectionnés"""
        selected_capteurs = []
        
        for i in range(self.capteur_checkboxes_layout.count()):
            widget = self.capteur_checkboxes_layout.itemAt(i).widget()
            if isinstance(widget, CheckBox) and widget.isChecked():
                selected_capteurs.append(widget.text())
                
        return selected_capteurs
        
    def generate_graph(self):
        """Génère un graphique à partir des données des capteurs sélectionnés"""
        # Récupérer les capteurs sélectionnés
        selected_capteurs = self.get_selected_capteurs()
        
        if not selected_capteurs:
            InfoBar.warning(
                title="Attention",
                content="Veuillez sélectionner au moins un capteur.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return
            
        # Récupérer le type de graphique
        graph_type = self.graph_type_combo.currentText()
        
        # Afficher la barre de progression
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        
        # Désactiver le bouton de génération pendant le traitement
        self.generate_button.setEnabled(False)
        
        # Créer un worker pour générer le graphique en arrière-plan
        worker = Worker(self.generate_graph_worker, selected_capteurs, graph_type)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.result.connect(self.display_graph)
        worker.signals.finished.connect(self.on_graph_generation_finished)
        worker.signals.error.connect(self.on_graph_generation_error)
        
        # Exécuter le worker
        self.thread_pool.start(worker)
        
    def generate_graph_worker(self, selected_capteurs, graph_type, progress_callback):
        """Fonction de génération de graphique exécutée dans un thread séparé"""
        try:
            # Simuler un chargement
            for i in range(0, 101, 10):
                progress_callback.emit(i)
                QThread.msleep(100)  # Pause pour simuler un traitement
                
            # Effacer la figure existante
            self.figure.clear()
            
            # Créer un subplot
            ax = self.figure.add_subplot(111)
            
            # Générer des données simulées selon le type de graphique
            if graph_type == "Température moyenne par mois":
                self.generate_temperature_by_month(ax, selected_capteurs)
            elif graph_type == "Humidité moyenne par mois":
                self.generate_humidity_by_month(ax, selected_capteurs)
            elif graph_type == "Température et humidité":
                self.generate_temperature_humidity(ax, selected_capteurs)
            elif graph_type == "Comparaison entre capteurs":
                self.generate_capteurs_comparison(ax, selected_capteurs)
                
            # Ajuster la mise en page
            self.figure.tight_layout()
            
            return True
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du graphique: {str(e)}")
            
    def generate_temperature_by_month(self, ax, selected_capteurs):
        """Génère un graphique de température moyenne par mois"""
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
        
        for capteur in selected_capteurs:
            # Générer des données aléatoires pour la simulation
            temperatures = [random.uniform(5, 30) for _ in range(12)]
            ax.bar(months, temperatures, alpha=0.7, label=capteur)
            
        ax.set_title('Température moyenne par mois')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Température (°C)')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        
    def generate_humidity_by_month(self, ax, selected_capteurs):
        """Génère un graphique d'humidité moyenne par mois"""
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
        
        for capteur in selected_capteurs:
            # Générer des données aléatoires pour la simulation
            humidity = [random.uniform(30, 90) for _ in range(12)]
            ax.plot(months, humidity, marker='o', linewidth=2, label=capteur)
            
        ax.set_title('Humidité moyenne par mois')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Humidité (%)')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        
    def generate_temperature_humidity(self, ax, selected_capteurs):
        """Génère un graphique de température et humidité"""
        days = list(range(1, 31))
        
        for capteur in selected_capteurs:
            # Générer des données aléatoires pour la simulation
            temperatures = [random.uniform(15, 30) for _ in range(30)]
            
            # Créer un deuxième axe pour l'humidité
            ax2 = ax.twinx()
            
            # Tracer la température
            line1, = ax.plot(days, temperatures, 'r-', label=f'{capteur} - Temp.')
            
            # Tracer l'humidité
            humidity = [random.uniform(40, 80) for _ in range(30)]
            line2, = ax2.plot(days, humidity, 'b-', label=f'{capteur} - Humid.')
            
            # Légendes
            lines = [line1, line2]
            ax.legend(lines, [l.get_label() for l in lines], loc='upper left')
            
            # Étiquettes
            ax.set_xlabel('Jour du mois')
            ax.set_ylabel('Température (°C)', color='r')
            ax2.set_ylabel('Humidité (%)', color='b')
            
            # Limites et grille
            ax.tick_params(axis='y', labelcolor='r')
            ax2.tick_params(axis='y', labelcolor='b')
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Titre
            ax.set_title(f'Température et humidité - {capteur}')
            
            # On ne traite que le premier capteur pour ce type de graphique
            break
            
    def generate_capteurs_comparison(self, ax, selected_capteurs):
        """Génère un graphique de comparaison entre capteurs"""
        # Générer des données aléatoires pour la simulation
        x = np.arange(len(selected_capteurs))
        width = 0.35
        
        # Température moyenne
        temp_means = [random.uniform(15, 25) for _ in range(len(selected_capteurs))]
        rects1 = ax.bar(x - width/2, temp_means, width, label='Température moyenne (°C)')
        
        # Humidité moyenne
        humidity_means = [random.uniform(50, 70) for _ in range(len(selected_capteurs))]
        rects2 = ax.bar(x + width/2, humidity_means, width, label='Humidité moyenne (%)')
        
        # Ajouter du texte, des étiquettes, etc.
        ax.set_title('Comparaison entre capteurs')
        ax.set_xticks(x)
        ax.set_xticklabels(selected_capteurs)
        ax.legend()
        
        # Ajouter les valeurs sur les barres
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.1f}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points de décalage vertical
                            textcoords="offset points",
                            ha='center', va='bottom')
                            
        autolabel(rects1)
        autolabel(rects2)
        
    def update_progress(self, value):
        """Met à jour la barre de progression"""
        self.progress_bar.setValue(value)
        
    def display_graph(self, result):
        """Affiche le graphique généré"""
        # Mettre à jour le canvas
        self.canvas.draw()
        
        # Activer le bouton d'export
        self.export_button.setEnabled(True)
        
    def on_graph_generation_finished(self):
        """Appelé lorsque la génération du graphique est terminée"""
        # Réactiver le bouton de génération
        self.generate_button.setEnabled(True)
        
        # Masquer la barre de progression
        self.progress_bar.hide()
        
        # Afficher un message de succès
        InfoBar.success(
            title="Succès",
            content="Le graphique a été généré avec succès.",
            parent=self,
            position=InfoBarPosition.TOP,
            duration=3000
        )
        
    def on_graph_generation_error(self, error):
        """Appelé en cas d'erreur lors de la génération du graphique"""
        # Réactiver le bouton de génération
        self.generate_button.setEnabled(True)
        
        # Masquer la barre de progression
        self.progress_bar.hide()
        
        # Afficher un message d'erreur
        InfoBar.error(
            title="Erreur",
            content=str(error),
            parent=self,
            position=InfoBarPosition.TOP
        )
        
    def export_graph(self):
        """Exporte le graphique actuel"""
        # Ouvrir une boîte de dialogue pour sélectionner le fichier de destination
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter le graphique",
            os.path.join(os.getcwd(), "output/exports", f"graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            "Images PNG (*.png);;Documents PDF (*.pdf);;Tous les fichiers (*.*)"
        )
        
        if file_path:
            try:
                # Créer le dossier de destination s'il n'existe pas
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Exporter le graphique
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                
                # Afficher un message de succès
                InfoBar.success(
                    title="Succès",
                    content=f"Le graphique a été exporté avec succès vers {file_path}",
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=3000
                )
                
            except Exception as e:
                InfoBar.error(
                    title="Erreur",
                    content=f"Impossible d'exporter le graphique: {str(e)}",
                    parent=self,
                    position=InfoBarPosition.TOP
                )

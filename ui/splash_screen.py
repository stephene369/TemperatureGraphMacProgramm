from PyQt5.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QProgressBar, QWidget
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QColor, QPainter, QFont
from qfluentwidgets import (FluentIcon, SplashScreen as FWSpashScreen, 
                           ProgressRing, TransparentPushButton, setTheme, Theme)

class SplashScreen(QSplashScreen):
    def __init__(self):
        """Écran de démarrage animé avec barre de progression"""
        # Création d'un pixmap pour le splash screen
        pixmap = QPixmap(500, 400)
        pixmap.fill(Qt.transparent)
        super().__init__(pixmap, Qt.WindowStaysOnTopHint)
        
        # Configuration du widget central
        self.central_widget = QWidget(self)
        self.central_widget.setGeometry(0, 0, 500, 400)
        
        # Mise en place du layout
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)
        
        # Titre de l'application
        self.title_label = QLabel("ClimaGraph", self.central_widget)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-family: 'Segoe UI';
            font-size: 36px;
            font-weight: bold;
            color: #0078D7;
        """)
        layout.addWidget(self.title_label)
        
        # Sous-titre
        self.subtitle_label = QLabel("Analyse de données climatiques", self.central_widget)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            font-family: 'Segoe UI';
            font-size: 16px;
            color: #505050;
        """)
        layout.addWidget(self.subtitle_label)
        
        # Espace
        layout.addSpacing(20)
        
        # Anneau de progression
        self.progress_ring = ProgressRing(self.central_widget)
        self.progress_ring.setFixedSize(80, 80)
        layout.addWidget(self.progress_ring, 0, Qt.AlignCenter)
        
        # Message de chargement
        self.loading_label = QLabel("Chargement...", self.central_widget)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            font-family: 'Segoe UI';
            font-size: 14px;
            color: #505050;
        """)
        layout.addWidget(self.loading_label)
        
        # Animation de chargement
        self.counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_loading_text)
        self.timer.start(400)
        
        # Positionnement au centre de l'écran
        self.setMask(pixmap.mask())
        
    def _update_loading_text(self):
        """Met à jour le texte de chargement avec une animation"""
        loading_texts = [
            "Chargement.",
            "Chargement..",
            "Chargement...",
            "Chargement...."
        ]
        self.loading_label.setText(loading_texts[self.counter % 4])
        self.counter += 1
        
    def paintEvent(self, event):
        """Personnalisation du rendu du splash screen"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fond avec coins arrondis
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        
        super().paintEvent(event)

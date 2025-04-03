import logging
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class Logger:
    """Classe pour gérer la journalisation de l'application"""
    
    _logger = None
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Récupère ou crée l'instance du logger"""
        if cls._logger is None:
            cls._setup_logger()
        return cls._logger
    
    @classmethod
    def _setup_logger(cls) -> None:
        """Configure le logger avec les handlers appropriés"""
        # Créer le logger
        logger = logging.getLogger("ClimaGraph")
        logger.setLevel(logging.DEBUG)
        
        # Éviter les doublons de handlers
        if logger.handlers:
            return
        
        # Créer le dossier de logs
        log_dir = Path.home() / '.climagraph' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Nom du fichier de log avec date
        log_file = log_dir / f"climagraph_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Handler pour le fichier
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Handler pour la console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formateur pour les messages
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Ajouter les handlers au logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Stocker l'instance
        cls._logger = logger
        
        logger.info("Logger initialisé")
    
    @classmethod
    def set_level(cls, level: int) -> None:
        """Définit le niveau de journalisation"""
        logger = cls.get_logger()
        logger.setLevel(level)
        
        # Mettre à jour le niveau du handler de console
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                handler.setLevel(level)

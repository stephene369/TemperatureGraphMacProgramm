"""
Module de journalisation pour l'application ClimaGraph
"""

import os
import logging
from datetime import datetime

# Configurer le logger
logger = logging.getLogger('climagraph')
logger.setLevel(logging.DEBUG)

# Créer le dossier de logs s'il n'existe pas
os.makedirs('logs', exist_ok=True)

# Handler pour les fichiers
file_handler = logging.FileHandler(f'logs/climagraph_{datetime.now().strftime("%Y%m%d")}.log')
file_handler.setLevel(logging.DEBUG)

# Handler pour la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formateur
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Ajouter les handlers au logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_info(message):
    """Enregistre un message d'information"""
    logger.info(message)

def log_warning(message):
    """Enregistre un avertissement"""
    logger.warning(message)

def log_error(message):
    """Enregistre une erreur"""
    logger.error(message)

def log_debug(message):
    """Enregistre un message de débogage"""
    logger.debug(message)

def log_exception(e):
    """Enregistre une exception"""
    logger.exception(f"Exception: {str(e)}")

"""
Fonctions de validation pour l'application ClimaGraph
"""

import os
import pandas as pd
from datetime import datetime

def is_valid_file_path(file_path):
    """Vérifie si le chemin de fichier est valide"""
    return os.path.exists(file_path) and os.path.isfile(file_path)

def is_valid_excel_file(file_path):
    """Vérifie si le fichier est un fichier Excel valide"""
    if not file_path.endswith(('.xlsx', '.xls')):
        return False
        
    try:
        # Tenter de lire le fichier avec pandas
        pd.read_excel(file_path, nrows=1)
        return True
    except Exception:
        return False

def is_valid_hobo_file(file_path):
    """Vérifie si le fichier est un fichier HOBO valide"""
    if not file_path.endswith('.hobo'):
        return False
        
    try:
        # Vérification basique du contenu du fichier
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_lines = [f.readline() for _ in range(5)]
            # Vérifier si le fichier contient des marqueurs typiques des fichiers HOBO
            return any('HOBO' in line for line in first_lines)
    except Exception:
        return False

def is_valid_date_column(df, column_name):
    """Vérifie si la colonne contient des dates valides"""
    try:
        # Tenter de convertir la colonne en datetime
        pd.to_datetime(df[column_name])
        return True
    except Exception:
        return False

def is_valid_numeric_column(df, column_name):
    """Vérifie si la colonne contient des valeurs numériques"""
    try:
        # Vérifier si la colonne peut être convertie en numérique
        pd.to_numeric(df[column_name])
        return True
    except Exception:
        return False

def validate_capteur_name(name, existing_names=None):
    """Valide le nom d'un capteur"""
    if not name or len(name.strip()) == 0:
        return False, "Le nom du capteur ne peut pas être vide."
        
    if existing_names is not None and name in existing_names:
        return False, f"Le capteur '{name}' existe déjà."
        
    return True, ""

def validate_column_mapping(mapping):
    """Valide le mappage des colonnes"""
    required_types = ["date", "temperature", "humidity"]
    
    # Vérifier que tous les types requis sont présents
    for req_type in required_types:
        if req_type not in mapping or not mapping[req_type]:
            return False, f"Le type de données '{req_type}' n'est pas mappé."
            
    return True, ""

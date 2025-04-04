"""
Module Utils - Fonctions utilitaires
"""
import uuid
import datetime
import os

def add_history_entry(history, action, capteur_id=None, details=None, capteurs=None):
    """
    Ajouter une entrée à l'historique
    
    Args:
        history (list): Liste des entrées d'historique
        action (str): Action effectuée
        capteur_id (str, optional): ID du capteur concerné
        details (dict, optional): Détails supplémentaires
        capteurs (dict, optional): Dictionnaire des capteurs pour récupérer le nom
        
    Returns:
        dict: L'entrée ajoutée
    """
    capteur_nom = None
    if capteur_id and capteurs and capteur_id in capteurs:
        capteur_nom = capteurs[capteur_id]["nom"]
    
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "capteur_id": capteur_id,
        "capteur_nom": capteur_nom,
        "details": details
    }
    
    history.append(entry)
    return entry

def format_date(date_obj, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Formater une date en chaîne de caractères
    
    Args:
        date_obj (datetime.datetime): Objet date à formater
        format_str (str, optional): Format de date. Par défaut: "%Y-%m-%d %H:%M:%S"
        
    Returns:
        str: Date formatée
    """
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.datetime.fromisoformat(date_obj)
        except ValueError:
            return date_obj
    
    if isinstance(date_obj, datetime.datetime):
        return date_obj.strftime(format_str)
    
    return str(date_obj)

def generate_unique_filename(prefix, extension, timestamp=True):
    """
    Générer un nom de fichier unique
    
    Args:
        prefix (str): Préfixe du nom de fichier
        extension (str): Extension du fichier (sans le point)
        timestamp (bool, optional): Ajouter un timestamp. Par défaut: True
        
    Returns:
        str: Nom de fichier unique
    """
    unique_id = str(uuid.uuid4())[:8]
    
    if timestamp:
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp_str}_{unique_id}.{extension}"
    else:
        return f"{prefix}_{unique_id}.{extension}"

def sanitize_filename(filename):
    """
    Nettoyer un nom de fichier pour le rendre valide
    
    Args:
        filename (str): Nom de fichier à nettoyer
        
    Returns:
        str: Nom de fichier nettoyé
    """
    # Remplacer les caractères invalides
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limiter la longueur
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename




def json_serialize(obj):
    """
    Convertit les objets non sérialisables en JSON en types sérialisables
    
    Args:
        obj: Objet à convertir
        
    Returns:
        Objet sérialisable en JSON
    """
    import pandas as pd
    import numpy as np
    import datetime
    
    if isinstance(obj, (pd.Timestamp, datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    else:
        return str(obj)

"""
Module Storage - Gestion du stockage des données
"""
import os
import json
import pandas as pd
import numpy as np
import datetime

class Storage:
    """
    Classe pour gérer le stockage persistant des données
    """
    def __init__(self, data_dir):
        """
        Initialise le gestionnaire de stockage
        
        Args:
            data_dir (str): Chemin du répertoire de données
        """
        self.data_dir = data_dir
        self.storage_file = os.path.join(data_dir, 'storage.json')
        self.history_file = os.path.join(data_dir, 'history.json')
    
    def load_capteurs(self):
        """
        Charger les données des capteurs depuis le fichier de stockage
        
        Returns:
            dict: Données des capteurs
        """
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("capteurs", {})
            except Exception as e:
                print(f"Erreur lors du chargement du stockage: {e}")
                return {}
        else:
            return {}
        
    def save_capteurs(self, capteurs):
        """
        Sauvegarder les données des capteurs
        
        Args:
            capteurs (dict): Données des capteurs à sauvegarder
            
        Returns:
            bool: True si la sauvegarde a réussi, False sinon
        """
        try:
            # Fonction pour convertir les objets non-sérialisables
            def json_serializable(obj):
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
                elif pd.isna(obj):
                    return None
                return obj
                
            # Créer la structure complète
            data = {"capteurs": capteurs}
            
            # Sauvegarder dans le fichier avec l'encodeur personnalisé
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=json_serializable)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du stockage: {e}")
            return False
    
    def load_history(self):
        """
        Charger l'historique depuis le fichier JSON
        
        Returns:
            list: Liste des entrées d'historique
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de l'historique: {e}")
                return []
        else:
            return []
    
    def save_history(self, history):
        """
        Sauvegarder l'historique dans le fichier JSON
        
        Args:
            history (list): Liste des entrées d'historique à sauvegarder
            
        Returns:
            bool: True si la sauvegarde a réussi, False sinon
        """
        try:
            # Fonction pour convertir les objets non-sérialisables
            def json_serializable(obj):
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
                elif pd.isna(obj):
                    return None
                return obj
            
            # Convertir les objets non sérialisables
            def prepare_for_json(item):
                if isinstance(item, dict):
                    return {k: prepare_for_json(v) for k, v in item.items()}
                elif isinstance(item, list):
                    return [prepare_for_json(i) for i in item]
                else:
                    return json_serializable(item)
            
            # Préparer l'historique pour la sérialisation
            prepared_history = prepare_for_json(history)
            
            # Sauvegarder dans le fichier
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(prepared_history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique: {e}")
            return False

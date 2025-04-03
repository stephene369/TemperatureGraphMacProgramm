import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import datetime
from services.logger import Logger

logger = Logger.get_logger()

class StorageManager:
    """Classe pour gérer le stockage persistant des données"""
    
    def __init__(self, storage_file: str = None):
        # Définir le fichier de stockage
        if storage_file:
            self.storage_file = Path(storage_file)
        else:
            # Utiliser un emplacement par défaut dans le dossier de l'utilisateur
            self.storage_file = Path.home() / '.climagraph' / 'storage.json'
        
        # Créer le dossier parent s'il n'existe pas
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Créer le fichier s'il n'existe pas
        if not self.storage_file.exists():
            self._initialize_storage()
    
    def _initialize_storage(self) -> None:
        """Initialise le fichier de stockage avec une structure vide"""
        initial_data = {
            "capteurs": [],
            "app_settings": {
                "last_export_dir": "",
                "theme": "light",
                "language": "fr"
            },
            "version": "1.0.0",
            "last_updated": datetime.datetime.now().isoformat()
        }
        
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Fichier de stockage initialisé: {self.storage_file}")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du stockage: {str(e)}")
    
    def _load_data(self) -> Dict[str, Any]:
        """Charge les données depuis le fichier de stockage"""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            logger.warning(f"Fichier de stockage non trouvé: {self.storage_file}")
            self._initialize_storage()
            return self._load_data()
        except json.JSONDecodeError:
            logger.error(f"Erreur de décodage JSON: {self.storage_file}")
            # Sauvegarder une copie du fichier corrompu
            if self.storage_file.exists():
                backup_file = self.storage_file.with_suffix('.json.bak')
                self.storage_file.rename(backup_file)
                logger.info(f"Fichier corrompu sauvegardé: {backup_file}")
            
            self._initialize_storage()
            return self._load_data()
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {str(e)}")
            return {
                "capteurs": [],
                "app_settings": {},
                "version": "1.0.0",
                "last_updated": datetime.datetime.now().isoformat()
            }
    
    def _save_data(self, data: Dict[str, Any]) -> bool:
        """Sauvegarde les données dans le fichier de stockage"""
        try:
            # Mettre à jour la date de dernière modification
            data["last_updated"] = datetime.datetime.now().isoformat()
            
            # Sauvegarder les données
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des données: {str(e)}")
            return False
    
    def load_capteurs(self) -> List[Dict[str, Any]]:
        """Charge la liste des capteurs"""
        data = self._load_data()
        return data.get("capteurs", [])
    
    def save_capteurs(self, capteurs: List[Dict[str, Any]]) -> bool:
        """Sauvegarde la liste des capteurs"""
        data = self._load_data()
        data["capteurs"] = capteurs
        return self._save_data(data)
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Récupère un paramètre de l'application"""
        data = self._load_data()
        return data.get("app_settings", {}).get(key, default)
    
    def save_setting(self, key: str, value: Any) -> bool:
        """Sauvegarde un paramètre de l'application"""
        data = self._load_data()
        
        if "app_settings" not in data:
            data["app_settings"] = {}
        
        data["app_settings"][key] = value
        return self._save_data(data)
    
    def clear_storage(self) -> bool:
        """Réinitialise le stockage (pour les tests ou la réinitialisation)"""
        try:
            self._initialize_storage()
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la réinitialisation du stockage: {str(e)}")
            return False

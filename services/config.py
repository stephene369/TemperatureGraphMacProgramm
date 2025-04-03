import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
from services.logger import Logger

logger = Logger.get_logger()

class Config:
    """Classe pour gérer la configuration de l'application"""
    
    def __init__(self, config_file: str = None):
        # Configuration par défaut
        self.default_config = {
            "app_name": "ClimaGraph",
            "version": "1.0.0",
            "debug": False,
            "output_dir": "output/exports",
            "theme": "light",
            "language": "fr",
            "max_recent_files": 10,
            "auto_save": True,
            "graph_dpi": 100,
            "date_format": "%d/%m/%Y %H:%M:%S"
        }
        
        # Définir le fichier de configuration
        if config_file:
            self.config_file = Path(config_file)
        else:
            # Utiliser un emplacement par défaut dans le dossier de l'application
            self.config_file = Path(__file__).parent.parent / "config.json"
        
        # Charger la configuration
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration depuis le fichier"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Fusionner avec la configuration par défaut
                merged_config = self.default_config.copy()
                merged_config.update(config)
                
                logger.info(f"Configuration chargée depuis {self.config_file}")
                return merged_config
            else:
                # Créer le fichier de configuration avec les valeurs par défaut
                self._save_config(self.default_config)
                return self.default_config
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration: {str(e)}")
            return self.default_config
    
    def _save_config(self, config: Dict[str, Any]) -> bool:
        """Sauvegarde la configuration dans le fichier"""
        try:
            # Créer le dossier parent s'il n'existe pas
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Configuration sauvegardée dans {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration: {str(e)}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Définit une valeur de configuration et la sauvegarde"""
        self.config[key] = value
        return self._save_config(self.config)
    
    def update(self, config_dict: Dict[str, Any]) -> bool:
        """Met à jour plusieurs valeurs de configuration et les sauvegarde"""
        self.config.update(config_dict)
        return self._save_config(self.config)
    
    def reset(self) -> bool:
        """Réinitialise la configuration aux valeurs par défaut"""
        self.config = self.default_config.copy()
        return self._save_config(self.config)

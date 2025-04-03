import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import traceback
from pathlib import Path

from core.models import Capteur, Dataset, AppState, GraphConfig
from core.file_loader import FileLoader
from core.column_detector import ColumnDetector
from core.graph_generator import GraphGenerator
from services.storage import StorageManager
from services.config import Config
from services.logger import Logger

logger = Logger.get_logger()

class ClimaGraphAPI:
    """API pour la communication entre Python et JavaScript"""
    
    def __init__(self, app_state: AppState, storage: StorageManager, config: Config):
        self.app_state = app_state
        self.storage = storage
        self.config = config
        self.file_loader = FileLoader()
        self.column_detector = ColumnDetector()
        self.graph_generator = GraphGenerator()
        
        # Charger les capteurs existants
        self._load_capteurs()
    
    def _load_capteurs(self) -> None:
        """Charge les capteurs depuis le stockage"""
        try:
            capteurs_data = self.storage.load_capteurs()
            for capteur_data in capteurs_data:
                capteur = Capteur.from_dict(capteur_data)
                self.app_state.add_capteur(capteur)
            
            logger.info(f"Chargement de {len(capteurs_data)} capteurs depuis le stockage")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des capteurs: {str(e)}")
    
    def _save_capteurs(self) -> None:
        """Sauvegarde les capteurs dans le stockage"""
        try:
            capteurs_data = [capteur.to_dict() for capteur in self.app_state.capteurs.values()]
            self.storage.save_capteurs(capteurs_data)
            logger.info(f"Sauvegarde de {len(capteurs_data)} capteurs dans le stockage")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des capteurs: {str(e)}")
    
    def get_capteurs(self) -> Dict[str, Any]:
        """Récupère la liste des capteurs"""
        try:
            capteurs = [capteur.to_dict() for capteur in self.app_state.capteurs.values()]
            return {"success": True, "capteurs": capteurs}
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des capteurs: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def add_capteur(self, nom: str) -> Dict[str, Any]:
        """Ajoute un nouveau capteur"""
        try:
            # Vérifier si le nom existe déjà
            for capteur in self.app_state.capteurs.values():
                if capteur.nom.lower() == nom.lower():
                    return {"success": False, "message": f"Un capteur avec le nom '{nom}' existe déjà"}
            
            # Créer un nouveau capteur
            capteur = Capteur(nom=nom)
            self.app_state.add_capteur(capteur)
            
            # Sauvegarder les capteurs
            self._save_capteurs()
            
            return {"success": True, "capteur": capteur.to_dict()}
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du capteur: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def update_capteur(self, capteur_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour un capteur existant"""
        try:
            capteur = self.app_state.get_capteur(capteur_id)
            if not capteur:
                return {"success": False, "message": f"Capteur avec ID {capteur_id} non trouvé"}
            
            # Mettre à jour les champs
            if "nom" in data:
                capteur.nom = data["nom"]
            if "file_path" in data:
                capteur.file_path = data["file_path"]
            if "columns" in data:
                capteur.columns = data["columns"]
            
            # Mettre à jour la date d'importation si un fichier est associé
            if "file_path" in data and data["file_path"]:
                capteur.imported_at = datetime.now()
            
            # Sauvegarder les capteurs
            self._save_capteurs()
            
            return {"success": True, "capteur": capteur.to_dict()}
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du capteur: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def remove_capteur(self, capteur_id: str) -> Dict[str, Any]:
        """Supprime un capteur"""
        try:
            if self.app_state.remove_capteur(capteur_id):
                # Sauvegarder les capteurs
                self._save_capteurs()
                return {"success": True}
            else:
                return {"success": False, "message": f"Capteur avec ID {capteur_id} non trouvé"}
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du capteur: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def select_file(self) -> Dict[str, Any]:
        """Ouvre une boîte de dialogue pour sélectionner un fichier"""
        try:
            file_path = self.file_loader.select_file()
            if file_path:
                return {"success": True, "path": file_path}
            else:
                return {"success": False, "message": "Aucun fichier sélectionné"}
        except Exception as e:
            logger.error(f"Erreur lors de la sélection du fichier: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def load_file(self, capteur_id: str, file_path: str) -> Dict[str, Any]:
        """Charge un fichier et détecte les colonnes"""
        try:
            # Vérifier si le capteur existe
            capteur = self.app_state.get_capteur(capteur_id)
            if not capteur:
                return {"success": False, "message": f"Capteur avec ID {capteur_id} non trouvé"}
            
            # Charger le fichier
            df, file_type = self.file_loader.load_file(file_path)
            if df is None:
                return {"success": False, "message": "Format de fichier non pris en charge"}
            
            # Créer un dataset
            columns = df.columns.tolist()
            preview_data = df.head(5).to_dict(orient='records')
            
            dataset = Dataset(
                capteur_id=capteur_id,
                columns=columns,
                preview_data=preview_data,
                file_type=file_type,
                row_count=len(df)
            )
            
            # Mettre à jour l'état de l'application
            self.app_state.current_dataset = dataset
            self.app_state.current_capteur_id = capteur_id
            
            # Détecter automatiquement les colonnes
            detected_columns = self.column_detector.detect_columns(df)
            
            return {
                "success": True, 
                "columns": columns, 
                "preview": preview_data,
                "detected": detected_columns,
                "file_type": file_type,
                "row_count": len(df)
            }
        except Exception as e:
            logger.error(f"Erreur lors du chargement du fichier: {str(e)}")
            traceback.print_exc()
            return {"success": False, "message": str(e)}
    
    def save_column_mapping(self, capteur_id: str, mapping: Dict[str, str]) -> Dict[str, Any]:
        """Sauvegarde le mappage des colonnes pour un capteur"""
        try:
            # Vérifier si le capteur existe
            capteur = self.app_state.get_capteur(capteur_id)
            if not capteur:
                return {"success": False, "message": f"Capteur avec ID {capteur_id} non trouvé"}
            
            # Vérifier si un dataset est chargé
            if not self.app_state.current_dataset or self.app_state.current_capteur_id != capteur_id:
                return {"success": False, "message": "Aucun fichier chargé pour ce capteur"}
            
            # Mettre à jour le mappage des colonnes
            capteur.columns = mapping
            
            # Sauvegarder les capteurs
            self._save_capteurs()
            
            return {"success": True, "capteur": capteur.to_dict()}
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du mappage des colonnes: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def generate_graph(self, graph_config: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un graphique basé sur la configuration fournie"""
        try:
            # Créer une configuration de graphique
            config = GraphConfig(
                type=graph_config.get("type", "line"),
                title=graph_config.get("title", ""),
                x_axis=graph_config.get("x_axis", ""),
                y_axis=graph_config.get("y_axis", ""),
                capteur_ids=graph_config.get("capteur_ids", []),
                options=graph_config.get("options", {})
            )
            
            # Charger les données pour chaque capteur
            capteurs_data = []
            for capteur_id in config.capteur_ids:
                capteur = self.app_state.get_capteur(capteur_id)
                if not capteur or not capteur.file_path:
                    continue
                
                df, _ = self.file_loader.load_file(capteur.file_path)
                if df is not None:
                    capteurs_data.append((capteur, df))
            
            if not capteurs_data:
                return {"success": False, "message": "Aucune donnée disponible pour générer le graphique"}
            
            # Générer le graphique
            fig = self.graph_generator.generate_graph(config, capteurs_data)
            
            # Convertir le graphique en base64
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close(fig)
            
            return {
                "success": True, 
                "graphic": image_base64, 
                "type": config.type,
                "title": config.title
            }
        except Exception as e:
            logger.error(f"Erreur lors de la génération du graphique: {str(e)}")
            traceback.print_exc()
            return {"success": False, "message": str(e)}
    
    def export_graph(self, image_base64: str, file_name: str = None) -> Dict[str, Any]:
        """Exporte un graphique en fichier image"""
        try:
            # Créer le dossier d'exportation s'il n'existe pas
            output_dir = Path(self.config.get("output_dir", "output/exports"))
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Générer un nom de fichier s'il n'est pas fourni
            if not file_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"graph_{timestamp}.png"
            
            # Ajouter l'extension .png si nécessaire
            if not file_name.lower().endswith('.png'):
                file_name += '.png'
            
            # Chemin complet du fichier
            file_path = output_dir / file_name
            
            # Décoder l'image base64 et l'enregistrer
            image_data = base64.b64decode(image_base64)
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            return {"success": True, "path": str(file_path)}
        except Exception as e:
            logger.error(f"Erreur lors de l'exportation du graphique: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def get_app_info(self) -> Dict[str, Any]:
        """Récupère des informations sur l'application"""
        try:
            return {
                "success": True,
                "version": self.config.get("version", "1.0.0"),
                "app_name": self.config.get("app_name", "ClimaGraph"),
                "output_dir": str(Path(self.config.get("output_dir", "output/exports")))
            }
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des informations de l'application: {str(e)}")
            return {"success": False, "message": str(e)}

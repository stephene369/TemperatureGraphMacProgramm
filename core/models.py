from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import json

@dataclass
class Capteur:
    """Représente un capteur avec ses métadonnées"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nom: str = ""
    file_path: str = ""
    columns: Dict[str, str] = field(default_factory=dict)
    imported_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire pour la sérialisation"""
        return {
            "id": self.id,
            "nom": self.nom,
            "file_path": self.file_path,
            "columns": self.columns,
            "imported_at": self.imported_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Capteur':
        """Crée un objet Capteur à partir d'un dictionnaire"""
        capteur = cls(
            id=data.get("id", str(uuid.uuid4())),
            nom=data.get("nom", ""),
            file_path=data.get("file_path", ""),
            columns=data.get("columns", {})
        )
        
        # Convertir la chaîne de date en objet datetime
        if "imported_at" in data:
            try:
                capteur.imported_at = datetime.fromisoformat(data["imported_at"])
            except ValueError:
                capteur.imported_at = datetime.now()
        
        return capteur

@dataclass
class Dataset:
    """Représente un ensemble de données chargé"""
    capteur_id: str
    columns: List[str] = field(default_factory=list)
    preview_data: List[Dict[str, Any]] = field(default_factory=list)
    file_type: str = ""
    row_count: int = 0

@dataclass
class GraphConfig:
    """Configuration pour la génération d'un graphique"""
    type: str
    title: str = ""
    x_axis: str = ""
    y_axis: str = ""
    capteur_ids: List[str] = field(default_factory=list)
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AppState:
    """État global de l'application"""
    capteurs: Dict[str, Capteur] = field(default_factory=dict)
    current_dataset: Optional[Dataset] = None
    current_capteur_id: Optional[str] = None
    
    def add_capteur(self, capteur: Capteur) -> None:
        """Ajoute un capteur à la liste"""
        self.capteurs[capteur.id] = capteur
    
    def get_capteur(self, capteur_id: str) -> Optional[Capteur]:
        """Récupère un capteur par son ID"""
        return self.capteurs.get(capteur_id)
    
    def remove_capteur(self, capteur_id: str) -> bool:
        """Supprime un capteur par son ID"""
        if capteur_id in self.capteurs:
            del self.capteurs[capteur_id]
            return True
        return False
    
    def update_capteur(self, capteur: Capteur) -> None:
        """Met à jour un capteur existant"""
        self.capteurs[capteur.id] = capteur

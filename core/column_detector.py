import pandas as pd
from typing import Dict, List, Any
import re
from services.logger import Logger

logger = Logger.get_logger()

class ColumnDetector:
    """Classe pour détecter automatiquement les colonnes dans un DataFrame"""
    
    def __init__(self):
        # Mots-clés pour la détection des colonnes
        self.date_keywords = [
            'date', 'time', 'timestamp', 'datetime', 'horodatage', 
            'heure', 'temps', 'date/heure', 'date et heure'
        ]
        
        self.temp_keywords = [
            'temp', 'température', 'temperature', 't°', 't °c', 
            'temp °c', 'température °c', 'temperature °c'
        ]
        
        self.humidity_keywords = [
            'humid', 'humidité', 'humidity', 'hr', 'rh', 
            'humidité relative', 'relative humidity', 'h%'
        ]
    
    def detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """Détecte les colonnes de date, température et humidité dans un DataFrame"""
        try:
            result = {
                'date': None,
                'temperature': None,
                'humidity': None
            }
            
            # Convertir les noms de colonnes en minuscules pour la comparaison
            columns_lower = {col.lower(): col for col in df.columns}
            
            # Détecter la colonne de date
            date_col = self._find_column(columns_lower, self.date_keywords)
            if date_col:
                result['date'] = date_col
            
            # Détecter la colonne de température
            temp_col = self._find_column(columns_lower, self.temp_keywords)
            if temp_col:
                result['temperature'] = temp_col
            
            # Détecter la colonne d'humidité
            humidity_col = self._find_column(columns_lower, self.humidity_keywords)
            if humidity_col:
                result['humidity'] = humidity_col
            
            # Si aucune colonne n'est détectée, essayer une détection basée sur les valeurs
            if not any(result.values()):
                result = self._detect_by_values(df)
            
            logger.info(f"Colonnes détectées: {result}")
            return result
        
        except Exception as e:
            logger.error(f"Erreur lors de la détection des colonnes: {str(e)}")
            return {'date': None, 'temperature': None, 'humidity': None}
    
    def _find_column(self, columns_lower: Dict[str, str], keywords: List[str]) -> str:
        """Trouve une colonne correspondant à l'un des mots-clés"""
        # Recherche exacte
        for keyword in keywords:
            if keyword in columns_lower:
                return columns_lower[keyword]
        
        # Recherche partielle
        for col_lower, col_original in columns_lower.items():
            for keyword in keywords:
                if keyword in col_lower:
                    return col_original
        
        return None
    
    def _detect_by_values(self, df: pd.DataFrame) -> Dict[str, str]:
        """Détecte les colonnes en analysant les valeurs"""
        result = {
            'date': None,
            'temperature': None,
            'humidity': None
        }
        
        # Parcourir chaque colonne
        for col in df.columns:
            # Échantillon de valeurs (non-nulles)
            sample = df[col].dropna().head(5).astype(str).tolist()
            
            if not sample:
                continue
            
            # Vérifier si c'est une colonne de date
            if not result['date'] and self._is_date_column(sample):
                result['date'] = col
                continue
            
            # Vérifier si c'est une colonne numérique
            if self._is_numeric_column(sample):
                # Analyser les valeurs pour déterminer s'il s'agit de température ou d'humidité
                values = pd.to_numeric(df[col].dropna().head(100), errors='coerce')
                
                if values.min() >= 0 and values.max() <= 100:
                    # Probablement de l'humidité (0-100%)
                    if not result['humidity']:
                        result['humidity'] = col
                elif values.min() >= -50 and values.max() <= 50:
                    # Probablement de la température (-50°C à 50°C)
                    if not result['temperature']:
                        result['temperature'] = col
        
        return result
    
    def _is_date_column(self, sample: List[str]) -> bool:
        """Vérifie si les valeurs ressemblent à des dates"""
        # Motifs de date courants
        date_patterns = [
            r'\d{2,4}[-/]\d{1,2}[-/]\d{1,2}',  # YYYY-MM-DD, DD/MM/YYYY
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',  # DD-MM-YYYY, MM/DD/YYYY
            r'\d{1,2}[-/]\w{3}[-/]\d{2,4}',    # DD-MMM-YYYY
            r'\d{4}\d{2}\d{2}',                # YYYYMMDD
            r'\d{1,2}:\d{2}:\d{2}',            # HH:MM:SS
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\s+\d{1,2}:\d{2}'  # Date + heure
        ]
        
        # Vérifier si au moins 3 valeurs correspondent à un motif de date
        matches = 0
        for value in sample:
            for pattern in date_patterns:
                if re.search(pattern, value):
                    matches += 1
                    break
        
        return matches >= min(3, len(sample))
    
    def _is_numeric_column(self, sample: List[str]) -> bool:
        """Vérifie si les valeurs sont numériques"""
        # Motif pour les nombres (entiers, décimaux, avec signes)
        numeric_pattern = r'^[-+]?\d*\.?\d+$'
        
        # Vérifier si au moins 3 valeurs correspondent au motif numérique
        matches = 0
        for value in sample:
            value = value.replace(',', '.').strip()  # Remplacer la virgule par un point
            if re.match(numeric_pattern, value):
                matches += 1
        
        return matches >= min(3, len(sample))

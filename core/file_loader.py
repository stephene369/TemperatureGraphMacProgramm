import os
import pandas as pd
import webview
from typing import Tuple, Optional
from pathlib import Path
from services.logger import Logger

logger = Logger.get_logger()

class FileLoader:
    """Classe pour charger différents types de fichiers de données"""
    
    def __init__(self):
        self.supported_extensions = ['.xlsx', '.xls', '.csv', '.hobo']
    
    def select_file(self) -> Optional[str]:
        """Ouvre une boîte de dialogue pour sélectionner un fichier"""
        try:
            file_types = ('Fichiers de données (*.xlsx;*.xls;*.csv;*.hobo)', 
                         'Fichiers Excel (*.xlsx;*.xls)', 
                         'Fichiers CSV (*.csv)',
                         'Fichiers HOBO (*.hobo)',
                         'Tous les fichiers (*.*)')
            
            file_path = webview.windows[0].create_file_dialog(
                webview.OPEN_DIALOG, 
                allow_multiple=False,
                file_types=file_types
            )
            
            if file_path and len(file_path) > 0:
                return file_path[0]
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la sélection du fichier: {str(e)}")
            return None
    
    def load_file(self, file_path: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Charge un fichier et retourne un DataFrame pandas"""
        try:
            file_path = Path(file_path)
            extension = file_path.suffix.lower()
            
            if extension not in self.supported_extensions:
                logger.warning(f"Extension de fichier non prise en charge: {extension}")
                return None, ""
            
            if extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
                return df, 'excel'
            
            elif extension == '.csv':
                # Essayer différents encodages et séparateurs
                try:
                    df = pd.read_csv(file_path, sep=',')
                except:
                    try:
                        df = pd.read_csv(file_path, sep=';')
                    except:
                        df = pd.read_csv(file_path, sep='\t', encoding='latin1')
                
                return df, 'csv'
            
            elif extension == '.hobo':
                # Format spécifique HOBO
                df = self._parse_hobo_file(file_path)
                return df, 'hobo'
            
            return None, ""
        
        except Exception as e:
            logger.error(f"Erreur lors du chargement du fichier {file_path}: {str(e)}")
            return None, ""
    
    def _parse_hobo_file(self, file_path: Path) -> pd.DataFrame:
        """Parse un fichier au format HOBO"""
        try:
            # Lecture du fichier ligne par ligne
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Trouver l'en-tête et les données
            header_line = -1
            for i, line in enumerate(lines):
                if "Date Time" in line or "Horodatage" in line:
                    header_line = i
                    break
            
            if header_line == -1:
                raise ValueError("Format de fichier HOBO non reconnu: en-tête introuvable")
            
            # Extraire l'en-tête et les données
            header = lines[header_line].strip().split(',')
            data_lines = [line.strip().split(',') for line in lines[header_line+1:] if line.strip()]
            
            # Créer un DataFrame
            df = pd.DataFrame(data_lines, columns=header)
            
            return df
        
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du fichier HOBO {file_path}: {str(e)}")
            raise

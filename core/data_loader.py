"""Module DataLoader - Chargement et traitement des données"""
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Classe pour charger et traiter les données des fichiers
    """
    
    def load_file(self, file_path):
        """
        Charger un fichier de données (Excel, CSV ou HOBO)
        
        Args:
            file_path (str): Chemin du fichier à charger
            
        Returns:
            pandas.DataFrame: Données chargées
            
        Raises:
            ValueError: Si le format de fichier n'est pas pris en charge
            Exception: Si une erreur se produit lors de la lecture du fichier
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier n'existe pas: {file_path}")
            
        try:
            file_extension = os.path.splitext(file_path.lower())[1]
            
            if file_extension in ('.xlsx', '.xls'):
                logger.info(f"Chargement du fichier Excel: {file_path}")
                df = pd.read_excel(file_path)
                if df.shape[1] < 2:
                    for header_row in range(10):
                        df = pd.read_excel(file_path, header=header_row)
                        if df.shape[1] >= 2:
                            break
                return df
                
            elif file_extension == '.csv':
                logger.info(f"Chargement du fichier CSV: {file_path}")
                df = pd.read_csv(file_path)
                if df.shape[1] < 2:
                    for header_row in range(10):
                        df = pd.read_csv(file_path, header=header_row)
                        if df.shape[1] >= 2:
                            break
                return df
                
            elif file_extension == '.hobo':
                logger.info(f"Chargement du fichier HOBO: {file_path}")
                # Les fichiers HOBO sont généralement des CSV avec des en-têtes spécifiques
                # Détecter le nombre de lignes à sauter
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = []
                    for i, line in enumerate(f):
                        if i < 20:  # Lire les 20 premières lignes
                            lines.append(line)
                        else:
                            break
                
                # Trouver la ligne qui contient probablement les en-têtes
                header_row = 0
                for i, line in enumerate(lines):
                    if any(keyword in line.lower() for keyword in ['date', 'time', 'temp', 'rh']):
                        header_row = i
                        break
                
                # Lire le fichier avec le bon nombre de lignes à sauter
                df = pd.read_csv(file_path, sep='\t', skiprows=header_row)
                if df.shape[1] < 2:
                    for skip_row in range(20):
                        df = pd.read_csv(file_path, sep='\t', skiprows=skip_row)
                        if df.shape[1] >= 2:
                            break
                return df                
            else:
                raise ValueError(f"Format de fichier non pris en charge: {file_path}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du fichier {file_path}: {str(e)}")
            raise Exception(f"Erreur lors de la lecture du fichier: {str(e)}")
    
    def detect_columns(self, df):
        """
        Détecter automatiquement les colonnes de date, température, humidité et point de rosée
        
        Args:
            df (pandas.DataFrame): DataFrame contenant les données
            
        Returns:
            dict: Mapping des colonnes détectées
        """
        columns = df.columns.tolist()
        mapping = {}
        
        # Dictionnaires de mots-clés pour chaque type de colonne
        keywords = {
    'date': [
        'date', 'time', 'datetime', 'horodatage', 'timestamp', 'période', 
        'date heure', 'gmt', 'date time', 'heure', 'jour'
    ],
    'temperature': [
        'temp', 'température', 'temperature', '°c', 'degré', 'deg', 'celsius',
        'temp.', 'lgr', 'sen', 's/n', 'température', 't°', 'thermique'
    ],
    'humidity': [
        'humid', 'humidité', 'humidity', 'hr', 'rh', '%', 
        'hr, %', 'humidité relative', 'hygrométrie', 'moisture'
    ],
    'dew_point': [
        'dew', 'point', 'rosée', 'point de rosée', 'dew point', 'dew_point', 'dp',
        'ptrosée', 'pt rosée', 'pt.rosée', 'condensation', 'point de condensation'
    ]
}

        
        
        
        
        # Fonction pour normaliser les noms de colonnes (supprimer accents, espaces, etc.)
        def normalize_column_name(col):
            import unicodedata
            import re
            # Convertir en minuscules et supprimer les accents
            col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8')
            # Supprimer les caractères spéciaux
            col = re.sub(r'[^a-zA-Z0-9]', ' ', col).lower()
            return col
        
        # Rechercher les colonnes pour chaque type
        for col_type, col_keywords in keywords.items():
            # D'abord, recherche exacte
            for col in columns:
                normalized_col = normalize_column_name(col)
                if any(keyword == normalized_col for keyword in col_keywords):
                    mapping[col_type] = col
                    break
            
            # Si pas trouvé, recherche partielle
            if col_type not in mapping:
                for col in columns:
                    normalized_col = normalize_column_name(col)
                    if any(keyword in normalized_col for keyword in col_keywords):
                        mapping[col_type] = col
                        break
        
        # Vérification supplémentaire pour les colonnes de date
        if 'date' not in mapping:
            # Essayer de détecter les colonnes de date par leur contenu
            for col in columns:
                try:
                    # Vérifier si la colonne peut être convertie en datetime
                    if pd.to_datetime(df[col], errors='coerce').notna().mean() > 0.5:
                        mapping['date'] = col
                        break
                except:
                    continue
        
        logger.info(f"Colonnes détectées: {mapping}")
        return mapping
    
    
    
    
    
    
    def load_capteur_data(self, capteur_data):
        """
        Charger et préparer les données d'un capteur
        
        Args:
            capteur_data (dict): Données du capteur (chemin du fichier et mappage des colonnes)
            
        Returns:
            pandas.DataFrame: Données préparées
            
        Raises:
            ValueError: Si les données du capteur sont incomplètes
            Exception: Si une erreur se produit lors du chargement des données
        """
        if not capteur_data.get("file_path"):
            raise ValueError("Aucun fichier associé au capteur")
            
        if not (capteur_data.get("columns") and 
                capteur_data["columns"].get("date") and 
                capteur_data["columns"].get("temperature")):
            raise ValueError("Mappage des colonnes incomplet")
        
        try:
            # Charger le fichier
            df = self.load_file(capteur_data["file_path"])
            
            # Vérifier que les colonnes mappées existent dans le DataFrame
            columns = capteur_data["columns"]
            for col_type, col_name in columns.items():
                if col_name not in df.columns:
                    raise ValueError(f"La colonne mappée '{col_name}' pour '{col_type}' n'existe pas dans le fichier")
            
            # Sélectionner les colonnes nécessaires
            col_list = [columns["date"], columns["temperature"]]
            if columns.get("humidity"):
                col_list.append(columns["humidity"])
            if columns.get("dew_point"):
                col_list.append(columns["dew_point"])
            
            # Créer une copie pour éviter les avertissements SettingWithCopyWarning
            mapped_df = df[col_list].copy()
            
            # Renommer les colonnes
            new_columns = ["date", "temperature"]
            if columns.get("humidity"):
                new_columns.append("humidity")
            if columns.get("dew_point"):
                new_columns.append("dew_point")
            
            mapped_df.columns = new_columns
            
            # Convertir les types de données
            mapped_df["date"] = pd.to_datetime(mapped_df["date"], errors="coerce")
            mapped_df["temperature"] = pd.to_numeric(mapped_df["temperature"], errors="coerce")
            
            if "humidity" in mapped_df.columns:
                mapped_df["humidity"] = pd.to_numeric(mapped_df["humidity"], errors="coerce")
                # S'assurer que l'humidité est en pourcentage (0-100)
                if mapped_df["humidity"].max() <= 1.0:
                    mapped_df["humidity"] = mapped_df["humidity"] * 100
            
            if "dew_point" in mapped_df.columns:
                mapped_df["dew_point"] = pd.to_numeric(mapped_df["dew_point"], errors="coerce")
            
            # Supprimer les lignes avec des valeurs manquantes dans les colonnes requises
            required_cols = ["date", "temperature"]
            mapped_df = mapped_df.dropna(subset=required_cols)
            
            # Trier par date
            mapped_df = mapped_df.sort_values("date")
            
            # Supprimer les doublons de date si nécessaire
            if mapped_df["date"].duplicated().any():
                # logger.warning(f"Doublons de dates détectés dans {capteur_data.get('nom', 'capteur')}. Suppression des doublons.")
                mapped_df = mapped_df.drop_duplicates(subset=["date"], keep="first")
            
            logger.info(f"Données chargées pour {capteur_data.get('nom', 'capteur')}: {len(mapped_df)} lignes")
            return mapped_df
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données pour {capteur_data.get('nom', 'capteur')}: {str(e)}")
            raise Exception(f"Erreur lors du chargement des données: {str(e)}")

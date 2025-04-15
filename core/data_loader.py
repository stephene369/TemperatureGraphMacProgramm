"""
Module DataLoader - Chargement et traitement des données
"""
import pandas as pd
from print_color.print_color import print 
class DataLoader:
    """
    Classe pour charger et traiter les données des fichiers
    """
    
    def load_file(self, file_path):
        """
        Charger un fichier de données (Excel ou HOBO)
        
        Args:
            file_path (str): Chemin du fichier à charger
            
        Returns:
            pandas.DataFrame: Données chargées
            
        Raises:
            ValueError: Si le format de fichier n'est pas pris en charge
            Exception: Si une erreur se produit lors de la lecture du fichier
        """
        try:
            if file_path.lower().endswith(('.xlsx', '.xls')):
                return pd.read_excel(file_path)
            elif file_path.lower().endswith('.hobo'):
                # Implémentation de la lecture des fichiers HOBO
                # Pour l'instant, on suppose que c'est un fichier texte avec des séparateurs de tabulation
                return pd.read_csv(file_path, sep='\t')
            else:
                raise ValueError(f"Format de fichier non pris en charge: {file_path}")
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier: {e}")
    
    def detect_columns(self, df):
        """
        Détecter automatiquement les colonnes de date, température et humidité
        
        Args:
            df (pandas.DataFrame): DataFrame contenant les données
            
        Returns:
            dict: Mapping des colonnes détectées
        """
        columns = df.columns.tolist()
        mapping = {}
        
        # Recherche de colonnes de date
        date_keywords = ['date', 'time', 'datetime', 'horodatage', 'timestamp']
        for col in columns:
            if any(keyword in col.lower() for keyword in date_keywords):
                mapping['date'] = col
                break
        
        # Recherche de colonnes de température
        temp_keywords = ['temp', 'température', 'temperature', '°c', 'degré']
        for col in columns:
            if any(keyword in col.lower() for keyword in temp_keywords):
                mapping['temperature'] = col
                break
        
        # Recherche de colonnes d'humidité
        humidity_keywords = ['humid', 'humidité', 'humidity', 'hr', 'rh']
        for col in columns:
            if any(keyword in col.lower() for keyword in humidity_keywords):
                mapping['humidity'] = col
                break

        
        # Recherche de colonnes de point de rosée
        dew_point_keywords = ['dew', 'point', 'rosée', 'point de rosée', 'dew point', "dew_point","Dew Point   (°C)"]
        for col in columns:
            if any(keyword in col.lower() for keyword in dew_point_keywords):
                mapping['dew_point'] = col
                break
        
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
        import pandas as pd

        if not capteur_data.get("file_path"):
            raise ValueError("Aucun fichier associé au capteur")

        if not (capteur_data.get("columns") and 
                capteur_data["columns"].get("date") and 
                capteur_data["columns"].get("temperature")):
            raise ValueError("Mappage des colonnes incomplet")

        # Charger le fichier
        df = self.load_file(capteur_data["file_path"])

        # Appliquer le mappage
        columns = capteur_data["columns"]
        col_list = [columns["date"], columns["temperature"]]

        if columns.get("humidity"):
            col_list.append(columns["humidity"])
        if columns.get("dew_point"):
            col_list.append(columns["dew_point"])

        mapped_df = df[col_list].copy()

        # Renommer les colonnes
        new_columns = ["date", "temperature"]
        if columns.get("humidity"):
            new_columns.append("humidity")
        if columns.get("dew_point"):
            new_columns.append("dew_point")

        mapped_df.columns = new_columns

        # Convertir les types de manière sécurisée
        mapped_df["date"] = pd.to_datetime(mapped_df["date"], errors="coerce")
        mapped_df["temperature"] = pd.to_numeric(mapped_df["temperature"], errors="coerce")
        if "humidity" in mapped_df.columns:
            mapped_df["humidity"] = pd.to_numeric(mapped_df["humidity"], errors="coerce")
        if "dew_point" in mapped_df.columns:
            mapped_df["dew_point"] = pd.to_numeric(mapped_df["dew_point"], errors="coerce")

        # Supprimer les lignes invalides
        required_cols = ["date", "temperature"]
        if "dew_point" in mapped_df.columns:
            required_cols.append("dew_point")
        mapped_df = mapped_df.dropna(subset=required_cols)

        # print(f"[✔] Données capteur chargées : {capteur_data['file_path']}")

        return mapped_df
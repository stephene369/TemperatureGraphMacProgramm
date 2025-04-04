"""
Module DataLoader - Chargement et traitement des données
"""
import pandas as pd

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
        
        # Charger le fichier
        df = self.load_file(capteur_data["file_path"])
        
        # Appliquer le mappage
        columns = capteur_data["columns"]
        mapped_df = df[[columns["date"], columns["temperature"]]]
        mapped_df.columns = ["date", "temperature"]
        
        # Ajouter l'humidité si disponible
        if columns.get("humidity"):
            mapped_df["humidity"] = df[columns["humidity"]]
        
        # Convertir la colonne de date
        mapped_df["date"] = pd.to_datetime(mapped_df["date"])
        
        return mapped_df

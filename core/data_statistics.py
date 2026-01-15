"""
Module d'analyse statistique des données climatiques
Calcule les statistiques pour température, humidité et luminosité
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DataStatistics:
    """
    Classe pour calculer les statistiques sur les données climatiques
    """
    
    def __init__(self, df, columns_mapping):
        """
        Initialise l'analyseur de statistiques
        
        Args:
            df (DataFrame): DataFrame contenant les données
            columns_mapping (dict): Mappage des colonnes
        """
        self.df = df.copy()
        self.columns = columns_mapping
        self._prepare_data()
    
    def _prepare_data(self):
        """Prépare les données pour l'analyse"""
        try:
            # Convertir la colonne date
            if self.columns.get('date'):
                self.df[self.columns['date']] = pd.to_datetime(self.df[self.columns['date']])
                self.df = self.df.sort_values(self.columns['date'])
                self.df['date_only'] = self.df[self.columns['date']].dt.date
            
            # Convertir les colonnes numériques
            numeric_columns = ['temperature', 'humidity', 'luminosity', 'dew_point']
            for col in numeric_columns:
                if self.columns.get(col):
                    self.df[self.columns[col]] = pd.to_numeric(
                        self.df[self.columns[col]], errors='coerce'
                    )
        except Exception as e:
            print(f"Erreur lors de la préparation des données: {e}")
    
    def calculate_temperature_stats(self, start_date=None, end_date=None):
        """
        Calcule les statistiques de température
        
        Args:
            start_date (str): Date de début (format YYYY-MM-DD)
            end_date (str): Date de fin (format YYYY-MM-DD)
            
        Returns:
            dict: Statistiques de température
        """
        if not self.columns.get('temperature'):
            return {'error': 'Colonne température non mappée'}
        
        df_filtered = self._filter_by_date(start_date, end_date)
        temp_col = self.columns['temperature']
        
        if df_filtered.empty or temp_col not in df_filtered.columns:
            return {'error': 'Aucune donnée de température disponible'}
        
        # Supprimer les valeurs manquantes
        df_temp = df_filtered.dropna(subset=[temp_col])
        
        if df_temp.empty:
            return {'error': 'Aucune donnée de température valide'}
        
        try:
            # Calculs de base
            temp_min = float(df_temp[temp_col].min())
            temp_max = float(df_temp[temp_col].max())
            
            # Écarts journaliers
            daily_stats = df_temp.groupby('date_only')[temp_col].agg(['min', 'max'])
            daily_ranges = daily_stats['max'] - daily_stats['min']
            
            max_daily_range = float(daily_ranges.max()) if not daily_ranges.empty else 0
            avg_daily_range = float(daily_ranges.mean()) if not daily_ranges.empty else 0
            
            return {
                'ecart_maximal_journalier': round(max_daily_range, 2),
                'ecart_moyen_journalier': round(avg_daily_range, 2),
                'temperature_minimale': round(temp_min, 2),
                'temperature_maximale': round(temp_max, 2),
                'nombre_jours_analyses': len(daily_stats),
                'periode': {
                    'debut': df_temp[self.columns['date']].min().strftime('%Y-%m-%d'),
                    'fin': df_temp[self.columns['date']].max().strftime('%Y-%m-%d')
                }
            }
        except Exception as e:
            return {'error': f'Erreur lors du calcul des statistiques: {str(e)}'}
    
    def calculate_humidity_stats(self, start_date=None, end_date=None):
        """
        Calcule les statistiques d'humidité
        
        Args:
            start_date (str): Date de début (format YYYY-MM-DD)
            end_date (str): Date de fin (format YYYY-MM-DD)
            
        Returns:
            dict: Statistiques d'humidité
        """
        if not self.columns.get('humidity'):
            return {'error': 'Colonne humidité non mappée'}
        
        df_filtered = self._filter_by_date(start_date, end_date)
        humidity_col = self.columns['humidity']
        
        if df_filtered.empty or humidity_col not in df_filtered.columns:
            return {'error': 'Aucune donnée d\'humidité disponible'}
        
        # Supprimer les valeurs manquantes
        df_hum = df_filtered.dropna(subset=[humidity_col])
        
        if df_hum.empty:
            return {'error': 'Aucune donnée d\'humidité valide'}
        
        try:
            # Calculs de base
            hum_min = float(df_hum[humidity_col].min())
            hum_max = float(df_hum[humidity_col].max())
            
            # Variations journalières
            daily_stats = df_hum.groupby('date_only')[humidity_col].agg(['min', 'max'])
            daily_ranges = daily_stats['max'] - daily_stats['min']
            
            max_daily_variation = float(daily_ranges.max()) if not daily_ranges.empty else 0
            avg_daily_variation = float(daily_ranges.mean()) if not daily_ranges.empty else 0
            
            # Pourcentages selon les seuils
            total_points = len(df_hum)
            above_65 = len(df_hum[df_hum[humidity_col] > 65])
            below_55 = len(df_hum[df_hum[humidity_col] > 55])
            
            pct_above_65 = (above_65 / total_points * 100) if total_points > 0 else 0
            pct_below_55 = (below_55 / total_points * 100) if total_points > 0 else 0
            
            # Fluctuations quotidiennes > + 10%
            high_fluctuation_days = len(daily_ranges[daily_ranges > 10])
            total_days = len(daily_ranges)
            pct_high_fluctuation = (high_fluctuation_days / total_days * 100) if total_days > 0 else 0
            
            return {
                'variation_maximale_quotidienne': round(max_daily_variation, 2),
                'ecart_moyen_journalier': round(avg_daily_variation, 2),
                'pourcentage_au_dessus_65': round(pct_above_65, 2),
                'pourcentage_au_dessous_55': round(pct_below_55, 2),
                'pourcentage_fluctuations_elevees': round(pct_high_fluctuation, 2),
                'humidite_minimale': round(hum_min, 2),
                'humidite_maximale': round(hum_max, 2),
                'nombre_jours_analyses': total_days,
                'periode': {
                    'debut': df_hum[self.columns['date']].min().strftime('%Y-%m-%d'),
                    'fin': df_hum[self.columns['date']].max().strftime('%Y-%m-%d')
                }
            }
        except Exception as e:
            return {'error': f'Erreur lors du calcul des statistiques: {str(e)}'}
    
    def calculate_luminosity_stats(self, start_date=None, end_date=None):
        """
        Calcule les statistiques de luminosité
        
        Args:
            start_date (str): Date de début (format YYYY-MM-DD)
            end_date (str): Date de fin (format YYYY-MM-DD)
            
        Returns:
            dict: Statistiques de luminosité
        """
        if not self.columns.get('luminosity'):
            return {'error': 'Colonne luminosité non mappée'}
        
        df_filtered = self._filter_by_date(start_date, end_date)
        lum_col = self.columns['luminosity']
        
        if df_filtered.empty or lum_col not in df_filtered.columns:
            return {'error': 'Aucune donnée de luminosité disponible'}
        
        # Supprimer les valeurs manquantes
        df_lum = df_filtered.dropna(subset=[lum_col])
        
        if df_lum.empty:
            return {'error': 'Aucune donnée de luminosité valide'}
        
        try:
            # Valeur maximale
            lum_max = float(df_lum[lum_col].max())
            
            # Durée d'exposition > 100 lux
            high_lux_data = df_lum[df_lum[lum_col] > 100]
            
            # Calculer la durée en supposant des mesures régulières
            if len(high_lux_data) > 1 and self.columns.get('date'):
                # Calculer l'intervalle moyen entre les mesures
                time_diffs = df_lum[self.columns['date']].diff().dropna()
                avg_interval_minutes = time_diffs.dt.total_seconds().mean() / 60
                
                # Durée d'exposition = nombre de points * intervalle moyen
                exposure_duration = len(high_lux_data) * avg_interval_minutes
            else:
                exposure_duration = len(high_lux_data)  # Nombre de points si pas de temps
            
            return {
                'valeur_maximale_lux': round(lum_max, 2),
                'duree_exposition_100_lux_minutes': round(exposure_duration, 2),
                'nombre_points_analyses': len(df_lum),
                'nombre_points_au_dessus_100_lux': len(high_lux_data),
                'periode': {
                    'debut': df_lum[self.columns['date']].min().strftime('%Y-%m-%d'),
                    'fin': df_lum[self.columns['date']].max().strftime('%Y-%m-%d')
                }
            }
        except Exception as e:
            return {'error': f'Erreur lors du calcul des statistiques: {str(e)}'}
    
    def _filter_by_date(self, start_date=None, end_date=None):
        """
        Filtre les données par période
        
        Args:
            start_date (str): Date de début
            end_date (str): Date de fin
            
        Returns:
            DataFrame: Données filtrées
        """
        df_filtered = self.df.copy()
        
        if not self.columns.get('date'):
            return df_filtered
        
        try:
            if start_date:
                start_date = pd.to_datetime(start_date)
                df_filtered = df_filtered[df_filtered[self.columns['date']] >= start_date]
            
            if end_date:
                end_date = pd.to_datetime(end_date)
                df_filtered = df_filtered[df_filtered[self.columns['date']] <= end_date]
        except Exception as e:
            print(f"Erreur lors du filtrage par date: {e}")
        
        return df_filtered
    
    def calculate_dew_point_stats(self, start_date=None, end_date=None):
        """
        Calcule les statistiques de point de rosée
        
        Args:
            start_date (str): Date de début (format YYYY-MM-DD)
            end_date (str): Date de fin (format YYYY-MM-DD)
            
        Returns:
            dict: Statistiques de point de rosée
        """
        if not self.columns.get('dew_point'):
            return {'error': 'Colonne point de rosée non mappée'}
        
        df_filtered = self._filter_by_date(start_date, end_date)
        dew_col = self.columns['dew_point']
        
        if df_filtered.empty or dew_col not in df_filtered.columns:
            return {'error': 'Aucune donnée de point de rosée disponible'}
        
        # Supprimer les valeurs manquantes
        df_dew = df_filtered.dropna(subset=[dew_col])
        
        if df_dew.empty:
            return {'error': 'Aucune donnée de point de rosée valide'}
        
        try:
            # Calculs de base
            dew_min = float(df_dew[dew_col].min())
            dew_max = float(df_dew[dew_col].max())
            dew_mean = float(df_dew[dew_col].mean())
            
            # Écarts journaliers
            daily_stats = df_dew.groupby('date_only')[dew_col].agg(['min', 'max'])
            daily_ranges = daily_stats['max'] - daily_stats['min']
            
            max_daily_range = float(daily_ranges.max()) if not daily_ranges.empty else 0
            avg_daily_range = float(daily_ranges.mean()) if not daily_ranges.empty else 0
            
            return {
                'point_rosee_minimal': round(dew_min, 2),
                'point_rosee_maximal': round(dew_max, 2),
                'point_rosee_moyen': round(dew_mean, 2),
                'ecart_maximal_journalier': round(max_daily_range, 2),
                'ecart_moyen_journalier': round(avg_daily_range, 2),
                'nombre_jours_analyses': len(daily_stats),
                'periode': {
                    'debut': df_dew[self.columns['date']].min().strftime('%Y-%m-%d'),
                    'fin': df_dew[self.columns['date']].max().strftime('%Y-%m-%d')
                }
            }
        except Exception as e:
            return {'error': f'Erreur lors du calcul des statistiques: {str(e)}'}

    def get_all_statistics(self, start_date=None, end_date=None):
        """
        Calcule toutes les statistiques disponibles
        
        Args:
            start_date (str): Date de début
            end_date (str): Date de fin
            
        Returns:
            dict: Toutes les statistiques
        """
        stats = {
            'temperature': self.calculate_temperature_stats(start_date, end_date),
            'humidity': self.calculate_humidity_stats(start_date, end_date),
            'luminosity': self.calculate_luminosity_stats(start_date, end_date),
            'dew_point': self.calculate_dew_point_stats(start_date, end_date)
        }
        
        return stats

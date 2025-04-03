import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
import random
from datetime import datetime, timedelta
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')  # Utiliser le backend non-interactif

from core.models import GraphConfig, Capteur
from services.logger import Logger

logger = Logger.get_logger()

class GraphGenerator:
    """Classe pour générer différents types de graphiques"""
    
    def __init__(self):
        # Configuration des styles de graphiques
        plt.style.use('seaborn-v0_8-whitegrid')
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                       '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        # Définir la langue française pour les dates
        import locale
        try:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'fr_FR')
            except:
                logger.warning("Impossible de définir la locale française")
    
    def generate_graph(self, config: GraphConfig, capteurs_data: List[Tuple[Capteur, pd.DataFrame]]) -> Figure:
        """Génère un graphique en fonction de la configuration"""
        try:
            # Créer une figure
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
            
            # Appliquer le type de graphique approprié
            if config.type == 'temperature_time':
                self._generate_temperature_time_graph(ax, config, capteurs_data)
            elif config.type == 'humidity_time':
                self._generate_humidity_time_graph(ax, config, capteurs_data)
            elif config.type == 'temp_humidity_scatter':
                self._generate_temp_humidity_scatter(ax, config, capteurs_data)
            elif config.type == 'monthly_avg_temp':
                self._generate_monthly_avg_temp(ax, config, capteurs_data)
            elif config.type == 'daily_minmax_temp':
                self._generate_daily_minmax_temp(ax, config, capteurs_data)
            elif config.type == 'humidity_distribution':
                self._generate_humidity_distribution(ax, config, capteurs_data)
            else:
                # Graphique par défaut ou simulation
                self._generate_simulated_graph(ax, config)
            
            # Configurer le titre et les étiquettes
            if config.title:
                ax.set_title(config.title, fontsize=14, pad=20)
            
            if config.x_axis:
                ax.set_xlabel(config.x_axis, fontsize=12)
            
            if config.y_axis:
                ax.set_ylabel(config.y_axis, fontsize=12)
            
            # Ajouter une légende si nécessaire
            if len(capteurs_data) > 1 or config.type in ['daily_minmax_temp']:
                ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)
            
            # Ajuster la mise en page
            plt.tight_layout()
            
            return fig
        
        except Exception as e:
            logger.error(f"Erreur lors de la génération du graphique: {str(e)}")
            # Créer un graphique d'erreur
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
            ax.text(0.5, 0.5, f"Erreur: {str(e)}", 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=12, color='red')
            plt.tight_layout()
            return fig
    
    def _generate_temperature_time_graph(self, ax, config: GraphConfig, 
                                         capteurs_data: List[Tuple[Capteur, pd.DataFrame]]) -> None:
        """Génère un graphique de température en fonction du temps"""
        for i, (capteur, df) in enumerate(capteurs_data):
            color = self.colors[i % len(self.colors)]
            
            # Obtenir les colonnes mappées
            date_col = capteur.columns.get('date')
            temp_col = capteur.columns.get('temperature')
            
            if not date_col or not temp_col or date_col not in df.columns or temp_col not in df.columns:
                continue
            
            # Convertir la colonne de date en datetime
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            
            # Tracer la température
            ax.plot(df[date_col], df[temp_col], color=color, label=capteur.nom, linewidth=2)
        
        # Configurer l'axe des x (dates)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Grille
        ax.grid(True, linestyle='--', alpha=0.7)
    
    def _generate_humidity_time_graph(self, ax, config: GraphConfig, 
                                      capteurs_data: List[Tuple[Capteur, pd.DataFrame]]) -> None:
        """Génère un graphique d'humidité en fonction du temps"""
        for i, (capteur, df) in enumerate(capteurs_data):
            color = self.colors[i % len(self.colors)]
            
            # Obtenir les colonnes mappées
            date_col = capteur.columns.get('date')
            humidity_col = capteur.columns.get('humidity')
            
            if not date_col or not humidity_col or date_col not in df.columns or humidity_col not in df.columns:
                continue
            
            # Convertir la colonne de date en datetime
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            
            # Tracer l'humidité
            ax.plot(df[date_col], df[humidity_col], color=color, label=capteur.nom, linewidth=2)
        
        # Configurer l'axe des x (dates)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Définir les limites de l'axe y (0-100%)
        ax.set_ylim(0, 100)
        
        # Grille
        ax.grid(True, linestyle='--', alpha=0.7)
    
    def _generate_temp_humidity_scatter(self, ax, config: GraphConfig, 
                                        capteurs_data: List[Tuple[Capteur, pd.DataFrame]]) -> None:
        """Génère un nuage de points température vs humidité"""
        for i, (capteur, df) in enumerate(capteurs_data):
            color = self.colors[i % len(self.colors)]
            
            # Obtenir les colonnes mappées
            temp_col = capteur.columns.get('temperature')
            humidity_col = capteur.columns.get('humidity')
            
            if not temp_col or not humidity_col or temp_col not in df.columns or humidity_col not in df.columns:
                continue
            
            # Tracer le nuage de points
            ax.scatter(df[temp_col], df[humidity_col], color=color, alpha=0.7, 
                      label=capteur.nom, s=30, edgecolors='w', linewidths=0.5)
        
        # Ajouter une ligne de tendance (régression polynomiale)
        if len(capteurs_data) == 1 and temp_col in df.columns and humidity_col in df.columns:
            x = df[temp_col].dropna()
            y = df[humidity_col].dropna()
            
            if len(x) > 10:  # Assez de points pour une régression
                try:
                    z = np.polyfit(x, y, 2)
                    p = np.poly1d(z)
                    
                    # Générer des points x pour la courbe
                    x_line = np.linspace(x.min(), x.max(), 100)
                    y_line = p(x_line)
                    
                    # Tracer la ligne de tendance
                    ax.plot(x_line, y_line, '--', color='red', 
                           label='Tendance', linewidth=2)
                except:
                    pass
        
        # Grille
        ax.grid(True, linestyle='--', alpha=0.7)
    
    def _generate_monthly_avg_temp(self, ax, config: GraphConfig, 
                                  capteurs_data: List[Tuple[Capteur, pd.DataFrame]]) -> None:
        """Génère un graphique de température moyenne mensuelle"""
        bar_width = 0.8 / len(capteurs_data) if capteurs_data else 0.8
        months_fr = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
        
        for i, (capteur, df) in enumerate(capteurs_data):
            color = self.colors[i % len(self.colors)]
            
            # Obtenir les colonnes mappées
            date_col = capteur.columns.get('date')
            temp_col = capteur.columns.get('temperature')
            
            if not date_col or not temp_col or date_col not in df.columns or temp_col not in df.columns:
                continue
            
            # Convertir la colonne de date en datetime
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            
            # Extraire le mois et calculer la moyenne
            df['month'] = df[date_col].dt.month
            monthly_avg = df.groupby('month')[temp_col].mean()
            
            # Positions des barres
            x = np.arange(len(months_fr))
            bar_positions = x - (len(capteurs_data) - 1) * bar_width / 2 + i * bar_width
            
            # Tracer les barres pour chaque mois disponible
            heights = [monthly_avg.get(m+1, 0) for m in range(12)]
            bars = ax.bar(bar_positions, heights, bar_width, color=color, alpha=0.7, label=capteur.nom)
            
            # Ajouter les valeurs au-dessus des barres
            for bar, height in zip(bars, heights):
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1,
                           f'{height:.1f}°C', ha='center', va='bottom', fontsize=8)
        
        # Configurer l'axe des x
        ax.set_xticks(x)
        ax.set_xticklabels(months_fr)
        
        # Grille
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    def _generate_daily_minmax_temp(self, ax, config: GraphConfig, 
                                   capteurs_data: List[Tuple[Capteur, pd.DataFrame]]) -> None:
        """Génère un graphique des températures min/max quotidiennes"""
        for i, (capteur, df) in enumerate(capteurs_data):
            color = self.colors[i % len(self.colors)]
            
            # Obtenir les colonnes mappées
            date_col = capteur.columns.get('date')
            temp_col = capteur.columns.get('temperature')
            
            if not date_col or not temp_col or date_col not in df.columns or temp_col not in df.columns:
                continue
            
            # Convertir la colonne de date en datetime
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            
            # Extraire la date (sans l'heure) et calculer min/max
            df['date_only'] = df[date_col].dt.date
            daily_stats = df.groupby('date_only')[temp_col].agg(['min', 'max', 'mean'])
            
            # Convertir l'index en datetime pour le tracé
            daily_stats.index = pd.to_datetime(daily_stats.index)
            
            # Tracer les lignes min/max/moyenne
            ax.plot(daily_stats.index, daily_stats['mean'], '-', color=color, 
                   label=f"{capteur.nom} - Moyenne", linewidth=2)
            ax.plot(daily_stats.index, daily_stats['max'], '--', color=color, 
                   alpha=0.7, label=f"{capteur.nom} - Max", linewidth=1.5)
            ax.plot(daily_stats.index, daily_stats['min'], ':', color=color, 
                   alpha=0.7, label=f"{capteur.nom} - Min", linewidth=1.5)
            
            # Remplir l'espace entre min et max
            ax.fill_between(daily_stats.index, daily_stats['min'], daily_stats['max'], 
                           color=color, alpha=0.2)
        
        # Configurer l'axe des x (dates)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Grille
        ax.grid(True, linestyle='--', alpha=0.7)
    
    def _generate_humidity_distribution(self, ax, config: GraphConfig, 
                                       capteurs_data: List[Tuple[Capteur, pd.DataFrame]]) -> None:
        """Génère un histogramme de distribution de l'humidité"""
        for i, (capteur, df) in enumerate(capteurs_data):
            color = self.colors[i % len(self.colors)]
            
            # Obtenir les colonnes mappées
            humidity_col = capteur.columns.get('humidity')
            
            if not humidity_col or humidity_col not in df.columns:
                continue
            
            # Tracer l'histogramme
            ax.hist(df[humidity_col].dropna(), bins=20, alpha=0.6, color=color, 
                   label=capteur.nom, edgecolor='white', linewidth=1)
        
        # Configurer les axes
        ax.set_xlim(0, 100)
        
        # Grille
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    def _generate_simulated_graph(self, ax, config: GraphConfig) -> None:
        """Génère un graphique simulé pour démonstration"""
        # Générer des données simulées
        np.random.seed(42)  # Pour la reproductibilité
        
        # Dates (3 mois)
        start_date = datetime.now() - timedelta(days=90)
        dates = [start_date + timedelta(days=i) for i in range(90)]
        
        # Température simulée (variation saisonnière + bruit)
        base_temp = 20  # Température de base
        seasonal_var = 5  # Variation saisonnière
        daily_var = 3  # Variation quotidienne
        
        temps = [base_temp + 
                seasonal_var * np.sin(2 * np.pi * i / 90) + 
                daily_var * np.random.randn() 
                for i in range(90)]
        
        # Tracer la température simulée
        ax.plot(dates, temps, 'o-', color='#1f77b4', markersize=4, 
               label='Température simulée', linewidth=2)
        
        # Ajouter une ligne de tendance
        z = np.polyfit(range(len(dates)), temps, 1)
        p = np.poly1d(z)
        ax.plot(dates, p(range(len(dates))), '--', color='red', 
               label='Tendance', linewidth=2)
        
        # Configurer l'axe des x (dates)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Ajouter une légende
        ax.legend(loc='best')
        
        # Grille
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Titre et étiquettes par défaut si non spécifiés
        if not config.title:
            ax.set_title('Simulation de température sur 3 mois', fontsize=14, pad=20)
        
        if not config.x_axis:
            ax.set_xlabel('Date', fontsize=12)
        
        if not config.y_axis:
            ax.set_ylabel('Température (°C)', fontsize=12)

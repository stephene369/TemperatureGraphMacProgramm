"""
Module GraphGenerator - Génération des graphiques
"""
import os
import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.dates as mdates


# Dictionnaire de mois en français
mois_fr = { 
    'January': 'Janv.', 'February': 'Févr.', 'March': 'Mars',
    'April': 'Avr.', 'May': 'Mai', 'June': 'Juin',
    'July': 'Juil.', 'August': 'Août', 'September': 'Sept.',
    'October': 'Oct.', 'November': 'Nov.', 'December': 'Déc.'
}
# Format de date personnalisé
class FrenchDateFormatter(mdates.DateFormatter):
    def __call__(self, x, pos=0):
        result = super().__call__(x, pos)
        for en, fr in mois_fr.items():
            result = result.replace(en, fr)
        return result
    
            
class GraphGenerator:
    """
    Classe pour générer des graphiques à partir des données
    """
    
    def __init__(self, output_dir):
        """
        Initialise le générateur de graphiques
        
        Args:
            output_dir (str): Répertoire de sortie pour les graphiques exportés
        """
        self.output_dir = output_dir
    



    def generate_temperature_time_graph(self, capteurs_data): 
        """
        Générer un graphique de température en fonction du temps
        
        Args:
            capteurs_data (dict): Données des capteurs
            
        Returns:
            dict: Résultat contenant les données pour Chart.js et l'image base64
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import numpy as np
        import base64
        import io


        # Formatteur de date français
        class FrenchDateFormatter(mdates.DateFormatter):
            def __call__(self, x, pos=0):
                result = super().__call__(x, pos)
                for en, fr in mois_fr.items():
                    result = result.replace(en, fr)
                return result

        # Créer une figure matplotlib
        fig, ax = plt.subplots(figsize=(18, 8))
        # Palette cyclique
        palette = [
            "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        color_index = 0

        # Ajouter les données de chaque capteur
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]
            dates = df["date"]
            temp = df["temperature"]

            color = palette[color_index % len(palette)]
            linestyle = '-' if "Ext" not in nom else ':'
            ax.plot(dates, temp, label=nom, color=color, linestyle=linestyle, linewidth=0.8)
            color_index += 1



        # Configuration du graphique
        ax.set_title("Températures quotidiennes", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Température (°C)")
        ax.set_ylim(-10, 40)

        # Moins de dates : 1 tous les 2 mois
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))

        # Quadrillage style papier millimétré
        ax.set_axisbelow(True)
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))  # chaque lundi
        ax.yaxis.set_major_locator(plt.MultipleLocator(5))  # grands carreaux
        ax.yaxis.set_minor_locator(plt.MultipleLocator(1))  # petits carreaux
        # Grille principale
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        # Grille secondaire
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='lower right', frameon=True)
        plt.tight_layout()

        # Convertir la figure en image base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        # Préparer les données pour Chart.js
        datasets = []
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"]
            dates = df["date"].dt.strftime('%Y-%m-%d %H:%M').tolist()
            temps = df["temperature"].tolist()

            r, g, b = np.random.randint(0, 200, 3)
            datasets.append({
                "label": capteur["nom"],
                "data": temps,
                "borderColor": f"rgba({r},{g},{b},1)",
                "backgroundColor": f"rgba({r},{g},{b},0.2)",
                "fill": False,
                "tension": 0.1
            })

        all_dates = []
        for capteur_id, capteur in capteurs_data.items():
            all_dates.extend(capteur["data"]["date"].dt.strftime('%Y-%m-%d %H:%M').tolist())
        all_dates = sorted(list(set(all_dates)))

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Température en fonction du temps",
                "x_axis": "Date",
                "y_axis": "Température (°C)",
                "labels": all_dates,
                "datasets": datasets
            },
            "image": [img_base64]
        }


        
    def generate_humidity_time_graph(self, capteurs_data):
        """
        Générer un graphique d'humidité en fonction du temps avec le style ClimaGraph.
        
        Args:
            capteurs_data (dict): Données des capteurs
            
        Returns:
            dict: Résultat contenant les données pour Chart.js et l'image base64
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import numpy as np
        import base64
        import io


        # Vérifier la présence des colonnes d'humidité
        for capteur_id, capteur in capteurs_data.items():
            if "humidity" not in capteur["data"].columns:
                return {
                    "success": False,
                    "message": f"Le capteur {capteur['nom']} n'a pas de données d'humidité"
                }

        # Créer la figure
        fig, ax = plt.subplots(figsize=(18, 8))

        # Palette cyclique
        palette = [
            "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        color_index = 0

        # Ajouter les courbes d'humidité
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"]
            nom = capteur["nom"]
            dates = df["date"]
            humidity = df["humidity"]

            color = palette[color_index % len(palette)]
            linestyle = '-' if "Ext" not in nom else ':'
            ax.plot(dates, humidity, label=nom, color=color, linestyle=linestyle, linewidth=0.8)
            color_index += 1

        # Configuration du graphique
        ax.set_title("Humidité relative quotidienne", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Humidité (%)")
        ax.set_ylim(0, 100)

        # Axe X – style ClimaGraph
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))

        # Grille style papier millimétré
        ax.set_axisbelow(True)
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))  # chaque lundi
        ax.yaxis.set_major_locator(plt.MultipleLocator(10))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(2))

        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='lower right', frameon=True)
        plt.tight_layout()

        # Convertir en image base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Humidité en fonction du temps",
                "x_axis": "Date",
                "y_axis": "Humidité (%)",
            },
            "image": [img_base64]
        }




    def generate_temperature_amplitude_graph(self, capteurs_data):
        """
        Générer un graphique d'amplitudes thermiques quotidiennes (Tmax - Tmin) avec le style ClimaGraph.

        Args:
            capteurs_data (dict): Données des capteurs

        Returns:
            dict: Résultat contenant les données pour Chart.js et l'image base64
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import numpy as np
        import base64
        import io
        import pandas as pd

        # Créer la figure
        fig, ax = plt.subplots(figsize=(18, 8))

        # Palette cyclique
        palette = [
            "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        color_index = 0

        # Tracer les amplitudes thermiques par jour
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]

            # Calculer les amplitudes journalières
            df["date_only"] = df["date"].dt.floor("D")
            grouped = df.groupby("date_only")["temperature"]
            amplitude = (grouped.max() - grouped.min()).reset_index()
            amplitude.columns = ["date", "amplitude"]

            color = palette[color_index % len(palette)]
            linestyle = '-' if "Ext" not in nom else ':'
            ax.plot(amplitude["date"], amplitude["amplitude"], label=nom, color=color, linestyle=linestyle, linewidth=0.8)
            color_index += 1

        # Configuration du graphique
        ax.set_title("Amplitudes thermiques quotidiennes", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Température (°C)")
        ax.set_ylim(0, 10)

        # Axe X : format français, espacé tous les 2 mois
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))

        # Grille millimétrée
        ax.set_axisbelow(True)
        ax.yaxis.set_major_locator(plt.MultipleLocator(1))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(0.2))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='lower right', frameon=True)
        plt.tight_layout()

        # Convertir la figure en image base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        # Chart.js : formatter les données (si jamais tu veux les afficher aussi en JS)
        datasets = []
        all_dates = []

        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            df["date_only"] = df["date"].dt.floor("D")
            grouped = df.groupby("date_only")["temperature"]
            amplitude = (grouped.max() - grouped.min()).reset_index()
            amplitude.columns = ["date", "amplitude"]

            dates = amplitude["date"].dt.strftime('%Y-%m-%d').tolist()
            values = amplitude["amplitude"].round(2).tolist()
            all_dates.extend(dates)

            r, g, b = np.random.randint(0, 200, 3)
            datasets.append({
                "label": capteur["nom"],
                "data": values,
                "borderColor": f"rgba({r},{g},{b},1)",
                "backgroundColor": f"rgba({r},{g},{b},0.2)",
                "fill": False,
                "tension": 0.1
            })

        all_dates = sorted(list(set(all_dates)))

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Amplitude thermique quotidienne",
                "x_axis": "Date",
                "y_axis": "Amplitude (°C)",
                "labels": all_dates,
                "datasets": datasets
            },
            "image": [img_base64]
        }



    def generate_humidity_amplitude_graph(self, capteurs_data):
        """
        Générer un graphique d'amplitude hydrique quotidienne (HRmax - HRmin) pour chaque capteur.
        
        Returns:
            dict: Résultat contenant les données pour Chart.js et l'image base64
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import numpy as np
        import base64
        import io
        import pandas as pd

        # Créer la figure
        fig, ax = plt.subplots(figsize=(18, 8))

        # Palette cyclique
        palette = [
            "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        color_index = 0

        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]

            if "humidity" not in df.columns:
                continue  # Sauter si le capteur n’a pas d’humidité

            df["date_only"] = df["date"].dt.floor("D")
            grouped = df.groupby("date_only")["humidity"]
            amplitude = (grouped.max() - grouped.min()).reset_index()
            amplitude.columns = ["date", "amplitude"]

            color = palette[color_index % len(palette)]
            linestyle = '-' if "Ext" not in nom else ':'
            ax.plot(amplitude["date"], amplitude["amplitude"], label=nom, color=color, linestyle=linestyle, linewidth=0.8)
            color_index += 1

        # Configuration du graphique
        ax.set_title("Amplitude hydrique quotidienne", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Humidité relative (%)")
        ax.set_ylim(0, 40)

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))

        # Grille papier millimétré
        ax.set_axisbelow(True)
        ax.yaxis.set_major_locator(plt.MultipleLocator(5))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='lower right', frameon=True)
        plt.tight_layout()

        # Export en base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        # Préparer les données pour Chart.js (si affiché en JS)
        datasets = []
        all_dates = []

        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            if "humidity" not in df.columns:
                continue

            df["date_only"] = df["date"].dt.floor("D")
            grouped = df.groupby("date_only")["humidity"]
            amplitude = (grouped.max() - grouped.min()).reset_index()
            amplitude.columns = ["date", "amplitude"]

            dates = amplitude["date"].dt.strftime('%Y-%m-%d').tolist()
            values = amplitude["amplitude"].round(2).tolist()
            all_dates.extend(dates)

            r, g, b = np.random.randint(0, 200, 3)
            datasets.append({
                "label": capteur["nom"],
                "data": values,
                "borderColor": f"rgba({r},{g},{b},1)",
                "backgroundColor": f"rgba({r},{g},{b},0.2)",
                "fill": False,
                "tension": 0.1
            })

        all_dates = sorted(list(set(all_dates)))

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Amplitude hydrique quotidienne",
                "x_axis": "Date",
                "y_axis": "Amplitude HR (%)",
                "labels": all_dates,
                "datasets": datasets
            },
            "image": [img_base64]
        }





    def generate_dew_point_risk_graph(self, capteurs_data):
        """
        Générer un graphique de l'écart au point de rosée (valeurs déjà mesurées).
        Affiche une zone de condensation pour les valeurs < 2°C.

        Returns:
            dict: Résultat contenant uniquement l'image base64
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import numpy as np
        import base64
        import io
        import pandas as pd

        fig, ax = plt.subplots(figsize=(18, 8))

        palette = [
            "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        color_index = 0

        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]

            if "date" not in df.columns or "temperature" not in df.columns:
                print(f"[⚠️] Capteur ignoré (colonnes manquantes) : {nom}")
                continue

            try:
                df["date"] = pd.to_datetime(df["date"])
                df["date_only"] = df["date"].dt.floor("D")
                grouped = df.groupby("date_only")["temperature"].mean().reset_index()
                grouped.columns = ["date", "ecart"]

                color = palette[color_index % len(palette)]
                linestyle = '-' if "Ext" not in nom else ':'

                ax.plot(grouped["date"], grouped["ecart"], label=nom, color=color, linestyle=linestyle, linewidth=0.8)

                # Remplir la zone de risque de condensation (écart < 2°C)
                ax.fill_between(
                    grouped["date"],
                    0,
                    2,
                    where=grouped["ecart"] < 2,
                    color='red',
                    alpha=0.1
                )

                color_index += 1

            except Exception as e:
                print(f"[❌] Erreur avec le capteur {nom} : {e}")
                continue

        # Mise en forme du graphique
        ax.set_title("Écart au point de rosée quotidien", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Température (°C)")
        ax.set_ylim(0, 15)

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))

        ax.set_axisbelow(True)
        ax.yaxis.set_major_locator(plt.MultipleLocator(1))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(0.2))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='lower right', frameon=True)
        plt.tight_layout()

        # Export de l'image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Écart au point de rosée quotidien",
                "x_axis": "Date",
                "y_axis": "Écart au point de rosée (°C)"
            },
            "image": [img_base64]
        }








    def generate_all_humidity_distribution_pair_graphs(self, capteurs_data, applito_pie=True, applito_hist=True):
        """
        Génère une image par capteur avec :
        - À gauche : camembert des tranches d'humidité
        - À droite : histogramme des amplitudes hydriques journalières

        Args:
            capteurs_data (dict): données capteurs
            applito_pie (bool): appliquer une palette personnalisée au camembert
            applito_hist (bool): appliquer une palette personnalisée à l'histogramme

        Returns:
            dict: contient une liste d’images base64 prêtes à l’affichage
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import numpy as np
        import base64
        import io
        import pandas as pd

        images_base64 = []

        # Palette camembert (par défaut)
        pie_colors = [
            "#d0e1f2", "#a5cce1", "#7db8d1", "#529ec0",
            "#3279a3", "#1e4f73", "#0a2a42"
        ]

        # Palette histogramme (par défaut une seule couleur)
        hist_colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        hist_color_cycle = iter(hist_colors)

        bins = [0, 40, 50, 60, 70, 80, 90, 100]
        labels = [
            "HR < 40%", "40% ≤ HR < 50%", "50% ≤ HR < 60%", "60% ≤ HR < 70%",
            "70% ≤ HR < 80%", "80% ≤ HR < 90%", "HR ≥ 90%"
        ]

        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]

            if not {"date", "humidity"}.issubset(df.columns):
                print(f"[⚠️] Capteur ignoré (colonnes manquantes) : {nom}")
                continue

            try:
                df["date"] = pd.to_datetime(df["date"])
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

                # Camembert : répartition des valeurs par classe
                cat = pd.cut(df["humidity"], bins=bins, labels=labels, include_lowest=True)
                freqs = cat.value_counts().sort_index()

                pie_col = pie_colors if applito_pie else None
                ax1.pie(freqs, labels=None, colors=pie_col, startangle=90, autopct='%1.0f%%', wedgeprops={"linewidth": 0})
                ax1.set_title(f"Capteur {nom}", fontsize=12)
                ax1.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5), title="Légende")

                # Histogramme : amplitude hydrique quotidienne
                df["date_only"] = df["date"].dt.floor("D")
                grouped = df.groupby("date_only")["humidity"]
                amplitude = (grouped.max() - grouped.min()).dropna()

                hist_color = next(hist_color_cycle) if applito_hist else "#1e4f73"
                ax2.hist(amplitude, bins=20, color=hist_color, edgecolor='white', weights=np.ones_like(amplitude) / len(amplitude))
                ax2.set_title(f"Capteur {nom}", fontsize=12)
                ax2.set_xlabel("Amplitude hydrique quotidienne (RH %)")
                ax2.set_ylabel("Fréquence (%)")
                ax2.set_xlim(0, 25)
                ax2.set_ylim(0, 0.14)
                ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y * 100)}%'))

                plt.tight_layout()

                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=200)
                buf.seek(0)
                images_base64.append(base64.b64encode(buf.read()).decode('utf-8'))
                plt.close()

            except Exception as e:
                print(f"[❌] Erreur pour le capteur {nom} : {e}")
                continue

        return {
            "success": True,
            "data": {
                "type": "combined",
                "title": "Profil d'humidité par capteur",
                "x_axis": "Catégories / Amplitude (RH %)",
                "y_axis": "Fréquence (%)",
                "description": "Pour chaque capteur, cette figure affiche un camembert des classes d'humidité relative et un histogramme des amplitudes hydriques quotidiennes.",
            },
            "image": images_base64
        }





    def generate_dew_point_risk_graph_(self, capteurs_data):
        """
        Générer un graphique des écarts au point de rosée à partir des colonnes 'temperature' et 'dew_point'.
        Trace une zone rouge lorsque l'écart < 3°C (risque de condensation).

        Returns:
            dict: Résultat contenant l'image base64.
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import numpy as np
        import base64
        import io
        import pandas as pd

        fig, ax = plt.subplots(figsize=(18, 8))

        palette = [
            "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        color_index = 0

        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]

            if not {"date", "temperature", "dew_point"}.issubset(df.columns):
                print(f"[⚠️] Capteur ignoré (colonnes manquantes) : {nom}")
                print(df.columns)
                continue

            try:
                df["date"] = pd.to_datetime(df["date"])
                df["date_only"] = df["date"].dt.floor("D")
                df["ecart"] = df["temperature"] - df["dew_point"]

                grouped = df.groupby("date_only")["ecart"].mean().reset_index()
                grouped.columns = ["date", "ecart"]

                color = palette[color_index % len(palette)]
                linestyle = '-' if "Ext" not in nom else ':'

                ax.plot(grouped["date"], grouped["ecart"], label=nom, color=color, linestyle=linestyle, linewidth=0.8)

                # Zone rouge : risque de condensation (< 3°C)
                ax.fill_between(
                    grouped["date"],
                    0,
                    3,
                    where=grouped["ecart"] < 3,
                    color='red',
                    alpha=0.2
                )

                color_index += 1

            except Exception as e:
                print(f"[❌] Erreur avec le capteur {nom} : {e}")
                continue

        # Mise en forme
        ax.set_title("Écart au point de rosée quotidien", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Température (°C)")
        ax.set_ylim(0, 15)

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))

        ax.yaxis.set_major_locator(plt.MultipleLocator(1))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(0.2))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)
        ax.set_axisbelow(True)

        ax.legend(loc='lower right', frameon=True)
        plt.tight_layout()

        # Export base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Écart au point de rosée quotidien",
                "x_axis": "Date",
                "y_axis": "Température (°C)"
            },
            "image": [img_base64]
        }




    def generate_dew_point_risk_graph_pr1(self, capteurs_data):
        """
        Génère le graphique PR1 : Écarts quotidiens au point de rosée.
        T - PR pour chaque capteur, avec zone rouge si écart < 3°C.

        Returns:
            dict: Contient l’image base64 et les métadonnées du graphique.
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import matplotlib.ticker as ticker
        import numpy as np
        import pandas as pd
        import io
        import base64

        fig, ax = plt.subplots(figsize=(18, 8))

        palette = ["#1f77b4", "#2ca02c", "#ff7f0e"]
        legend_names = ["T-PR_Nord", "C4 (Est)", "C6 (Sud Est)"]
        color_index = 0

        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]

            if not {"date", "temperature", "dew_point"}.issubset(df.columns):
                print(f"[⚠️] Capteur ignoré : {nom}")
                continue

            df["date"] = pd.to_datetime(df["date"])
            df["date_only"] = df["date"].dt.floor("D")
            df["ecart"] = df["temperature"] - df["dew_point"]

            grouped = df.groupby("date_only")["ecart"].mean().reset_index()
            grouped.columns = ["date", "ecart"]

            color = palette[color_index % len(palette)]
            label = legend_names[color_index] if color_index < len(legend_names) else nom
            ax.plot(grouped["date"], grouped["ecart"], label=label, color=color, linewidth=0.9)

            # Remplir la zone rouge si écart < 3°C
            ax.fill_between(
                grouped["date"],
                0,
                3,
                where=grouped["ecart"] < 3,
                color='red',
                alpha=0.15
            )

            color_index += 1

        # Mise en forme
        ax.set_title("Écart au point de rosée quotidien", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Température (°C)")
        ax.set_ylim(0, 15)


        class FrenchDateFormatter(mdates.DateFormatter):
            def __call__(self, x, pos=0):
                result = super().__call__(x, pos)
                for en, fr in mois_fr.items():
                    result = result.replace(en, fr)
                return result

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))

        ax.set_axisbelow(True)
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='upper right', frameon=True)
        plt.tight_layout()

        # Export base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Écart au point de rosée quotidien",
                "x_axis": "Date",
                "y_axis": "Température (°C)"
            },
            "image": [img_base64]
        }

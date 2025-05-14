"""
Module GraphGenerator - Génération des graphiques
"""
import os
import io
import base64
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('Agg')
import base64
import io
import pandas as pd
from numpy import inf , random , arange,ones_like
from matplotlib.patches import Patch



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
        Générer un graphique de température quotidienne moyenne en fonction du temps
        
        Args:
            capteurs_data (dict): Données des capteurs
            
        Returns:
            dict: Résultat contenant l'image base64 du graphique
        """


        # Dictionnaire de mois en français
        mois_fr = {
            "January": "janvier", "February": "février", "March": "mars",
            "April": "avril", "May": "mai", "June": "juin",
            "July": "juillet", "August": "août", "September": "septembre",
            "October": "octobre", "November": "novembre", "December": "décembre"
        }

        # Formatteur de date français
        class FrenchDateFormatter(mdates.DateFormatter):
            def __call__(self, x, pos=0):
                result = super().__call__(x, pos)
                for en, fr in mois_fr.items():
                    result = result.replace(en, fr)
                return result

        # Créer la figure
        fig, ax = plt.subplots(figsize=(18, 8))

        # Palette cyclique
        palette = [
            "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        color_index = 0

        # Traiter chaque capteur
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]
            
            df["date"] = pd.to_datetime(df["date"])
            df["jour"] = df["date"].dt.floor("D")  # enlever l'heure

            # Moyenne quotidienne
            df_journalier = df.groupby("jour")["temperature"].mean().reset_index()

            # Tracer
            color = palette[color_index % len(palette)]
            linestyle = '-' if "Ext" not in nom else ':'  # extérieur en pointillé
            ax.plot(df_journalier["jour"], df_journalier["temperature"], 
                    label=nom, color=color, linestyle=linestyle, linewidth=1.0)
            color_index += 1

        # Configuration du graphique
        ax.set_title("Températures quotidiennes", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Température (°C)")
        # ax.set_ylim(-10, 40)

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))

        # Quadrillage type papier millimétré
        ax.set_axisbelow(True)
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))
        ax.yaxis.set_major_locator(plt.MultipleLocator(5))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='lower right', frameon=True,prop={'size': 12})
        plt.tight_layout()

        # Convertir en image base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Températures quotidiennes",
                "x_axis": "Date",
                "y_axis": "Température (°C)",
            },
            "image": [img_base64]
        }


    def generate_humidity_time_graph(self, capteurs_data):
        """
        Générer un graphique d'humidité quotidienne moyenne en fonction du temps.
        
        Args:
            capteurs_data (dict): Données des capteurs
            
        Returns:
            dict: Résultat contenant l'image base64 du graphique
        """


        # Dictionnaire des mois en français
        mois_fr = {
            "January": "janvier", "February": "février", "March": "mars",
            "April": "avril", "May": "mai", "June": "juin",
            "July": "juillet", "August": "août", "September": "septembre",
            "October": "octobre", "November": "novembre", "December": "décembre"
        }

        # Formatteur de date français
        class FrenchDateFormatter(mdates.DateFormatter):
            def __call__(self, x, pos=0):
                result = super().__call__(x, pos)
                for en, fr in mois_fr.items():
                    result = result.replace(en, fr)
                return result

        # Vérifier les colonnes
        for capteur_id, capteur in capteurs_data.items():
            if "humidity" not in capteur["data"].columns:
                return {
                    "success": False,
                    "message": f"Le capteur {capteur['nom']} n'a pas de données d'humidité"
                }

        fig, ax = plt.subplots(figsize=(18, 8))
        palette = [
            "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        color_index = 0

        # Traiter chaque capteur
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]
            df["date"] = pd.to_datetime(df["date"])
            df["jour"] = df["date"].dt.floor("D")

            # Moyenne d'humidité quotidienne
            df_journalier = df.groupby("jour")["humidity"].mean().reset_index()

            # Tracer
            color = palette[color_index % len(palette)]
            linestyle = '-' if "Ext" not in nom else ':'
            ax.plot(df_journalier["jour"], df_journalier["humidity"], 
                    label=nom, color=color, linestyle=linestyle, linewidth=1.2)
            color_index += 1

        # Configuration du graphique
        ax.set_title("Humidité relative quotidienne moyenne", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Humidité (%)")
        #ax.set_ylim(0, 100)

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))

        ax.set_axisbelow(True)
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))
        ax.yaxis.set_major_locator(plt.MultipleLocator(10))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(2))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='upper right', frameon=True,prop={'size': 12})
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Humidité relative quotidienne",
                "x_axis": "Date",
                "y_axis": "Humidité (%)",
            },
            "image": [img_base64]
        }



    def generate_temperature_amplitude_graph(self, capteurs_data):
        """
        Générer un graphique d'amplitudes thermiques quotidiennes (Tmax - Tmin) avec le style ISCGraph.

        Args:
            capteurs_data (dict): Données des capteurs

        Returns:
            dict: Résultat contenant les données pour Chart.js et l'image base64
        """


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
        #ax.set_ylim(0, 10)

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

        ax.legend(loc='upper right', frameon=True,prop={'size': 12})
        plt.tight_layout()

        # Convertir la figure en image base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        # Chart.js : formatter les données (si jamais tu veux les afficher aussi en JS)
        datasets = []
        all_dates = []

        # for capteur_id, capteur in capteurs_data.items():
        #     df = capteur["data"].copy()
        #     df["date_only"] = df["date"].dt.floor("D")
        #     grouped = df.groupby("date_only")["temperature"]
        #     amplitude = (grouped.max() - grouped.min()).reset_index()
        #     amplitude.columns = ["date", "amplitude"]

        #     dates = amplitude["date"].dt.strftime('%Y-%m-%d').tolist()
        #     values = amplitude["amplitude"].round(2).tolist()
        #     all_dates.extend(dates)

        #     r, g, b = random.randint(0, 200, 3)
        #     datasets.append({
        #         "label": capteur["nom"],
        #         "data": values,
        #         "borderColor": f"rgba({r},{g},{b},1)",
        #         "backgroundColor": f"rgba({r},{g},{b},0.2)",
        #         "fill": False,
        #         "tension": 0.1
        #     })

        all_dates = sorted(list(set(all_dates)))

        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Amplitude hydrique quotidienne",
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
        #ax.set_ylim(0, 40)

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))

        # Grille papier millimétré
        ax.set_axisbelow(True)
        ax.yaxis.set_major_locator(plt.MultipleLocator(5))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='upper right', frameon=True,prop={'size': 12})
        plt.tight_layout()

        # Export en base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
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

            r, g, b = random.randint(0, 200, 3)
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
        #ax.set_ylim(0, 15)

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))

        ax.set_axisbelow(True)
        ax.yaxis.set_major_locator(plt.MultipleLocator(1))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(0.2))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)

        ax.legend(loc='lower right', frameon=True,prop={'size': 12})
        plt.tight_layout()

        # Export de l'image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
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
        images_base64 = []
        recapitulatif = {}

        pie_colors = [
            "#a8cce6", "#66b2e6", "#3399e6", "#007acc", "#005cb2", "#003d80", "#001f40", "#000022"
        ]

        hist_colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        hist_color_cycle = iter(hist_colors)

        # ✅ Bins et labels pour humidité relative
        humidity_bins = [-inf, 65, 70, 75, 80, 85, 90, 95, inf]
        humidity_labels = [
            "HR < 65%",
            "65% ≤ HR < 70%",
            "70% ≤ HR < 75%",
            "75% ≤ HR < 80%",
            "80% ≤ HR < 85%",
            "85% ≤ HR < 90%",
            "90% ≤ HR < 95%",
            "HR ≥ 95%"
        ]
        
        humidity_bins = [-inf, 40, 50, 60, 70, 80, 90, inf]
        humidity_labels = [
            "HR < 40%", 
            "40% ≤ HR < 50%", 
            "50% ≤ HR < 60%", 
            "60% ≤ HR < 70%",
            "70% ≤ HR < 80%", 
            "80% ≤ HR < 90%", 
            "HR ≥ 90%"
        ]


        # ✅ Bins pour amplitude
        amplitude_bins = arange(0, 26, 1)  # 0 à 25
        amplitude_labels = [f"{i}-{i+1} % " for i in range(25)]

        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]

            if not {"date", "humidity"}.issubset(df.columns):
                print(f"[⚠️] Capteur ignoré (colonnes manquantes) : {nom}")
                continue

            try:
                df["date"] = pd.to_datetime(df["date"])
                df["jour"] = df["date"].dt.floor("D")

                df_journalier = df.groupby("jour")["humidity"].mean().reset_index()

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

                # 🟠 CAMEMBERT
                cat = pd.cut(df["humidity"], bins=humidity_bins, labels=humidity_labels, include_lowest=True)
                freqs = cat.value_counts().sort_index()
                freqs = freqs.reindex(humidity_labels, fill_value=0)

                labels_with_counts = [f"{label} : {count}" for label, count in zip(humidity_labels, freqs)]

                # Affichage console
                # print(f"\n🔹 Répartition HR - {nom}")
                # for line in labels_with_counts:
                #     print(line)

                recapitulatif[nom] = {
                    "repartition_hr": dict(zip(humidity_labels, freqs.astype(int))),
                }

                pie_col = pie_colors if applito_pie else None
                ax1.pie(freqs, 
                        labels=None, 
                        colors=pie_col, 
                        startangle=90, counterclock=False,
                        wedgeprops={"linewidth": 0})
                ax1.set_title(f"Capteur {nom}", fontsize=12)
                ax1.legend(humidity_labels, 
                           loc="center left", 
                           bbox_to_anchor=(1, 0.5), 
                           #title="Légende"
                           prop={'size': 12}
                           )
                

                # 🔵 HISTOGRAMME
                grouped = df.groupby("jour")["humidity"]
                amplitude = (grouped.max() - grouped.min()).dropna()
                
                

                hist_color = next(hist_color_cycle) if applito_hist else "#1e4f73"
                n, bins_hist, patches = ax2.hist(amplitude, 
                                                bins=amplitude_bins, 
                                                color=hist_color, 
                                                edgecolor='white', 
                                                weights=ones_like(amplitude) / len(amplitude),
                                                rwidth=.4)

                # # Texte au-dessus des barres
                # for i in range(len(patches)):
                #     height = patches[i].get_height()
                #     if height > 0:
                #         ax2.text(patches[i].get_x() + patches[i].get_width() / 2,
                #                 height + 0.5,
                #                 f'{int(height)}',
                #                 ha='center', va='bottom', fontsize=8)

                ax2.set_title(f"Capteur {nom}", fontsize=12)
                ax2.set_xlabel("Amplitude hydrique quotidienne (RH %)")
                ax2.set_ylabel("Fréquence (%)")
                ax2.set_xlim(0, 25)
                ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y * 100)}%'))
                

                # Affichage console
                # amplitude_counts = pd.cut(amplitude, bins=amplitude_bins, right=False).value_counts().sort_index()
                # print(f"\n🔹 Amplitudes hydriques - {nom}")
                # amplitude_text_lines = []
                # for label, count in zip(amplitude_labels, amplitude_counts):
                #     print(f"{label}: {count} mesure{'s' if count != 1 else ''}")
                #     amplitude_text_lines.append((label, int(count)))

                # recapitulatif[nom]["amplitudes"] = dict(amplitude_text_lines)

                plt.tight_layout()

                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=150)
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
                "y_axis": "Nombre de mesures",
                "description": "Pour chaque capteur, cette figure affiche un camembert des classes d'humidité relative (moyenne quotidienne) et un histogramme des amplitudes hydriques journalières avec les effectifs.",
                # "details": recapitulatif  # <== Résumé chiffré ici
            },
            "image": images_base64
        }





    def generate_all_humidity_distribution_pair_graphs_(self, capteurs_data, applito_pie=True, applito_hist=True):
        """
        Génère une image par capteur avec :
        - À gauche : camembert des tranches d'humidité (moyennes quotidiennes)
        - À droite : histogramme des amplitudes hydriques journalières
        """


        images_base64 = []

        pie_colors = [
    "#a8cce6",  # légèrement plus sombre que #b3d9f2
    "#66b2e6",  # légèrement plus sombre que #80bfff
    "#3399e6",  # légèrement plus sombre que #4da6ff
    "#007acc",  # légèrement plus sombre que #1a8cff
    "#005cb2",  # légèrement plus sombre que #0066cc
    "#003d80",  # inchangé, bien équilibré
    "#001f40"   # légèrement plus sombre que #00264d
]


        hist_colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
        ]
        hist_color_cycle = iter(hist_colors)

        bins = bins = [-inf, 40, 50, 60, 70, 80, 90, inf]
        labels = [
            "HR < 40%", 
            "40% ≤ HR < 50%", 
            "50% ≤ HR < 60%", 
            "60% ≤ HR < 70%",
            "70% ≤ HR < 80%", 
            "80% ≤ HR < 90%", 
            "HR ≥ 90%"
        ]

        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"].copy()
            nom = capteur["nom"]

            if not {"date", "humidity"}.issubset(df.columns):
                print(f"[⚠️] Capteur ignoré (colonnes manquantes) : {nom}")
                continue

            try:
                df["date"] = pd.to_datetime(df["date"])
                df["jour"] = df["date"].dt.floor("D")
                # df["jour"] = df["date"]

                # Moyenne journalière d'humidité pour le camembert
                df_journalier = df.groupby("jour")["humidity"].mean().reset_index()

                # Création de la figure
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

                # 🟠 CAMEMBERT
                cat = pd.cut(df_journalier["humidity"], bins=bins, labels=labels, include_lowest=True)
                freqs = cat.value_counts().sort_index()
                freqs = freqs.reindex(labels, fill_value=0)  # assure le bon ordre

                pie_col = pie_colors if applito_pie else None
                ax1.pie(freqs, labels=None, colors=pie_col, 
                        startangle=90, counterclock=False,
                        autopct='%1.0f%%', wedgeprops={"linewidth": 0})
                ax1.set_title(f"Capteur {nom}", fontsize=12)
                ax1.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5), title="Légende",prop={'size': 12})

                # 🔵 HISTOGRAMME
                grouped = df.groupby("jour")["humidity"]
                amplitude = (grouped.max() - grouped.min()).dropna()

                hist_color = next(hist_color_cycle) if applito_hist else "#1e4f73"
                ax2.hist(amplitude, 
                        bins=arange(0, 26, 1), 
                        color=hist_color, 
                        edgecolor='white', 
                        weights=(ones_like(amplitude) / len(amplitude)),
                        rwidth=.4)

                ax2.set_title(f"Capteur {nom}", fontsize=12)
                ax2.set_xlabel("Amplitude hydrique quotidienne (RH %)")
                ax2.set_ylabel("Fréquence (%)")
                ax2.set_xlim(0, 25)
                ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y * 100)}%'))

                plt.tight_layout()

                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=150)
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
                "description": "Pour chaque capteur, cette figure affiche un camembert des classes d'humidité relative (moyenne quotidienne) et un histogramme des amplitudes hydriques journalières.",
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
                    alpha=0.2,
                    
                )

                color_index += 1

            except Exception as e:
                print(f"[❌] Erreur avec le capteur {nom} : {e}")
                continue

        # Mise en forme
        ax.set_title("Écart au point de rosée quotidien", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Température (°C)")
        #ax.set_ylim(0, 15)

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(FrenchDateFormatter('%d %B\n%Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))

        ax.yaxis.set_major_locator(plt.MultipleLocator(1))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(0.2))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='black', alpha=0.5)
        ax.grid(which='minor', linestyle='-', linewidth=0.3, color='grey', alpha=0.3)
        ax.set_axisbelow(True)
        
        handles, labels = ax.get_legend_handles_labels()
        # Ajouter un patch personnalisé pour la zone rouge
        red_patch = Patch(color='red', alpha=0.2, label="Zone à risque (< 3°C)")
        handles.append(red_patch)
        labels.append("Zone à risque (< 3°C)")

        ax.legend(handles=handles, labels=labels, loc='upper right', frameon=True,prop={'size': 12})
        plt.tight_layout()

        # Export base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
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
        #ax.set_ylim(0, 15)
        # update


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

        ax.legend(loc='upper right', frameon=True,prop={'size': 12})
        plt.tight_layout()

        # Export base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
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

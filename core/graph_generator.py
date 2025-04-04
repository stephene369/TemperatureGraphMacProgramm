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
        # Créer une figure matplotlib
        plt.figure(figsize=(12, 6))
        
        # Ajouter les données de chaque capteur
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"]
            plt.plot(df["date"], df["temperature"], label=capteur["nom"])
        
        # Configurer le graphique
        plt.title("Température en fonction du temps")
        plt.xlabel("Date")
        plt.ylabel("Température (°C)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        # Ajuster la mise en page
        plt.tight_layout()
        
        # Convertir la figure en image base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        # Préparer les données pour Chart.js
        datasets = []
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"]
            
            # Générer des couleurs aléatoires
            r = np.random.randint(0, 200)
            g = np.random.randint(0, 200)
            b = np.random.randint(0, 200)
            color = f"rgba({r}, {g}, {b}, 1)"
            
            # Formater les dates et les valeurs
            dates = df["date"].dt.strftime('%Y-%m-%d %H:%M').tolist()
            temps = df["temperature"].tolist()
            
            datasets.append({
                "label": capteur["nom"],
                "data": temps,
                "borderColor": color,
                "backgroundColor": f"rgba({r}, {g}, {b}, 0.2)",
                "fill": False,
                "tension": 0.1
            })
        
        # Obtenir toutes les dates uniques
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
            "image": img_base64
        }
    
    def generate_humidity_time_graph(self, capteurs_data):
        """
        Générer un graphique d'humidité en fonction du temps
        
        Args:
            capteurs_data (dict): Données des capteurs
            
        Returns:
            dict: Résultat contenant les données pour Chart.js et l'image base64
        """
        # Vérifier que tous les capteurs ont des données d'humidité
        for capteur_id, capteur in capteurs_data.items():
            if "humidity" not in capteur["data"].columns:
                return {
                    "success": False,
                    "message": f"Le capteur {capteur['nom']} n'a pas de données d'humidité"
                }
        
        # Créer une figure matplotlib
        plt.figure(figsize=(12, 6))
        
        # Ajouter les données de chaque capteur
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"]
            plt.plot(df["date"], df["humidity"], label=capteur["nom"])
        
        # Configurer le graphique
        plt.title("Humidité en fonction du temps")
        plt.xlabel("Date")
        plt.ylabel("Humidité (%)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        # Ajuster la mise en page
        plt.tight_layout()
        
        # Convertir la figure en image base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        # Préparer les données pour Chart.js
        datasets = []
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"]
            
            # Générer des couleurs aléatoires
            r = np.random.randint(0, 200)
            g = np.random.randint(0, 200)
            b = np.random.randint(0, 200)
            color = f"rgba({r}, {g}, {b}, 1)"
            
            # Formater les dates et les valeurs
            dates = df["date"].dt.strftime('%Y-%m-%d %H:%M').tolist()
            humidity = df["humidity"].tolist()
            
            datasets.append({
                "label": capteur["nom"],
                "data": humidity,
                "borderColor": color,
                "backgroundColor": f"rgba({r}, {g}, {b}, 0.2)",
                "fill": False,
                "tension": 0.1
            })
        
        # Obtenir toutes les dates uniques
        all_dates = []
        for capteur_id, capteur in capteurs_data.items():
            all_dates.extend(capteur["data"]["date"].dt.strftime('%Y-%m-%d %H:%M').tolist())
        all_dates = sorted(list(set(all_dates)))
        
        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Humidité en fonction du temps",
                "x_axis": "Date",
                "y_axis": "Humidité (%)",
                "labels": all_dates,
                "datasets": datasets
            },
            "image": img_base64
        }
    
    # Autres méthodes de génération de graphiques...
    # Note: Les autres méthodes de génération de graphiques seraient implémentées ici
    # de manière similaire aux deux méthodes ci-dessus.
    
    def export_graph(self, graph_data, filename, format="png"):
        """
        Exporter un graphique en fichier image
        
        Args:
            graph_data (dict): Données du graphique (contenant l'image base64)
            filename (str): Nom du fichier
            format (str): Format d'export (png, jpg, pdf)
            
        Returns:
            str: Chemin du fichier exporté
        """
        # Vérifier que les données contiennent une image
        if "image" not in graph_data:
            raise ValueError("Les données du graphique ne contiennent pas d'image")
        
        # Créer le chemin complet
        filepath = os.path.join(self.output_dir, f"{filename}.{format}")
        
        # Décoder l'image base64
        img_data = base64.b64decode(graph_data["image"])
        
        # Enregistrer l'image
        with open(filepath, "wb") as f:
            f.write(img_data)
        
        return filepath
def generate_temperature_humidity_graph(self, capteurs_data):
    """
    Générer un graphique de température vs humidité
    
    Args:
        capteurs_data (dict): Données des capteurs
        
    Returns:
        dict: Résultat contenant les données pour Chart.js et l'image base64
    """
    # Vérifier que tous les capteurs ont des données d'humidité
    for capteur_id, capteur in capteurs_data.items():
        if "humidity" not in capteur["data"].columns:
            return {
                "success": False,
                "message": f"Le capteur {capteur['nom']} n'a pas de données d'humidité"
            }
    
    # Créer une figure matplotlib
    plt.figure(figsize=(10, 8))
    
    # Ajouter les données de chaque capteur
    for capteur_id, capteur in capteurs_data.items():
        df = capteur["data"]
        plt.scatter(df["temperature"], df["humidity"], label=capteur["nom"], alpha=0.7)
    
    # Configurer le graphique
    plt.title("Température vs Humidité")
    plt.xlabel("Température (°C)")
    plt.ylabel("Humidité (%)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Ajuster la mise en page
    plt.tight_layout()
    
    # Convertir la figure en image base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Préparer les données pour Chart.js
    datasets = []
    for capteur_id, capteur in capteurs_data.items():
        df = capteur["data"]
        
        # Générer des couleurs aléatoires
        r = np.random.randint(0, 200)
        g = np.random.randint(0, 200)
        b = np.random.randint(0, 200)
        color = f"rgba({r}, {g}, {b}, 1)"
        
        # Préparer les données pour le graphique de dispersion
        data = []
        for i in range(len(df)):
            data.append({
                "x": df["temperature"].iloc[i],
                "y": df["humidity"].iloc[i]
            })
        
        datasets.append({
            "label": capteur["nom"],
            "data": data,
            "backgroundColor": color,
            "pointRadius": 5,
            "pointHoverRadius": 7
        })
    
    return {
        "success": True,
        "data": {
            "type": "scatter",
            "title": "Température vs Humidité",
            "x_axis": "Température (°C)",
            "y_axis": "Humidité (%)",
            "datasets": datasets
        },
        "image": img_base64
    }

def generate_temperature_monthly_graph(self, capteurs_data):
    """
    Générer un graphique de température moyenne par mois
    
    Args:
        capteurs_data (dict): Données des capteurs
        
    Returns:
        dict: Résultat contenant les données pour Chart.js et l'image base64
    """
    # Créer une figure matplotlib
    plt.figure(figsize=(12, 6))
    
    # Préparer les données pour chaque capteur
    monthly_data = {}
    all_months = set()
    
    for capteur_id, capteur in capteurs_data.items():
        df = capteur["data"]
        
        # Ajouter le mois comme colonne
        df["month"] = df["date"].dt.strftime('%Y-%m')
        
        # Calculer la moyenne par mois
        monthly_avg = df.groupby("month")["temperature"].mean()
        
        # Stocker les données
        monthly_data[capteur_id] = {
            "nom": capteur["nom"],
            "months": monthly_avg.index.tolist(),
            "temps": monthly_avg.values.tolist()
        }
        
        # Collecter tous les mois
        all_months.update(monthly_avg.index.tolist())
    
    # Trier les mois
    all_months = sorted(list(all_months))
    
    # Créer des positions pour les barres
    n_capteurs = len(capteurs_data)
    bar_width = 0.8 / n_capteurs
    
    # Ajouter les barres pour chaque capteur
    for i, (capteur_id, data) in enumerate(monthly_data.items()):
        # Créer un dictionnaire pour faciliter l'accès aux valeurs
        month_to_temp = dict(zip(data["months"], data["temps"]))
        
        # Préparer les valeurs pour tous les mois
        temps = [month_to_temp.get(month, 0) for month in all_months]
        
        # Calculer les positions des barres
        positions = np.arange(len(all_months)) + i * bar_width - (n_capteurs - 1) * bar_width / 2
        
        # Ajouter les barres
        plt.bar(positions, temps, width=bar_width, label=data["nom"])
    
    # Configurer le graphique
    plt.title("Température moyenne par mois")
    plt.xlabel("Mois")
    plt.ylabel("Température moyenne (°C)")
    plt.xticks(np.arange(len(all_months)), all_months, rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.legend()
    
    # Ajuster la mise en page
    plt.tight_layout()
    
    # Convertir la figure en image base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Préparer les données pour Chart.js
    datasets = []
    for capteur_id, data in monthly_data.items():
        # Générer des couleurs aléatoires
        r = np.random.randint(0, 200)
        g = np.random.randint(0, 200)
        b = np.random.randint(0, 200)
        color = f"rgba({r}, {g}, {b}, 1)"
        
        # Préparer les valeurs pour tous les mois
        month_to_temp = dict(zip(data["months"], data["temps"]))
        temps = [month_to_temp.get(month, 0) for month in all_months]
        
        datasets.append({
            "label": data["nom"],
            "data": temps,
            "backgroundColor": color,
            "borderColor": f"rgba({r}, {g}, {b}, 1)",
            "borderWidth": 1
        })
    
    return {
        "success": True,
        "data": {
            "type": "bar",
            "title": "Température moyenne par mois",
            "x_axis": "Mois",
            "y_axis": "Température moyenne (°C)",
            "labels": all_months,
            "datasets": datasets
        },
        "image": img_base64
    }
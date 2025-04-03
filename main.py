import os
import sys
import json
import webview
import datetime
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Utiliser le backend Agg pour générer des graphiques sans interface
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import base64
import uuid
from pathlib import Path
import io

# Définir les chemins de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, 'ui')
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'exports')

# Créer les répertoires s'ils n'existent pas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chemin du fichier de stockage
STORAGE_FILE = os.path.join(DATA_DIR, 'storage.json')
HISTORY_FILE = os.path.join(DATA_DIR, 'history.json')

# Classe API pour la communication entre Python et JavaScript
class API:
    def __init__(self):
        # Charger les données de stockage
        self.storage = self._load_storage()
        self.history = self._load_history()
    
    # Méthodes utilitaires
    def _load_storage(self):
        """Charger les données de stockage depuis le fichier JSON"""
        if os.path.exists(STORAGE_FILE):
            try:
                with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement du stockage: {e}")
                return {"capteurs": {}}
        else:
            return {"capteurs": {}}
    
    def _save_storage(self):
        """Sauvegarder les données de stockage dans le fichier JSON"""
        try:
            with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.storage, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du stockage: {e}")
            return False
    
    def _load_history(self):
        """Charger l'historique depuis le fichier JSON"""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de l'historique: {e}")
                return []
        else:
            return []
    
    def _save_history(self):
        """Sauvegarder l'historique dans le fichier JSON"""
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique: {e}")
            return False
    
    def _add_history_entry(self, action, capteur_id=None, details=None):
        """Ajouter une entrée à l'historique"""
        capteur_nom = None
        if capteur_id and capteur_id in self.storage["capteurs"]:
            capteur_nom = self.storage["capteurs"][capteur_id]["nom"]
        
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action,
            "capteur_id": capteur_id,
            "capteur_nom": capteur_nom,
            "details": details
        }
        
        self.history.append(entry)
        self._save_history()
    
    def _load_data_file(self, file_path):
        """Charger un fichier de données (Excel ou HOBO)"""
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
    
    def _detect_columns(self, df):
        """Détecter automatiquement les colonnes de date, température et humidité"""
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
    
    # Méthodes d'API exposées à JavaScript
    def get_app_info(self):
        """Obtenir des informations sur l'application"""
        return {
            "success": True,
            "version": "1.0.0",
            "name": "ClimaGraph",
            "data_dir": DATA_DIR,
            "output_dir": OUTPUT_DIR
        }
    
    def get_capteurs(self):
        """Obtenir la liste des capteurs"""
        capteurs = []
        for capteur_id, capteur_data in self.storage["capteurs"].items():
            capteur = {
                "id": capteur_id,
                "nom": capteur_data["nom"],
                "file_path": capteur_data.get("file_path"),
                "columns": capteur_data.get("columns")
            }
            capteurs.append(capteur)
        
        return {
            "success": True,
            "capteurs": capteurs
        }
    
    def add_capteur(self, nom):
        """Ajouter un nouveau capteur"""
        try:
            # Vérifier si le nom existe déjà
            for capteur in self.storage["capteurs"].values():
                if capteur["nom"] == nom:
                    return {
                        "success": False,
                        "message": f"Un capteur avec le nom '{nom}' existe déjà"
                    }
            
            # Créer un nouvel ID unique
            capteur_id = str(uuid.uuid4())
            
            # Ajouter le capteur
            self.storage["capteurs"][capteur_id] = {
                "nom": nom,
                "created_at": datetime.datetime.now().isoformat()
            }
            
            # Sauvegarder les modifications
            self._save_storage()
            
            # Ajouter à l'historique
            self._add_history_entry("Ajout de capteur", capteur_id)
            
            return {
                "success": True,
                "capteur_id": capteur_id
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'ajout du capteur: {e}"
            }
    
    def update_capteur(self, capteur_id, nom):
        """Mettre à jour un capteur existant"""
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.storage["capteurs"]:
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Vérifier si le nom existe déjà pour un autre capteur
            for cid, capteur in self.storage["capteurs"].items():
                if capteur["nom"] == nom and cid != capteur_id:
                    return {
                        "success": False,
                        "message": f"Un capteur avec le nom '{nom}' existe déjà"
                    }
            
            # Mettre à jour le capteur
            old_nom = self.storage["capteurs"][capteur_id]["nom"]
            self.storage["capteurs"][capteur_id]["nom"] = nom
            self.storage["capteurs"][capteur_id]["updated_at"] = datetime.datetime.now().isoformat()
            
            # Sauvegarder les modifications
            self._save_storage()
            
            # Ajouter à l'historique
            self._add_history_entry("Modification de capteur", capteur_id, {"old_nom": old_nom, "new_nom": nom})
            
            return {
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la mise à jour du capteur: {e}"
            }
    
    def delete_capteur(self, capteur_id):
        """Supprimer un capteur"""
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.storage["capteurs"]:
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Récupérer le nom pour l'historique
            nom = self.storage["capteurs"][capteur_id]["nom"]
            
            # Supprimer le capteur
            del self.storage["capteurs"][capteur_id]
            
            # Sauvegarder les modifications
            self._save_storage()
            
            # Ajouter à l'historique
            self._add_history_entry("Suppression de capteur", capteur_id, {"nom": nom})
            
            return {
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la suppression du capteur: {e}"
            }
    
    def select_file(self, capteur_id):
        """Sélectionner un fichier pour un capteur"""
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.storage["capteurs"]:
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Ouvrir la boîte de dialogue de sélection de fichier
            file_types = ('Fichiers Excel (*.xlsx;*.xls)', 'Fichiers HOBO (*.hobo)')
            file_path = webview.windows[0].create_file_dialog(
                webview.OPEN_DIALOG, 
                allow_multiple=False,
                file_types=file_types
            )
            
            if not file_path:
                return {
                    "success": False,
                    "message": "Aucun fichier sélectionné"
                }
            
            file_path = file_path[0]  # create_file_dialog retourne une liste
            
            # Charger le fichier pour vérifier qu'il est valide
            df = self._load_data_file(file_path)
            
            # Détecter automatiquement les colonnes
            columns = self._detect_columns(df)
            needs_mapping = not (columns.get('date') and columns.get('temperature'))
            
            # Mettre à jour le capteur
            self.storage["capteurs"][capteur_id]["file_path"] = file_path
            self.storage["capteurs"][capteur_id]["columns"] = columns
            self.storage["capteurs"][capteur_id]["file_updated_at"] = datetime.datetime.now().isoformat()
            
            # Sauvegarder les modifications
            self._save_storage()
            
            # Ajouter à l'historique
            self._add_history_entry("Association de fichier", capteur_id, {
                "file_path": file_path,
                "columns": columns
            })
            
            return {
                "success": True,
                "needs_mapping": needs_mapping
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la sélection du fichier: {e}"
            }
    
    def get_capteurs_for_mapping(self):
        """Obtenir la liste des capteurs qui ont un fichier associé"""
        capteurs = []
        for capteur_id, capteur_data in self.storage["capteurs"].items():
            if capteur_data.get("file_path"):
                capteur = {
                    "id": capteur_id,
                    "nom": capteur_data["nom"],
                    "file_path": capteur_data["file_path"],
                    "columns": capteur_data.get("columns")
                }
                capteurs.append(capteur)
        
        return {
            "success": True,
            "capteurs": capteurs
        }
    
    def get_columns_for_mapping(self, capteur_id):
        """Obtenir les colonnes disponibles pour le mappage"""
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.storage["capteurs"]:
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Vérifier si le capteur a un fichier associé
            if not self.storage["capteurs"][capteur_id].get("file_path"):
                return {
                    "success": False,
                    "message": "Aucun fichier associé à ce capteur"
                }
            
            # Charger le fichier
            file_path = self.storage["capteurs"][capteur_id]["file_path"]
            df = self._load_data_file(file_path)
            
            # Récupérer les noms des colonnes
            columns = df.columns.tolist()
            
            return {
                "success": True,
                "columns": columns
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la récupération des colonnes: {e}"
            }
    
    def get_data_preview(self, capteur_id):
        """Obtenir un aperçu des données pour le mappage"""
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.storage["capteurs"]:
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Vérifier si le capteur a un fichier associé
            if not self.storage["capteurs"][capteur_id].get("file_path"):
                return {
                    "success": False,
                    "message": "Aucun fichier associé à ce capteur"
                }
            
            # Charger le fichier
            file_path = self.storage["capteurs"][capteur_id]["file_path"]
            df = self._load_data_file(file_path)
            
            # Limiter à 10 lignes pour l'aperçu
            preview_df = df.head(10)
            
            # Convertir en format JSON-compatible
            preview = {
                "columns": preview_df.columns.tolist(),
                "data": preview_df.values.tolist()
            }
            
            return {
                "success": True,
                "preview": preview
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la récupération de l'aperçu: {e}"
            }
    
    def save_column_mapping(self, capteur_id, mapping):
        """Enregistrer le mappage des colonnes pour un capteur"""
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.storage["capteurs"]:
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Vérifier si le capteur a un fichier associé
            if not self.storage["capteurs"][capteur_id].get("file_path"):
                return {
                    "success": False,
                    "message": "Aucun fichier associé à ce capteur"
                }
            
            # Mettre à jour le mappage des colonnes
            self.storage["capteurs"][capteur_id]["columns"] = mapping
            self.storage["capteurs"][capteur_id]["mapping_updated_at"] = datetime.datetime.now().isoformat()
            
            # Sauvegarder les modifications
            self._save_storage()
            
            # Ajouter à l'historique
            self._add_history_entry("Mappage des colonnes", capteur_id, {"columns": mapping})
            
            return {
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'enregistrement du mappage: {e}"
            }
    
    def get_capteurs_for_graphs(self):
        """Obtenir la liste des capteurs disponibles pour les graphiques"""
        capteurs = []
        for capteur_id, capteur_data in self.storage["capteurs"].items():
            # Vérifier si le capteur a un fichier et un mappage complet
            if (capteur_data.get("file_path") and 
                capteur_data.get("columns") and 
                capteur_data["columns"].get("date") and 
                capteur_data["columns"].get("temperature")):
                
                capteur = {
                    "id": capteur_id,
                    "nom": capteur_data["nom"],
                    "has_humidity": bool(capteur_data["columns"].get("humidity"))
                }
                capteurs.append(capteur)
        
        return {
            "success": True,
            "capteurs": capteurs
        }
    
    def get_graph_types(self):
        """Obtenir la liste des types de graphiques disponibles"""
        graph_types = [
            {
                "id": "temperature_time",
                "name": "Température en fonction du temps",
                "description": "Graphique linéaire montrant l'évolution de la température au fil du temps pour chaque capteur."
            },
            {
                "id": "humidity_time",
                "name": "Humidité en fonction du temps",
                "description": "Graphique linéaire montrant l'évolution de l'humidité au fil du temps pour chaque capteur."
            },
            {
                "id": "temperature_humidity",
                "name": "Température vs Humidité",
                "description": "Graphique de dispersion montrant la relation entre température et humidité pour chaque capteur."
            },
            {
                "id": "temperature_monthly",
                "name": "Moyenne mensuelle de température",
                "description": "Histogramme montrant la température moyenne par mois pour chaque capteur."
            },
            {
                "id": "humidity_monthly",
                "name": "Moyenne mensuelle d'humidité",
                "description": "Histogramme montrant l'humidité moyenne par mois pour chaque capteur."
            },
            {
                "id": "temperature_daily",
                "name": "Cycle journalier de température",
                "description": "Graphique linéaire montrant la température moyenne par heure de la journée."
            },
            {
                "id": "humidity_daily",
                "name": "Cycle journalier d'humidité",
                "description": "Graphique linéaire montrant l'humidité moyenne par heure de la journée."
            },
            {
                "id": "temperature_distribution",
                "name": "Distribution des températures",
                "description": "Histogramme montrant la distribution des valeurs de température pour chaque capteur."
            },
            {
                "id": "humidity_distribution",
                "name": "Distribution des humidités",
                "description": "Histogramme montrant la distribution des valeurs d'humidité pour chaque capteur."
            },
            {
                "id": "temperature_comparison",
                "name": "Comparaison des températures",
                "description": "Boîte à moustaches comparant les distributions de température entre capteurs."
            }
        ]
        
        return {
            "success": True,
            "types": graph_types
        }
    
    def generate_graph(self, graph_type, capteur_ids):
        """Générer un graphique à partir des données des capteurs"""
        try:
            # Vérifier que les capteurs existent
            capteurs_data = {}
            for capteur_id in capteur_ids:
                if capteur_id not in self.storage["capteurs"]:
                    return {
                        "success": False,
                        "message": f"Capteur {capteur_id} non trouvé"
                    }
                
                capteur_data = self.storage["capteurs"][capteur_id]
                
                # Vérifier que le capteur a un fichier et un mappage
                if not capteur_data.get("file_path"):
                    return {
                        "success": False,
                        "message": f"Le capteur {capteur_data['nom']} n'a pas de fichier associé"
                    }
                
                if not (capteur_data.get("columns") and 
                        capteur_data["columns"].get("date") and 
                        capteur_data["columns"].get("temperature")):
                    return {
                        "success": False,
                        "message": f"Le capteur {capteur_data['nom']} n'a pas de mappage complet"
                    }
                
                # Charger les données
                file_path = capteur_data["file_path"]
                df = self._load_data_file(file_path)
                
                # Appliquer le mappage
                columns = capteur_data["columns"]
                mapped_df = df[[columns["date"], columns["temperature"]]]
                mapped_df.columns = ["date", "temperature"]
                
                # Ajouter l'humidité si disponible
                if columns.get("humidity"):
                    mapped_df["humidity"] = df[columns["humidity"]]
                
                # Convertir la colonne de date
                mapped_df["date"] = pd.to_datetime(mapped_df["date"])
                
                # Stocker les données
                capteurs_data[capteur_id] = {
                    "nom": capteur_data["nom"],
                    "data": mapped_df
                }
            
            # Générer le graphique en fonction du type
            if graph_type == "temperature_time":
                return self._generate_temperature_time_graph(capteurs_data)
            elif graph_type == "humidity_time":
                return self._generate_humidity_time_graph(capteurs_data)
            elif graph_type == "temperature_humidity":
                return self._generate_temperature_humidity_graph(capteurs_data)
            elif graph_type == "temperature_monthly":
                return self._generate_temperature_monthly_graph(capteurs_data)
            elif graph_type == "humidity_monthly":
                return self._generate_humidity_monthly_graph(capteurs_data)
            elif graph_type == "temperature_daily":
                return self._generate_temperature_daily_graph(capteurs_data)
            elif graph_type == "humidity_daily":
                return self._generate_humidity_daily_graph(capteurs_data)
            elif graph_type == "temperature_distribution":
                return self._generate_temperature_distribution_graph(capteurs_data)
            elif graph_type == "humidity_distribution":
                return self._generate_humidity_distribution_graph(capteurs_data)
            elif graph_type == "temperature_comparison":
                return self._generate_temperature_comparison_graph(capteurs_data)
            else:
                return {
                    "success": False,
                    "message": f"Type de graphique non pris en charge: {graph_type}"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la génération du graphique: {e}"
            }
    
    def _generate_temperature_time_graph(self, capteurs_data):
        """Générer un graphique de température en fonction du temps"""
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
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Température en fonction du temps",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
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
    
    def _generate_humidity_time_graph(self, capteurs_data):
        """Générer un graphique d'humidité en fonction du temps"""
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
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Humidité en fonction du temps",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
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
    
    def _generate_temperature_humidity_graph(self, capteurs_data):
        """Générer un graphique de température vs humidité"""
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
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Température vs Humidité",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
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
    
    def _generate_temperature_monthly_graph(self, capteurs_data):
        """Générer un graphique de température moyenne par mois"""
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
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Température moyenne par mois",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
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
    
    def _generate_humidity_monthly_graph(self, capteurs_data):
        """Générer un graphique d'humidité moyenne par mois"""
        # Vérifier que tous les capteurs ont des données d'humidité
        for capteur_id, capteur in capteurs_data.items():
            if "humidity" not in capteur["data"].columns:
                return {
                    "success": False,
                    "message": f"Le capteur {capteur['nom']} n'a pas de données d'humidité"
                }
        
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
            monthly_avg = df.groupby("month")["humidity"].mean()
            
            # Stocker les données
            monthly_data[capteur_id] = {
                "nom": capteur["nom"],
                "months": monthly_avg.index.tolist(),
                "humidity": monthly_avg.values.tolist()
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
            month_to_humidity = dict(zip(data["months"], data["humidity"]))
            
            # Préparer les valeurs pour tous les mois
            humidity = [month_to_humidity.get(month, 0) for month in all_months]
            
            # Calculer les positions des barres
            positions = np.arange(len(all_months)) + i * bar_width - (n_capteurs - 1) * bar_width / 2
            
            # Ajouter les barres
            plt.bar(positions, humidity, width=bar_width, label=data["nom"])
        
        # Configurer le graphique
        plt.title("Humidité moyenne par mois")
        plt.xlabel("Mois")
        plt.ylabel("Humidité moyenne (%)")
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
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Humidité moyenne par mois",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
        # Préparer les données pour Chart.js
        datasets = []
        for capteur_id, data in monthly_data.items():
            # Générer des couleurs aléatoires
            r = np.random.randint(0, 200)
            g = np.random.randint(0, 200)
            b = np.random.randint(0, 200)
            color = f"rgba({r}, {g}, {b}, 1)"
            
            # Préparer les valeurs pour tous les mois
            month_to_humidity = dict(zip(data["months"], data["humidity"]))
            humidity = [month_to_humidity.get(month, 0) for month in all_months]
            
            datasets.append({
                "label": data["nom"],
                "data": humidity,
                "backgroundColor": color,
                "borderColor": f"rgba({r}, {g}, {b}, 1)",
                "borderWidth": 1
            })
        
        return {
            "success": True,
            "data": {
                "type": "bar",
                "title": "Humidité moyenne par mois",
                "x_axis": "Mois",
                "y_axis": "Humidité moyenne (%)",
                "labels": all_months,
                "datasets": datasets
            },
            "image": img_base64
        }
    
    def _generate_temperature_daily_graph(self, capteurs_data):
        """Générer un graphique du cycle journalier de température"""
        # Créer une figure matplotlib
        plt.figure(figsize=(12, 6))
        
        # Préparer les données pour chaque capteur
        hourly_data = {}
        
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"]
            
            # Ajouter l'heure comme colonne
            df["hour"] = df["date"].dt.hour
            
            # Calculer la moyenne par heure
            hourly_avg = df.groupby("hour")["temperature"].mean()
            
            # Stocker les données
            hourly_data[capteur_id] = {
                "nom": capteur["nom"],
                "hours": hourly_avg.index.tolist(),
                "temps": hourly_avg.values.tolist()
            }
        
        # Ajouter les lignes pour chaque capteur
        for capteur_id, data in hourly_data.items():
            plt.plot(data["hours"], data["temps"], marker='o', label=data["nom"])
        
        # Configurer le graphique
        plt.title("Cycle journalier de température")
        plt.xlabel("Heure")
        plt.ylabel("Température moyenne (°C)")
        plt.xticks(range(0, 24))
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
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Cycle journalier de température",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
        # Préparer les données pour Chart.js
        datasets = []
        for capteur_id, data in hourly_data.items():
            # Générer des couleurs aléatoires
            r = np.random.randint(0, 200)
            g = np.random.randint(0, 200)
            b = np.random.randint(0, 200)
            color = f"rgba({r}, {g}, {b}, 1)"
            
            # Préparer les valeurs pour toutes les heures
            hour_to_temp = dict(zip(data["hours"], data["temps"]))
            temps = [hour_to_temp.get(hour, None) for hour in range(24)]
            
            datasets.append({
                "label": data["nom"],
                "data": temps,
                "borderColor": color,
                "backgroundColor": f"rgba({r}, {g}, {b}, 0.2)",
                "fill": False,
                "tension": 0.1
            })
        
        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Cycle journalier de température",
                "x_axis": "Heure",
                "y_axis": "Température moyenne (°C)",
                "labels": list(range(24)),
                "datasets": datasets
            },
            "image": img_base64
        }
    
    def _generate_humidity_daily_graph(self, capteurs_data):
        """Générer un graphique du cycle journalier d'humidité"""
        # Vérifier que tous les capteurs ont des données d'humidité
        for capteur_id, capteur in capteurs_data.items():
            if "humidity" not in capteur["data"].columns:
                return {
                    "success": False,
                    "message": f"Le capteur {capteur['nom']} n'a pas de données d'humidité"
                }
        
        # Créer une figure matplotlib
        plt.figure(figsize=(12, 6))
        
        # Préparer les données pour chaque capteur
        hourly_data = {}
        
        for capteur_id, capteur in capteurs_data.items():
            df = capteur["data"]
            
            # Ajouter l'heure comme colonne
            df["hour"] = df["date"].dt.hour
            
            # Calculer la moyenne par heure
            hourly_avg = df.groupby("hour")["humidity"].mean()
            
            # Stocker les données
            hourly_data[capteur_id] = {
                "nom": capteur["nom"],
                "hours": hourly_avg.index.tolist(),
                "humidity": hourly_avg.values.tolist()
            }
        
        # Ajouter les lignes pour chaque capteur
        for capteur_id, data in hourly_data.items():
            plt.plot(data["hours"], data["humidity"], marker='o', label=data["nom"])
        
        # Configurer le graphique
        plt.title("Cycle journalier d'humidité")
        plt.xlabel("Heure")
        plt.ylabel("Humidité moyenne (%)")
        plt.xticks(range(0, 24))
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
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Cycle journalier d'humidité",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
        # Préparer les données pour Chart.js
        datasets = []
        for capteur_id, data in hourly_data.items():
            # Générer des couleurs aléatoires
            r = np.random.randint(0, 200)
            g = np.random.randint(0, 200)
            b = np.random.randint(0, 200)
            color = f"rgba({r}, {g}, {b}, 1)"
            
            # Préparer les valeurs pour toutes les heures
            hour_to_humidity = dict(zip(data["hours"], data["humidity"]))
            humidity = [hour_to_humidity.get(hour, None) for hour in range(24)]
            
            datasets.append({
                "label": data["nom"],
                "data": humidity,
                "borderColor": color,
                "backgroundColor": f"rgba({r}, {g}, {b}, 0.2)",
                "fill": False,
                "tension": 0.1
            })
        
        return {
            "success": True,
            "data": {
                "type": "line",
                "title": "Cycle journalier d'humidité",
                "x_axis": "Heure",
                "y_axis": "Humidité moyenne (%)",
                "labels": list(range(24)),
                "datasets": datasets
            },
            "image": img_base64
        }
    
    def _generate_temperature_distribution_graph(self, capteurs_data):
        """Générer un histogramme de distribution des températures"""
        # Créer une figure matplotlib
        plt.figure(figsize=(12, 6))
        
        # Déterminer les limites pour les bins
        all_temps = []
        for capteur_id, capteur in capteurs_data.items():
            all_temps.extend(capteur["data"]["temperature"].tolist())
        
        min_temp = min(all_temps)
        max_temp = max(all_temps)
        
        # Créer des bins avec un pas de 1°C
        bins = np.arange(np.floor(min_temp), np.ceil(max_temp) + 1, 1)
        
        # Ajouter les histogrammes pour chaque capteur
        for capteur_id, capteur in capteurs_data.items():
            plt.hist(capteur["data"]["temperature"], bins=bins, alpha=0.5, label=capteur["nom"])
        
        # Configurer le graphique
        plt.title("Distribution des températures")
        plt.xlabel("Température (°C)")
        plt.ylabel("Nombre d'observations")
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
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Distribution des températures",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
        # Préparer les données pour Chart.js
        datasets = []
        for capteur_id, capteur in capteurs_data.items():
            # Générer des couleurs aléatoires
            r = np.random.randint(0, 200)
            g = np.random.randint(0, 200)
            b = np.random.randint(0, 200)
            color = f"rgba({r}, {g}, {b}, 0.7)"
            
            # Calculer l'histogramme
            hist, _ = np.histogram(capteur["data"]["temperature"], bins=bins)
            
            datasets.append({
                "label": capteur["nom"],
                "data": hist.tolist(),
                "backgroundColor": color,
                "borderColor": f"rgba({r}, {g}, {b}, 1)",
                "borderWidth": 1
            })
        
        # Préparer les labels (centres des bins)
        bin_centers = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins) - 1)]
        bin_labels = [f"{bins[i]:.1f}-{bins[i+1]:.1f}" for i in range(len(bins) - 1)]
        
        return {
            "success": True,
            "data": {
                "type": "bar",
                "title": "Distribution des températures",
                "x_axis": "Température (°C)",
                "y_axis": "Nombre d'observations",
                "labels": bin_labels,
                "datasets": datasets
            },
            "image": img_base64
        }
    
    def _generate_humidity_distribution_graph(self, capteurs_data):
        """Générer un histogramme de distribution des humidités"""
        # Vérifier que tous les capteurs ont des données d'humidité
        for capteur_id, capteur in capteurs_data.items():
            if "humidity" not in capteur["data"].columns:
                return {
                    "success": False,
                    "message": f"Le capteur {capteur['nom']} n'a pas de données d'humidité"
                }
        
        # Créer une figure matplotlib
        plt.figure(figsize=(12, 6))
        
        # Déterminer les limites pour les bins
        all_humidity = []
        for capteur_id, capteur in capteurs_data.items():
            all_humidity.extend(capteur["data"]["humidity"].tolist())
        
        min_humidity = min(all_humidity)
        max_humidity = max(all_humidity)
        
        # Créer des bins avec un pas de 5%
        bins = np.arange(np.floor(min_humidity / 5) * 5, np.ceil(max_humidity / 5) * 5 + 5, 5)
        
        # Ajouter les histogrammes pour chaque capteur
        for capteur_id, capteur in capteurs_data.items():
            plt.hist(capteur["data"]["humidity"], bins=bins, alpha=0.5, label=capteur["nom"])
        
        # Configurer le graphique
        plt.title("Distribution des humidités")
        plt.xlabel("Humidité (%)")
        plt.ylabel("Nombre d'observations")
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
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Distribution des humidités",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
        # Préparer les données pour Chart.js
        datasets = []
        for capteur_id, capteur in capteurs_data.items():
            # Générer des couleurs aléatoires
            r = np.random.randint(0, 200)
            g = np.random.randint(0, 200)
            b = np.random.randint(0, 200)
            color = f"rgba({r}, {g}, {b}, 0.7)"
            
            # Calculer l'histogramme
            hist, _ = np.histogram(capteur["data"]["humidity"], bins=bins)
            
            datasets.append({
                "label": capteur["nom"],
                "data": hist.tolist(),
                "backgroundColor": color,
                "borderColor": f"rgba({r}, {g}, {b}, 1)",
                "borderWidth": 1
            })
        
        # Préparer les labels (centres des bins)
        bin_centers = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins) - 1)]
        bin_labels = [f"{bins[i]:.1f}-{bins[i+1]:.1f}" for i in range(len(bins) - 1)]
        
        return {
            "success": True,
            "data": {
                "type": "bar",
                "title": "Distribution des humidités",
                "x_axis": "Humidité (%)",
                "y_axis": "Nombre d'observations",
                "labels": bin_labels,
                "datasets": datasets
            },
            "image": img_base64
        }
    
    def _generate_temperature_comparison_graph(self, capteurs_data):
        """Générer une boîte à moustaches comparant les distributions de température"""
        # Créer une figure matplotlib
        plt.figure(figsize=(12, 6))
        
        # Préparer les données pour la boîte à moustaches
        data = []
        labels = []
        
        for capteur_id, capteur in capteurs_data.items():
            data.append(capteur["data"]["temperature"].tolist())
            labels.append(capteur["nom"])
        
        # Créer la boîte à moustaches
        plt.boxplot(data, labels=labels)
        
        # Configurer le graphique
        plt.title("Comparaison des distributions de température")
        plt.xlabel("Capteur")
        plt.ylabel("Température (°C)")
        plt.grid(True, linestyle='--', alpha=0.7, axis='y')
        
        # Ajuster la mise en page
        plt.tight_layout()
        
        # Convertir la figure en image base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        # Ajouter à l'historique
        capteur_ids = list(capteurs_data.keys())
        self._add_history_entry("Génération de graphique", None, {
            "graph_type": "Comparaison des distributions de température",
            "capteurs": [capteurs_data[cid]["nom"] for cid in capteur_ids]
        })
        
        # Préparer les données pour Chart.js
        datasets = []
        
        # Pour chaque capteur, calculer les statistiques de la boîte à moustaches
        for i, (capteur_id, capteur) in enumerate(capteurs_data.items()):
            temps = capteur["data"]["temperature"].tolist()
            
            # Calculer les statistiques
            q1 = np.percentile(temps, 25)
            median = np.percentile(temps, 50)
            q3 = np.percentile(temps, 75)
            iqr = q3 - q1
            lower_whisker = max(min(temps), q1 - 1.5 * iqr)
            upper_whisker = min(max(temps), q3 + 1.5 * iqr)
            
            # Générer des couleurs aléatoires
            r = np.random.randint(0, 200)
            g = np.random.randint(0, 200)
            b = np.random.randint(0, 200)
            color = f"rgba({r}, {g}, {b}, 1)"
            
            datasets.append({
                "label": capteur["nom"],
                "data": [{
                    "min": lower_whisker,
                    "q1": q1,
                    "median": median,
                    "q3": q3,
                    "max": upper_whisker
                }],
                "backgroundColor": f"rgba({r}, {g}, {b}, 0.5)",
                "borderColor": color,
                "borderWidth": 1
            })
        
        return {
            "success": True,
            "data": {
                "type": "boxplot",
                "title": "Comparaison des distributions de température",
                "x_axis": "Capteur",
                "y_axis": "Température (°C)",
                "labels": labels,
                "datasets": datasets
            },
            "image": img_base64
        }
    
    def export_graph(self, graph_type, capteur_ids, format="png"):
        """Exporter un graphique en fichier image"""
        try:
            # Générer le graphique
            result = self.generate_graph(graph_type, capteur_ids)
            
            if not result["success"]:
                return result
            
            # Créer un nom de fichier unique
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            capteur_names = []
            for capteur_id in capteur_ids:
                if capteur_id in self.storage["capteurs"]:
                    capteur_names.append(self.storage["capteurs"][capteur_id]["nom"])
            
            capteur_str = "_".join(capteur_names) if capteur_names else "all"
            filename = f"{graph_type}_{capteur_str}_{timestamp}.{format}"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Décoder l'image base64
            img_data = base64.b64decode(result["image"])
            
            # Enregistrer l'image
            with open(filepath, "wb") as f:
                f.write(img_data)
            
            # Ajouter à l'historique
            self._add_history_entry("Export de graphique", None, {
                "graph_type": graph_type,
                "capteurs": capteur_names,
                "format": format,
                "filepath": filepath
            })
            
            return {
                "success": True,
                "filepath": filepath
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'export du graphique: {e}"
            }
    
    def get_history(self):
        """Obtenir l'historique des actions"""
        return {
            "success": True,
            "history": self.history
        }
    
    def export_history(self):
        """Exporter l'historique en fichier CSV"""
        try:
            # Créer un nom de fichier unique
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"historique_{timestamp}.csv"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Créer le contenu CSV
            csv_content = "Date,Action,Capteur,Détails\n"
            
            for entry in self.history:
                # Formater la date
                date_str = datetime.datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                
                # Formater le capteur
                capteur_str = entry.get("capteur_nom", "")
                
                # Formater les détails
                details_str = ""
                if entry.get("details"):
                    details = entry["details"]
                    if isinstance(details, dict):
                        details_str = "; ".join([f"{k}: {v}" for k, v in details.items()])
                    else:
                        details_str = str(details)
                
                # Échapper les virgules et les guillemets
                capteur_str = f'"{capteur_str}"' if "," in capteur_str else capteur_str
                details_str = f'"{details_str}"' if "," in details_str else details_str
                
                # Ajouter la ligne
                csv_content += f"{date_str},{entry['action']},{capteur_str},{details_str}\n"
            
            # Enregistrer le fichier
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(csv_content)
            
            return {
                "success": True,
                "filepath": filepath
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'export de l'historique: {e}"
            }


# Fonction principale
def main():
    # Créer l'API
    api = API()
    
    # Créer la fenêtre
    window = webview.create_window(
        title='ClimaGraph',
        url=os.path.join(UI_DIR, 'index.html'),
        js_api=api,
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600)
    )
    
    # Démarrer l'application
    webview.start(debug=True)


if __name__ == '__main__':
    main()

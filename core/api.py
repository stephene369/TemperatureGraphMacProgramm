"""
Module API - Fournit l'interface entre Python et JavaScript
"""
import os
import json
import uuid
import datetime
from core.storage import Storage
from core.data_loader import DataLoader
from core.graph_generator import GraphGenerator
from core.utils import add_history_entry
import webview
from print_color.print_color import print


# Définir les chemins de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "exports")

# Créer les répertoires s'ils n'existent pas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chemin du fichier de stockage
STORAGE_FILE = os.path.join(DATA_DIR, "storage.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")


class API:
    """
    Classe API pour la communication entre Python et JavaScript
    Expose les méthodes accessibles depuis l'interface web
    """

    def __init__(self, base_dir, data_dir, output_dir, image_outputdir):
        """
        Initialise l'API avec les chemins de base et charge les données

        Args:
            base_dir (str): Chemin de base de l'application
            data_dir (str): Chemin du répertoire de données
            output_dir (str): Chemin du répertoire d'exports
        """

        self.base_dir = base_dir
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.image_outputdir = image_outputdir

        # Initialiser le stockage
        self.storage = Storage(data_dir)

        # # Charger les données
        self.capteurs = self.storage.load_capteurs()
        self.history = self.storage.load_history()

        # Initialiser les autres composants
        self.data_loader = DataLoader()
        self.graph_generator = GraphGenerator(output_dir)

    # Méthodes d'API exposées à JavaScript
    def get_app_info(self):
        """Obtenir des informations sur l'application"""
        return {
            "success": True,
            "version": "1.0.0",
            "name": "ISCGraph",
            "data_dir": self.data_dir,
            "output_dir": self.output_dir,
        }

    def get_capteurs(self):
        """Obtenir la liste des capteurs"""
        capteurs = []
        for capteur_id, capteur_data in self.capteurs.items():
            if capteur_data.get("details"):
                capteur = {
                    "id": capteur_id,
                    "nom": capteur_data["nom"],
                    "file_path": capteur_data["details"].get("file_path"),
                    "columns": capteur_data.get("columns"),
                }
            else:
                capteur = {
                    "id": capteur_id,
                    "nom": capteur_data["nom"],
                    "file_path": capteur_data.get("file_path"),
                    "columns": capteur_data.get("columns"),
                }
            capteurs.append(capteur)
        return {"success": True, "capteurs": capteurs}

    def add_capteur(self, nom):
        """
        Ajouter un nouveau capteur

        Args:
            nom (str): Nom du capteur à ajouter

        Returns:
            dict: Résultat de l'opération
        """
        try:
            # Vérifier si le nom existe déjà
            for capteur in self.capteurs.values():
                if capteur["nom"] == nom:
                    return {
                        "success": False,
                        "message": f"Un capteur avec le nom '{nom}' existe déjà",
                    }

            # Créer un nouvel ID unique
            capteur_id = str(uuid.uuid4())

            # Ajouter le capteur
            self.capteurs[capteur_id] = {
                "nom": nom,
                "created_at": datetime.datetime.now().isoformat(),
            }

            # Sauvegarder les modifications
            self.storage.save_capteurs(self.capteurs)

            # Ajouter à l'historique
            add_history_entry(
                self.history, "Ajout de capteur", capteur_id, None, self.capteurs
            )
            self.storage.save_history(self.history)

            return {"success": True, "capteur_id": capteur_id}
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'ajout du capteur: {e}",
            }

    def update_capteur(self, capteur_id, nom):
        """
        Mettre à jour un capteur existant

        Args:
            capteur_id (str): ID du capteur à mettre à jour
            nom (str): Nouveau nom du capteur

        Returns:
            dict: Résultat de l'opération
        """
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.capteurs:
                return {"success": False, "message": "Capteur non trouvé"}

            # Vérifier si le nom existe déjà pour un autre capteur
            for cid, capteur in self.capteurs.items():
                if capteur["nom"] == nom and cid != capteur_id:
                    return {
                        "success": False,
                        "message": f"Un capteur avec le nom '{nom}' existe déjà",
                    }

            # Mettre à jour le capteur
            old_nom = self.capteurs[capteur_id]["nom"]
            self.capteurs[capteur_id]["nom"] = nom
            self.capteurs[capteur_id][
                "updated_at"
            ] = datetime.datetime.now().isoformat()

            # Sauvegarder les modifications
            self.storage.save_capteurs(self.capteurs)

            # Ajouter à l'historique
            add_history_entry(
                self.history,
                "Modification de capteur",
                capteur_id,
                {"old_nom": old_nom, "new_nom": nom},
                self.capteurs,
            )
            self.storage.save_history(self.history)

            return {"success": True}
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la mise à jour du capteur: {e}",
            }

    def delete_capteur(self, capteur_id):
        """
        Supprimer un capteur

        Args:
            capteur_id (str): ID du capteur à supprimer

        Returns:
            dict: Résultat de l'opération
        """
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.capteurs:
                return {"success": False, "message": "Capteur non trouvé"}

            # Récupérer le nom pour l'historique
            nom = self.capteurs[capteur_id]["nom"]

            # Supprimer le capteur
            del self.capteurs[capteur_id]

            # Sauvegarder les modifications
            self.storage.save_capteurs(self.capteurs)

            # Ajouter à l'historique
            add_history_entry(
                self.history,
                "Suppression de capteur",
                capteur_id,
                {"nom": nom},
                self.capteurs,
            )
            self.storage.save_history(self.history)

            return {"success": True}
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la suppression du capteur: {e}",
            }

    def select_file(self, capteur_id):
        """
        Sélectionner un fichier pour un capteur

        Args:
            capteur_id (str): ID du capteur

        Returns:
            dict: Résultat de l'opération
        """
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.capteurs:
                return {"success": False, "message": "Capteur non trouvé"}

            # Ouvrir la boîte de dialogue de sélection de fichier
            file_types = ("Fichiers Excel (*.xlsx;*.xls)", "Fichiers HOBO (*.hobo)", "Fichiers CSV (*.csv)")
            file_path = webview.windows[0].create_file_dialog(
                webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
            )
            if not file_path:
                return {"success": False, "message": "Aucun fichier sélectionné"}

            file_path = file_path[0]  # create_file_dialog retourne une liste

            # Charger le fichier pour vérifier qu'il est valide
            df = self.data_loader.load_file(file_path)

            # Détecter automatiquement les colonnes
            columns = self.data_loader.detect_columns(df)
            needs_mapping = not (columns.get("date") and columns.get("temperature") )

            # Mettre à jour le capteur
            self.capteurs[capteur_id]["file_path"] = file_path
            self.capteurs[capteur_id]["columns"] = columns
            self.capteurs[capteur_id][
                "file_updated_at"
            ] = datetime.datetime.now().isoformat()

            # Sauvegarder les modifications
            self.storage.save_capteurs(self.capteurs)

            # Ajouter à l'historique
            add_history_entry(
                self.history,
                "Association de fichier",
                capteur_id,
                {"file_path": file_path, "columns": columns},
                self.capteurs,
            )
            self.storage.save_history(self.history)

            return {"success": True, "needs_mapping": needs_mapping}
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la sélection du fichier: {e}",
            }

    # Autres méthodes d'API...
    # Note: Les autres méthodes seraient implémentées de manière similaire,
    # en utilisant les classes utilitaires pour la logique métier.

    def get_capteurs_for_mapping(self):
        """
        Obtenir la liste des capteurs qui ont un fichier associé

        Returns:
            dict: Résultat contenant la liste des capteurs
        """
        capteurs = []
        for capteur_id, capteur_data in self.capteurs.items():
            if capteur_data.get("file_path"):
                capteur = {
                    "id": capteur_id,
                    "nom": capteur_data["nom"],
                    "file_path": capteur_data["file_path"],
                    "columns": capteur_data.get("columns"),
                }
                capteurs.append(capteur)

        return {"success": True, "capteurs": capteurs}

    def get_columns_for_mapping(self, capteur_id):
        """
        Obtenir les colonnes disponibles pour le mappage

        Args:
            capteur_id (str): ID du capteur

        Returns:
            dict: Résultat contenant la liste des colonnes
        """

        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.capteurs:
                return {"success": False, "message": "Capteur non trouvé"}

            # Vérifier si le capteur a un fichier associé
            if not self.capteurs[capteur_id].get("file_path"):
                return {
                    "success": False,
                    "message": "Aucun fichier associé à ce capteur",
                }

            # Charger le fichier
            file_path = self.capteurs[capteur_id]["file_path"]
            df = self.data_loader.load_file(file_path)

            # Récupérer les noms des colonnes
            columns = df.columns.tolist()

            return {"success": True, "columns": columns}
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la récupération des colonnes: {e}",
            }

    def get_data_preview(self, capteur_id):
        """
        Obtenir un aperçu des données pour le mappage

        Args:
            capteur_id (str): ID du capteur

        Returns:
            dict: Résultat contenant l'aperçu des données
        """
        try:
            import logging
            import os
            import pandas as pd
            import numpy as np

            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.info("Début de get_data_preview")

            # Vérifier si le capteur existe
            if capteur_id not in self.capteurs:
                return {"success": False, "message": "Capteur non trouvé"}

            # Vérifier si le capteur a un fichier associé
            if not self.capteurs[capteur_id].get("file_path"):
                return {
                    "success": False,
                    "message": "Aucun fichier associé à ce capteur",
                }

            # Charger le fichier
            file_path = self.capteurs[capteur_id]["file_path"]
            normalized_path = os.path.normpath(file_path)

            try:
                df = self.data_loader.load_file(normalized_path)
            except Exception as e:
                logger.error(f"Erreur lors du chargement avec data_loader: {e}")

                # Fallback: essayer de charger directement avec pandas
                def try_read_with_different_headers(file_path, file_type):
                    for header_row in range(5):  # Essayer les 5 premières lignes
                        try:
                            if file_type == 'excel':
                                df = pd.read_excel(file_path, header=header_row)
                            elif file_type == 'csv':
                                df = pd.read_csv(file_path, header=header_row)
                            elif file_type == 'hobo':
                                df = pd.read_csv(file_path, sep="\t", header=header_row)
                            
                            if len(df.columns) == 2:
                                return df
                        except:
                            continue
                    return None

                if normalized_path.lower().endswith((".xlsx", ".xls")):
                    df = try_read_with_different_headers(normalized_path, 'excel')
                    if df is None:
                        raise ValueError("Impossible de trouver un format valide avec 2 colonnes pour le fichier Excel")
                elif normalized_path.lower().endswith(".csv"):
                    df = try_read_with_different_headers(normalized_path, 'csv')
                    if df is None:
                        raise ValueError("Impossible de trouver un format valide avec 2 colonnes pour le fichier CSV")
                elif normalized_path.lower().endswith(".hobo"):
                    df = try_read_with_different_headers(normalized_path, 'hobo')
                    if df is None:
                        raise ValueError("Impossible de trouver un format valide avec 2 colonnes pour le fichier HOBO")                
                    else:
                        raise ValueError(
                        f"Format de fichier non pris en charge: {normalized_path}"
                    )

            # Limiter à 10 lignes pour l'aperçu
            preview_df = df.head(6)

            # Convertir toutes les données en types sérialisables JSON
            def convert_to_serializable(val):
                if isinstance(val, (pd.Timestamp, np.datetime64)):
                    return val.isoformat() if hasattr(val, "isoformat") else str(val)
                elif isinstance(val, (np.integer, np.int64)):
                    return int(val)
                elif isinstance(val, (np.floating, float)):
                    return float(val)
                elif isinstance(val, np.ndarray):
                    return val.tolist()
                elif pd.isna(val):
                    return None
                else:
                    return str(val)

            # Convertir les colonnes et les données en format sérialisable
            columns = preview_df.columns.tolist()

            # Convertir chaque valeur dans les données
            data = []
            for _, row in preview_df.iterrows():
                serialized_row = [convert_to_serializable(val) for val in row]
                data.append(serialized_row)

            logger.info("Aperçu généré avec succès")

            # Convertir en format JSON-compatible
            preview = {"columns": columns, "data": data}

            return {"success": True, "preview": preview}
        except Exception as e:
            import traceback

            logging.error(f"Exception dans get_data_preview: {e}")
            logging.error(traceback.format_exc())
            return {
                "success": False,
                "message": f"Erreur lors de la récupération de l'aperçu: {e}",
            }

    def save_column_mapping(self, capteur_id, mapping):
        """
        Enregistrer le mappage des colonnes pour un capteur

        Args:
            capteur_id (str): ID du capteur
            mapping (dict): Mappage des colonnes

        Returns:
            dict: Résultat de l'opération
        """
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.capteurs:
                return {"success": False, "message": "Capteur non trouvé"}

            # Vérifier si le capteur a un fichier associé
            if not self.capteurs[capteur_id].get("file_path"):
                return {
                    "success": False,
                    "message": "Aucun fichier associé à ce capteur",
                }

            # Mettre à jour le mappage des colonnes
            self.capteurs[capteur_id]["columns"] = mapping
            self.capteurs[capteur_id][
                "mapping_updated_at"
            ] = datetime.datetime.now().isoformat()

            # Sauvegarder les modifications
            self.storage.save_capteurs(self.capteurs)

            # Ajouter à l'historique
            add_history_entry(
                self.history,
                "Mappage des colonnes",
                capteur_id,
                {"columns": mapping},
                self.capteurs,
            )
            self.storage.save_history(self.history)

            return {"success": True}
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'enregistrement du mappage: {e}",
            }

    def get_capteurs_for_graphs(self):
        """
        Obtenir la liste des capteurs disponibles pour les graphiques

        Returns:
            dict: Résultat contenant la liste des capteurs
        """
        capteurs = []
        for capteur_id, capteur_data in self.capteurs.items():
            # Vérifier si le capteur a un fichier et un mappage complet
            if (
                capteur_data.get("file_path")
                and capteur_data.get("columns")
                and capteur_data["columns"].get("date")
                and capteur_data["columns"].get("temperature")
            ):

                capteur = {
                    "id": capteur_id,
                    "nom": capteur_data["nom"],
                    "has_humidity": bool(capteur_data["columns"].get("humidity")),
                }
                capteurs.append(capteur)

        return {"success": True, "capteurs": capteurs}

    def get_graph_types(self):
        """
        Obtenir la liste des types de graphiques disponibles

        Returns:
            dict: Résultat contenant la liste des types de graphiques
        """
        graph_types = [
            {
                "id": "temperature_time",
                "name": "Températures quotidiennes",
                "description": "Graphique linéaire montrant l'évolution quotidienne de la température pour chaque capteur.",
            },
            {
                "id": "temperature_amplitude",
                "name": "Amplitude thermiques quotidiennes",
                "description": "Graphique linéaire montrant les écarts journaliers de température (max - min) pour chaque capteur.",
            },
            {
                "id": "humidity_time",
                "name": "Humidité relative quotidienne",
                "description": "Graphique linéaire montrant l'évolution quotidienne de l'humidité relative pour chaque capteur.",
            },
            {
                "id": "humidity_amplitude",
                "name": "Amplitude hydrique quotidienne",
                "description": "Graphique linéaire montrant les écarts journaliers d'humidité relative pour chaque capteur.",
            },
            {
                "id": "humidity_profile_per_sensor",
                "name": "Profil d'humidité par capteur",
                "description": "Pour chaque capteur, ce graphique affiche la répartition des niveaux d’humidité relative (camembert) ainsi que la distribution de l’amplitude hydrique quotidienne (histogramme).",
            },
            # {
            #     "id": "humidity_distribution_c3",
            #     "name": "Distribution de l’humidité relative (capteur C3)",
            #     "description": "Histogramme représentant la fréquence des valeurs d'humidité enregistrées par le capteur C3.",
            # },
            # {
            #     "id": "humidity_amplitude_distribution_c3",
            #     "name": "Distribution des amplitudes hydriques (capteur C3)",
            #     "description": "Histogramme représentant la fréquence des amplitudes hydriques mesurées par le capteur C3.",
            # },
            # {
            #     "id": "humidity_distribution_c4",
            #     "name": "Distribution de l’humidité relative (capteur C4)",
            #     "description": "Histogramme représentant la fréquence des valeurs d'humidité enregistrées par le capteur C4.",
            # },
            # {
            #     "id": "humidity_distribution_c6",
            #     "name": "Distribution de l’humidité relative (capteur C6)",
            #     "description": "Histogramme représentant la fréquence des valeurs d'humidité enregistrées par le capteur C6.",
            # },
            # {
            #     "id": "humidity_amplitude_distribution_c6",
            #     "name": "Distribution des amplitudes hydriques (capteur C6)",
            #     "description": "Histogramme représentant la fréquence des amplitudes hydriques mesurées par le capteur C6.",
            # },
            {
                "id": "dew_point_risk",
                "name": "Écart au point de rosée (risque de condensation)",
                "description": "Graphique montrant l’écart entre la température et le point de rosée, avec identification des zones de condensation.",
            },
        ]

        return {"success": True, "types": graph_types}
    
    
    









    def generate_graph(self, graph_type, capteur_ids, options=None):
        import pandas as pd
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Génération du graphique {graph_type} pour les capteurs {capteur_ids} avec options {options}")
            
            # Initialiser options avec un dictionnaire vide par défaut
            options = options or {}
            
            start_date = options.get('start_date')
            end_date = options.get('end_date')
            
            # Convertir les dates une seule fois si elles sont spécifiées
            start_date_obj = pd.to_datetime(start_date) if start_date else None
            end_date_obj = pd.to_datetime(end_date) if end_date else None
            
            # Vérifier la validité des dates dès le début
            if start_date_obj and end_date_obj and start_date_obj > end_date_obj:
                return {
                    "success": False,
                    "message": "La date de début doit être antérieure à la date de fin"
                }
            
            # Définir les types de graphiques qui nécessitent des colonnes spécifiques
            humidity_graphs = {
                "humidity_time", "temperature_humidity", "humidity_monthly", 
                "humidity_daily", "humidity_distribution", "humidity_amplitude", 
                "humidity_profile_per_sensor"
            }
            dew_point_graphs = {"dew_point_risk"}
            
            # Vérifier que les capteurs existent et préparer les données
            capteurs_data = {}
            time_deltas = {}
            largest_time_delta = None
            
            for capteur_id in capteur_ids:
                # Vérifications préliminaires
                if capteur_id not in self.capteurs:
                    return {"success": False, "message": f"Capteur {capteur_id} non trouvé"}
                    
                capteur_data = self.capteurs[capteur_id]
                capteur_nom = capteur_data['nom']
                
                if not capteur_data.get("file_path"):
                    return {"success": False, "message": f"Le capteur {capteur_nom} n'a pas de fichier associé"}
                
                columns = capteur_data.get("columns", {})
                if not all(columns.get(col) for col in ["date", "temperature"]):
                    return {"success": False, "message": f"Le capteur {capteur_nom} n'a pas de mappage complet pour les colonnes obligatoires"}
                
                # Vérifier les colonnes spécifiques selon le type de graphique
                if graph_type in humidity_graphs and not columns.get("humidity"):
                    return {"success": False, "message": f"Le capteur {capteur_nom} n'a pas de données d'humidité nécessaires pour ce graphique"}
                    
                if graph_type in dew_point_graphs and not columns.get("dew_point"):
                    return {"success": False, "message": f"Le capteur {capteur_nom} n'a pas de données de point de rosée nécessaires pour ce graphique"}
                
                # Charger et traiter les données
                try:
                    df = self.data_loader.load_capteur_data(capteur_data)
                    
                    # Convertir la colonne de date en datetime si nécessaire
                    if not pd.api.types.is_datetime64_any_dtype(df['date']):
                        df['date'] = pd.to_datetime(df['date'])
                    
                    # Filtrer par date si spécifié
                    if start_date_obj or end_date_obj:
                        # Vérifier que les dates sont dans la plage des données
                        if start_date_obj and start_date_obj > df['date'].max():
                            return {"success": False, "message": f"La date de début est postérieure à toutes les données pour le capteur {capteur_nom}"}
                        
                        if end_date_obj and end_date_obj < df['date'].min():
                            return {"success": False, "message": f"La date de fin est antérieure à toutes les données pour le capteur {capteur_nom}"}
                        
                        # Appliquer les filtres de date
                        if start_date_obj:
                            df = df[df['date'] >= start_date_obj]
                        if end_date_obj:
                            df = df[df['date'] <= end_date_obj]
                    
                    # Vérifier si le dataframe est vide après filtrage
                    if df.empty:
                        return {"success": False, "message": f"Aucune donnée disponible pour le capteur {capteur_nom} dans la plage de dates spécifiée"}
                    
                    # Calculer l'amplitude de temps
                    df = df.sort_values('date')
                    time_diffs = df['date'].diff().dropna()
                    
                    if not time_diffs.empty:
                        median_time_delta = time_diffs.median()
                        time_deltas[capteur_id] = median_time_delta
                        
                        # Mettre à jour la plus grande amplitude
                        if largest_time_delta is None or median_time_delta > largest_time_delta:
                            largest_time_delta = median_time_delta
                    
                    # Stocker les données
                    capteurs_data[capteur_id] = {"nom": capteur_nom, "data": df}
                    
                except Exception as e:
                    logger.error(f"Erreur lors du chargement des données: {e}")
                    return {"success": False, "message": f"Erreur lors du chargement des données pour {capteur_nom}: {e}"}
            
            # Vérifier si tous les capteurs ont le même intervalle de temps
            need_normalization = False
            if len(time_deltas) > 1:
                first_delta = next(iter(time_deltas.values()))
                for delta in time_deltas.values():
                    if delta != first_delta:
                        need_normalization = True
                        break
            
            # Normaliser les données seulement si nécessaire
            if need_normalization and largest_time_delta is not None:
                logger.info("Normalisation des données avec différents intervalles de temps")
                for capteur_id, capteur in capteurs_data.items():
                    df = capteur["data"]
                    
                    # Supprimer les doublons de date
                    if df['date'].duplicated().any():
                        df = df.drop_duplicates(subset=['date'], keep='first')
                    
                    # Créer un nouvel index de temps
                    min_date, max_date = df['date'].min(), df['date'].max()
                    new_index = pd.date_range(start=min_date, end=max_date, freq=largest_time_delta)
                    
                    # Réindexer avec interpolation
                    df_reindexed = df.set_index('date').reindex(new_index).interpolate(method='time')
                    df_reindexed.reset_index(inplace=True)
                    df_reindexed.rename(columns={'index': 'date'}, inplace=True)
                    
                    capteurs_data[capteur_id]["data"] = df_reindexed
            else:
                logger.info("Normalisation ignorée - tous les capteurs ont le même intervalle de temps ou un seul capteur sélectionné")
            
            # Utiliser un dictionnaire pour mapper les types de graphiques aux méthodes
            graph_generators = {
                "temperature_time": self.graph_generator.generate_temperature_time_graph,
                "humidity_time": self.graph_generator.generate_humidity_time_graph,
                "temperature_amplitude": self.graph_generator.generate_temperature_amplitude_graph,
                "humidity_amplitude": self.graph_generator.generate_humidity_amplitude_graph,
                "humidity_profile_per_sensor": self.graph_generator.generate_all_humidity_distribution_pair_graphs,
                "dew_point_risk": self.graph_generator.generate_dew_point_risk_graph_
            }
            
            # Générer le graphique
            if graph_type in graph_generators:
                return graph_generators[graph_type](capteurs_data)
            else:
                return {"success": False, "message": f"Type de graphique non pris en charge: {graph_type}"}
                
        except Exception as e:
            import traceback
            logger.error(f"Exception dans generate_graph: {e}")
            logger.error(traceback.format_exc())
            return {"success": False, "message": f"Erreur lors de la génération du graphique: {e}"}

        



    
    
    
    
    
    


    def export_graph(self, graph_type, capteur_ids, format="png"):
        """
        Exporter un graphique en fichier image

        Args:
            graph_type (str): Type de graphique à exporter
            capteur_ids (list): Liste des IDs des capteurs
            format (str): Format d'export (png, jpg, pdf)

        Returns:
            dict: Résultat de l'opération
        """
        try:
            # Générer le graphique
            result = self.generate_graph(graph_type, capteur_ids)

            if not result["success"]:
                return result

            # Créer un nom de fichier unique
            capteur_names = []
            for capteur_id in capteur_ids:
                if capteur_id in self.capteurs:
                    capteur_names.append(self.capteurs[capteur_id]["nom"])

            capteur_str = "_".join(capteur_names) if capteur_names else "all"
            filename = f"{graph_type}_{capteur_str}"

            # Exporter le graphique
            filepath = self.graph_generator.export_graph(result, filename, format)

            # Ajouter à l'historique
            add_history_entry(
                self.history,
                "Export de graphique",
                None,
                {
                    "graph_type": graph_type,
                    "capteurs": capteur_names,
                    "format": format,
                    "filepath": filepath,
                },
                self.capteurs,
            )
            self.storage.save_history(self.history)

            return {"success": True, "filepath": filepath}
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'export du graphique: {e}",
            }

    def get_history(self):
        """
        Obtenir l'historique des actions

        Returns:
            dict: Résultat contenant l'historique
        """
        return {"success": True, "history": self.history}

    def export_history(self):
        """
        Exporter l'historique en fichier CSV

        Returns:
            dict: Résultat de l'opération
        """
        try:
            # Créer un nom de fichier unique
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"historique_{timestamp}.csv"
            filepath = os.path.join(self.output_dir, filename)

            # Créer le contenu CSV
            csv_content = "Date,Action,Capteur,Détails\n"

            for entry in self.history:
                # Formater la date
                date_str = datetime.datetime.fromisoformat(entry["timestamp"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                # Formater le capteur
                capteur_str = entry.get("capteur_nom", "")

                # Formater les détails
                details_str = ""
                if entry.get("details"):
                    details = entry["details"]
                    if isinstance(details, dict):
                        details_str = "; ".join(
                            [f"{k}: {v}" for k, v in details.items()]
                        )
                    else:
                        details_str = str(details)

                # Échapper les virgules et les guillemets
                capteur_str = f'"{capteur_str}"' if "," in capteur_str else capteur_str
                details_str = f'"{details_str}"' if "," in details_str else details_str

                # Ajouter la ligne
                csv_content += (
                    f"{date_str},{entry['action']},{capteur_str},{details_str}\n"
                )

            # Enregistrer le fichier
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(csv_content)

            return {"success": True, "filepath": filepath}
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'export de l'historique: {e}",
            }

    def _save_storage(self):
        """Sauvegarder les données de stockage dans le fichier JSON"""
        try:
            # Fonction pour convertir les objets non-sérialisables
            def json_serializable(obj):
                import pandas as pd
                import numpy as np
                import datetime

                if isinstance(obj, (pd.Timestamp, datetime.datetime, datetime.date)):
                    return obj.isoformat()
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, pd.Series):
                    return obj.tolist()
                elif hasattr(pd, "isna") and pd.isna(obj):
                    return None
                return obj

            with open(STORAGE_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    self.storage,
                    f,
                    ensure_ascii=False,
                    indent=2,
                    default=json_serializable,
                )
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du stockage: {e}")
            return False

    def _save_history(self):
        """Sauvegarder l'historique dans le fichier JSON"""
        try:
            # Fonction pour convertir les objets non-sérialisables
            def json_serializable(obj):
                import pandas as pd
                import numpy as np
                import datetime

                if isinstance(obj, (pd.Timestamp, datetime.datetime, datetime.date)):
                    return obj.isoformat()
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, pd.Series):
                    return obj.tolist()
                elif hasattr(pd, "isna") and pd.isna(obj):
                    return None
                return obj

            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    self.history,
                    f,
                    ensure_ascii=False,
                    indent=2,
                    default=json_serializable,
                )
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique: {e}")
            return False

    def save_image_with_dialog(
        self, image_base64, default_name="graphique", capteurId=""
    ):
        """
        Ouvrir une boîte de dialogue pour enregistrer une image

        Args:
            image_base64 (str): Image en format base64
            default_name (str): Nom par défaut du fichier

        Returns:
            dict: Résultat de l'opération
        """
        try:
            import base64
            import os

            # Préparer le nom de fichier par défaut
            capteur = ""
            # print(self.capteurs, color='blue')
            if capteurId:
                try:
                    capteur = self.capteurs[capteurId]["nom"]
                except Exception as e:
                    print(e)

            default_filename = f"{default_name.replace(' ', '_')}-Capteur-{capteur}--{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

            # Ouvrir la boîte de dialogue de sauvegarde
            file_path = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG,
                directory=self.image_outputdir,
                save_filename=default_filename,
                file_types=(
                    "Images PNG (*.png)",
                    "Images JPEG (*.jpg;*.jpeg)",
                    "Documents PDF (*.pdf)",
                ),
            )

            if not file_path:
                # L'utilisateur a annulé
                return {
                    "success": False,
                    "message": "Opération annulée par l'utilisateur",
                }

            # Décoder l'image base64
            img_data = base64.b64decode(image_base64)

            # Enregistrer l'image
            with open(file_path, "wb") as f:
                f.write(img_data)

            return {"success": True, "filepath": file_path}
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {
                "success": False,
                "message": f"Erreur lors de l'enregistrement de l'image: {e}",
            }

    def save_all_images_with_dialog(self, graph_images, capteurId=""):
        """
        Ouvrir une boîte de dialogue pour choisir un dossier et y enregistrer toutes les images

        Args:
            graph_images (list): Liste de dictionnaires contenant les images et leurs noms

        Returns:
            dict: Résultat de l'opération
        """

        try:

            import base64
            import os

            # Ouvrir la boîte de dialogue pour sélectionner un dossier
            folder_path = webview.windows[0].create_file_dialog(
                webview.FOLDER_DIALOG, directory=self.image_outputdir
            )

            if not folder_path:
                # L'utilisateur a annulé
                return {
                    "success": False,
                    "message": "Opération annulée par l'utilisateur",
                }

            folder_path = folder_path[0]  # create_file_dialog retourne une liste
            capteur = ""
            if capteurId:
                try:
                    capteur = self.capteurs[capteurId]["nom"]
                except Exception as e:
                    print(e)
            # Créer le dossier s'il n'existe pas
            os.makedirs(folder_path, exist_ok=True)

            # Enregistrer chaque image
            saved_files = []
            for graph in graph_images:
                try:
                    # Préparer le nom de fichier
                    filename = f"{graph['name'].replace(' ', '_')}-id-{graph['id']}-{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    filepath = os.path.join(folder_path, filename)

                    # Décoder l'image base64
                    img_data = base64.b64decode(graph["image"])

                    # Enregistrer l'image
                    with open(filepath, "wb") as f:
                        f.write(img_data)

                    saved_files.append(filepath)
                except Exception as e:
                    print(
                        f"Erreur lors de l'enregistrement de l'image {graph['name']}: {e}"
                    )

            return {"success": True, "folder_path": folder_path, "files": saved_files}
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {
                "success": False,
                "message": f"Erreur lors de l'enregistrement des images: {e}",
            }

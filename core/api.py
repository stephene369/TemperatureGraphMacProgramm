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

class API:
    """
    Classe API pour la communication entre Python et JavaScript
    Expose les méthodes accessibles depuis l'interface web
    """
    def __init__(self, base_dir, data_dir, output_dir):
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
        
        # Initialiser le stockage
        self.storage = Storage(data_dir)
        
        # Charger les données
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
            "name": "ClimaGraph",
            "data_dir": self.data_dir,
            "output_dir": self.output_dir
        }
    
    def get_capteurs(self):
        """Obtenir la liste des capteurs"""
        capteurs = []
        for capteur_id, capteur_data in self.capteurs.items():
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
                        "message": f"Un capteur avec le nom '{nom}' existe déjà"
                    }
            
            # Créer un nouvel ID unique
            capteur_id = str(uuid.uuid4())
            
            # Ajouter le capteur
            self.capteurs[capteur_id] = {
                "nom": nom,
                "created_at": datetime.datetime.now().isoformat()
            }
            
            # Sauvegarder les modifications
            self.storage.save_capteurs(self.capteurs)
            
            # Ajouter à l'historique
            add_history_entry(self.history, "Ajout de capteur", capteur_id, None, self.capteurs)
            self.storage.save_history(self.history)
            
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
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Vérifier si le nom existe déjà pour un autre capteur
            for cid, capteur in self.capteurs.items():
                if capteur["nom"] == nom and cid != capteur_id:
                    return {
                        "success": False,
                        "message": f"Un capteur avec le nom '{nom}' existe déjà"
                    }
            
            # Mettre à jour le capteur
            old_nom = self.capteurs[capteur_id]["nom"]
            self.capteurs[capteur_id]["nom"] = nom
            self.capteurs[capteur_id]["updated_at"] = datetime.datetime.now().isoformat()
            
            # Sauvegarder les modifications
            self.storage.save_capteurs(self.capteurs)
            
            # Ajouter à l'historique
            add_history_entry(
                self.history, 
                "Modification de capteur", 
                capteur_id, 
                {"old_nom": old_nom, "new_nom": nom},
                self.capteurs
            )
            self.storage.save_history(self.history)
            
            return {
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la mise à jour du capteur: {e}"
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
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
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
                self.capteurs
            )
            self.storage.save_history(self.history)
            
            return {
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la suppression du capteur: {e}"
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
            df = self.data_loader.load_file(file_path)
            
            # Détecter automatiquement les colonnes
            columns = self.data_loader.detect_columns(df)
            needs_mapping = not (columns.get('date') and columns.get('temperature'))
            
            # Mettre à jour le capteur
            self.capteurs[capteur_id]["file_path"] = file_path
            self.capteurs[capteur_id]["columns"] = columns
            self.capteurs[capteur_id]["file_updated_at"] = datetime.datetime.now().isoformat()
            
            # Sauvegarder les modifications
            self.storage.save_capteurs(self.capteurs)
            
            # Ajouter à l'historique
            add_history_entry(
                self.history, 
                "Association de fichier", 
                capteur_id, 
                {"file_path": file_path, "columns": columns},
                self.capteurs
            )
            self.storage.save_history(self.history)
            
            return {
                "success": True,
                "needs_mapping": needs_mapping
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la sélection du fichier: {e}"
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
                    "columns": capteur_data.get("columns")
                }
                capteurs.append(capteur)
        
        return {
            "success": True,
            "capteurs": capteurs
        }

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
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Vérifier si le capteur a un fichier associé
            if not self.capteurs[capteur_id].get("file_path"):
                return {
                    "success": False,
                    "message": "Aucun fichier associé à ce capteur"
                }
            
            # Charger le fichier
            file_path = self.capteurs[capteur_id]["file_path"]
            df = self.data_loader.load_file(file_path)
            
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
        """
        Obtenir un aperçu des données pour le mappage
        
        Args:
            capteur_id (str): ID du capteur
            
        Returns:
            dict: Résultat contenant l'aperçu des données
        """
        try:
            # Vérifier si le capteur existe
            if capteur_id not in self.capteurs:
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Vérifier si le capteur a un fichier associé
            if not self.capteurs[capteur_id].get("file_path"):
                return {
                    "success": False,
                    "message": "Aucun fichier associé à ce capteur"
                }
            
            # Charger le fichier
            file_path = self.capteurs[capteur_id]["file_path"]
            df = self.data_loader.load_file(file_path)
            
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
                return {
                    "success": False,
                    "message": "Capteur non trouvé"
                }
            
            # Vérifier si le capteur a un fichier associé
            if not self.capteurs[capteur_id].get("file_path"):
                return {
                    "success": False,
                    "message": "Aucun fichier associé à ce capteur"
                }
            
            # Mettre à jour le mappage des colonnes
            self.capteurs[capteur_id]["columns"] = mapping
            self.capteurs[capteur_id]["mapping_updated_at"] = datetime.datetime.now().isoformat()
            
            # Sauvegarder les modifications
            self.storage.save_capteurs(self.capteurs)
            
            # Ajouter à l'historique
            add_history_entry(
                self.history, 
                "Mappage des colonnes", 
                capteur_id, 
                {"columns": mapping},
                self.capteurs
            )
            self.storage.save_history(self.history)
            
            return {
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'enregistrement du mappage: {e}"
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
        """
        Obtenir la liste des types de graphiques disponibles
        
        Returns:
            dict: Résultat contenant la liste des types de graphiques
        """
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
            # Ajouter les autres types de graphiques ici...
        ]
        
        return {
            "success": True,
            "types": graph_types
        }

    def generate_graph(self, graph_type, capteur_ids):
        """
        Générer un graphique à partir des données des capteurs
        
        Args:
            graph_type (str): Type de graphique à générer
            capteur_ids (list): Liste des IDs des capteurs
            
        Returns:
            dict: Résultat contenant les données du graphique
        """
        try:
            # Vérifier que les capteurs existent
            capteurs_data = {}
            for capteur_id in capteur_ids:
                if capteur_id not in self.capteurs:
                    return {
                        "success": False,
                        "message": f"Capteur {capteur_id} non trouvé"
                    }
                
                capteur_data = self.capteurs[capteur_id]
                
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
                try:
                    df = self.data_loader.load_capteur_data(capteur_data)
                    
                    # Stocker les données
                    capteurs_data[capteur_id] = {
                        "nom": capteur_data["nom"],
                        "data": df
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "message": f"Erreur lors du chargement des données pour {capteur_data['nom']}: {e}"
                    }
            
            # Générer le graphique en fonction du type
            if graph_type == "temperature_time":
                return self.graph_generator.generate_temperature_time_graph(capteurs_data)
            elif graph_type == "humidity_time":
                return self.graph_generator.generate_humidity_time_graph(capteurs_data)
            # Ajouter les autres types de graphiques ici...
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
                    "filepath": filepath
                },
                self.capteurs
            )
            self.storage.save_history(self.history)
            
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
        """
        Obtenir l'historique des actions
        
        Returns:
            dict: Résultat contenant l'historique
        """
        return {
            "success": True,
            "history": self.history
        }

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

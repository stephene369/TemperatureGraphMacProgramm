"""
Module de stockage pour l'application ClimaGraph
"""

import os
import json
import sqlite3
from datetime import datetime

class Storage:
    """Classe de gestion du stockage des données"""
    
    def __init__(self, storage_type="json"):
        """Initialise le stockage"""
        self.storage_type = storage_type
        
        # Créer le dossier de données s'il n'existe pas
        os.makedirs("data", exist_ok=True)
        
        if storage_type == "sqlite":
            # Initialiser la base de données SQLite
            self.init_sqlite_db()
            
    def init_sqlite_db(self):
        """Initialise la base de données SQLite"""
        conn = sqlite3.connect("data/climagraph.db")
        cursor = conn.cursor()
        
        # Créer la table des capteurs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS capteurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            file_path TEXT,
            imported_at TEXT
        )
        ''')
        
        # Créer la table des mappages de colonnes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS column_mappings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capteur_id INTEGER,
            data_type TEXT,
            column_name TEXT,
            FOREIGN KEY (capteur_id) REFERENCES capteurs (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def save_capteurs(self, capteurs):
        """Sauvegarde les capteurs"""
        if self.storage_type == "json":
            self._save_capteurs_json(capteurs)
        elif self.storage_type == "sqlite":
            self._save_capteurs_sqlite(capteurs)
            
    def _save_capteurs_json(self, capteurs):
        """Sauvegarde les capteurs dans un fichier JSON"""
        with open("data/capteurs.json", "w") as f:
            json.dump({"capteurs": capteurs}, f, indent=2)
            
    def _save_capteurs_sqlite(self, capteurs):
        """Sauvegarde les capteurs dans la base de données SQLite"""
        conn = sqlite3.connect("data/climagraph.db")
        cursor = conn.cursor()
        
        # Vider les tables
        cursor.execute("DELETE FROM column_mappings")
        cursor.execute("DELETE FROM capteurs")
        
        # Insérer les capteurs
        for name, data in capteurs.items():
            cursor.execute(
                "INSERT INTO capteurs (name, file_path, imported_at) VALUES (?, ?, ?)",
                (name, data["file_path"], data.get("imported_at", datetime.now().isoformat()))
            )
            
            capteur_id = cursor.lastrowid
            
            # Insérer les mappages de colonnes
            for data_type, column_name in data.get("columns", {}).items():
                cursor.execute(
                    "INSERT INTO column_mappings (capteur_id, data_type, column_name) VALUES (?, ?, ?)",
                    (capteur_id, data_type, column_name)
                )
                
        conn.commit()
        conn.close()
        
    def load_capteurs(self):
        """Charge les capteurs"""
        if self.storage_type == "json":
            return self._load_capteurs_json()
        elif self.storage_type == "sqlite":
            return self._load_capteurs_sqlite()
            
    def _load_capteurs_json(self):
        """Charge les capteurs depuis un fichier JSON"""
        if os.path.exists("data/capteurs.json"):
            with open("data/capteurs.json", "r") as f:
                data = json.load(f)
                return data.get("capteurs", {})
        return {}
        
    def _load_capteurs_sqlite(self):
        """Charge les capteurs depuis la base de données SQLite"""
        capteurs = {}
        
        conn = sqlite3.connect("data/climagraph.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Récupérer tous les capteurs
        cursor.execute("SELECT * FROM capteurs")
        capteur_rows = cursor.fetchall()
        
        for capteur_row in capteur_rows:
            capteur_id = capteur_row["id"]
            name = capteur_row["name"]
            
            # Récupérer les mappages de colonnes pour ce capteur
            cursor.execute("SELECT * FROM column_mappings WHERE capteur_id = ?", (capteur_id,))
            mapping_rows = cursor.fetchall()
            
            columns = {}
            for mapping_row in mapping_rows:
                data_type = mapping_row["data_type"]
                column_name = mapping_row["column_name"]
                columns[data_type] = column_name
                
            capteurs[name] = {
                "file_path": capteur_row["file_path"],
                "imported_at": capteur_row["imported_at"],
                "columns": columns
            }
            
        conn.close()
        
        return capteurs

"""
Configuration de l'application ClimaGraph
"""

# Chemins des dossiers
DATA_DIR = "data"
EXPORT_DIR = "output/exports"

# Types de fichiers supportés
SUPPORTED_FILE_TYPES = [
    "Excel (*.xlsx)",
    "HOBO (*.hobo)",
    "CSV (*.csv)"
]

# Configuration des graphiques
GRAPH_TYPES = [
    "Température moyenne par mois",
    "Humidité moyenne par mois",
    "Température et humidité",
    "Comparaison entre capteurs"
]

# Couleurs des graphiques
GRAPH_COLORS = [
    "#1f77b4",  # Bleu
    "#ff7f0e",  # Orange
    "#2ca02c",  # Vert
    "#d62728",  # Rouge
    "#9467bd",  # Violet
    "#8c564b",  # Marron
    "#e377c2",  # Rose
    "#7f7f7f",  # Gris
    "#bcbd22",  # Jaune-vert
    "#17becf"   # Bleu clair
]

# Configuration de l'interface
UI_CONFIG = {
    "sidebar_width": 200,
    "min_window_width": 800,
    "min_window_height": 600,
    "default_theme": "auto"  # "light", "dark", "auto"
}

#!/bin/bash

# Définir les couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Script d'installation de ClimaGraph pour macOS ===${NC}"

# Vérifier si Homebrew est installé
if ! command -v brew &> /dev/null; then
    echo -e "${BLUE}Installation de Homebrew...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Ajouter Homebrew au PATH
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    echo -e "${GREEN}Homebrew est déjà installé.${NC}"
fi

# Installer Python 3.11
echo -e "${BLUE}Installation de Python 3.11...${NC}"
brew install python@3.11

# Lier Python 3.11
brew link --force python@3.11

# Vérifier l'installation de Python
python_version=$(python3 --version)
echo -e "${GREEN}$python_version installé avec succès.${NC}"

# Aller dans le dossier Documents
echo -e "${BLUE}Navigation vers le dossier Documents...${NC}"
cd ~/Documents

# Vérifier si Chrome est installé
if [ ! -d "/Applications/Google Chrome.app" ]; then
    echo -e "${BLUE}Google Chrome n'est pas installé. Installation en cours...${NC}"
    # Chrome est gratuit sur macOS
    brew install --cask google-chrome
    echo -e "${GREEN}Google Chrome installé avec succès.${NC}"
else
    echo -e "${GREEN}Google Chrome est déjà installé.${NC}"
fi

# Créer le dossier ClimatGraphCode
echo -e "${BLUE}Création du dossier ClimatGraphCode...${NC}"
mkdir -p ClimatGraphCode
cd ClimatGraphCode

# Installer git si nécessaire
if ! command -v git &> /dev/null; then
    echo -e "${BLUE}Installation de Git...${NC}"
    brew install git
fi

# Cloner le dépôt
echo -e "${BLUE}Clonage du dépôt GitHub...${NC}"
git clone https://github.com/stephene369/TemperatureGraphMacProgramm.git
cd TemperatureGraphMacProgramm

# Créer un environnement virtuel
echo -e "${BLUE}Création de l'environnement virtuel...${NC}"
python3 -m venv venv

# Activer l'environnement virtuel
echo -e "${BLUE}Activation de l'environnement virtuel...${NC}"
source venv/bin/activate

# Installer les dépendances depuis requirements.txt
echo -e "${BLUE}Installation des dépendances...${NC}"
pip install --upgrade pip

# Installer les dépendances principales
pip install matplotlib numpy openpyxl packaging pandas python-dateutil pytz pywebview pyinstaller

# Installer PyInstaller si ce n'est pas déjà fait
if ! pip show pyinstaller &> /dev/null; then
    echo -e "${BLUE}Installation de PyInstaller...${NC}"
    pip install pyinstaller
fi

# Créer l'exécutable avec PyInstaller
echo -e "${BLUE}Création de l'exécutable avec PyInstaller...${NC}"

# Vérifier si l'icône existe
ICON_PATH=""
if [ -f "ui/assets/img/app_icon.icns" ]; then
    ICON_PATH="ui/assets/img/app_icon.icns"
elif [ -f "ui/assets/img/app_icon.ico" ]; then
    ICON_PATH="ui/assets/img/app_icon.ico"
elif [ -f "ui/assets/img/logo.png" ]; then
    ICON_PATH="ui/assets/img/logo.png"
fi

# Commande PyInstaller avec ou sans icône
if [ -n "$ICON_PATH" ]; then
    pyinstaller --noconfirm --onefile --windowed --icon "$ICON_PATH" --name "ClimaGraph" --clean --add-data "ui:ui/" "main.py"
else
    pyinstaller --noconfirm --onefile --windowed --name "ClimaGraph" --clean --add-data "ui:ui/" "main.py"
fi

# Vérifier si l'exécutable a été créé
if [ -d "dist/ClimaGraph.app" ]; then
    echo -e "${GREEN}Exécutable créé avec succès!${NC}"
    
    # Copier l'application dans le dossier Applications
    echo -e "${BLUE}Installation de l'application dans le dossier Applications...${NC}"
    cp -R dist/ClimaGraph.app /Applications/
    
    # Lancer l'application
    echo -e "${BLUE}Lancement de l'application ClimaGraph...${NC}"
    open /Applications/ClimaGraph.app
    
    echo -e "${GREEN}=== Installation terminée avec succès! ===${NC}"
    echo -e "${GREEN}L'application ClimaGraph est maintenant installée dans votre dossier Applications.${NC}"
else
    echo -e "${RED}Impossible de trouver l'exécutable généré.${NC}"
    echo -e "${RED}Veuillez vérifier le dossier 'dist' et réessayer.${NC}"
    
    # Afficher le contenu du dossier dist pour le débogage
    echo -e "${BLUE}Contenu du dossier dist:${NC}"
    ls -la dist/
fi

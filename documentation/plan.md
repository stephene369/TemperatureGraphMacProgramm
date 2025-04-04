
---

## ✅ **Plan de travail pour le développeur**

Ce plan est conçu pour guider étape par étape la création d’une application robuste, modulaire et évolutive.

---

### 🧱 1. STRUCTURE DE PROJET

#### Arborescence suggérée :

```
ClimaGraph/
├── main.py
├── ui/                    # Composants d'interface (FluentWidgets)
│   ├── main_window.py
│   ├── capteur_selector.py
│   ├── column_mapper.py
│   └── graph_display.py
│
├── core/                  # Logique métier
│   ├── models.py          # Capteur, Dataset, Colonnes, Historique
│   ├── file_loader.py
│   ├── column_detector.py
│   └── graph_simulator.py
│
├── services/              # Persistance & logique transversale
│   ├── storage.py         # Sauvegarde historique (JSON ou SQLite)
│   ├── config.py          # Fichier de config (structure, paths)
│   └── logger.py
│
├── utils/                 # Outils utiles (threading, formats)
│   ├── worker.py          # Threading: QRunnable + QThreadPool
│   └── validators.py
│
├── assets/
│   └── icons/
│
└── output/
    └── exports/           # Graphiques exportés
```

---

### 🧩 2. FONCTIONNALITÉS CLÉS À IMPLÉMENTER

#### 📁 2.1 - Gestion des capteurs & fichiers
- Ajouter un **capteur** avec un nom personnalisé
- Associer **1 fichier de données** à chaque capteur
- Sauvegarde de cette association dans l’**historique local**

#### <i class='bx bx-brain' style="color: #4a6cf7;"></i>
 2.2 - Détection automatique des colonnes
- Lecture de la première ligne → Détection automatique des colonnes :
  - `Date`, `Température`, `Humidité`
- Si non détecté → Interface de **mappage manuel par l’utilisateur**

#### 💾 2.3 - Sauvegarde de l’historique (important)
- Pour chaque capteur :
  - Chemin du fichier
  - Mappage des colonnes
  - Date d’import
- Sauvegardé dans :
  - Soit un fichier `.json`
  - Soit une petite **base SQLite locale**

Exemple d’entrée JSON :

```json
{
  "capteurs": {
    "Est": {
      "file_path": "path/to/file.xlsx",
      "columns": {
        "date": "Horodatage",
        "temperature": "Température",
        "humidity": "HR"
      },
      "imported_at": "2025-04-03T15:21:00"
    }
  }
}
```

---

### 📊 3. SIMULATION DE GRAPHIQUE

#### Type :
- Simple **histogramme** ou **bar plot** basé sur des données aléatoires
- Par exemple : "Moyenne de température par mois (simulée)"

#### Affichage :
- Utiliser `matplotlib` intégré via `FigureCanvasQTAgg`
- Affichage dans la vue principale `FluentPage` avec les contrôles de sélection

#### Export :
- Exporter en `.png` ou `.pdf` dans `/output/exports/`

---

### 🧵 4. ROBUSTESSE & THREADING

- Utiliser **`QThreadPool` + `QRunnable`** pour :
  - Lecture fichier
  - Génération de graph
- Mise à jour de l’interface avec des `pyqtSignal`
- Aucun freeze même si les fichiers sont gros

---

### <i class='bx bx-brain' style="color: #4a6cf7;"></i>
 5. DESIGN UI (avec PyQt-FluentWidgets)

#### 🧭 Navigation
- **Sidebar** :
  - 🏠 Accueil
  - 📁 Capteurs & Fichiers
  - <i class='bx bx-brain' style="color: #4a6cf7;"></i>
 Mappage des Colonnes
  - 📊 Graphique Simulé
  - 🕓 Historique

#### 🪟 Pages :
- **CapteurSelectorPage** : liste, ajout, édition
- **ColumnMapperPage** : liste déroulante pour mapper les colonnes
- **GraphPage** : bouton → génère histogramme simulé
- **HistoriquePage** : tableau avec tous les imports

---

## 🧪 EXEMPLES DE TÂCHES POUR LE DEV

### Étape 1 – Base de projet
- Installer PyQt5 + FluentWidgets + matplotlib
- Créer les dossiers & la navigation de base avec les pages

### Étape 2 – Interface capteurs
- Ajouter capteur
- Associer un fichier
- Sauvegarder l’info dans un fichier `.json`

### Étape 3 – Détection + mappage
- Lire les colonnes du fichier Excel
- Si colonne non reconnue → ouvrir fenêtre de mappage

### Étape 4 – Génération graphique simulé
- Bar plot : température moyenne par mois (générée aléatoirement)
- Afficher et exporter

### Étape 5 – Ajout de threading
- Utiliser QThreadPool pour génération de graph sans bloquer l’interface

---








- Ajouter **des remarques internes** ou **instructions personnalisées**
- Laisser des **notes explicatives pour l'utilisateur final** ou pour le développeur
- Ou tout simplement y afficher du **contenu dynamique d'aide ou d'état**

---

## 📐 Structure type pour **chaque page de l’application**

Chaque page (vue) dans ton interface PyQt-FluentWidgets inclura :

### 🧭 Navigation principale
Utilisation de `NavigationInterface` de FluentWidgets, avec des `NavigationItem` vers :

- Accueil
- Capteurs
- Mappage des colonnes
- Graphique simulé
- Historique

---

## 📄 Composants de chaque page

Chaque `Page` contiendra cette **structure visuelle de base** :

### ✅ 1. **En-tête clair**
```plaintext
📌 Titre de la page (ex: "Gestion des capteurs")
🧾 Sous-titre (court résumé ou consigne)
```

### <i class='bx bx-brain' style="color: #4a6cf7;"></i>
 2. **Zone de contenu principal**
Contient le formulaire, les boutons ou les vues interactives.

### 💬 3. **Zone de remarque ou instructions**
Un composant `InfoBar` ou une `TextArea`/`TextLabel` visible en permanence :
- Permet d’ajouter une note, une aide, une explication
- Éditable ou statique selon besoin

Exemple :
```plaintext
💡 Remarques / Consignes :
- Veuillez charger un fichier par capteur.
- Le nom du capteur doit être unique.
- En cas d’erreur de lecture, utilisez la page de mappage.
```

### 📦 4. **Pied de page facultatif**
Avec des boutons secondaires :
- Annuler / Réinitialiser / Sauvegarder
- Afficher plus d’options (ex: bouton “Avancé”)

---

## 🧩 Exemple d’une page "Capteurs"

```plaintext
📌 Capteurs & Fichiers
🧾 Associez un fichier de données à chaque capteur

───────────────
[ + Ajouter un capteur ]
[ 🔍 Liste des capteurs ]  ← TableView
───────────────

💬 Remarques :
- Un capteur correspond à un point de mesure.
- Les fichiers peuvent être en .xlsx ou .hobo (plus tard).
- L’historique est sauvegardé automatiquement.

[ Enregistrer ]  [ Suivant → Mappage des colonnes ]
```

---

## 📘 Exemple de composants FluentWidgets à utiliser

| Élément                | Widget Qt / Fluent          |
|------------------------|-----------------------------|
| Remarque non éditable  | `InfoBar`, `Label`, `MessageBox` |
| Remarque éditable      | `TextEdit`, `PlainTextEdit` |
| Aide contextuelle      | `ToolTip`, `IconButton` avec popover |
| Actions utilisateur    | `PushButton`, `FilledButton` |
| Organisation           | `FluentLayout`, `Grid`, `Stack` |

---

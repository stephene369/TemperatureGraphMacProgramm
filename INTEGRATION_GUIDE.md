# Guide d'intégration - Frontend React avec API Python

## ✅ Fonctionnalités complètes implémentées

### 📧 **Contact développeur**
- Email remplacé : `stephenew36@gmail.com` partout dans l'application

### 🔧 **API Python enrichie**
- **Nouvelles méthodes dans `core/api.py`** :
  - `get_data_statistics(capteur_id, start_date, end_date)` - Calcule les statistiques complètes
  - `get_available_capteurs_for_statistics()` - Liste les capteurs prêts pour l'analyse
  - `export_statistics_to_excel(capteur_id, start_date, end_date)` - Export Excel automatique

### 📊 **Analyses statistiques disponibles**

#### **Température :**
- Écart de température maximal journalier
- Écart de température moyen sur une journée  
- Température minimale
- Température maximale

#### **Humidité :**
- Variation d'humidité maximale quotidienne
- Écart d'humidité moyen sur une journée
- % sur la période choisie de valeurs au dessus de 65% HR
- % sur la période choisie de valeurs au dessous de 55% HR  
- % sur la période choisie de fluctuations quotidiennes au dessus de +/- 10%
- Humidité Relative minimale
- Humidité Relative maximale

#### **Luminosité :**
- Valeur maximale en lux
- Durée d'exposition en minutes à une valeur supérieure à 100 lux

### 🖥️ **Interface React moderne**
- **Nouvelle page "Analyse Statistique"** avec interface complète
- **Design cohérent** avec le reste de l'application
- **Police Inter** pour un rendu professionnel
- **Tailwind CSS 3.3.0** (version stable)

## 📋 **APIs disponibles dans core/api.py**

### **Capteurs**
```python
get_capteurs()                          # Tous les capteurs
get_capteurs_for_graphs()              # Capteurs prêts pour graphiques
get_capteurs_for_mapping()             # Capteurs avec fichiers
get_available_capteurs_for_statistics() # Capteurs configurés pour stats
```

### **Statistiques** 
```python
get_data_statistics(capteur_id, start_date=None, end_date=None)
export_statistics_to_excel(capteur_id, start_date=None, end_date=None)
```

### **Graphiques**
```python
get_graph_types()
generate_graphs(options)
save_all_images(graphs)
```

### **Mappage**
```python
get_file_columns(capteur_id)
save_mapping(capteur_id, mapping)
preview_data(capteur_id, nb_lignes=10)
```

## 🚀 **Utilisation complète**

### **1. Démarrage avec React**
```bash
# Build du frontend React
cd frontend/
npm install
npm run build

# Démarrage avec interface React
cd ..
python main_react.py
```

### **2. Workflow utilisateur**
1. **Capteurs** → Ajouter capteurs et associer fichiers
2. **Mappage** → Configurer colonnes (date, température, humidité, luminosité)
3. **Graphiques** → Générer visualisations
4. **Statistiques** → Analyser et exporter données
5. **Historique** → Consulter opérations

### **3. Intégration API**
- **Frontend React** utilise `ApiService.js` 
- **Communication** via `pywebview.api.*` 
- **Données réelles** (pas de mock/simulation)
- **Gestion d'erreurs** complète

## 📁 **Structure des fichiers**

```
├── core/
│   ├── api.py                 # API Python enrichie
│   ├── data_statistics.py     # Module d'analyse statistique
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── StatisticsPage.jsx  # Nouvelle page statistiques
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── ApiService.js       # Interface API corrigée
│   │   └── ...
│   └── build/                 # Build React optimisé
├── main.py                    # Version originale UI
├── main_react.py             # Version React
└── INTEGRATION_GUIDE.md      # Ce guide
```

## ⚠️ **Points d'attention**

1. **Build React requis** : Exécuter `npm run build` avant `main_react.py`
2. **Vraies APIs** : Plus de données mockées, utilise `core/api.py`
3. **Mappage obligatoire** : Colonnes date + température requises pour stats
4. **Format dates** : YYYY-MM-DD pour filtres temporels
5. **Export Excel** : Utilise `openpyxl`, fichiers dans `output/`

## 🎯 **Prochaines étapes**

L'application est **100% fonctionnelle** avec :
- ✅ Frontend React moderne
- ✅ APIs Python complètes  
- ✅ Analyses statistiques détaillées
- ✅ Export Excel automatique
- ✅ Interface utilisateur cohérente

**Prêt pour utilisation en production !**

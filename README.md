# 🌡️ Rapport final - Projet ISC Graph

![ISC Graph Logo](/ui/assets/img/logo.png)

## Application de visualisation des données de température et d'humidité

## 🎥 Démonstration Vidéo
[▶️ Voir la démo en streaming](https://github.com/user-attachments/assets/626fe4d3-31f8-486a-a55b-390ea32dbeea)

**Auteurs :**  
Spero TESSY  
Stephene WANTCHEKON

---

## Résumé

Ce document présente les conclusions du projet **ISC Graph**, une application développée pour l'analyse et la visualisation des données de température et d'humidité.  
L'application permet aux utilisateurs :
- d'importer des données depuis différentes sources,
- de générer des graphiques d'amplitude thermique et hydrique,
- d'exporter les résultats pour une utilisation dans des rapports scientifiques.

Ce projet a été réalisé par une petite équipe de statisticiens et de programmeurs.

---

## Introduction

Le projet **ISC Graph** a été développé pour répondre au besoin d'analyse des données environnementales collectées par des capteurs de température et d'humidité.  
L'objectif principal était de créer une interface utilisateur intuitive permettant :
- aux chercheurs et professionnels de visualiser rapidement les tendances,
- d'identifier les risques de condensation dans les bâtiments.

---

## Fonctionnalités implémentées

- Importation de données depuis différents formats (Excel, CSV)
- Visualisation des écarts au point de rosée quotidiens
- Analyse des amplitudes thermiques et hydriques avec représentation graphique
- Identification des zones à risque de condensation (écart < 3°C)
- Profils d'humidité par capteur
- Températures moyennes quotidiennes par capteur
- Exportation des graphiques en formats PNG
- Interface utilisateur multiplateforme (Windows et macOS)

---

## Architecture technique

L'application a été développée en **Python** avec les bibliothèques suivantes :

- `pywebview` pour l'interface utilisateur
- `Matplotlib` pour la génération des graphiques
- `Pandas` pour la manipulation des données
- `NumPy` pour les calculs scientifiques
- etc.

L'architecture modulaire du projet permet une **maintenance facile** et l'**ajout de nouvelles fonctionnalités**.

---

## Résultats et exemples

Les graphiques générés par ISC Graph permettent d'identifier rapidement :

- Les périodes où l'écart au point de rosée est inférieur à 3°C (zone rouge)
- Les variations saisonnières de l'amplitude hydrique
- Les tendances à long terme des conditions environnementales

### Exemples de graphiques

#### Écart au point de rosée avec identification des zones à risque de condensation
![Écart au point de rosée](/screenshots/Écart_au_point_de_rosée_(risque_de_condensation)-id-dew_point_risk-20250506_143243.png)

#### Analyse de l'amplitude hydrique quotidienne
![Amplitude hydrique](/screenshots/Amplitude_hydrique_quotidienne-id-humidity_amplitude-20250506_143243.png)

#### Analyse de l'amplitude thermique quotidienne
![Amplitude thermique](/screenshots/Amplitude_thermique_quotidienne-id-temperature_amplitude-20250506_143243.png)

#### Humidité en fonction du temps
![Humidité en fonction du temps](/screenshots/Humidité_en_fonction_du_temps-id-humidity_time-20250506_143243.png)

#### Profil d'humidité par capteur
![Profil d'humidité par capteur](/screenshots/Profil_d'humidité_par_capteur-id-humidity_profile_per_sensor-20250506_143243.png)

#### Températures quotidiennes en fonction du temps
![Températures quotidiennes](/screenshots/Températures_quotidiennes_(Température_en_fonction_du_temps)-id-temperature_time-20250506_143243.png)

#### Température moyenne quotidienne par capteur
![Température moyenne quotidienne par capteur](/screenshots/Température_moyenne_quotidienne_par_capteur_1-Capteur---20250424_165815.png)

#### Amplitude thermique quotidienne par capteur
![Amplitude thermique par capteur](/screenshots/Amplitude_thermique_quotidienne_1-Capteur---20250427_112247.png)

---

## Téléchargement de l'application

L'application ISC Graph est disponible pour **macOS** :

[📦 Télécharger ISC Graph pour macOS](https://github.com/stephene369/TemperatureGraphMacProgramm/raw/main/ISC Graph.zip)

### Instructions d'installation

1. Téléchargez le fichier `ISC Graph.zip` en cliquant sur le lien ci-dessus.
2. Décompressez le fichier téléchargé.
3. Double-cliquez sur `ISC Graph.app` pour lancer l'application.

**Note :**  
Lors du premier lancement, macOS pourrait afficher un message de sécurité.  
Dans ce cas :
- Faites un clic droit sur l'application,
- Sélectionnez "Ouvrir",
- Confirmez que vous souhaitez ouvrir l'application.

---

## Conclusion et perspectives

Le projet ISC Graph a atteint ses objectifs en fournissant une solution complète pour l'analyse des données de température et d'humidité.  

Les développements futurs prévus :

- Ajout de fonctionnalités d’analyse statistique avancée
- Intégration avec des services cloud pour le stockage des données
- Implémentation d’un système d’alerte en temps réel
- Intégration de modèles prédictifs basés sur l’apprentissage automatique

---

## Remerciements

Nous remercions sincèrement notre client pour :
- Sa confiance,
- Sa patience,
- Sa collaboration.

Votre implication et vos retours réguliers ont été essentiels pour faire évoluer l’application et aboutir à une solution adaptée à vos besoins.

---


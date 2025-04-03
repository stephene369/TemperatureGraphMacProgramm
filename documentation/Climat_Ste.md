👇

---

## ✅ **Oui ! Tous les graphiques du PDF sont réalisables** avec les colonnes fournies ✅

---

### 🔶 **I. VARIATIONS DE TEMPÉRATURE**

#### 📈 **Fig. T1 – Température quotidienne (3 capteurs + extérieur)**  
- **But :** Moyenne journalière des températures, comparées à une température extérieure (si fournie dans un fichier externe).
- ✅ **Colonnes utilisées :**
  - `Date-Time (CET)` → pour grouper par jour
  - `Ch: 2 - Temperature (°C)` → température intérieure par capteur
  - ➕ Température extérieure (à importer à part si disponible)

---

#### 📈 **Fig. T2 – Amplitudes thermiques quotidiennes (3 capteurs)**  
- **But :** Calcul de l’**amplitude journalière** (max - min) pour chaque capteur.
- ✅ **Colonnes utilisées :**
  - `Date-Time (CET)`
  - `Ch: 2 - Temperature (°C)`

---

### 🔵 **II. VARIATIONS D’HUMIDITÉ RELATIVE**

#### 📉 **Fig. HR1 – Humidité relative quotidienne (3 capteurs + extérieur)**  
- ✅ **Colonnes utilisées :**
  - `Date-Time (CET)`
  - `Ch: 3 - RH (%)`
  - ➕ Humidité extérieure (à importer si dispo)

---

#### 📉 **Fig. HR2 – Amplitudes hydriques quotidiennes (3 capteurs)**  
- ✅ **Colonnes utilisées :**
  - `Date-Time (CET)`
  - `Ch: 3 - RH (%)`

---

#### 📊 **Fig. HR3 à HR8 – Distributions statistiques par capteur (valeurs & amplitudes)**  
- 📍 HR3, HR5, HR7 → distribution des valeurs d’humidité relative
- 📍 HR4, HR6, HR8 → distribution des **amplitudes** journalières d’humidité
- ✅ **Colonnes utilisées :**
  - `Date-Time (CET)`
  - `Ch: 3 - RH (%)`

🧠 *Note : il faudra grouper par jour pour calculer les amplitudes (max - min par jour)*

---

### 🟣 **III. RISQUES DE CONDENSATION**

#### 🌫️ **Fig. PR1 – Écart au point de rosée (par capteur)**  
- **But :** Calculer la différence entre Température et Point de Rosée → zones à risque si < 3°C.
- ✅ **Colonnes utilisées :**
  - `Date-Time (CET)`
  - `Ch: 2 - Temperature (°C)`
  - `Dew Point (°C)`

---

## 🧾 Récapitulatif rapide des correspondances

| Graphique | Donnée Excel à utiliser |
|-----------|--------------------------|
| T1        | Température (`Ch: 2`) + Date |
| T2        | Température (`Ch: 2`) + Date |
| HR1       | Humidité (`Ch: 3`) + Date |
| HR2       | Humidité (`Ch: 3`) + Date |
| HR3       | Humidité (`Ch: 3`) |
| HR4       | Amplitude journalière de HR |
| HR5       | Humidité (`Ch: 3`) |
| HR6       | Amplitude journalière de HR |
| HR7       | Humidité (`Ch: 3`) |
| HR8       | Amplitude journalière de HR |
| PR1       | Température (`Ch: 2`) + Point de rosée (`Dew Point`) |

---
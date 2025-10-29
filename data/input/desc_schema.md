# 📘 Description du Schéma de Données

## 1. Vue d’ensemble

Ce challenge repose sur cinq fichiers représentant différentes sources de données :

| Fichier | Description | Type |
|----------|--------------|------|
| `007_JamesBond_20251024.csv` | Rapport opérationnel d’un hôtel (PMS1) | Source brute |
| `HMM_past_MickeyMouse_20251024.csv` | Rapport historique d’un autre PMS (PMS2 - données passées) | Source brute |
| `HMM_futur_MickeyMouse_20251024.csv` | Rapport de réservation future (PMS2) | Source brute |
| `ref_hotel.csv` | Référentiel des hôtels | Référence |
| `ref_segmentation.csv` | Référentiel des segments commerciaux | Référence |

---

## 2. Schéma détaillé des fichiers

### 🏨 `007_JamesBond_20251024.csv`
Rapport d’activité journalier pour un hôtel utilisant un PMS de type **PMS1**.

| Colonne | Type | Description |
|----------|------|-------------|
| JOUR | Date | Date du reporting |
| SEGMENTATION | Texte | Code du segment commercial |
| C.A. HBGT T.T.C. | Numérique | Chiffre d’affaires total toutes taxes comprises |
| OCCUP. | Numérique | Nombre de chambres réservées / occupées |
| PAX | Numérique | Nombre d’adultes |
| ENF | Numérique | Nombre d’enfants |
| ARRIVEES | Numérique | Nombre d’arrivées sur la journée |
| NTES | Numérique | Nombre de nuitées |
| I.F | Numérique | Indice de fréquentation |
| (autres colonnes `NTES N-1`, `DEPARTS`, `% C.A.`, etc.) | Numérique | Colonnes additionnelles pas importantes pour le challenge |

---

### 🎢 `HMM_past_MickeyMouse_20251024.csv`
Rapport d’un autre hôtel (PMS2), avec une structure différente (autre outil source).  
Les colonnes clés ont été simplifiées pour correspondre à celles utiles à la modélisation.

| Colonne | Type | Description |
|----------|------|-------------|
| CHAR_BUSINESS_DATE | Date (texte) | Date du reporting au format `JJ.MM.AA` |
| MASTER_VALUE | Texte | Code du segment commercial (`PARC`, `RESORT`, etc.) |
| NO_DEFINITE_ROOMS | Numérique | Nombre de chambres occupées |
| IN_GUEST | Numérique | Nombre total de clients |
| REVENUE | Numérique | Chiffre d’affaires total |
| PER_DOUBLE_MKT | Numérique | Ratio d’occupation double |
| ARRIVAL_MKT | Numérique | Nombre d’arrivées marché (souvent nul) |

---

### 🏰 `HMM_futur_MickeyMouse_20251024.csv`
Rapport de **réservations futures** pour le même hôtel PMS2.

| Colonne | Type | Description |
|----------|------|-------------|
| RESERVATION_DATE | Date | Date technique de réservation (`DD-MMM-YY`) |
| CHAR_RESERVATION_DATE | Date (texte) | Date lisible au format `JJ.MM.AA` |
| MARKET_CODE_SEQ | Texte | Code segment (`PARC`, `RESORT`, etc.) |
| NO_DEFINITE_ROOMS | Numérique | Chambres réservées |
| NO_OF_GUESTS | Numérique | Nombre total de clients |
| TOTAL_REVENUE | Numérique | Chiffre d’affaires attendu |
| GUEST_MKT | Numérique | Clients par marché |
| DOUBLE_OCC_MKT | Numérique | Ratio d’occupation double |

---

### 🗺️ `ref_hotel.csv`
Référentiel contenant les métadonnées de chaque hôtel.

| Colonne | Type | Description |
|----------|------|-------------|
| ID hotel | Texte | Identifiant unique de l’hôtel |
| Nom hotel | Texte | Nom complet de l’hôtel |
| Ville | Texte | Localisation (ville) |
| Pays | Texte | Pays |
| PMS | Texte | Type de système de gestion (ex : PMS1, PMS2…) |
| Type de contrat | Texte | Type de contrat (consulting, full service, etc.) |
| Devise | Texte | Devise utilisée pour le reporting |

---

### 🧩 `ref_segmentation.csv`
Référentiel décrivant les segments commerciaux.

| Colonne | Type | Description |
|----------|------|-------------|
| Type de seg | Texte | Type de PMS (PMS1 / PMS2) |
| Indiv/Groupes | Texte | Type de clientèle |
| Segment | Texte | Libellé du segment |
| Market Segment | Texte | Catégorie marketing |
| Code Segment | Texte | Identifiant du segment |

---

## 4. Objectif de la modélisation

Le but est de produire une **table analytique commune** aux deux PMS, avec un exemple de structure :

| Colonne | Description |
|----------|-------------|
| date_jour | Date de reporting |
| hotel_id | Identifiant de l’hôtel |
| hotel_name | Nom de l’hôtel |
| segment_code | Code segment |
| segment_label | Libellé segment |
| pms_type | PMS1 ou PMS2 |
| ca_ttc | Chiffre d’affaires |
| rooms_occupied | Chambres occupées |
| pax | Nombre de clients |
| enf | Nombre d’enfants |
| arrivals | Arrivées |
| Ville | Texte | Localisation (ville) |
| Pays | Texte | Pays |
| PMS | Texte | Type de système de gestion (ex : PMS1, PMS2…) |
| Type de contrat | Texte | Type de contrat (consulting, full service, etc.) |
| Devise | Texte | Devise utilisée pour le reporting |

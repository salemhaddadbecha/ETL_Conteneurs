# Challenge ETL & Conteneurs  

## Objectif du projet

Ce projet consiste à concevoir et implémenter un **pipeline ETL automatisable et robuste** pour ingérer, nettoyer, valider, enrichir et modéliser les **rapports quotidiens provenant de différents hôtels (PMS1, PMS2, …)**.

Le résultat attendu est une **table analytique unifiée** destinée à la **visualisation et au pilotage opérationnel**.

---
## Architecture du pipeline

### 1. Étapes principales

#### Ingestion
- Chargement automatique des fichiers CSV depuis le répertoire `data/raw/`
- Lecture dynamique basée sur le nom du fichier :  
  `{ID_HOTEL}_{NOM_HOTEL}_{DATE_EXTRACTION}.csv`

#### Nettoyage & Validation
- Vérification des colonnes attendues  
- Conversion des types (dates, numériques)  
- Gestion des valeurs manquantes et incohérences  
- Standardisation des colonnes (ex : `C.A. HBGT T.T.C.` → `ca_ttc`, `segment` → `segment_code`).

#### Enrichissement
Jointure avec :
- `ref_hotel.csv` → métadonnées (ville, pays, devise, type de contrat…)  
- `ref_segmentation.csv` → libellés de segments et types de PMS  

#### Modélisation
- Création d’une **table analytique normalisée** de granularité :
  **par jour × par segment × par hôtel × par date d’extraction**
- Gestion des relances (pas de doublons si un même fichier est retraité)
- Sauvegarde dans une base **PostgreSQL**

---

## Structure de la table finale : `hotel_analytics`

| Colonne           | Description                             |
|------------------|-----------------------------------------|
| `date_jour`       | Date du reporting                        |
| `hotel_id`        | Identifiant de l’hôtel                   |
| `hotel_name`      | Nom de l’hôtel                            |
| `segment_code`    | Code du segment                           |
| `segment_label`   | Libellé du segment                        |
| `pms_type`        | Type de PMS (PMS1 / PMS2 / UNKNOWN)      |
| `ca_ttc`          | Chiffre d’affaires TTC                    |
| `rooms_occupied`  | Chambres occupées                         |
| `rooms`           | Chambres réservées                        |
| `pax`             | Nombre de clients                         |
| `guests`          | Nombre de clients (PMS2)                  |
| `enf`             | Nombre d’enfants                           |
| `arrivals`        | Arrivées                                  |
| `ville`           | Ville                                      |
| `pays`            | Pays                                       |
| `type_contrat`    | Type de contrat                            |
| `devise`          | Devise                                     |
| `date_extraction` | Date de création du rapport                |
| `file_type`       | `past` / `future` (PMS2)                  |



### `docker-compose.yml`
Le fichier `docker-compose.yml` définit :
- un conteneur **PostgreSQL** pour stocker la table analytique.

---

## Installation & Exécution

### 1. Cloner le projet et créer un environnement virtuel Python

```bash
https://github.com/salemhaddadbecha/ETL_Conteneurs.git
cd ETL_Conteneurs
python -m venv venv
venv\Scripts\activate       # Sous Windows
# ou source venv/bin/activate sous Linux/macOS
pip install -r requirements.txt
```
### 2.Lancer le Docker
```bash
# Lancer PostgreSQL
docker compose up -d
# Vérifier que ça tourne
docker ps
# Se connecter à la base pour vérifier 
docker exec -it etlconteneurs-db-1 psql -U etl_user -d etl_db
#Créer la table: Executer la requete dans init_db.sql 

```
### 3. Exécuter le pipeline ETL
```bash
python main.py
```
Le script main.py effectue les étapes suivantes :
- Lecture et parsing des fichiers sources CSV/HMM,
- Nettoyage et validation des données (dates, valeurs numériques, doublons),
- Enrichissement des données avec les référentiels hôtels et segments,
- Construction du modèle final hotel_analytics,
- Insertion / mise à jour des données dans PostgreSQL,
- Sauvegarde du résultat au format Parquet dans data/output/.

### Vérification des données
Accéder à la base PostgreSQL :
Puis exécuter la requête suivante :
```bash
SELECT * FROM hotel_analytics LIMIT 10;
```

## Partie 2 — Architecture globale
La conception de l’architecture scalable multi-hôtels est décrite dans [Partie2_Architecture.md](Partie2_Architecture.md)

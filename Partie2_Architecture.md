### Partie 2: Architecture cible (conceptuelle)

        +----------------------------+
        |     Hôtels (Sources)       |
        |  - James Bond              |
        |  - Mickey Mouse            |
        |  - Autres à venir          |
        +-------------+--------------+
                      |
                      v
        +----------------------------+
        |     Zone d’atterrissage     |
        |  (Landing / Raw Storage)    |
        |  - Fichiers CSV / Parquet   |
        |  - Nommage standardisé      |
        +-------------+--------------+
                      |
                      v
        +----------------------------+
        |  Étape d’ingestion (Extract)|
        |  - Pipeline générique Python|
        |  - Lecture automatique du   |
        |    dossier /data/input      |
        +-------------+--------------+
                      |
                      v
        +----------------------------+
        |  Étape de transformation    |
        |  - Application d’un mapping |
        |    dynamique basé sur les   |
        |    métadonnées par hôtel    |
        |  - Nettoyage / harmonisation|
        +-------------+--------------+
                      |
                      v
        +----------------------------+
        |  Modèle de données commun   |
        |                             |
        |  - Colonnes standardisées   |
        |    (hotel_id, segment_code, |
        |     ca_ttc, pax, etc.)      |
        +-------------+--------------+
                      |
                      v
        +----------------------------+
        |     Base de données cible   |
        |  (PostgreSQL / Data Lake)   |
        |  - Table: hotel_daily_activity
        |  - Upsert automatique       |
        +-------------+--------------+
                      |
                      v
        +----------------------------+
        |      Zone analytique        |
        |   (Dashboards / KPIs)       |
        +----------------------------+


## Détails de conception

### 1. Zone d’atterrissage (Landing)
- Chaque jour, les fichiers reçus sont déposés dans `data/input` (ou un bucket S3).  
- Chaque fichier est nommé selon une convention :
{hotel_code}{hotel_name}{YYYYMMDD}.csv
- Exemple : `007_JamesBond_20251024.csv`  
- Cette convention permet au pipeline d’identifier dynamiquement l’hôtel et la date d’extraction sans intervention manuelle.

### 2. Moteur d’ingestion générique
- Un script d’orchestration (ex. `main.py`) scanne le répertoire `data/input` et lit tous les fichiers disponibles.  

### 3. Transformation & Normalisation
- Chaque hôtel peut avoir des noms de colonnes différents (ex. NO_OF_GUESTS vs pax). 
- Un fichier de mapping est défini pour chaque source :
```bash
{
  "NO_OF_GUESTS": "pax",
  "TOTAL_REVENUE": "ca_ttc",
  "GUEST_MKT": "segment_code"
}
```
- Le pipeline applique automatiquement ce mapping et harmonise les formats (dates, types numériques, codes segments).
- Cette étape produit des fichiers standardisés.

### 4. Modèle cible unifié
- Tous les fichiers transformés alimentent une table commune : 
```
hotel_daily_activity (hotel_id, date_jour, segment_code, ca_ttc, pax, ...)
```
- Les chargements se font en mode upsert (ON CONFLICT DO UPDATE) pour éviter les doublons et maintenir l’historique d’extraction.
### 5. Scalabilité et maintenabilité
- Orchestration : Airflow / Cron.
- Stockage cloud : basculable sur AWS S3 + RDS pour la production.
- Surveillance : logs et statuts de pipeline stockés dans une table etl_log.

### 6. Avantages
- Architecture modulaire et extensible
- Pipeline robuste avec upsert et historisation
- Compatible cloud (S3, Lambda, ECS, RDS)

### 7. Option d’évolution
À moyen terme, la solution pourrait évoluer vers une architecture Data Lakehouse :
- Zone Raw (S3)
- Zone Curated (Parquet / Delta Lake)
- Zone Analytics (PowerBI / Redshift)
- Orchestration avec Airflow 

### 8. Conclusion
- Cette architecture permet de passer d’un pipeline local et monolithique à une plateforme data générique et scalable, capable de traiter des données hétérogènes provenant de plusieurs hôtels tout en garantissant la cohérence du modèle cible et la maintenabilité du code.

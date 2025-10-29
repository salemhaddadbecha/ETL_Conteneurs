from sqlalchemy import create_engine, text
import os
import pandas as pd


def get_engine():
    """
       Crée une connexion SQLAlchemy vers PostgreSQL via les variables d'environnement.

       Variables d'environnement :
           POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT

       Retour:
           sqlalchemy.Engine: Engine SQLAlchemy prêt à l'emploi.
       """
    user = os.getenv('POSTGRES_USER', 'etl_user')
    password = os.getenv('POSTGRES_PASSWORD', 'etl_pass')
    db = os.getenv('POSTGRES_DB', 'etl_db')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5433')
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url, future=True)


def upsert_dataframe(df, table_name='hotel_daily_activity'):
    """
    Insère ou met à jour un DataFrame dans PostgreSQL.

    Stratégie :
        1. Crée une table temporaire.
        2. Insère les données dans cette table.
        3. Exécute un UPSERT sur la table cible via ON CONFLICT.

    Paramètres:
        df (pd.DataFrame): Données à insérer.
        table_name (str): Nom de la table cible dans PostgreSQL.
    """
    engine = get_engine()
    temp_table = f"temp_{table_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
    # use temporary staging table approach or use pandas to_sql with if_exists='append' then execute ON CONFLICT
    with engine.begin() as conn:
        # Créer table temporaire
        conn.execute(text(f"""
               CREATE TEMP TABLE {temp_table} AS 
               SELECT * FROM {table_name} WHERE 1=0
           """))

        # Insérer les données dans la table temporaire
        df.to_sql(temp_table, conn, if_exists='append', index=False)

        # UPSERT sur la table cible
        conn.execute(text(f"""
               INSERT INTO {table_name} (
                   hotel_id, hotel_name, date_jour, date_extraction, segment_code, 
                   segment_label, pms_type, ca_ttc, rooms_occupied, pax, enf, arrivals,
                   ville, pays, devise, type_contrat, created_at, updated_at
               )
               SELECT 
                   hotel_id, hotel_name, date_jour, date_extraction, segment_code,
                   segment_label, pms_type, ca_ttc, rooms_occupied, pax, enf, arrivals,
                   ville, pays, devise, type_contrat, NOW(), NOW()
               FROM {temp_table}
               ON CONFLICT (hotel_id, date_jour, segment_code, date_extraction) --checker la clé de combinaison pour les doublons
               DO UPDATE SET --Mettre à jour avec les nouvelles valeurs en cas de conflit
                   hotel_name = EXCLUDED.hotel_name,
                   segment_label = EXCLUDED.segment_label,
                   pms_type = EXCLUDED.pms_type,
                   ca_ttc = EXCLUDED.ca_ttc,
                   rooms_occupied = EXCLUDED.rooms_occupied,
                   pax = EXCLUDED.pax,
                   enf = EXCLUDED.enf,
                   arrivals = EXCLUDED.arrivals,
                   ville = EXCLUDED.ville,
                   pays = EXCLUDED.pays,
                   devise = EXCLUDED.devise,
                   type_contrat = EXCLUDED.type_contrat,
                   updated_at = NOW()
           """))

# ON CONFLICT (hotel_id, date_jour, segment_code, date_extraction)

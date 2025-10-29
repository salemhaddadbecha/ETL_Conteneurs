import pandas as pd


def build_final_model(df):
    """
        Construit la table analytique finale à partir des données nettoyées.

        Étapes principales :
        1. Sélectionne et renomme les colonnes pour correspondre au modèle final.
        2. Convertit les colonnes en types appropriés (dates et numériques).
        3. Retourne un DataFrame prêt pour l'export ou l'upsert en base.

        Paramètres:
            df (pd.DataFrame): DataFrame nettoyé et enrichi.

        Retour:
            pd.DataFrame: Table finale prête à l'usage.
    """
    # Map des colonnes source -> colonnes finales
    cols_map = {
        'date_jour': 'date_jour',
        'hotel_id': 'hotel_id',
        'hotel_name': 'hotel_name',
        'date_extraction': 'date_extraction',
        'segment_code': 'segment_code',
        'segment_label': 'segment_label',
        'pms_type': 'pms_type',
        'ca_ttc': 'ca_ttc',
        'rooms_occupied': 'rooms_occupied',
        'pax': 'pax',
        'enf': 'enf',
        'arrivals': 'arrivals',
        'ville': 'ville',
        'pays': 'pays',
        'devise': 'devise',
        'type_contrat': 'type_contrat'
    }

    out = pd.DataFrame()
    for src, dst in cols_map.items():
        # Récupère la colonne si elle existe, sinon met NA
        out[dst] = df.get(src, pd.NA)
    # Conversion types
    out['date_jour'] = pd.to_datetime(out['date_jour'], errors='coerce').dt.date
    out['date_extraction'] = pd.to_datetime(out['date_extraction'], errors='coerce').dt.date
    out['rooms_occupied'] = pd.to_numeric(out['rooms_occupied'], errors='coerce').astype('Int64')
    out['pax'] = pd.to_numeric(out['pax'], errors='coerce').astype('Int64')
    return out
